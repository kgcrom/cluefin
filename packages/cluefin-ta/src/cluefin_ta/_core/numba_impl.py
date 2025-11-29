"""
Numba-accelerated implementations of low-level technical analysis computations.

These functions provide significant speedup (4-6x) over pure NumPy implementations
by using JIT compilation with LLVM.
"""

import numpy as np
from numba import jit


@jit(nopython=True, cache=True)
def ema_loop(
    close: np.ndarray, period: int, alpha: float, initial_sma: float
) -> np.ndarray:
    """
    EMA calculation loop (Numba-accelerated).

    Args:
        close: Array of closing prices
        period: EMA period
        alpha: Smoothing factor (2 / (period + 1))
        initial_sma: Initial SMA value for first EMA

    Returns:
        Array of EMA values with NaN for initial periods
    """
    n = len(close)
    result = np.empty(n, dtype=np.float64)

    # Fill NaN for initial periods
    for i in range(period - 1):
        result[i] = np.nan

    result[period - 1] = initial_sma

    for i in range(period, n):
        result[i] = alpha * close[i] + (1 - alpha) * result[i - 1]

    return result


@jit(nopython=True, cache=True)
def rolling_std(data: np.ndarray, period: int) -> np.ndarray:
    """
    Rolling standard deviation - population (Numba-accelerated).

    Args:
        data: Input data array
        period: Window size

    Returns:
        Array of rolling std values with NaN for initial periods
    """
    n = len(data)
    result = np.empty(n, dtype=np.float64)

    # Fill NaN for initial periods
    for i in range(period - 1):
        result[i] = np.nan

    for i in range(period - 1, n):
        # Calculate mean
        total = 0.0
        for j in range(i - period + 1, i + 1):
            total += data[j]
        mean = total / period

        # Calculate variance
        var_sum = 0.0
        for j in range(i - period + 1, i + 1):
            diff = data[j] - mean
            var_sum += diff * diff

        result[i] = np.sqrt(var_sum / period)

    return result


@jit(nopython=True, cache=True)
def wilder_smooth(
    values: np.ndarray, period: int, initial_value: float, start_idx: int
) -> np.ndarray:
    """
    Wilder's smoothing method (Numba-accelerated).

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
    result = np.empty(n, dtype=np.float64)

    # Fill NaN for initial periods
    for i in range(start_idx):
        result[i] = np.nan

    result[start_idx] = initial_value

    for i in range(start_idx + 1, n):
        result[i] = (result[i - 1] * (period - 1) + values[i]) / period

    return result


@jit(nopython=True, cache=True)
def rolling_minmax(
    high: np.ndarray, low: np.ndarray, period: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Rolling highest high and lowest low (Numba-accelerated).

    Args:
        high: Array of high prices
        low: Array of low prices
        period: Window size

    Returns:
        Tuple of (highest_high, lowest_low) arrays
    """
    n = len(high)
    highest = np.empty(n, dtype=np.float64)
    lowest = np.empty(n, dtype=np.float64)

    # Fill NaN for initial periods
    for i in range(period - 1):
        highest[i] = np.nan
        lowest[i] = np.nan

    for i in range(period - 1, n):
        max_val = high[i - period + 1]
        min_val = low[i - period + 1]

        for j in range(i - period + 2, i + 1):
            if high[j] > max_val:
                max_val = high[j]
            if low[j] < min_val:
                min_val = low[j]

        highest[i] = max_val
        lowest[i] = min_val

    return highest, lowest


@jit(nopython=True, cache=True)
def true_range_loop(
    high: np.ndarray, low: np.ndarray, close: np.ndarray
) -> np.ndarray:
    """
    True Range calculation loop (Numba-accelerated).

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array of True Range values with NaN for first element
    """
    n = len(close)
    result = np.empty(n, dtype=np.float64)
    result[0] = np.nan

    for i in range(1, n):
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])

        # max of three values
        if hl >= hc and hl >= lc:
            result[i] = hl
        elif hc >= hl and hc >= lc:
            result[i] = hc
        else:
            result[i] = lc

    return result


@jit(nopython=True, cache=True)
def obv_loop(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    On Balance Volume calculation loop (Numba-accelerated).

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


@jit(nopython=True, cache=True)
def ad_loop(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray
) -> np.ndarray:
    """
    Accumulation/Distribution calculation loop (Numba-accelerated).

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
