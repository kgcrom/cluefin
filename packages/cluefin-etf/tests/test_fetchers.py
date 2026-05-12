import requests

from cluefin_etf import (
    FallbackFetcher,
    FetchMetadata,
    FetchResult,
    PlaywrightFetcher,
    ProviderName,
    RateLimitedFetcher,
    SimpleHttpFetcher,
    _fetchers,
)
from cluefin_etf._errors import FetchError


class FailingFetcher:
    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        raise FetchError("failed")


class RecordingFetcher:
    def __init__(self, strategy: str) -> None:
        self.strategy = strategy
        self.calls: list[tuple[str, ProviderName | str, dict]] = []

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        self.calls.append((url, provider, kwargs))
        return FetchResult(
            html="<html><body>usable ETF page content for tests</body></html>",
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy=self.strategy),
        )


class StaticHtmlFetcher:
    def __init__(self, html: str, strategy: str = "playwright") -> None:
        self.html = html
        self.strategy = strategy

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        return FetchResult(
            html=self.html,
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


def test_simple_http_fetcher_posts_form_data(requests_mock):
    requests_mock.post(
        "https://example.test/etf-list",
        text='{"ok":true}',
        status_code=200,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )

    result = SimpleHttpFetcher().fetch(
        "https://example.test/etf-list",
        provider="kiwoom",
        method="POST",
        headers={"X-Requested-With": "XMLHttpRequest"},
        data={"pageNo": "1"},
        referrer="https://example.test/etf",
    )

    assert result.html == '{"ok":true}'
    assert result.metadata.provider == ProviderName.KIWOOM
    assert result.metadata.strategy == "http"
    assert requests_mock.last_request.method == "POST"
    assert requests_mock.last_request.text == "pageNo=1"
    assert requests_mock.last_request.headers["Referer"] == "https://example.test/etf"
    assert requests_mock.last_request.headers["X-Requested-With"] == "XMLHttpRequest"


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
    assert primary.calls == [
        ("https://example.test/etf", "tiger", {"method": "GET", "headers": None, "data": None, "referrer": None})
    ]
    assert fallback.calls == []


def test_fallback_fetcher_uses_playwright_after_primary_failure():
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=FailingFetcher(), fallback=fallback).fetch(
        "https://example.test/etf",
        provider="tiger",
    )

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "failed"
    assert fallback.calls == [
        ("https://example.test/etf", "tiger", {"method": "GET", "headers": None, "data": None, "referrer": None})
    ]


def test_fallback_fetcher_preserves_post_request_options_for_fallback():
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=FailingFetcher(), fallback=fallback).fetch(
        "https://example.test/etf-list",
        provider="kiwoom",
        method="POST",
        headers={"X-Requested-With": "XMLHttpRequest"},
        data={"pageNo": "1"},
        referrer="https://example.test/etf",
    )

    assert result.metadata.strategy == "playwright"
    assert fallback.calls == [
        (
            "https://example.test/etf-list",
            "kiwoom",
            {
                "method": "POST",
                "headers": {"X-Requested-With": "XMLHttpRequest"},
                "data": {"pageNo": "1"},
                "referrer": "https://example.test/etf",
            },
        )
    ]


def test_fallback_fetcher_uses_playwright_when_http_html_is_invalid():
    primary = StaticHtmlFetcher("<html><body>invalid primary page content</body></html>", strategy="http")
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch(
        "https://example.test/etf",
        provider="tiger",
        validator=lambda fetch_result: "usable ETF page" in fetch_result.html,
    )

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "validator_rejected"


def test_fallback_fetcher_raises_fetch_error_when_fallback_validator_rejects_result():
    primary = StaticHtmlFetcher("<html><body>invalid primary page content</body></html>", strategy="http")
    fallback = StaticHtmlFetcher("<html><body>invalid fallback page content</body></html>")
    fetcher = FallbackFetcher(primary=primary, fallback=fallback)

    try:
        fetcher.fetch(
            "https://example.test/etf",
            provider="tiger",
            validator=lambda fetch_result: "valid-marker" in fetch_result.html,
        )
    except FetchError as exc:
        assert "validator_rejected" in str(exc)
        assert "primary reason: validator_rejected" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")


def test_fallback_fetcher_raises_fetch_error_when_fallback_html_is_empty():
    fetcher = FallbackFetcher(primary=FailingFetcher(), fallback=StaticHtmlFetcher(""))

    try:
        fetcher.fetch("https://example.test/etf", provider="tiger")
    except FetchError as exc:
        assert "empty_html" in str(exc)
        assert "primary reason: failed" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")


