"""시장 개요 화면 — 급등/급락 컬럼 정렬과 KIS 수급·자금 패널.

2026-09-02 실측 회귀: KIS 자금동향은 정상 응답이었는데 패널에 높이·테두리가 없어
"안 보이는" 상태였고, 투자자 순매수는 KIS 가 오름차순으로 줘 한 달 전 5일이 보였다.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from rich.cells import cell_len
from textual.app import App
from textual.widgets import Static

import cluefin_desk
from cluefin_desk.screens.market_overview import MarketOverviewScreen


def _mover(name, price, rate):
    return SimpleNamespace(stock_name=name, current_price=price, change_rate=rate)


def _investor(date, prsn, frgn, orgn):
    return SimpleNamespace(stck_bsop_date=date, prsn_ntby_qty=prsn, frgn_ntby_qty=frgn, orgn_ntby_qty=orgn)


def _fund(date, dpmn, crdt, mmf):
    return SimpleNamespace(bsop_date=date, cust_dpmn_amt=dpmn, crdt_loan_rmnd=crdt, mmf_amt=mmf)


class TestMoverLines:
    def test_korean_and_ascii_names_align(self):
        items = [
            _mover("삼성전자", "70000", "3.5"),
            _mover("SK", "1200", "12.25"),
            _mover("LG에너지솔루션", "400000", "0.5"),
        ]
        lines = MarketOverviewScreen._format_mover_lines("급등", items, positive=True)
        body = lines[1:]
        # 현재가 컬럼이 끝나는 위치(셀 폭)가 모든 줄에서 같다
        widths = {cell_len(line.split("  [red]")[0]) for line in body}
        assert len(widths) == 1
        assert "[red]  +3.50%[/red]" in body[0]
        assert "[red] +12.25%[/red]" in body[1]

    def test_losers_use_blue_without_plus(self):
        lines = MarketOverviewScreen._format_mover_lines("급락", [_mover("A", "10", "-4.2")], positive=False)
        assert "[blue]  -4.20%[/blue]" in lines[1]

    def test_empty_says_so(self):
        assert MarketOverviewScreen._format_mover_lines("급등", [], positive=True)[1].strip() == "데이터 없음"


class TestKisLines:
    def test_investor_lines_show_latest_first(self):
        items = [_investor("20260803", "1", "2", "3"), _investor("20260901", "21879", "-100", "5")]
        lines = MarketOverviewScreen._format_kis_investor_lines(items)
        assert lines[2].startswith("20260901")
        assert "21,879" in lines[2]

    def test_fund_lines(self):
        lines = MarketOverviewScreen._format_kis_fund_lines([_fund("20260901", "981691", "334302", "2576303")])
        assert "억원" in lines[0]
        assert "981,691" in lines[2] and "2,576,303" in lines[2]

    def test_empty(self):
        assert "데이터 없음" in MarketOverviewScreen._format_kis_fund_lines([])[1]


class FakeFetcher:
    def __init__(self, has_kis=True, fund_error=False):
        self.has_kis = has_kis
        self._fund_error = fund_error

    def get_all_industry_index(self, inds_cd="001"):
        item = SimpleNamespace(
            stk_cd="001",
            stk_nm="종합(KOSPI)",
            cur_prc="6562.72",
            pred_pre="-27.30",
            flu_rt="-0.41",
            trde_qty="1000",
            pre_sig="5",
        )
        return SimpleNamespace(body=SimpleNamespace(all_inds_idex=[item]))

    def get_market_investor_trend_daily(self, market="KSP"):
        return [_investor("20260901", "21879", "-100", "5")]

    def get_market_fund_summary(self):
        if self._fund_error:
            raise RuntimeError("KIS 500")
        return [_fund("20260901", "981691", "334302", "2576303")]


class FakeScreener:
    def get_top_gainers(self):
        return [_mover("삼성전자", "70000", "3.5")]

    def get_top_losers(self):
        return [_mover("카카오", "40000", "-2.1")]


class HarnessApp(App):
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher, screener):
        super().__init__()
        self.fetcher = fetcher
        self.screener = screener
        self._current_screen_key = "1"

    def on_mount(self) -> None:
        self.push_screen(MarketOverviewScreen())


def _text(screen, selector):
    return str(screen.query_one(selector, Static).content)


async def _loaded(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


@pytest.mark.asyncio
class TestMarketOverviewScreen:
    async def test_kis_panels_are_filled_and_visible(self):
        app = HarnessApp(FakeFetcher(), FakeScreener())
        async with app.run_test(size=(140, 50)) as pilot:
            screen = await _loaded(app, pilot)
            assert "981,691" in _text(screen, "#kis-fund-panel")
            assert "21,879" in _text(screen, "#kis-investor-panel")
            fund = screen.query_one("#kis-fund-panel", Static)
            assert fund.region.width > 0 and fund.region.height > 0
            assert "+3.50%" in _text(screen, "#top-gainers-panel")

    async def test_without_kis_keys_panels_say_so(self):
        app = HarnessApp(FakeFetcher(has_kis=False), FakeScreener())
        async with app.run_test(size=(140, 50)) as pilot:
            screen = await _loaded(app, pilot)
            assert "KIS 키 없음" in _text(screen, "#kis-fund-panel")

    async def test_fund_failure_is_shown_and_investor_panel_survives(self):
        app = HarnessApp(FakeFetcher(fund_error=True), FakeScreener())
        async with app.run_test(size=(140, 50)) as pilot:
            screen = await _loaded(app, pilot)
            assert "로드 실패: KIS 500" in _text(screen, "#kis-fund-panel")
            assert "21,879" in _text(screen, "#kis-investor-panel")
