"""
Overlap Studies (Moving Averages) - ta-lib compatible implementations.

Functions:
    SMA: Simple Moving Average
    EMA: Exponential Moving Average
    WMA: Weighted Moving Average
    DEMA: Double Exponential Moving Average
    TEMA: Triple Exponential Moving Average
    KAMA: Kaufman Adaptive Moving Average
    BBANDS: Bollinger Bands
"""

import numpy as np

from cluefin_ta._core import get_impl


def SMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Simple Moving Average.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of SMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    # Use cumsum for efficient calculation (already vectorized, no Numba needed)
    cumsum = np.cumsum(np.insert(close, 0, 0))
    result[timeperiod - 1 :] = (cumsum[timeperiod:] - cumsum[:-timeperiod]) / timeperiod

    return result


def EMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Exponential Moving Average.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of EMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < timeperiod:
        return np.full(n, np.nan)

    # Calculate multiplier (smoothing factor)
    alpha = 2.0 / (timeperiod + 1)

    # Initialize with SMA for the first EMA value
    initial_sma = np.mean(close[:timeperiod])

    # Use optimized implementation
    impl = get_impl()
    return impl.ema_loop(close, timeperiod, alpha, initial_sma)


def WMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Weighted Moving Average.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of WMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)
    result = np.full(n, np.nan)

    if n < timeperiod:
        return result

    # Create weights: 1, 2, 3, ..., timeperiod
    weights = np.arange(1, timeperiod + 1, dtype=np.float64)
    weight_sum = weights.sum()

    # Calculate WMA for each position
    for i in range(timeperiod - 1, n):
        window = close[i - timeperiod + 1 : i + 1]
        result[i] = np.sum(window * weights) / weight_sum

    return result


def DEMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Double Exponential Moving Average.

    DEMA = 2 * EMA(close) - EMA(EMA(close))

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of DEMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < timeperiod:
        return np.full(n, np.nan)

    # Calculate EMA of close
    ema1 = EMA(close, timeperiod)

    # For EMA of EMA, we need to handle NaN values - only use valid values
    # ta-lib calculates EMA2 starting from the first valid EMA1 value
    valid_start = timeperiod - 1
    ema1_valid = ema1[valid_start:]

    # Calculate EMA of the valid EMA1 values
    ema2_valid = EMA(ema1_valid, timeperiod)

    # Map back to full array
    ema2 = np.full(n, np.nan)
    ema2[valid_start:] = ema2_valid

    # DEMA = 2 * EMA1 - EMA2
    return 2.0 * ema1 - ema2


def TEMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Triple Exponential Moving Average.

    TEMA = 3 * EMA1 - 3 * EMA2 + EMA3

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 30)

    Returns:
        Array of TEMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < timeperiod:
        return np.full(n, np.nan)

    # Calculate EMA1
    ema1 = EMA(close, timeperiod)

    # For EMA2, use valid EMA1 values only
    valid_start1 = timeperiod - 1
    ema1_valid = ema1[valid_start1:]
    ema2_valid = EMA(ema1_valid, timeperiod)

    ema2 = np.full(n, np.nan)
    ema2[valid_start1:] = ema2_valid

    # For EMA3, use valid EMA2 values only
    valid_start2 = valid_start1 + timeperiod - 1
    if valid_start2 < n:
        ema2_for_ema3 = ema2[valid_start1:]
        ema3_part = EMA(ema2_for_ema3[~np.isnan(ema2_for_ema3)], timeperiod)

        ema3 = np.full(n, np.nan)
        ema3_start = valid_start2
        ema3[ema3_start : ema3_start + len(ema3_part)] = ema3_part
    else:
        ema3 = np.full(n, np.nan)

    # TEMA = 3 * EMA1 - 3 * EMA2 + EMA3
    return 3.0 * ema1 - 3.0 * ema2 + ema3


def KAMA(close: np.ndarray, timeperiod: int = 30) -> np.ndarray:
    """
    Kaufman Adaptive Moving Average.

    Uses efficiency ratio to dynamically adjust smoothing factor.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the efficiency ratio (default: 30)

    Returns:
        Array of KAMA values with NaN for initial periods
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < timeperiod:
        return np.full(n, np.nan)

    # Fast and slow smoothing constants (ta-lib defaults: fast=2, slow=30)
    fast_sc = 2.0 / (2 + 1)  # 2 / 3
    slow_sc = 2.0 / (30 + 1)  # 2 / 31

    impl = get_impl()
    return impl.kama_loop(close, timeperiod, fast_sc, slow_sc)


def BBANDS(
    close: np.ndarray,
    timeperiod: int = 5,
    nbdevup: float = 2.0,
    nbdevdn: float = 2.0,
    matype: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Bollinger Bands.

    Args:
        close: Array of closing prices
        timeperiod: Number of periods for the moving average (default: 5)
        nbdevup: Number of standard deviations for upper band (default: 2.0)
        nbdevdn: Number of standard deviations for lower band (default: 2.0)
        matype: Moving average type (0=SMA, 1=EMA) - currently only SMA supported

    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    if n < timeperiod:
        nan_arr = np.full(n, np.nan)
        return nan_arr, nan_arr.copy(), nan_arr.copy()

    # Calculate middle band (SMA)
    middle = SMA(close, timeperiod)

    # Use optimized rolling std
    impl = get_impl()
    std = impl.rolling_std(close, timeperiod)

    upper = middle + nbdevup * std
    lower = middle - nbdevdn * std

    return upper, middle, lower


__all__ = ["SMA", "EMA", "WMA", "DEMA", "TEMA", "KAMA", "BBANDS"]
