"""종목 상세 화면 — 패널 포매터와 탭 로딩 흐름.

이 화면의 탭들은 실패하거나 빈 응답을 받으면 예외 없이 "Loading ..." 자리표시자에
머문다. 그 상태를 잡기 위해 Pilot 하네스로 화면을 띄워 패널 텍스트를 확인한다.
"""

from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
from textual.app import App
from textual.widgets import DataTable, Static

import cluefin_desk
from cluefin_desk.screens.stock_detail import StockDetailScreen

STOCK_CODE = "005930"


# ---------------------------------------------------------------- 포매터 단위 테스트


def _broker_body():
    body = SimpleNamespace(stk_nm="삼성전자", stk_cd=STOCK_CODE, cur_prc="70,000", flu_rt="0.72")
    for i in range(1, 6):
        setattr(body, f"buy_trde_ori_nm_{i}", f"매수사{i}")
        setattr(body, f"buy_trde_qty_{i}", f"{i}00")
        setattr(body, f"sel_trde_ori_nm_{i}", f"매도사{i}")
        setattr(body, f"sel_trde_qty_{i}", f"{i}50")
    return body


class TestFormatBrokerLines:
    def test_lists_both_sides(self):
        text = "\n".join(StockDetailScreen._format_broker_lines(_broker_body()))
        assert "매매원 현황 — 삼성전자" in text
        assert "매수 상위" in text and "매도 상위" in text
        assert "매수사1" in text and "매도사5" in text


class TestFormatMarginLines:
    def test_empty_says_so(self):
        assert StockDetailScreen._format_margin_lines([]) == ["신용거래 추이 데이터 없음"]

    def test_rows_rendered(self):
        item = SimpleNamespace(dt="20260228", cur_prc="70,000", new="100", rpya="90", remn="1,000", remn_rt="0.5")
        text = "\n".join(StockDetailScreen._format_margin_lines([item]))
        assert "신용거래 추이" in text
        assert "20260228" in text


class TestFormatOpinionLines:
    def test_empty_says_so(self):
        assert StockDetailScreen._format_opinion_lines(None) == ["최근 6개월 내 증권사 투자의견이 없습니다."]

    def test_rows_rendered_with_percent(self):
        item = SimpleNamespace(
            stck_bsop_date="20260220",
            mbcr_name="미래에셋증권",
            invt_opnn="매수",
            rgbf_invt_opnn="매수",
            hts_goal_prc="95,000",
            dprt="35.7",
        )
        text = "\n".join(StockDetailScreen._format_opinion_lines([item]))
        assert "미래에셋증권" in text
        assert "35.7%" in text

    def test_missing_disparity_does_not_render_none(self):
        item = SimpleNamespace(
            stck_bsop_date="20260220",
            mbcr_name="미래에셋증권",
            invt_opnn="매수",
            rgbf_invt_opnn="-",
            hts_goal_prc="95,000",
            dprt=None,
        )
        text = "\n".join(StockDetailScreen._format_opinion_lines([item]))
        assert "None" not in text


def _kis_supply_args(**overrides):
    args = {
        "trend_df": pd.DataFrame(),
        "actions_df": pd.DataFrame(),
        "short_rows": [],
        "credit_rows": [],
        "program_rows": [],
    }
    args.update(overrides)
    return args


class TestFormatKisSupplyLines:
    def test_nothing_available_yields_no_lines(self):
        """빈 줄 목록이면 호출부가 패널을 건드리지 않는다 — 키움 절반만 남는다."""
        assert StockDetailScreen._format_kis_supply_lines(**_kis_supply_args()) == []

    def test_sections_are_independent(self):
        short = SimpleNamespace(
            stck_bsop_date="20260228", ssts_cntg_qty="1,000", ssts_vol_rlim="1.2", acml_ssts_cntg_qty="9,000"
        )
        text = "\n".join(StockDetailScreen._format_kis_supply_lines(**_kis_supply_args(short_rows=[short])))
        assert "공매도 추이 (KIS)" in text
        assert "신용잔고 추이" not in text
        assert "1.2%" in text

    def test_investor_trend_and_corporate_actions(self):
        index = pd.to_datetime(["2026-02-26", "2026-02-27"])
        trend_df = pd.DataFrame(
            {"개인": [1.0, -2.0], "외국인": [3.0, 4.0], "기관계": [5.0, 6.0], "연기금": [7.0, 8.0]}, index=index
        )
        actions_df = pd.DataFrame({"event": ["배당락"]}, index=pd.to_datetime(["2025-12-30"]))
        text = "\n".join(
            StockDetailScreen._format_kis_supply_lines(**_kis_supply_args(trend_df=trend_df, actions_df=actions_df))
        )
        assert "투자자별 일별 순매수" in text
        # 최신 일자가 위로 온다
        assert text.index("2026-02-27") < text.index("2026-02-26")
        assert "배당락" in text


