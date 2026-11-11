"""`cache peers`: industry/sector fallback, size/correlation ordinal ranks, CLI wiring."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from cluefin_openapi_cli.cache import peers as cache_peers
from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.main import run_cli

_AS_OF = date(2026, 4, 1)


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.close()
    return tmp_path


def _insert_company(
    conn, code: str, *, sector: str = "전기/전자", industry: str = "반도체", list_count: int = 1_000_000
) -> None:
    conn.execute(
        "INSERT INTO company (code, name, market, sector, industry, list_count, is_admin, is_halted) "
        "VALUES (?, ?, 'KOSPI', ?, ?, ?, false, false)",
        [code, f"stock-{code}", sector, industry, list_count],
    )


def _insert_flat_series(conn, code: str, close: float, *, days: int = 260, as_of: date = _AS_OF) -> None:
    """``days`` identical bars ending on ``as_of`` — enough history for `cache screen`'s price factors."""

    start = as_of - timedelta(days=days - 1)
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, high, adj_factor, volume, value) VALUES (?, ?, ?, ?, 1.0, 100, 1000.0)",
        [(code, start + timedelta(days=i), close, close) for i in range(days)],
    )


def _insert_return_series(conn, code: str, returns: list[float], *, as_of: date = _AS_OF) -> None:
    """A daily-return path ending on ``as_of``, oldest first; ``close`` compounds from 100.0."""

    start = as_of - timedelta(days=len(returns))
    close = 100.0
    rows = []
    for i, ret in enumerate(returns):
        close *= 1 + ret
        rows.append((code, start + timedelta(days=i + 1), close, close))
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, high, adj_factor, volume, value) VALUES (?, ?, ?, ?, 1.0, 100, 1000.0)",
        rows,
    )


def test_peers_rejects_unknown_code(cache) -> None:
    conn = store.open_store()
    conn.close()

    conn = store.open_store(read_only=True)
    with pytest.raises(CliError) as exc:
        cache_peers.peers(conn, _AS_OF, "999999")
    conn.close()
    assert exc.value.exit_code == 2


def test_peers_falls_back_to_sector_when_industry_has_fewer_than_3(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010", sector="전기/전자", industry="반도체")
    _insert_company(conn, "900020", sector="전기/전자", industry="디스플레이")  # same sector, different industry
    _insert_company(conn, "900030", sector="전기/전자", industry="디스플레이")
    _insert_company(conn, "900040", sector="화학", industry="정밀화학")  # different sector entirely
    for code in ("900010", "900020", "900030", "900040"):
        _insert_flat_series(conn, code, 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010")
    conn.close()

    assert payload["group_by"] == "sector"
    assert payload["group_value"] == "전기/전자"
    assert {row["code"] for row in payload["rows"]} == {"900020", "900030"}


def test_peers_keeps_industry_when_at_least_3_peers(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010", industry="반도체")
    for code in ("900020", "900030", "900040"):
        _insert_company(conn, code, industry="반도체")
    _insert_company(conn, "900050", industry="디스플레이")
    for code in ("900010", "900020", "900030", "900040", "900050"):
        _insert_flat_series(conn, code, 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010", top=10)
    conn.close()

    assert payload["group_by"] == "industry"
    assert {row["code"] for row in payload["rows"]} == {"900020", "900030", "900040"}


def test_peers_correlation_is_null_below_the_overlap_minimum(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_company(conn, "900020")
    _insert_company(conn, "900030")
    # Only 60 days of history -- below the 120-day overlap minimum.
    _insert_flat_series(conn, "900010", 100.0, days=60)
    _insert_flat_series(conn, "900020", 100.0, days=60)
    _insert_flat_series(conn, "900030", 100.0, days=60)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010", top=10)
    conn.close()

    for row in payload["rows"]:
        assert row["return_correlation"] is None
        assert row["overlap_days"] < 120


def test_peers_ranks_by_size_closeness_and_correlation_sum(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010", list_count=1_000_000)  # target
    _insert_company(conn, "900020", list_count=1_000_000)  # same size, perfectly correlated
    _insert_company(conn, "900030", list_count=10_000_000)  # 10x size, same path (still correlated)
    conn.close()
    conn = store.open_store()
    path = [0.01, -0.02, 0.015, -0.01, 0.02, -0.015] * 40  # 240 days, > 120-day overlap, has variance
    _insert_return_series(conn, "900010", path)
    _insert_return_series(conn, "900020", path)
    _insert_return_series(conn, "900030", path)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010", top=10)
    conn.close()

    rows = {row["code"]: row for row in payload["rows"]}
    # Both move identically (correlation 1.0 for both), so only the size-closeness rank should separate them.
    assert rows["900020"]["combined_rank"] < rows["900030"]["combined_rank"]
    assert rows["900020"]["size_rank"] < rows["900030"]["size_rank"]


def test_peers_rows_carry_the_screen_factor_table(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_company(conn, "900020")
    _insert_company(conn, "900030")
    for code in ("900010", "900020", "900030"):
        _insert_flat_series(conn, code, 100.0)
        conn.execute(
            "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency) "
            "VALUES (?, '2025', '11011', 'CFS', '당기순이익', 10.0, 'KRW')",
            [code],
        )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010", top=10)
    conn.close()

    for row in payload["rows"]:
        assert "mcap" in row
        assert "per" in row
        assert "rs_1m" in row


def test_peers_top_trims_rows(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    for code in ("900020", "900030", "900040", "900050"):
        _insert_company(conn, code)
        _insert_flat_series(conn, code, 100.0)
    _insert_flat_series(conn, "900010", 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010", top=2)
    conn.close()

    assert payload["candidates"] == 4
    assert payload["count"] == 2
    assert len(payload["rows"]) == 2


def test_cli_peers_reads_the_cache(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_company(conn, "900020")
    _insert_company(conn, "900030")
    for code in ("900010", "900020", "900030"):
        _insert_flat_series(conn, code, 100.0)
    conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, 1000.0, 1.0)", [_AS_OF])
    conn.close()

    result = run_cli(
        ["cache", "peers", "--code", "900010", "--as-of", _AS_OF.strftime("%Y%m%d"), "--top", "5", "--json"]
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["code"] == "900010"
    assert {row["code"] for row in payload["rows"]} == {"900020", "900030"}


def test_cli_peers_requires_code(cache) -> None:
    result = run_cli(["cache", "peers", "--json"])
    assert result.exit_code == 2


def test_cli_peers_rejects_unknown_code(cache) -> None:
    result = run_cli(["cache", "peers", "--code", "999999", "--json"])
    assert result.exit_code == 2


def test_peers_of_a_stock_without_a_group_are_empty_not_every_ungrouped_stock(cache) -> None:
    conn = store.open_store()
    for code in ("900010", "900020", "900030", "900040"):
        conn.execute(
            "INSERT INTO company (code, name, market, list_count, is_admin, is_halted) "
            "VALUES (?, ?, 'KOSPI', 1000000, false, false)",
            [code, f"stock-{code}"],
        )
        _insert_flat_series(conn, code, 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = cache_peers.peers(conn, _AS_OF, "900010")
    conn.close()

    assert payload["candidates"] == 0
    assert payload["rows"] == []
