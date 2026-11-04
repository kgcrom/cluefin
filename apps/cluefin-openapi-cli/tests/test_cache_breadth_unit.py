"""`cache rs`/`cache breadth`: percentile math, distribution days, follow-through day, CLI wiring."""

from __future__ import annotations

import json
from datetime import date, timedelta

import numpy as np
import pytest

from cluefin_openapi_cli.cache import breadth, store
from cluefin_openapi_cli.main import run_cli


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.close()
    return tmp_path


def _calendar(n: int, start: date = date(2024, 1, 2)) -> list[date]:
    return [start + timedelta(days=i) for i in range(n)]


# ---------------------------------------------------------------------------
# _percentile_rank: pure math
# ---------------------------------------------------------------------------


def test_percentile_rank_no_ties_spans_0_to_99() -> None:
    ranks = breadth._percentile_rank(np.array([10.0, 40.0, 20.0, 30.0]))

    # sorted order: 10, 20, 30, 40 -> ranks 0,1,2,3 -> *33
    by_value = dict(zip([10.0, 40.0, 20.0, 30.0], ranks, strict=True))
    assert by_value[10.0] == pytest.approx(0.0)
    assert by_value[20.0] == pytest.approx(33.0)
    assert by_value[30.0] == pytest.approx(66.0)
    assert by_value[40.0] == pytest.approx(99.0)


def test_percentile_rank_ties_share_the_average_rank() -> None:
    # 10, 10, 20, 30: the tied 10s share rank (0+1)/2 = 0.5 -> 0.5/3*99 = 16.5
    ranks = breadth._percentile_rank(np.array([10.0, 10.0, 20.0, 30.0]))

    assert ranks[0] == pytest.approx(16.5)
    assert ranks[1] == pytest.approx(16.5)
    assert ranks[2] == pytest.approx(66.0)
    assert ranks[3] == pytest.approx(99.0)


def test_percentile_rank_single_value_is_zero() -> None:
    assert breadth._percentile_rank(np.array([42.0])) == pytest.approx([0.0])


def test_percentile_rank_empty_is_empty() -> None:
    assert list(breadth._percentile_rank(np.array([]))) == []


# ---------------------------------------------------------------------------
# rs(): cross-sectional RS(1M) + sector RS, against a small synthetic universe
# ---------------------------------------------------------------------------


def _insert_company(conn, code: str, sector: str) -> None:
    conn.execute(
        "INSERT INTO company (code, name, market, sector, industry) VALUES (?, ?, 'KOSPI', ?, 'ind')",
        [code, f"stock-{code}", sector],
    )


def _insert_return_series(conn, code: str, start_close: float, end_close: float) -> None:
    """22 daily bars so the 21-trading-day return is exactly ``end_close / start_close - 1``."""

    calendar = _calendar(22)
    closes = [start_close] + [100.0] * 20 + [end_close]
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [(code, day, close) for day, close in zip(calendar, closes, strict=True)],
    )


# Two sectors of 3 stocks each (meets `_MIN_SECTOR_STOCKS`), distinct 21-day returns.
_RS_UNIVERSE = {
    # code: (sector, start_close, end_close)
    "900010": ("A", 100.0, 150.0),  # +50%, highest overall
    "900020": ("A", 100.0, 120.0),  # +20%
    "900030": ("A", 100.0, 90.0),  # -10%, lowest overall
    "900040": ("B", 100.0, 105.0),  # +5%
    "900050": ("B", 100.0, 100.0),  # 0%
    "900060": ("B", 100.0, 95.0),  # -5%
}


@pytest.fixture
def rs_cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    for code, (sector, start_close, end_close) in _RS_UNIVERSE.items():
        _insert_company(conn, code, sector)
        _insert_return_series(conn, code, start_close, end_close)
    conn.close()
    return tmp_path


