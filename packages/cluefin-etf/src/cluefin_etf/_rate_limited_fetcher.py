from __future__ import annotations

import time
from collections.abc import Callable, Mapping

from cluefin_etf._fetcher_types import HttpMethod, PageFetcher, PageValidator, RequestData
from cluefin_etf._models import FetchResult, ProviderName


class RateLimitedFetcher:
    """Throttle consecutive provider page calls made through a shared fetcher."""

    def __init__(
        self,
        fetcher: PageFetcher,
        *,
        min_interval_seconds: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.fetcher = fetcher
        self.min_interval_seconds = min_interval_seconds
        self._clock = clock
        self._sleeper = sleeper
        self._last_request_at: float | None = None

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
        self._sleep_until_allowed()
        try:
            return self.fetcher.fetch(
                url,
                provider=provider,
                validator=validator,
                method=method,
                headers=headers,
                data=data,
                referrer=referrer,
            )
        finally:
            self._last_request_at = self._clock()

    def _sleep_until_allowed(self) -> None:
        if self._last_request_at is None:
            return

        elapsed = self._clock() - self._last_request_at
        remaining = self.min_interval_seconds - elapsed
        if remaining > 0:
            self._sleeper(remaining)
