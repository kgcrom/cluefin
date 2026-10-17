"""`/` 종목 검색 모달 — 실제 앱 바인딩으로 열고, 고른 코드가 상세 화면 진입으로 이어지는지.

`CluefinDeskApp.__init__` 은 생성만으로 실계좌 인증을 하므로 건너뛰고(App.__init__ 만 부른다),
색인 로더와 상세 화면 진입만 가짜로 바꾼다. 바인딩·`action_search_stock`·`get_listing` 캐시는 실제 코드다.
"""

import threading
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.screen import Screen
from textual.widgets import Input, OptionList, Static

import cluefin_desk.app as app_module
from cluefin_desk.app import CluefinDeskApp
from cluefin_desk.data.listing import ListedStock, StockListing
from cluefin_desk.screens.stock_search import StockSearchScreen

LISTING = StockListing(
    [
        ListedStock("100010", "가나전자", "KOSPI", "거래소", "전기전자"),
        ListedStock("100015", "가나전자우", "KOSPI", "거래소", ""),
        ListedStock("200020", "가나바이오", "KOSDAQ", "코스닥", ""),
        ListedStock("0001A0", "마바테크", "KOSDAQ", "코스닥", ""),
    ]
)


class HarnessDeskApp(CluefinDeskApp):
    def __init__(self):
        App.__init__(self)
        self.fetcher = SimpleNamespace(kiwoom_client="fake-kiwoom")  # load_listing 이 가짜라 쓰이지 않는다
        self._current_screen_key = "1"
        self._listing = None
        self._listing_lock = threading.Lock()
        self.opened: list[str] = []

    def on_mount(self, event) -> None:
        # Textual 은 부모 클래스의 on_mount 도 부른다 — 막지 않으면 실제 시장 개요 화면이 뜬다
        event.prevent_default()
        self.push_screen(Screen())

    def open_stock_detail(self, stock_code):
        if stock_code:
            self.opened.append(stock_code)


@pytest.fixture
def loader_calls(monkeypatch):
    calls = []

    def fake_load_listing(kiwoom_client):
        calls.append(kiwoom_client)
        return LISTING

    monkeypatch.setattr(app_module, "load_listing", fake_load_listing)
    return calls


@pytest.fixture
def failing_loader(monkeypatch):
    def fake_load_listing(kiwoom_client):
        raise RuntimeError("ka10099 timeout")

    monkeypatch.setattr(app_module, "load_listing", fake_load_listing)


async def _settle(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()


async def _open_search(app, pilot):
    await pilot.press("slash")
    await _settle(app, pilot)
    assert isinstance(app.screen, StockSearchScreen)
    return app.screen


async def _type(app, pilot, text):
    app.screen.query_one("#search-input", Input).value = text
    await pilot.pause()


def _status(screen) -> str:
    return str(screen.query_one("#search-status", Static).content)


def _candidates(screen) -> list[str]:
    results = screen.query_one("#search-results", OptionList)
    return [results.get_option_at_index(i).id for i in range(results.option_count)]


@pytest.mark.asyncio
class TestStockSearch:
    async def test_slash_opens_and_index_loads(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            screen = await _open_search(app, pilot)
            assert _status(screen) == "4종목"
            assert screen.query_one("#search-input", Input).has_focus

    async def test_exact_name_enter_opens_detail(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            await _open_search(app, pilot)
            await _type(app, pilot, "가나전자")
            await pilot.press("enter")
            await pilot.pause()
            assert app.opened == ["100010"]
            assert not isinstance(app.screen, StockSearchScreen)

    async def test_ambiguous_name_moves_to_candidates(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            screen = await _open_search(app, pilot)
            await _type(app, pilot, "가나")
            assert _candidates(screen) == ["100010", "100015", "200020"]
            assert "후보 3개" in _status(screen)

            await pilot.press("enter")  # 여러 개라 열지 않고 후보 목록으로
            await pilot.pause()
            assert app.opened == []
            assert screen.query_one("#search-results", OptionList).has_focus

            await pilot.press("down", "enter")
            await pilot.pause()
            assert app.opened == ["100015"]

    async def test_digits_go_into_input_not_screen_bindings(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            screen = await _open_search(app, pilot)
            await pilot.press("1", "0", "0", "0")
            await pilot.pause()
            assert app.screen is screen
            assert screen.query_one("#search-input", Input).value == "1000"
            assert _candidates(screen) == ["100010", "100015"]

    async def test_lowercase_alphanumeric_code(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            await _open_search(app, pilot)
            await pilot.press(*"0001a0", "enter")
            await pilot.pause()
            assert app.opened == ["0001A0"]

    async def test_unknown_code_with_index_says_so(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            screen = await _open_search(app, pilot)
            await pilot.press(*"999999", "enter")
            await pilot.pause()
            assert app.opened == []
            assert _status(screen) == "맞는 종목 없음"

    async def test_index_failure_is_shown_and_code_still_opens(self, failing_loader):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            screen = await _open_search(app, pilot)
            assert "종목 목록 로딩 실패" in _status(screen)
            assert "ka10099 timeout" in _status(screen)
            await pilot.press(*"005930", "enter")
            await pilot.pause()
            assert app.opened == ["005930"]

    async def test_escape_closes_without_opening(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            await _open_search(app, pilot)
            await pilot.press("escape")
            await pilot.pause()
            assert app.opened == []
            assert not isinstance(app.screen, StockSearchScreen)

    async def test_index_is_fetched_once_per_app(self, loader_calls):
        app = HarnessDeskApp()
        async with app.run_test() as pilot:
            await _open_search(app, pilot)
            await pilot.press("escape")
            await pilot.pause()
            await _open_search(app, pilot)
            assert loader_calls == ["fake-kiwoom"]
