"""
Shared test fixtures for cluefin-ta tests.
"""

import numpy as np
import pytest


@pytest.fixture
def sample_close():
    """Sample closing prices for testing."""
    np.random.seed(42)
    # Generate realistic stock price data
    base_price = 100.0
    returns = np.random.randn(100) * 0.02  # 2% daily volatility
    prices = base_price * np.cumprod(1 + returns)
    return prices.astype(np.float64)


@pytest.fixture
def sample_ohlcv():
    """Sample OHLCV data for testing."""
    np.random.seed(42)
    n = 100
    base_price = 100.0

    # Generate close prices
    returns = np.random.randn(n) * 0.02
    close = base_price * np.cumprod(1 + returns)

    # Generate OHLC based on close
    high = close * (1 + np.abs(np.random.randn(n) * 0.01))
    low = close * (1 - np.abs(np.random.randn(n) * 0.01))
    open_prices = low + (high - low) * np.random.rand(n)

    # Ensure high >= close >= low and high >= open >= low
    high = np.maximum(high, np.maximum(close, open_prices))
    low = np.minimum(low, np.minimum(close, open_prices))

    # Generate volume
    volume = np.random.randint(1000000, 10000000, n).astype(np.float64)

    return {
        "open": open_prices.astype(np.float64),
        "high": high.astype(np.float64),
        "low": low.astype(np.float64),
        "close": close.astype(np.float64),
        "volume": volume,
    }


@pytest.fixture
def short_data():
    """Short data array for edge case testing."""
    return np.array([100.0, 101.0, 99.0, 102.0, 98.0], dtype=np.float64)


@pytest.fixture
def constant_data():
    """Constant price data for edge case testing."""
    return np.full(50, 100.0, dtype=np.float64)
