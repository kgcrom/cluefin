"""테마·업종 화면 — 표가 채워지는지, 실패가 화면에 남는지.

2026-09-02 실측 회귀: 키움 응답 모델의 `max_length=20` 때문에 20자를 넘는 테마명이
오면 pydantic 이 응답 전체를 거부했고(`string_too_long`), 화면은 로그만 남긴 채 빈
표로 멈췄다. 모델 쪽 수정은 packages/cluefin-openapi 테스트가, "실패가 보이는지" 는
여기가 지킨다.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.widgets import DataTable, Static

import cluefin_desk
from cluefin_desk.screens.theme_sector import ThemeSectorScreen

LONG_THEME_NAME = "2차전지(전고체) 및 폐배터리 리사이클링 밸류체인"


def _theme_item(name=LONG_THEME_NAME, code="319"):
    return SimpleNamespace(thema_grp_cd=code, thema_nm=name, stk_num="12", flu_rt="1.25")


def _sector_item():
    return SimpleNamespace(stk_cd="001", stk_nm="종합(KOSPI)", flu_rt="0.42", rising="450", fall="380")


class FakeFetcher:
    def __init__(self, theme_error: bool = False, sector_error: bool = False, themes=None):
        self._theme_error = theme_error
        self._sector_error = sector_error
        self._themes = [_theme_item()] if themes is None else themes

    def get_theme_group(self):
        if self._theme_error:
            raise ValueError("1 validation error for 테마 thema_grp.56.thema_nm")
        return SimpleNamespace(body=SimpleNamespace(thema_grp=self._themes))

    def get_all_industry_index(self, inds_cd: str = "001"):
        if self._sector_error:
            raise RuntimeError("업종 조회 실패")
        return SimpleNamespace(body=SimpleNamespace(all_inds_idex=[_sector_item()]))

    def get_theme_group_stocks(self, thema_grp_cd: str):
        item = SimpleNamespace(
            stk_cd="005930", stk_nm="삼성전자", cur_prc="70,000", flu_rt="0.72", acc_trde_qty="12345678"
        )
        return SimpleNamespace(body=SimpleNamespace(thema_comp_stk=[item]))


class HarnessApp(App):
    """ThemeSectorScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱 —
    실제 `CluefinDeskApp` 은 생성만으로 실계좌 인증을 때린다."""

    # 실제 스타일시트를 물려 테스트가 tcss 회귀까지 잡게 한다.
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self._current_screen_key = "3"

    def on_mount(self) -> None:
        self.push_screen(ThemeSectorScreen())


def _status(screen, selector: str) -> str:
    return str(screen.query_one(selector, Static).content)


async def _loaded(app: HarnessApp, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


@pytest.mark.asyncio
class TestThemeSectorScreen:
    async def test_long_theme_name_reaches_the_table(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert screen.query_one("#theme-group-list", DataTable).row_count == 1
            assert "테마 1건" in _status(screen, "#theme-status")

    async def test_sector_table_filled(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert screen.query_one("#sector-list", DataTable).row_count == 1

    async def test_theme_failure_is_shown_not_only_logged(self):
        app = HarnessApp(FakeFetcher(theme_error=True))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            status = _status(screen, "#theme-status")
            assert "테마 목록 로딩 실패" in status
            assert "validation error" in status
            # 테마가 깨져도 업종은 계속 로드된다
            assert screen.query_one("#sector-list", DataTable).row_count == 1

    async def test_sector_failure_does_not_break_theme(self):
        app = HarnessApp(FakeFetcher(sector_error=True))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert "업종 목록 로딩 실패" in _status(screen, "#sector-chart-panel")
            assert screen.query_one("#theme-group-list", DataTable).row_count == 1

    async def test_empty_theme_response_says_so(self):
        app = HarnessApp(FakeFetcher(themes=[]))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _status(screen, "#theme-status") == "테마 데이터 없음"

    async def test_selecting_a_theme_loads_its_stocks(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            table = screen.query_one("#theme-group-list", DataTable)
            table.focus()
            await pilot.press("enter")
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert screen.query_one("#theme-stocks-table", DataTable).row_count == 1
