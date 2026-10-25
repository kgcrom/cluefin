"""`dart financial-summary` and the `statements` module it computes with.

The statement cases are the cluefin-factory vitest cases (archived 2026-10-18) ported to
pytest: synthetic rows, no real filings. The handler is driven by a fake DART client keyed by
(year, reprt_code, fs_div) so call counts, the consolidated→separate fallback and the as_of
filter can be asserted.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import statements as s
from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers import dart as handlers
from cluefin_openapi_cli.validation import validate_params


def _revenue(**amounts) -> dict:
    return {"sj_div": "CIS", "account_id": "ifrs-full_Revenue", **amounts}


def _report(year, reprt_code, rows, rcept_no="20250101000001") -> s.Report:
    return s.Report(year=year, reprt_code=reprt_code, rcept_no=rcept_no, rows=rows)


# 2025's four reports, each also carrying 2024 in its comparative columns.
YEAR_2025 = [
    _report(
        2025,
        "11013",
        [_revenue(thstrm_amount="100", thstrm_add_amount="100", frmtrm_q_amount="80", frmtrm_add_amount="80")],
    ),
    _report(2025, "11012", [_revenue(thstrm_amount="120", thstrm_add_amount="220", frmtrm_add_amount="170")]),
    _report(2025, "11014", [_revenue(thstrm_amount="110", thstrm_add_amount="330", frmtrm_add_amount="250")]),
    _report(2025, "11011", [_revenue(thstrm_amount="460", frmtrm_amount="350", bfefrmtrm_amount="300")]),
]


def test_won_strips_commas_and_treats_blank_and_dash_as_missing() -> None:
    assert s.won("1,234,567") == 1234567
    assert s.won("-5") == -5
    assert s.won("") is None
    assert s.won("-") is None
    assert s.won(None) is None


def test_growth_is_a_number_only_when_both_sides_are_positive() -> None:
    assert s.growth(130, 100) == pytest.approx(30)
    assert s.growth(10, -5) == "흑전"
    assert s.growth(-10, 5) == "적전"
    assert s.growth(-10, -5) == "적지"
    assert s.growth(10, None) is None


def test_quarters_subtract_year_to_date_and_take_4q_from_the_annual() -> None:
    quarters = s.quarters(YEAR_2025)
    assert {q["period"]: q["revenue"] for q in quarters} == {
        "2024Q1": 80,
        "2024Q2": 90,
        "2024Q3": 80,
        "2024Q4": 100,
        "2025Q1": 100,
        "2025Q2": 120,
        "2025Q3": 110,
        "2025Q4": 130,
    }
    assert quarters[-1]["yoy"]["revenue"] == pytest.approx(30)
    assert quarters[0]["yoy"] is None


def test_a_years_own_report_beats_the_comparative_column_of_the_next() -> None:
    own_2024 = _report(2024, "11011", [_revenue(thstrm_amount="360")])
    q4 = next(q for q in s.quarters([*YEAR_2025, own_2024]) if q["period"] == "2024Q4")
    assert q4["revenue"] == 110  # 360 − 250, not 350 − 250


def test_a_quarter_without_the_previous_cumulative_is_left_out() -> None:
    only_fy = [_report(2025, "11011", [_revenue(thstrm_amount="460")])]
    assert s.quarters(only_fy) == []


def _bs(account_nm, thstrm_amount, account_id="-표준계정코드 미사용-") -> dict:
    return {"sj_div": "BS", "account_nm": account_nm, "account_id": account_id, "thstrm_amount": thstrm_amount}


def test_borrowings_sum_loan_and_bond_lines_by_label() -> None:
    rows = [_bs("단기차입금", "100"), _bs("사채", "50"), _bs("장기 차입금", "30"), _bs("리스부채", "9")]
    assert s.borrowings(rows, "thstrm_amount") == (180, "차입금·사채 (단기차입금+사채+장기차입금)")


def test_borrowings_fall_back_to_financial_liabilities_and_say_so() -> None:
    rows = [
        _bs("단기금융부채", "70", "ifrs-full_CurrentFinancialLiabilities"),
        _bs("장기금융부채", "20", "ifrs-full_NoncurrentFinancialLiabilities"),
    ]
    amount, basis = s.borrowings(rows, "thstrm_amount")
    assert amount == 90
    assert basis.startswith("금융부채")
    assert s.borrowings([_bs("리스부채", "9")], "thstrm_amount") == (None, None)


def _annual_row(sj_div, account_id, values) -> dict:
    return {
        "sj_div": sj_div,
        "account_id": account_id,
        "thstrm_amount": values[2],
        "frmtrm_amount": values[1],
        "bfefrmtrm_amount": values[0],
    }


ANNUAL_ROWS = [
    _annual_row("CIS", "ifrs-full_Revenue", ["1000", "1000", "1000"]),
    _annual_row("CIS", "dart_OperatingIncomeLoss", ["100", "100", "100"]),
    _annual_row("CIS", "ifrs-full_ProfitLossAttributableToOwnersOfParent", ["50", "50", "60"]),
    _annual_row("BS", "ifrs-full_Liabilities", ["300", "300", "300"]),
    _annual_row("BS", "ifrs-full_Equity", ["100", "100", "150"]),
    _annual_row("BS", "ifrs-full_EquityAttributableToOwnersOfParent", ["100", "100", "140"]),
    _annual_row("CF", "ifrs-full_CashFlowsFromUsedInOperatingActivities", ["80", "80", "80"]),
    _annual_row(
        "CF", "ifrs-full_PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities", ["30", "30", "120"]
    ),
]


def test_annual_gives_three_years_oldest_first_with_roe_on_average_equity() -> None:
    y1, _, y3 = s.annual(_report(2025, "11011", ANNUAL_ROWS))
    assert y1["year"] == 2023
    assert y1["roe"] is None
    assert y3["roe"] == pytest.approx(50)  # 60 / ((100 + 140) / 2)
    assert y3["debt_ratio"] == pytest.approx(200)
    assert y3["free_cash_flow"] == -40
    assert y3["opm"] == pytest.approx(10)


def test_latest_reads_income_year_to_date_and_cash_flow_as_is() -> None:
    rows = [
        _revenue(thstrm_amount="120", thstrm_add_amount="220"),
        {"sj_div": "CF", "account_id": "ifrs-full_CashFlowsFromUsedInOperatingActivities", "thstrm_amount": "40"},
    ]
    figures = s.latest(_report(2026, "11012", rows))
    assert figures["period"] == "2026H1"
    assert figures["revenue"] == 220
    assert figures["operating_cash_flow"] == 40
    assert "roe" not in figures


def test_trailing_needs_all_four_quarters() -> None:
    q = lambda v: {"net_income_owners": v}  # noqa: E731
    assert s.trailing([q(1), q(2), q(3), q(4), q(5)], "net_income_owners") == 14
    assert s.trailing([q(1), q(None), q(3), q(4)], "net_income_owners") is None
    assert s.trailing([q(1), q(2)], "net_income_owners") is None


def test_to_eok_converts_money_fields_only() -> None:
    out = s.to_eok({"revenue": 2e8, "opm": 12.5, "yoy": {"revenue": 3.0}, "borrowings_basis": "x"})
    assert out == {"revenue": 2.0, "opm": 12.5, "yoy": {"revenue": 3.0}, "borrowings_basis": "x"}


# ---------------------------------------------------------------------------
# handler
# ---------------------------------------------------------------------------


class _Row:
    def __init__(self, data: dict) -> None:
        self._data = data

    def model_dump(self) -> dict:
        return dict(self._data)


class _Result:
    def __init__(self, rows: list[dict]) -> None:
        self.result = type("Envelope", (), {"status": "000", "list": [_Row(r) for r in rows]})()


class _FakeStatements:
    """`get_single_company_full_statements` keyed by (year, reprt_code, fs_div); unknown keys answer no rows."""

    def __init__(self, reports: dict[tuple[int, str, str], list[dict]]) -> None:
        self._reports = reports
        self.calls: list[tuple[str, str, str, str]] = []

    def get_single_company_full_statements(self, corp_code, bsns_year, reprt_code, fs_div):
        self.calls.append((corp_code, bsns_year, reprt_code, fs_div))
        return _Result(self._reports.get((int(bsns_year), reprt_code, fs_div), []))


class _FakeSession:
    def __init__(self, reports) -> None:
        self.statements = _FakeStatements(reports)

    def get_dart(self):
        return type("Client", (), {"periodic_report_financial_statement": self.statements})()


def _rows_with_receipt(rows: list[dict], rcept_no: str) -> list[dict]:
    return [{**row, "rcept_no": rcept_no} for row in rows]


def _two_years(fs_div: str) -> dict:
    """2025's four reports plus 2026 Q1/H1, all consolidated unless told otherwise."""
    reports = {(r.year, r.reprt_code, fs_div): _rows_with_receipt(r.rows, f"{r.year}0815000001") for r in YEAR_2025}
    reports[(2026, "11013", fs_div)] = _rows_with_receipt(
        [_revenue(thstrm_amount="150", thstrm_add_amount="150", frmtrm_q_amount="100", frmtrm_add_amount="100")],
        "20260515000001",
    )
    reports[(2026, "11012", fs_div)] = _rows_with_receipt(
        [_revenue(thstrm_amount="170", thstrm_add_amount="320", frmtrm_add_amount="220")],
        "20260814000001",
    )
    return reports


