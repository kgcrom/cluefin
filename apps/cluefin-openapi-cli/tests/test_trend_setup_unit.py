"""trend_setup features, pivot and strength match the watchlist backtest (factory `a5cfbcf`)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from cluefin_openapi_cli.trend_setup import (
    MIN_CANDLES,
    IndexCloses,
    IndexDateMismatch,
    PriceArrays,
    find_pivot,
    fractal_highs,
    price_features,
    return_pct,
    strength,
    true_range,
    weighted_return,
)

FIXTURES = Path(__file__).parent / "fixtures" / "trend_setup"
# 10-06 closes: 300 real daily bars each, with the values the backtest's Python code computed.
# `expected` keys are the backtest's names; the files are renamed (stock-a…) on purpose.
GOLDEN = ["stock-a", "stock-b", "stock-c", "stock-d"]
FEATURE_NAMES = {
    "close": "close",
    "sma_50": "ma50",
    "sma_150": "ma150",
    "sma_200": "ma200",
    "high_52w": "hi52",
    "low_52w": "lo52",
    "gap_to_high_pct": "gap52h",
    "from_low_pct": "from52l",
    "return_21d_pct": "r21",
    "weighted_return": "rs_raw",
    "range_10d_pct": "range10",
    "atr14_pct": "atr14p",
    "volume_20_50": "v20_50",
    "traded_value_20d_eok": "tv20",
    "dist_sma50_pct": "dist_ma50",
    "depth_60d_pct": "depth60",
}


def load(name: str) -> dict:
    return json.loads((FIXTURES / f"{name}.json").read_text())


def prices_of(name: str) -> PriceArrays:
    return _prices(load(name)["candles"])


def _prices(candles: list[dict]) -> PriceArrays:
    keys = ("date", "open", "high", "low", "close", "volume", "value")
    return PriceArrays.from_rows([tuple(candle[key] for key in keys) for candle in candles])


def index_of(market: str) -> IndexCloses:
    data = load("index-0001" if market == "KOSPI" else "index-1001")
    return IndexCloses.from_pairs((row["date"], row["close"]) for row in data["closes"])


def _from_highs(highs: list[float]) -> PriceArrays:
    """Bars with the given highs; lows sit 10 below, closes 5 below."""

    return PriceArrays.from_rows(
        [(str(20260101 + i), high - 5, high, high - 10, high - 5, 1000, 1e9) for i, high in enumerate(highs)]
    )


@pytest.mark.parametrize("name", GOLDEN)
def test_features_match_backtest(name: str) -> None:
    expected = load(name)["expected"]

    got = price_features(prices_of(name))

    assert got is not None
    for ours, theirs in FEATURE_NAMES.items():
        assert getattr(got, ours) == pytest.approx(expected[theirs], abs=1e-6), ours
    assert got.template is expected["tt"]
    assert got.date == "20261006"


def test_52w_high_excludes_the_day_and_uses_intraday_highs() -> None:
    candles = load("stock-d")["candles"]
    got = price_features(_prices(candles))
    assert got is not None
    assert got.high_52w == max(candle["high"] for candle in candles[-251:-1])

    # A higher high on the day itself does not move the reference, so the gap can be positive.
    lifted = [*candles[:-1], {**candles[-1], "high": 1e9, "close": got.high_52w * 1.05}]
    lifted_features = price_features(_prices(lifted))
    assert lifted_features is not None
    assert lifted_features.gap_to_high_pct == pytest.approx(5, abs=1e-6)


def test_features_need_min_candles() -> None:
    candles = load("stock-a")["candles"]

    assert price_features(_prices(candles[-(MIN_CANDLES - 1) :])) is None
    assert price_features(_prices(candles[-MIN_CANDLES:])) is not None


def test_weighted_return_counts_the_last_quarter_twice() -> None:
    closes = np.full(251, 100.0)
    assert weighted_return(closes) == 5
    closes[250] = 200
    assert weighted_return(closes) == 10
    assert weighted_return(closes[1:]) is None


def test_return_pct_is_none_when_short() -> None:
    assert return_pct(np.array([100.0, 110.0]), 1) == pytest.approx(10)
    assert return_pct(np.array([100.0, 110.0]), 2) is None


def test_true_range_includes_the_gap_from_the_previous_close() -> None:
    high, low, close = np.array([100.0, 120.0]), np.array([90.0, 110.0]), np.array([95.0, 115.0])

    assert true_range(high, low, close, 0) == 10
    assert true_range(high, low, close, 1) == 25


@pytest.mark.parametrize("name", GOLDEN)
def test_pivot_matches_backtest(name: str) -> None:
    expected = load(name)["expected"]

    got = find_pivot(prices_of(name))

    assert got is not None
    assert got.price == expected["pivot"]
    assert got.last_contraction_pct == pytest.approx(expected["last_contr"], abs=1e-6)
    assert got.contractions == expected["n_legs"]


def test_pivot_reference_values() -> None:
    a, b, c = (find_pivot(prices_of(name)) for name in ("stock-a", "stock-b", "stock-c"))

    assert a is not None
    assert a.price == 179700
    assert b is not None
    assert f"{b.last_contraction_pct:.1f}" == "9.9"
    assert c is not None
    assert c.price == 6040


def test_fractal_high_needs_three_lower_bars_on_each_side() -> None:
    assert fractal_highs(np.array([10, 11, 12, 20, 19, 18, 17], dtype=float)) == [3]


def test_fractal_left_equal_disqualifies_right_equal_does_not() -> None:
    assert fractal_highs(np.array([20, 11, 12, 20, 19, 18, 17], dtype=float)) == []
    assert fractal_highs(np.array([10, 11, 12, 20, 20, 18, 17, 16], dtype=float)) == [3]


def test_highs_in_the_last_three_bars_are_not_confirmed() -> None:
    assert fractal_highs(np.array([10, 11, 12, 13, 14, 30, 20, 19], dtype=float)) == []


def test_contraction_legs_from_the_base_high_excluding_the_pivot_bar_low() -> None:
    highs = [
        *([50] * 10),
        *(100, 90, 80, 70, 80),  # base high 100 → low 60 (40%)
        *(95, 85, 80, 82, 84),  # swing high 95 → low 70
        *(90, 86, 84, 85, 87, 88),  # swing high 90 → low 74
    ]

    got = find_pivot(_from_highs(highs))

    assert got is not None
    assert got.price == 90
    assert got.contractions == 3
    assert got.age == 5
    assert got.legs[0] == pytest.approx(40)
    assert got.legs[1] == pytest.approx((1 - 70 / 95) * 100)
    assert got.last_contraction_pct == pytest.approx((1 - 74 / 90) * 100)


def test_no_confirmed_high_means_no_pivot() -> None:
    assert find_pivot(_from_highs([1, 2, 3, 4, 5, 6, 7, 8])) is None


@pytest.mark.parametrize("name", GOLDEN)
def test_strength_matches_backtest(name: str) -> None:
    data = load(name)

    got = strength(prices_of(name), index_of(data["market"]))

    assert got is not None
    assert got.rel == pytest.approx(data["expected"]["rel"], abs=1e-6)
    assert got.excess_21d_pp == pytest.approx(data["expected"]["ex21"], abs=1e-6)


def test_strength_reference_values() -> None:
    weak = strength(prices_of("stock-a"), index_of("KOSPI"))
    strong = strength(prices_of("stock-d"), index_of("KOSDAQ"))

    assert weak is not None
    assert f"{weak.rel:.2f}" == "0.81"
    assert strong is not None
    assert f"{strong.rel:.2f}" == "2.95"


def test_strength_reads_the_index_on_the_stock_date_and_ignores_later_days() -> None:
    index = index_of("KOSPI")
    later = IndexCloses(dates=(*index.dates, "20261007"), closes=np.append(index.closes, 1.0))

    assert strength(prices_of("stock-a"), later) == strength(prices_of("stock-a"), index)


def test_strength_fails_when_the_index_lacks_the_date() -> None:
    index = index_of("KOSPI")

    with pytest.raises(IndexDateMismatch, match="20261006"):
        strength(prices_of("stock-a"), IndexCloses(dates=index.dates[:-1], closes=index.closes[:-1]))


def test_strength_is_none_when_either_side_is_short() -> None:
    prices, index = prices_of("stock-a"), index_of("KOSPI")
    short_index = IndexCloses(dates=index.dates[-250:], closes=index.closes[-250:])

    assert strength(prices.window(start=-250), index) is None
    assert strength(prices, short_index) is None
