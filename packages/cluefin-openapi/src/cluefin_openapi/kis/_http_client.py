import json
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union
from uuid import uuid4

import requests
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    KISAPIError,
    KISAuthenticationError,
    KISAuthorizationError,
    KISNetworkError,
    KISRateLimitError,
    KISServerError,
    KISTimeoutError,
    KISValidationError,
)


class HttpClient(object):
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
        self._last_response_debug: Optional[Dict[str, Any]] = None

        if self.env == "prod":
            self.base_url = "https://openapi.koreainvestment.com:9443"
        else:
            self.base_url = "https://openapivts.koreainvestment.com:29443"

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

        if self.debug:
            logger.enable("cluefin_openapi.kis")
        else:
            logger.disable("cluefin_openapi.kis")

    @property
    def domestic_account(self):
        """국내주식 주문/계좌"""
        from ._domestic_account import DomesticAccount

        return DomesticAccount(self)

    @property
    def domestic_basic_quote(self):
        """국내주식 기본시세"""
        from ._domestic_basic_quote import DomesticBasicQuote

        return DomesticBasicQuote(self)

    @property
    def domestic_issue_other(self):
        """국내주식 업종/기타"""
        from ._domestic_issue_other import DomesticIssueOther

        return DomesticIssueOther(self)

    @property
    def domestic_stock_info(self):
        """국내주식 종목정보"""
        from ._domestic_stock_info import DomesticStockInfo

        return DomesticStockInfo(self)

    @property
    def domestic_market_analysis(self):
        """국내주식 시세분석"""
        from ._domestic_market_analysis import DomesticMarketAnalysis

        return DomesticMarketAnalysis(self)

    @property
    def domestic_ranking_analysis(self):
        """국내주식 순위분석"""
        from ._domestic_ranking_analysis import DomesticRankingAnalysis

        return DomesticRankingAnalysis(self)

    @property
    def onmarket_bond_basic_quote(self):
        """장내채권 기본시세"""
        from ._onmarket_bond_basic_quote import OnmarketBondBasicQuote

        return OnmarketBondBasicQuote(self)

    @property
    def overseas_account(self):
        """해외주식 주문/계좌"""
        from ._overseas_account import OverseasAccount

        return OverseasAccount(self)

    @property
    def overseas_basic_quote(self):
        """해외주식 기본시세"""
        from ._overseas_basic_quote import BasicQuote

        return BasicQuote(self)

    @property
    def overseas_market_analysis(self):
        """해외주식 시세분석"""
        from ._overseas_market_analysis import OverseasMarketAnalysis

        return OverseasMarketAnalysis(self)

    def _build_headers(self, headers: dict) -> dict:
        """Build merged headers with authentication."""
        merged_headers = dict(self._session.headers)
        merged_headers["content-type"] = "application/json;charset=UTF-8"
        merged_headers["accept"] = "application/json"
        merged_headers["authorization"] = f"Bearer {self.token}"
        merged_headers["appkey"] = self.app_key
        merged_headers["appsecret"] = self.secret_key
        merged_headers["custtype"] = "P"  # P: 개인, C: 법인
        merged_headers.update(headers)  # Merge custom headers (e.g., tr_id)
        return merged_headers

    def _safe_json(self, response: requests.Response) -> Optional[Dict]:
        """Safely parse JSON response, returning None if parsing fails."""
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
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

    def _sanitize_request_context(self, request_context: dict) -> dict:
        """Keep only non-secret request metadata for debugging."""
        headers = request_context.get("headers", {})
        sanitized = {
            "method": request_context.get("method"),
            "path": request_context.get("path"),
            "url": request_context.get("url"),
            "tr_id": headers.get("tr_id") or headers.get("TR_ID"),
        }
        if "params" in request_context:
            sanitized["params"] = request_context["params"]
        if "body" in request_context:
            sanitized["body"] = request_context["body"]
        return sanitized

    def _serialize_payload(self, payload: Any) -> str:
        """Serialize payload for previews and debug artifacts."""
        if isinstance(payload, (dict, list)):
            return json.dumps(payload, ensure_ascii=False, indent=2, default=str)
        return str(payload)

    def _write_debug_artifact(
        self,
        request_context: dict,
        response: requests.Response,
        response_payload: Any,
    ) -> Optional[str]:
        """Persist the last response payload to a temp file for quick inspection."""
        try:
            debug_dir = Path(tempfile.gettempdir()) / "cluefin-kis-debug"
            debug_dir.mkdir(parents=True, exist_ok=True)

            path_slug = (request_context.get("path") or "response").strip("/").replace("/", "_") or "response"
            tr_id = request_context.get("tr_id") or "unknown-tr-id"
            artifact_path = debug_dir / f"{int(time.time())}-{tr_id}-{path_slug}-{uuid4().hex[:8]}.json"

            artifact = {
                "request": request_context,
                "response": {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response_payload,
                },
            }
            artifact_path.write_text(
                json.dumps(artifact, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            return None

        return str(artifact_path)

    def _record_last_response(self, response: requests.Response, request_context: dict) -> None:
        """Store a sanitized snapshot of the last response for test failure reporting."""
        response_payload = self._safe_json(response)
        if response_payload is None:
            response_payload = response.text

        sanitized_context = self._sanitize_request_context(request_context)
        artifact_path = self._write_debug_artifact(sanitized_context, response, response_payload)
        preview = self._serialize_payload(response_payload)
        if len(preview) > 4000:
            preview = f"{preview[:4000]}\n... (truncated)"

        self._last_response_debug = {
            "request": sanitized_context,
            "status_code": response.status_code,
            "artifact_path": artifact_path,
            "preview": preview,
        }

    @property
    def last_response_debug(self) -> Optional[Dict[str, Any]]:
        """Return the last recorded response snapshot."""
        return self._last_response_debug

    def format_last_response_debug(self) -> str:
        """Format the last response snapshot for pytest failure output."""
        if not self._last_response_debug:
            return ""

        request = self._last_response_debug["request"]
        lines = [
            f"status_code: {self._last_response_debug['status_code']}",
            f"method: {request.get('method')}",
            f"path: {request.get('path')}",
        ]
        if request.get("tr_id"):
            lines.append(f"tr_id: {request['tr_id']}")
        if "params" in request:
            lines.append(f"params: {json.dumps(request['params'], ensure_ascii=False, default=str)}")
        if "body" in request:
            lines.append(f"body: {json.dumps(request['body'], ensure_ascii=False, default=str)}")
        if self._last_response_debug.get("artifact_path"):
            lines.append(f"artifact_path: {self._last_response_debug['artifact_path']}")
        lines.append("response_preview:")
        lines.append(self._last_response_debug["preview"])
        return "\n".join(lines)

    # TODO 법인은 추후 필요해지면 구현
    def _get(self, path: str, headers: dict, params: dict) -> requests.Response:
        """Make a GET request with rate limiting, retry, and error handling."""
        # Apply rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
            raise KISRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                request_context={"url": f"{self.base_url}{path}", "path": path},
            )

        url = self.base_url + path
        merged_headers = self._build_headers(headers)

        if self.debug:
            logger.debug(f"GET {url}")
            logger.debug(f"Headers: {merged_headers}")
            logger.debug(f"Params: {params}")
            logger.debug(f"Rate limiter tokens available: {self._rate_limiter.available_tokens:.2f}")

        request_context = {
            "url": url,
            "path": path,
            "method": "GET",
            "headers": merged_headers,
            "params": params,
        }
        self._last_response_debug = None

        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()

                response = self._session.get(url, headers=merged_headers, params=params, timeout=self.timeout)

                duration = time.time() - start_time

                if self.debug:
                    logger.debug(f"Response received in {duration:.3f}s - Status: {response.status_code}")
                    logger.debug(f"Response Headers: {response.headers}")
                    logger.debug(f"Response Body: {response.text}")

                self._record_last_response(response, request_context)

                # Handle different HTTP status codes
                if response.status_code == 200:
                    return response
                elif response.status_code == 400:
                    raise KISValidationError(
                        f"Bad request: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 401:
                    raise KISAuthenticationError(
                        "Authentication failed - invalid or expired token",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 403:
                    raise KISAuthorizationError(
                        "Access forbidden - insufficient permissions",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 429:
                    retry_after = self._get_retry_after(response)
                    if attempt < self.max_retries:
                        wait_time = retry_after or (2**attempt)
                        logger.warning(
                            f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{self.max_retries}"
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        raise KISRateLimitError(
                            f"Rate limit exceeded after {self.max_retries} retries",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            request_context=request_context,
                            retry_after=retry_after,
                        )
                elif 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        wait_time = 2**attempt
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise KISServerError(
                            f"Server error: {response.text}",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            request_context=request_context,
                        )
                else:
                    raise KISAPIError(
                        f"Unexpected status code {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )

            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Request timeout, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KISTimeoutError(
                        f"Request timeout after {self.max_retries} retries",
                        request_context=request_context,
                    ) from e
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Connection error, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KISNetworkError(
                        f"Network connection failed: {str(e)}",
                        request_context=request_context,
                    ) from e
            except requests.exceptions.RequestException as e:
                raise KISNetworkError(
                    f"Request failed: {str(e)}",
                    request_context=request_context,
                ) from e

        # This should never be reached, but just in case
        raise KISAPIError("Maximum retries exceeded", request_context=request_context)

    # TODO 법인은 추후 필요해지면 구현
    def _post(self, path: str, headers: dict, body: dict) -> requests.Response:
        """Make a POST request with rate limiting, retry, and error handling."""
        # Apply rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
            raise KISRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                request_context={"url": f"{self.base_url}{path}", "path": path},
            )

        url = self.base_url + path
        merged_headers = self._build_headers(headers)

        if self.debug:
            logger.debug(f"POST {url}")
            logger.debug(f"Headers: {merged_headers}")
            logger.debug(f"Body: {body}")
            logger.debug(f"Rate limiter tokens available: {self._rate_limiter.available_tokens:.2f}")

        request_context = {
            "url": url,
            "path": path,
            "method": "POST",
            "headers": merged_headers,
            "body": body,
        }
        self._last_response_debug = None

        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()

                response = self._session.post(url, headers=merged_headers, json=body, timeout=self.timeout)

                duration = time.time() - start_time

                if self.debug:
                    logger.debug(f"Response received in {duration:.3f}s - Status: {response.status_code}")
                    logger.debug(f"Response Headers: {response.headers}")
                    logger.debug(f"Response Body: {response.text}")

                self._record_last_response(response, request_context)

                # Handle different HTTP status codes
                if response.status_code == 200:
                    return response
                elif response.status_code == 400:
                    raise KISValidationError(
                        f"Bad request: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 401:
                    raise KISAuthenticationError(
                        "Authentication failed - invalid or expired token",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 403:
                    raise KISAuthorizationError(
                        "Access forbidden - insufficient permissions",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 429:
                    retry_after = self._get_retry_after(response)
                    if attempt < self.max_retries:
                        wait_time = retry_after or (2**attempt)
                        logger.warning(
                            f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{self.max_retries}"
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        raise KISRateLimitError(
                            f"Rate limit exceeded after {self.max_retries} retries",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            request_context=request_context,
                            retry_after=retry_after,
                        )
                elif 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        wait_time = 2**attempt
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise KISServerError(
                            f"Server error: {response.text}",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            request_context=request_context,
                        )
                else:
                    raise KISAPIError(
                        f"Unexpected status code {response.status_code}: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )

            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Request timeout, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KISTimeoutError(
                        f"Request timeout after {self.max_retries} retries",
                        request_context=request_context,
                    ) from e
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Connection error, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KISNetworkError(
                        f"Network connection failed: {str(e)}",
                        request_context=request_context,
                    ) from e
            except requests.exceptions.RequestException as e:
                raise KISNetworkError(
                    f"Request failed: {str(e)}",
                    request_context=request_context,
                ) from e

        # This should never be reached, but just in case
        raise KISAPIError("Maximum retries exceeded", request_context=request_context)

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()