def test_fallback_fetcher_raises_fetch_error_when_fallback_html_is_too_short():
    fetcher = FallbackFetcher(primary=FailingFetcher(), fallback=StaticHtmlFetcher("<html></html>"))

    try:
        fetcher.fetch("https://example.test/etf", provider="tiger")
    except FetchError as exc:
        assert "html_too_short" in str(exc)
        assert "primary reason: failed" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")


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
    primary.fetch = lambda url, *, provider, validator=None, **kwargs: FetchResult(
        html="",
        metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
    )
    fallback = RecordingFetcher("playwright")

    result = FallbackFetcher(primary=primary, fallback=fallback).fetch("https://example.test/etf", provider="tiger")

    assert result.metadata.strategy == "playwright"
    assert result.metadata.fallback_reason == "empty_html"


def test_rate_limited_fetcher_sleeps_between_consecutive_page_calls():
    now = 100.0
    sleeps = []

    def clock() -> float:
        return now

    def sleeper(seconds: float) -> None:
        nonlocal now
        sleeps.append(seconds)
        now += seconds

    fetcher = RateLimitedFetcher(
        RecordingFetcher("http"),
        min_interval_seconds=1.0,
        clock=clock,
        sleeper=sleeper,
    )

    fetcher.fetch("https://example.test/page-1", provider="kodex")
    now += 0.25
    fetcher.fetch("https://example.test/page-2", provider="kodex")

    assert sleeps == [0.75]


def test_rate_limited_fetcher_records_failed_calls_before_next_delay():
    now = 100.0
    sleeps = []
    fetcher = RateLimitedFetcher(
        FailingFetcher(),
        min_interval_seconds=1.0,
        clock=lambda: now,
        sleeper=sleeps.append,
    )

    try:
        fetcher.fetch("https://example.test/page-1", provider="kodex")
    except FetchError:
        pass
    else:
        raise AssertionError("FetchError was not raised")

    fetcher.fetcher = RecordingFetcher("http")
    fetcher.fetch("https://example.test/page-2", provider="kodex")

    assert sleeps == [1.0]


def test_create_default_fetcher_rate_limits_fallback_fetcher():
    fetcher = _fetchers.create_default_fetcher()

    assert isinstance(fetcher, RateLimitedFetcher)
    assert isinstance(fetcher.fetcher, FallbackFetcher)


class FakeExternalBrowserSession:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.closed = False

    def fetch_html(self, url: str, **kwargs) -> tuple[str, str]:
        self.calls.append((url, kwargs))
        return "<html><body>rendered ETF page content</body></html>", f"{url}?rendered=1"

    def close(self) -> None:
        self.closed = True


def test_playwright_fetcher_reuses_external_session_without_closing_it():
    session = FakeExternalBrowserSession()

    result = PlaywrightFetcher(session=session).fetch("https://example.test/etf", provider="kodex")

    assert result.html == "<html><body>rendered ETF page content</body></html>"
    assert result.metadata.strategy == "playwright"
    assert result.metadata.final_url == "https://example.test/etf?rendered=1"
    assert session.calls == [
        ("https://example.test/etf", {"method": "GET", "headers": None, "data": None, "referrer": None})
    ]
    assert session.closed is False


def test_playwright_fetcher_passes_post_request_options_to_session():
    session = FakeExternalBrowserSession()

    PlaywrightFetcher(session=session).fetch(
        "https://example.test/etf-list",
        provider="kiwoom",
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        data={"pageNo": "1"},
        referrer="https://example.test/etf",
    )

    assert session.calls == [
        (
            "https://example.test/etf-list",
            {
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                "data": {"pageNo": "1"},
                "referrer": "https://example.test/etf",
            },
        )
    ]


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

        def fetch_html(self, url: str, **kwargs) -> tuple[str, str]:
            return "<html><body>rendered ETF page content</body></html>", f"{url}?rendered=1"

    monkeypatch.setattr(_fetchers, "PlaywrightBrowserSession", FakeOneShotSession)

    result = PlaywrightFetcher(timeout_ms=1234, headless=False).fetch("https://example.test/etf", provider="kodex")

    assert result.metadata.strategy == "playwright"
    assert sessions[0].kwargs["timeout_ms"] == 1234
    assert sessions[0].kwargs["headless"] is False
    assert sessions[0].kwargs["ignore_https_errors"] is True
    assert sessions[0].closed is True


def test_playwright_browser_session_stores_configuration():
    session = _fetchers.PlaywrightBrowserSession(
        timeout_ms=1234,
        headless=False,
        locale="ko-KR",
        timezone_id="Asia/Seoul",
        user_agent="test-agent",
        ignore_https_errors=False,
    )

    assert session.timeout_ms == 1234
    assert session.headless is False
    assert session.locale == "ko-KR"
    assert session.timezone_id == "Asia/Seoul"
    assert session.user_agent == "test-agent"
    assert session.ignore_https_errors is False
    assert session._manager is None
    assert session._browser is None
    assert session._context is None


