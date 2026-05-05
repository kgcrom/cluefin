from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from typing import Any, Literal, Protocol
from urllib.parse import urlencode, urlsplit

import requests

from cluefin_etf._errors import FetchError
from cluefin_etf._models import FetchMetadata, FetchResult, ProviderName

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


class BrowserSession(Protocol):
    def fetch_html(
        self,
        url: str,
        *,
        method: HttpMethod = "GET",
        headers: Mapping[str, str] | None = None,
        data: RequestData | None = None,
        referrer: str | None = None,
    ) -> tuple[str, str | None]:
        """Fetch rendered HTML and return `(html, final_url)`."""


class PlaywrightBrowserSession:
    """Reusable Playwright browser/context lifecycle for multi-page crawls."""

    def __init__(
        self,
        *,
        timeout_ms: float = 30_000,
        headless: bool = True,
        locale: str = "ko-KR",
        timezone_id: str = "Asia/Seoul",
        user_agent: str = "cluefin-etf/0.1",
        ignore_https_errors: bool = True,
    ) -> None:
        self.timeout_ms = timeout_ms
        self.headless = headless
        self.locale = locale
        self.timezone_id = timezone_id
        self.user_agent = user_agent
        self.ignore_https_errors = ignore_https_errors
        self._manager = None
        self._browser = None
        self._context = None

    def __enter__(self) -> "PlaywrightBrowserSession":
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise FetchError("Playwright is not installed") from exc

        self._manager = sync_playwright()
        playwright = self._manager.__enter__()
        self._browser = playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context(
            locale=self.locale,
            timezone_id=self.timezone_id,
            user_agent=self.user_agent,
            ignore_https_errors=self.ignore_https_errors,
        )
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._context is not None:
            self._context.close()
            self._context = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._manager is not None:
            self._manager.__exit__(exc_type, exc, traceback)
            self._manager = None

    def fetch_html(
        self,
        url: str,
        *,
        method: HttpMethod = "GET",
        headers: Mapping[str, str] | None = None,
        data: RequestData | None = None,
        referrer: str | None = None,
    ) -> tuple[str, str | None]:
        if self._context is None:
            raise FetchError("PlaywrightBrowserSession is not open")

        page = self._context.new_page()
        try:
            if method == "GET":
                page.goto(url, wait_until="networkidle", timeout=self.timeout_ms, referer=referrer)
                return page.content(), page.url

            page.goto(referrer or _origin_url(url), wait_until="networkidle", timeout=self.timeout_ms)
            result = page.evaluate(
                """async ({url, method, headers, body, referrer}) => {
                    const options = {
                        method,
                        headers,
                        body,
                        credentials: "include"
                    };
                    if (referrer) {
                        options.referrer = referrer;
                    }
                    const response = await fetch(url, options);
                    return {
                        ok: response.ok,
                        status: response.status,
                        text: await response.text(),
                        url: response.url
                    };
                }""",
                {
                    "url": url,
                    "method": method,
                    "headers": dict(headers or {}),
                    "body": _browser_request_body(data),
                    "referrer": referrer,
                },
            )
            if not result["ok"]:
                raise FetchError(f"Playwright fetch failed for {url}: status {result['status']}")
            return result["text"], result["url"]
        finally:
            page.close()


class PlaywrightFetcher:
    """Fetch ETF pages with Playwright for JavaScript-rendered pages."""

    def __init__(
        self,
        timeout_ms: float = 30_000,
        headless: bool = True,
        session: BrowserSession | None = None,
        locale: str = "ko-KR",
        timezone_id: str = "Asia/Seoul",
        user_agent: str = "cluefin-etf/0.1",
        ignore_https_errors: bool = True,
    ) -> None:
        self.timeout_ms = timeout_ms
        self.headless = headless
        self.session = session
        self.locale = locale
        self.timezone_id = timezone_id
        self.user_agent = user_agent
        self.ignore_https_errors = ignore_https_errors

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
        try:
            if self.session is not None:
                html, final_url = self.session.fetch_html(
                    url,
                    method=method,
                    headers=headers,
                    data=data,
                    referrer=referrer,
                )
            else:
                with PlaywrightBrowserSession(
                    timeout_ms=self.timeout_ms,
                    headless=self.headless,
                    locale=self.locale,
                    timezone_id=self.timezone_id,
                    user_agent=self.user_agent,
                    ignore_https_errors=self.ignore_https_errors,
                ) as session:
                    html, final_url = session.fetch_html(
                        url,
                        method=method,
                        headers=headers,
                        data=data,
                        referrer=referrer,
                    )
        except Exception as exc:
            if isinstance(exc, FetchError):
                raise
            raise FetchError(f"Playwright fetch failed for {url}") from exc

        return FetchResult(
            html=html,
            metadata=FetchMetadata(
                provider=ProviderName(provider),
                url=url,
                strategy="playwright",
                final_url=final_url,
                elapsed_ms=(time.perf_counter() - started_at) * 1000,
            ),
        )


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
        return result.model_copy(update={"metadata": result.metadata.model_copy(update={"fallback_reason": reason})})


def create_default_fetcher() -> FallbackFetcher:
    return FallbackFetcher()


def _browser_request_body(data: RequestData | None) -> str | None:
    if data is None:
        return None
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, str):
        return data
    return urlencode(data, doseq=True)


def _origin_url(url: str) -> str:
    parsed = urlsplit(url)
    return f"{parsed.scheme}://{parsed.netloc}"
