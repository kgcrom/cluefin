"""`cache load --only financials_quarterly` and the `financials_ttm` rebuild."""

from __future__ import annotations

from datetime import date, datetime
from types import SimpleNamespace

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.financials import ACCOUNT_ALIASES
from cluefin_openapi_cli.cache.financials_quarterly import (
    QUARTER_REPORT_CODES,
    default_quarters,
    load_financials_quarterly,
    quarter_due,
)
from cluefin_openapi_cli.cache.financials_ttm import _REBUILD_SQL, FLOW_ACCOUNTS, rebuild_ttm


def _item(code: str, account_nm: str, amount: str, cum: str | None = None, prior: str | None = None, fs_div="CFS"):
    return SimpleNamespace(
        stock_code=code,
        fs_div=fs_div,
        account_nm=account_nm,
        thstrm_amount=amount,
        thstrm_add_amount=cum,
        frmtrm_add_amount=prior,
        currency="KRW",
    )


def _result(status: str, items: list | None):
    return SimpleNamespace(result=SimpleNamespace(status=status, message="", list=items))


class FakeDart:
    def __init__(self, by_period: dict[tuple[str, str], object]) -> None:
        self.by_period = by_period
        self.calls: list[tuple[str, str, str]] = []
        self.periodic_report_financial_statement = self

    def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
        self.calls.append((corp_code, bsns_year, reprt_code))
        return self.by_period.get((bsns_year, reprt_code), _result("013", None))


def _conn(pairs: list[tuple[str, str]]):
    conn = store.open_store(":memory:")
    conn.executemany("INSERT INTO company (code, name, corp_code) VALUES (?, 'X', ?)", pairs)
    return conn


def _annual(conn, code: str, year: str, account_nm: str, amount: float, basis: str = "CFS") -> None:
    conn.execute(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at) "
        "VALUES (?, ?, '11011', ?, ?, ?, 'KRW', ?)",
        [code, year, basis, account_nm, amount, datetime(2026, 1, 1)],
    )


def test_default_quarters_only_past_deadlines() -> None:
    quarters = default_quarters(date(2026, 11, 22))
    assert quarters[0] == ("2022", 1)
    assert quarters[-1] == ("2026", 3)
    assert len(quarters) == 15
    assert ("2026", 3) not in default_quarters(date(2026, 11, 13))
    assert quarter_due(2025, 4) == date(2026, 3, 31)


def test_loads_three_month_cumulative_and_prior_cumulative() -> None:
    conn = _conn([("005930", "00126380")])
    dart = FakeDart(
        {
            ("2026", "11014"): _result(
                "000",
                [
                    _item("005930", "매출액", "195", "500", "239"),
                    _item("005930", "자산총계", "791"),
                ],
            )
        }
    )

    stats = load_financials_quarterly(conn, dart=dart, today=date(2026, 11, 22), quarters=(("2026", 3),))

    assert stats.calls == 1
    assert stats.codes_ok == 1
    rows = conn.execute(
        "SELECT account_nm, quarter, reprt_code, amount, cum_amount, prior_cum_amount FROM financials_quarterly "
        "ORDER BY account_nm"
    ).fetchall()
    assert rows == [
        ("매출액", 3, QUARTER_REPORT_CODES[3], 195.0, 500.0, 239.0),
        ("자산총계", 3, QUARTER_REPORT_CODES[3], 791.0, None, None),
    ]
    assert conn.execute("SELECT status FROM financials_quarterly_fetch_log").fetchall() == [("ok",)]


def test_empty_is_retried_only_while_the_quarter_is_recent() -> None:
    conn = _conn([("005930", "00126380")])
    dart = FakeDart({})

    load_financials_quarterly(conn, dart=dart, today=date(2026, 11, 22), quarters=(("2026", 3), ("2023", 3)))
    assert len(dart.calls) == 2
    dart.calls.clear()

    load_financials_quarterly(conn, dart=dart, today=date(2026, 11, 22), quarters=(("2026", 3), ("2023", 3)))
    assert [call[1] for call in dart.calls] == ["2026"]


def test_quota_stops_and_leaves_the_rest_unlogged() -> None:
    conn = _conn([("005930", "00126380")])
    dart = FakeDart({("2025", "11013"): _result("020", None)})

    stats = load_financials_quarterly(conn, dart=dart, today=date(2026, 11, 22), quarters=(("2025", 1), ("2025", 2)))

    assert stats.quota_exhausted is True
    assert len(dart.calls) == 1
    assert conn.execute("SELECT count(*) FROM financials_quarterly_fetch_log").fetchone() == (0,)


