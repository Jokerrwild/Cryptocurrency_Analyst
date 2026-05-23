from __future__ import annotations

"""Regulatory overlay for Bayesian regime scoring.

Provides a small bias modifier per asset based on the current regulatory environment.
Positive bias tilts toward bullish regimes; negative tilts bearish.
This is updated manually as the regulatory landscape evolves.
"""

# Format: { asset_label: { "bias": float, "notes": str } }
# bias range: [-0.5, 0.5]. Keep it small; it supplements, not overrides.
_REGULATORY_DATA: dict[str, dict] = {
    "BTC": {
        "bias": 0.10,
        "notes": "Bitcoin ETF approvals and growing institutional acceptance provide mild bullish regulatory tailwind.",
    },
    "ETH": {
        "bias": 0.05,
        "notes": "Ethereum ETF discussions ongoing. Slightly positive but uncertain.",
    },
    "SOL": {
        "bias": -0.05,
        "notes": "SOL listed as security in certain SEC filings. Mild headwind.",
    },
    "XRP": {
        "bias": 0.15,
        "notes": "Ripple partial legal victory vs SEC. Positive regulatory clarity for XRP.",
    },
    "DOGE": {
        "bias": 0.0,
        "notes": "No significant regulatory activity. Neutral.",
    },
}

_DEFAULT = {"bias": 0.0, "notes": "No regulatory data available for this asset."}


def get_regulatory_scores(asset_label: str) -> dict:
    """Return regulatory bias and notes for a given asset."""
    return _REGULATORY_DATA.get(asset_label.upper(), _DEFAULT)


def get_all_regulatory_notes() -> list[str]:
    """Return all regulatory notes as a list of strings for report injection."""
    lines = []
    for label, data in _REGULATORY_DATA.items():
        bias_str = f"+{data['bias']:.2f}" if data['bias'] >= 0 else f"{data['bias']:.2f}"
        lines.append(f"[{label}] Regulatory bias: {bias_str} — {data['notes']}")
    return lines
