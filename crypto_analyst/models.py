from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Candle:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class SeriesSummary:
    label: str
    closes: list[float] = field(default_factory=list)
    volumes: list[float] = field(default_factory=list)
    timestamps: list[int] = field(default_factory=list)

    @property
    def latest_close(self) -> float | None:
        return self.closes[-1] if self.closes else None

    @property
    def latest_volume(self) -> float | None:
        return self.volumes[-1] if self.volumes else None


@dataclass
class MarketSnapshot:
    crypto: list[SeriesSummary] = field(default_factory=list)
    macro: list[SeriesSummary] = field(default_factory=list)
    timestamp_utc: str = ""


@dataclass
class RegimeProbability:
    regime: str
    probability: float
    confidence: str  # "High" | "Medium" | "Low"


@dataclass
class PositionSizing:
    target_asset: str
    win_probability: float
    kelly_fraction: float   # Half-Kelly
    suggested_pct: float    # % of portfolio to allocate
    risk_reward_ratio: float
    rationale: str


@dataclass
class AnalysisResult:
    snapshot: MarketSnapshot
    regime_probabilities: list[RegimeProbability]
    leading_regime: str
    confidence_score: float
    position_sizing: PositionSizing | None
    quantitative_evidence: list[str]
    qualitative_evidence: list[str]
    interpretation: str
    invalidation_conditions: list[str]
    decision_support: str
    monitor_next: list[str]
    report_path: str = ""
    delivery_status: str = "pending"  # pending | success | failed
