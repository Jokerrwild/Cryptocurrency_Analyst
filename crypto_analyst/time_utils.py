from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def utc_now_str() -> str:
    return utc_now().strftime("%Y-%m-%d %H:%M UTC")


def resolve_timezone(tz_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(tz_name)
    except Exception:
        return ZoneInfo("America/New_York")


def local_now(tz_name: str = "America/New_York") -> datetime:
    return datetime.now(tz=resolve_timezone(tz_name))


def is_within_window(window: str, tz_name: str = "America/New_York") -> bool:
    """Return True if current local time is inside HH:MM-HH:MM window."""
    try:
        start_str, end_str = window.split("-")
        now = local_now(tz_name)
        start = now.replace(
            hour=int(start_str.split(":")[0]),
            minute=int(start_str.split(":")[1]),
            second=0, microsecond=0
        )
        end = now.replace(
            hour=int(end_str.split(":")[0]),
            minute=int(end_str.split(":")[1]),
            second=0, microsecond=0
        )
        return start <= now <= end
    except Exception:
        return True  # fail open


def report_timestamp(tz_name: str = "America/New_York") -> str:
    return local_now(tz_name).strftime("%Y%m%d_%H%M%S")
