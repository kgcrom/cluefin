"""
Portfolio Metrics - Risk and return analysis functions.

Functions:
    MDD: Maximum Drawdown
    CAGR: Compound Annual Growth Rate
    SHARPE: Sharpe Ratio
    SORTINO: Sortino Ratio
    CALMAR: Calmar Ratio
    VOLATILITY: Annualized Volatility
    BETA: Beta against a benchmark
    ALPHA: Jensen's Alpha against a benchmark
    PERIODIC_RATE: Annual rate to per-period rate (for risk_free)

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

    if len(returns) == 0 or periods_per_year <= 0:
        return 0.0

    # Calculate total return
    total_return = np.prod(1 + returns) - 1

    # Calculate number of years
    n_periods = len(returns)
    n_years = n_periods / periods_per_year

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


def PERIODIC_RATE(annual_rate: float | np.ndarray, periods_per_year: int = 252) -> float | np.ndarray:
    """
    Convert an annual rate to a per-period rate, compounding: ``(1 + r) ** (1 / n) - 1``.

    ``SHARPE``/``SORTINO``/``ALPHA`` take ``risk_free`` per period. Passing an annual
    yield straight in (``0.035`` for a 3.5% treasury) subtracts 3.5% from every *daily*
    return and swamps the ratio; convert it with this first.

    Args:
        annual_rate: Annual rate as a decimal (``0.035`` for 3.5% — ECOS and KIS quote
            yields in percent, so divide by 100). A scalar, or an array such as a daily
            series of treasury yields aligned with the returns.
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Per-period rate, a float for a scalar input or an array of the same shape
    """
    rate = (1 + np.asarray(annual_rate, dtype=np.float64)) ** (1 / periods_per_year) - 1
    return float(rate) if rate.ndim == 0 else rate


def _excess(returns: np.ndarray, risk_free: float | np.ndarray) -> np.ndarray:
    risk_free = np.asarray(risk_free, dtype=np.float64)
    if risk_free.ndim != 0 and risk_free.shape != returns.shape:
        raise ValueError(
            f"risk_free must be a scalar or an array aligned with returns; got {risk_free.shape} for {returns.shape}"
        )
    return returns - risk_free


def SHARPE(
    returns: np.ndarray,
    risk_free: float | np.ndarray = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Sharpe Ratio.

    Calculates the risk-adjusted return using total volatility:
    ``mean(r - rf) / std(r - rf, ddof=1) * sqrt(periods_per_year)``.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        risk_free: Risk-free rate **per period**, not annual — a scalar, or an array
            the same length as ``returns`` (e.g. daily treasury yields). Convert an
            annual rate with ``PERIODIC_RATE`` (default: 0)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Sharpe ratio (annualized), or NaN when there are fewer than 2 periods or the
        excess returns have no volatility (the ratio is undefined, not zero)

    Raises:
        ValueError: If ``risk_free`` is an array of a different length
    """
    returns = np.asarray(returns, dtype=np.float64)
    excess_returns = _excess(returns, risk_free)

    if len(returns) < 2:
        return float("nan")

    mean_excess = np.mean(excess_returns)
    std_excess = np.std(excess_returns, ddof=1)

    if np.isclose(std_excess, 0, atol=1e-15):
        return float("nan")

    return float((mean_excess / std_excess) * np.sqrt(periods_per_year))


def SORTINO(
    returns: np.ndarray,
    risk_free: float | np.ndarray = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Sortino Ratio.

    Calculates the risk-adjusted return using downside volatility only, with the
    risk-free rate as the target: ``mean(r - rf) / DD * sqrt(periods_per_year)``.
    The downside deviation ``DD = sqrt(mean(min(r - rf, 0) ** 2))`` averages over
    **all** periods (periods above the target count as zero), not over the losing
    periods only — dividing by the loss count inflates DD and understates the ratio.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        risk_free: Risk-free rate **per period**, not annual — a scalar, or an array
            the same length as ``returns``. Convert an annual rate with
            ``PERIODIC_RATE`` (default: 0)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Sortino ratio (annualized). ``inf`` when nothing falls below the target and the
        mean excess return is positive; NaN when there are fewer than 2 periods, or no
        downside with a non-positive mean

    Raises:
        ValueError: If ``risk_free`` is an array of a different length
    """
    returns = np.asarray(returns, dtype=np.float64)
    excess_returns = _excess(returns, risk_free)

    if len(returns) < 2:
        return float("nan")

    mean_excess = np.mean(excess_returns)
    downside_std = np.sqrt(np.mean(np.minimum(excess_returns, 0.0) ** 2))

    # No downside (or one so small its squares underflow)
    if downside_std == 0:
        return float("inf") if mean_excess > 0 else float("nan")

    return float((mean_excess / downside_std) * np.sqrt(periods_per_year))


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


def _paired(returns: np.ndarray, benchmark_returns: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    if returns.shape != benchmark_returns.shape:
        raise ValueError(
            f"returns and benchmark_returns must be date-aligned arrays of the same length; "
            f"got {returns.shape} and {benchmark_returns.shape}"
        )
    return returns, benchmark_returns


def _beta(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    if len(returns) < 2:
        return float("nan")
    benchmark_var = np.var(benchmark_returns, ddof=1)
    if np.isclose(benchmark_var, 0, atol=1e-30):
        return float("nan")
    return float(np.cov(returns, benchmark_returns, ddof=1)[0, 1] / benchmark_var)


def BETA(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Beta against a benchmark.

    Cov(returns, benchmark) / Var(benchmark), both with ``ddof=1``.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        benchmark_returns: Benchmark returns for the same periods, aligned by date
            with ``returns`` (same length, same order). Align before calling — e.g.
            a stock's suspended days must be dropped from both or filled in both.

    Returns:
        Beta, or NaN when there are fewer than 2 periods or the benchmark has no variance

    Raises:
        ValueError: If the two arrays differ in length
    """
    returns, benchmark_returns = _paired(returns, benchmark_returns)
    return _beta(returns, benchmark_returns)


def ALPHA(
    returns: np.ndarray,
    benchmark_returns: np.ndarray,
    risk_free: float | np.ndarray = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Jensen's Alpha against a benchmark (annualized).

    ``(mean(r - rf) - beta * mean(b - rf)) * periods_per_year``, where beta is taken
    over the excess returns ``r - rf`` and ``b - rf``.

    Args:
        returns: Array of periodic returns (e.g., daily returns as decimals)
        benchmark_returns: Benchmark returns for the same periods, aligned by date
        risk_free: Risk-free rate **per period** — a scalar, or an array the same
            length as ``returns``. Convert an annual rate with ``PERIODIC_RATE`` (default: 0)
        periods_per_year: Number of periods in a year (default: 252 for trading days)

    Returns:
        Annualized alpha as a decimal (e.g., 0.03 for 3% a year), or NaN when beta is
        undefined (fewer than 2 periods, or a benchmark with no variance)

    Raises:
        ValueError: If the arrays differ in length
    """
    returns, benchmark_returns = _paired(returns, benchmark_returns)
    excess, benchmark_excess = _excess(returns, risk_free), _excess(benchmark_returns, risk_free)
    beta = _beta(excess, benchmark_excess)
    if np.isnan(beta):
        return float("nan")
    return float((np.mean(excess) - beta * np.mean(benchmark_excess)) * periods_per_year)


__all__ = [
    "MDD",
    "CAGR",
    "VOLATILITY",
    "SHARPE",
    "SORTINO",
    "CALMAR",
    "BETA",
    "ALPHA",
    "PERIODIC_RATE",
]
