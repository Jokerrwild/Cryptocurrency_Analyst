from __future__ import annotations

import math
from typing import Any

from .indicators import momentum_score, trend_score, volatility_score, volume_score
from .models import AnalysisResult, MarketSnapshot, PositionSizing, RegimeProbability
from .position_sizing import cross_asset_momentum_rank, suggest_allocation
from .regulatory import get_regulatory_scores
from .time_utils import utc_now_str

REGIMES = [
    "Bullish accumulation",
    "Bullish continuation",
    "Neutral consolidation",
    "Bearish distribution",
    "Bearish continuation",
    "High-volatility transition",
    "Macro-driven risk-off",
]


def softmax(scores: dict[str, float]) -> dict[str, float]:
    vals = list(scores.values())
    max_v = max(vals)
    exps = {k: math.exp(v - max_v) for k, v in scores.items()}
    total = sum(exps.values())
    return {k: v / total for k, v in exps.items()}


def _macro_support(snapshot: MarketSnapshot) -> float:
    """Derive macro support signal from SPY/QQQ trend vs DXY."""
    spy = next((s for s in snapshot.macro if s.label == "SPY"), None)
    qqq = next((s for s in snapshot.macro if s.label == "QQQ"), None)
    dxy = next((s for s in snapshot.macro if s.label == "DXY"), None)
    equity_signal = 0.0
    if spy and len(spy.closes) >= 2:
        equity_signal += (spy.closes[-1] - spy.closes[-2]) / (spy.closes[-2] or 1)
    if qqq and len(qqq.closes) >= 2:
        equity_signal += (qqq.closes[-1] - qqq.closes[-2]) / (qqq.closes[-2] or 1)
    equity_signal = max(-1.0, min(1.0, equity_signal * 10))
    dxy_drag = 0.0
    if dxy and len(dxy.closes) >= 2:
        dxy_drag = -1 * max(-0.5, min(0.5, (dxy.closes[-1] - dxy.closes[-2]) / (dxy.closes[-2] or 1) * 10))
    return max(-1.0, min(1.0, equity_signal + dxy_drag))


def analyze_snapshot(
    snapshot: MarketSnapshot,
    cfg: dict[str, Any],
) -> AnalysisResult:
    """Core Bayesian analysis. Returns a fully populated AnalysisResult."""
    base_label = cfg.get("base_asset", "BTC")
    base_series = next(
        (s for s in snapshot.crypto if s.label == base_label),
        snapshot.crypto[0] if snapshot.crypto else None,
    )

    # --- Compute signals ---
    trend = trend_score(base_series) if base_series else 0.0
    momentum = momentum_score(base_series) if base_series else 0.0
    volatility = volatility_score(base_series) if base_series else 0.0
    volume = volume_score(base_series) if base_series else 0.5
    macro = _macro_support(snapshot)

    # Volume invalidation: low volume weakens trend signals
    vol_weight = 0.5 + 0.5 * volume  # [0.5, 1.0]

    # Regulatory overlay
    reg_scores = get_regulatory_scores(base_label)
    reg_bias = reg_scores.get("bias", 0.0)

    # --- Regime scoring ---
    raw: dict[str, float] = {r: 0.0 for r in REGIMES}
    raw["Bullish accumulation"] = (
        1.2 * max(0, trend) + 1.0 * max(0, momentum) + 0.8 * max(0, macro)
        - 0.4 * volatility + 0.5 * volume + reg_bias
    ) * vol_weight
    raw["Bullish continuation"] = (
        1.4 * max(0, trend) + 1.2 * max(0, momentum) + 0.8 * macro
        - 0.35 * volatility + 0.4 * volume
    ) * vol_weight
    raw["Neutral consolidation"] = (
        0.8 - abs(trend) * 0.8 - abs(momentum) * 0.6 + 0.3
    )
    raw["Bearish distribution"] = (
        1.2 * max(0, -trend) + 1.0 * max(0, -momentum) - 0.8 * max(0, macro)
        + 0.4 * volatility - 0.5 * volume - reg_bias
    ) * vol_weight
    raw["Bearish continuation"] = (
        1.4 * max(0, -trend) + 1.2 * max(0, -momentum) - 0.8 * macro
        + 0.35 * volatility - 0.4 * volume
    ) * vol_weight
    raw["High-volatility transition"] = (
        1.5 * volatility + 0.3 * abs(momentum) + 0.2 * abs(trend)
    )
    raw["Macro-driven risk-off"] = (
        1.3 * max(0, -macro) + 0.4 * volatility + 0.3 * max(0, -trend)
    )

    probs = softmax(raw)
    leading = max(probs, key=lambda k: probs[k])
    leading_prob = probs[leading]

    # Confidence score: gap to second place, data coverage, signal coherence
    sorted_probs = sorted(probs.values(), reverse=True)
    gap = sorted_probs[0] - sorted_probs[1] if len(sorted_probs) > 1 else 0.0
    data_coverage = min(1.0, (len(base_series.closes) if base_series else 0) / 50)
    coherence = 1.0 - abs(trend - momentum) / 2
    confidence_score = min(1.0, gap * 3 * data_coverage * coherence)
    confidence_label = "High" if confidence_score > 0.6 else ("Medium" if confidence_score > 0.3 else "Low")

    regime_probabilities = [
        RegimeProbability(
            regime=r,
            probability=round(p, 4),
            confidence=confidence_label if r == leading else "Low",
        )
        for r, p in sorted(probs.items(), key=lambda x: -x[1])
    ]

    # --- Position sizing (Kelly) ---
    momentum_scores = {
        s.label: momentum_score(s)
        for s in snapshot.crypto
        if s.closes
    }
    target_asset = cross_asset_momentum_rank(momentum_scores)
    kelly_fraction, suggested_pct, ps_rationale = suggest_allocation(
        win_probability=leading_prob,
        leading_regime=leading,
        target_asset=target_asset,
    )
    pos_sizing = PositionSizing(
        target_asset=target_asset,
        win_probability=leading_prob,
        kelly_fraction=kelly_fraction,
        suggested_pct=suggested_pct,
        risk_reward_ratio=2.0,
        rationale=ps_rationale,
    )

    # --- Evidence builders ---
    quant_evidence = _build_quant_evidence(base_series, trend, momentum, volatility, volume, macro, momentum_scores)
    qual_evidence = ["Qualitative context: news feed and regulatory sentiment not yet injected. Use notes parameter."]
    interpretation = _build_interpretation(leading, leading_prob, confidence_label, trend, momentum)
    invalidation = _build_invalidation(leading, trend, momentum)
    decision_support = _build_decision_support(leading, pos_sizing)
    monitor_next = [
        f"{base_label} close relative to EMA-50",
        "DXY trend continuation or reversal",
        "SPY/QQQ session volume",
        "Regulatory headlines for tracked assets",
        "Regime velocity (probability shift >5% vs last interval)",
    ]

    return AnalysisResult(
        snapshot=snapshot,
        regime_probabilities=regime_probabilities,
        leading_regime=leading,
        confidence_score=round(confidence_score, 4),
        position_sizing=pos_sizing,
        quantitative_evidence=quant_evidence,
        qualitative_evidence=qual_evidence,
        interpretation=interpretation,
        invalidation_conditions=invalidation,
        decision_support=decision_support,
        monitor_next=monitor_next,
    )


