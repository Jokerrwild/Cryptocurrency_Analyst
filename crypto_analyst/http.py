from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class FetchError(Exception):
    """Raised when an HTTP request fails or returns unexpected data."""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


def fetch_json(
    url: str,
    params: dict[str, Any] | None = None,
    timeout: int = 15,
) -> Any:
    """Fetch JSON from a URL. Raises FetchError on failure."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raise FetchError(f"HTTP {e.code} fetching {url}", status_code=e.code) from e
    except urllib.error.URLError as e:
        raise FetchError(f"URL error fetching {url}: {e.reason}") from e
    except Exception as e:
        raise FetchError(f"Unexpected error fetching {url}: {e}") from e
