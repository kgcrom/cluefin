import time
from typing import Dict, Optional

import requests
from loguru import logger

from cluefin_openapi._rate_limiter import TokenBucket

from ._exceptions import (
    KrxAPIError,
    KrxAuthenticationError,
    KrxAuthorizationError,
    KrxClientError,
    KrxNetworkError,
    KrxRateLimitError,
    KrxServerError,
    KrxTimeoutError,
)


class Client(object):
    # TODO convert auth_key type to SecretStr
    def __init__(
        self,
        auth_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        debug: bool = False,
        rate_limit_requests_per_second: float = 5.0,
        rate_limit_burst: int = 10,
    ):
        self.auth_key = auth_key
        self.base_url = "https://data-dbg.krx.co.kr"
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug

        # Create a reusable session for connection pooling
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "cluefin-openapi/1.0",
            }
        )

        # Initialize rate limiter
        self._rate_limiter = TokenBucket(capacity=rate_limit_burst, refill_rate=rate_limit_requests_per_second)

        # Configure logging
        if self.debug:
            logger.enable("cluefin_openapi.krx")
        else:
            logger.disable("cluefin_openapi.krx")

    @property
    def index(self):
        from ._index import Index

        return Index(self)

    @property
    def stock(self):
        from ._stock import Stock

        return Stock(self)

    @property
    def exchange_traded_product(self):
        from ._exchange_traded_product import ExchangeTradedProduct

        return ExchangeTradedProduct(self)

    @property
    def bond(self):
        from ._bond import Bond

        return Bond(self)

    @property
    def derivatives(self):
        from ._derivatives import Derivatives

        return Derivatives(self)

    @property
    def general_product(self):
        from ._general_product import GeneralProduct

        return GeneralProduct(self)

    @property
    def esg(self):
        from ._esg import Esg

        return Esg(self)

    def _get(self, path: str, params: Optional[Dict] = None):
        """Make a GET request with rate limiting and retry logic."""
        # Apply rate limiting
        if not self._rate_limiter.wait_for_tokens(timeout=self.timeout):
            raise KrxRateLimitError(
                "Rate limit timeout - could not acquire token within timeout period",
            )

        url = self.base_url + path
        headers = {"AUTH_KEY": self.auth_key}

        # Log request details in debug mode
        if self.debug:
            logger.debug(f"Making GET request to {url}")
            logger.debug(f"Params: {params}")
            logger.debug(f"Rate limiter tokens available: {self._rate_limiter.available_tokens:.2f}")

        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()

                response = self._session.get(
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )

                duration = time.time() - start_time

                # Log response details in debug mode
                if self.debug:
                    logger.debug(f"Response received in {duration:.3f}s - Status: {response.status_code}")

                # Handle different HTTP status codes
                if response.status_code == 200:
                    try:
                        return response.json()
                    except ValueError:
                        # JSON 파싱 실패시 텍스트 반환
                        return response.text
                elif response.status_code == 401:
                    raise KrxAuthenticationError(
                        "Authentication failed - invalid or expired token",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )
                elif response.status_code == 403:
                    raise KrxAuthorizationError(
                        "Access forbidden - insufficient permissions",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
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
                        raise KrxRateLimitError(
                            f"Rate limit exceeded after {self.max_retries} retries",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                            retry_after=retry_after,
                        )
                elif 400 <= response.status_code < 500:
                    raise KrxClientError(
                        f"Client error: {response.text}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )
                elif 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        wait_time = 2**attempt
                        logger.warning(f"Server error {response.status_code}, retrying in {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise KrxServerError(
                            f"Server error: {response.text}",
                            status_code=response.status_code,
                            response_data=self._safe_json(response),
                        )
                else:
                    raise KrxAPIError(
                        f"Unexpected error: {response.status_code}",
                        status_code=response.status_code,
                        response_data=self._safe_json(response),
                    )

            except requests.exceptions.Timeout as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Request timeout, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KrxTimeoutError(
                        f"Request timeout after {self.max_retries} retries",
                    ) from e
            except requests.exceptions.ConnectionError as e:
                if attempt < self.max_retries:
                    wait_time = 2**attempt
                    logger.warning(f"Connection error, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    raise KrxNetworkError(
                        f"Network connection failed: {str(e)}",
                    ) from e
            except requests.exceptions.RequestException as e:
                raise KrxNetworkError(
                    f"Request failed: {str(e)}",
                ) from e

        # This should never be reached, but just in case
        raise KrxAPIError("Maximum retries exceeded")

    def _safe_json(self, response: requests.Response) -> Optional[Dict]:
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
