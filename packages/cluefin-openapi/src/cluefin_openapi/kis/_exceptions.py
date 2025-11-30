"""Custom exceptions for KIS API client."""

from typing import Any, Dict, Optional


class KISAPIError(Exception):
    """Base exception for all KIS API errors."""

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
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class KISValidationError(KISAPIError):
    """Raised when request validation fails (400 Bad Request)."""

    pass


class KISServerError(KISAPIError):
    """Raised when server error occurs (5xx status codes)."""

    pass


class KISNetworkError(KISAPIError):
    """Raised when network/connection errors occur."""

    pass


class KISTimeoutError(KISAPIError):
    """Raised when request timeout occurs."""

    pass
