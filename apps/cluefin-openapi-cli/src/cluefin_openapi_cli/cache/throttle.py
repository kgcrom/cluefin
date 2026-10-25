"""Sequential KIS calls for bulk loads, retrying "too many requests per second" briefly.

KIS answers going over its per-second limit with HTTP 500 + `EGW00201`, not 429, and does
so at ~10% of calls even at the client's own 20 req/s. The client treats that as a server
error and sleeps 1s, 2s, … before retrying, which caps a bulk load at ~5 calls/s (measured
2026-10-18). Loaders open the client with ``max_retries=0`` and retry here after 0.1s,
which measured ~15 successful calls/s. One call at a time, never in parallel.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, TypeVar

__all__ = ["RATE_LIMIT_CODE", "is_rate_limited", "kis_call", "kis_error_code"]

RATE_LIMIT_CODE = "EGW00201"
# Other transient KIS failures seen during a bulk load (2026-10-18): a gateway routing error
# (HTTP 500), "please query again" (HTTP 500) and "SESSION FULL" (HTTP 200, rt_cd 9). They clear
# within a second or two.
_TRANSIENT_CODES = frozenset({"EGW00300", "EGW00316", "OPSQ1002"})
_PAUSE_SECONDS = 0.1
_TRANSIENT_PAUSE_SECONDS = 1.0
_MAX_ATTEMPTS = 30
_MAX_TRANSIENT_ATTEMPTS = 5

T = TypeVar("T")


def kis_error_code(exc: BaseException) -> str | None:
    """`msg_cd` of a KIS error: HTTP errors (KISServerError …) and body errors (KISResponseError) both carry it."""
    data = getattr(exc, "response_data", None)
    if isinstance(data, dict) and data.get("msg_cd"):
        return str(data["msg_cd"])
    return None


def is_rate_limited(exc: BaseException) -> bool:
    return kis_error_code(exc) == RATE_LIMIT_CODE


def kis_call(
    fn: Callable[..., T],
    *args: Any,
    sleep: Callable[[float], None] = time.sleep,
    max_attempts: int = _MAX_ATTEMPTS,
) -> T:
    """Call ``fn(*args)``; pause and retry on rate-limit and known transient codes, else propagate."""

    transient_attempts = 0
    for attempt in range(max_attempts):
        try:
            return fn(*args)
        except Exception as exc:
            code = kis_error_code(exc)
            if attempt == max_attempts - 1:
                raise
            if code == RATE_LIMIT_CODE:
                sleep(_PAUSE_SECONDS)
            elif code in _TRANSIENT_CODES and transient_attempts < _MAX_TRANSIENT_ATTEMPTS:
                transient_attempts += 1
                sleep(_TRANSIENT_PAUSE_SECONDS)
            else:
                raise
    raise AssertionError("unreachable")  # pragma: no cover
