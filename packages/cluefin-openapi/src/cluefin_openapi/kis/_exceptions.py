"""Custom exceptions for KIS API client."""

from typing import Any


class KISAPIError(Exception):
    """Base exception for all KIS API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        self.request_context = request_context or {}

    def __str__(self) -> str:
        base_msg = self.message
        if self.status_code:
            base_msg = f"[{self.status_code}] {base_msg}"
        return base_msg


class KISAuthenticationError(KISAPIError):
    """Raised when authentication fails (401 Unauthorized)."""

    pass


class KISAuthorizationError(KISAPIError):
    """Raised when authorization fails (403 Forbidden)."""

    pass


class KISRateLimitError(KISAPIError):
    """Raised when rate limit is exceeded (429 Too Many Requests)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
        retry_after: int | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class KISValidationError(KISAPIError):
    """Raised when request validation fails (400 Bad Request) or API response parsing fails.

    response_data contains the raw API response that caused the validation failure.
    """

    pass


class KISResponseError(KISAPIError, ValueError):
    """Raised when the HTTP call succeeds but the body says it failed (`rt_cd != "0"`).

    Also a ``ValueError`` because these errors were plain ``ValueError`` before; callers that catch
    ``ValueError`` keep working. ``response_data`` holds only ``rt_cd``/``msg_cd``/``msg1``.
    """

    pass


def raise_for_rt_cd(response_data: dict[str, Any]) -> None:
    """Raise ``KISResponseError`` when a KIS body reports failure (`rt_cd` other than ``"0"``)."""
    rt_cd = response_data.get("rt_cd")
    if rt_cd != "0":
        msg_cd = response_data.get("msg_cd", "")
        msg1 = response_data.get("msg1", "Unknown error")
        raise KISResponseError(
            f"KIS API Error [{msg_cd}]: {msg1} (rt_cd={rt_cd})",
            response_data={"rt_cd": rt_cd, "msg_cd": msg_cd, "msg1": msg1},
        )


class KISServerError(KISAPIError):
    """Raised when server error occurs (5xx status codes)."""

    pass


class KISNetworkError(KISAPIError):
    """Raised when network/connection errors occur."""

    pass


class KISTimeoutError(KISAPIError):
    """Raised when request timeout occurs."""

    pass
