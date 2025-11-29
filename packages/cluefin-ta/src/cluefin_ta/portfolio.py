"""
Portfolio Metrics - Risk and return analysis functions.

Functions:
    MDD: Maximum Drawdown
    CAGR: Compound Annual Growth Rate
    SHARPE: Sharpe Ratio
    SORTINO: Sortino Ratio
    CALMAR: Calmar Ratio
    VOLATILITY: Annualized Volatility

These functions are not part of ta-lib but are commonly used
for portfolio performance analysis.
"""

import numpy as np


def MDD(returns: np.ndarray) -> float:
    """
    Maximum Drawdown.

    Calculates the maximum peak-to-trough decline in portfolio value.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)

    Returns:
        Maximum drawdown as a positive decimal (e.g., 0.2 for 20% drawdown)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) == 0:
        return 0.0

    # Calculate cumulative returns (wealth index) starting from 1
    # Include initial value of 1 to properly track from beginning
    cumulative = np.concatenate([[1.0], np.cumprod(1 + returns)])

    # Calculate running maximum
    running_max = np.maximum.accumulate(cumulative)

    # Calculate drawdowns
    drawdowns = (running_max - cumulative) / running_max

    return float(np.max(drawdowns))


def CAGR(returns: np.ndarray, periods_per_year: int = 252) -> float:
    """
    Compound Annual Growth Rate.

    Calculates the annualized return assuming compounding.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        CAGR as a decimal (e.g., 0.1 for 10% annual return)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) == 0:
        return 0.0

    # Calculate total return
    total_return = np.prod(1 + returns) - 1

    # Calculate number of years
    n_periods = len(returns)
    n_years = n_periods / periods_per_year

    if n_years <= 0:
        return 0.0

    # CAGR = (1 + total_return)^(1/n_years) - 1
    if total_return <= -1:
        return -1.0  # Total loss

    cagr = (1 + total_return) ** (1 / n_years) - 1

    return float(cagr)


def VOLATILITY(returns: np.ndarray, periods_per_year: int = 252) -> float:
    """
    Annualized Volatility.

    Calculates the annualized standard deviation of returns.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Annualized volatility as a decimal (e.g., 0.2 for 20% volatility)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) < 2:
        return 0.0

    # Annualize the standard deviation
    return float(np.std(returns, ddof=1) * np.sqrt(periods_per_year))


def SHARPE(
    returns: np.ndarray,
    risk_free: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Sharpe Ratio.

    Calculates the risk-adjusted return using total volatility.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        risk_free: Risk-free rate per period (default: 0)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Sharpe ratio (annualized)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) < 2:
        return 0.0

    # Calculate excess returns
    excess_returns = returns - risk_free

    # Calculate mean and std of excess returns
    mean_excess = np.mean(excess_returns)
    std_excess = np.std(excess_returns, ddof=1)

    if std_excess == 0 or np.isclose(std_excess, 0, atol=1e-15):
        return 0.0

    # Annualize the Sharpe ratio
    sharpe = (mean_excess / std_excess) * np.sqrt(periods_per_year)

    return float(sharpe)


def SORTINO(
    returns: np.ndarray,
    risk_free: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Sortino Ratio.

    Calculates the risk-adjusted return using downside volatility only.
    Unlike Sharpe ratio, it only penalizes downside volatility.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        risk_free: Risk-free rate per period (default: 0)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Sortino ratio (annualized)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) < 2:
        return 0.0

    # Calculate excess returns
    excess_returns = returns - risk_free

    # Calculate mean excess return
    mean_excess = np.mean(excess_returns)

    # Calculate downside deviation (only negative returns)
    negative_returns = excess_returns[excess_returns < 0]

    if len(negative_returns) == 0:
        # No negative returns, return infinity or large number
        return float("inf") if mean_excess > 0 else 0.0

    # Downside deviation (semi-standard deviation)
    downside_std = np.sqrt(np.mean(negative_returns**2))

    if downside_std == 0:
        return 0.0

    # Annualize the Sortino ratio
    sortino = (mean_excess / downside_std) * np.sqrt(periods_per_year)

    return float(sortino)


def CALMAR(returns: np.ndarray, periods_per_year: int = 252) -> float:
    """
    Calmar Ratio.

    Calculates the ratio of CAGR to Maximum Drawdown.
    Higher values indicate better risk-adjusted performance.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Calmar ratio (CAGR / MDD)
    """
    returns = np.asarray(returns, dtype=np.float64)

    if len(returns) == 0:
        return 0.0

    cagr = CAGR(returns, periods_per_year)
    mdd = MDD(returns)

    if mdd == 0:
        return float("inf") if cagr > 0 else 0.0

    return float(cagr / mdd)


__all__ = [
    "MDD",
    "CAGR",
    "VOLATILITY",
    "SHARPE",
    "SORTINO",
    "CALMAR",
]
