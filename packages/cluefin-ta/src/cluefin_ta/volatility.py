"""
Volatility Indicators - ta-lib compatible implementations.

Functions:
    TRANGE: True Range
    ATR: Average True Range
    NATR: Normalized Average True Range
"""

import numpy as np


def TRANGE(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    True Range.

    True Range is the greatest of:
    - Current High - Current Low
    - |Current High - Previous Close|
    - |Current Low - Previous Close|

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array of True Range values with NaN for first element
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.full(n, np.nan)

    if n < 2:
        return result

    # Calculate True Range for each period (starting from index 1)
    for i in range(1, n):
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        result[i] = max(hl, hc, lc)

    return result


def ATR(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Average True Range.

    Uses Wilder's smoothing method (similar to EMA with alpha = 1/timeperiod).

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of ATR values with NaN for initial periods
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.full(n, np.nan)

    if n < timeperiod + 1:
        return result

    # Calculate True Range
    tr = TRANGE(high, low, close)

    # First ATR value is SMA of True Range
    result[timeperiod] = np.mean(tr[1 : timeperiod + 1])

    # Subsequent values use Wilder's smoothing
    for i in range(timeperiod + 1, n):
        result[i] = (result[i - 1] * (timeperiod - 1) + tr[i]) / timeperiod

    return result


def NATR(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    timeperiod: int = 14,
) -> np.ndarray:
    """
    Normalized Average True Range.

    NATR = (ATR / Close) * 100

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        timeperiod: Number of periods (default: 14)

    Returns:
        Array of NATR values (percentage) with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)

    atr = ATR(high, low, close, timeperiod)

    # Avoid division by zero
    with np.errstate(divide="ignore", invalid="ignore"):
        result = (atr / close) * 100.0
        result = np.where(close == 0, np.nan, result)

    return result


__all__ = ["TRANGE", "ATR", "NATR"]
