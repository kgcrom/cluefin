"""Pure-function tests for `quality.py` — synthetic three-year figures, no DART calls."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import quality as q


def test_effective_tax_rate_is_clamped_to_0_40_percent() -> None:
    assert q.effective_tax_rate(20, 70) == pytest.approx(20 / 70)
    assert q.effective_tax_rate(50, 70) == pytest.approx(0.40)  # would be ~71%, clamped
    assert q.effective_tax_rate(-5, 70) == pytest.approx(0.0)  # negative tax (credit), clamped to 0
    assert q.effective_tax_rate(20, 0) is None
    assert q.effective_tax_rate(20, -10) is None
    assert q.effective_tax_rate(None, 70) is None


def test_invested_capital_is_equity_plus_borrowings_minus_cash() -> None:
    assert q.invested_capital(100, 50, 20) == 130
    assert q.invested_capital(None, 50, 20) is None


def _year(**overrides) -> dict:
    base = {
        "year": 2025,
        "revenue": 1000.0,
        "gross_profit": 300.0,
        "operating_income": 100.0,
        "pretax_income": 80.0,
        "income_tax_expense": 20.0,
        "net_income": 60.0,
        "net_income_owners": 60.0,
        "assets": 800.0,
        "current_assets": 400.0,
        "current_liabilities": 200.0,
        "noncurrent_liabilities": 150.0,
        "liabilities": 350.0,
        "equity": 450.0,
        "equity_owners": 450.0,
        "retained_earnings": 200.0,
        "cash": 100.0,
        "borrowings": 150.0,
        "operating_cash_flow": 90.0,
    }
    base.update(overrides)
    return base


def test_roic_uses_after_tax_operating_income_over_average_invested_capital() -> None:
    previous = _year(equity_owners=400.0, borrowings=150.0, cash=80.0)  # invested capital 470
    current = _year(equity_owners=450.0, borrowings=150.0, cash=100.0)  # invested capital 500

    result = q.roic(current, previous)

    assert result["effective_tax_rate"] == pytest.approx(25.0)  # 20/80
    assert result["nopat"] == pytest.approx(75.0)  # 100 * 0.75
    assert result["invested_capital"] == pytest.approx(485.0)  # avg(500, 470)
    assert result["invested_capital_averaged"] is True
    assert result["value"] == pytest.approx(75.0 / 485.0 * 100)


def test_roic_falls_back_to_point_in_time_capital_without_a_previous_year() -> None:
    result = q.roic(_year(), None)
    assert result["invested_capital_averaged"] is False
    assert result["invested_capital"] == pytest.approx(500.0)


def test_dupont_product_matches_reported_roe_on_clean_inputs() -> None:
    previous = _year(assets=700.0, equity_owners=400.0)
    current = _year(assets=800.0, equity_owners=450.0, roe=pytest.approx(60 / 425 * 100))

    result = q.dupont(current, previous)

    net_margin = 60 / 1000
    asset_turnover = 1000 / 750  # avg assets 750
    leverage = 750 / 425  # avg assets / avg equity
    expected_roe = net_margin * asset_turnover * leverage * 100
    assert result["roe_check"] == pytest.approx(expected_roe)
    assert result["net_margin"] == pytest.approx(net_margin * 100)
    assert result["asset_turnover"] == pytest.approx(asset_turnover)
    assert result["leverage"] == pytest.approx(leverage)


def test_accrual_ratio_is_net_income_minus_cfo_over_average_assets() -> None:
    previous = _year(assets=700.0)
    current = _year(assets=800.0, net_income=60.0, operating_cash_flow=90.0)

    result = q.accrual_ratio(current, previous)

    assert result["accruals"] == pytest.approx(-30.0)
    assert result["avg_assets"] == pytest.approx(750.0)
    assert result["value"] == pytest.approx(-30.0 / 750.0 * 100)


def test_altman_z_double_prime_combines_four_components() -> None:
    result = q.altman_z_double_prime(_year())

    x1 = (400.0 - 200.0) / 800.0
    x2 = 200.0 / 800.0
    x3 = 100.0 / 800.0
    x4 = 450.0 / 350.0
    expected = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4
    assert result["value"] == pytest.approx(expected)
    assert result["missing"] == []


def test_altman_z_is_null_with_a_reason_when_there_is_no_classified_balance_sheet() -> None:
    bank_year = _year(current_assets=None, current_liabilities=None)

    result = q.altman_z_double_prime(bank_year)

    assert result["value"] is None
    assert result["x1"] is None
    assert any("x1" in reason for reason in result["missing"])
    assert result["x2"] is not None  # retained_earnings/assets still computable


def test_piotroski_f_score_scores_nine_items_and_sums_them() -> None:
    previous = _year(
        revenue=900.0,
        gross_profit=250.0,
        assets=700.0,
        noncurrent_liabilities=200.0,
        current_assets=350.0,
        current_liabilities=250.0,
        net_income=40.0,
        proceeds_from_share_issuance=0.0,
    )
    current = _year(proceeds_from_share_issuance=0.0)

    result = q.piotroski_f_score(current, previous)

    assert result["incomplete"] is False
    # roa_positive, cfo_positive, roa_improved (60/800 > 40/700), cfo_exceeds_net_income (90>60),
    # leverage_decreased (150/800 < 200/700), current_ratio_improved (2.0 > 1.4),
    # no_new_shares, gross_margin_improved (0.3 > 0.278), asset_turnover_improved (1.25 > 1.286 → 0)
    assert result["items"]["roa_positive"] == 1
    assert result["items"]["cfo_positive"] == 1
    assert result["items"]["roa_improved"] == 1
    assert result["items"]["cfo_exceeds_net_income"] == 1
    assert result["items"]["leverage_decreased"] == 1
    assert result["items"]["current_ratio_improved"] == 1
    assert result["items"]["no_new_shares"] == 1
    assert result["items"]["gross_margin_improved"] == 1
    assert result["items"]["asset_turnover_improved"] == 0
    assert result["total"] == 8


def test_piotroski_f_score_treats_a_share_issuance_as_scoring_zero() -> None:
    previous = _year()
    current = _year(proceeds_from_share_issuance=50.0)

    result = q.piotroski_f_score(current, previous)

    assert result["items"]["no_new_shares"] == 0


def test_piotroski_f_score_is_incomplete_without_a_previous_year() -> None:
    result = q.piotroski_f_score(_year(), None)
    assert result["incomplete"] is True
    assert result["total"] is None
    assert all(v is None for v in result["items"].values())


def test_piotroski_f_score_is_incomplete_when_a_bank_has_no_current_ratio() -> None:
    previous = _year(current_assets=None, current_liabilities=None)
    current = _year(current_assets=None, current_liabilities=None)

    result = q.piotroski_f_score(current, previous)

    assert result["incomplete"] is True
    assert result["items"]["current_ratio_improved"] is None
    assert result["total"] is not None  # other 8 items still scored


def test_compute_returns_three_years_and_one_f_score() -> None:
    years = [
        _year(year=2023, assets=700.0, equity_owners=400.0),
        _year(year=2024, assets=750.0, equity_owners=425.0),
        _year(year=2025, assets=800.0, equity_owners=450.0),
    ]

    result = q.compute(years)

    assert [y["year"] for y in result["years"]] == [2023, 2024, 2025]
    assert result["years"][0]["roic"]["invested_capital_averaged"] is False  # oldest has no prior year
    assert result["years"][-1]["roic"]["invested_capital_averaged"] is True
    assert result["f_score"]["incomplete"] is False
    assert isinstance(result["notes"], list)
    assert result["notes"]
