import requests

from cluefin_etf import (
    FallbackFetcher,
    FetchMetadata,
    FetchResult,
    PlaywrightFetcher,
    ProviderName,
    SimpleHttpFetcher,
    _fetchers,
)
from cluefin_etf._errors import FetchError


class FailingFetcher:
    def fetch(self, url: str, *, provider: ProviderName | str, validator=None) -> FetchResult:
        raise FetchError("failed")


class RecordingFetcher:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.calls: list[tuple[str, ProviderName | str]] = []

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None) -> FetchResult:
        self.calls.append((url, provider))
        return FetchResult(
            html="<html><body>usable ETF page content for tests</body></html>",
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy=self.strategy),
        )


def test_simple_http_fetcher_returns_html(requests_mock):
    requests_mock.get(
        "https://example.test/etf",
        text="<html>KODEX</html>",
        status_code=200,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    result = SimpleHttpFetcher().fetch("https://example.test/etf", provider="kodex")

    assert result.html == "<html>KODEX</html>"
    assert result.metadata.provider == ProviderName.KODEX
    assert result.metadata.strategy == "http"
    assert result.metadata.status_code == 200
    assert result.metadata.final_url == "https://example.test/etf"
    assert result.metadata.content_type is not None


def test_simple_http_fetcher_raises_fetch_error(requests_mock):
    requests_mock.get("https://example.test/etf", exc=requests.exceptions.Timeout)

    fetcher = SimpleHttpFetcher()

    try:
        fetcher.fetch("https://example.test/etf", provider="kodex")
    except FetchError:
        pass
    else:
        raise AssertionError("FetchError was not raised")


def test_fallback_fetcher_uses_primary_first():
    primary = RecordingFetcher("http")
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch("https://example.test/etf", provider="tiger")

    assert result.metadata.strategy == "http"
    assert primary.calls == [("https://example.test/etf", "tiger")]
    assert fallback.calls == []


def test_fallback_fetcher_uses_playwright_after_primary_failure():
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=FailingFetcher(), fallback=fallback).fetch(
        "https://example.test/etf",
        provider="tiger",
    )

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "failed"
    assert fallback.calls == [("https://example.test/etf", "tiger")]


def test_fallback_fetcher_uses_playwright_when_http_html_is_invalid():
    primary = RecordingFetcher("http")
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch(
        "https://example.test/etf",
        provider="tiger",
        validator=lambda fetch_result: "valid-marker" in fetch_result.html,
    )

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "validator_rejected"


def test_fallback_fetcher_does_not_fallback_when_validator_accepts_result():
    primary = RecordingFetcher("http")
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch(
        "https://example.test/etf",
        provider="tiger",
        validator=lambda fetch_result: "usable ETF page" in fetch_result.html,
    )

    assert result.metadata.strategy == "http"
    assert fallback.calls == []


def test_fallback_fetcher_uses_playwright_for_empty_html():
    primary = RecordingFetcher("http")
    primary.fetch = lambda url, *, provider, validator=None: FetchResult(
        html="",
        metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
    )
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch("https://example.test/etf", provider="tiger")

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "empty_html"


class FakeExternalBrowserSession:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.closed = False

    def fetch_html(self, url: str) -> tuple[str, str]:
        self.calls.append(url)
        return "<html><body>rendered ETF page content</body></html>", f"{url}?rendered=1"

    def close(self) -> None:
        self.closed = True


def test_playwright_fetcher_reuses_external_session_without_closing_it():
    session = FakeExternalBrowserSession()

    result = PlaywrightFetcher(session=session).fetch("https://example.test/etf", provider="kodex")

    assert result.html == "<html><body>rendered ETF page content</body></html>"
    assert result.metadata.strategy == "playwright"
    assert result.metadata.final_url == "https://example.test/etf?rendered=1"
    assert session.calls == ["https://example.test/etf"]
    assert session.closed is False


def test_playwright_fetcher_closes_internal_one_shot_session(monkeypatch):
    sessions = []

    class FakeOneShotSession:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs
            self.closed = False
            sessions.append(self)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback) -> None:
            self.closed = True

        def fetch_html(self, url: str) -> tuple[str, str]:
            return "<html><body>rendered ETF page content</body></html>", f"{url}?rendered=1"

    monkeypatch.setattr(_fetchers, "PlaywrightBrowserSession", FakeOneShotSession)

    result = PlaywrightFetcher(timeout_ms=1234, headless=False).fetch("https://example.test/etf", provider="kodex")

    assert result.metadata.strategy == "playwright"
    assert sessions[0].kwargs["timeout_ms"] == 1234
    assert sessions[0].kwargs["headless"] is False
    assert sessions[0].closed is True
