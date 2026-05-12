from __future__ import annotations

from cluefin_etf._browser_fetcher import (
    BrowserSession,
    PlaywrightBrowserSession,
    PlaywrightFetcher,
    _browser_request_body,
    _origin_url,
)
from cluefin_etf._fallback_fetcher import FallbackFetcher
from cluefin_etf._fetcher_types import HttpMethod, PageFetcher, PageValidator, RequestData
from cluefin_etf._http_fetcher import SimpleHttpFetcher
from cluefin_etf._rate_limited_fetcher import RateLimitedFetcher


def create_default_fetcher() -> RateLimitedFetcher:
    return RateLimitedFetcher(FallbackFetcher())


__all__ = [
    "BrowserSession",
    "FallbackFetcher",
    "HttpMethod",
    "PageFetcher",
    "PageValidator",
    "PlaywrightBrowserSession",
    "PlaywrightFetcher",
    "RateLimitedFetcher",
    "RequestData",
    "SimpleHttpFetcher",
    "_browser_request_body",
    "_origin_url",
    "create_default_fetcher",
]
