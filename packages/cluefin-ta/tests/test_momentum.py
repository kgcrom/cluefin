"""
Tests for momentum indicators (RSI, MACD, STOCH, STOCHF, WILLR, MOM, ROC, CCI, MFI, ADX).
"""

import numpy as np
import pytest
import talib

from cluefin_ta import ADX, CCI, MACD, MFI, MOM, ROC, RSI, STOCH, STOCHF, WILLR


class TestRSI:
    """Tests for Relative Strength Index."""

    def test_rsi_matches_talib(self, sample_close):
        """Verify RSI matches ta-lib output."""
        timeperiod = 14
        expected = talib.RSI(sample_close, timeperiod=timeperiod)
        actual = RSI(sample_close, timeperiod=timeperiod)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_rsi_range(self, sample_close):
        """Verify RSI values are in range [0, 100]."""
        result = RSI(sample_close, timeperiod=14)
        valid = result[~np.isnan(result)]
        assert np.all(valid >= 0)
        assert np.all(valid <= 100)

    def test_rsi_short_array(self, short_data):
        """Test RSI with array shorter than timeperiod."""
        result = RSI(short_data, timeperiod=14)
        assert np.all(np.isnan(result))

    def test_rsi_empty_array(self):
        """Empty input: ta-lib returns an empty array, lock down the same behavior."""
        empty = np.array([], dtype=np.float64)
        expected = talib.RSI(empty, timeperiod=14)
        actual = RSI(empty, timeperiod=14)
        assert len(actual) == len(expected) == 0

    def test_rsi_constant_prices(self, constant_data):
        """Test RSI with constant prices (no change) matches ta-lib exactly (0, not 100)."""
        timeperiod = 14
        expected = talib.RSI(constant_data, timeperiod=timeperiod)
        actual = RSI(constant_data, timeperiod=timeperiod)

        np.testing.assert_array_equal(np.isnan(actual), np.isnan(expected))
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_rsi_flat_then_rising(self):
        """Flat prices followed by a rise exercise the Wilder-smoothed zero branch."""
        close = np.r_[np.full(20, 10.0), np.arange(10.0, 20.0)]
        expected = talib.RSI(close, timeperiod=14)
        actual = RSI(close, timeperiod=14)
        np.testing.assert_allclose(actual, expected, rtol=1e-10, equal_nan=True)


class TestMACD:
    """Tests for Moving Average Convergence/Divergence."""

    @pytest.mark.parametrize(
        ("fast", "slow", "signal"),
        [(12, 26, 9), (5, 35, 5), (3, 10, 16), (26, 12, 9)],
        ids=["default", "wide", "long-signal", "swapped"],
    )
    def test_macd_matches_talib(self, sample_close, fast, slow, signal):
        """Values and NaN prefix match ta-lib, which seeds the fast EMA at the slow EMA's first bar."""
        expected = talib.MACD(sample_close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
        actual = MACD(sample_close, fastperiod=fast, slowperiod=slow, signalperiod=signal)

        for name, ours, theirs in zip(("macd", "signal", "hist"), actual, expected, strict=True):
            np.testing.assert_array_equal(np.isnan(ours), np.isnan(theirs), err_msg=name)
            mask = ~np.isnan(theirs)
            np.testing.assert_allclose(ours[mask], theirs[mask], rtol=1e-10, err_msg=name)

    def test_macd_at_exact_lookback_length(self, sample_close):
        """One bar more than the lookback gives exactly one value; one less gives none."""
        for n in (33, 34):
            expected = talib.MACD(sample_close[:n])
            actual = MACD(sample_close[:n])

            for ours, theirs in zip(actual, expected, strict=True):
                np.testing.assert_array_equal(np.isnan(ours), np.isnan(theirs))

    def test_macd_histogram_calculation(self, sample_close):
        """Verify histogram = MACD - Signal."""
        macd, signal, hist = MACD(sample_close)
        mask = ~np.isnan(signal)
        expected_hist = macd[mask] - signal[mask]
        np.testing.assert_allclose(hist[mask], expected_hist, rtol=1e-10)

    def test_macd_short_array(self, short_data):
        """Test MACD with short array."""
        macd, signal, hist = MACD(short_data)
        # All should be NaN for short array
        assert np.all(np.isnan(macd))
        assert np.all(np.isnan(signal))
        assert np.all(np.isnan(hist))


class TestSTOCH:
    """Tests for Stochastic Oscillator."""

    def test_stoch_matches_talib(self, sample_ohlcv):
        """Verify STOCH matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected_k, expected_d = talib.STOCH(high, low, close)
        actual_k, actual_d = STOCH(high, low, close)

        # Compare non-NaN values
        k_mask = ~np.isnan(expected_k)
        d_mask = ~np.isnan(expected_d)

        np.testing.assert_array_equal(np.isnan(actual_k), np.isnan(expected_k))
        np.testing.assert_array_equal(np.isnan(actual_d), np.isnan(expected_d))
        np.testing.assert_allclose(actual_k[k_mask], expected_k[k_mask], rtol=1e-10)
        np.testing.assert_allclose(actual_d[d_mask], expected_d[d_mask], rtol=1e-10)

    def test_stoch_range(self, sample_ohlcv):
        """Verify STOCH values are in range [0, 100]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        slowk, slowd = STOCH(high, low, close)

        valid_k = slowk[~np.isnan(slowk)]
        valid_d = slowd[~np.isnan(slowd)]

        assert np.all(valid_k >= 0) and np.all(valid_k <= 100)
        assert np.all(valid_d >= 0) and np.all(valid_d <= 100)


class TestWILLR:
    """Tests for Williams %R."""

    def test_willr_matches_talib(self, sample_ohlcv):
        """Verify WILLR matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.WILLR(high, low, close, timeperiod=14)
        actual = WILLR(high, low, close, timeperiod=14)

        # Compare non-NaN values
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_willr_range(self, sample_ohlcv):
        """Verify WILLR values are in range [-100, 0]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = WILLR(high, low, close, timeperiod=14)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= -100)
        assert np.all(valid <= 0)


