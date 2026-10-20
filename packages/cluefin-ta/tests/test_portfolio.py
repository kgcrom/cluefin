"""
Tests for portfolio metrics (MDD, CAGR, SHARPE, SORTINO, CALMAR, VOLATILITY, BETA, ALPHA).
"""

import warnings

import numpy as np
import pytest

from cluefin_ta import ALPHA, BETA, CAGR, CALMAR, MDD, PERIODIC_RATE, SHARPE, SORTINO, VOLATILITY


class TestMDD:
    """Tests for Maximum Drawdown."""

    def test_mdd_basic(self):
        """Test MDD with a simple drawdown scenario."""
        # 10% up, then 20% down, then 5% up
        returns = np.array([0.10, -0.20, 0.05])
        mdd = MDD(returns)

        # Cumulative: 1.10, 0.88, 0.924
        # Max so far: 1.10, 1.10, 1.10
        # Drawdown: 0, 0.20, 0.16
        assert mdd == pytest.approx(0.20, rel=1e-10)

    def test_mdd_no_drawdown(self):
        """Test MDD with all positive returns."""
        returns = np.array([0.05, 0.03, 0.02, 0.04])
        mdd = MDD(returns)
        assert mdd == pytest.approx(0.0, abs=1e-10)

    def test_mdd_empty(self):
        """Test MDD with empty array."""
        returns = np.array([])
        mdd = MDD(returns)
        assert mdd == 0.0

    def test_mdd_single_loss(self):
        """Test MDD with single loss."""
        returns = np.array([-0.15])
        mdd = MDD(returns)
        assert mdd == pytest.approx(0.15, rel=1e-10)

    def test_mdd_recovery(self):
        """Test MDD after recovery."""
        # Down 50%, then up 100% (full recovery)
        returns = np.array([-0.50, 1.00])
        mdd = MDD(returns)
        # Cumulative: 0.5, 1.0
        # Max: 1.0, 1.0
        # The max drawdown was 50%
        assert mdd == pytest.approx(0.50, rel=1e-10)


class TestCAGR:
    """Tests for Compound Annual Growth Rate."""

    def test_cagr_basic(self):
        """Test CAGR with known returns."""
        # 252 daily returns of ~0.0397% each should give ~10% annual
        daily_return = (1.10 ** (1 / 252)) - 1
        returns = np.full(252, daily_return)
        cagr = CAGR(returns, periods_per_year=252)
        assert cagr == pytest.approx(0.10, rel=1e-3)

    def test_cagr_two_years(self):
        """Test CAGR over two years."""
        # 21% total over 2 years = 10% CAGR
        daily_return = (1.21 ** (1 / 504)) - 1
        returns = np.full(504, daily_return)
        cagr = CAGR(returns, periods_per_year=252)
        assert cagr == pytest.approx(0.10, rel=1e-3)

    def test_cagr_negative(self):
        """Test CAGR with negative total return."""
        # -10% per period for simplicity
        returns = np.array([-0.10, -0.10])
        cagr = CAGR(returns, periods_per_year=2)
        # Total return: 0.9 * 0.9 - 1 = -0.19
        # CAGR: (0.81)^1 - 1 = -0.19
        assert cagr < 0

    def test_cagr_empty(self):
        """Test CAGR with empty array."""
        returns = np.array([])
        cagr = CAGR(returns)
        assert cagr == 0.0


class TestVOLATILITY:
    """Tests for Annualized Volatility."""

    def test_volatility_basic(self):
        """Test volatility calculation."""
        # Daily returns with known std
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, 252)  # ~2% daily vol
        vol = VOLATILITY(returns, periods_per_year=252)
        # Should be approximately 2% * sqrt(252) ≈ 31.7%
        assert vol == pytest.approx(0.02 * np.sqrt(252), rel=0.15)

    def test_volatility_zero(self):
        """Test volatility with constant returns."""
        returns = np.full(100, 0.01)
        vol = VOLATILITY(returns)
        assert vol == pytest.approx(0.0, abs=1e-10)

    def test_volatility_single(self):
        """Test volatility with single return."""
        returns = np.array([0.05])
        vol = VOLATILITY(returns)
        assert vol == 0.0


