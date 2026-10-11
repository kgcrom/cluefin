"""
Low-level NumPy loops and rolling-window helpers shared by the indicator modules.
"""

import numpy as np


def ema_loop(values: np.ndarray, start: int, alpha: float, seed: float) -> np.ndarray:
    """
    EMA from ``seed`` at index ``start`` on, NaN before.

    Uses ta-lib's update ``prev + (x - prev) * alpha`` rather than
    ``alpha * x + (1 - alpha) * prev``; the two round differently.
    """
    n = len(values)
    result = np.full(n, np.nan)
    if start >= n:
        return result

    prev = seed
    result[start] = prev
    for i in range(start + 1, n):
        prev = (values[i] - prev) * alpha + prev
        result[i] = prev

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
    data = np.asarray(data, dtype=np.float64)
    n = len(data)
    result = np.full(n, np.nan)

    if n < period:
        return result

    # Vectorized rolling std using cumulative sums for O(n) performance.
    cumsum = np.cumsum(np.insert(data, 0, 0.0))
    cumsum_sq = np.cumsum(np.insert(data * data, 0, 0.0))

    sum_x = cumsum[period:] - cumsum[:-period]
    sum_x2 = cumsum_sq[period:] - cumsum_sq[:-period]

    mean = sum_x / period
    mean_sq = sum_x2 / period
    var = mean_sq - mean * mean
    var = np.maximum(var, 0.0)  # Numerical guard against small negatives

    result[period - 1 :] = np.sqrt(var)
    return result


def wilder_smooth(values: np.ndarray, period: int, initial_value: float, start_idx: int) -> np.ndarray:
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


def rolling_minmax(high: np.ndarray, low: np.ndarray, period: int) -> tuple[np.ndarray, np.ndarray]:
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


