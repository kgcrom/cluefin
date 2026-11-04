"""dilution.py — pure row normalization for `dart dilution-watch`.

No DART client involved: rows are plain dicts shaped like `dump_model` output of one
`_MAJOR_EVENTS` item (handlers/dart.py).
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.dilution import (
    DILUTION_KINDS,
    NOT_COVERED,
    normalize_row,
    with_pct_of_shares,
)


def test_convertible_bond_maps_amount_conversion_price_and_refixing_floor() -> None:
    row = {
        "rcept_no": "20260115000123",
        "corp_name": "테스트기업",
        "bd_fta": "10,000,000,000",
        "cv_prc": "5,000",
        "act_mktprcfl_cvprc_lwtrsprc": "3,500",
        "cvisstk_cnt": "2,000,000",
    }

    result = normalize_row("convertible-bond", row)

    assert result.rcept_dt == "20260115"
    assert result.kind == "convertible-bond"
    assert result.corp_name == "테스트기업"
    assert result.amount_won == 10_000_000_000
    assert result.conversion_price == 5_000
    assert result.refixing_floor == 3_500
    assert result.new_shares == 2_000_000
    assert result.pct_of_shares is None


def test_bond_with_warrant_uses_exercise_price_field() -> None:
    row = {
        "rcept_no": "20260201000456",
        "corp_name": "테스트기업",
        "bd_fta": "5,000,000,000",
        "ex_prc": "1,200",
        "act_mktprcfl_cvprc_lwtrsprc": "900",
        "nstk_isstk_cnt": "4,166,666",
    }

    result = normalize_row("bond-with-warrant", row)

    assert result.conversion_price == 1_200
    assert result.refixing_floor == 900
    assert result.new_shares == 4_166_666


def test_exchangeable_bond_has_no_refixing_field_in_the_library_model() -> None:
    row = {
        "rcept_no": "20260301000789",
        "corp_name": "테스트기업",
        "bd_fta": "3,000,000,000",
        "ex_prc": "8,000",
        "extg_stkcnt": "375,000",
    }

    result = normalize_row("exchangeable-bond", row)

    assert result.conversion_price == 8_000
    assert result.refixing_floor is None
    assert result.new_shares == 375_000


def test_rights_offering_sums_fund_purposes_for_amount() -> None:
    row = {
        "rcept_no": "20260401000111",
        "corp_name": "테스트기업",
        "fdpp_fclt": "1,000,000",
        "fdpp_bsninh": "-",
        "fdpp_op": "2,000,000",
        "fdpp_dtrp": None,
        "fdpp_ocsa": "0",
        "fdpp_etc": "500,000",
        "nstk_ostk_cnt": "100,000",
    }

    result = normalize_row("rights-offering", row)

    assert result.amount_won == 3_500_000
    assert result.conversion_price is None
    assert result.new_shares == 100_000


def test_bonus_issue_has_no_money_fields() -> None:
    row = {"rcept_no": "20260501000222", "corp_name": "테스트기업", "nstk_ostk_cnt": "50,000"}

    result = normalize_row("bonus-issue", row)

    assert result.amount_won is None
    assert result.new_shares == 50_000


def test_rights_and_bonus_issue_sums_both_new_share_components() -> None:
    row = {
        "rcept_no": "20260601000333",
        "corp_name": "테스트기업",
        "piic_fdpp_fclt": "1,000,000",
        "piic_fdpp_bsninh": "-",
        "piic_fdpp_op": "-",
        "piic_fdpp_dtrp": "-",
        "piic_fdpp_ocsa": "-",
        "piic_fdpp_etc": "-",
        "piic_nstk_ostk_cnt": "10,000",
        "fric_nstk_ostk_cnt": "20,000",
    }

    result = normalize_row("rights-and-bonus-issue", row)

    assert result.amount_won == 1_000_000
    assert result.new_shares == 30_000


def test_capital_reduction_reports_new_shares_as_negative() -> None:
    row = {"rcept_no": "20260701000444", "corp_name": "테스트기업", "crstk_ostk_cnt": "1,000,000"}

    result = normalize_row("capital-reduction", row)

    assert result.new_shares == -1_000_000


def test_treasury_stock_acquisition_reports_new_shares_as_negative() -> None:
    row = {
        "rcept_no": "20260801000555",
        "corp_name": "테스트기업",
        "aqpln_stk_ostk": "300,000",
        "aqpln_prc_ostk": "9,000,000,000",
    }

    result = normalize_row("treasury-stock-acquisition", row)

    assert result.amount_won == 9_000_000_000
    assert result.new_shares == -300_000


def test_treasury_stock_disposal_reports_new_shares_as_positive() -> None:
    row = {
        "rcept_no": "20260901000666",
        "corp_name": "테스트기업",
        "dppln_stk_ostk": "150,000",
        "dppln_prc_ostk": "4,500,000,000",
    }

    result = normalize_row("treasury-stock-disposal", row)

    assert result.amount_won == 4_500_000_000
    assert result.new_shares == 150_000


def test_treasury_trust_contract_has_amount_but_no_share_count() -> None:
    row = {"rcept_no": "20261001000777", "corp_name": "테스트기업", "ctr_prc": "2,000,000,000"}

    result = normalize_row("treasury-trust-contract", row)

    assert result.amount_won == 2_000_000_000
    assert result.new_shares is None


def test_treasury_trust_termination_uses_post_termination_amount() -> None:
    row = {"rcept_no": "20261101000888", "corp_name": "테스트기업", "ctr_prc_atcc": "500,000,000"}

    result = normalize_row("treasury-trust-termination", row)

    assert result.amount_won == 500_000_000
    assert result.new_shares is None


def test_unsupported_kind_raises() -> None:
    with pytest.raises(ValueError, match="unsupported dilution kind"):
        normalize_row("treasury-stock-retirement", {})


@pytest.mark.parametrize("kind", DILUTION_KINDS)
def test_every_declared_kind_is_handled(kind: str) -> None:
    """Every slug in DILUTION_KINDS must be a branch normalize_row recognizes, not just declared."""

    normalize_row(kind, {"rcept_no": "20260101000001", "corp_name": "테스트기업"})


def test_not_covered_states_treasury_stock_retirement_is_excluded() -> None:
    kinds = {entry["kind"] for entry in NOT_COVERED}
    assert "treasury-stock-retirement" in kinds
    assert "treasury-stock-retirement" not in DILUTION_KINDS


def test_with_pct_of_shares_computes_percentage() -> None:
    row = normalize_row("convertible-bond", {"rcept_no": "20260101000001", "cvisstk_cnt": "1,000,000"})

    result = with_pct_of_shares(row, total_shares=100_000_000)

    assert result.pct_of_shares == pytest.approx(1.0)


def test_with_pct_of_shares_leaves_none_when_new_shares_missing() -> None:
    row = normalize_row("treasury-trust-contract", {"rcept_no": "20260101000001", "ctr_prc": "1,000"})

    result = with_pct_of_shares(row, total_shares=100_000_000)

    assert result.pct_of_shares is None


def test_with_pct_of_shares_leaves_none_when_total_shares_missing() -> None:
    row = normalize_row("convertible-bond", {"rcept_no": "20260101000001", "cvisstk_cnt": "1,000,000"})

    result = with_pct_of_shares(row, total_shares=None)

    assert result.pct_of_shares is None
