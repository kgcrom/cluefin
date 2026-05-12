from __future__ import annotations

import time
from collections.abc import Mapping
from typing import Protocol
from urllib.parse import urlencode, urlsplit

from cluefin_etf._errors import FetchError
from cluefin_etf._fetcher_types import HttpMethod, PageValidator, RequestData
from cluefin_etf._models import FetchMetadata, FetchResult, ProviderName


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
            html, final_url = self._fetch_html(url, method=method, headers=headers, data=data, referrer=referrer)
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

    def _fetch_html(
        self,
        url: str,
        *,
        method: HttpMethod,
        headers: Mapping[str, str] | None,
        data: RequestData | None,
        referrer: str | None,
    ) -> tuple[str, str | None]:
        if self.session is not None:
            return self.session.fetch_html(url, method=method, headers=headers, data=data, referrer=referrer)

        from cluefin_etf import _fetchers

        session_cls = getattr(_fetchers, "PlaywrightBrowserSession", PlaywrightBrowserSession)
        with session_cls(
            timeout_ms=self.timeout_ms,
            headless=self.headless,
            locale=self.locale,
            timezone_id=self.timezone_id,
            user_agent=self.user_agent,
            ignore_https_errors=self.ignore_https_errors,
        ) as session:
            return session.fetch_html(url, method=method, headers=headers, data=data, referrer=referrer)


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
