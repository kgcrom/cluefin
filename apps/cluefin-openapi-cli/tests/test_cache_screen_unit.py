"""`cache screen`: factor math, `--where` parsing, universe/sort/preset wiring, CLI."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from cluefin_openapi_cli.cache import screen, store
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.review import paths as review_paths

_AS_OF = date(2026, 4, 1)


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
    industry: str = "반도체",
    list_count: int | None = 1_000_000,
) -> None:
    conn.execute(
        "INSERT INTO company (code, name, market, sector, industry, list_count, is_admin, is_halted) "
        "VALUES (?, ?, ?, ?, ?, ?, false, false)",
        [code, name or f"stock-{code}", market, sector, industry, list_count],
    )


def _insert_close(conn, code: str, close: float, *, as_of: date = _AS_OF, high: float | None = None) -> None:
    conn.execute(
        "INSERT INTO ohlcv (code, date, close, high, adj_factor, volume, value) VALUES (?, ?, ?, ?, 1.0, 100, 1000.0)",
        [code, as_of, close, high if high is not None else close],
    )


def _insert_financials(conn, code: str, year: str, **accounts: float) -> None:
    rows = [(code, year, "11011", "CFS", name, amount, "KRW") for name, amount in accounts.items()]
    conn.executemany(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency) VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows,
    )


def _insert_index_bar(conn, *, as_of: date = _AS_OF) -> None:
    conn.execute("INSERT INTO ohlcv (code, date, close, adj_factor) VALUES ('U0001', ?, 1000.0, 1.0)", [as_of])


_BASELINE_ACCOUNTS = dict(
    영업이익=100.0, 자산총계=1000.0, 유동부채=200.0, 부채총계=400.0, 자본총계=500.0, 매출액=800.0, 당기순이익=50.0
)


def _setup_candidate(conn, code: str, *, close: float = 100.0, year: str = "2025", **company_kwargs) -> None:
    _insert_company(conn, code, **company_kwargs)
    _insert_close(conn, code, close)
    _insert_financials(conn, code, year, **_BASELINE_ACCOUNTS)


# ---------------------------------------------------------------------------
# parse_where: regex parsing, never eval
# ---------------------------------------------------------------------------


def test_parse_where_accepts_all_operators() -> None:
    conditions = screen.parse_where("per<10,pbr<=2,roe>5,mcap>=1,per!=0,rs_1m=50")
    assert [(c.factor, c.op, c.value) for c in conditions] == [
        ("per", "<", 10.0),
        ("pbr", "<=", 2.0),
        ("roe", ">", 5.0),
        ("mcap", ">=", 1.0),
        ("per", "!=", 0.0),
        ("rs_1m", "=", 50.0),
    ]


def test_parse_where_rejects_unknown_factor() -> None:
    with pytest.raises(CliError) as exc:
        screen.parse_where("not_a_factor>10")
    assert exc.value.exit_code == 2
    assert exc.value.data["issues"][0]["problem"] == "unknown factor `not_a_factor`"


def test_parse_where_rejects_malformed_clause() -> None:
    with pytest.raises(CliError) as exc:
        screen.parse_where("per<<10")
    assert exc.value.exit_code == 2


def test_parse_where_rejects_eval_payload() -> None:
    # A clause that isn't `factor op number` must fail to parse, never be executed.
    with pytest.raises(CliError):
        screen.parse_where("__import__('os').system('true')")


def test_factor_catalog_lists_every_documented_factor() -> None:
    names = {entry["factor"] for entry in screen.factor_catalog()["factors"]}
    assert names == {
        "mcap",
        "value_20d",
        "per",
        "pbr",
        "psr",
        "earnings_yield",
        "roe",
        "opm",
        "debt_ratio",
        "roic",
        "revenue_yoy",
        "op_yoy",
        "revenue_cagr_3y",
        "rs_1m",
        "ret_3m",
        "ret_6m",
        "ret_12m",
        "high_52w_gap",
        "above_ma50",
    }


# ---------------------------------------------------------------------------
# universe + sector/industry/market/code filters
# ---------------------------------------------------------------------------


def test_screen_includes_financial_sector_unlike_magic_formula(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", sector="금융")
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    assert payload["universe"] == 1
    assert payload["rows"][0]["code"] == "900010"


def test_screen_nulls_earnings_yield_and_roic_for_excluded_sectors(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", sector="금융")
    _setup_candidate(conn, "900020", sector="전기/전자")
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    rows = {row["code"]: row for row in payload["rows"]}
    assert rows["900010"]["earnings_yield"] is None
    assert rows["900010"]["roic"] is None
    assert rows["900020"]["earnings_yield"] is not None
    assert rows["900020"]["roic"] is not None
    # Every other factor still computes for the excluded sector.
    assert rows["900010"]["roe"] is not None
    assert rows["900010"]["per"] is not None


def test_screen_market_sector_industry_code_narrow_output_rows_only(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010", market="KOSPI", sector="전기/전자", industry="반도체")
    _setup_candidate(conn, "900020", market="KOSDAQ", sector="화학", industry="정밀화학")
    conn.close()

    conn = store.open_store(read_only=True)
    by_market = screen.screen(conn, _AS_OF, market="KOSDAQ")
    by_sector = screen.screen(conn, _AS_OF, sector="전기/전자")
    by_industry = screen.screen(conn, _AS_OF, industry="정밀화학")
    by_code = screen.screen(conn, _AS_OF, codes=["900010"])
    conn.close()

    assert by_market["universe"] == 2  # population unaffected by the row filter
    assert [row["code"] for row in by_market["rows"]] == ["900020"]
    assert [row["code"] for row in by_sector["rows"]] == ["900010"]
    assert [row["code"] for row in by_industry["rows"]] == ["900020"]
    assert [row["code"] for row in by_code["rows"]] == ["900010"]


# ---------------------------------------------------------------------------
# financial ratios
# ---------------------------------------------------------------------------


def test_screen_nulls_per_pbr_psr_on_non_positive_denominator(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    _insert_financials(
        conn,
        "900010",
        "2025",
        영업이익=-10.0,
        자산총계=1000.0,
        유동부채=200.0,
        부채총계=400.0,
        자본총계=-50.0,
        매출액=-5.0,
        당기순이익=-20.0,
    )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    row = payload["rows"][0]
    assert row["per"] is None
    assert row["pbr"] is None
    assert row["psr"] is None
    assert row["roe"] is None  # equity <= 0
    assert row["opm"] is None  # revenue <= 0
    # invested capital (assets - current_liab = 800) is still positive, so roic computes — negative
    # EBIT just makes it a negative (valid) value, not undefined.
    assert row["roic"] == pytest.approx(-10 / 800 * 100)


def test_screen_revenue_yoy_and_op_yoy_use_the_two_most_recent_cached_years(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    _insert_financials(
        conn,
        "900010",
        "2024",
        매출액=100.0,
        영업이익=10.0,
        자산총계=1.0,
        유동부채=1.0,
        자본총계=1.0,
        당기순이익=1.0,
        부채총계=1.0,
    )
    _insert_financials(
        conn,
        "900010",
        "2025",
        매출액=150.0,
        영업이익=5.0,
        자산총계=1.0,
        유동부채=1.0,
        자본총계=1.0,
        당기순이익=1.0,
        부채총계=1.0,
    )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    row = payload["rows"][0]
    assert row["revenue_yoy"] == pytest.approx(50.0)
    assert row["op_yoy"] == pytest.approx(-50.0)
    assert row["revenue_cagr_3y"] is None  # fewer than 4 cached years


def test_screen_revenue_cagr_3y_needs_four_cached_years(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    for year, revenue in (("2022", 100.0), ("2023", 110.0), ("2024", 120.0), ("2025", 133.1)):
        _insert_financials(
            conn,
            "900010",
            year,
            매출액=revenue,
            영업이익=10.0,
            자산총계=1.0,
            유동부채=1.0,
            자본총계=1.0,
            당기순이익=1.0,
            부채총계=1.0,
        )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    row = payload["rows"][0]
    # (133.1/100)^(1/3) - 1 == 10%
    assert row["revenue_cagr_3y"] == pytest.approx(10.0, abs=0.01)


def test_screen_uses_fiscal_year_due_by_as_of(cache) -> None:
    conn = store.open_store()
    as_of = date(2026, 3, 2)  # before the 사업보고서 deadline for FY2025
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0, as_of=as_of)
    _insert_index_bar(conn, as_of=as_of)
    _insert_financials(conn, "900010", "2024", **_BASELINE_ACCOUNTS)
    _insert_financials(conn, "900010", "2025", **{k: v * 2 for k, v in _BASELINE_ACCOUNTS.items()})
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, as_of)
    conn.close()

    assert payload["rows"][0]["fiscal_year"] == "2024"


# ---------------------------------------------------------------------------
# price-based factors (returns, 52w gap, 50dma, turnover) — one window-SQL pass
# ---------------------------------------------------------------------------


def _insert_series(conn, code: str, closes: list[float], *, start: date, value: float = 1000.0) -> None:
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, high, adj_factor, volume, value) VALUES (?, ?, ?, ?, 1.0, 100, ?)",
        [(code, start + timedelta(days=i), close, close, value) for i, close in enumerate(closes)],
    )


def test_screen_ret_windows_and_high_52w_gap_and_above_ma50(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    start = _AS_OF - timedelta(days=252)
    # Flat 100 for 252 bars, then the 253rd (as_of) bar jumps to 150 — exactly one return window.
    closes = [100.0] * 252 + [150.0]
    _insert_series(conn, "900010", closes, start=start)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    row = payload["rows"][0]
    assert row["ret_3m"] == pytest.approx(50.0)
    assert row["ret_6m"] == pytest.approx(50.0)
    assert row["ret_12m"] == pytest.approx(50.0)
    assert row["high_52w_gap"] == pytest.approx(50.0)  # prior high is 100, now 150
    assert row["above_ma50"] == 1


def test_screen_value_20d_is_the_trailing_average_turnover(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    start = _AS_OF - timedelta(days=19)
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor, volume, value) VALUES (?, ?, 100.0, 1.0, 100, ?)",
        [("900010", start + timedelta(days=i), float(i + 1) * 1000.0) for i in range(20)],
    )
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    # Average of 1000..20000 in steps of 1000 is 10500.
    assert payload["rows"][0]["value_20d"] == pytest.approx(10500.0)


def test_screen_above_ma50_is_null_without_50_days_of_data(cache) -> None:
    conn = store.open_store()
    _insert_company(conn, "900010")
    _insert_close(conn, "900010", 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    assert payload["rows"][0]["above_ma50"] is None


def test_screen_rs_1m_is_ranked_against_the_full_universe_not_the_row_filter(cache) -> None:
    conn = store.open_store()
    start = _AS_OF - timedelta(days=21)
    for code, market, ret in (("900010", "KOSPI", 0.30), ("900020", "KOSDAQ", 0.10), ("900030", "KOSDAQ", -0.10)):
        _insert_company(conn, code, market=market)
        _insert_series(conn, code, [100.0] * 21 + [100.0 * (1 + ret)], start=start)
    conn.close()

    conn = store.open_store(read_only=True)
    full = screen.screen(conn, _AS_OF)
    narrowed = screen.screen(conn, _AS_OF, market="KOSDAQ")
    conn.close()

    full_rs = {row["code"]: row["rs_1m"] for row in full["rows"]}
    narrowed_rs = {row["code"]: row["rs_1m"] for row in narrowed["rows"]}
    assert full_rs["900020"] == narrowed_rs["900020"]
    assert full_rs["900020"] != 99  # best is 900010, excluded from the KOSDAQ view but still ranked


# ---------------------------------------------------------------------------
# --where filtering + dropped_null + sort + top
# ---------------------------------------------------------------------------


def test_screen_where_filters_rows_and_counts_dropped_null(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010")  # roe computable
    _insert_company(conn, "900020")  # no financials at all -> roe null
    _insert_close(conn, "900020", 100.0)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF, where=screen.parse_where("roe>5"))
    conn.close()

    assert [row["code"] for row in payload["rows"]] == ["900010"]
    assert payload["dropped_null"] == {"roe": 1}


def test_screen_sort_defaults_to_code_without_sort(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900020")
    _setup_candidate(conn, "900010")
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF)
    conn.close()

    assert [row["code"] for row in payload["rows"]] == ["900010", "900020"]


def test_screen_sort_by_factor_descending_nulls_last(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010")  # roe computes from _BASELINE_ACCOUNTS
    _insert_company(conn, "900020")
    _insert_close(conn, "900020", 100.0)  # no financials -> roe null
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF, sort="roe")
    conn.close()

    assert payload["rows"][0]["code"] == "900010"
    assert payload["rows"][-1]["code"] == "900020"
    assert payload["rows"][-1]["roe"] is None


def test_screen_top_trims_rows_not_population(cache) -> None:
    conn = store.open_store()
    for code in ("900010", "900020", "900030"):
        _setup_candidate(conn, code)
    conn.close()

    conn = store.open_store(read_only=True)
    payload = screen.screen(conn, _AS_OF, top=1)
    conn.close()

    assert payload["matched"] == 3
    assert payload["count"] == 1
    assert len(payload["rows"]) == 1


# ---------------------------------------------------------------------------
# CLI wiring: options, --factors, --preset
# ---------------------------------------------------------------------------


def test_cli_screen_reads_the_cache(cache) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010")
    _insert_index_bar(conn)
    conn.close()

    result = run_cli(["cache", "screen", "--as-of", _AS_OF.strftime("%Y%m%d"), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["rows"][0]["code"] == "900010"


def test_cli_screen_factors_true_is_offline(cache) -> None:
    result = run_cli(["cache", "screen", "--factors", "true", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert {entry["factor"] for entry in payload["factors"]} >= {"per", "roe", "rs_1m"}


def test_cli_screen_rejects_unknown_where_factor(cache) -> None:
    result = run_cli(["cache", "screen", "--where", "nope>1", "--json"])
    assert result.exit_code == 2


def test_cli_screen_rejects_unknown_sort_factor(cache) -> None:
    result = run_cli(["cache", "screen", "--sort", "nope", "--json"])
    assert result.exit_code == 2


def test_cli_screen_rejects_where_and_preset_together(cache) -> None:
    result = run_cli(["cache", "screen", "--where", "per<10", "--preset", "my-quality", "--json"])
    assert result.exit_code == 2


def test_cli_screen_preset_missing_file_is_usage_error(cache, monkeypatch, tmp_path) -> None:
    monkeypatch.delenv(review_paths.RESEARCH_DIR_ENV, raising=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".git").mkdir()

    result = run_cli(["cache", "screen", "--preset", "my-quality", "--json"])
    assert result.exit_code == 2


def test_cli_screen_preset_reads_research_screens_toml(cache, monkeypatch, tmp_path) -> None:
    conn = store.open_store()
    _setup_candidate(conn, "900010")
    _insert_index_bar(conn)
    conn.close()

    research = tmp_path / "research"
    research.mkdir()
    (research / "screens.toml").write_text('[my-quality]\nwhere = "roe>5"\nsort = "roe"\n', encoding="utf-8")
    monkeypatch.setenv(review_paths.RESEARCH_DIR_ENV, str(research))

    result = run_cli(["cache", "screen", "--as-of", _AS_OF.strftime("%Y%m%d"), "--preset", "my-quality", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["rows"][0]["code"] == "900010"
    assert payload["sort"] == "roe"


def test_cli_screen_preset_unknown_name_lists_available(cache, monkeypatch, tmp_path) -> None:
    research = tmp_path / "research"
    research.mkdir()
    (research / "screens.toml").write_text('[my-quality]\nwhere = "roe>5"\n', encoding="utf-8")
    monkeypatch.setenv(review_paths.RESEARCH_DIR_ENV, str(research))

    result = run_cli(["cache", "screen", "--preset", "no-such-preset", "--json"])
    assert result.exit_code == 2
    payload = json.loads(result.stdout)
    assert payload["error"]["data"]["presets"] == ["my-quality"]
