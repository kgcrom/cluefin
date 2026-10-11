"""
Volume Indicators - ta-lib compatible implementations.

Functions:
    OBV: On Balance Volume
    AD: Accumulation/Distribution Line
    ADOSC: Chaikin A/D Oscillator
"""

import numpy as np

from cluefin_ta._core import ad_loop, obv_loop


def OBV(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """
    On Balance Volume.

    OBV is a cumulative indicator that adds volume on up days
    and subtracts volume on down days.

    Args:
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of OBV values
    """
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < 2:
        result = np.zeros(n, dtype=np.float64)
        if n >= 1:
            result[0] = volume[0]
        return result

    return obv_loop(close, volume)


def AD(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
) -> np.ndarray:
    """
    Accumulation/Distribution Line (Chaikin A/D Line).

    AD = Previous AD + Money Flow Volume
    where Money Flow Volume = Money Flow Multiplier * Volume
    and Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data

    Returns:
        Array of A/D values
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < 1:
        return np.zeros(n, dtype=np.float64)

    return ad_loop(high, low, close, volume)


def ADOSC(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    fastperiod: int = 3,
    slowperiod: int = 10,
) -> np.ndarray:
    """
    Chaikin A/D Oscillator.

    ADOSC = EMA(AD, fastperiod) - EMA(AD, slowperiod)

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        volume: Array of volume data
        fastperiod: Fast EMA period (default: 3)
        slowperiod: Slow EMA period (default: 10)

    Returns:
        Array of ADOSC values with NaN for initial periods
    """
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    volume = np.asarray(volume, dtype=np.float64)
    n = len(close)

    if n < slowperiod:
        return np.full(n, np.nan)

    # Calculate A/D line
    ad = AD(high, low, close, volume)

    # Calculate EMAs of A/D using ta-lib's EMA algorithm
    # ta-lib uses a different EMA calculation for ADOSC
    # It starts EMA from index 0 (no warmup period for A/D values)
    result = np.full(n, np.nan)

    fast_ema = _ema_from_first(ad, fastperiod)
    slow_ema = _ema_from_first(ad, slowperiod)

    # ADOSC = Fast EMA - Slow EMA (starting from slowperiod - 1)
    result[slowperiod - 1 :] = fast_ema[slowperiod - 1 :] - slow_ema[slowperiod - 1 :]

    return result


def _ema_from_first(values: np.ndarray, period: int) -> np.ndarray:
    """EMA seeded with the first value, in ADOSC's ``k * x + (1 - k) * prev`` form."""
    alpha = 2.0 / (period + 1)
    prev = float(values[0])
    smoothed = [prev]
    for value in values[1:].tolist():
        prev = alpha * value + (1 - alpha) * prev
        smoothed.append(prev)
    return np.array(smoothed)


__all__ = ["OBV", "AD", "ADOSC"]