def test_rs_orders_rows_by_percentile_best_first(rs_cache) -> None:
    conn = store.open_store(read_only=True)
    as_of = _calendar(22)[-1]

    payload = breadth.rs(conn, as_of)
    conn.close()

    assert [row["code"] for row in payload["rows"]][:1] == ["900010"]  # +50% is the top return
    assert [row["code"] for row in payload["rows"]][-1:] == ["900030"]  # -10% is the bottom
    assert payload["rows"][0]["rs_1m"] == 99
    assert payload["rows"][-1]["rs_1m"] == 0
    assert payload["judged"] == 6
    assert payload["skipped"] == 0


def test_rs_sector_percentile_ranks_sector_a_above_sector_b(rs_cache) -> None:
    # Sector A median return (+20%) beats sector B median (0%): with only 2 sector groups,
    # the better one gets 99 and the other 0.
    conn = store.open_store(read_only=True)
    as_of = _calendar(22)[-1]

    payload = breadth.rs(conn, as_of)
    conn.close()

    by_code = {row["code"]: row for row in payload["rows"]}
    assert by_code["900010"]["sector_rs"] == 99
    assert by_code["900020"]["sector_rs"] == 99
    assert by_code["900030"]["sector_rs"] == 99
    assert by_code["900040"]["sector_rs"] == 0
    assert by_code["900050"]["sector_rs"] == 0
    assert by_code["900060"]["sector_rs"] == 0
    assert payload["groups"]["A"]["median_return_1m_pct"] == pytest.approx(20.0)
    assert payload["groups"]["B"]["median_return_1m_pct"] == pytest.approx(0.0)


def test_rs_group_below_min_size_is_dropped(rs_cache) -> None:
    conn = store.open_store()
    conn.execute("INSERT INTO company (code, name, market, sector) VALUES ('900070', 'solo', 'KOSPI', 'C')")
    _insert_return_series(conn, "900070", 100.0, 130.0)
    conn.close()
    as_of = _calendar(22)[-1]

    conn = store.open_store(read_only=True)
    payload = breadth.rs(conn, as_of)
    conn.close()

    assert "C" not in payload["groups"]
    by_code = {row["code"]: row for row in payload["rows"]}
    assert by_code["900070"]["sector_rs"] is None
    assert by_code["900070"]["rs_1m"] is not None  # own RS is unaffected by the group size


def test_rs_market_and_code_filters(rs_cache) -> None:
    conn = store.open_store(read_only=True)
    as_of = _calendar(22)[-1]

    payload = breadth.rs(conn, as_of, codes=["900010", "900040"])
    conn.close()

    assert {row["code"] for row in payload["rows"]} == {"900010", "900040"}


def test_rs_by_industry_groups_on_the_industry_column(rs_cache) -> None:
    conn = store.open_store()
    conn.execute("UPDATE company SET industry = 'ind-x' WHERE code IN ('900010', '900020', '900030')")
    conn.execute("UPDATE company SET industry = 'ind-y' WHERE code IN ('900040', '900050', '900060')")
    conn.close()
    as_of = _calendar(22)[-1]

    conn = store.open_store(read_only=True)
    payload = breadth.rs(conn, as_of, group_by="industry")
    conn.close()

    assert payload["group_by"] == "industry"
    assert set(payload["groups"]) == {"ind-x", "ind-y"}


def test_rs_skips_stocks_without_a_bar_on_as_of(rs_cache) -> None:
    conn = store.open_store(read_only=True)
    future_day = _calendar(23)[-1]  # no code has a bar here

    payload = breadth.rs(conn, future_day)
    conn.close()

    assert payload["judged"] == 0
    assert all(row["rs_1m"] is None for row in payload["rows"])


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------


def test_cli_rs_rejects_bad_by(cache) -> None:
    result = run_cli(["cache", "rs", "--by", "country", "--json"])

    assert result.exit_code == 2


def test_cli_rs_rejects_bad_market(cache) -> None:
    result = run_cli(["cache", "rs", "--market", "nyse", "--json"])

    assert result.exit_code == 2


