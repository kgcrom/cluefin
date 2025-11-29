"""
Pattern Recognition (Candlestick) - ta-lib compatible implementations.

Functions:
    CDLDOJI: Doji pattern
    CDLHAMMER: Hammer pattern
    CDLENGULFING: Engulfing pattern

All pattern functions return:
    +100: Bullish pattern
       0: No pattern
    -100: Bearish pattern
"""

import numpy as np


def _body_size(open_price: float, close_price: float) -> float:
    """Calculate the body size of a candle."""
    return abs(close_price - open_price)


def _upper_shadow(high: float, open_price: float, close_price: float) -> float:
    """Calculate the upper shadow of a candle."""
    return high - max(open_price, close_price)


def _lower_shadow(low: float, open_price: float, close_price: float) -> float:
    """Calculate the lower shadow of a candle."""
    return min(open_price, close_price) - low


def _candle_range(high: float, low: float) -> float:
    """Calculate the full range of a candle."""
    return high - low


def CDLDOJI(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Doji Pattern.

    A doji is formed when the open and close are virtually equal.
    The shadows can vary in length.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (bullish doji), -100 (bearish doji), or 0 (no pattern)
    """
    open_arr = np.asarray(open_arr, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.zeros(n, dtype=np.int32)

    # Doji threshold: body should be less than 10% of the range
    doji_threshold = 0.1

    for i in range(n):
        candle_range = _candle_range(high[i], low[i])

        if candle_range == 0:
            continue

        body = _body_size(open_arr[i], close[i])
        body_ratio = body / candle_range

        if body_ratio <= doji_threshold:
            # Doji detected - return +100 as neutral (ta-lib convention)
            result[i] = 100

    return result


def CDLHAMMER(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Hammer Pattern.

    A hammer is a bullish reversal pattern with:
    - Small body at the upper end of the trading range
    - Long lower shadow (at least 2x the body)
    - Little or no upper shadow

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (hammer), or 0 (no pattern)
    """
    open_arr = np.asarray(open_arr, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.zeros(n, dtype=np.int32)

    for i in range(n):
        candle_range = _candle_range(high[i], low[i])

        if candle_range == 0:
            continue

        body = _body_size(open_arr[i], close[i])
        lower_shadow = _lower_shadow(low[i], open_arr[i], close[i])
        upper_shadow = _upper_shadow(high[i], open_arr[i], close[i])

        # Hammer criteria:
        # 1. Lower shadow at least 2x the body
        # 2. Upper shadow very small (less than 10% of range)
        # 3. Body in upper portion of range

        if body == 0:
            body = 0.001 * candle_range  # Prevent division by zero

        lower_shadow_ratio = lower_shadow / body if body > 0 else 0
        upper_shadow_ratio = upper_shadow / candle_range

        if lower_shadow_ratio >= 2.0 and upper_shadow_ratio <= 0.1:
            result[i] = 100

    return result


def CDLENGULFING(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Engulfing Pattern.

    Bullish Engulfing: Previous candle is bearish (red), current candle is bullish (green)
                       and current body completely engulfs previous body.

    Bearish Engulfing: Previous candle is bullish (green), current candle is bearish (red)
                       and current body completely engulfs previous body.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (bullish engulfing), -100 (bearish engulfing), or 0 (no pattern)
    """
    open_arr = np.asarray(open_arr, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.zeros(n, dtype=np.int32)

    if n < 2:
        return result

    for i in range(1, n):
        prev_open = open_arr[i - 1]
        prev_close = close[i - 1]
        curr_open = open_arr[i]
        curr_close = close[i]

        prev_is_bullish = prev_close > prev_open
        curr_is_bullish = curr_close > curr_open

        prev_body_high = max(prev_open, prev_close)
        prev_body_low = min(prev_open, prev_close)
        curr_body_high = max(curr_open, curr_close)
        curr_body_low = min(curr_open, curr_close)

        # Bullish Engulfing: prev bearish, curr bullish, curr engulfs prev
        if not prev_is_bullish and curr_is_bullish:
            if curr_body_high > prev_body_high and curr_body_low < prev_body_low:
                result[i] = 100

        # Bearish Engulfing: prev bullish, curr bearish, curr engulfs prev
        elif prev_is_bullish and not curr_is_bullish:
            if curr_body_high > prev_body_high and curr_body_low < prev_body_low:
                result[i] = -100

    return result


__all__ = ["CDLDOJI", "CDLHAMMER", "CDLENGULFING"]