class TestSHARPE:
    """Tests for Sharpe Ratio."""

    def test_sharpe_positive(self):
        """Test Sharpe ratio with positive excess returns."""
        # Daily returns with mean 0.05% and std 1%
        np.random.seed(42)
        mean_return = 0.0005
        std_return = 0.01
        returns = np.random.normal(mean_return, std_return, 252)
        sharpe = SHARPE(returns, risk_free=0, periods_per_year=252)

        # Expected Sharpe ≈ (mean / std) * sqrt(252)
        expected = (np.mean(returns) / np.std(returns, ddof=1)) * np.sqrt(252)
        assert sharpe == pytest.approx(expected, rel=1e-5)

    def test_sharpe_with_risk_free(self):
        """Test Sharpe ratio with non-zero risk-free rate."""
        returns = np.array([0.01, 0.02, 0.015, 0.012, 0.018])
        risk_free = 0.001  # 0.1% per period
        sharpe = SHARPE(returns, risk_free=risk_free, periods_per_year=252)

        excess = returns - risk_free
        expected = (np.mean(excess) / np.std(excess, ddof=1)) * np.sqrt(252)
        assert sharpe == pytest.approx(expected, rel=1e-5)

    def test_sharpe_zero_vol_is_nan(self):
        """No volatility leaves the ratio undefined; 0.0 would read as "no excess return"."""
        returns = np.full(10, 0.01)

        assert np.isnan(SHARPE(returns))

    def test_sharpe_with_risk_free_array(self):
        """A per-period risk-free series is subtracted bar by bar."""
        returns = np.array([0.01, 0.02, 0.015, 0.012, 0.018])
        risk_free = np.array([0.0001, 0.0002, 0.0001, 0.0003, 0.0002])

        excess = returns - risk_free
        expected = (np.mean(excess) / np.std(excess, ddof=1)) * np.sqrt(252)
        assert SHARPE(returns, risk_free=risk_free) == pytest.approx(expected, rel=1e-12)

    @pytest.mark.parametrize("ratio", [SHARPE, SORTINO], ids=lambda f: f.__name__)
    def test_risk_free_length_mismatch_raises(self, ratio):
        with pytest.raises(ValueError, match="aligned with returns"):
            ratio(np.zeros(5), risk_free=np.zeros(4))


class TestSORTINO:
    """Tests for Sortino Ratio."""

    def test_sortino_basic(self):
        """Test Sortino ratio calculation."""
        # Mix of positive and negative returns
        returns = np.array([0.02, -0.01, 0.03, -0.02, 0.01, 0.02, -0.005])
        sortino = SORTINO(returns, risk_free=0, periods_per_year=252)

        # Should be positive for this mix
        assert sortino > 0

    def test_sortino_no_downside(self):
        """Test Sortino ratio with no negative returns."""
        returns = np.array([0.01, 0.02, 0.015, 0.012])
        sortino = SORTINO(returns, risk_free=0, periods_per_year=252)
        assert sortino == float("inf")

    def test_sortino_vs_sharpe(self):
        """With a positive mean, Sortino >= Sharpe: the downside deviation over all N is below the std."""
        np.random.seed(42)
        returns = np.random.normal(0.004, 0.02, 100)
        assert np.mean(returns) > 0

        assert SORTINO(returns) >= SHARPE(returns)

    def test_sortino_downside_averages_over_all_periods(self):
        """Hand-computed: r = [2%, -1%, 3%, -2%] → DD = sqrt((1e-4 + 4e-4) / 4), not / 2."""
        returns = np.array([0.02, -0.01, 0.03, -0.02])

        downside = np.sqrt((0.01**2 + 0.02**2) / 4)
        expected = (0.005 / downside) * np.sqrt(252)
        assert SORTINO(returns) == pytest.approx(expected, rel=1e-12)

    def test_sortino_target_is_risk_free(self):
        """Returns above zero but below the risk-free rate count as downside."""
        returns = np.array([0.001, 0.003, 0.0005, 0.004])
        risk_free = 0.002

        excess = returns - risk_free
        downside = np.sqrt(np.mean(np.minimum(excess, 0) ** 2))
        expected = (np.mean(excess) / downside) * np.sqrt(252)
        assert SORTINO(returns, risk_free=risk_free) == pytest.approx(expected, rel=1e-12)

    def test_sortino_flat_series_is_nan(self):
        """No downside and no excess return: undefined, neither 0 nor inf."""
        assert np.isnan(SORTINO(np.zeros(10)))

    def test_sortino_all_negative_below_risk_free(self):
        """Test Sortino when every return is negative and below the risk-free rate."""
        returns = np.array([-0.01, -0.02, -0.015, -0.03, -0.01])
        risk_free = 0.0
        periods_per_year = 252

        sortino = SORTINO(returns, risk_free=risk_free, periods_per_year=periods_per_year)

        excess_returns = returns - risk_free
        mean_excess = np.mean(excess_returns)
        negative_returns = excess_returns[excess_returns < 0]
        downside_std = np.sqrt(np.mean(negative_returns**2))
        expected = (mean_excess / downside_std) * np.sqrt(periods_per_year)

        assert np.isfinite(sortino)
        assert sortino < 0
        np.testing.assert_allclose(sortino, expected, rtol=1e-10)