# ---------------------------------------------------------------------------
# distribution days
# ---------------------------------------------------------------------------


def test_distribution_day_is_a_decline_on_higher_volume(cache) -> None:
    calendar = _calendar(3)
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, volume, adj_factor) VALUES ('U0001', ?, ?, ?, 1.0)",
        [
            (calendar[0], 1000.0, 100.0),
            (calendar[1], 994.0, 150.0),  # -0.6%, higher volume -> distribution day
            (calendar[2], 995.0, 50.0),  # +0.1%, lower volume -> not
        ],
    )

    result = breadth._distribution_days(conn, "U0001", calendar[-1])
    conn.close()

    assert result["count"] == 1
    assert result["days"] == [{"date": calendar[1].isoformat(), "change_pct": pytest.approx(-0.6, abs=1e-2)}]


def test_distribution_day_decline_without_higher_volume_does_not_count(cache) -> None:
    calendar = _calendar(2)
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, volume, adj_factor) VALUES ('U0001', ?, ?, ?, 1.0)",
        [(calendar[0], 1000.0, 200.0), (calendar[1], 990.0, 100.0)],  # -1%, lower volume
    )

    result = breadth._distribution_days(conn, "U0001", calendar[-1])
    conn.close()

    assert result["count"] == 0


# ---------------------------------------------------------------------------
# follow-through day
# ---------------------------------------------------------------------------


def _ftd_fixture(conn, *, breakout_gain: float, breakout_volume: float) -> list[date]:
    """50 days of monotone decline (swing low on the 50th), then a rally day 1, then a window."""

    calendar = _calendar(61)
    closes = [2000.0 - i * 20.0 for i in range(50)]  # idx0..49, idx49 = 1020 is the window min
    closes.append(1030.0)  # idx50 = day 1 (up from 1020)
    closes.append(1032.0)  # idx51
    closes.append(1034.0)  # idx52
    closes.append(round(1034.0 * (1 + breakout_gain / 100), 4))  # idx53 = day 4 of the rally
    closes.extend([closes[-1]] * 7)  # idx54..60, flat
    volumes = [1000.0] * 53 + [breakout_volume] + [1000.0] * 7
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, volume, adj_factor) VALUES ('U0001', ?, ?, ?, 1.0)",
        list(zip(calendar, closes, volumes, strict=True)),
    )
    return calendar


def test_follow_through_day_found_on_day_4_with_higher_volume(cache) -> None:
    conn = store.open_store()
    calendar = _ftd_fixture(conn, breakout_gain=3.0, breakout_volume=2000.0)

    result = breadth._follow_through_day(conn, "U0001", calendar[-1])
    conn.close()

    assert result["rally_day1"] == calendar[50].isoformat()
    assert result["found"] is True
    assert result["date"] == calendar[53].isoformat()
    assert result["day_number"] == 4
    assert result["gain_pct"] == pytest.approx(3.0, abs=1e-2)


def test_follow_through_day_not_found_below_the_gain_threshold(cache) -> None:
    conn = store.open_store()
    calendar = _ftd_fixture(conn, breakout_gain=0.5, breakout_volume=2000.0)  # below 1.25%

    result = breadth._follow_through_day(conn, "U0001", calendar[-1])
    conn.close()

    assert result["rally_day1"] == calendar[50].isoformat()
    assert result["found"] is False
    assert result["date"] is None


def test_follow_through_day_not_found_without_higher_volume(cache) -> None:
    conn = store.open_store()
    calendar = _ftd_fixture(conn, breakout_gain=3.0, breakout_volume=500.0)  # lower volume

    result = breadth._follow_through_day(conn, "U0001", calendar[-1])
    conn.close()

    assert result["found"] is False


