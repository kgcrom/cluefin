"""`cache magic-formula`: universe filters, approximate EV/ROIC math, percentile-rank sum, CLI wiring."""

from __future__ import annotations

from datetime import date

import pytest

from cluefin_openapi_cli.cache import magic, store
from cluefin_openapi_cli.main import run_cli

_AS_OF = date(2026, 3, 2)


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.close()
    return tmp_path


def _insert_company(
    conn,
    code: str,
    *,
    name: str | None = None,
    market: str = "KOSPI",
    sector: str = "전기/전자",
    list_count: int | None = 1_000_000,
    is_admin: bool = False,
    is_halted: bool = False,
) -> None:
    conn.execute(
        "INSERT INTO company (code, name, market, sector, list_count, is_admin, is_halted) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [code, name or f"stock-{code}", market, sector, list_count, is_admin, is_halted],
    )


def _insert_close(conn, code: str, close: float, *, as_of: date = _AS_OF) -> None:
    conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)", [code, as_of, close])


def _insert_financials(
    conn,
    code: str,
    *,
    year: str = "2025",
    ebit: float | None,
    assets: float | None,
    current_liab: float | None,
    total_liab: float | None,
) -> None:
    accounts = {
        "영업이익": ebit,
        "자산총계": assets,
        "유동부채": current_liab,
        "부채총계": total_liab,
    }
    rows = [
        (code, year, "11011", "CFS", account_nm, amount, "KRW")
        for account_nm, amount in accounts.items()
        if amount is not None
    ]
    if rows:
        conn.executemany(
            "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            rows,
        )


def _setup_candidate(
    conn,
    code: str,
    *,
    close: float,
    ebit: float,
    assets: float,
    current_liab: float,
    total_liab: float,
    **company_kwargs,
) -> None:
    _insert_company(conn, code, **company_kwargs)
    _insert_close(conn, code, close)
    _insert_financials(conn, code, ebit=ebit, assets=assets, current_liab=current_liab, total_liab=total_liab)


def _insert_mcap_filler(conn, code: str = "900090") -> None:
    """A tiny-market-cap stock with no financials, just so a small universe under test has a

    clear "bottom 20%" to drop — with only the stocks under test (often tied or close in
    market cap), the quantile cutoff can land on or above every one of them and drop them all.
    """

    _insert_company(conn, code)
    _insert_close(conn, code, 1.0)


def _insert_index_bar(conn, *, as_of: date = _AS_OF) -> None:
    conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, 1000.0, 1.0)", [as_of])


# ---------------------------------------------------------------------------
# universe filters
# ---------------------------------------------------------------------------


def test_screen_excludes_financial_insurance_utility_sectors(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0)
    for code, sector in (("900020", "금융"), ("900030", "증권"), ("900040", "보험"), ("900050", "전기/가스")):
        _setup_candidate(
            conn, code, close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0, sector=sector
        )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["universe"] == 5
    assert payload["after_sector_admin_halt"] == 1
    assert {row["code"] for row in payload["rows"]} == {"900010"}


def test_screen_excludes_admin_and_halted(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0)
    _setup_candidate(
        conn, "900020", close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0, is_admin=True
    )
    _setup_candidate(
        conn, "900030", close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0, is_halted=True
    )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert {row["code"] for row in payload["rows"]} == {"900010"}
    assert payload["after_sector_admin_halt"] == 1


def test_screen_excludes_bottom_20pct_by_market_cap(cache) -> None:
    # list_count fixed at 1, close == mcap: 10, 20, 30, 40, 50 -> np.quantile(.., 0.2) == 18,
    # only the 10 falls at/below the cutoff.
    conn = store.open_store()
    for code, mcap in (("900010", 10.0), ("900020", 20.0), ("900030", 30.0), ("900040", 40.0), ("900050", 50.0)):
        _setup_candidate(
            conn,
            code,
            close=mcap,
            ebit=100.0,
            assets=1000.0,
            current_liab=200.0,
            total_liab=400.0,
            list_count=1,
        )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["after_sector_admin_halt"] == 5
    assert payload["after_mcap_filter"] == 4
    assert payload["excluded"]["bottom_mcap_20pct"] == 1
    assert "900010" not in {row["code"] for row in payload["rows"]}


