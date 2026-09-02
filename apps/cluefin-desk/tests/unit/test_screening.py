"""랭킹 화면 — 12개 탭이 채워지는지, 빈 표의 이유가 보이는지.

표만 있는 화면이라 "데이터 없음 / KIS 키 없음 / 조회 실패" 가 모두 같은 빈 표로 보였다.
탭별 상태줄이 그 셋을 구분하는지 Pilot 하네스로 확인한다.
"""

from pathlib import Path

import pytest
from textual.app import App
from textual.widgets import Static

import cluefin_desk
from cluefin_desk.data.screener import ScreeningItem
from cluefin_desk.screens.screening import KIS_TABLE_IDS, TAB_CONFIG, ScreeningScreen
from cluefin_desk.widgets.stock_table import StockScreeningTable

ALL_TABLE_IDS = [table_id for _, _, table_id in TAB_CONFIG]
KIWOOM_TABLE_IDS = [t for t in ALL_TABLE_IDS if t not in KIS_TABLE_IDS]

# screener 메서드명 ↔ 표 id — 화면의 매핑과 같아야 한다
LOADERS = {
    "table-gainers": "get_top_gainers",
    "table-losers": "get_top_losers",
    "table-volume": "get_top_volume",
    "table-value": "get_top_value",
    "table-foreigner": "get_top_foreigner_net_buy",
    "table-newhigh": "get_new_high_price",
    "table-volatility": "get_price_volatility",
    "table-margin": "get_top_margin_ratio",
    "table-dividend": "get_dividend_yield_top",
    "table-short": "get_short_selling_top",
    "table-credit": "get_credit_balance_top",
    "table-disparity": "get_disparity_index_top",
}


def _item(rank=1, code="005930", name="삼성전자"):
    return ScreeningItem(
        rank=rank, stock_code=code, stock_name=name, current_price="70000", change_rate="1.25", volume="12345678"
    )


class FakeScreener:
    """모든 로더가 같은 1행을 준다. `empty`/`failing` 으로 특정 표만 비우거나 터뜨린다."""

    def __init__(self, empty=(), failing=()):
        self._empty = set(empty)
        self._failing = set(failing)
        for table_id, method in LOADERS.items():
            setattr(self, method, self._loader_for(table_id))

    def _loader_for(self, table_id):
        def _load():
            if table_id in self._failing:
                raise RuntimeError(f"{table_id} 조회 실패")
            return [] if table_id in self._empty else [_item()]

        return _load


class FakeFetcher:
    def __init__(self, has_kis=True):
        self.has_kis = has_kis


class HarnessApp(App):
    """ScreeningScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱 —
    실제 `CluefinDeskApp` 은 생성만으로 실계좌 인증을 때린다."""

    # 실제 스타일시트를 물려 테스트가 tcss 회귀까지 잡게 한다.
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, screener, fetcher=None):
        super().__init__()
        self.screener = screener
        self.fetcher = fetcher or FakeFetcher()
        self._current_screen_key = "2"

    def on_mount(self) -> None:
        self.push_screen(ScreeningScreen())


def _status(screen, table_id: str) -> str:
    return str(screen.query_one(f"#status-{table_id}", Static).content)


def _rows(screen, table_id: str) -> int:
    return screen.query_one(f"#{table_id}", StockScreeningTable).row_count


async def _loaded(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


@pytest.mark.asyncio
class TestScreeningScreen:
    async def test_all_twelve_tabs_are_filled(self):
        app = HarnessApp(FakeScreener())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            for table_id in ALL_TABLE_IDS:
                assert _rows(screen, table_id) == 1, table_id
                assert _status(screen, table_id) == "1건", table_id

    async def test_without_kis_keys_only_kis_tabs_say_so(self):
        app = HarnessApp(FakeScreener(), FakeFetcher(has_kis=False))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            for table_id in KIS_TABLE_IDS:
                assert "KIS 키 없음" in _status(screen, table_id), table_id
                assert _rows(screen, table_id) == 0
            for table_id in KIWOOM_TABLE_IDS:
                assert _rows(screen, table_id) == 1, table_id

    async def test_empty_result_is_labelled_not_silent(self):
        app = HarnessApp(FakeScreener(empty={"table-newhigh"}))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _rows(screen, "table-newhigh") == 0
            assert "데이터 없음" in _status(screen, "table-newhigh")

    async def test_one_failing_tab_does_not_block_the_rest(self):
        app = HarnessApp(FakeScreener(failing={"table-volume"}))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            status = _status(screen, "table-volume")
            assert "로딩 실패" in status and "table-volume 조회 실패" in status
            # 같은 워커(키움 그룹)의 뒤 탭들도 채워진다
            assert _rows(screen, "table-value") == 1
            assert _rows(screen, "table-margin") == 1
            # 다른 워커(KIS 그룹)도 영향 없다
            assert _rows(screen, "table-dividend") == 1

    async def test_no_status_is_left_loading(self):
        app = HarnessApp(FakeScreener(), FakeFetcher(has_kis=False))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            for table_id in ALL_TABLE_IDS:
                assert "Loading" not in _status(screen, table_id), table_id
