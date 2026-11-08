"""Pure-function tests for `investor_metrics.py` — synthetic figures, no DART/KIS calls."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import investor_metrics as im


def test_fcf_yield_is_free_cash_flow_over_market_cap() -> None:
    result = im.fcf_yield(free_cash_flow=50.0, market_cap=1000.0)
    assert result["value"] == pytest.approx(5.0)
    assert result["reason"] is None


def test_fcf_yield_is_null_with_a_reason_when_market_cap_is_missing() -> None:
    result = im.fcf_yield(free_cash_flow=50.0, market_cap=None)
    assert result["value"] is None
    assert "market_cap" in result["reason"]


def test_fcf_yield_is_null_when_market_cap_is_zero_or_negative() -> None:
    result = im.fcf_yield(free_cash_flow=50.0, market_cap=0.0)
    assert result["value"] is None
    assert "0 이하" in result["reason"]


def test_owner_earnings_combines_net_income_da_capex_and_working_capital() -> None:
    result = im.owner_earnings(
        net_income_owners=100.0,
        depreciation=20.0,
        amortization=5.0,
        capex=40.0,
        working_capital_increase=10.0,
    )
    assert result["value"] == pytest.approx(100.0 + 20.0 + 5.0 - 40.0 - 10.0)
    assert result["reason"] is None


def test_owner_earnings_subtracts_capex_filed_as_negative() -> None:
    result = im.owner_earnings(
        net_income_owners=100.0,
        depreciation=20.0,
        amortization=5.0,
        capex=-40.0,
        working_capital_increase=10.0,
    )
    assert result["value"] == pytest.approx(100.0 + 20.0 + 5.0 - 40.0 - 10.0)
    assert result["components"]["capex"] == -40.0


def test_owner_earnings_is_null_not_zero_when_depreciation_is_missing() -> None:
    result = im.owner_earnings(
        net_income_owners=100.0,
        depreciation=None,
        amortization=5.0,
        capex=40.0,
        working_capital_increase=10.0,
    )
    assert result["value"] is None
    assert "감가상각" in result["reason"]
    assert result["components"]["depreciation"] is None  # echoed, not defaulted to 0


def test_owner_earnings_is_null_when_amortization_is_missing_too() -> None:
    result = im.owner_earnings(
        net_income_owners=100.0,
        depreciation=20.0,
        amortization=None,
        capex=40.0,
        working_capital_increase=10.0,
    )
    assert result["value"] is None


def test_owner_earnings_yield_divides_by_market_cap() -> None:
    result = im.owner_earnings_yield(owner_earnings_value=75.0, market_cap=1500.0)
    assert result["value"] == pytest.approx(5.0)


def test_ev_ebit_and_earnings_yield_are_reciprocal() -> None:
    ev_ebit = im.ev_ebit(ev=1200.0, ebit=100.0)
    earnings_yield = im.earnings_yield(ebit=100.0, ev=1200.0)

    assert ev_ebit["value"] == pytest.approx(12.0)
    assert earnings_yield["value"] == pytest.approx(100.0 / 1200.0 * 100)
    assert earnings_yield["value"] == pytest.approx(100.0 / ev_ebit["value"])


def test_ev_ebit_is_null_when_ebit_is_zero_or_negative() -> None:
    result = im.ev_ebit(ev=1200.0, ebit=-10.0)
    assert result["value"] is None
    assert "0 이하" in result["reason"]


def test_eps_cagr_is_the_two_point_compound_growth_rate() -> None:
    result = im.eps_cagr(eps_start=1000.0, eps_end=1210.0, years=2)
    assert result["value"] == pytest.approx(10.0)
    assert result["reason"] is None


def test_eps_cagr_is_null_when_either_endpoint_is_a_loss() -> None:
    result = im.eps_cagr(eps_start=-100.0, eps_end=1000.0, years=2)
    assert result["value"] is None
    assert "적자" in result["reason"]


def test_eps_cagr_is_null_with_a_reason_when_an_input_is_missing() -> None:
    result = im.eps_cagr(eps_start=None, eps_end=1000.0, years=2)
    assert result["value"] is None
    assert "eps_start" in result["reason"]


def test_peg_is_per_over_growth_percent() -> None:
    result = im.peg(per=15.0, growth_pct=10.0, growth_source="dart_3y_eps_cagr")
    assert result["value"] == pytest.approx(1.5)
    assert result["growth_source"] == "dart_3y_eps_cagr"
    assert result["reason"] is None


def test_peg_is_null_when_growth_is_zero_or_negative() -> None:
    result = im.peg(per=15.0, growth_pct=-5.0, growth_source="kis_estimated_eps_growth")
    assert result["value"] is None
    assert "성장률" in result["reason"]


def test_shareholder_yield_nets_payouts_against_issuance() -> None:
    result = im.shareholder_yield(
        dividends_paid=-30.0,
        treasury_shares_acquired=-20.0,
        treasury_shares_disposed=5.0,
        proceeds_from_share_issuance=10.0,
        market_cap=1000.0,
    )
    # abs(30) + abs(20) - abs(5) - abs(10) = 35
    assert result["value"] == pytest.approx(3.5)
    assert result["reason"] is None


def test_shareholder_yield_is_null_when_any_cash_flow_item_is_missing() -> None:
    result = im.shareholder_yield(
        dividends_paid=-30.0,
        treasury_shares_acquired=-20.0,
        treasury_shares_disposed=None,
        proceeds_from_share_issuance=10.0,
        market_cap=1000.0,
    )
    assert result["value"] is None
    assert "treasury_shares_disposed" in result["reason"]
    assert result["components"]["treasury_shares_disposed"] is None  # not defaulted to 0


def test_shareholder_yield_treats_missing_rows_as_zero_when_cash_flow_statement_was_read() -> None:
    result = im.shareholder_yield(
        dividends_paid=-30.0,
        treasury_shares_acquired=None,
        treasury_shares_disposed=None,
        proceeds_from_share_issuance=None,
        market_cap=1000.0,
        cash_flow_statement_present=True,
    )
    assert result["value"] == pytest.approx(3.0)
    assert result["assumed_zero"] == [
        "treasury_shares_acquired",
        "treasury_shares_disposed",
        "proceeds_from_share_issuance",
    ]
    assert result["components"]["treasury_shares_disposed"] is None