class TestCALMAR:
    """Tests for Calmar Ratio."""

    def test_calmar_basic(self):
        """Test Calmar ratio calculation."""
        # Returns that give 10% CAGR and 20% MDD
        daily_return = (1.10 ** (1 / 252)) - 1
        returns = np.full(252, daily_return)
        # Add a drawdown
        returns[100] = -0.20  # Big down day

        calmar = CALMAR(returns, periods_per_year=252)
        cagr = CAGR(returns, periods_per_year=252)
        mdd = MDD(returns)

        assert calmar == pytest.approx(cagr / mdd, rel=1e-5)

    def test_calmar_no_drawdown(self):
        """Test Calmar ratio with no drawdown."""
        returns = np.array([0.01, 0.02, 0.01, 0.015])
        calmar = CALMAR(returns, periods_per_year=252)
        assert calmar == float("inf")

    def test_calmar_empty(self):
        """Test Calmar ratio with empty array."""
        returns = np.array([])
        calmar = CALMAR(returns)
        assert calmar == 0.0


def _benchmark(n: int = 252, seed: int = 7) -> np.ndarray:
    return np.random.default_rng(seed).normal(0.0004, 0.01, n)


class TestBETA:
    """Tests for Beta. No ta-lib counterpart, so the oracle is the formula itself."""

    def test_beta_hand_computed(self):
        """Cov/Var by hand: b = [1, 2, 3]%, r = [2, 1, 6]% → cov 2e-4, var 1e-4."""
        benchmark = np.array([0.01, 0.02, 0.03])
        returns = np.array([0.02, 0.01, 0.06])

        assert BETA(returns, benchmark) == pytest.approx(2.0, rel=1e-12)

    def test_beta_of_linear_combination(self):
        """r = c + k·b gives beta k exactly, whatever the intercept."""
        benchmark = _benchmark()

        assert BETA(0.0003 + 1.5 * benchmark, benchmark) == pytest.approx(1.5, rel=1e-12)
        assert BETA(-0.5 * benchmark, benchmark) == pytest.approx(-0.5, rel=1e-12)

    def test_beta_matches_ols_slope(self):
        """Beta is the OLS slope of returns on the benchmark."""
        benchmark = _benchmark()
        returns = 1.2 * benchmark + np.random.default_rng(1).normal(0, 0.005, benchmark.size)

        slope = np.polyfit(benchmark, returns, 1)[0]
        assert BETA(returns, benchmark) == pytest.approx(slope, rel=1e-10)

    def test_beta_of_benchmark_is_one(self):
        benchmark = _benchmark()

        assert BETA(benchmark, benchmark) == pytest.approx(1.0, rel=1e-12)

    def test_beta_length_mismatch_raises(self):
        """Arrays that are not date-aligned must not be silently truncated."""
        with pytest.raises(ValueError, match="same length"):
            BETA(np.zeros(5), np.zeros(4))

    @pytest.mark.parametrize(
        "returns, benchmark",
        [
            (np.array([0.01]), np.array([0.02])),
            (np.array([0.01, 0.02, -0.01]), np.full(3, 0.01)),
        ],
        ids=["single-period", "flat-benchmark"],
    )
    def test_beta_undefined_is_nan(self, returns, benchmark):
        assert np.isnan(BETA(returns, benchmark))


class TestALPHA:
    """Tests for Jensen's Alpha (annualized, arithmetic)."""

    def test_alpha_of_constructed_series(self):
        """r - rf = a + β(b - rf) exactly → alpha = a × periods_per_year."""
        benchmark = _benchmark()
        a, beta, rf = 0.0002, 1.3, 0.0001
        returns = rf + a + beta * (benchmark - rf)

        assert ALPHA(returns, benchmark, risk_free=rf) == pytest.approx(a * 252, rel=1e-10)

    def test_alpha_with_risk_free_array(self):
        """A per-period risk-free series (e.g. daily from treasury yields) is subtracted bar by bar."""
        benchmark = _benchmark()
        rf = np.linspace(0.00008, 0.00014, benchmark.size)
        a, beta = -0.0001, 0.8
        returns = rf + a + beta * (benchmark - rf)

        assert ALPHA(returns, benchmark, risk_free=rf, periods_per_year=250) == pytest.approx(a * 250, rel=1e-10)

    def test_alpha_of_benchmark_is_zero(self):
        benchmark = _benchmark()

        assert ALPHA(benchmark, benchmark, risk_free=0.0001) == pytest.approx(0.0, abs=1e-15)

    def test_alpha_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="same length"):
            ALPHA(np.zeros(3), np.zeros(4))

    def test_alpha_flat_benchmark_is_nan(self):
        assert np.isnan(ALPHA(np.array([0.01, 0.02, -0.01]), np.full(3, 0.01)))


