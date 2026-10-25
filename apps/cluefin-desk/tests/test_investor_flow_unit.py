"""투자자 화면 — 업종별투자자순매수(ka10051) 스케일과 업종 → 구성 종목 동선.

2026-09-02 실측 회귀: ka10051 은 등락률·지수를 100배 정수로 준다 (`-210` = -2.10%) 는데
그대로 float 로 찍어 -210.00% 로 보였고, mrkt_tp="0001" 은 서버가 코스닥으로 해석했다.
업종 표에서 Enter 를 눌러도 아무 일도 없었다 — DataTable 이 Enter 를 먼저 먹기 때문.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.widgets import DataTable, Static

import cluefin_desk
from cluefin_desk.screens.investor_flow import InvestorFlowScreen


def _sector(code="106", name="제조", cur_prc="-270406", flu_rt="-210", frgn="-2668", ind="+3698"):
    return SimpleNamespace(
        inds_cd=code, inds_nm=name, cur_prc=cur_prc, flu_rt=flu_rt, frgnr_netprps=frgn, ind_netprps=ind
    )


class TestSectorRow:
    def test_scale_is_divided_by_100(self):
        name, index, rate, frgn, ind = InvestorFlowScreen._format_sector_row(_sector())
        assert name == "제조"
        assert index == "2,704.06"
        assert rate == "[blue]-2.10%[/blue]"
        assert frgn == "-2,668" and ind == "+3,698"

    def test_positive_rate_is_red_with_plus(self):
        _, _, rate, _, _ = InvestorFlowScreen._format_sector_row(_sector(cur_prc="+49457", flu_rt="+48"))
        assert rate == "[red]+0.48%[/red]"

    def test_blank_values(self):
        _, index, rate, _, _ = InvestorFlowScreen._format_sector_row(_sector(cur_prc="", flu_rt="-"))
        assert index == "-" and rate == "-"


class FakeFetcher:
    def __init__(self):
        self.calls = []

    def _resp(self, **body):
        return SimpleNamespace(headers={}, body=SimpleNamespace(**body))

    def get_top_foreigner_period_trading(self, trde_tp="1"):
        return self._resp(for_dt_trde_upper=[])

    def get_top_intraday_trading_by_investor(self, trde_tp="1", orgn_tp="1000"):
        return self._resp(opmr_invsr_trde_upper=[])

    def get_top_50_program_net_buy(self):
        return self._resp(prm_netprps_upper_50=[])

    def get_industry_investor_net_buy(self, mrkt_tp="0", amt_qty_tp="1"):
        self.calls.append(("ka10051", mrkt_tp))
        if mrkt_tp == "1":
            return self._resp(inds_netprps=[_sector(code="101", name="종합(KOSDAQ)", cur_prc="-80398")])
        return self._resp(
            inds_netprps=[_sector(code="001", name="종합(KOSPI)", cur_prc="-656272", flu_rt="-399"), _sector()]
        )

    def get_industry_price_by_sector(self, mrkt_tp="0", inds_cd="001"):
        self.calls.append(("ka20002", mrkt_tp, inds_cd))
        item = SimpleNamespace(
            stk_cd="000080", stk_nm="하이트진로", cur_prc="-15510", flu_rt="-0.58", now_trde_qty="90861"
        )
        return self._resp(inds_stkpc=[item])


class HarnessApp(App):
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self._current_screen_key = "5"

    def on_mount(self) -> None:
        self.push_screen(InvestorFlowScreen())


async def _loaded(app, pilot):
    await pilot.pause()
    await app.workers.wait_for_complete()
    await pilot.pause()
    return app.screen


@pytest.mark.asyncio
class TestInvestorFlowScreen:
    async def test_default_market_is_kospi_and_rates_are_percent(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test(size=(160, 50)) as pilot:
            screen = await _loaded(app, pilot)
            assert ("ka10051", "0") in fetcher.calls
            table = screen.query_one("#sector-investor-table", DataTable)
            assert table.row_count == 2
            row = table.get_row_at(0)
            assert row[1] == "6,562.72"
            assert "-3.99%" in row[2]
            assert "-210" not in " ".join(str(c) for c in table.get_row_at(1))

    async def test_enter_on_sector_loads_its_stocks(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test(size=(160, 50)) as pilot:
            screen = await _loaded(app, pilot)
            table = screen.query_one("#sector-investor-table", DataTable)
            table.focus()
            table.move_cursor(row=1)
            await pilot.press("enter")
            await app.workers.wait_for_complete()
            await pilot.pause()
            assert ("ka20002", "0", "106") in fetcher.calls
            stocks = screen.query_one("#sector-stocks-table", DataTable)
            assert stocks.row_count == 1
            assert stocks.get_row_at(0)[2] == "15,510"
            assert "구성 종목 1건" in str(screen.query_one("#sector-status", Static).content)

    async def test_switching_market_reloads_with_kosdaq_code(self):
        fetcher = FakeFetcher()
        app = HarnessApp(fetcher)
        async with app.run_test(size=(160, 50)) as pilot:
            screen = await _loaded(app, pilot)
            screen._reload_sector_investor("1")
            await _loaded(app, pilot)
            assert ("ka10051", "1") in fetcher.calls
            table = screen.query_one("#sector-investor-table", DataTable)
            assert table.row_count == 1
            assert table.get_row_at(0)[0] == "종합(KOSDAQ)"
