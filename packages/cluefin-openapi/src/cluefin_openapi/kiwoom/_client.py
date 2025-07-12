import json
import time
from typing import Dict, List, Literal, Optional, Tuple

import requests
from loguru import logger

from ._cache import SimpleCache, create_cache_key
from ._exceptions import (
    KiwoomAPIError,
    KiwoomAuthenticationError,
    KiwoomAuthorizationError,
    KiwoomNetworkError,
    KiwoomRateLimitError,
    KiwoomServerError,
    KiwoomTimeoutError,
    KiwoomValidationError,
)
from ._rate_limiter import TokenBucket


class MockResponse:
    """Mock response object for caching."""

    def __init__(self, status_code: int, headers: dict, content: bytes, json_data: Optional[dict] = None):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self._json_data = json_data

    def json(self):
        if self._json_data is not None:
            return self._json_data
        return json.loads(self.content.decode())

    @property
    def text(self):
        return self.content.decode()


class Client(object):
    def __init__(
        self,
        token: str,
        env: Literal["dev", "prod"],
        timeout: int = 30,
        max_retries: int = 3,
        debug: bool = False,
        rate_limit_requests_per_second: float = 10.0,
        rate_limit_burst: int = 20,
        enable_caching: bool = False,
        cache_ttl: int = 300,
    ):
        self.token = token
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug
        self.enable_caching = enable_caching

        if env == "dev":
            self.url = "https://mockapi.kiwoom.com"
        elif env == "prod":
            self.url = "https://api.kiwoom.com"
        else:
            raise ValueError("Invalid environment")

        # Create a reusable session for connection pooling
        self._session = requests.Session()

        # Set common headers for all requests
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "cluefin-kiwoom/0.1.0",
            }
        )

        # Initialize rate limiter
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        # Initialize cache if enabled
        self._cache = SimpleCache(default_ttl=cache_ttl) if enable_caching else None

        # Configure logging
        if self.debug:
            logger.enable("cluefin_openapi.kiwoom")
        else:
            logger.disable("cluefin_openapi.kiwoom")

    @property
    def account(self):
        from ._domestic_account import DomesticAccount

        return DomesticAccount(self)

    @property
    def chart(self):
        from ._domestic_chart import DomesticChart

        return DomesticChart(self)

    @property
    def credit_order(self):
        from ._domestic_credit_order import DomesticCreditOrder

        return DomesticCreditOrder(self)

    @property
    def etf(self):
        from ._domestic_etf import DomesticETF

        return DomesticETF(self)

    @property
    def foreign(self):
        from ._domestic_foreign import DomesticForeign

        return DomesticForeign(self)

    @property
    def market_conditions(self):
        from ._domestic_market_condition import DomesticMarketCondition

        return DomesticMarketCondition(self)

    @property
    def order(self):
        from ._domestic_order import DomesticOrder

        return DomesticOrder(self)

    @property
    def rank_info(self):
        from ._domestic_rank_info import DomesticRankInfo

        return DomesticRankInfo(self)

    @property
    def sector(self):
        from ._domestic_sector import DomesticSector

        return DomesticSector(self)

    @property
    def stock_info(self):
        from ._domestic_stock_info import DomesticStockInfo

        return DomesticStockInfo(self)

    @property
    def theme(self):
        from ._domestic_theme import DomesticTheme

        return DomesticTheme(self)

    def _post(self, path: str, headers: dict, body: dict, use_cache: bool = True):
        """Make a POST request with improved error handling and logging."""
        # Check cache first if enabled
        cache_key = None
        if self._cache and use_cache:
            cache_key = create_cache_key(f"{self.url}{path}", headers, body)
            cached_response = self._cache.get(cache_key)
            if cached_response:
                if self.debug:
                    logger.debug(f"Cache hit for {path}")
                return cached_response

        # Apply rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
            raise KiwoomRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
                request_context={"url": f"{self.url}{path}", "path": path},
            )

        url = f"{self.url}{path}"

        # Merge headers with authentication
        merged_headers = headers.copy()
        merged_headers["Authorization"] = f"Bearer {self.token}"

        # Log request details in debug mode
        if self.debug:
            logger.debug(f"Making POST request to {url}")
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

        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()

                response = self._session.post(
                    url=url,
                    headers=merged_headers,
                    data=json.dumps(body),
                    timeout=self.timeout,
                )

                duration = time.time() - start_time

                # Log response details in debug mode
                if self.debug:
                    logger.debug(f"Response received in {duration:.3f}s - Status: {response.status_code}")
                    logger.debug(f"Response headers: {dict(response.headers)}")

                # Handle different HTTP status codes
                if response.status_code == 200:
                    # Cache successful responses if caching is enabled
                    if self._cache and use_cache and cache_key:
                        # Create a mock response object to cache
                        cached_response = MockResponse(
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            content=response.content,
                            json_data=self._safe_json(response),
                        )
                        self._cache.set(cache_key, cached_response)
                        if self.debug:
                            logger.debug(f"Cached response for {path}")

                    return response
                elif response.status_code == 400:
                    raise KiwoomValidationError(
                        f"Bad request: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 401:
                    raise KiwoomAuthenticationError(
                        "Authentication failed - invalid or expired token",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                        request_context=request_context,
                    )
                elif response.status_code == 403:
                    raise KiwoomAuthorizationError(
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
                        raise KiwoomRateLimitError(
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
                        raise KiwoomServerError(
                            f"Server error: {response.text}",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            request_context=request_context,
                        )
                else:
                    raise KiwoomAPIError(
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
                    raise KiwoomTimeoutError(
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
                    raise KiwoomNetworkError(
                        f"Network connection failed: {str(e)}",
                        request_context=request_context,
                    ) from e
            except requests.exceptions.RequestException as e:
                raise KiwoomNetworkError(
                    f"Request failed: {str(e)}",
                    request_context=request_context,
                ) from e

        # This should never be reached, but just in case
        raise KiwoomAPIError("Maximum retries exceeded", request_context=request_context)

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

    def close(self):
        """Close the HTTP session."""
        if hasattr(self, "_session"):
            self._session.close()

    def batch_post(self, requests_data: List[Tuple[str, dict, dict]]) -> List[requests.Response]:
        """
        Execute multiple POST requests with rate limiting.

        Args:
            requests_data: List of tuples (path, headers, body)

        Returns:
            List of response objects
        """
        responses = []
        for path, headers, body in requests_data:
            try:
                response = self._post(path, headers, body)
                responses.append(response)
            except Exception as e:
                # For batch requests, we collect errors instead of raising immediately
                error_response = MockResponse(
                    status_code=0,
                    headers={},
                    content=json.dumps({"error": str(e)}).encode(),
                    json_data={"error": str(e), "exception_type": type(e).__name__},
                )
                responses.append(error_response)
        return responses

    def clear_cache(self):
        """Clear the request cache if caching is enabled."""
        if self._cache:
            self._cache.clear()
            if self.debug:
                logger.debug("Cache cleared")

    def cache_info(self) -> Optional[Dict]:
        """Get cache statistics if caching is enabled."""
        if self._cache:
            return self._cache.cache_info()
        return None

    def cleanup_cache(self) -> int:
        """Remove expired entries from cache if caching is enabled."""
        if self._cache:
            return self._cache.cleanup_expired()
        return 0
