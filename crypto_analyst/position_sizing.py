from __future__ import annotations

"""Half-Kelly Criterion position sizing.

Rule: f* = (b*p - q) / b  where:
  p = win probability (posterior regime probability)
  q = 1 - p (loss probability)
  b = net odds (risk/reward ratio, default 2.0 = 2:1 R/R)
Half-Kelly: f = f* / 2  (reduces variance, standard practice)

The output is capped at MAX_POSITION_PCT to prevent overallocation.
"""

MAX_POSITION_PCT = 25.0   # Never suggest more than 25% of portfolio
MIN_POSITION_PCT = 0.0    # Below this threshold = no allocation recommended
DEFAULT_RR = 2.0          # Default risk/reward ratio
KELLY_FRACTION = 0.5      # Half-Kelly divisor

# Minimum win probability before any allocation is recommended
MIN_WIN_PROB_THRESHOLD = 0.55


def half_kelly(
    win_probability: float,
    risk_reward_ratio: float = DEFAULT_RR,
) -> float:
    """Calculate the Half-Kelly fraction.

    Args:
        win_probability: Posterior probability of a favorable outcome (0.0-1.0).
        risk_reward_ratio: Net reward per unit risked (e.g. 2.0 = 2:1).

    Returns:
        Allocation fraction in [0.0, 1.0]. 0.0 if Kelly is negative.
    """
    p = max(0.0, min(1.0, win_probability))
    q = 1.0 - p
    b = max(0.01, risk_reward_ratio)  # avoid division by zero

    full_kelly = (b * p - q) / b
    half = full_kelly * KELLY_FRACTION
    return max(0.0, half)  # floor at 0 (never short via Kelly)


def suggest_allocation(
    win_probability: float,
    risk_reward_ratio: float = DEFAULT_RR,
    leading_regime: str = "",
    target_asset: str = "BTC",
) -> tuple[float, float, str]:
    """Return (kelly_fraction, suggested_pct, rationale).

    The suggested_pct is the portfolio percentage to allocate.
    Returns 0% with rationale if probability is below threshold.
    """
    if win_probability < MIN_WIN_PROB_THRESHOLD:
        return (
            0.0,
            0.0,
            f"Win probability {win_probability:.1%} is below the minimum threshold "
            f"({MIN_WIN_PROB_THRESHOLD:.0%}) for allocation. HOLD — no new position.",
        )

    kelly = half_kelly(win_probability, risk_reward_ratio)
    suggested_pct = min(kelly * 100, MAX_POSITION_PCT)

    rationale = (
        f"Half-Kelly with p={win_probability:.1%}, b={risk_reward_ratio:.1f}:1 R/R "
        f"yields f*={kelly:.3f}. Suggested allocation: {suggested_pct:.1f}% of portfolio "
        f"into {target_asset}. Regime: {leading_regime}. "
        f"This is an educational sizing estimate — final decision rests with the human."
    )

    return kelly, suggested_pct, rationale


def cross_asset_momentum_rank(
    momentum_scores: dict[str, float],
) -> str:
    """Select the highest-momentum asset from a dict of {label: score}.

    Returns the label of the asset with the highest positive momentum score.
    Falls back to 'BTC' if all scores are non-positive.
    """
    if not momentum_scores:
        return "BTC"
    best = max(momentum_scores, key=lambda k: momentum_scores[k])
    if momentum_scores[best] <= 0:
        return "BTC"  # no positive momentum anywhere
    return best
