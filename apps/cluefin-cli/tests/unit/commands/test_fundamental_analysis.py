from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

import cluefin_cli.commands.fundamental_analysis as fa
from cluefin_cli.commands.fundamental_analysis import (
    _display_accounts,
    _display_dividends,
    _display_indicators,
    _display_overview,
    _display_shareholders,
    _format_amount,
    _format_indicator,
    _format_share_value,
    fundamental_analysis,
)
from cluefin_cli.data.fundamentals import (
    AccountSnapshot,
    DividendSnapshot,
    IndicatorSnapshot,
    ShareholderSnapshot,
)

# ---------------------------------------------------------------------------
# format helpers
# ---------------------------------------------------------------------------


def test_format_amount() -> None:
    assert _format_amount(None, "KRW") == "-"
    assert _format_amount(Decimal("1000"), None) == "1,000"
    assert _format_amount(Decimal("1000"), "KRW") == "1,000 KRW"
    assert _format_amount(Decimal("1234.50"), None) == "1,234.50"


def test_format_indicator() -> None:
    assert _format_indicator(IndicatorSnapshot("c", "n", None, None)) == "-"
    assert _format_indicator(IndicatorSnapshot("c", "n", Decimal("0.25"), "%")) == "25.00%"
    assert _format_indicator(IndicatorSnapshot("c", "n", Decimal("12.5"), None)) == "12.50"


def test_format_share_value() -> None:
    assert _format_share_value(None) == "-"
    assert _format_share_value("1,000") == "1,000"
    assert _format_share_value("abc") == "abc"
    assert _format_share_value("  ") == "  "


# ---------------------------------------------------------------------------
# display functions (with data and empty)
# ---------------------------------------------------------------------------


def test_display_overview() -> None:
    overview = SimpleNamespace(
        corp_name="삼성전자",
        induty_code="264",
        ceo_nm="대표",
        corp_cls="Y",
        est_dt="19690113",
        acc_mt="12",
        hm_url="http://x",
        ir_url=None,
        phn_no="02-0000",
    )
    _display_overview("005930", "00126380", overview)


def test_display_accounts_with_and_without_data() -> None:
    _display_accounts([])
    accounts = [
        AccountSnapshot("Revenue", "매출액", "2023", Decimal("1000"), "2022", Decimal("900"), "KRW"),
    ]
    _display_accounts(accounts)


def test_display_indicators_with_and_without_data() -> None:
    _display_indicators([])
    indicators = [
        IndicatorSnapshot("Profitability", "ROE", Decimal("0.12"), "%"),
        IndicatorSnapshot("Growth", "Revenue Growth", Decimal("5.0"), None),
    ]
    _display_indicators(indicators)


def test_display_dividends_with_and_without_data() -> None:
    _display_dividends([])
    dividends = [DividendSnapshot("현금배당", "100", "90", None, "보통주")]
    _display_dividends(dividends)


def test_display_shareholders_with_and_without_data() -> None:
    _display_shareholders([], 5)
    holders = [
        ShareholderSnapshot("이재용", "최대주주", "120", "1.2", "100", "1.0"),
        ShareholderSnapshot("기타", None, None, None, None, None),
    ]
    _display_shareholders(holders, max_rows=1)  # exercise truncation


# ---------------------------------------------------------------------------
# command entry point
# ---------------------------------------------------------------------------


def test_command_invokes_analysis(monkeypatch) -> None:
    called = {}

    async def _fake(stock_code, year, report_code, max_shareholders):
        called["args"] = (stock_code, year, report_code, max_shareholders)

    monkeypatch.setattr(fa, "_perform_fundamental_analysis", _fake)
    result = CliRunner().invoke(fundamental_analysis, ["005930", "--report", "q1"])
    assert result.exit_code == 0
    assert called["args"][0] == "005930"
    assert called["args"][2] == "11013"  # q1 report code


def test_command_handles_errors_gracefully(monkeypatch) -> None:
    async def _boom(*args, **kwargs):
        raise RuntimeError("dart down")

    monkeypatch.setattr(fa, "_perform_fundamental_analysis", _boom)
    result = CliRunner().invoke(fundamental_analysis, ["005930"])
    # Error is caught and reported; command still exits 0.
    assert result.exit_code == 0
