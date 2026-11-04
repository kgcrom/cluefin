import re
from typing import Any, Literal, overload

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
from ._model import DartStatusCode

# 키가 틀리면 DART 는 HTTP 200 본문의 status 로 알린다(JSON 이든 ZIP 자리의 XML 이든). 2026-11-02 실측.
KEY_ERROR_STATUSES = frozenset(
    {
        DartStatusCode.UNREGISTERED_KEY.value,
        DartStatusCode.DISABLED_KEY.value,
        DartStatusCode.INACCESSIBLE_IP.value,
        DartStatusCode.EXPIRED_ACCOUNT.value,
    }
)
_XML_STATUS = re.compile(rb"<status>\s*(\d{3})\s*</status>")
_XML_MESSAGE = re.compile(rb"<message>(.*?)</message>", re.S)


def _raise_for_key_status(status: object, message: object, request_context: dict) -> None:
    if status in KEY_ERROR_STATUSES:
        raise DartAuthenticationError(
            f"{status} {message or 'DART rejected the key'}",
            status_code=None,
            response_data={"status": status, "message": message},
            request_context=request_context,
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
    def major_matters_report(self):
        """주요사항보고서 주요정보 (DS005). `major_shareholder_disclosure` was its old, mismatched name."""
        from ._major_shareholder_disclosure import MajorMattersReport

        return MajorMattersReport(self)

    @property
    def major_shareholder_disclosure(self):
        """Deprecated alias for :attr:`major_matters_report` (2026-11-04, B-13)."""
        import warnings

        warnings.warn(
            "Client.major_shareholder_disclosure is deprecated; use Client.major_matters_report instead "
            "(it serves 주요사항보고서, not major-shareholder disclosures).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.major_matters_report

    @property
    def public_disclosure(self):
        from ._public_disclosure import PublicDisclosure

        return PublicDisclosure(self)

    @property
    def periodic_report_key_information(self):
        from ._periodic_report_key_information import PeriodicReportKeyInformation

        return PeriodicReportKeyInformation(self)

    @property
    def share_disclosure_comprehensive(self):
        from ._share_disclosure_comprehensive import ShareDisclosureComprehensive

        return ShareDisclosureComprehensive(self)

    @property
    def periodic_report_financial_statement(self):
        from ._periodic_report_financial_statement import PeriodicReportFinancialStatement

        return PeriodicReportFinancialStatement(self)

    def _get_bytes(self, path: str, *, params: dict | None = None) -> bytes:
        """Make a GET request and return raw bytes with rate limiting and retry."""
        return self._request(path, params=params, return_json=False)

    def _get(self, path: str, *, params: dict | None = None) -> Any:
        """Make a GET request and return JSON with rate limiting and retry."""
        return self._request(path, params=params, return_json=True)

    def _dispatch_dart(self, response: requests.Response, request_context: dict) -> Exception | None:
        """Map a non-200 HTTP response to the appropriate DART exception.

        Returns an Exception to raise, or None to accept the response (200 path
        is handled by the shared loop before this is called). Kept separate from
        the shared _dispatch_by_status: DART has no 400/validation split and its
        message wording differs ("Client error:", "Unexpected error:").
        """
        if response.status_code == 401:
            return DartAuthenticationError(
                "Authentication failed - invalid or expired token",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
            )
        elif response.status_code == 403:
            return DartAuthorizationError(
                "Access forbidden - insufficient permissions",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
            )
        elif response.status_code == 429:
            # Terminal 429 (called only on final retry by _execute_with_retry)
            return DartRateLimitError(
                f"Rate limit exceeded after {self.max_retries} retries",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
                retry_after=self._get_retry_after(response),
            )
        elif 500 <= response.status_code < 600:
            # Terminal 5xx (called only on final retry by _execute_with_retry)
            return DartServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
            )
        elif 400 <= response.status_code < 500:
            return DartClientError(
                f"Client error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
            )
        else:
            return DartAPIError(
                f"Unexpected error: {response.status_code}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
                request_context=request_context,
            )

    @overload
    def _request(self, path: str, *, params: dict | None = ..., return_json: Literal[False]) -> bytes: ...
    @overload
    def _request(self, path: str, *, params: dict | None = ..., return_json: Literal[True] = ...) -> Any: ...
    def _request(self, path: str, *, params: dict | None = None, return_json: bool = True) -> Any:
        """Internal request method with rate limiting and retry logic."""
        url = self.base_url + path
        # Copy so the auth secret is never written back into the caller's dict
        params = dict(params) if params else {}
        params["crtfc_key"] = self.auth_key

        # crtfc_key is the auth secret — redact it in the context that flows
        # into exceptions and hooks (the real key still goes on the wire).
        request_context = {
            "url": url,
            "path": path,
            "method": "GET",
            "params": {**params, "crtfc_key": "***"},
        }

        response = self._execute_with_retry(
            send_fn=lambda: self._session.get(url, params=params, timeout=self.timeout),
            rate_limiter=self._rate_limiter,
            timeout=self.timeout,
            max_retries=self.max_retries,
            request_context=request_context,
            dispatch=lambda resp: self._dispatch_dart(resp, request_context),
            rate_limit_error=lambda: DartRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                status_code=None,
                request_context={"url": url, "path": path},
            ),
            timeout_error_cls=DartTimeoutError,
            network_error_cls=DartNetworkError,
        )
        if return_json:
            payload = response.json()
            if isinstance(payload, dict):
                _raise_for_key_status(payload.get("status"), payload.get("message"), request_context)
            return payload
        content = response.content
        if not content.startswith(b"PK"):  # ZIP 이 아니면 오류 XML 일 수 있다
            match = _XML_STATUS.search(content[:512])
            if match:
                message = _XML_MESSAGE.search(content[:512])
                _raise_for_key_status(
                    match.group(1).decode(),
                    message.group(1).decode("utf-8", "replace") if message else None,
                    request_context,
                )
        return content

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()
