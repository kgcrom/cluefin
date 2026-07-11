"""Cluefin Kiwoom API Client Package."""

from ._auth import Auth
from ._client import Client
from ._error_codes import KIWOOM_ERROR_CODES, error_type_for_code, resolve_kiwoom_error
from ._exceptions import (
    KiwoomAPIError,
    KiwoomAuthenticationError,
    KiwoomAuthorizationError,
    KiwoomNetworkError,
    KiwoomRateLimitError,
    KiwoomServerError,
    KiwoomTimeoutError,
    KiwoomValidationError,
)

__all__ = [
    "KIWOOM_ERROR_CODES",
    "Auth",
    "Client",
    "KiwoomAPIError",
    "KiwoomAuthenticationError",
    "KiwoomAuthorizationError",
    "KiwoomNetworkError",
    "KiwoomRateLimitError",
    "KiwoomServerError",
    "KiwoomTimeoutError",
    "KiwoomValidationError",
    "error_type_for_code",
    "resolve_kiwoom_error",
]


def hello() -> str:
    return "Hello from cluefin-openapi/kiwoom!"
