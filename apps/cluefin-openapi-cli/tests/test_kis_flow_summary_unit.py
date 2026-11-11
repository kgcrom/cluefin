"""`kis stock flow-summary` — one fake `domestic_market_analysis` answering all five series.

The window arithmetic itself is covered with synthetic rows in test_flows_unit.py; this file drives
the handler end to end: five-call wiring, the intraday-drop rule (`_flow_summary_now`, same pattern as
`domestic_basic_quote._now`), partial-series failure (`missing`), and the always-null
`foreign_ownership`/`pct_of_listed_shares` blocks.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers


class _Row:
    def __init__(self, data: dict) -> None:
        self._data = data

    def model_dump(self) -> dict:
        return dict(self._data)


class _Body:
    def __init__(self, **fields) -> None:
        for name, value in fields.items():
            setattr(self, name, value)


class _Response:
    def __init__(self, body: _Body) -> None:
        self.body = body


def _investor_row(date: str, **amounts) -> dict:
    base = {
        "stck_bsop_date": date,
        "acml_tr_pbmn": "1000",
        "frgn_ntby_tr_pbmn": "0",
        "orgn_ntby_tr_pbmn": "0",
        "prsn_ntby_tr_pbmn": "0",
    }
    base.update(amounts)
    return base


def _short_selling_row(date: str, ratio: str = "3.0") -> dict:
    return {"stck_bsop_date": date, "ssts_vol_rlim": ratio}


def _loan_row(date: str, rmnd_stcn: str = "100", rmnd_amt: str = "10") -> dict:
    return {"bsop_date": date, "rmnd_stcn": rmnd_stcn, "rmnd_amt": rmnd_amt}


def _credit_row(date: str, rmnd_stcn: str = "200", rmnd_amt: str = "20") -> dict:
    return {"deal_date": date, "whol_loan_rmnd_stcn": rmnd_stcn, "whol_loan_rmnd_amt": rmnd_amt}


def _program_row(date: str, pbmn: str = "0") -> dict:
    return {"stck_bsop_date": date, "whol_smtn_ntby_tr_pbmn": pbmn}


class _MarketAnalysis:
    def __init__(
        self,
        *,
        investor_rows: list[dict],
        short_selling_rows: list[dict],
        loan_rows: list[dict],
        credit_rows: list[dict],
        program_rows: list[dict],
        fail: str | None = None,
        fail_exc: Exception | None = None,
    ) -> None:
        self._rows = {
            "investors": investor_rows,
            "short_selling": short_selling_rows,
            "stock_loan": loan_rows,
            "credit": credit_rows,
            "program": program_rows,
        }
        self._fail = fail
        self._fail_exc = fail_exc or RuntimeError("boom")
        self.calls: list[tuple] = []

    def get_investor_trading_trend_by_stock_daily(self, **kwargs):
        self.calls.append(("investors", kwargs))
        if self._fail == "investors":
            raise self._fail_exc
        return _Response(_Body(output1=_Row({}), output2=[_Row(r) for r in self._rows["investors"]]))

    def get_short_selling_trend_daily(self, **kwargs):
        self.calls.append(("short_selling", kwargs))
        if self._fail == "short_selling":
            raise self._fail_exc
        return _Response(_Body(output1=_Row({}), output2=[_Row(r) for r in self._rows["short_selling"]]))

    def get_stock_loan_trend_daily(self, **kwargs):
        self.calls.append(("stock_loan", kwargs))
        if self._fail == "stock_loan":
            raise self._fail_exc
        return _Response(_Body(output1=[_Row(r) for r in self._rows["stock_loan"]]))

    def get_credit_balance_trend_daily(self, **kwargs):
        self.calls.append(("credit", kwargs))
        if self._fail == "credit":
            raise self._fail_exc
        return _Response(_Body(output=[_Row(r) for r in self._rows["credit"]]))

    def get_program_trading_trend_by_stock_daily(self, **kwargs):
        self.calls.append(("program", kwargs))
        if self._fail == "program":
            raise self._fail_exc
        return _Response(_Body(output=[_Row(r) for r in self._rows["program"]]))


class _Session:
    def __init__(self, market_analysis: _MarketAnalysis) -> None:
        self._market_analysis = market_analysis

    def get_kis(self):
        return type("Client", (), {"domestic_market_analysis": self._market_analysis})()


_TODAY = "20261111"  # must match the mocked `_flow_summary_now()` below


def _market_analysis(**overrides) -> _MarketAnalysis:
    defaults = {
        "investor_rows": [
            _investor_row(_TODAY, frgn_ntby_tr_pbmn="10", orgn_ntby_tr_pbmn="5", prsn_ntby_tr_pbmn="-15")
        ],
        "short_selling_rows": [_short_selling_row(_TODAY)],
        "loan_rows": [_loan_row(_TODAY)],
        "credit_rows": [_credit_row("20261109")],  # settlement lag — not today
        "program_rows": [_program_row(_TODAY)],
    }
    defaults.update(overrides)
    return _MarketAnalysis(**defaults)


@pytest.fixture(autouse=True)
def _after_session_final(monkeypatch):
    # 16:00 KST — after the 15:40 cutoff, so today's row is kept everywhere.
    monkeypatch.setattr(handlers, "_flow_summary_now", lambda: datetime(2026, 11, 11, 16, 0))


def test_calls_all_five_series_once() -> None:
    session = _Session(_market_analysis())
    handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    names = [name for name, _ in session._market_analysis.calls]
    assert names == ["investors", "short_selling", "stock_loan", "credit", "program"]


def test_default_windows_are_5_20_60() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["windows"] == [5, 20, 60]
    assert set(result["investors"]["foreign"]["windows"].keys()) == {"5", "20", "60"}


def test_custom_windows_are_parsed() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930", "windows": "3,10"}, session)
    assert result["windows"] == [3, 10]
    assert set(result["program"]["windows"].keys()) == {"3", "10"}


def test_invalid_windows_is_exit_2() -> None:
    session = _Session(_market_analysis())
    with pytest.raises(CliError) as excinfo:
        handlers.handle_kis_flow_summary({"stock_code": "005930", "windows": "5,abc"}, session)
    assert excinfo.value.exit_code == EXIT_USAGE


def test_investor_net_buy_amount_is_scaled_from_million_won() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    # frgn_ntby_tr_pbmn "10" (백만원) -> 10 * 1_000_000 원
    assert result["investors"]["foreign"]["windows"]["5"]["net_buy_amount"] == pytest.approx(10_000_000.0)
    assert result["investors"]["institution"]["windows"]["5"]["net_buy_amount"] == pytest.approx(5_000_000.0)
    assert result["investors"]["individual"]["windows"]["5"]["net_buy_amount"] == pytest.approx(-15_000_000.0)


def test_foreign_ownership_is_always_null_with_a_reason() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["foreign_ownership"]["value"] is None
    assert result["foreign_ownership"]["reason"]


def test_stock_loan_and_credit_pct_of_listed_shares_is_null_with_a_reason() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["stock_loan"]["pct_of_listed_shares"] is None
    assert result["stock_loan"]["pct_of_listed_shares_reason"]
    assert result["credit"]["pct_of_listed_shares"] is None
    assert result["credit"]["pct_of_listed_shares_reason"]


def test_credit_as_of_keeps_its_own_settlement_lagged_date() -> None:
    session = _Session(_market_analysis())
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["as_of"]["credit"] == "20261109"
    assert result["as_of"]["investors"] == _TODAY


def test_one_series_failing_is_recorded_in_missing_and_others_still_compute() -> None:
    session = _Session(_market_analysis(fail="credit"))
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert "credit" in result["missing"]
    assert result["credit"]["latest"] is None
    assert result["investors"]["foreign"]["windows"]["5"]["net_buy_amount"] is not None


def test_credentials_error_is_not_swallowed() -> None:
    class _AuthenticationError(Exception):
        pass

    session = _Session(_market_analysis(fail="investors", fail_exc=_AuthenticationError("bad key")))
    with pytest.raises(_AuthenticationError):
        handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)


def test_intraday_row_is_dropped_before_the_session_final(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_flow_summary_now", lambda: datetime(2026, 11, 11, 14, 0))
    session = _Session(
        _market_analysis(
            investor_rows=[_investor_row(_TODAY), _investor_row("20261110")],
            short_selling_rows=[_short_selling_row(_TODAY), _short_selling_row("20261110")],
            loan_rows=[_loan_row(_TODAY), _loan_row("20261110")],
            program_rows=[_program_row(_TODAY), _program_row("20261110")],
        )
    )
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["dropped_intraday_row"]["investors"] == _TODAY
    assert result["dropped_intraday_row"]["short_selling"] == _TODAY
    assert result["dropped_intraday_row"]["stock_loan"] == _TODAY
    assert result["dropped_intraday_row"]["program"] == _TODAY
    assert result["as_of"]["investors"] == "20261110"


def test_intraday_row_is_kept_after_the_session_final() -> None:
    session = _Session(_market_analysis(investor_rows=[_investor_row(_TODAY), _investor_row("20261110")]))
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["dropped_intraday_row"] == {}
    assert result["as_of"]["investors"] == _TODAY


def test_rows_reports_the_received_count_before_dropping(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_flow_summary_now", lambda: datetime(2026, 11, 11, 14, 0))
    session = _Session(_market_analysis(investor_rows=[_investor_row(_TODAY), _investor_row("20261110")]))
    result = handlers.handle_kis_flow_summary({"stock_code": "005930"}, session)
    assert result["rows"]["investors"] == 2
