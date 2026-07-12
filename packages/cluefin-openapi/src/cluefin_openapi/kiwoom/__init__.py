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
from ._overseas_condition_search import OverseasConditionSearch
from ._overseas_realtime import OverseasRealtime
from ._socket_client import KiwoomWebSocketClient, KiwoomWebSocketMessage

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
    "KiwoomWebSocketClient",
    "KiwoomWebSocketMessage",
    "OverseasConditionSearch",
    "OverseasRealtime",
    "error_type_for_code",
    "resolve_kiwoom_error",
]


def hello() -> str:
    return "Hello from cluefin-openapi/kiwoom!"
