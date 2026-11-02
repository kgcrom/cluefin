"""`cache base-rate`/`cache base-rate-build`: cell math, merge-up, forward returns and touch rate.

The build pipeline (`_judge_universe`/`_build_date`) is exercised with `cache.trend`'s
`_universe`/`_indices`/`_series` and `trend_setup.analyze` monkeypatched — real trend-setup
math is already covered by `test_cache_trend_unit.py`; here only base-rate's own SQL/state
machine (sampling, incrementality, idempotence, mcap terciles) is under test.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pytest

from cluefin_openapi_cli import trend_setup as trend_setup_module
from cluefin_openapi_cli.cache import baserate, store
from cluefin_openapi_cli.cache import trend as cache_trend_module
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.main import run_cli

# ---------------------------------------------------------------------------
# pure helpers
# ---------------------------------------------------------------------------


def test_bucket_of_terciles() -> None:
    cut1, cut2 = baserate._mcap_buckets([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])

    assert baserate._bucket_of(5.0, cut1, cut2) == 0
    assert baserate._bucket_of(cut1, cut1, cut2) == 0
    assert baserate._bucket_of(cut2, cut1, cut2) == 1
    assert baserate._bucket_of(1e9, cut1, cut2) == 2


def test_status_to_state_covers_every_trend_setup_status() -> None:
    # Keep in sync with `cache.trend._STATUS_ORDER`.
    statuses = {
        "setup",
        "breaking_out",
        "g3_candidate",
        "g2",
        "extended",
        "far_below_pivot",
        "overheated",
        "no_group",
        "illiquid",
    }
    assert set(baserate._STATUS_TO_STATE) == statuses
    assert baserate._STATUS_TO_STATE["illiquid"] is None
    assert {v for v in baserate._STATUS_TO_STATE.values() if v} == {"g1", "g2", "g3", "none"}


# ---------------------------------------------------------------------------
# cell resolution / merge-up
# ---------------------------------------------------------------------------


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.close()
    return tmp_path


def _insert_setup_state(rows: list[tuple]) -> None:
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO setup_state (sample_date, code, market, state, mcap_bucket, mcap, adj_close, index_code, "
        "index_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.close()


def _row(i: int, state: str = "g3", bucket: int = 0) -> tuple:
    day = date(2024, 1, 1) + timedelta(days=i)
    return (day, f"C{i:04d}", "KOSPI", state, bucket, 1000.0 + i, 100.0, "U0001", 1000.0)


def test_resolve_cell_merges_up_when_small(cache) -> None:
    # group×mcap: 5 rows (below MIN_SAMPLES). group (any bucket, state g3): 40 rows.
    rows = [_row(i, "g3", 0) for i in range(5)] + [_row(100 + i, "g3", 1) for i in range(35)]
    _insert_setup_state(rows)
    conn = store.open_store(read_only=True)

    level, chosen = baserate._resolve_cell(conn, "g3", 0)

    assert level == "group"
    assert len(chosen) == 40


def test_resolve_cell_keeps_group_mcap_when_big_enough(cache) -> None:
    rows = [_row(i, "g3", 0) for i in range(30)]
    _insert_setup_state(rows)
    conn = store.open_store(read_only=True)

    level, chosen = baserate._resolve_cell(conn, "g3", 0)

    assert level == "group_mcap"
    assert len(chosen) == 30


def test_resolve_cell_falls_back_to_all(cache) -> None:
    rows = [_row(i, "g3", 0) for i in range(3)] + [_row(200 + i, "none", 2) for i in range(4)]
    _insert_setup_state(rows)
    conn = store.open_store(read_only=True)

    level, chosen = baserate._resolve_cell(conn, "g3", 0)

    assert level == "all"
    assert len(chosen) == 7  # still below MIN_SAMPLES, but "all" is the last resort


# ---------------------------------------------------------------------------
# forward excess return
# ---------------------------------------------------------------------------


def _calendar(n: int, start: date = date(2024, 1, 2)) -> list[date]:
    return [start + timedelta(days=i) for i in range(n)]


def test_horizon_stats_computes_excess_return_against_the_index(cache) -> None:
    calendar = _calendar(40)
    base_a, base_b = calendar[10], calendar[11]
    fwd_a, fwd_b = calendar[10 + 20], calendar[11 + 20]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, high, low, adj_factor) VALUES (?, ?, ?, ?, ?, 1.0)",
        [
            ("A1", base_a, 100.0, 100.0, 100.0),
            ("A1", fwd_a, 110.0, 110.0, 110.0),
            ("A2", base_b, 200.0, 200.0, 200.0),
            ("A2", fwd_b, 180.0, 180.0, 180.0),
            ("U0001", base_a, 1000.0, 1000.0, 1000.0),
            ("U0001", fwd_a, 1050.0, 1050.0, 1050.0),
            ("U0001", base_b, 2000.0, 2000.0, 2000.0),
            ("U0001", fwd_b, 1900.0, 1900.0, 1900.0),
        ],
    )
    rows = [
        (base_a, "A1", "KOSPI", "U0001"),
        (base_b, "A2", "KOSPI", "U0001"),
    ]

    stats = baserate._horizon_stats(conn, rows, calendar, 20, target_pct=None, stop_pct=None)

    expected_excess = np.array([110 / 100 - 1 - (1050 / 1000 - 1), 180 / 200 - 1 - (1900 / 2000 - 1)])
    quantiles = np.quantile(expected_excess, baserate._QUANTILES)
    assert stats["n"] == 2
    assert stats["distinct_dates"] == 2
    assert stats["mean"] == pytest.approx(float(expected_excess.mean()), abs=1e-6)
    assert stats["p50"] == pytest.approx(float(quantiles[2]), abs=1e-6)
    assert stats["p10"] == pytest.approx(float(quantiles[0]), abs=1e-6)
    assert stats["share_positive"] == pytest.approx(0.5)
    assert stats["touch"] is None


def test_horizon_stats_drops_samples_without_a_forward_date(cache) -> None:
    calendar = _calendar(5)
    conn = store.open_store()
    rows = [(calendar[4], "A1", "KOSPI", "U0001")]  # no day 20 sessions ahead

    stats = baserate._horizon_stats(conn, rows, calendar, 20, target_pct=None, stop_pct=None)

    assert stats == {
        "n": 0,
        "distinct_dates": 0,
        "p10": None,
        "p25": None,
        "p50": None,
        "p75": None,
        "p90": None,
        "mean": None,
        "share_positive": None,
        "touch": None,
    }


def test_horizon_stats_rereads_the_base_price_so_a_later_adj_factor_rewrite_cannot_go_stale(cache) -> None:
    """Regression: `setup_state` used to freeze the base adjusted close at build time.

    `cache load` can rewrite a stock's *whole* `adj_factor` history once it detects a new
    corporate action (AGENTS.md "0.5원 넘게 다르면 … 전 구간 재계산"). A cell built before that
    rewrite must not keep comparing an old-factor base price against a current-factor forward
    price — both have to come from the same (the current) factor, or the excess return jumps
    by the correction ratio for no economic reason.
    """

    calendar = _calendar(40)
    base_day, fwd_day = calendar[10], calendar[30]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [
            ("P1", base_day, 100.0),
            ("P1", fwd_day, 120.0),
            ("U0001", base_day, 1000.0),
            ("U0001", fwd_day, 1000.0),  # flat index: excess == the stock's own return
        ],
    )
    # `rows` is exactly the shape `_resolve_cell` returns now: no stored adj_close, so the
    # base price can only come from a fresh read of `ohlcv`.
    rows = [(base_day, "P1", "KOSPI", "U0001")]

    before = baserate._horizon_stats(conn, rows, calendar, 20, target_pct=None, stop_pct=None)
    assert before["mean"] == pytest.approx(120 / 100 - 1, abs=1e-9)

    # Simulate a later `cache load` that discovers a new corporate action and recomputes P1's
    # whole adj_factor history, changing the factor on `base_day` only (the split's effective
    # date falls between base_day and fwd_day, so the two days now carry different factors).
    conn.execute("UPDATE ohlcv SET adj_factor = 2.0 WHERE code = 'P1' AND date = ?", [base_day])

    after = baserate._horizon_stats(conn, rows, calendar, 20, target_pct=None, stop_pct=None)

    # The same `rows` (same setup_state cell) must now reflect the corrected factor, not a
    # value frozen at build time.
    assert after["mean"] == pytest.approx(120 / (100 * 2.0) - 1, abs=1e-9)
    assert after["mean"] != before["mean"]


# ---------------------------------------------------------------------------
# touch rate (target/stop), including the same-day-both-hit tie
# ---------------------------------------------------------------------------


def test_touch_rate_same_day_both_hit_counts_as_stop(cache) -> None:
    calendar = _calendar(2)
    base_day, next_day = calendar[0], calendar[1]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, high, low, adj_factor) VALUES (?, ?, 100.0, ?, ?, 1.0)",
        [
            ("T1", base_day, None, None),
            ("T2", base_day, None, None),
            ("T3", base_day, None, None),
            ("T4", base_day, None, None),
            ("T1", next_day, 112.0, 95.0),  # target only (+10% = 110 reached, -10% = 90 not)
            ("T2", next_day, 112.0, 85.0),  # both reached same day -> counts as stop
            ("T3", next_day, 105.0, 85.0),  # stop only
            ("T4", next_day, 101.0, 99.0),  # neither
        ],
    )
    rows = [(base_day, code, "KOSPI", "U0001") for code in ("T1", "T2", "T3", "T4")]

    stats = baserate._horizon_stats(conn, rows, calendar, 1, target_pct=10.0, stop_pct=10.0)

    touch = stats["touch"]
    assert touch["n"] == 4
    assert touch["target_rate"] == pytest.approx(0.25)
    assert touch["stop_rate"] == pytest.approx(0.5)
    assert touch["neither_rate"] == pytest.approx(0.25)


# ---------------------------------------------------------------------------
# query(): orchestration and output shape, with `_current_state`/`_current_bucket` stubbed
# ---------------------------------------------------------------------------


def test_query_output_shape_and_merge_up_note(cache, monkeypatch) -> None:
    calendar = _calendar(60)
    as_of = calendar[-1]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, 1.0, 1.0)",
        [("U0001", day) for day in calendar],
    )
    conn.execute("INSERT INTO company (code, name, market, list_count) VALUES ('900000', 'test', 'KOSPI', 1000)")
    rows = [_row(i, "g3", 0) for i in range(3)]  # tiny cell: must merge up, but "all" stays below MIN_SAMPLES
    conn.executemany(
        "INSERT INTO setup_state (sample_date, code, market, state, mcap_bucket, mcap, adj_close, index_code, "
        "index_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.close()
    monkeypatch.setattr(baserate, "_current_state", lambda conn, code, market, as_of: "g3")
    monkeypatch.setattr(
        baserate, "_current_bucket", lambda conn, code, as_of: {"bucket": 0, "mcap": 123.0, "universe_n": 10}
    )

    conn = store.open_store(read_only=True)
    try:
        payload = baserate.query(conn, "900000", as_of=as_of, horizons=(20,))
    finally:
        conn.close()

    assert payload["code"] == "900000"
    assert payload["state"]["state"] == "g3"
    assert payload["cell"]["level"] == "all"
    assert payload["cell"]["n"] == 3
    assert set(payload["horizons"]) == {"20"}
    assert any("미만" in note for note in payload["notes"])


def test_query_unknown_code_is_a_usage_error(cache) -> None:
    conn = store.open_store()
    conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', '2024-01-02', 1.0, 1.0)")
    conn.close()
    conn = store.open_store(read_only=True)

    with pytest.raises(CliError):
        baserate.query(conn, "000000")
    conn.close()


# ---------------------------------------------------------------------------
# build(): sampling, incrementality, idempotence, cell assignment -- via monkeypatched
# cache.trend internals and trend_setup.analyze (the price-feature math is covered
# elsewhere; this only tests base-rate's own SQL/state machine).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _FakePrices:
    dates: tuple[str, ...]

    def window(self, start: int | None = None, stop: int | None = None) -> _FakePrices:
        return self


_UNIVERSE = [
    {"code": "B0001", "market": "KOSPI", "name": "a", "list_count": 1000},
    {"code": "B0002", "market": "KOSPI", "name": "b", "list_count": 1000},
    {"code": "B0003", "market": "KOSPI", "name": "c", "list_count": 1000},
]
# Cycle through states so the mapping (_STATUS_TO_STATE) and mcap terciles both get exercised.
_STATUS_CYCLE = ["setup", "no_group", "overheated"]


@pytest.fixture
def build_cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO company (code, name, market, list_count) VALUES (?, ?, ?, ?)",
        [(row["code"], row["name"], row["market"], row["list_count"]) for row in _UNIVERSE],
    )
    conn.close()
    return tmp_path


def _add_calendar_day(day: date, closes: dict[str, float]) -> None:
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [(code, day, close) for code, close in closes.items()],
    )
    conn.close()


def _patch_build(monkeypatch) -> None:
    monkeypatch.setattr(cache_trend_module, "_universe", lambda conn, d, market, codes: _UNIVERSE)
    monkeypatch.setattr(
        cache_trend_module,
        "_indices",
        lambda conn, d: {
            "U0001": trend_setup_module.IndexCloses(dates=(d.strftime("%Y%m%d"),), closes=np.array([1000.0]))
        },
    )
    monkeypatch.setattr(
        cache_trend_module,
        "_series",
        lambda conn, codes, d: {code: _FakePrices(dates=(d.strftime("%Y%m%d"),)) for code in codes},
    )

    def _fake_analyze(prices: _FakePrices, index) -> dict:
        n = int(prices.dates[0][-2:])  # use the day-of-month to vary state deterministically
        code_rank = n % 3
        return {"setup": {"status": _STATUS_CYCLE[code_rank]}, "close": 100.0 + n}

    monkeypatch.setattr(trend_setup_module, "analyze", _fake_analyze)


def test_build_is_incremental_and_idempotent(build_cache, monkeypatch) -> None:
    _patch_build(monkeypatch)
    days = [date(2024, 1, 2) + timedelta(days=i) for i in range(11)]  # indices 0..10
    for i, day in enumerate(days):
        _add_calendar_day(day, {"U0001": 1000.0, "B0001": 100.0 + i, "B0002": 50.0 + i, "B0003": 20.0 + i})
    conn = store.open_store()

    first = baserate.build(conn, stride=5)

    assert first["sample_dates"] == 3  # indices 0, 5, 10
    assert first["dates_added"] == 3
    assert first["rows_added"] == 9  # 3 stocks x 3 dates
    assert first["table"]["dates"] == 3

    # No new calendar days: rerunning finds nothing new (idempotent).
    second = baserate.build(conn, stride=5)
    assert second["dates_added"] == 0
    assert second["rows_added"] == 0
    assert second["table"]["rows"] == first["table"]["rows"]

    # One more trading day lands exactly on the next stride point (index 15 needs indices up to
    # 15; add 5 more days, indices 11..15).
    for i in range(11, 16):
        day = date(2024, 1, 2) + timedelta(days=i)
        _add_calendar_day(day, {"U0001": 1000.0, "B0001": 100.0 + i, "B0002": 50.0 + i, "B0003": 20.0 + i})
    third = baserate.build(conn, stride=5)
    assert third["dates_added"] == 1  # only index 15 is new
    assert third["table"]["dates"] == 4

    conn.close()


def test_build_assigns_mcap_terciles_within_the_sample_day(build_cache, monkeypatch) -> None:
    _patch_build(monkeypatch)
    day = date(2024, 1, 10)  # day-of-month 10 -> rank 10 % 3 == 1 -> "no_group" -> state "none"
    _add_calendar_day(day, {"U0001": 1000.0, "B0001": 300.0, "B0002": 200.0, "B0003": 100.0})
    conn = store.open_store()

    rows = baserate._build_date(conn, day)
    conn.close()

    by_code = {row[1]: row for row in rows}
    assert {row[3] for row in rows} == {"none"}  # all three codes share the same fake status this day
    assert by_code["B0003"][4] == 0  # smallest mcap -> bucket 0
    assert by_code["B0002"][4] == 1
    assert by_code["B0001"][4] == 2  # largest mcap -> bucket 2


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------


def test_cli_rejects_target_pct_without_stop_pct(cache) -> None:
    result = run_cli(["cache", "base-rate", "--code", "000000", "--target-pct", "10", "--json"])

    assert result.exit_code == 2


def test_cli_requires_code(cache) -> None:
    result = run_cli(["cache", "base-rate", "--json"])

    assert result.exit_code == 2


def test_cli_base_rate_build_and_query_wiring(build_cache, monkeypatch) -> None:
    _patch_build(monkeypatch)
    days = [date(2024, 1, 2) + timedelta(days=i) for i in range(11)]
    for i, day in enumerate(days):
        _add_calendar_day(day, {"U0001": 1000.0, "B0001": 100.0 + i, "B0002": 50.0 + i, "B0003": 20.0 + i})

    build_result = run_cli(["cache", "base-rate-build", "--stride", "5", "--json"])
    assert build_result.exit_code == 0
    build_payload = json.loads(build_result.stdout)
    assert build_payload["dates_added"] == 3

    monkeypatch.setattr(baserate, "_current_state", lambda conn, code, market, as_of: "none")
    monkeypatch.setattr(
        baserate, "_current_bucket", lambda conn, code, as_of: {"bucket": 1, "mcap": 1.0, "universe_n": 3}
    )
    query_result = run_cli(["cache", "base-rate", "--code", "B0001", "--horizons", "1", "--json"])
    assert query_result.exit_code == 0
    payload = json.loads(query_result.stdout)
    assert payload["code"] == "B0001"
    assert set(payload["horizons"]) == {"1"}
