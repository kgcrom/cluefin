from __future__ import annotations

import numpy as np
import pandas as pd
import plotext as plt
import pytest

from cluefin_cli.display.charts import ChartRenderer


@pytest.fixture(autouse=True)
def _reset_plotext():
    # plotext keeps global figure state between calls; reset so string-label
    # bar charts aren't misinterpreted using a previous plot's date settings.
    plt.clear_figure()
    yield
    plt.clear_figure()


@pytest.fixture
def ohlcv() -> pd.DataFrame:
    n = 60
    base = np.linspace(100, 160, n)
    return pd.DataFrame(
        {
            "open": base,
            "high": base + 2,
            "low": base - 2,
            "close": base + 1,
            "volume": np.arange(n) * 1000 + 1000,
        }
    )


@pytest.fixture
def indicators() -> pd.DataFrame:
    n = 60
    base = np.linspace(100, 160, n)
    return pd.DataFrame(
        {
            "sma_20": base,
            "sma_50": base - 1,
            "rsi": np.linspace(20, 80, n),
            "macd": np.linspace(-2, 2, n),
            "macd_signal": np.linspace(-1, 1, n),
            "macd_histogram": np.linspace(-0.5, 0.5, n),
        }
    )


def test_render_stock_chart_empty_data_returns_early(capsys) -> None:
    ChartRenderer().render_stock_chart(pd.DataFrame())
    # No exception; nothing meaningful rendered.


def test_render_stock_chart_with_full_indicators(ohlcv, indicators) -> None:
    ChartRenderer().render_stock_chart(ohlcv, indicators)


def test_render_stock_chart_without_indicators(ohlcv) -> None:
    ChartRenderer().render_stock_chart(ohlcv, None)


def test_render_macd_chart_without_histogram_column(ohlcv, indicators) -> None:
    # Drop the explicit histogram so the fallback (macd - signal) branch runs.
    no_hist = indicators.drop(columns=["macd_histogram"])
    ChartRenderer().render_stock_chart(ohlcv, no_hist)


def test_render_foreign_trading_chart_with_data() -> None:
    ChartRenderer().render_foreign_trading_chart({"buy": 5e9, "sell": 3e9})


def test_render_foreign_trading_chart_empty_returns_early() -> None:
    ChartRenderer().render_foreign_trading_chart({})
    ChartRenderer().render_foreign_trading_chart(None)