def _build_quant_evidence(
    series, trend, momentum, volatility, volume, macro, momentum_scores
) -> list[str]:
    lines = []
    if series:
        lines.append(f"{series.label} latest close: ${series.latest_close:,.2f}" if series.latest_close else f"{series.label}: no price data")
    lines.append(f"Trend score: {trend:+.3f} (positive = above EMA-50)")
    lines.append(f"Momentum score: {momentum:+.3f} (EMA-12 vs EMA-26 spread)")
    lines.append(f"Volatility score: {volatility:.3f} (0=calm, 1=extreme)")
    lines.append(f"Volume score: {volume:.3f} (0.5=avg, 1.0=2x avg)")
    lines.append(f"Macro support: {macro:+.3f} (equity trend minus DXY drag)")
    for label, score in sorted(momentum_scores.items(), key=lambda x: -x[1]):
        lines.append(f"  Momentum [{label}]: {score:+.3f}")
    return lines


def _build_interpretation(regime, prob, confidence, trend, momentum) -> str:
    return (
        f"Leading regime is '{regime}' with posterior probability {prob:.1%} "
        f"(confidence: {confidence}). "
        f"Trend signal is {'positive' if trend > 0 else 'negative'} ({trend:+.2f}) "
        f"and momentum is {'building' if momentum > 0 else 'waning'} ({momentum:+.2f}). "
        f"Treat this as a probabilistic belief state, not a deterministic prediction."
    )


def _build_invalidation(regime, trend, momentum) -> list[str]:
    conds = []
    if "Bullish" in regime:
        conds.append("Trend flips negative (close drops below EMA-50)")
        conds.append("Momentum turns sharply negative over 2+ intervals")
        conds.append("Volume collapses below 50% of 20-period average")
    elif "Bearish" in regime:
        conds.append("Trend recovers above EMA-50 with volume confirmation")
        conds.append("Macro support turns positive (SPY/QQQ sustained recovery)")
    else:
        conds.append("Regime velocity exceeds 5% shift toward Bullish or Bearish")
        conds.append("Volume breakout above 1.5x average")
    return conds


def _build_decision_support(regime, pos_sizing: PositionSizing) -> str:
    return (
        f"Target asset: {pos_sizing.target_asset} (highest cross-asset momentum). "
        f"Suggested allocation: {pos_sizing.suggested_pct:.1f}% of portfolio (Half-Kelly). "
        f"Regime context: {regime}. "
        f"{pos_sizing.rationale}"
    )