def true_range_loop(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    """
    True Range calculation (vectorized).

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
    n = len(close)
    result = np.full(n, np.nan)

    if n < 2:
        return result

    # Vectorized calculation for indices 1 to n
    prev_close = close[:-1]
    hl = high[1:] - low[1:]
    hc = np.abs(high[1:] - prev_close)
    lc = np.abs(low[1:] - prev_close)

    result[1:] = np.maximum(np.maximum(hl, hc), lc)
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


def ad_loop(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray) -> np.ndarray:
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


def kama_loop(
    close: np.ndarray,
    period: int,
    fast_sc: float,
    slow_sc: float,
) -> np.ndarray:
    """
    Kaufman Adaptive Moving Average, following ta-lib's TA_KAMA.

    The first value is at index ``period`` (seeded from ``close[period - 1]``). The
    volatility sum is a running total like ta-lib's, and an efficiency ratio whose
    volatility is (near) zero counts as 1, also like ta-lib.

    Args:
        close: Array of closing prices
        period: Efficiency ratio period
        fast_sc: Fast smoothing constant (2 / (fast + 1))
        slow_sc: Slow smoothing constant (2 / (slow + 1))

    Returns:
        Array of KAMA values with NaN for the first ``period`` bars
    """
    n = len(close)
    result = np.full(n, np.nan)

    if n <= period:
        return result

    prices = close.tolist()
    abs_diff = [abs(prices[j + 1] - prices[j]) for j in range(n - 1)]
    sc_range = fast_sc - slow_sc

    volatility = 0.0
    for j in range(period):
        volatility += abs_diff[j]

    kama = prices[period - 1]
    for i in range(period, n):
        if i > period:
            volatility -= abs_diff[i - period - 1]
            volatility += abs_diff[i - 1]
        change = prices[i] - prices[i - period]
        efficiency = 1.0 if volatility <= change or _is_zero(volatility) else abs(change / volatility)
        sc = efficiency * sc_range + slow_sc
        sc *= sc
        kama = (prices[i] - kama) * sc + kama
        result[i] = kama

    return result


def _is_zero(value: float) -> bool:
    """ta-lib's TA_IS_ZERO: within 1e-8 of zero."""
    return -1e-8 < value < 1e-8


def adx_loop(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
    """
    Average Directional Index, following ta-lib's TA_ADX.

    The Wilder sums of +DM, -DM and TR start from ``period - 1`` bars and are smoothed
    from bar ``period`` on; the first ADX (index ``2 * period - 1``) averages the DX of
    bars ``period .. 2 * period - 1``. A bar whose TR or DI sum is (near) zero adds no DX
    and leaves the ADX unchanged, as in ta-lib.

    Args:
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices
        period: Smoothing period

    Returns:
        Array of ADX values with NaN for the first ``2 * period - 1`` bars
    """
    n = len(close)
    result = np.full(n, np.nan)
    first = 2 * period - 1

    if n <= first:
        return result

    highs, lows, closes = high.tolist(), low.tolist(), close.tolist()
    plus_dm = minus_dm = tr = 0.0

    def directional_move(t: int) -> tuple[float, float]:
        up = highs[t] - highs[t - 1]
        down = lows[t - 1] - lows[t]
        if down > 0 and up < down:
            return 0.0, down
        if up > 0 and up > down:
            return up, 0.0
        return 0.0, 0.0

    def true_range(t: int) -> float:
        return max(highs[t] - lows[t], abs(highs[t] - closes[t - 1]), abs(lows[t] - closes[t - 1]))

    def smooth(t: int) -> None:
        nonlocal plus_dm, minus_dm, tr
        up, down = directional_move(t)
        minus_dm = minus_dm - minus_dm / period + down
        plus_dm = plus_dm - plus_dm / period + up
        tr = tr - tr / period + true_range(t)

    def directional_index() -> float | None:
        if _is_zero(tr):
            return None
        minus_di = 100.0 * (minus_dm / tr)
        plus_di = 100.0 * (plus_dm / tr)
        di_sum = minus_di + plus_di
        if _is_zero(di_sum):
            return None
        return 100.0 * (abs(minus_di - plus_di) / di_sum)

    for t in range(1, period):
        up, down = directional_move(t)
        plus_dm += up
        minus_dm += down
        tr += true_range(t)

    dx_sum = 0.0
    for t in range(period, first + 1):
        smooth(t)
        dx = directional_index()
        if dx is not None:
            dx_sum += dx

    adx = dx_sum / period
    result[first] = adx
    for t in range(first + 1, n):
        smooth(t)
        dx = directional_index()
        if dx is not None:
            adx = (adx * (period - 1) + dx) / period
        result[t] = adx

    return result


def mfi_loop(
    typical_price: np.ndarray,
    volume: np.ndarray,
    period: int,
) -> np.ndarray:
    """
    Money Flow Index calculation loop.

    Args:
        typical_price: Array of typical prices ((H+L+C)/3)
        volume: Array of volume data
        period: MFI period

    Returns:
        Array of MFI values (0-100) with NaN for initial periods
    """
    n = len(typical_price)
    result = np.full(n, np.nan)

    if n < period + 1:
        return result

    # Raw money flow
    raw_mf = typical_price * volume

    for i in range(period, n):
        pos_mf = 0.0
        neg_mf = 0.0

        for j in range(i - period + 1, i + 1):
            if typical_price[j] > typical_price[j - 1]:
                pos_mf += raw_mf[j]
            elif typical_price[j] < typical_price[j - 1]:
                neg_mf += raw_mf[j]

        if neg_mf != 0:
            mf_ratio = pos_mf / neg_mf
            result[i] = 100.0 - (100.0 / (1.0 + mf_ratio))
        else:
            result[i] = 100.0

    return result


__all__ = [
    "ema_loop",
    "rolling_std",
    "wilder_smooth",
    "rolling_minmax",
    "true_range_loop",
    "obv_loop",
    "ad_loop",
    "kama_loop",
    "adx_loop",
    "mfi_loop",
]
