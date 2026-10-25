"""`cache load --only rates`: one ECOS call per series, holidays skipped, last week re-read."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

from cluefin_openapi.ecos import KTB_3Y

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.rates import RATE_SERIES, load_rates


class FakeEcos:
    def __init__(self, *, sample: bool = False) -> None:
        self.is_sample = sample
        self.calls: list[tuple[str, str, str]] = []
        self.statistic_search = self

    def search_series(self, series, start, end):
        self.calls.append((series.item_code, start, end))
        rows = [
            SimpleNamespace(time="20260105", value="3.10"),
            SimpleNamespace(time="20260106", value=None),  # not yet tallied
            SimpleNamespace(time="20260107", value="3.15"),
        ]
        return SimpleNamespace(rows=rows)


def _load(conn, ecos, last_day=date(2026, 1, 7)):
    return load_rates(conn, ecos=ecos, since=date(2016, 1, 1), last_day=last_day)


def test_loads_every_series_and_skips_empty_values() -> None:
    conn = store.open_store(":memory:")
    ecos = FakeEcos()

    stats = _load(conn, ecos)

    assert stats.calls == len(RATE_SERIES) and stats.rows == 2 * len(RATE_SERIES) and not stats.errors
    assert (KTB_3Y.item_code, "20160101", "20260107") in ecos.calls
    rows = conn.execute("SELECT date, value FROM rates WHERE series = 'ktb3y' ORDER BY date").fetchall()
    assert rows == [(date(2026, 1, 5), 3.10), (date(2026, 1, 7), 3.15)]


def test_daily_run_rereads_the_last_week() -> None:
    conn = store.open_store(":memory:")
    _load(conn, FakeEcos())
    ecos = FakeEcos()

    _load(conn, ecos, last_day=date(2026, 1, 20))

    assert (KTB_3Y.item_code, "20251231", "20260120") in ecos.calls
    assert conn.execute("SELECT count(*) FROM rates WHERE series = 'ktb3y'").fetchone()[0] == 2


def test_sample_key_skips_with_an_error() -> None:
    conn = store.open_store(":memory:")
    ecos = FakeEcos(sample=True)

    stats = _load(conn, ecos)

    assert ecos.calls == [] and stats.errors[0]["code"] == "ecos"


def test_status_reports_rates_per_series() -> None:
    conn = store.open_store(":memory:")
    _load(conn, FakeEcos())

    rates = store.status(conn)["rates"]

    assert rates["ktb3y"] == {"rows": 2, "first_date": "2026-01-05", "last_date": "2026-01-07"}