def test_summary_uses_consolidated_statements_in_eight_calls() -> None:
    session = _FakeSession(_two_years("CFS"))

    result = handlers.handle_financial_summary({"corp_code": "00000001", "as_of": "20261018"}, session)

    assert result["statement_basis"] == "CFS"
    assert result["calls"] == 8
    assert len(session.statements.calls) == 8
    assert {c[3] for c in session.statements.calls} == {"CFS"}
    assert [q["period"] for q in result["quarters"]] == [
        "2024Q3",
        "2024Q4",
        "2025Q1",
        "2025Q2",
        "2025Q3",
        "2025Q4",
        "2026Q1",
        "2026Q2",
    ]
    assert result["quarters"][-1]["revenue"] == pytest.approx(170 / 1e8)
    assert result["latest"]["period"] == "2026H1"
    assert result["latest"]["revenue"] == pytest.approx(320 / 1e8)
    assert result["reports"][-1] == {
        "year": 2026,
        "reprt_code": "11012",
        "rcept_no": "20260814000001",
        "received_on": "20260814",
    }
    assert result["ttm"]["revenue"] == pytest.approx((110 + 130 + 150 + 170) / 1e8)
    assert result["annual"][-1]["year"] == 2025
    assert result["unit"] == "억원"


def test_summary_falls_back_to_separate_statements_when_there_is_no_consolidated() -> None:
    session = _FakeSession(_two_years("OFS"))

    result = handlers.handle_financial_summary({"corp_code": "00000001", "as_of": "20261018"}, session)

    assert result["statement_basis"] == "OFS"
    assert result["calls"] == 16
    assert [c[3] for c in session.statements.calls][:8] == ["CFS"] * 8


