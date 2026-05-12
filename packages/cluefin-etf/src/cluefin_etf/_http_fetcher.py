from __future__ import annotations

import time
from collections.abc import Mapping

import requests

from cluefin_etf._errors import FetchError
from cluefin_etf._fetcher_types import HttpMethod, PageValidator, RequestData
from cluefin_etf._models import FetchMetadata, FetchResult, ProviderName


class SimpleHttpFetcher:
    """Fetch ETF pages with plain HTTP before using browser automation."""

    def __init__(
        self,
        session: requests.Session | None = None,
        timeout: float = 20.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.session = session or requests.Session()
        self.timeout = timeout
        self.headers = {
            "User-Agent": "cluefin-etf/0.1",
            **(headers or {}),
        }

    def fetch(
        self,
        url: str,
        *,
        provider: ProviderName | str,
        validator: PageValidator | None = None,
        method: HttpMethod = "GET",
        headers: Mapping[str, str] | None = None,
        data: RequestData | None = None,
        referrer: str | None = None,
    ) -> FetchResult:
        started_at = time.perf_counter()
        request_headers = {**self.headers, **(headers or {})}
        if referrer is not None:
            request_headers.setdefault("Referer", referrer)

        try:
            response = self.session.request(
                method,
                url,
                headers=request_headers,
                data=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise FetchError(f"HTTP fetch failed for {url}") from exc

        elapsed_ms = (
            response.elapsed.total_seconds() * 1000 if response.elapsed else (time.perf_counter() - started_at) * 1000
        )
        return FetchResult(
            html=response.text,
            metadata=FetchMetadata(
                provider=ProviderName(provider),
                url=url,
                strategy="http",
                status_code=response.status_code,
                final_url=response.url,
                content_type=response.headers.get("Content-Type"),
                elapsed_ms=elapsed_ms,
            ),
        )
