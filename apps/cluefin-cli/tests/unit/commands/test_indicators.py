"""Tests for TechnicalAnalyzer indicator calculations."""

import numpy as np
import pandas as pd

from cluefin_cli.commands.analysis.indicators import TechnicalAnalyzer


def _make_ohlcv(n: int = 60) -> pd.DataFrame:
    """Build a deterministic OHLCV fixture with an upward-trending close."""
    rng = np.random.default_rng(42)
    close = 100 + np.cumsum(rng.normal(loc=0.3, scale=1.0, size=n))
    high = close + rng.uniform(0.5, 1.5, size=n)
    low = close - rng.uniform(0.5, 1.5, size=n)
    volume = rng.integers(1_000, 10_000, size=n).astype(float)
    return pd.DataFrame({"open": close, "high": high, "low": low, "close": close, "volume": volume})


class TestCalculateAll:
    def test_adx_column_present_and_bounded(self):
        result = TechnicalAnalyzer().calculate_all(_make_ohlcv())
        assert "adx" in result
        valid = result["adx"].dropna()
        assert not valid.empty
        assert valid.between(0, 100).all()

    def test_atr_column_present_and_non_negative(self):
        result = TechnicalAnalyzer().calculate_all(_make_ohlcv())
        assert "atr" in result
        valid = result["atr"].dropna()
        assert not valid.empty
        assert (valid >= 0).all()

    def test_obv_column_present_same_length_as_input(self):
        data = _make_ohlcv()
        result = TechnicalAnalyzer().calculate_all(data)
        assert "obv" in result
        assert len(result["obv"]) == len(data)
        assert result["obv"].notna().all()

    def test_empty_input_returns_empty_dataframe(self):
        result = TechnicalAnalyzer().calculate_all(pd.DataFrame())
        assert result.empty


class TestCalculateRiskMetrics:
    def test_returns_mdd_and_sharpe_for_sufficient_data(self):
        metrics = TechnicalAnalyzer().calculate_risk_metrics(_make_ohlcv())
        assert set(metrics) == {"mdd", "sharpe"}
        assert 0 <= metrics["mdd"] <= 1
        assert isinstance(metrics["sharpe"], float)

    def test_empty_dict_when_fewer_than_two_returns(self):
        data = _make_ohlcv(n=1)
        metrics = TechnicalAnalyzer().calculate_risk_metrics(data)
        assert metrics == {}

    def test_drops_leading_nan_from_pct_change(self):
        # 3 rows -> 2 non-null returns after dropna(), which is the minimum
        # for calculate_risk_metrics to compute. Proves the leading NaN from
        # pct_change() doesn't poison the result via an uncounted extra row.
        data = _make_ohlcv(n=3)
        metrics = TechnicalAnalyzer().calculate_risk_metrics(data)
        assert metrics != {}
        assert np.isfinite(metrics["mdd"])
        assert np.isfinite(metrics["sharpe"])