class TestSTOCHF:
    """Tests for Fast Stochastic Oscillator."""

    def test_stochf_matches_talib(self, sample_ohlcv):
        """Verify STOCHF matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected_k, expected_d = talib.STOCHF(high, low, close)
        actual_k, actual_d = STOCHF(high, low, close)

        k_mask = ~np.isnan(expected_k)
        d_mask = ~np.isnan(expected_d)

        np.testing.assert_array_equal(np.isnan(actual_k), np.isnan(expected_k))
        np.testing.assert_array_equal(np.isnan(actual_d), np.isnan(expected_d))
        np.testing.assert_allclose(actual_k[k_mask], expected_k[k_mask], rtol=1e-10)
        np.testing.assert_allclose(actual_d[d_mask], expected_d[d_mask], rtol=1e-10)

    def test_stochf_range(self, sample_ohlcv):
        """Verify STOCHF values are in range [0, 100]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        fastk, fastd = STOCHF(high, low, close)

        valid_k = fastk[~np.isnan(fastk)]
        valid_d = fastd[~np.isnan(fastd)]

        assert np.all(valid_k >= 0) and np.all(valid_k <= 100)
        assert np.all(valid_d >= 0) and np.all(valid_d <= 100)


class TestMOM:
    """Tests for Momentum."""

    def test_mom_matches_talib(self, sample_close):
        """Verify MOM matches ta-lib output."""
        timeperiod = 10
        expected = talib.MOM(sample_close, timeperiod=timeperiod)
        actual = MOM(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_mom_short_array(self, short_data):
        """Test MOM with short array."""
        result = MOM(short_data, timeperiod=10)
        assert np.all(np.isnan(result))


class TestROC:
    """Tests for Rate of Change."""

    def test_roc_matches_talib(self, sample_close):
        """Verify ROC matches ta-lib output."""
        timeperiod = 10
        expected = talib.ROC(sample_close, timeperiod=timeperiod)
        actual = ROC(sample_close, timeperiod=timeperiod)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_roc_short_array(self, short_data):
        """Test ROC with short array."""
        result = ROC(short_data, timeperiod=10)
        assert np.all(np.isnan(result))


class TestCCI:
    """Tests for Commodity Channel Index."""

    def test_cci_matches_talib(self, sample_ohlcv):
        """Verify CCI matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.CCI(high, low, close, timeperiod=14)
        actual = CCI(high, low, close, timeperiod=14)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_cci_short_array(self, short_data):
        """Test CCI with short array."""
        result = CCI(short_data, short_data, short_data, timeperiod=14)
        assert np.all(np.isnan(result))


class TestMFI:
    """Tests for Money Flow Index."""

    def test_mfi_matches_talib(self, sample_ohlcv):
        """Verify MFI matches ta-lib output."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        expected = talib.MFI(high, low, close, volume, timeperiod=14)
        actual = MFI(high, low, close, volume, timeperiod=14)

        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_mfi_range(self, sample_ohlcv):
        """Verify MFI values are in range [0, 100]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]
        volume = sample_ohlcv["volume"]

        result = MFI(high, low, close, volume, timeperiod=14)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= 0)
        assert np.all(valid <= 100)


class TestADX:
    """Tests for Average Directional Index."""

    def test_adx_matches_talib(self, sample_ohlcv):
        """Verify ADX matches ta-lib output within acceptable tolerance."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        expected = talib.ADX(high, low, close, timeperiod=14)
        actual = ADX(high, low, close, timeperiod=14)

        np.testing.assert_array_equal(np.isnan(actual), np.isnan(expected))
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    @pytest.mark.parametrize("timeperiod", [5, 14, 30])
    def test_adx_matches_talib_on_tick_rounded_prices(self, timeperiod):
        """KRX-like prices on a 50-won grid produce equal highs/lows (zero DM) often."""
        rng = np.random.default_rng(timeperiod)
        close = np.round(50000 * np.exp(np.cumsum(rng.normal(0, 0.02, 600))) / 50) * 50
        high = close + np.round(np.abs(rng.normal(0, 300, 600)) / 50) * 50
        low = close - np.round(np.abs(rng.normal(0, 300, 600)) / 50) * 50

        expected = talib.ADX(high, low, close, timeperiod=timeperiod)
        actual = ADX(high, low, close, timeperiod=timeperiod)

        np.testing.assert_array_equal(np.isnan(actual), np.isnan(expected))
        mask = ~np.isnan(expected)
        np.testing.assert_allclose(actual[mask], expected[mask], rtol=1e-10)

    def test_adx_range(self, sample_ohlcv):
        """Verify ADX values are in range [0, 100]."""
        high = sample_ohlcv["high"]
        low = sample_ohlcv["low"]
        close = sample_ohlcv["close"]

        result = ADX(high, low, close, timeperiod=14)
        valid = result[~np.isnan(result)]

        assert np.all(valid >= 0)
        assert np.all(valid <= 100)

    def test_adx_short_array(self, short_data):
        """Test ADX with short array."""
        result = ADX(short_data, short_data, short_data, timeperiod=14)
        assert np.all(np.isnan(result))
