"""
Every ta-lib-backed indicator against ta-lib on many long series.

The per-module tests use one 100-bar fixture, which hid NaN-prefix and algorithm
differences (STOCH's %K prefix, MACD's seeding) that only show on other data. This sweep
checks the NaN mask exactly and values to 1e-9 of the series' scale; a pure relative
tolerance is meaningless where ta-lib's value is ~0 (CCI, MFI, MACD histogram).
"""

import numpy as np
import pytest
import talib

import cluefin_ta

INDICATORS = [
    ("SMA", "c"),
    ("EMA", "c"),
    ("WMA", "c"),
    ("DEMA", "c"),
    ("TEMA", "c"),
    ("KAMA", "c"),
    ("BBANDS", "c"),
    ("RSI", "c"),
    ("MACD", "c"),
    ("MOM", "c"),
    ("ROC", "c"),
    ("STOCH", "hlc"),
    ("STOCHF", "hlc"),
    ("WILLR", "hlc"),
    ("CCI", "hlc"),
    ("ADX", "hlc"),
    ("TRANGE", "hlc"),
    ("ATR", "hlc"),
    ("NATR", "hlc"),
    ("MFI", "hlcv"),
    ("AD", "hlcv"),
    ("ADOSC", "hlcv"),
    ("OBV", "cv"),
]


def _series(seed: int, tick: float | None) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = 800
    close = 50000 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    open_arr = close * (1 + rng.normal(0, 0.01, n))
    high = np.maximum(open_arr, close) * (1 + np.abs(rng.normal(0, 0.01, n)))
    low = np.minimum(open_arr, close) * (1 - np.abs(rng.normal(0, 0.01, n)))
    if tick is not None:
        high, low, close = (np.round(a / tick) * tick for a in (high, low, close))
    volume = rng.integers(100_000, 10_000_000, n).astype(np.float64)
    return {"h": high, "l": low, "c": close, "v": volume}


@pytest.mark.parametrize("tick", [None, 50.0], ids=["continuous", "tick50"])
@pytest.mark.parametrize("seed", range(4))
@pytest.mark.parametrize(("name", "inputs"), INDICATORS, ids=[name for name, _ in INDICATORS])
def test_matches_talib(name, inputs, seed, tick):
    data = _series(seed, tick)
    args = [data[key] for key in inputs]

    ours = getattr(cluefin_ta, name)(*args)
    theirs = getattr(talib, name)(*args)
    if not isinstance(ours, tuple):
        ours, theirs = (ours,), (theirs,)

    for index, (actual, expected) in enumerate(zip(ours, theirs, strict=True)):
        np.testing.assert_array_equal(np.isnan(actual), np.isnan(expected), err_msg=f"output {index} NaN mask")
        mask = ~np.isnan(expected)
        scale = float(np.max(np.abs(expected[mask]))) if mask.any() else 1.0
        np.testing.assert_allclose(
            actual[mask], expected[mask], rtol=1e-9, atol=1e-9 * scale, err_msg=f"output {index}"
        )
