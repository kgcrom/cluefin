"""DART API Exception classes."""

from typing import Any, Dict, Optional


class DartAPIError(Exception):
    """Base exception class for DART API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data

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
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data)


class DartAuthorizationError(DartAPIError):
    """Exception raised for 403 authorization errors."""

    def __init__(
        self,
        message: str = "Access forbidden - insufficient permissions",
        status_code: int = 403,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data)


class DartClientError(DartAPIError):
    """Exception raised for 4xx client errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data)


class DartServerError(DartAPIError):
    """Exception raised for 5xx server errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data)
