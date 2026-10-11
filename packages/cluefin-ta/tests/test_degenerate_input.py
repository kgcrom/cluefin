"""
Tests for zero-denominator and short-input guards.

Flat bars (high == low == close) are what a trading halt looks like, and a series that
only rises is common for short windows. These must produce defined values, not NaN or
division warnings. Does not import talib, so it runs without the TA-Lib C library.
"""

import warnings

import numpy as np
import pytest

from cluefin_ta import AD, ADX, KAMA, MFI, OBV
from cluefin_ta._core import adx_loop, kama_loop, mfi_loop, rolling_std, true_range_loop

N = 40
FLAT = np.full(N, 100.0)
VOLUME = np.arange(1, N + 1, dtype=np.float64) * 10


@pytest.fixture(autouse=True)
def _division_warnings_are_errors():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        yield


class TestFlatBars:
    """Every bar has high == low == close (거래정지)."""

    def test_obv_carries_forward_on_unchanged_close(self):
        result = OBV(FLAT, VOLUME)

        np.testing.assert_array_equal(result, np.full(N, VOLUME[0]))

    def test_ad_adds_nothing_for_zero_range_bar(self):
        result = AD(FLAT, FLAT, FLAT, VOLUME)

        np.testing.assert_array_equal(result, np.zeros(N))

    def test_kama_holds_price_when_volatility_is_zero(self):
        result = KAMA(FLAT, timeperiod=10)

        assert np.isnan(result[:10]).all()
        np.testing.assert_array_equal(result[10:], np.full(N - 10, 100.0))

    def test_adx_is_zero_when_true_range_is_zero(self):
        timeperiod = 14

        result = ADX(FLAT, FLAT, FLAT, timeperiod=timeperiod)

        warmup = 2 * timeperiod - 1
        assert np.isnan(result[:warmup]).all()
        np.testing.assert_array_equal(result[warmup:], np.zeros(N - warmup))


def test_mfi_is_100_when_there_is_no_negative_money_flow():
    """Typical price rises every bar, so the money-flow ratio has a zero denominator."""
    close = np.linspace(100.0, 140.0, N)
    timeperiod = 14

    result = MFI(close + 1, close - 1, close, np.full(N, 1000.0), timeperiod=timeperiod)

    assert np.isnan(result[:timeperiod]).all()
    np.testing.assert_array_equal(result[timeperiod:], np.full(N - timeperiod, 100.0))


@pytest.mark.parametrize(
    "call",
    [
        pytest.param(lambda x: rolling_std(x, 5), id="rolling_std"),
        pytest.param(lambda x: kama_loop(x, 5, 2 / 3, 2 / 31), id="kama_loop"),
        pytest.param(lambda x: mfi_loop(x, np.ones_like(x), 5), id="mfi_loop"),
        pytest.param(lambda x: true_range_loop(x, x, x), id="true_range_loop"),
        pytest.param(lambda x: adx_loop(x, x, x, 5), id="adx_loop"),
    ],
)
def test_core_loop_shorter_than_window_is_all_nan(call):
    """The public wrappers check length first; the loops keep their own guard for direct callers."""
    short = np.array([100.0])

    result = call(short)

    assert len(result) == 1
    assert np.isnan(result).all()
