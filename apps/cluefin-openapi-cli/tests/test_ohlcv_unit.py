from __future__ import annotations

import math

import pytest

from cluefin_openapi_cli.ohlcv import (
    Candle,
    CandleSeries,
    adj_price_flag,
    fetch_kis_daily_series,
    from_kis_daily,
    from_kis_minute,
    from_kis_period,
    from_kiwoom_daily,
    from_kiwoom_minute,
)


def _kis_daily_row(date: str, close: str, volume: str = "1000") -> dict[str, str]:
    return {
        "stck_bsop_date": date,
        "stck_oprc": "100",
        "stck_hgpr": "110",
        "stck_lwpr": "90",
        "stck_clpr": close,
        "acml_vol": volume,
    }


# ---------------------------------------------------------------------------
# Parsing: gaps are NaN, prices are magnitudes
# ---------------------------------------------------------------------------


def test_blank_and_garbage_values_become_nan_not_zero() -> None:
    """A zero-priced candle reads as a crash to zero and poisons every indicator."""

    series = from_kis_daily(
        [
            {
                "stck_bsop_date": "20260101",
                "stck_oprc": "",
                "stck_hgpr": "-",
                "stck_lwpr": None,
                "stck_clpr": "abc",
                "acml_vol": "   ",
            }
        ],
        stock_code="005930",
    )

    candle = series.candles[0]
    assert all(math.isnan(value) for value in (candle.open, candle.high, candle.low, candle.close, candle.volume))
    assert candle.complete is False
    assert series.missing_count == 1


def test_kiwoom_signed_prices_are_read_as_magnitudes() -> None:
    """Kiwoom marks down days with a leading `-`; a negative close would break TA outright."""

    series = from_kiwoom_daily(
        [
            {
                "dt": "20260101",
                "open_pric": "-270000",
                "high_pric": "-271000",
                "low_pric": "-269000",
                "cur_prc": "-270406",
                "trde_qty": "12345",
            }
        ],
        stock_code="005930",
    )

    candle = series.candles[0]
    assert (candle.open, candle.high, candle.low, candle.close) == (270000.0, 271000.0, 269000.0, 270406.0)
    assert candle.volume == 12345.0


def test_unsigned_kiwoom_prices_are_unchanged() -> None:
    series = from_kiwoom_daily(
        [
            {
                "dt": "20260101",
                "open_pric": "500",
                "high_pric": "510",
                "low_pric": "490",
                "cur_prc": "505",
                "trde_qty": "7",
            }
        ],
        stock_code="005930",
    )

    assert series.candles[0].close == 505.0


def test_thousands_separators_are_parsed() -> None:
    series = from_kis_daily([_kis_daily_row("20260101", "1,234,500", "9,999")], stock_code="005930")

    assert series.candles[0].close == 1234500.0
    assert series.candles[0].volume == 9999.0


# ---------------------------------------------------------------------------
# Ordering and de-duplication
# ---------------------------------------------------------------------------


def test_newest_first_vendor_order_is_reversed_to_oldest_first() -> None:
    """KIS chart responses arrive newest-first; indicators need the opposite."""

    series = from_kis_period(
        [_kis_daily_row("20260103", "300"), _kis_daily_row("20260102", "200"), _kis_daily_row("20260101", "100")],
        stock_code="005930",
    )

    assert series.timestamps == ("20260101", "20260102", "20260103")
    assert [candle.close for candle in series.candles] == [100.0, 200.0, 300.0]


def test_duplicate_timestamps_collapse_to_one_candle() -> None:
    """Overlapping pagination windows repeat dates; a duplicated bar would double-count in OBV."""

    series = from_kis_period(
        [_kis_daily_row("20260101", "100"), _kis_daily_row("20260101", "150")],
        stock_code="005930",
    )

    assert len(series) == 1
    assert series.candles[0].close == 150.0


def test_rows_without_a_timestamp_are_dropped() -> None:
    series = from_kis_period([_kis_daily_row("", "100"), _kis_daily_row("20260101", "200")], stock_code="005930")

    assert series.timestamps == ("20260101",)


# ---------------------------------------------------------------------------
# Endpoint-specific field mapping
# ---------------------------------------------------------------------------


def test_kis_minute_uses_bar_close_and_bar_volume() -> None:
    """Minute bars have no `stck_clpr`, and `acml_vol` is the running day total on output1."""

    series = from_kis_minute(
        [
            {
                "stck_bsop_date": "20260101",
                "stck_cntg_hour": "090100",
                "stck_oprc": "100",
                "stck_hgpr": "110",
                "stck_lwpr": "90",
                "stck_prpr": "105",
                "cntg_vol": "42",
            }
        ],
        stock_code="005930",
    )

    candle = series.candles[0]
    assert candle.timestamp == "20260101090100"
    assert candle.close == 105.0
    assert candle.volume == 42.0


def test_kiwoom_minute_timestamp_comes_from_one_packed_field() -> None:
    series = from_kiwoom_minute(
        [
            {
                "cntr_tm": "202601010901",
                "open_pric": "100",
                "high_pric": "110",
                "low_pric": "90",
                "cur_prc": "105",
                "trde_qty": "42",
            }
        ],
        stock_code="005930",
    )

    assert series.candles[0].timestamp == "202601010901"


def test_normalizers_accept_pydantic_style_objects() -> None:
    """Handlers pass vendor response models straight through, not dicts."""

    class Row:
        stck_bsop_date = "20260101"
        stck_oprc = "100"
        stck_hgpr = "110"
        stck_lwpr = "90"
        stck_clpr = "105"
        acml_vol = "42"

    series = from_kis_daily([Row()], stock_code="005930")

    assert series.candles[0].close == 105.0


