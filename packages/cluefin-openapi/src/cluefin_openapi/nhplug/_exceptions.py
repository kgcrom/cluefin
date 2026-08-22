"""Custom exceptions for NH PLUG API client."""

from typing import Any, Dict, Optional


class NHPlugAPIError(Exception):
    """Base exception for all NH PLUG API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
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


class NHPlugAuthenticationError(NHPlugAPIError):
    """Raised when authentication fails (401 Unauthorized)."""

    pass


class NHPlugAuthorizationError(NHPlugAPIError):
    """Raised when authorization fails (403 Forbidden)."""

    pass


class NHPlugRateLimitError(NHPlugAPIError):
    """Raised when rate limit is exceeded (429 Too Many Requests).

    NH guidance: retry 429 with the SAME token — re-issuing a token on 429
    triggers security alerts on the account.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class NHPlugValidationError(NHPlugAPIError):
    """Raised when request validation fails (400 Bad Request)."""

    pass


class NHPlugServerError(NHPlugAPIError):
    """Raised when server returns 5xx errors."""

    pass


class NHPlugNetworkError(NHPlugAPIError):
    """Raised when network-related errors occur."""

    pass


class NHPlugTimeoutError(NHPlugAPIError):
    """Raised when request times out."""

    pass