def _quarter(conn, code, year, quarter, account_nm, amount, cum=None, prior=None, basis="CFS") -> None:
    conn.execute(
        "INSERT INTO financials_quarterly (code, year, quarter, reprt_code, basis, account_nm, amount, cum_amount, "
        "prior_cum_amount, currency, loaded_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'KRW', ?)",
        [
            code,
            year,
            quarter,
            QUARTER_REPORT_CODES[quarter],
            basis,
            account_nm,
            amount,
            cum,
            prior,
            datetime(2026, 1, 1),
        ],
    )


def _ttm(conn, year: str, quarter: int, account_nm: str):
    return conn.execute(
        "SELECT quarter_amount, ttm_amount FROM financials_ttm WHERE code = '005930' AND year = ? AND quarter = ? "
        "AND account_nm = ?",
        [year, quarter, account_nm],
    ).fetchone()


def test_ttm_from_cumulative_prior_annual_and_comparative() -> None:
    conn = store.open_store(":memory:")
    _annual(conn, "005930", "2025", "매출액", 333.0)
    _quarter(conn, "005930", "2026", 3, "매출액", 195.0, cum=500.0, prior=239.0)
    _quarter(conn, "005930", "2026", 3, "자산총계", 791.0)

    rebuild_ttm(conn)

    assert _ttm(conn, "2026", 3, "매출액") == (195.0, 500.0 + 333.0 - 239.0)
    assert _ttm(conn, "2026", 3, "자산총계") == (791.0, 791.0)


def test_ttm_falls_back_to_prior_year_quarterly_and_folds_aliases() -> None:
    conn = store.open_store(":memory:")
    _annual(conn, "005930", "2025", "당기순이익(손실)", 45.0)
    _quarter(conn, "005930", "2025", 2, "당기순이익(손실)", 5.0, cum=13.0)
    _quarter(conn, "005930", "2026", 2, "당기순이익(손실)", 71.0, cum=118.0)

    rebuild_ttm(conn)

    assert _ttm(conn, "2026", 2, "당기순이익") == (71.0, 118.0 + 45.0 - 13.0)


def test_fourth_quarter_is_annual_minus_third_quarter_cumulative() -> None:
    conn = store.open_store(":memory:")
    _annual(conn, "005930", "2025", "영업이익", 43.0)
    _annual(conn, "005930", "2025", "자본총계", 400.0)
    _quarter(conn, "005930", "2025", 3, "영업이익", 12.0, cum=23.0)

    rebuild_ttm(conn)

    assert _ttm(conn, "2025", 4, "영업이익") == (20.0, 43.0)
    assert _ttm(conn, "2025", 4, "자본총계") == (400.0, 400.0)


def test_mixed_basis_gives_null_ttm() -> None:
    conn = store.open_store(":memory:")
    _annual(conn, "005930", "2025", "매출액", 333.0, basis="OFS")
    _quarter(conn, "005930", "2026", 3, "매출액", 195.0, cum=500.0, prior=239.0)

    rebuild_ttm(conn)

    assert _ttm(conn, "2026", 3, "매출액") == (195.0, None)


def test_static_rebuild_sql_matches_aliases_and_flow_accounts() -> None:
    for alias, canonical in ACCOUNT_ALIASES.items():
        assert f"WHEN '{alias}' THEN '{canonical}'" in _REBUILD_SQL
    flows = ", ".join(f"'{name}'" for name in FLOW_ACCOUNTS)
    assert _REBUILD_SQL.count(f"IN ({flows})") == 2


def test_non_standard_flow_line_gets_a_real_ttm() -> None:
    conn = store.open_store(":memory:")
    _annual(conn, "005930", "2025", "법인세차감전 순이익", 60.0)
    _quarter(conn, "005930", "2025", 3, "법인세차감전 순이익", 15.0, cum=40.0)
    _quarter(conn, "005930", "2026", 3, "법인세차감전 순이익", 30.0, cum=90.0, prior=40.0)

    rebuild_ttm(conn)

    assert _ttm(conn, "2026", 3, "법인세차감전 순이익") == (30.0, 90.0 + 60.0 - 40.0)
    assert _ttm(conn, "2025", 4, "법인세차감전 순이익") == (20.0, 60.0)
