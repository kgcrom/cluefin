"""SEC EDGAR client (www.sec.gov, data.sec.gov).

SEC has no API key: every request declares its caller in the User-Agent header
("Name email@example.com"). See https://www.sec.gov/os/accessing-edgar-data
"""

from cluefin_openapi.sec._client import Client
from cluefin_openapi.sec._exceptions import (
    SecAPIError,
    SecAuthorizationError,
    SecClientError,
    SecNetworkError,
    SecNotFoundError,
    SecRateLimitError,
    SecServerError,
    SecTimeoutError,
)

__all__ = [
    "Client",
    "SecAPIError",
    "SecAuthorizationError",
    "SecClientError",
    "SecNetworkError",
    "SecNotFoundError",
    "SecRateLimitError",
    "SecServerError",
    "SecTimeoutError",
]