def test_summary_drops_reports_received_after_as_of() -> None:
    session = _FakeSession(_two_years("CFS"))

    result = handlers.handle_financial_summary({"corp_code": "00000001", "as_of": "20260601"}, session)

    assert result["latest"]["period"] == "2026Q1"
    assert all(r["received_on"] <= "20260601" for r in result["reports"])


def test_summary_fetches_the_previous_annual_report_alone_before_march() -> None:
    """2026-03-01: 2025's Q1/H1/Q3 are filed, its annual report is not — the 2024 annual fills the 3-year table."""
    reports = {
        (r.year, r.reprt_code, "CFS"): _rows_with_receipt(r.rows, "20250815000001")
        for r in YEAR_2025
        if r.reprt_code != "11011"
    }
    reports[(2024, "11011", "CFS")] = _rows_with_receipt(
        [_revenue(thstrm_amount="350", frmtrm_amount="300", bfefrmtrm_amount="280")], "20250315000001"
    )
    session = _FakeSession(reports)

    result = handlers.handle_financial_summary({"corp_code": "00000001", "as_of": "20260301"}, session)

    assert result["calls"] == 9
    assert session.statements.calls[-1][1:3] == ("2024", "11011")
    assert result["latest"]["period"] == "20259M"
    assert [y["year"] for y in result["annual"]] == [2022, 2023, 2024]


def test_summary_without_any_report_is_exit_4_with_the_call_count() -> None:
    session = _FakeSession({})

    with pytest.raises(CliError) as info:
        handlers.handle_financial_summary({"corp_code": "00000001", "as_of": "20261018", "fs_div": "CFS"}, session)

    assert info.value.exit_code == EXIT_BROKER
    assert info.value.data["calls"] == 8


def test_summary_schema_rejects_bad_quarters_and_basis() -> None:
    schema = handlers.handle_financial_summary._rpc_schema.parameters
    assert validate_params({"corp_code": "00126380", "quarters": 2}, schema).issues
    assert validate_params({"corp_code": "00126380", "fs_div": "both"}, schema).issues
    assert not validate_params({"corp_code": "00126380", "as_of": "20261018", "quarters": 8}, schema).issues
