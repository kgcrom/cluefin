"""
Pattern Recognition (Candlestick) - ta-lib compatible implementations.

Functions:
    CDLDOJI: Doji pattern
    CDLHAMMER: Hammer pattern
    CDLENGULFING: Engulfing pattern

These follow ta-lib's C source: thresholds are not fixed ratios of the bar itself but
multiples of the average of a "candle setting" range (real body, high-low or shadows)
over the preceding bars, kept as a running total exactly as ta-lib keeps it. Bars inside
ta-lib's lookback are 0.

All pattern functions return:
    +100: Bullish pattern (CDLDOJI and CDLHAMMER only return this)
    +80 / -80: Engulfing whose open or close equals the previous bar's (ta-lib's "partial")
       0: No pattern
    -100: Bearish pattern
"""

import numpy as np

# ta-lib's default candle settings: (range type, average period, factor)
_REAL_BODY, _HIGH_LOW, _SHADOWS = 0, 1, 2
_BODY_DOJI = (_HIGH_LOW, 10, 0.1)
_BODY_SHORT = (_REAL_BODY, 10, 1.0)
_SHADOW_LONG = (_REAL_BODY, 0, 1.0)
_SHADOW_VERY_SHORT = (_HIGH_LOW, 10, 0.1)
_NEAR = (_HIGH_LOW, 5, 0.2)


def _as_float_arrays(*arrays: np.ndarray) -> list[np.ndarray]:
    return [np.asarray(a, dtype=np.float64) for a in arrays]


def _real_body(open_arr: np.ndarray, close: np.ndarray) -> np.ndarray:
    return np.abs(close - open_arr)


def _upper_shadow(open_arr: np.ndarray, high: np.ndarray, close: np.ndarray) -> np.ndarray:
    return high - np.maximum(open_arr, close)


def _lower_shadow(open_arr: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    return np.minimum(open_arr, close) - low


def _candle_range(setting: tuple, open_arr, high, low, close) -> np.ndarray:
    """ta-lib's TA_CANDLERANGE for every bar."""
    range_type = setting[0]
    if range_type == _REAL_BODY:
        return _real_body(open_arr, close)
    if range_type == _HIGH_LOW:
        return high - low
    return _upper_shadow(open_arr, high, close) + _lower_shadow(open_arr, low, close)


def _candle_average(setting: tuple, ranges: np.ndarray, first: int) -> np.ndarray:
    """ta-lib's TA_CANDLEAVERAGE at every bar from ``first`` on (NaN before).

    The value at bar ``i`` averages ``ranges`` over the ``period`` bars before ``i``. The
    sum is a running total (add the new bar, drop the trailing one) rather than a fresh
    sum, because that is how ta-lib accumulates it and its rounding decides ties.
    """
    range_type, period, factor = setting
    divisor = 2.0 if range_type == _SHADOWS else 1.0
    averages = np.full(len(ranges), np.nan)
    if period == 0:
        averages[first:] = factor * ranges[first:] / divisor
        return averages
    if first < period:
        return averages

    total = 0.0
    for i in range(first - period, first):
        total += float(ranges[i])
    for i in range(first, len(ranges)):
        averages[i] = factor * (total / period) / divisor
        total += float(ranges[i] - ranges[i - period])
    return averages


def CDLDOJI(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Doji Pattern.

    The real body is at most 10% of the average high-low range of the previous 10 bars
    (ta-lib's BodyDoji setting). The shadows can have any length.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (doji) or 0 (no pattern); the first 10 bars are 0
    """
    open_arr, high, low, close = _as_float_arrays(open_arr, high, low, close)
    result = np.zeros(len(close), dtype=np.int32)

    lookback = _BODY_DOJI[1]
    if len(close) <= lookback:
        return result

    doji_body = _candle_average(_BODY_DOJI, _candle_range(_BODY_DOJI, open_arr, high, low, close), lookback)
    body = _real_body(open_arr, close)
    hits = body[lookback:] <= doji_body[lookback:]
    result[lookback:] = np.where(hits, 100, 0)
    return result


def CDLHAMMER(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Hammer Pattern.

    ta-lib's definition, all relative to the preceding bars' averages:
    - Short real body (below the average body of the previous 10 bars)
    - Long lower shadow (longer than the bar's own real body)
    - Very short upper shadow (below 10% of the average high-low range of 10 bars)
    - Body below or near the previous bar's low (within 20% of its 5-bar average range)

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (hammer) or 0 (no pattern); the first 11 bars are 0
    """
    open_arr, high, low, close = _as_float_arrays(open_arr, high, low, close)
    n = len(close)
    result = np.zeros(n, dtype=np.int32)

    settings = (_BODY_SHORT, _SHADOW_LONG, _SHADOW_VERY_SHORT, _NEAR)
    lookback = max(setting[1] for setting in settings) + 1
    if n <= lookback:
        return result

    def average(setting: tuple, first: int) -> np.ndarray:
        return _candle_average(setting, _candle_range(setting, open_arr, high, low, close), first)

    body_short = average(_BODY_SHORT, lookback)
    shadow_long = average(_SHADOW_LONG, lookback)
    shadow_very_short = average(_SHADOW_VERY_SHORT, lookback)
    # "Near" is measured on the previous bar
    near_previous = average(_NEAR, lookback - 1)[lookback - 1 : n - 1]

    tail = slice(lookback, n)
    body_bottom = np.minimum(close, open_arr)[tail]
    hits = (
        (_real_body(open_arr, close)[tail] < body_short[tail])
        & (_lower_shadow(open_arr, low, close)[tail] > shadow_long[tail])
        & (_upper_shadow(open_arr, high, close)[tail] < shadow_very_short[tail])
        & (body_bottom <= low[lookback - 1 : n - 1] + near_previous)
    )
    result[tail] = np.where(hits, 100, 0)
    return result


def CDLENGULFING(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Engulfing Pattern.

    Bullish: a black (close < open) bar followed by a white bar whose real body covers it.
    Bearish: a white bar followed by a black bar whose real body covers it. A bar with
    close == open counts as white, as in ta-lib. One end may coincide with the previous
    body's end; that "partial" engulfing scores 80 instead of 100.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100/+80 (bullish), -100/-80 (bearish), or 0 (no pattern); the first
        2 bars are 0
    """
    open_arr, high, low, close = _as_float_arrays(open_arr, high, low, close)
    n = len(close)
    result = np.zeros(n, dtype=np.int32)

    lookback = 2
    if n <= lookback:
        return result

    color = np.where(close >= open_arr, 1, -1)
    o, c = open_arr[lookback:], close[lookback:]
    prev_o, prev_c = open_arr[lookback - 1 : n - 1], close[lookback - 1 : n - 1]
    curr_color, prev_color = color[lookback:], color[lookback - 1 : n - 1]

    white_engulfs_black = (
        (curr_color == 1) & (prev_color == -1) & (((c >= prev_o) & (o < prev_c)) | ((c > prev_o) & (o <= prev_c)))
    )
    black_engulfs_white = (
        (curr_color == -1) & (prev_color == 1) & (((o >= prev_c) & (c < prev_o)) | ((o > prev_c) & (c <= prev_o)))
    )
    strength = np.where((o != prev_c) & (c != prev_o), 100, 80)
    result[lookback:] = np.where(white_engulfs_black | black_engulfs_white, curr_color * strength, 0)
    return result


__all__ = ["CDLDOJI", "CDLHAMMER", "CDLENGULFING"]
