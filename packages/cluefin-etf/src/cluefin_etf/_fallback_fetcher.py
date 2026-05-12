from __future__ import annotations

from collections.abc import Mapping

from cluefin_etf._browser_fetcher import PlaywrightFetcher
from cluefin_etf._errors import FetchError
from cluefin_etf._fetcher_types import HttpMethod, PageFetcher, PageValidator, RequestData
from cluefin_etf._http_fetcher import SimpleHttpFetcher
from cluefin_etf._models import FetchResult, ProviderName


class FallbackFetcher:
    """Try plain HTTP first and fall back to Playwright on fetch failure."""

    def __init__(
        self,
        primary: PageFetcher | None = None,
        fallback: PageFetcher | None = None,
        min_html_length: int = 50,
    ) -> None:
        self.primary = primary or SimpleHttpFetcher()
        self.fallback = fallback or PlaywrightFetcher()
        self.min_html_length = min_html_length

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
        try:
            result = self.primary.fetch(
                url,
                provider=provider,
                validator=validator,
                method=method,
                headers=headers,
                data=data,
                referrer=referrer,
            )
        except FetchError as exc:
            return self._fetch_fallback(
                url,
                provider=provider,
                validator=validator,
                method=method,
                headers=headers,
                data=data,
                referrer=referrer,
                reason=str(exc),
            )

        fallback_reason = self.should_fallback(result, validator=validator)
        if fallback_reason is not None:
            return self._fetch_fallback(
                url,
                provider=provider,
                validator=validator,
                method=method,
                headers=headers,
                data=data,
                referrer=referrer,
                reason=fallback_reason,
            )

        return result

    def should_fallback(self, result: FetchResult, validator: PageValidator | None = None) -> str | None:
        html = result.html.strip()
        if not html:
            return "empty_html"
        if len(html) < self.min_html_length:
            return "html_too_short"
        if validator is not None and not validator(result):
            return "validator_rejected"
        return None

    def _fetch_fallback(
        self,
        url: str,
        *,
        provider: ProviderName | str,
        validator: PageValidator | None,
        method: HttpMethod,
        headers: Mapping[str, str] | None,
        data: RequestData | None,
        referrer: str | None,
        reason: str,
    ) -> FetchResult:
        result = self.fallback.fetch(
            url,
            provider=provider,
            validator=validator,
            method=method,
            headers=headers,
            data=data,
            referrer=referrer,
        )
        fallback_reason = self.should_fallback(result, validator=validator)
        if fallback_reason is not None:
            raise FetchError(
                f"Fallback fetch result was rejected for {url}: {fallback_reason}; primary reason: {reason}"
            )
        return result.model_copy(update={"metadata": result.metadata.model_copy(update={"fallback_reason": reason})})
