"""Cluefin Kiwoom API Client Package."""

from ._auth import Auth
from ._client import Client
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
]


def hello() -> str:
    return "Hello from cluefin-kiwoom!"