class TestPortfolioIntegration:
    """Integration tests for portfolio metrics."""

    def test_realistic_portfolio(self):
        """Test all metrics with realistic daily returns."""
        np.random.seed(42)
        # Simulate 1 year of daily returns: ~10% annual return, ~20% vol
        n_days = 252
        daily_vol = 0.20 / np.sqrt(252)
        daily_mean = 0.10 / 252
        returns = np.random.normal(daily_mean, daily_vol, n_days)

        mdd = MDD(returns)
        cagr = CAGR(returns, periods_per_year=252)
        vol = VOLATILITY(returns, periods_per_year=252)
        sharpe = SHARPE(returns, periods_per_year=252)
        sortino = SORTINO(returns, periods_per_year=252)
        calmar = CALMAR(returns, periods_per_year=252)

        # All should be finite
        assert np.isfinite(mdd)
        assert np.isfinite(cagr)
        assert np.isfinite(vol)
        assert np.isfinite(sharpe)
        assert np.isfinite(sortino)
        assert np.isfinite(calmar)

        # MDD should be positive
        assert mdd >= 0

        # Volatility should be approximately 20%
        assert 0.10 < vol < 0.40

    def test_bear_market(self):
        """Test metrics in a bear market scenario."""
        # Simulate -30% annual return
        returns = np.full(252, -0.30 / 252)
        returns += np.random.normal(0, 0.01, 252)

        mdd = MDD(returns)
        cagr = CAGR(returns, periods_per_year=252)
        sharpe = SHARPE(returns, periods_per_year=252)

        assert mdd > 0  # Should have drawdown
        assert cagr < 0  # Negative return
        assert sharpe < 0  # Negative Sharpe


class TestPortfolioGuards:
    """Edge inputs: wipe-outs (상장폐지), series too short for a standard deviation."""

    @pytest.mark.parametrize("periods_per_year", [0, -252])
    def test_cagr_non_positive_periods_per_year_is_zero(self, periods_per_year):
        """No year length to annualise over; 0 used to raise ZeroDivisionError."""
        returns = np.array([0.01, 0.02])

        assert CAGR(returns, periods_per_year=periods_per_year) == 0.0

    def test_cagr_total_loss_is_minus_one(self):
        """A position that goes to zero has CAGR -100%, however long the series."""
        returns = np.array([0.05, 0.02, -1.0])

        assert CAGR(returns, periods_per_year=252) == -1.0

    def test_cagr_loss_beyond_total_is_capped_at_minus_one(self):
        """A leveraged loss over 100% must not be raised to a power (sign flips for even exponents)."""
        returns = np.array([-1.5])

        # Uncapped: (1 - 1.5) ** (1 / 0.5) - 1 = -0.75
        assert CAGR(returns, periods_per_year=2) == -1.0

    @pytest.mark.parametrize("ratio", [SHARPE, SORTINO], ids=lambda f: f.__name__)
    def test_ratio_of_single_return_is_nan(self, ratio):
        """One return has no dispersion to divide by."""
        assert np.isnan(ratio(np.array([0.01])))

    def test_sortino_underflowing_downside_is_treated_as_none(self):
        """Negative returns so small their squares underflow count as no downside."""
        returns = np.array([0.01, -1e-200])

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            sortino = SORTINO(returns)

        assert sortino == float("inf")


class TestPERIODIC_RATE:
    """Annual → per-period rate for risk_free."""

    def test_compounds_back_to_annual(self):
        daily = PERIODIC_RATE(0.035, periods_per_year=252)

        assert isinstance(daily, float)
        assert (1 + daily) ** 252 - 1 == pytest.approx(0.035, rel=1e-12)

    def test_array_keeps_shape(self):
        """A daily treasury series (ECOS gives percent: divide by 100 first) converts element-wise."""
        annual = np.array([3.5, 3.4, 3.6]) / 100

        daily = PERIODIC_RATE(annual)

        assert daily.shape == (3,)
        np.testing.assert_allclose((1 + daily) ** 252 - 1, annual, rtol=1e-12)

    def test_annual_rate_passed_raw_is_far_off(self):
        """Why the helper exists: a raw annual 3.5% as risk_free flips a strong Sharpe negative."""
        returns = np.tile([0.012, -0.008], 126)  # mean 0.2% a day, std 1%

        assert SHARPE(returns, risk_free=PERIODIC_RATE(0.035)) > 0
        assert SHARPE(returns, risk_free=0.035) < 0