def test_playwright_browser_session_requires_open_context():
    session = _fetchers.PlaywrightBrowserSession()

    try:
        session.fetch_html("https://example.test/etf")
    except FetchError as exc:
        assert "not open" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")


class FakePlaywrightPage:
    def __init__(self) -> None:
        self.goto_calls = []
        self.evaluate_calls = []
        self.url = "https://example.test/etf?rendered=1"
        self.closed = False
        self.evaluate_result = {
            "ok": True,
            "status": 200,
            "text": "<html><body>rendered ETF page content</body></html>",
            "url": "https://example.test/api?rendered=1",
        }

    def goto(self, url: str, **kwargs) -> None:
        self.goto_calls.append((url, kwargs))

    def content(self) -> str:
        return "<html><body>rendered ETF page content</body></html>"

    def evaluate(self, script: str, payload: dict):
        self.evaluate_calls.append((script, payload))
        return self.evaluate_result

    def close(self) -> None:
        self.closed = True


class FakePlaywrightContext:
    def __init__(self, page: FakePlaywrightPage) -> None:
        self.page = page

    def new_page(self) -> FakePlaywrightPage:
        return self.page


def test_playwright_browser_session_fetches_get_page_from_open_context():
    page = FakePlaywrightPage()
    session = _fetchers.PlaywrightBrowserSession(timeout_ms=1234)
    session._context = FakePlaywrightContext(page)

    html, final_url = session.fetch_html("https://example.test/etf", referrer="https://example.test")

    assert html == "<html><body>rendered ETF page content</body></html>"
    assert final_url == "https://example.test/etf?rendered=1"
    assert page.goto_calls == [
        (
            "https://example.test/etf",
            {"wait_until": "networkidle", "timeout": 1234, "referer": "https://example.test"},
        )
    ]
    assert page.closed is True


def test_playwright_browser_session_fetches_post_with_encoded_body():
    page = FakePlaywrightPage()
    session = _fetchers.PlaywrightBrowserSession(timeout_ms=1234)
    session._context = FakePlaywrightContext(page)

    html, final_url = session.fetch_html(
        "https://example.test/api",
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"pageNo": "1", "type": ["domestic", "bond"]},
        referrer="https://example.test/etf",
    )

    assert html == "<html><body>rendered ETF page content</body></html>"
    assert final_url == "https://example.test/api?rendered=1"
    assert page.goto_calls == [("https://example.test/etf", {"wait_until": "networkidle", "timeout": 1234})]
    assert page.evaluate_calls[0][1] == {
        "url": "https://example.test/api",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "body": "pageNo=1&type=domestic&type=bond",
        "referrer": "https://example.test/etf",
    }
    assert page.closed is True


def test_playwright_browser_session_uses_origin_for_post_without_referrer():
    page = FakePlaywrightPage()
    session = _fetchers.PlaywrightBrowserSession(timeout_ms=1234)
    session._context = FakePlaywrightContext(page)

    session.fetch_html("https://example.test/api", method="POST", data=b"pageNo=1")

    assert page.goto_calls == [("https://example.test", {"wait_until": "networkidle", "timeout": 1234})]
    assert page.evaluate_calls[0][1]["body"] == "pageNo=1"


def test_playwright_browser_session_raises_fetch_error_for_failed_post_response():
    page = FakePlaywrightPage()
    page.evaluate_result = {"ok": False, "status": 500, "text": "failed", "url": "https://example.test/api"}
    session = _fetchers.PlaywrightBrowserSession()
    session._context = FakePlaywrightContext(page)

    try:
        session.fetch_html("https://example.test/api", method="POST")
    except FetchError as exc:
        assert "status 500" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")
    assert page.closed is True


def test_playwright_browser_session_exit_closes_open_resources():
    closed = []

    class Closeable:
        def __init__(self, name: str) -> None:
            self.name = name

        def close(self) -> None:
            closed.append(self.name)

    class Manager:
        def __exit__(self, exc_type, exc, traceback) -> None:
            closed.append("manager")

    session = _fetchers.PlaywrightBrowserSession()
    session._context = Closeable("context")
    session._browser = Closeable("browser")
    session._manager = Manager()

    session.__exit__(None, None, None)

    assert closed == ["context", "browser", "manager"]
    assert session._context is None
    assert session._browser is None
    assert session._manager is None


def test_playwright_fetcher_wraps_unexpected_session_errors():
    class BrokenSession:
        def fetch_html(self, url: str, **kwargs) -> tuple[str, str]:
            raise ValueError("broken")

    fetcher = PlaywrightFetcher(session=BrokenSession())

    try:
        fetcher.fetch("https://example.test/etf", provider="kodex")
    except FetchError as exc:
        assert "Playwright fetch failed" in str(exc)
    else:
        raise AssertionError("FetchError was not raised")
