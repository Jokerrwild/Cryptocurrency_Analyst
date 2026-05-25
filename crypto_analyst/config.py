from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "timezone": "America/New_York",
    "report_dir": "reports",
    "database_path": "crypto_analyst.db",
    "database_retention_days": 5,
    "base_asset": "BTC",
    "crypto_lookback_days": 5,
    "crypto_assets": [
        {"label": "BTC", "source": "coinbase", "product_id": "BTC-USD", "granularity_seconds": 3600},
        {"label": "ETH", "source": "coinbase", "product_id": "ETH-USD", "granularity_seconds": 3600},
        {"label": "SOL", "source": "coinbase", "product_id": "SOL-USD", "granularity_seconds": 3600},
        {"label": "XRP", "source": "coinbase", "product_id": "XRP-USD", "granularity_seconds": 3600},
        {"label": "ADA", "source": "coinbase", "product_id": "ADA-USD", "granularity_seconds": 3600},
        {"label": "ZEC", "source": "coinbase", "product_id": "ZEC-USD", "granularity_seconds": 3600},
    ],
    "macro_assets": [
        {"label": "SPY", "source": "yahoo", "symbol": "SPY", "range": "3mo", "interval": "1d", "interpretation": "risk_on_equity"},
        {"label": "QQQ", "source": "yahoo", "symbol": "QQQ", "range": "3mo", "interval": "1d", "interpretation": "risk_on_equity"},
        {"label": "DXY", "source": "yahoo", "symbol": "DX-Y.NYB", "range": "3mo", "interval": "1d", "interpretation": "risk_off_dollar"},
        {"label": "10Y", "source": "yahoo", "symbol": "^TNX", "range": "3mo", "interval": "1d", "interpretation": "risk_off_yield"},
    ],
    # Telegram delivery — set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in env or here
    "telegram": {
        "enabled": False,
        "bot_token": "",   # or set via env: TELEGRAM_BOT_TOKEN
        "chat_id": "",     # or set via env: TELEGRAM_CHAT_ID
        "retry_delay_seconds": 5,
    },
    # Execution schedule
    "schedule": {
        "interval_minutes": 60,
        "active_window": "08:00-21:00",   # EST only runs during this window
        "run_at_times": [],                # e.g. ["09:00", "12:00", "16:00"]
    },
}


def load_config(path: str = "config.json") -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_CONFIG)
    p = Path(path)
    if p.exists():
        with open(p) as f:
            overrides = json.load(f)
        cfg = _deep_merge(cfg, overrides)
    return cfg


def _deep_merge(base: dict, overrides: dict) -> dict:
    result = deepcopy(base)
    for k, v in overrides.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result
