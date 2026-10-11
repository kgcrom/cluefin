"""SEC EDGAR API Exception classes."""

from typing import Any, Dict, Optional


class SecAPIError(Exception):
    """Base exception class for SEC EDGAR API errors."""

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
        if self.status_code:
            return f"SEC API Error [{self.status_code}]: {self.message}"
        return f"SEC API Error: {self.message}"


class SecAuthorizationError(SecAPIError):
    """Exception raised for 403 responses.

    SEC answers 403 both to requests without a declared User-Agent and to clients
    that exceeded the fair-access rate, so retrying does not help.
    """

    def __init__(
        self,
        message: str = "Access forbidden",
        status_code: int = 403,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class SecNotFoundError(SecAPIError):
    """Exception raised for 404 responses (unknown CIK, concept, frame or file)."""

    def __init__(
        self,
        message: str = "Not found",
        status_code: int = 404,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class SecClientError(SecAPIError):
    """Exception raised for other 4xx client errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class SecServerError(SecAPIError):
    """Exception raised for 5xx server errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class SecRateLimitError(SecAPIError):
    """Exception raised for 429 rate limit errors or rate limit timeout."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = 429,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
        self.retry_after = retry_after


class SecTimeoutError(SecAPIError):
    """Exception raised for request timeout errors."""

    def __init__(
        self,
        message: str = "Request timeout",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)


class SecNetworkError(SecAPIError):
    """Exception raised for network connection errors."""

    def __init__(
        self,
        message: str = "Network connection failed",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data, request_context)
