"""`cache rs`: percentile math, RS(1M)/sector RS, CLI wiring."""

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


def test_cli_rs_reads_the_cache(rs_cache) -> None:

    as_of = _calendar(22)[-1]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, 1000.0, 1.0)",
        [(day,) for day in _calendar(22)],
    )
    conn.close()

    rs_result = run_cli(["cache", "rs", "--as-of", as_of.strftime("%Y%m%d"), "--json"])

    assert rs_result.exit_code == 0
    assert json.loads(rs_result.stdout)["as_of"] == as_of.isoformat()
