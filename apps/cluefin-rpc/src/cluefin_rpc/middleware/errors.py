"""Map broker exceptions to JSON-RPC error codes."""

from __future__ import annotations

from typing import Any

from cluefin_rpc.middleware.auth import SessionNotInitialized
from cluefin_rpc.protocol import (
    AUTH_ERROR,
    BROKER_API_ERROR,
    INTERNAL_ERROR,
    INVALID_PARAMS,
    RATE_LIMIT_ERROR,
    SESSION_ERROR,
)


def map_exception_to_rpc_error(exc: Exception) -> tuple[int, str, Any]:
    """Map a Python exception to a (code, message, data) tuple for JSON-RPC error response."""
    exc_type = type(exc).__name__
    exc_msg = str(exc)

    # Session errors
    if isinstance(exc, SessionNotInitialized):
        return SESSION_ERROR, exc_msg, {"type": exc_type}

    # Import broker exceptions lazily to avoid hard dependency at module level
    try:
        from cluefin_openapi.kis._exceptions import KISAuthenticationError, KISRateLimitError
    except ImportError:
        KISAuthenticationError = type(None)
        KISRateLimitError = type(None)

    try:
        from cluefin_openapi.kiwoom._exceptions import KiwoomAuthenticationError, KiwoomRateLimitError
    except ImportError:
        KiwoomAuthenticationError = type(None)
        KiwoomRateLimitError = type(None)

    try:
        from cluefin_openapi.dart._exceptions import DartAuthenticationError, DartRateLimitError
    except ImportError:
        DartAuthenticationError = type(None)
        DartRateLimitError = type(None)

    # Auth errors -> -32001
    auth_errors = (KISAuthenticationError, KiwoomAuthenticationError, DartAuthenticationError)
    if isinstance(exc, auth_errors):
        return AUTH_ERROR, exc_msg, {"type": exc_type}

    # Rate limit errors -> -32002
    rate_limit_errors = (KISRateLimitError, KiwoomRateLimitError, DartRateLimitError)
    if isinstance(exc, rate_limit_errors):
        data: dict[str, Any] = {"type": exc_type}
        if hasattr(exc, "retry_after") and exc.retry_after is not None:
            data["retry_after"] = exc.retry_after
        return RATE_LIMIT_ERROR, exc_msg, data

    # Broker API errors -> -32003
    try:
        from cluefin_openapi.dart._exceptions import DartAPIError
        from cluefin_openapi.kis._exceptions import KISAPIError
        from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

        broker_errors = (KISAPIError, KiwoomAPIError, DartAPIError)
    except ImportError:
        broker_errors = ()

    if isinstance(exc, broker_errors):
        data = {"type": exc_type}
        if hasattr(exc, "status_code") and exc.status_code is not None:
            data["status_code"] = exc.status_code
        if hasattr(exc, "response_data") and exc.response_data is not None:
            data["response_data"] = exc.response_data
        return BROKER_API_ERROR, exc_msg, data

    # Validation errors -> -32602
    if isinstance(exc, (ValueError, TypeError)):
        return INVALID_PARAMS, exc_msg, {"type": exc_type}

    # Everything else -> -32603
    return INTERNAL_ERROR, exc_msg, {"type": exc_type}
