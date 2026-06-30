from typing import Dict, Optional

import requests

from cluefin_openapi._http_base import BaseHttpClient
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


class Client(BaseHttpClient):
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

    def _dispatch_dart(self, response: requests.Response) -> Optional[Exception]:
        """Map a non-200 HTTP response to the appropriate DART exception.

        Returns an Exception to raise, or None to accept the response (200 path
        is handled by the shared loop before this is called).
        """
        if response.status_code == 401:
            return DartAuthenticationError(
                "Authentication failed - invalid or expired token",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif response.status_code == 403:
            return DartAuthorizationError(
                "Access forbidden - insufficient permissions",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif response.status_code == 429:
            # Terminal 429 (called only on final retry by _execute_with_retry)
            return DartRateLimitError(
                f"Rate limit exceeded after {self.max_retries} retries",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                retry_after=self._get_retry_after(response),
            )
        elif 500 <= response.status_code < 600:
            # Terminal 5xx (called only on final retry by _execute_with_retry)
            return DartServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif 400 <= response.status_code < 500:
            return DartClientError(
                f"Client error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        else:
            return DartAPIError(
                f"Unexpected error: {response.status_code}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )

    def _request(self, path: str, *, params: Optional[Dict] = None, return_json: bool = True):
        """Internal request method with rate limiting and retry logic."""
        url = self.base_url + path
        if params is None:
            params = {}
        params["crtfc_key"] = self.auth_key

        request_context = {"url": url, "path": path, "method": "GET", "params": params}

        response = self._execute_with_retry(
            send_fn=lambda: self._session.get(url, params=params, timeout=self.timeout),
            rate_limiter=self._rate_limiter,
            timeout=self.timeout,
            max_retries=self.max_retries,
            request_context=request_context,
            dispatch=self._dispatch_dart,
            rate_limit_error=lambda: DartRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                status_code=None,
            ),
            timeout_error=lambda e: DartTimeoutError(f"Request timeout after {self.max_retries} retries"),
            network_error=lambda e: (
                DartNetworkError(f"Network connection failed: {str(e)}")
                if isinstance(e, requests.exceptions.ConnectionError)
                else DartNetworkError(f"Request failed: {str(e)}")
            ),
        )
        return response.json() if return_json else response.content

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()