def test_follow_through_day_needs_a_swing_low_first(cache) -> None:
    calendar = _calendar(10)
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, volume, adj_factor) VALUES ('U0001', ?, 1000.0, 100.0, 1.0)",
        [(day,) for day in calendar],
    )

    result = breadth._follow_through_day(conn, "U0001", calendar[-1])
    conn.close()

    assert result["rally_day1"] is None
    assert result["found"] is False


# ---------------------------------------------------------------------------
# breadth(): stock-level counts (highs/lows, %>50dma, advance/decline)
# ---------------------------------------------------------------------------


def _breadth_universe(conn) -> date:
    """4 stocks sharing a flat 254-day history, diverging on the final day; see inline comments."""

    history_days = 254
    calendar = _calendar(history_days + 1)
    as_of = calendar[-1]
    codes = ["900010", "900020", "900030", "900040"]
    for code in codes:
        conn.execute("INSERT INTO company (code, name, market) VALUES (?, ?, 'KOSPI')", [code, f"stock-{code}"])
        conn.executemany(
            "INSERT INTO ohlcv (code, date, open, high, low, close, adj_factor) VALUES (?, ?, ?, ?, ?, ?, 1.0)",
            [(code, day, 100.0, 110.0, 90.0, 100.0) for day in calendar[:history_days]],
        )
    # Final day, per stock: (high, low, close) — history above gives a 110/90/100 baseline.
    finals = {
        "900010": (120.0, 100.0, 190.0),  # new high (> the 110 baseline), above 50dma, advancing
        "900020": (105.0, 80.0, 55.0),  # new low (< the 90 baseline), below 50dma, declining
        "900030": (105.0, 92.0, 100.0),  # unchanged, at the 50dma (counts as above, >=)
        "900040": (105.0, 92.0, 101.0),  # advancing, above 50dma, not a new high/low
    }
    conn.executemany(
        "INSERT INTO ohlcv (code, date, open, high, low, close, adj_factor) VALUES (?, ?, ?, ?, ?, ?, 1.0)",
        [(code, as_of, close, high, low, close) for code, (high, low, close) in finals.items()],
    )
    return as_of


def test_breadth_counts_highs_lows_50dma_and_advance_decline(cache) -> None:
    conn = store.open_store()
    as_of = _breadth_universe(conn)

    payload = breadth.breadth(conn, as_of)
    conn.close()

    assert payload["universe"] == 4
    assert payload["new_52w_high"] == 1
    assert payload["new_52w_low"] == 1
    assert payload["above_50dma"] == 3
    assert payload["above_50dma_judged"] == 4
    assert payload["advancing"] == 2
    assert payload["declining"] == 1
    assert payload["unchanged"] == 1
    assert set(payload["indices"]) == {"U0001", "U1001", "U2001"}


def test_breadth_market_filter(cache) -> None:
    conn = store.open_store()
    as_of = _breadth_universe(conn)
    conn.execute("UPDATE company SET market = 'KOSDAQ' WHERE code = '900010'")

    payload = breadth.breadth(conn, as_of, market="KOSDAQ")
    conn.close()

    assert payload["universe"] == 1
    assert payload["new_52w_high"] == 1


def test_cli_breadth_rejects_bad_market(cache) -> None:
    result = run_cli(["cache", "breadth", "--market", "nyse", "--json"])

    assert result.exit_code == 2


def test_cli_rs_and_breadth_read_the_cache(rs_cache) -> None:
    as_of = _calendar(22)[-1]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, 1000.0, 1.0)",
        [(day,) for day in _calendar(22)],
    )
    conn.close()

    rs_result = run_cli(["cache", "rs", "--as-of", as_of.strftime("%Y%m%d"), "--json"])
    breadth_result = run_cli(["cache", "breadth", "--as-of", as_of.strftime("%Y%m%d"), "--json"])

    assert rs_result.exit_code == 0
    assert json.loads(rs_result.stdout)["as_of"] == as_of.isoformat()
    assert breadth_result.exit_code == 0
    assert json.loads(breadth_result.stdout)["as_of"] == as_of.isoformat()
