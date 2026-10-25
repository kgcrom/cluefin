"""
Tests for candlestick pattern recognition (CDLDOJI, CDLHAMMER, CDLENGULFING).

Patterns are integer outputs decided by threshold comparisons, so parity with ta-lib is
exact equality, not a tolerance. Tick-rounded prices are included because KRX prices sit
on a tick grid, which makes ta-lib's ties (<= vs <, the 80 "partial" engulfing) common.
"""

import warnings

import numpy as np
import pytest
import talib

from cluefin_ta import CDLDOJI, CDLENGULFING, CDLHAMMER

PATTERNS = [CDLDOJI, CDLHAMMER, CDLENGULFING]


def _bars(seed: int, n: int, tick: float | None) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    close = 50000 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    open_arr = close * (1 + rng.normal(0, 0.01, n))
    high = np.maximum(open_arr, close) * (1 + np.abs(rng.normal(0, 0.006, n)))
    low = np.minimum(open_arr, close) * (1 - np.abs(rng.normal(0, 0.006, n)))
    if tick is None:
        return open_arr, high, low, close
    return tuple(np.round(a / tick) * tick for a in (open_arr, high, low, close))


def _talib(pattern):
    return getattr(talib, pattern.__name__)


@pytest.mark.parametrize("pattern", PATTERNS, ids=lambda f: f.__name__)
class TestTalibParity:
    def test_matches_talib(self, pattern, sample_ohlcv):
        ohlc = (sample_ohlcv["open"], sample_ohlcv["high"], sample_ohlcv["low"], sample_ohlcv["close"])

        np.testing.assert_array_equal(pattern(*ohlc), _talib(pattern)(*ohlc))

    @pytest.mark.parametrize("tick", [None, 50.0, 500.0])
    @pytest.mark.parametrize("seed", range(5))
    def test_matches_talib_on_long_series(self, pattern, seed, tick):
        ohlc = _bars(seed, 1500, tick)

        np.testing.assert_array_equal(pattern(*ohlc), _talib(pattern)(*ohlc))

    def test_matches_talib_inside_and_around_lookback(self, pattern):
        """Lengths 0..13 cover every pattern's lookback (2, 10, 11) and the first bar after it."""
        ohlc = _bars(1, 13, 50.0)
        for n in range(len(ohlc[0]) + 1):
            prefix = tuple(a[:n] for a in ohlc)

            np.testing.assert_array_equal(pattern(*prefix), _talib(pattern)(*prefix), err_msg=f"n={n}")

    def test_flat_bars_are_no_pattern_without_division_warning(self, pattern):
        """거래정지: high == low == open == close for every bar."""
        flat = np.full(30, 100.0)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = pattern(flat, flat, flat, flat)

        np.testing.assert_array_equal(result, _talib(pattern)(flat, flat, flat, flat))


class TestCDLDOJI:
    def test_doji_is_relative_to_previous_ranges(self):
        """Body 0.5 is a doji after ten bars of range 10 (threshold 0.1 * 10 = 1)."""
        open_arr = np.full(11, 100.0)
        close = np.append(np.full(10, 104.0), 100.5)
        high = np.full(11, 105.0)
        low = np.full(11, 95.0)

        result = CDLDOJI(open_arr, high, low, close)

        assert result[:10].tolist() == [0] * 10
        assert result[10] == 100


class TestCDLENGULFING:
    # Bar 0 only fills ta-lib's 2-bar lookback
    @pytest.mark.parametrize(
        ("open_arr", "close", "expected"),
        [
            ([100, 105, 99], [101, 100, 106], 100),  # white body covers the black one
            ([100, 105, 100], [101, 100, 106], 80),  # open equals the previous close
            ([100, 100, 106], [101, 105, 99], -100),  # black body covers the white one
            ([100, 100, 105], [101, 105, 99], -80),  # open equals the previous close
            ([100, 105, 101], [101, 100, 104], 0),  # inside the previous body
        ],
    )
    def test_engulfing_scores(self, open_arr, close, expected):
        open_arr = np.array(open_arr, dtype=np.float64)
        close = np.array(close, dtype=np.float64)
        high = np.maximum(open_arr, close) + 1
        low = np.minimum(open_arr, close) - 1

        result = CDLENGULFING(open_arr, high, low, close)

        assert result.tolist() == [0, 0, expected]
        assert result.tolist() == talib.CDLENGULFING(open_arr, high, low, close).tolist()