# ---------------------------------------------------------------------------
# adj_price polarity
# ---------------------------------------------------------------------------


def test_adj_price_polarity_is_inverted_between_the_two_kis_endpoints() -> None:
    """chart.daily reads 1 as adjusted; chart.period reads 0 as adjusted."""

    assert adj_price_flag("chart.daily", adjusted=True) == "1"
    assert adj_price_flag("chart.daily", adjusted=False) == "0"
    assert adj_price_flag("chart.period", adjusted=True) == "0"
    assert adj_price_flag("chart.period", adjusted=False) == "1"


def test_unknown_endpoint_is_rejected_rather_than_guessed() -> None:
    with pytest.raises(ValueError, match="Unknown chart endpoint"):
        adj_price_flag("chart.nonexistent")


# ---------------------------------------------------------------------------
# arrays() / tail()
# ---------------------------------------------------------------------------


def test_arrays_are_float64_and_aligned_with_candle_order() -> None:
    series = from_kis_period(
        [_kis_daily_row("20260102", "200", "20"), _kis_daily_row("20260101", "100", "10")],
        stock_code="005930",
    )

    arrays = series.arrays()
    assert set(arrays) == {"open", "high", "low", "close", "volume"}
    assert arrays["close"].dtype.name == "float64"
    assert list(arrays["close"]) == [100.0, 200.0]
    assert list(arrays["volume"]) == [10.0, 20.0]


def test_tail_keeps_the_most_recent_candles() -> None:
    series = from_kis_period(
        [_kis_daily_row(f"2026010{index}", str(index * 100)) for index in range(1, 6)],
        stock_code="005930",
    )

    assert series.tail(2).timestamps == ("20260104", "20260105")
    assert series.tail(0) is series
    assert series.tail(99) is series


# ---------------------------------------------------------------------------
# KIS date-window pagination
# ---------------------------------------------------------------------------


class _FakeQuote:
    def __init__(self, pages: list[list[dict[str, str]]]) -> None:
        self._pages = pages
        self.calls: list[tuple] = []

    def get_stock_period_quote(self, market, code, start, end, period, adj):  # noqa: PLR0913
        self.calls.append((market, code, start, end, period, adj))
        rows = self._pages.pop(0) if self._pages else []
        return type("Response", (), {"body": type("Body", (), {"output2": rows})()})()


class _FakeKis:
    def __init__(self, pages: list[list[dict[str, str]]]) -> None:
        self.domestic_basic_quote = _FakeQuote(pages)


def test_pagination_walks_backwards_until_count_is_satisfied() -> None:
    """chart.period has no cursor, so more history means moving the date window back."""

    kis = _FakeKis(
        [
            [_kis_daily_row("20260110", "110"), _kis_daily_row("20260109", "109")],
            [_kis_daily_row("20260108", "108"), _kis_daily_row("20260107", "107")],
        ]
    )

    series = fetch_kis_daily_series(kis, "005930", count=4, end_date="20260110")

    assert len(kis.domestic_basic_quote.calls) == 2
    assert series.timestamps == ("20260107", "20260108", "20260109", "20260110")


def test_pagination_stops_on_the_first_empty_window() -> None:
    kis = _FakeKis([[_kis_daily_row("20260110", "110")], []])

    series = fetch_kis_daily_series(kis, "005930", count=50, end_date="20260110")

    assert len(kis.domestic_basic_quote.calls) == 2
    assert len(series) == 1


def test_pagination_is_bounded_when_windows_keep_returning_rows() -> None:
    """A thinly traded or delisted code must not loop back to the epoch."""

    kis = _FakeKis([[_kis_daily_row(f"2026010{index}", "100")] for index in range(9, 0, -1)] * 3)

    fetch_kis_daily_series(kis, "005930", count=10_000, end_date="20260110")

    assert len(kis.domestic_basic_quote.calls) == 12


def test_next_window_starts_before_the_oldest_row_actually_returned() -> None:
    """Stepping by a fixed stride instead would skip rows whenever a window hit the row cap."""

    kis = _FakeKis([[_kis_daily_row("20260110", "110"), _kis_daily_row("20260105", "105")], []])

    fetch_kis_daily_series(kis, "005930", count=50, end_date="20260110")

    second_call_end = kis.domestic_basic_quote.calls[1][3]
    assert second_call_end == "20260104"


def test_pagination_requests_the_adjusted_price_literal_for_this_endpoint() -> None:
    kis = _FakeKis([[_kis_daily_row("20260110", "110")]])

    fetch_kis_daily_series(kis, "005930", count=1, end_date="20260110", adjusted=True)

    assert kis.domestic_basic_quote.calls[0][5] == "0"


def test_pagination_trims_to_the_requested_count() -> None:
    kis = _FakeKis([[_kis_daily_row(f"2026011{index}", "100") for index in range(0, 5)]])

    series = fetch_kis_daily_series(kis, "005930", count=2, end_date="20260120")

    assert series.timestamps == ("20260113", "20260114")


def test_non_positive_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="count must be positive"):
        fetch_kis_daily_series(_FakeKis([]), "005930", count=0)


def test_empty_series_survives_arrays_and_tail() -> None:
    series = CandleSeries(stock_code="005930", source="test", candles=())

    assert len(series) == 0
    assert list(series.arrays()["close"]) == []
    assert series.tail(5) is series


def test_candle_complete_flag() -> None:
    assert Candle("20260101", 1.0, 2.0, 0.5, 1.5, 10.0).complete is True
    assert Candle("20260101", 1.0, 2.0, 0.5, math.nan, 10.0).complete is False
