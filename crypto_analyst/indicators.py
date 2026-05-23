from __future__ import annotations

import math
from statistics import mean, pstdev

from .models import Candle, SeriesSummary


def clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def pct_change(current: float, previous: float | None) -> float | None:
    if previous is None or previous == 0:
        return None
    return ((current - previous) / previous) * 100


def ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    smoothing = 2 / (period + 1)
    current = mean(values[:period])
    for value in values[period:]:
        current = (value * smoothing) + (current * (1 - smoothing))
    return current


def rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) <= period:
        return None
    gains: list[float] = []
    losses: list[float] = []
    for prev, curr in zip(values[-period - 1:-1], values[-period:]):
        change = curr - prev
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))
    avg_gain = mean(gains)
    avg_loss = mean(losses)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def momentum_score(series: SeriesSummary, fast: int = 12, slow: int = 26) -> float:
    """Normalized momentum: EMA(fast) - EMA(slow), clamped to [-1, 1]."""
    closes = series.closes
    if not closes or len(closes) < slow:
        return 0.0
    e_fast = ema(closes, fast)
    e_slow = ema(closes, slow)
    if e_fast is None or e_slow is None or e_slow == 0:
        return 0.0
    raw = (e_fast - e_slow) / e_slow
    return clamp(raw * 10, -1.0, 1.0)  # scale to [-1, 1]


def volatility_score(series: SeriesSummary, window: int = 20) -> float:
    """Rolling std of returns as a normalized volatility signal [0, 1]."""
    closes = series.closes[-window - 1:] if len(series.closes) > window else series.closes
    if len(closes) < 2:
        return 0.0
    returns = [(b - a) / a for a, b in zip(closes[:-1], closes[1:]) if a != 0]
    if not returns:
        return 0.0
    return clamp(pstdev(returns) * 10, 0.0, 1.0)


def volume_score(series: SeriesSummary, window: int = 20) -> float:
    """Compare latest volume to average: >1 means above-average volume."""
    vols = series.volumes
    if len(vols) < 2:
        return 0.5
    avg = mean(vols[-window:])
    if avg == 0:
        return 0.5
    ratio = vols[-1] / avg
    return clamp(ratio / 2, 0.0, 1.0)  # normalize: ratio of 2 = 1.0


def trend_score(series: SeriesSummary) -> float:
    """Simple close vs EMA-50 trend signal, clamped [-1, 1]."""
    closes = series.closes
    if len(closes) < 50:
        return 0.0
    e50 = ema(closes, 50)
    if e50 is None or e50 == 0:
        return 0.0
    raw = (closes[-1] - e50) / e50
    return clamp(raw * 10, -1.0, 1.0)
