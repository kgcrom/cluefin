from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Literal, Protocol

from cluefin_etf._models import FetchResult, ProviderName

PageValidator = Callable[[FetchResult], bool]
HttpMethod = Literal["GET", "POST"]
RequestData = Mapping[str, Any] | str | bytes


class PageFetcher(Protocol):
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
        """Fetch a page and return raw HTML with metadata."""
