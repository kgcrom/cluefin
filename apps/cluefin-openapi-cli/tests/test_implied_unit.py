"""`implied.py` — RIM 내재 ROE·역DCF 내재 성장률 산수. 순수 함수라 네트워크·세션 없이 손계산과 대조한다."""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import implied

# ---------------------------------------------------------------------------
# cost_of_equity / wacc
# ---------------------------------------------------------------------------


def test_cost_of_equity_is_capm() -> None:
    assert implied.cost_of_equity(0.03, 1.2, 0.06) == pytest.approx(0.03 + 1.2 * 0.06)


def test_after_tax_cost_of_debt() -> None:
    assert implied.after_tax_cost_of_debt(0.05, 0.25) == pytest.approx(0.0375)


def test_wacc_is_market_value_weighted() -> None:
    # equity 700, debt 300 -> weights 0.7/0.3
    out = implied.wacc(700, 300, cost_of_equity=0.10, after_tax_cost_of_debt=0.04)
    assert out == pytest.approx(0.7 * 0.10 + 0.3 * 0.04)


def test_wacc_is_none_when_capital_is_non_positive() -> None:
    assert implied.wacc(0, 0, 0.1, 0.04) is None
    assert implied.wacc(-100, 50, 0.1, 0.04) is None


# ---------------------------------------------------------------------------
# rim_value — hand-computed cross-checks
# ---------------------------------------------------------------------------


def test_rim_value_one_year_closed_form() -> None:
    b0, roe0, coe = 1000.0, 0.15, 0.08
    value = implied.rim_value(b0, roe0, coe, fade_years=1, payout_ratio=0.3)
    expected = b0 + (roe0 - coe) * b0 / (1 + coe)
    assert value == pytest.approx(expected)


def test_rim_value_two_years_full_payout_keeps_book_flat() -> None:
    """payout_ratio=1.0 means book never grows, so both years' residual income use the same B0."""
    b0, roe0, coe = 1000.0, 0.15, 0.08
    value = implied.rim_value(b0, roe0, coe, fade_years=2, payout_ratio=1.0)
    roe_year2 = coe + (roe0 - coe) * 0.5
    expected = b0 + (roe0 - coe) * b0 / (1 + coe) + (roe_year2 - coe) * b0 / (1 + coe) ** 2
    assert value == pytest.approx(expected)


def test_rim_value_at_roe_equal_cost_of_equity_is_just_book_value() -> None:
    """No excess return anywhere -> residual income is zero every year."""
    assert implied.rim_value(1000.0, 0.08, 0.08, fade_years=10, payout_ratio=0.3) == pytest.approx(1000.0)


def test_rim_value_zero_fade_years_returns_book_value() -> None:
    assert implied.rim_value(1000.0, 0.5, 0.08, fade_years=0, payout_ratio=0.3) == 1000.0


# ---------------------------------------------------------------------------
# implied_roe — bisection round-trips and edge cases
# ---------------------------------------------------------------------------


def test_implied_roe_round_trips_through_rim_value() -> None:
    b0, coe, fade, payout = 1000.0, 0.08, 10, 0.3
    target_roe = 0.18
    market_cap = implied.rim_value(b0, target_roe, coe, fade, payout)

    result = implied.implied_roe(market_cap, b0, coe, fade, payout)

    assert result.reason is None
    assert result.value == pytest.approx(target_roe, abs=1e-5)


def test_implied_roe_is_none_with_non_positive_book_equity() -> None:
    result = implied.implied_roe(1000.0, 0.0, 0.08, 10, 0.3)
    assert result.value is None
    assert result.reason == "non_positive_book_equity"


def test_implied_roe_has_no_solution_outside_the_search_bracket() -> None:
    # A market cap far beyond what any ROE in [-10%, 10%] could justify.
    result = implied.implied_roe(1_000_000.0, 1000.0, 0.08, 10, 0.3, lo=-0.1, hi=0.1)
    assert result.value is None
    assert result.reason == "no_solution_in_range"


# ---------------------------------------------------------------------------
# reverse_dcf_ev / implied_growth
# ---------------------------------------------------------------------------


def test_reverse_dcf_ev_is_none_when_wacc_does_not_exceed_terminal_growth() -> None:
    assert (
        implied.reverse_dcf_ev(1000, 0.05, 0.15, 0.22, 2.5, wacc_rate=0.02, horizon_years=10, terminal_growth=0.02)
        is None
    )


def test_reverse_dcf_ev_increases_with_growth_for_a_healthy_margin() -> None:
    revenue0, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth = (
        1000.0,
        0.2,
        0.22,
        2.5,
        0.09,
        10,
        0.02,
    )
    low = implied.reverse_dcf_ev(
        revenue0, 0.02, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth
    )
    high = implied.reverse_dcf_ev(
        revenue0, 0.08, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth
    )
    assert low is not None
    assert high is not None
    assert high > low


def test_implied_growth_round_trips_through_reverse_dcf_ev() -> None:
    revenue0, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth = (
        1000.0,
        0.18,
        0.22,
        2.5,
        0.09,
        10,
        0.02,
    )
    target_growth = 0.06
    ev = implied.reverse_dcf_ev(
        revenue0, target_growth, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth
    )
    assert ev is not None

    result = implied.implied_growth(
        ev, revenue0, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth
    )

    assert result.reason is None
    assert result.value == pytest.approx(target_growth, abs=1e-5)


def test_implied_growth_is_none_with_non_positive_revenue() -> None:
    result = implied.implied_growth(1000.0, 0.0, 0.2, 0.22, 2.5, 0.09, 10, 0.02)
    assert result.value is None
    assert result.reason == "non_positive_revenue"


def test_implied_growth_is_none_when_wacc_not_above_terminal_growth() -> None:
    result = implied.implied_growth(1000.0, 1000.0, 0.2, 0.22, 2.5, 0.02, 10, 0.02)
    assert result.value is None
    assert result.reason == "wacc_not_above_terminal_growth"


def test_implied_growth_has_no_solution_outside_the_search_bracket() -> None:
    result = implied.implied_growth(1_000_000_000.0, 1000.0, 0.18, 0.22, 2.5, 0.09, 10, 0.02, lo=-0.05, hi=0.05)
    assert result.value is None
    assert result.reason == "no_solution_in_range"


# ---------------------------------------------------------------------------
# bisect — the shared helper directly
# ---------------------------------------------------------------------------


def test_bisect_finds_a_linear_root() -> None:
    result = implied.bisect(lambda x: 2 * x + 1, target=5.0, lo=-10.0, hi=10.0)
    assert result.value == pytest.approx(2.0)
    assert result.reason is None


def test_bisect_reports_no_solution_when_target_is_outside_the_bracket() -> None:
    result = implied.bisect(lambda x: x, target=100.0, lo=0.0, hi=1.0)
    assert result.value is None
    assert result.reason == "no_solution_in_range"


def test_bisect_reports_undefined_function_at_bracket() -> None:
    def f(x: float) -> float | None:
        return None if x == 0.0 else x

    result = implied.bisect(f, target=1.0, lo=0.0, hi=10.0)
    assert result.value is None
    assert result.reason == "f_undefined_at_bracket"
