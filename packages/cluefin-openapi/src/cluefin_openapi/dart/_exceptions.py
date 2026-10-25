"""DART API Exception classes."""

from typing import Any


class DartAPIError(Exception):
    """Base exception class for DART API errors."""

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
        if self.status_code:
            return f"DART API Error [{self.status_code}]: {self.message}"
        return f"DART API Error: {self.message}"


class DartAuthenticationError(DartAPIError):
    """Exception raised for 401 authentication errors."""

    def __init__(
        self,
        message: str = "Authentication failed - invalid or expired token",
        status_code: int = 401,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class DartAuthorizationError(DartAPIError):
    """Exception raised for 403 authorization errors."""

    def __init__(
        self,
        message: str = "Access forbidden - insufficient permissions",
        status_code: int = 403,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class DartClientError(DartAPIError):
    """Exception raised for 4xx client errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class DartServerError(DartAPIError):
    """Exception raised for 5xx server errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class DartRateLimitError(DartAPIError):
    """Exception raised for 429 rate limit errors or rate limit timeout."""

    def __init__(
        self,
        message: str,
        status_code: int | None = 429,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
        retry_after: int | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class DartTimeoutError(DartAPIError):
    """Exception raised for request timeout errors."""

    def __init__(
        self,
        message: str = "Request timeout",
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class DartNetworkError(DartAPIError):
    """Exception raised for network connection errors."""

    def __init__(
        self,
        message: str = "Network connection failed",
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
        request_context: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
