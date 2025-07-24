"""KRX API Exception classes."""

from typing import Dict, Optional


class KrxAPIError(Exception):
    """Base exception class for KRX API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data

    def __str__(self):
        if self.status_code:
            return f"KRX API Error [{self.status_code}]: {self.message}"
        return f"KRX API Error: {self.message}"


class KrxAuthenticationError(KrxAPIError):
    """Exception raised for 401 authentication errors."""

    def __init__(
        self,
        message: str = "Authentication failed - invalid or expired token",
        status_code: int = 401,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message, status_code, response_data)


class KrxAuthorizationError(KrxAPIError):
    """Exception raised for 403 authorization errors."""

    def __init__(
        self,
        message: str = "Access forbidden - insufficient permissions",
        status_code: int = 403,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message, status_code, response_data)


class KrxClientError(KrxAPIError):
    """Exception raised for 4xx client errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message, status_code, response_data)


class KrxServerError(KrxAPIError):
    """Exception raised for 5xx server errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_data: Optional[Dict] = None,
    ):
        super().__init__(message, status_code, response_data)
