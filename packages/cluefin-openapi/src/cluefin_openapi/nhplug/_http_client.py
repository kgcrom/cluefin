import time
from typing import Any, Dict, Literal, Optional, Union

import requests
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi._http_base import BaseHttpClient
from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    NHPlugAPIError,
    NHPlugAuthenticationError,
    NHPlugAuthorizationError,
    NHPlugNetworkError,
    NHPlugRateLimitError,
    NHPlugServerError,
    NHPlugTimeoutError,
    NHPlugValidationError,
)

_ERROR_TYPES = {
    "validation": NHPlugValidationError,
    "auth": NHPlugAuthenticationError,
    "authz": NHPlugAuthorizationError,
    "rate_limit": NHPlugRateLimitError,
    "server": NHPlugServerError,
    "api": NHPlugAPIError,
}


class HttpClient(BaseHttpClient):
    """NH PLUG REST client.

    모든 호출은 `POST` + JSON 바디이며, 요청 파라미터는 `Input_0` 봉투로 감싸
    전송한다. 응답은 `rsp_cd`/`rsp_msg` + `Output_N` 봉투. 연속조회(페이지네이션)는
    요청/응답 헤더 `cts`/`cts_flag` 로 처리한다.
    """

    def __init__(
        self,
        token: str,
        app_key: str,
        secret_key: Union[str, SecretStr],
        env: Literal["prod", "dev"] = "prod",
        debug: bool = False,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_requests_per_second: float = 20.0,
        rate_limit_burst: int = 3,
    ):
        self.token = token
        self.app_key = app_key
        self.secret_key = secret_key.get_secret_value() if isinstance(secret_key, SecretStr) else secret_key
        self.env = env
        self.debug = debug
        self.timeout = timeout
        self.max_retries = max_retries

        # prod = 운영(실제 주문 체결), dev = 모의투자(moapi)
        if self.env == "prod":
            self.base_url = "https://api.nhplug.com:8443"
        else:
            self.base_url = "https://moapi.nhplug.com:8443"

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "cluefin-openapi/1.0",
                "Authorization": f"Bearer {self.token}",
                "x-client-id": self.app_key,
                "x-client-secret": self.secret_key,
            }
        )

        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        if self.debug:
            logger.enable("cluefin_openapi.nhplug")
        else:
            logger.disable("cluefin_openapi.nhplug")

    @property
    def common(self):
        """공통 (계좌·실시간 세션)"""
        from ._common import Common

        return Common(self)

    @property
    def krstock_order(self):
        """국내주식 주문"""
        from ._krstock_order import KrStockOrder

        return KrStockOrder(self)

    @property
    def krstock_inquiry(self):
        """국내주식 조회"""
        from ._krstock_inquiry import KrStockInquiry

        return KrStockInquiry(self)

    @property
    def krstock_quote(self):
        """국내주식 시세"""
        from ._krstock_quote import KrStockQuote

        return KrStockQuote(self)

    @property
    def overseas_stock_order(self):
        """해외주식 주문"""
        from ._overseas_stock_order import OverseasStockOrder

        return OverseasStockOrder(self)

    @property
    def overseas_stock_inquiry(self):
        """해외주식 조회"""
        from ._overseas_stock_inquiry import OverseasStockInquiry

        return OverseasStockInquiry(self)

    @property
    def overseas_stock_quote(self):
        """해외주식 시세"""
        from ._overseas_stock_quote import OverseasStockQuote

        return OverseasStockQuote(self)

    def post(
        self,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        cts: Optional[str] = None,
    ) -> requests.Response:
        """Send an envelope-wrapped POST request.

        Args:
            path: API path, e.g. "/n2/acctinfo".
            body: Input parameters; wrapped as {"Input_0": body}.
            cts: 연속거래키. 이전 응답 헤더의 `cts` 값을 그대로 전달하면 다음 페이지를 받는다.

        Returns:
            requests.Response: raw response (envelope parsing is done by category modules)
        """
        url = f"{self.base_url}{path}"
        headers: Dict[str, str] = {}
        if cts is not None:
            headers["cts"] = cts
            headers["cts_flag"] = "Y"

        payload = {"Input_0": body or {}}
        request_context = {"method": "POST", "path": path, "url": url, "body": payload}

        last_exception: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
                raise NHPlugRateLimitError(
                    "Local rate limiter timed out waiting for capacity",
                    request_context=self._sanitize_request_context(request_context),
                )
            try:
                response = self._session.post(url, json=payload, headers=headers, timeout=self.timeout)
            except requests.Timeout as e:
                raise NHPlugTimeoutError(
                    f"Request timed out after {self.timeout}s",
                    request_context=self._sanitize_request_context(request_context),
                ) from e
            except requests.RequestException as e:
                raise NHPlugNetworkError(
                    f"Network error: {e}",
                    request_context=self._sanitize_request_context(request_context),
                ) from e

            if response.status_code == 200:
                return response

            # 429 재시도에는 기존 토큰을 그대로 사용한다 (재발급 금지 — 보안 알림 유발).
            if response.status_code == 429 and attempt < self.max_retries:
                retry_after = self._get_retry_after(response) or 2**attempt
                logger.warning(f"Rate limited on {path}, retrying in {retry_after}s (attempt {attempt + 1})")
                time.sleep(retry_after)
                continue

            last_exception = self._dispatch_by_status(
                response,
                self._sanitize_request_context(request_context),
                _ERROR_TYPES,
            )
            break

        if last_exception is None:
            last_exception = NHPlugRateLimitError(f"Rate limit exceeded after {self.max_retries} retries")
        raise last_exception
