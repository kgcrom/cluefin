"""`adj_factor`: flat probe, full recompute on events, daily extension, rounding tolerance."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from types import SimpleNamespace

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.adjust import load_adjustments
from cluefin_openapi_cli.cache.bars import load_bars

SINCE = date(2016, 1, 1)


def _weekdays(start: date, end: date) -> list[date]:
    return [
        start + timedelta(days=i) for i in range((end - start).days + 1) if (start + timedelta(days=i)).weekday() < 5
    ]


class FakeKis:
    """Raw closes per code plus events (day, ratio): adjusted = round(raw × product of later ratios)."""

    def __init__(self, raw: dict[str, dict[date, float]], events: dict[str, list[tuple[date, float]]]):
        self.raw = raw
        self.events = events
        self.calls: list[tuple[str, str]] = []
        self.domestic_basic_quote = SimpleNamespace(get_stock_period_quote=self._stock)
        self.domestic_issue_other = SimpleNamespace(get_sector_period_quote=self._index)

    def adjusted(self, code: str, day: date) -> float:
        factor = 1.0
        for event_day, ratio in self.events.get(code, []):
            if day < event_day:
                factor *= ratio
        return float(round(self.raw[code][day] * factor))

    def _stock(self, market, code, d1, d2, period, adj):
        self.calls.append((code, adj))
        start, end = (datetime.strptime(d, "%Y%m%d").date() for d in (d1, d2))
        days = sorted((d for d in self.raw.get(code, {}) if start <= d <= end), reverse=True)[:100]
        rows = []
        for day in days:
            close = self.adjusted(code, day) if adj == "0" else self.raw[code][day]
            rows.append(
                SimpleNamespace(
                    stck_bsop_date=day.strftime("%Y%m%d"),
                    stck_oprc=str(close),
                    stck_hgpr=str(close),
                    stck_lwpr=str(close),
                    stck_clpr=str(close),
                    acml_vol="1",
                    acml_tr_pbmn="1",
                    flng_cls_code="00",
                    prtt_rate="0",
                    revl_issu_reas="",
                )
            )
        return SimpleNamespace(body=SimpleNamespace(output2=rows))

    def _index(self, *args):
        return SimpleNamespace(body=SimpleNamespace(output2=[]))


LAST = date(2026, 10, 16)
DAYS = _weekdays(date(2024, 1, 1), LAST)
SPLIT = date(2025, 5, 2)


def _setup(events):
    raw = {
        "FLAT00": {d: 1000.0 for d in DAYS},
        "SPLIT0": {d: (50000.0 if d < SPLIT else 1000.0) for d in DAYS},
    }
    conn = store.open_store(":memory:")
    conn.executemany(
        "INSERT INTO company (code, listed_on) VALUES (?, ?)",
        [("FLAT00", date(2024, 1, 1)), ("SPLIT0", date(2024, 1, 1))],
    )
    kis = FakeKis(raw, events)
    load_bars(conn, kis=kis, since=SINCE, last_day=LAST, sleep=lambda _s: None)
    kis.calls.clear()
    return conn, kis


def _factor(conn, code, day):
    return conn.execute("SELECT adj_factor FROM ohlcv WHERE code = ? AND date = ?", [code, day]).fetchone()[0]


def _adjusted_matches(conn, kis, code) -> bool:
    rows = conn.execute("SELECT date, close * adj_factor FROM ohlcv WHERE code = ?", [code]).fetchall()
    return all(abs(value - kis.adjusted(code, day)) < 1e-6 for day, value in rows)


def test_flat_stock_costs_one_probe_and_split_stock_is_recomputed() -> None:
    conn, kis = _setup({"SPLIT0": [(SPLIT, 1 / 50)]})

    stats = load_adjustments(conn, kis=kis, sleep=lambda _s: None)

    assert [c for c, adj in kis.calls if c == "FLAT00"] == ["FLAT00"]
    assert all(adj == "0" for _, adj in kis.calls)  # chart.period "0" = adjusted
    assert stats.probed_flat == 1 and stats.recomputed == 1
    assert _factor(conn, "SPLIT0", SPLIT - timedelta(days=1)) == 1 / 50
    assert _factor(conn, "SPLIT0", SPLIT) == 1.0
    assert _adjusted_matches(conn, kis, "SPLIT0")


def test_daily_run_extends_with_one_call_and_skips_up_to_date_codes() -> None:
    conn, kis = _setup({"SPLIT0": [(SPLIT, 1 / 50)]})
    load_adjustments(conn, kis=kis, sleep=lambda _s: None)
    assert load_adjustments(conn, kis=kis, sleep=lambda _s: None).skipped == 2

    new_days = _weekdays(LAST + timedelta(days=1), LAST + timedelta(days=4))
    for code in kis.raw:
        for day in new_days:
            kis.raw[code][day] = 1000.0
    load_bars(conn, kis=kis, since=SINCE, last_day=new_days[-1], sleep=lambda _s: None)
    kis.calls.clear()

    stats = load_adjustments(conn, kis=kis, sleep=lambda _s: None)

    assert sorted(c for c, _ in kis.calls) == ["FLAT00", "SPLIT0"]
    assert stats.extended == 2 and stats.recomputed == 0
    assert _factor(conn, "SPLIT0", new_days[-1]) == 1.0


def test_new_event_rescales_whole_history() -> None:
    conn, kis = _setup({})
    load_adjustments(conn, kis=kis, sleep=lambda _s: None)
    bonus = date(2026, 10, 20)
    for code in kis.raw:
        kis.raw[code][bonus] = 500.0
    kis.events["FLAT00"] = [(bonus, 0.5)]
    load_bars(conn, kis=kis, since=SINCE, last_day=bonus, sleep=lambda _s: None)

    stats = load_adjustments(conn, kis=kis, sleep=lambda _s: None)

    assert stats.recomputed == 1  # FLAT00 only; SPLIT0 has no events in this setup
    assert _factor(conn, "FLAT00", DAYS[0]) == 0.5
    assert _adjusted_matches(conn, kis, "FLAT00")


def test_rounded_adjusted_prices_do_not_trigger_recompute() -> None:
    conn, kis = _setup({"SPLIT0": [(SPLIT, 1 / 3)]})
    for code in kis.raw:
        kis.raw[code] = {d: (1234.0 if d < SPLIT else 411.0) for d in kis.raw[code]}
    conn.execute("DELETE FROM ohlcv")
    load_bars(conn, kis=kis, since=SINCE, last_day=LAST, sleep=lambda _s: None)
    load_adjustments(conn, kis=kis, sleep=lambda _s: None)
    day = LAST + timedelta(days=3)
    for code in kis.raw:
        kis.raw[code][day] = 411.0
    load_bars(conn, kis=kis, since=SINCE, last_day=day, sleep=lambda _s: None)

    stats = load_adjustments(conn, kis=kis, sleep=lambda _s: None)

    assert stats.recomputed == 0 and stats.extended == 2
    assert _adjusted_matches(conn, kis, "SPLIT0")


def test_bar_replace_resets_adjustment_state() -> None:
    conn, kis = _setup({"SPLIT0": [(SPLIT, 1 / 50)]})
    load_adjustments(conn, kis=kis, sleep=lambda _s: None)
    kis.raw["SPLIT0"][LAST] = 999.0  # vendor correction inside the recheck window

    load_bars(conn, kis=kis, since=SINCE, last_day=LAST, sleep=lambda _s: None)

    assert conn.execute("SELECT count(*) FROM adj_log WHERE code = 'SPLIT0'").fetchone()[0] == 0
    stats = load_adjustments(conn, kis=kis, sleep=lambda _s: None)
    assert stats.recomputed == 1 and _adjusted_matches(conn, kis, "SPLIT0")
