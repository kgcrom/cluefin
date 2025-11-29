"""
Volume Indicators - ta-lib compatible implementations.

Functions:
    OBV: On Balance Volume
    AD: Accumulation/Distribution Line
"""

import numpy as np


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

    result = np.zeros(n, dtype=np.float64)

    if n < 2:
        return result

    # First value
    result[0] = volume[0]

    # Calculate OBV
    for i in range(1, n):
        if close[i] > close[i - 1]:
            result[i] = result[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            result[i] = result[i - 1] - volume[i]
        else:
            result[i] = result[i - 1]

    return result


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

    result = np.zeros(n, dtype=np.float64)

    if n < 1:
        return result

    for i in range(n):
        hl_range = high[i] - low[i]

        if hl_range != 0:
            # Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)
            # Simplified: (2 * Close - Low - High) / (High - Low)
            mfm = ((close[i] - low[i]) - (high[i] - close[i])) / hl_range
        else:
            mfm = 0.0

        # Money Flow Volume
        mfv = mfm * volume[i]

        # Accumulate
        if i == 0:
            result[i] = mfv
        else:
            result[i] = result[i - 1] + mfv

    return result


__all__ = ["OBV", "AD"]
