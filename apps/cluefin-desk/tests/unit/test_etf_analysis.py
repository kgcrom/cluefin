"""ETF 화면 — 표·상태줄이 채워지는지, N 키 NAV 패널이 실패까지 보여주는지.

이전엔 시세 조회가 실패하거나 비어도 표가 빈 채로 멈췄고, NAV 상세 실패는 로그에만
남았다. 포매터는 순수 함수로, 화면 흐름은 Pilot 하네스로 본다.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.widgets import DataTable, Static

import cluefin_desk
from cluefin_desk.screens.etf_analysis import NAV_HINT, EtfAnalysisScreen

# ---------------------------------------------------------------- 포매터 단위 테스트


def _etf(code="069500", name="KODEX 200", pre_rt="1.25", nav="40,123.45", trace="0.12", qty="1234567"):
    return SimpleNamespace(
        stk_cd=code, stk_nm=name, close_pric="40,170", pre_rt=pre_rt, nav=nav, trace_eor_rt=trace, trde_qty=qty
    )


class TestFormatEtfRow:
    def test_full_row(self):
        row = EtfAnalysisScreen._format_etf_row(1, _etf())
        assert row[0] == "1" and row[1] == "069500" and row[2] == "KODEX 200"
        assert "+1.25%" in row[4]
        assert row[5] == "40,123.45"
        assert row[6] == "0.12%"
        assert row[7] == "1,234,567"

    def test_blank_and_dash_values_do_not_raise(self):
        """키움은 없는 값을 "" 또는 "-" 로 준다."""
        row = EtfAnalysisScreen._format_etf_row(2, _etf(pre_rt="-", nav="", trace="", qty=""))
        assert row[4] == "0.00%"
        assert row[5] == "-" and row[6] == "-" and row[7] == "-"

    def test_negative_rate_is_blue(self):
        row = EtfAnalysisScreen._format_etf_row(1, _etf(pre_rt="-0.8"))
        assert "[blue]-0.80%" in row[4]


def _nav_row():
    return SimpleNamespace(stck_bsop_date="20260901", stck_clpr="40,170", nav="40,123.45", dprt="0.12")


def _component():
    return SimpleNamespace(hts_kor_isnm="삼성전자", stck_prpr="70,000", prdy_ctrt="0.72", etf_cnfg_issu_rlim="31.2")


class TestFormatNavLines:
    def test_both_sections(self):
        text = "\n".join(EtfAnalysisScreen._format_nav_lines("069500", [_nav_row()], [_component()]))
        assert "069500 — NAV 괴리 추이" in text
        assert "20260901" in text and "0.12%" in text
        assert "구성종목 상위" in text and "삼성전자" in text and "비중 31.2%" in text

    def test_empty_sections_say_so(self):
        text = "\n".join(EtfAnalysisScreen._format_nav_lines("069500", [], None))
        assert "NAV 데이터 없음" in text
        assert "구성종목 데이터 없음" in text


# ------------------------------------------------------------------- Pilot 하네스


class FakeFetcher:
    def __init__(self, has_kis=True, items=None, prices_error=False, nav_error=False):
        self.has_kis = has_kis
        self._items = [_etf()] if items is None else items
        self._prices_error = prices_error
        self._nav_error = nav_error

    def get_etf_full_price(self):
        if self._prices_error:
            raise RuntimeError("ka40004 조회 실패")
        return SimpleNamespace(body=SimpleNamespace(etfall_mrpr=self._items))

    def get_etf_nav_daily_trend(self, stk_cd, days=30):
        if self._nav_error:
            raise RuntimeError("NAV 조회 실패")
        return [_nav_row()]

    def get_etf_component_prices(self, stk_cd):
        return [_component()]


class HarnessApp(App):
    """EtfAnalysisScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱 —
    실제 `CluefinDeskApp` 은 생성만으로 실계좌 인증을 때린다."""

    # 실제 스타일시트를 물려 테스트가 tcss 회귀까지 잡게 한다.
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self._current_screen_key = "4"

    def on_mount(self) -> None:
        self.push_screen(EtfAnalysisScreen())


def _text(screen, selector: str) -> str:
    return str(screen.query_one(selector, Static).content)


async def _loaded(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


async def _press_nav(app, pilot, screen):
    screen.query_one("#etf-price-table", DataTable).focus()
    await pilot.press("n")
    await app.workers.wait_for_complete()
    await pilot.pause()


@pytest.mark.asyncio
class TestEtfScreen:
    async def test_table_filled_and_status_counts(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert screen.query_one("#etf-price-table", DataTable).row_count == 1
            assert _text(screen, "#etf-status") == "ETF 1건 (전체 1)"
            assert _text(screen, "#etf-kis-panel") == NAV_HINT

    async def test_empty_response_is_labelled(self):
        app = HarnessApp(FakeFetcher(items=[]))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert _text(screen, "#etf-status") == "ETF 데이터 없음"

    async def test_price_failure_is_shown_not_only_logged(self):
        app = HarnessApp(FakeFetcher(prices_error=True))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            status = _text(screen, "#etf-status")
            assert "ETF 시세 로딩 실패" in status and "ka40004" in status

    async def test_nav_key_fills_panel(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            await _press_nav(app, pilot, screen)
            panel = _text(screen, "#etf-kis-panel")
            assert "069500 — NAV 괴리 추이" in panel and "삼성전자" in panel

    async def test_nav_key_without_kis_explains(self):
        app = HarnessApp(FakeFetcher(has_kis=False))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            await _press_nav(app, pilot, screen)
            assert "KIS_APP_KEY" in _text(screen, "#etf-kis-panel")

    async def test_nav_failure_is_shown_in_panel(self):
        app = HarnessApp(FakeFetcher(nav_error=True))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            await _press_nav(app, pilot, screen)
            panel = _text(screen, "#etf-kis-panel")
            assert "NAV 상세 로딩 실패" in panel and "NAV 조회 실패" in panel
