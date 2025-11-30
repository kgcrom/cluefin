import time
from typing import Dict, Optional

import requests

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    DartAPIError,
    DartAuthenticationError,
    DartAuthorizationError,
    DartClientError,
    DartNetworkError,
    DartRateLimitError,
    DartServerError,
    DartTimeoutError,
)


class Client(object):
    def __init__(
        self,
        auth_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 10,
    ):
        self.auth_key = auth_key
        self.base_url = "https://opendart.fss.or.kr"
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "cluefin-openapi/1.0",
            }
        )

        # Initialize rate limiter
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

    @property
    def major_shareholder_disclosure(self):
        from ._major_shareholder_disclosure import MajorShareholderDisclosure

        return MajorShareholderDisclosure(self)

    @property
    def public_disclosure(self):
        from ._public_disclosure import PublicDisclosure

        return PublicDisclosure(self)

    @property
    def periodic_report_key_information(self):
        from ._periodic_report_key_information import PeriodicReportKeyInformation

        return PeriodicReportKeyInformation(self)

    def _get_bytes(self, path: str, *, params: Optional[Dict] = None):
        """Make a GET request and return raw bytes with rate limiting and retry."""
        return self._request(path, params=params, return_json=False)

    def _get(self, path: str, *, params: Optional[Dict] = None):
        """Make a GET request and return JSON with rate limiting and retry."""
        return self._request(path, params=params, return_json=True)

    def _request(self, path: str, *, params: Optional[Dict] = None, return_json: bool = True):
        """Internal request method with rate limiting and retry logic."""
        # Apply rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
            raise DartRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                status_code=None,
            )

        url = self.base_url + path
        if params is None:
            params = {}
        params["crtfc_key"] = self.auth_key

        for attempt in range(self.max_retries + 1):
            try:
                response = self._session.get(url, params=params, timeout=self.timeout)

                # Handle different HTTP status codes
                if response.status_code == 200:
                    return response.json() if return_json else response.content
                elif response.status_code == 401:
                    raise DartAuthenticationError(
                        "Authentication failed - invalid or expired token",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )
                elif response.status_code == 403:
                    raise DartAuthorizationError(
                        "Access forbidden - insufficient permissions",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )
                elif response.status_code == 429:
                    retry_after = self._get_retry_after(response)
                    if attempt < self.max_retries:
                        wait_time = retry_after or (2**attempt)
                        time.sleep(wait_time)
                        continue
                    else:
                        raise DartRateLimitError(
                            f"Rate limit exceeded after {self.max_retries} retries",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            retry_after=retry_after,
                        )
                elif 400 <= response.status_code < 500:
                    raise DartClientError(
                        f"Client error: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )
                elif 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        wait_time = 2**attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        raise DartServerError(
                            f"Server error: {response.text}",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                        )
                else:
                    raise DartAPIError(
                        f"Unexpected error: {response.status_code}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )

            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise DartTimeoutError(f"Request timeout after {self.max_retries} retries") from e

            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise DartNetworkError(f"Network connection failed: {str(e)}") from e

            except requests.exceptions.RequestException as e:
                raise DartNetworkError(f"Request failed: {str(e)}") from e

        # This should never be reached, but just in case
        raise DartAPIError("Maximum retries exceeded")

    def _safe_json(self, response) -> Optional[Dict]:
        """Safely parse JSON response, returning None if parsing fails."""
        try:
            return response.json()
        except (ValueError, requests.exceptions.JSONDecodeError):
            return None

    def _get_retry_after(self, response: requests.Response) -> Optional[int]:
        """Extract retry-after value from response headers."""
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        return None

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()