def test_screen_excludes_stock_without_price_or_list_count(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")  # no ohlcv bar on as_of
    _insert_financials(conn, "900010", ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["excluded"]["no_price_or_list_count"] == 1
    assert payload["rows"] == []


# ---------------------------------------------------------------------------
# financials availability
# ---------------------------------------------------------------------------


def test_screen_excludes_stock_with_no_cached_financials(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["excluded"]["no_financials_or_missing_accounts"] == 1
    assert payload["rows"] == []


def test_screen_excludes_stock_missing_one_required_account(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", close=100.0, ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=None)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["excluded"]["no_financials_or_missing_accounts"] == 1


def test_screen_uses_latest_cached_fiscal_year(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    _insert_financials(conn, "900010", year="2023", ebit=1.0, assets=10.0, current_liab=1.0, total_liab=1.0)
    _insert_financials(conn, "900010", year="2025", ebit=100.0, assets=1000.0, current_liab=200.0, total_liab=400.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["rows"][0]["fiscal_year"] == "2025"


def test_screen_excludes_non_positive_ebit_capital_or_ev(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", close=100.0, ebit=-5.0, assets=1000.0, current_liab=200.0, total_liab=400.0)
    _setup_candidate(conn, "900020", close=100.0, ebit=100.0, assets=200.0, current_liab=300.0, total_liab=400.0)
    _insert_mcap_filler(conn)  # keeps both subjects above the bottom-20% mcap cutoff
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    assert payload["excluded"]["non_positive_ebit_or_capital_or_ev"] == 2
    assert payload["rows"] == []


# ---------------------------------------------------------------------------
# ranking: percentile-rank sum, descending
# ---------------------------------------------------------------------------


def test_screen_ranks_by_combined_percentile_descending(cache) -> None:
    conn = store.open_store()
    # 900010: mcap 100, EBIT 50 -> EV=100+40=140, ey=50/140≈0.357; capital=1000-200=800, roic=50/800=0.0625
    _setup_candidate(conn, "900010", close=100.0, ebit=50.0, assets=1000.0, current_liab=200.0, total_liab=40.0)
    # 900020: mcap 100, EBIT 5 -> EV=100+40=140, ey=5/140≈0.0357; capital=800, roic=5/800=0.00625 (worst on both)
    _setup_candidate(conn, "900020", close=100.0, ebit=5.0, assets=1000.0, current_liab=200.0, total_liab=40.0)
    # 900030: mcap 100, EBIT 20 -> EV=140, ey=20/140≈0.143; capital=800, roic=20/800=0.025 (middle on both)
    _setup_candidate(conn, "900030", close=100.0, ebit=20.0, assets=1000.0, current_liab=200.0, total_liab=40.0)
    _insert_mcap_filler(conn)  # keeps all three tied-mcap subjects above the bottom-20% cutoff
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF)
    conn.close()

    codes = [row["code"] for row in payload["rows"]]
    assert codes == ["900010", "900030", "900020"]
    assert payload["rows"][0]["earnings_yield_rank"] == 99
    assert payload["rows"][0]["roic_rank"] == 99
    assert payload["rows"][0]["combined_rank"] == 198
    assert payload["rows"][-1]["combined_rank"] == 0
    assert payload["ranked"] == 3


def test_screen_top_trims_rows_not_ranking_population(cache) -> None:
    conn = store.open_store()
    for i, code in enumerate(("900010", "900020", "900030")):
        _setup_candidate(conn, code, close=100.0, ebit=10.0 + i, assets=1000.0, current_liab=200.0, total_liab=40.0)
    _insert_mcap_filler(conn)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = magic.screen(conn, _AS_OF, top=1)
    conn.close()

    assert payload["ranked"] == 3
    assert payload["count"] == 1
    assert len(payload["rows"]) == 1


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------


def test_cli_magic_formula_reads_the_cache(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", close=100.0, ebit=50.0, assets=1000.0, current_liab=200.0, total_liab=40.0)
    _insert_index_bar(conn)
    conn.close()

    result = run_cli(["cache", "magic-formula", "--as-of", _AS_OF.strftime("%Y%m%d"), "--top", "5", "--json"])

    assert result.exit_code == 0
    import json

    payload = json.loads(result.stdout)
    assert payload["top"] == 5
    assert payload["rows"][0]["code"] == "900010"


def test_cli_magic_formula_rejects_non_positive_top(cache) -> None:
    result = run_cli(["cache", "magic-formula", "--top", "0", "--json"])

    assert result.exit_code == 2


def test_cli_magic_formula_rejects_non_integer_top(cache) -> None:
    result = run_cli(["cache", "magic-formula", "--top", "abc", "--json"])

    assert result.exit_code == 2
