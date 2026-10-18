"""`ohlcv` load: window walking, incremental append, correction replace, delisted skip, indices."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.bars import INDICES, load_bars
from cluefin_openapi_cli.cache.cli import _last_closed_day

SINCE = date(2016, 1, 1)


def _weekdays(start: date, end: date) -> list[date]:
    days, day = [], start
    while day <= end:
        if day.weekday() < 5:
            days.append(day)
        day += timedelta(days=1)
    return days


class FakeKis:
    """Serves synthetic daily series like KIS: newest first, capped rows per call."""

    def __init__(self, series: dict[str, dict[date, float]], *, fail: frozenset[str] = frozenset()):
        self.series = series
        self.fail = fail
        self.stock_calls: list[tuple[str, str, str, str]] = []
        self.index_calls: list[str] = []
        self.domestic_basic_quote = SimpleNamespace(get_stock_period_quote=self._stock)
        self.domestic_issue_other = SimpleNamespace(get_sector_period_quote=self._index)

    def _rows(self, code, d1, d2, cap):
        start, end = (datetime.strptime(d, "%Y%m%d").date() for d in (d1, d2))
        days = sorted((d for d in self.series.get(code, {}) if start <= d <= end), reverse=True)
        return days[:cap]

    def _stock(self, market, code, d1, d2, period, adj):
        self.stock_calls.append((code, d1, d2, adj))
        if code in self.fail:
            raise ValueError("KIS API Error [OPSQ0001]: broken")
        rows = []
        for day in self._rows(code, d1, d2, 100):
            close = self.series[code][day]
            rows.append(
                SimpleNamespace(
                    stck_bsop_date=day.strftime("%Y%m%d"),
                    stck_oprc="0" if close == 0 else str(close),
                    stck_hgpr=str(close),
                    stck_lwpr=str(close),
                    stck_clpr=str(close),
                    acml_vol="10",
                    acml_tr_pbmn="1000",
                    flng_cls_code="02" if day.month == 12 and day.day == 28 else "00",
                    prtt_rate="0.00",
                    revl_issu_reas="",
                )
            )
        return SimpleNamespace(body=SimpleNamespace(output2=rows))

    def _index(self, market, iscd, d1, d2, period):
        self.index_calls.append(iscd)
        rows = [
            SimpleNamespace(
                stck_bsop_date=day.strftime("%Y%m%d"),
                bstp_nmix_prpr="2500.5",
                bstp_nmix_oprc="2490.1",
                bstp_nmix_hgpr="2510.0",
                bstp_nmix_lwpr="2480.0",
                acml_vol="1",
                acml_tr_pbmn="2",
            )
            for day in self._rows("IDX", d1, d2, 50)
        ]
        return SimpleNamespace(body=SimpleNamespace(output2=rows))


def _store_with(companies):
    conn = store.open_store(":memory:")
    conn.executemany("INSERT INTO company (code, listed_on, delisted_on) VALUES (?, ?, ?)", companies)
    return conn


def _closes(conn, code):
    return dict(conn.execute("SELECT date, close FROM ohlcv WHERE code = ? ORDER BY date", [code]).fetchall())


def _load(conn, kis, last_day):
    return load_bars(conn, kis=kis, since=SINCE, last_day=last_day, sleep=lambda _s: None)


@pytest.fixture
def market():
    last = date(2026, 10, 16)
    full = _weekdays(date(2015, 6, 1), last)
    # 000660 halts for ~7 months in 2020: an empty window in the middle must not end the walk.
    halted = [d for d in full if not (date(2020, 3, 1) <= d <= date(2020, 9, 30))]
    series = {
        "005930": {d: 100.0 + i for i, d in enumerate(full)},
        "000660": {d: 50.0 for d in halted},
        "117930": {d: 10.0 for d in full if d <= date(2017, 3, 6)},
        "IDX": {d: 1.0 for d in full},
    }
    return last, series


def test_initial_load_walks_whole_history_through_a_halt(market) -> None:
    last, series = market
    conn = _store_with(
        [("005930", date(1975, 6, 11), None), ("000660", date(1996, 12, 26), None), ("117930", None, date(2017, 3, 7))]
    )
    kis = FakeKis(series)

    stats = _load(conn, kis, last)

    expected = [d for d in series["005930"] if SINCE <= d <= last]
    assert list(_closes(conn, "005930")) == expected
    halted_2020 = [d for d in _closes(conn, "000660") if d.year == 2020]
    assert min(_closes(conn, "000660")) == date(2016, 1, 1)  # a Friday in this synthetic calendar
    assert halted_2020[0] < date(2020, 3, 1) and halted_2020[-1] > date(2020, 9, 30)
    assert list(_closes(conn, "117930"))[-1] == date(2017, 3, 6)
    assert all(adj == "1" for *_, adj in kis.stock_calls)  # chart.period "1" = unadjusted
    assert stats.errors == [] and stats.replaced == 0
    for cache_code, _ in INDICES:
        assert len(_closes(conn, cache_code)) == len(expected)
    calls_005930 = sum(1 for call in kis.stock_calls if call[0] == "005930")
    assert calls_005930 <= len(expected) // 95 + 3


def test_daily_run_appends_with_one_call_per_code(market) -> None:
    last, series = market
    conn = _store_with([("005930", date(1975, 6, 11), None)])
    kis = FakeKis(series)
    _load(conn, kis, last)
    for day in _weekdays(last + timedelta(days=1), last + timedelta(days=4)):
        series["005930"][day] = 9999.0
        series["IDX"][day] = 1.0
    kis.stock_calls.clear()

    stats = _load(conn, kis, last + timedelta(days=4))

    assert [call[0] for call in kis.stock_calls] == ["005930"]
    assert stats.rows == 2 + 3 * 2  # two new weekdays for the stock, two for each index
    assert _closes(conn, "005930")[date(2026, 10, 20)] == 9999.0


def test_corrected_recent_close_replaces_whole_history(market) -> None:
    last, series = market
    conn = _store_with([("005930", date(1975, 6, 11), None)])
    kis = FakeKis(series)
    _load(conn, kis, last)
    series["005930"][date(2026, 10, 1)] = 1.0
    series["005930"][date(2016, 1, 4)] = 2.0

    stats = _load(conn, kis, last)

    assert stats.replaced == 1
    assert _closes(conn, "005930")[date(2016, 1, 4)] == 2.0


def test_delisted_code_is_skipped_once_complete(market) -> None:
    last, series = market
    conn = _store_with([("117930", None, date(2017, 3, 7))])
    kis = FakeKis(series)
    _load(conn, kis, last)
    kis.stock_calls.clear()

    stats = _load(conn, kis, last)

    assert kis.stock_calls == [] and stats.skipped == 1


def test_zero_price_is_null_and_markers_are_kept(market) -> None:
    last, series = market
    series["005930"][date(2026, 10, 15)] = 0.0
    conn = _store_with([("005930", date(1975, 6, 11), None)])
    _load(conn, FakeKis(series), last)

    zero = conn.execute("SELECT open, close FROM ohlcv WHERE code = '005930' AND date = DATE '2026-10-15'").fetchone()
    marker = conn.execute("SELECT lock_code FROM ohlcv WHERE code = '005930' AND date = DATE '2025-12-29'").fetchone()
    lock = conn.execute("SELECT count(*) FROM ohlcv WHERE code = '005930' AND lock_code = '02'").fetchone()

    assert zero == (None, None)
    assert marker == ("00",)
    assert lock[0] > 0


def test_one_failing_code_does_not_stop_the_load(market) -> None:
    last, series = market
    conn = _store_with([("000660", date(1996, 12, 26), None), ("005930", date(1975, 6, 11), None)])

    stats = _load(conn, FakeKis(series, fail=frozenset({"000660"})), last)

    assert [error["code"] for error in stats.errors] == ["000660"]
    assert _closes(conn, "005930") and not _closes(conn, "000660")


def test_new_listing_starts_at_listing_date(market) -> None:
    last, series = market
    conn = _store_with([("005930", date(2026, 9, 1), None)])

    _load(conn, FakeKis(series), last)

    assert min(_closes(conn, "005930")) == date(2026, 9, 1)


@pytest.mark.parametrize(
    ("now", "expected"),
    [(datetime(2026, 10, 19, 15, 59), date(2026, 10, 18)), (datetime(2026, 10, 19, 16, 0), date(2026, 10, 19))],
)
def test_last_closed_day_waits_for_the_session_to_end(now, expected) -> None:
    assert _last_closed_day(now) == expected
