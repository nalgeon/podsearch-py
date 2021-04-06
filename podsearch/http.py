"""HTTP requests wrapper."""

from typing import Optional
import json
import urllib.request
import urllib.parse
from urllib.error import (
    HTTPError,
    URLError,
)


def get(url: str, params: Optional[dict] = None) -> dict:
    """Perform HTTP GET request and return response as JSON"""
    try:
        query_str = urllib.parse.urlencode(params or {})
        req = urllib.request.Request(f"{url}?{query_str}")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        raise Exception(f"HTTP error {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise Exception(f"Network error: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise Exception(f"Failed to parse response: {exc}") from exc
