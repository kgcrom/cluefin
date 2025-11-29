"""
Pattern Recognition (Candlestick) - ta-lib compatible implementations.

Functions:
    CDLDOJI: Doji pattern
    CDLHAMMER: Hammer pattern
    CDLENGULFING: Engulfing pattern
    CDLSHOOTINGSTAR: Shooting Star pattern
    CDLHANGINGMAN: Hanging Man pattern
    CDLHARAMI: Harami pattern
    CDLPIERCING: Piercing Line pattern
    CDLMORNINGSTAR: Morning Star pattern (3-bar)
    CDLEVENINGSTAR: Evening Star pattern (3-bar)
    CDLDARKCLOUDCOVER: Dark Cloud Cover pattern (2-bar)

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


def _is_bullish(open_price: float, close_price: float) -> bool:
    """Check if a candle is bullish (close > open)."""
    return close_price > open_price


def _is_bearish(open_price: float, close_price: float) -> bool:
    """Check if a candle is bearish (close < open)."""
    return close_price < open_price


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


def CDLSHOOTINGSTAR(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Shooting Star Pattern.

    A shooting star is a bearish reversal pattern with:
    - Small body at the lower end of the trading range
    - Long upper shadow (at least 2x the body)
    - Little or no lower shadow
    - Typically appears after an uptrend

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with -100 (shooting star), or 0 (no pattern)
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

        # Shooting Star criteria (opposite of hammer):
        # 1. Upper shadow at least 2x the body
        # 2. Lower shadow very small (less than 10% of range)
        # 3. Body in lower portion of range

        if body == 0:
            body = 0.001 * candle_range  # Prevent division by zero

        upper_shadow_ratio = upper_shadow / body if body > 0 else 0
        lower_shadow_ratio = lower_shadow / candle_range

        if upper_shadow_ratio >= 2.0 and lower_shadow_ratio <= 0.1:
            result[i] = -100

    return result


def CDLHANGINGMAN(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Hanging Man Pattern.

    A hanging man has the same shape as a hammer but appears at the top of an uptrend.
    It's a bearish reversal pattern with:
    - Small body at the upper end of the trading range
    - Long lower shadow (at least 2x the body)
    - Little or no upper shadow

    Note: This implementation detects the candlestick shape only.
    For proper trading use, additional trend context should be considered.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with -100 (hanging man), or 0 (no pattern)
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

        # Hanging Man has same shape as hammer
        # 1. Lower shadow at least 2x the body
        # 2. Upper shadow very small (less than 10% of range)

        if body == 0:
            body = 0.001 * candle_range

        lower_shadow_ratio = lower_shadow / body if body > 0 else 0
        upper_shadow_ratio = upper_shadow / candle_range

        if lower_shadow_ratio >= 2.0 and upper_shadow_ratio <= 0.1:
            # Return -100 as it's a bearish reversal signal when at top
            result[i] = -100

    return result


def CDLHARAMI(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Harami Pattern.

    A harami is a two-candle pattern where the second candle's body is completely
    contained within the first candle's body.

    Bullish Harami: First candle bearish, second candle bullish and contained.
    Bearish Harami: First candle bullish, second candle bearish and contained.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (bullish harami), -100 (bearish harami), or 0 (no pattern)
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

        prev_is_bullish = _is_bullish(prev_open, prev_close)
        curr_is_bullish = _is_bullish(curr_open, curr_close)

        prev_body_high = max(prev_open, prev_close)
        prev_body_low = min(prev_open, prev_close)
        curr_body_high = max(curr_open, curr_close)
        curr_body_low = min(curr_open, curr_close)

        # Check if current body is contained within previous body
        is_contained = curr_body_high < prev_body_high and curr_body_low > prev_body_low

        if is_contained:
            # Bullish Harami: prev bearish, curr bullish
            if not prev_is_bullish and curr_is_bullish:
                result[i] = 100
            # Bearish Harami: prev bullish, curr bearish
            elif prev_is_bullish and not curr_is_bullish:
                result[i] = -100

    return result


def CDLPIERCING(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Piercing Line Pattern.

    A bullish reversal pattern consisting of two candles:
    1. First candle is a long bearish candle
    2. Second candle opens below the first candle's low
    3. Second candle closes above the midpoint of the first candle's body

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (piercing line), or 0 (no pattern)
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

        prev_is_bearish = _is_bearish(prev_open, prev_close)
        curr_is_bullish = _is_bullish(curr_open, curr_close)

        if not prev_is_bearish or not curr_is_bullish:
            continue

        prev_body = _body_size(prev_open, prev_close)
        prev_midpoint = prev_close + (prev_body / 2)  # For bearish: close < open

        # Piercing Line criteria:
        # 1. Previous candle is bearish
        # 2. Current candle is bullish
        # 3. Current opens below previous low
        # 4. Current closes above midpoint of previous body but below previous open
        if curr_open < low[i - 1] and curr_close > prev_midpoint and curr_close < prev_open:
            result[i] = 100

    return result


def CDLMORNINGSTAR(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Morning Star Pattern (3-bar bullish reversal).

    A three-candle pattern indicating a potential bullish reversal:
    1. First candle: Large bearish candle
    2. Second candle: Small body (star) that gaps down from first
    3. Third candle: Large bullish candle that closes above first candle's midpoint

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with +100 (morning star), or 0 (no pattern)
    """
    open_arr = np.asarray(open_arr, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.zeros(n, dtype=np.int32)

    if n < 3:
        return result

    for i in range(2, n):
        # Day 1 (first): Large bearish candle
        day1_open = open_arr[i - 2]
        day1_close = close[i - 2]
        day1_body = _body_size(day1_open, day1_close)
        day1_range = _candle_range(high[i - 2], low[i - 2])
        day1_is_bearish = _is_bearish(day1_open, day1_close)

        # Day 2 (star): Small body
        day2_open = open_arr[i - 1]
        day2_close = close[i - 1]
        day2_body = _body_size(day2_open, day2_close)
        day2_body_high = max(day2_open, day2_close)

        # Day 3 (current): Large bullish candle
        day3_open = open_arr[i]
        day3_close = close[i]
        day3_body = _body_size(day3_open, day3_close)
        day3_is_bullish = _is_bullish(day3_open, day3_close)

        if day1_range == 0:
            continue

        # Criteria:
        # 1. Day 1 is bearish with substantial body (> 50% of range)
        # 2. Day 2 has small body (< 30% of day 1 body) and gaps down
        # 3. Day 3 is bullish and closes above day 1 midpoint

        day1_midpoint = (day1_open + day1_close) / 2
        day1_body_ratio = day1_body / day1_range

        # Check day 1 is substantial bearish
        if not day1_is_bearish or day1_body_ratio < 0.5:
            continue

        # Check day 2 is small body (star) and gaps down
        if day2_body > day1_body * 0.3:
            continue

        # Gap down check: day2 body high should be below day1 close
        if day2_body_high >= day1_close:
            continue

        # Check day 3 is bullish and closes above day 1 midpoint
        if not day3_is_bullish:
            continue

        if day3_close <= day1_midpoint:
            continue

        # Day 3 should have substantial body
        if day3_body < day1_body * 0.5:
            continue

        result[i] = 100

    return result


def CDLEVENINGSTAR(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Evening Star Pattern (3-bar bearish reversal).

    A three-candle pattern indicating a potential bearish reversal:
    1. First candle: Large bullish candle
    2. Second candle: Small body (star) that gaps up from first
    3. Third candle: Large bearish candle that closes below first candle's midpoint

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with -100 (evening star), or 0 (no pattern)
    """
    open_arr = np.asarray(open_arr, dtype=np.float64)
    high = np.asarray(high, dtype=np.float64)
    low = np.asarray(low, dtype=np.float64)
    close = np.asarray(close, dtype=np.float64)
    n = len(close)

    result = np.zeros(n, dtype=np.int32)

    if n < 3:
        return result

    for i in range(2, n):
        # Day 1 (first): Large bullish candle
        day1_open = open_arr[i - 2]
        day1_close = close[i - 2]
        day1_body = _body_size(day1_open, day1_close)
        day1_range = _candle_range(high[i - 2], low[i - 2])
        day1_is_bullish = _is_bullish(day1_open, day1_close)

        # Day 2 (star): Small body
        day2_open = open_arr[i - 1]
        day2_close = close[i - 1]
        day2_body = _body_size(day2_open, day2_close)
        day2_body_low = min(day2_open, day2_close)

        # Day 3 (current): Large bearish candle
        day3_open = open_arr[i]
        day3_close = close[i]
        day3_body = _body_size(day3_open, day3_close)
        day3_is_bearish = _is_bearish(day3_open, day3_close)

        if day1_range == 0:
            continue

        # Criteria:
        # 1. Day 1 is bullish with substantial body (> 50% of range)
        # 2. Day 2 has small body (< 30% of day 1 body) and gaps up
        # 3. Day 3 is bearish and closes below day 1 midpoint

        day1_midpoint = (day1_open + day1_close) / 2
        day1_body_ratio = day1_body / day1_range

        # Check day 1 is substantial bullish
        if not day1_is_bullish or day1_body_ratio < 0.5:
            continue

        # Check day 2 is small body (star) and gaps up
        if day2_body > day1_body * 0.3:
            continue

        # Gap up check: day2 body low should be above day1 close
        if day2_body_low <= day1_close:
            continue

        # Check day 3 is bearish and closes below day 1 midpoint
        if not day3_is_bearish:
            continue

        if day3_close >= day1_midpoint:
            continue

        # Day 3 should have substantial body
        if day3_body < day1_body * 0.5:
            continue

        result[i] = -100

    return result


def CDLDARKCLOUDCOVER(
    open_arr: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> np.ndarray:
    """
    Dark Cloud Cover Pattern (2-bar bearish reversal).

    A two-candle bearish reversal pattern:
    1. First candle: Large bullish candle
    2. Second candle: Opens above first's high (gap up), closes below first's midpoint

    This is the bearish counterpart to the Piercing Line pattern.

    Args:
        open_arr: Array of opening prices
        high: Array of high prices
        low: Array of low prices
        close: Array of closing prices

    Returns:
        Array with -100 (dark cloud cover), or 0 (no pattern)
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

        prev_is_bullish = _is_bullish(prev_open, prev_close)
        curr_is_bearish = _is_bearish(curr_open, curr_close)

        if not prev_is_bullish or not curr_is_bearish:
            continue

        prev_body = _body_size(prev_open, prev_close)
        prev_midpoint = prev_open + (prev_body / 2)  # For bullish: open < close

        # Dark Cloud Cover criteria:
        # 1. Previous candle is bullish
        # 2. Current candle is bearish
        # 3. Current opens above previous high (gap up)
        # 4. Current closes below midpoint of previous body but above previous open
        if curr_open > high[i - 1] and curr_close < prev_midpoint and curr_close > prev_open:
            result[i] = -100

    return result


__all__ = [
    "CDLDOJI",
    "CDLHAMMER",
    "CDLENGULFING",
    "CDLSHOOTINGSTAR",
    "CDLHANGINGMAN",
    "CDLHARAMI",
    "CDLPIERCING",
    "CDLMORNINGSTAR",
    "CDLEVENINGSTAR",
    "CDLDARKCLOUDCOVER",
]
