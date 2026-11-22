"""`cache screen`'s TTM / latest-quarter factors (cache/screen_ttm.py)."""

from __future__ import annotations

from datetime import date

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.screen_ttm import latest_due_period, ttm_by_code, ttm_factors


def _ttm(conn, rows) -> None:
    conn.executemany(
        "INSERT INTO financials_ttm (code, year, quarter, account_nm, quarter_amount, ttm_amount, basis) "
        "VALUES ('005930', ?, ?, ?, ?, ?, 'CFS')",
        rows,
    )


def test_latest_due_period_follows_deadlines() -> None:
    assert latest_due_period(date(2026, 11, 22)) == (2026, 3)
    assert latest_due_period(date(2026, 11, 13)) == (2026, 2)
    assert latest_due_period(date(2026, 4, 1)) == (2025, 4)
    assert latest_due_period(date(2026, 3, 30)) == (2025, 3)


def test_factors_use_latest_due_quarter_and_same_quarter_last_year() -> None:
    conn = store.open_store(":memory:")
    _ttm(
        conn,
        [
            ("2026", 3, "매출액", 195.0, 594.0),
            ("2026", 3, "영업이익", 107.0, 274.0),
            ("2026", 3, "당기순이익", 75.0, 214.0),
            ("2026", 3, "자본총계", 500.0, 500.0),
            ("2025", 3, "매출액", 86.0, 300.0),
            ("2025", 3, "영업이익", 12.0, 30.0),
        ],
    )

    entry = ttm_by_code(conn, ["005930"], date(2026, 11, 22))["005930"]
    factors = ttm_factors(entry, 1000.0)

    assert factors["ttm_period"] == "2026Q3"
    assert factors["per_ttm"] == round(1000 / 214, 2)
    assert factors["psr_ttm"] == round(1000 / 594, 2)
    assert factors["pbr_mrq"] == 2.0
    assert factors["roe_ttm"] == round(214 / 500 * 100, 2)
    assert factors["opm_ttm"] == round(274 / 594 * 100, 2)
    assert factors["revenue_yoy_q"] == round((195 / 86 - 1) * 100, 2)
    assert factors["op_yoy_q"] == round((107 / 12 - 1) * 100, 2)


def test_quarter_not_yet_due_is_not_used() -> None:
    conn = store.open_store(":memory:")
    _ttm(conn, [("2026", 3, "매출액", 195.0, 594.0), ("2026", 2, "매출액", 171.0, 480.0)])

    entry = ttm_by_code(conn, ["005930"], date(2026, 11, 13))["005930"]

    assert ttm_factors(entry, None)["ttm_period"] == "2026Q2"


def test_no_quarters_gives_nulls() -> None:
    factors = ttm_factors(None, 1000.0)
    assert set(factors.values()) == {None}
