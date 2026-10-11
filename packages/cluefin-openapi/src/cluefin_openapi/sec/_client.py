from typing import Optional
from urllib.parse import urlsplit

import requests

from cluefin_openapi._http_base import BaseHttpClient
from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    SecAPIError,
    SecAuthorizationError,
    SecClientError,
    SecNetworkError,
    SecNotFoundError,
    SecRateLimitError,
    SecServerError,
    SecTimeoutError,
)

WWW_BASE_URL = "https://www.sec.gov"
DATA_BASE_URL = "https://data.sec.gov"

# SEC fair-access policy: at most 10 requests per second per client.
MAX_REQUESTS_PER_SECOND = 10.0

_ALLOWED_HOSTS = frozenset({urlsplit(WWW_BASE_URL).hostname, urlsplit(DATA_BASE_URL).hostname})


class Client(BaseHttpClient):
    """HTTP client for SEC EDGAR (www.sec.gov and data.sec.gov).

    SEC has no API key. Instead every request must declare who is calling in the
    User-Agent header ("Name email@example.com"); undeclared or over-rate clients get 403.
    """

    def __init__(
        self,
        user_agent: str,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_requests_per_second: float = 8.0,
        rate_limit_burst: int = 8,
    ):
        self.user_agent = _validate_user_agent(user_agent)
        if not 0 < rate_limit_requests_per_second <= MAX_REQUESTS_PER_SECOND:
            raise ValueError(
                f"rate_limit_requests_per_second는 0보다 크고 {MAX_REQUESTS_PER_SECOND:g} 이하여야 합니다 "
                f"(SEC 공정 접근 한도). 받은 값: {rate_limit_requests_per_second}"
            )
        if not 0 < rate_limit_burst <= MAX_REQUESTS_PER_SECOND:
            raise ValueError(
                f"rate_limit_burst는 1 이상 {MAX_REQUESTS_PER_SECOND:g} 이하여야 합니다. 받은 값: {rate_limit_burst}"
            )

        self.timeout = timeout
        self.max_retries = max_retries
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept-Encoding": "gzip, deflate",
            }
        )
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

    def _get_json(self, url: str):
        """GET a sec.gov URL and return the decoded JSON body."""
        return self._request(url).json()

    def _get_bytes(self, url: str) -> bytes:
        """GET a sec.gov URL and return the raw body."""
        return self._request(url).content

    def _dispatch_sec(self, response: requests.Response, request_context: dict) -> Optional[Exception]:
        """Map a non-200 HTTP response to the appropriate SEC exception."""
        common = {
            "status_code": response.status_code,
            "response_data": self._safe_json(response),
            "request_context": request_context,
        }
        if response.status_code == 403:
            return SecAuthorizationError(
                "SEC가 요청을 거부했습니다. User-Agent에 이름과 이메일이 들어 있는지, "
                "초당 10회를 넘기지 않았는지 확인하세요 (한도를 넘기면 SEC가 한동안 계속 거부합니다).",
                **common,
            )
        elif response.status_code == 404:
            return SecNotFoundError(f"Not found: {request_context['url']}", **common)
        elif response.status_code == 429:
            # Terminal 429 (called only on final retry by _execute_with_retry)
            return SecRateLimitError(
                f"Rate limit exceeded after {self.max_retries} retries",
                retry_after=self._get_retry_after(response),
                **common,
            )
        elif 500 <= response.status_code < 600:
            # Terminal 5xx (called only on final retry by _execute_with_retry)
            return SecServerError(f"Server error: {response.status_code}", **common)
        elif 400 <= response.status_code < 500:
            return SecClientError(f"Client error: {response.status_code}", **common)
        else:
            return SecAPIError(f"Unexpected status code: {response.status_code}", **common)

    def _request(self, url: str) -> requests.Response:
        """Internal request method with rate limiting and retry logic."""
        parts = urlsplit(url)
        if parts.scheme != "https" or parts.hostname not in _ALLOWED_HOSTS:
            raise ValueError(f"SEC 클라이언트는 https://www.sec.gov, https://data.sec.gov 만 호출합니다: {url}")

        # The User-Agent lives in the session headers and stays out of the context.
        request_context = {"url": url, "path": parts.path, "method": "GET"}

        return self._execute_with_retry(
            send_fn=lambda: self._session.get(url, timeout=self.timeout),
            rate_limiter=self._rate_limiter,
            timeout=self.timeout,
            max_retries=self.max_retries,
            request_context=request_context,
            dispatch=lambda resp: self._dispatch_sec(resp, request_context),
            rate_limit_error=lambda: SecRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                status_code=None,
                request_context=request_context,
            ),
            timeout_error_cls=SecTimeoutError,
            network_error_cls=SecNetworkError,
        )

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()


def _validate_user_agent(user_agent: str) -> str:
    value = (user_agent or "").strip()
    if "@" not in value:
        raise ValueError(
            'SEC 요청에는 "이름 이메일" 형식의 User-Agent가 필요합니다 (예: "Jane Doe jane@example.com"). '
            ".env의 SEC_USER_AGENT를 확인하세요."
        )
    return value
