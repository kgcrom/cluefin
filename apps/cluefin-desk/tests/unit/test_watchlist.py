"""관심종목 화면 — 그룹 → 종목 → 시세가 채워지는지, 비었거나 실패한 이유가 보이는지."""

from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.screen import Screen
from textual.widgets import DataTable, Static

import cluefin_desk
import cluefin_desk.screens.stock_detail as stock_detail_module
from cluefin_desk.screens.watchlist import NO_GROUPS, NO_HTS, WatchlistScreen


def _group(code, name, count):
    return SimpleNamespace(inter_grp_code=code, inter_grp_name=name, ask_cnt=f"{count:03d}")


def _stock(code, name):
    return SimpleNamespace(jong_code=code, hts_kor_isnm=name, fid_mrkt_cls_code="J")


def _quote(code, name, price="14530", rate="3.12"):
    return SimpleNamespace(
        inter_shrn_iscd=code,
        inter_kor_isnm=name,
        inter2_prpr=price,
        prdy_ctrt=rate,
        acml_vol="38079",
        acml_tr_pbmn="551826555",
        inter2_oprc="13950",
        inter2_hgpr="14660",
        inter2_lwpr="13950",
    )


GROUPS = [_group("000", "1그룹", 2), _group("001", "2그룹", 0), _group("002", "3그룹", 1)]
STOCKS = {
    "000": [_stock("100010", "가나전자"), _stock("0001A0", "마바테크")],
    "001": [],
    "002": [_stock("200020", "다라바이오")],
}


class FakeFetcher:
    def __init__(self, has_hts=True, groups=None, group_error=None):
        self.has_hts = has_hts
        self._groups = GROUPS if groups is None else groups
        self._group_error = group_error
        self.calls = []

    def get_watchlist_groups(self):
        self.calls.append("groups")
        if self._group_error:
            raise RuntimeError(self._group_error)
        return self._groups

    def get_watchlist_stocks(self, group_code):
        self.calls.append(("stocks", group_code))
        return STOCKS[group_code]

    def get_watchlist_quotes(self, pairs):
        self.calls.append(("quotes", tuple(pairs)))
        return [_quote(code, f"{code}시세명") for _, code in pairs]


class HarnessApp(App):
    """WatchlistScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱 —
    실제 `CluefinDeskApp` 은 생성만으로 실계좌 인증을 때린다."""

    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self._current_screen_key = "6"

    def on_mount(self) -> None:
        self.push_screen(WatchlistScreen())


class FakeDetail(Screen):
    def __init__(self, stock_code):
        super().__init__()
        self.stock_code = stock_code


async def _loaded(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


def _status(screen) -> str:
    return str(screen.query_one("#watchlist-status", Static).content)


def _table(screen, table_id) -> DataTable:
    return screen.query_one(f"#{table_id}", DataTable)


def _codes(screen) -> list[str]:
    table = _table(screen, "watchlist-stocks")
    return [str(table.coordinate_to_cell_key((i, 0)).row_key.value) for i in range(table.row_count)]


@pytest.mark.asyncio
class TestWatchlistScreen:
    async def test_without_hts_id_says_so_and_calls_nothing(self):
        fetcher = FakeFetcher(has_hts=False)
        app = HarnessApp(fetcher)
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _status(screen) == NO_HTS
            assert fetcher.calls == []

    async def test_groups_then_first_group_quotes(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _table(screen, "watchlist-groups").row_count == 3
            assert _codes(screen) == ["100010", "0001A0"]
            assert "1그룹 — 2종목" in _status(screen)
            assert fetcher.calls == ["groups", ("stocks", "000"), ("quotes", (("J", "100010"), ("J", "0001A0")))]

    async def test_no_groups(self):
        app = HarnessApp(FakeFetcher(groups=[]))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _status(screen) == NO_GROUPS
            assert _table(screen, "watchlist-stocks").row_count == 0

    async def test_selecting_empty_group_says_no_stocks(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            groups = _table(screen, "watchlist-groups")
            groups.focus()
            groups.move_cursor(row=1)
            await pilot.press("enter")
            screen = await _loaded(app, pilot)
            assert _table(screen, "watchlist-stocks").row_count == 0
            assert _status(screen) == "2그룹 — 종목 없음"
            assert ("quotes", ()) not in fetcher.calls  # 빈 그룹은 시세를 부르지 않는다

    async def test_group_failure_is_shown(self):
        app = HarnessApp(FakeFetcher(group_error="KIS API Error [EGW00201]: 초당 거래건수 초과"))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert "관심 그룹 로딩 실패" in _status(screen)
            assert "EGW00201" in _status(screen)

    async def test_refresh_keeps_selected_group(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            groups = _table(screen, "watchlist-groups")
            groups.focus()
            groups.move_cursor(row=2)
            await pilot.press("enter")
            await _loaded(app, pilot)
            fetcher.calls.clear()

            await pilot.press("r")
            screen = await _loaded(app, pilot)
            assert fetcher.calls[:2] == ["groups", ("stocks", "002")]
            assert _codes(screen) == ["200020"]

    async def test_enter_on_stock_opens_detail(self, monkeypatch):
        monkeypatch.setattr(stock_detail_module, "StockDetailScreen", FakeDetail)
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            stocks = _table(screen, "watchlist-stocks")
            stocks.focus()
            stocks.move_cursor(row=1)
            await pilot.press("enter")
            await pilot.pause()
            assert isinstance(app.screen, FakeDetail)
            assert app.screen.stock_code == "0001A0"


class TestFormatQuoteRows:
    def test_formats_numbers_rate_and_eok(self):
        rows = WatchlistScreen._format_quote_rows([_stock("100010", "가나전자")], [_quote("100010", "가나전자")])
        assert rows == [
            ("100010", "가나전자", "14,530", "[red]+3.12%[/red]", "38,079", "5.5", "13,950", "14,660", "13,950")
        ]

    def test_negative_and_flat_rates(self):
        assert WatchlistScreen._rate("-1.5") == "[blue]-1.50%[/blue]"
        assert WatchlistScreen._rate("0.00") == "0.00%"
        assert WatchlistScreen._rate("") == "-"

    def test_missing_quote_keeps_code_and_name(self):
        rows = WatchlistScreen._format_quote_rows([_stock("100010", "가나전자")], [])
        assert rows == [("100010", "가나전자", "-", "-", "-", "-", "-", "-", "-")]

    def test_keeps_group_order_and_escapes_markup(self):
        stocks = [_stock("200020", "[bold]다라"), _stock("100010", "가나전자")]
        quotes = [_quote("100010", "가나전자"), _quote("200020", "")]
        rows = WatchlistScreen._format_quote_rows(stocks, quotes)
        assert [row[0] for row in rows] == ["200020", "100010"]
        assert rows[0][1] == "\\[bold]다라"
