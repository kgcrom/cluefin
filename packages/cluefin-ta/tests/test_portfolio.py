"""
Tests for portfolio metrics (MDD, CAGR, SHARPE, SORTINO, CALMAR, VOLATILITY).
"""

import numpy as np
import pytest

from cluefin_ta import CAGR, CALMAR, MDD, SHARPE, SORTINO, VOLATILITY


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

    def test_sharpe_zero_vol(self):
        """Test Sharpe ratio with zero volatility."""
        returns = np.full(10, 0.01)
        sharpe = SHARPE(returns)
        assert sharpe == 0.0


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
        """Test that Sortino >= Sharpe for same returns."""
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, 100)
        sharpe = SHARPE(returns, periods_per_year=252)
        sortino = SORTINO(returns, periods_per_year=252)

        # Sortino should be >= Sharpe when there are negative returns
        # because downside std <= total std
        if np.any(returns < 0):
            assert sortino >= sharpe


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