# ------------------------------------------------------------------- Pilot 하네스


def _price_frame(rows: int = 60):
    index = pd.date_range("2026-01-01", periods=rows, freq="D")
    base = list(range(1000, 1000 + rows))
    return pd.DataFrame(
        {
            "open": base,
            "high": [v + 10 for v in base],
            "low": [v - 10 for v in base],
            "close": base,
            "volume": [10_000] * rows,
        },
        index=index,
    )


class FakeFetcher:
    def __init__(self, has_kis: bool = True, broker_error: bool = False):
        self.has_kis = has_kis
        self._broker_error = broker_error

    async def get_basic_data(self, stock_code):
        return pd.DataFrame([{"stock_code": stock_code, "stock_name": "삼성전자", "market_name": "KOSPI"}])

    async def get_stock_data(self, stock_code):
        return _price_frame()

    def get_institutional_investor_by_stock(self, stock_code):
        item = SimpleNamespace(
            dt="20260228",
            cur_prc="70,000",
            flu_rt="0.72",
            ind_invsr="100",
            frgnr_invsr="200",
            orgn="300",
        )
        return SimpleNamespace(body=SimpleNamespace(stk_invsr_orgn=[item]))

    def get_stock_trading_member(self, stock_code):
        if self._broker_error:
            raise RuntimeError("TR 폐지된 항목입니다")
        return SimpleNamespace(body=_broker_body())

    def get_margin_trading_trend(self, stock_code):
        item = SimpleNamespace(dt="20260228", cur_prc="70,000", new="100", rpya="90", remn="1,000", remn_rt="0.5")
        return SimpleNamespace(body=SimpleNamespace(crd_trde_trend=[item]))

    def get_investor_trend_daily(self, stock_code, days=10):
        index = pd.to_datetime(["2026-02-27"])
        return pd.DataFrame({"개인": [1.0], "외국인": [2.0], "기관계": [3.0], "연기금": [4.0]}, index=index)

    def get_corporate_actions(self, stock_code):
        return pd.DataFrame()

    def get_short_selling_trend(self, stock_code):
        return []

    def get_credit_balance_trend(self, stock_code):
        return []

    def get_program_trading_trend(self, stock_code):
        return []

    def get_investment_opinions(self, stock_code):
        return [
            SimpleNamespace(
                stck_bsop_date="20260220",
                mbcr_name="미래에셋증권",
                invt_opnn="매수",
                rgbf_invt_opnn="매수",
                hts_goal_prc="95,000",
                dprt="35.7",
            )
        ]


class HarnessApp(App):
    """StockDetailScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱 —
    실제 `CluefinDeskApp` 은 생성만으로 실계좌 인증을 때린다."""

    # 실제 스타일시트를 물려 테스트가 tcss 회귀까지 잡게 한다.
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self._current_screen_key = "1"

    def on_mount(self) -> None:
        self.push_screen(StockDetailScreen(STOCK_CODE))


def _panel_text(screen, selector: str) -> str:
    return str(screen.query_one(selector, Static).content)


async def _loaded(app: HarnessApp, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


@pytest.mark.asyncio
class TestStockDetailScreen:
    async def test_no_panel_is_left_loading(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            for selector in (
                "#detail-title-bar",
                "#broker-detail-content",
                "#supply-detail-content",
                "#opinion-detail-content",
            ):
                assert "Loading" not in _panel_text(screen, selector), f"{selector} 가 Loading 에서 멈췄다"

    async def test_each_tab_shows_its_own_data(self):
        app = HarnessApp(FakeFetcher())
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert "삼성전자" in _panel_text(screen, "#detail-title-bar")
            assert screen.query_one("#investor-detail-table", DataTable).row_count == 1
            assert "매매원 현황" in _panel_text(screen, "#broker-detail-content")
            assert "신용거래 추이" in _panel_text(screen, "#supply-detail-content")
            assert "투자자별 일별 순매수" in _panel_text(screen, "#kis-supply-content")
            assert "미래에셋증권" in _panel_text(screen, "#opinion-detail-content")

    async def test_one_failing_tab_does_not_block_the_others(self):
        app = HarnessApp(FakeFetcher(broker_error=True))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            broker = _panel_text(screen, "#broker-detail-content")
            assert "매매원 로딩 실패" in broker and "TR 폐지" in broker
            assert "신용거래 추이" in _panel_text(screen, "#supply-detail-content")
            assert "미래에셋증권" in _panel_text(screen, "#opinion-detail-content")

    async def test_without_kis_only_kis_panels_degrade(self):
        app = HarnessApp(FakeFetcher(has_kis=False))
        async with app.run_test() as pilot:
            screen = await _loaded(app, pilot)
            assert "KIS_APP_KEY" in _panel_text(screen, "#opinion-detail-content")
            assert _panel_text(screen, "#kis-supply-content") == ""
            assert "신용거래 추이" in _panel_text(screen, "#supply-detail-content")
