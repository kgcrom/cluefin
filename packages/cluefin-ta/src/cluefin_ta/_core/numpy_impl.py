"""
Pure NumPy implementations of low-level technical analysis computations.

These functions are used when Numba is not available.
All functions are designed to match Numba-accelerated versions exactly.
"""

import numpy as np


def ema_loop(
    close: np.ndarray, period: int, alpha: float, initial_sma: float
) -> np.ndarray:
    """
    EMA calculation loop.

    Args:
        close: Array of closing prices
        period: EMA period
        alpha: Smoothing factor (2 / (period + 1))
        initial_sma: Initial SMA value for first EMA

    Returns:
        Array of EMA values with NaN for initial periods
    """
    n = len(close)
    result = np.full(n, np.nan)
    result[period - 1] = initial_sma

    for i in range(period, n):
        result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]

    return result


def rolling_std(data: np.ndarray, period: int) -> np.ndarray:
    """
    Rolling standard deviation (population).

    Args:
        data: Input data array
        period: Window size

    Returns:
        Array of rolling std values with NaN for initial periods
    """
    n = len(data)
    result = np.full(n, np.nan)

    for i in range(period - 1, n):
        window = data[i - period + 1 : i + 1]
        result[i] = np.std(window, ddof=0)

    return result


def wilder_smooth(
    values: np.ndarray, period: int, initial_value: float, start_idx: int
) -> np.ndarray:
    """
    Wilder's smoothing method.

    Used by RSI and ATR for smoothed averages.

    Args:
        values: Input values to smooth
        period: Smoothing period
        initial_value: Initial value (typically SMA of first period)
        start_idx: Starting index for smoothed values

    Returns:
        Array of smoothed values with NaN for initial periods
    """
    n = len(values)
    result = np.full(n, np.nan)
    result[start_idx] = initial_value

    for i in range(start_idx + 1, n):
        result[i] = (result[i - 1] * (period - 1) + values[i]) / period

    return result


def rolling_minmax(
    high: np.ndarray, low: np.ndarray, period: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Rolling highest high and lowest low.

    Args:
        high: Array of high prices
        low: Array of low prices
        period: Window size

    Returns:
        Tuple of (highest_high, lowest_low) arrays
    """
    n = len(high)
    highest = np.full(n, np.nan)
    lowest = np.full(n, np.nan)

    for i in range(period - 1, n):
        highest[i] = np.max(high[i - period + 1 : i + 1])
        lowest[i] = np.min(low[i - period + 1 : i + 1])

    return highest, lowest


def true_range_loop(
    high: np.ndarray, low: np.ndarray, close: np.ndarray
) -> np.ndarray:
    """
    True Range calculation loop.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array of True Range values with NaN for first element
    """
    n = len(close)
    result = np.full(n, np.nan)

    for i in range(1, n):
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        result[i] = max(hl, hc, lc)

    return result


def obv_loop(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    On Balance Volume calculation loop.

    Args:
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of OBV values
    """
    n = len(close)
    result = np.zeros(n, dtype=np.float64)
    result[0] = volume[0]

    for i in range(1, n):
        if close[i] > close[i - 1]:
            result[i] = result[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            result[i] = result[i - 1] - volume[i]
        else:
            result[i] = result[i - 1]

    return result


def ad_loop(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray
) -> np.ndarray:
    """
    Accumulation/Distribution calculation loop.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of A/D values
    """
    n = len(close)
    result = np.zeros(n, dtype=np.float64)

    for i in range(n):
        hl_range = high[i] - low[i]

        if hl_range != 0:
            mfm = ((close[i] - low[i]) - (high[i] - close[i])) / hl_range
        else:
            mfm = 0.0

        mfv = mfm * volume[i]

        if i == 0:
            result[i] = mfv
        else:
            result[i] = result[i - 1] + mfv

    return result


__all__ = [
    "ema_loop",
    "rolling_std",
    "wilder_smooth",
    "rolling_minmax",
    "true_range_loop",
    "obv_loop",
    "ad_loop",
]
