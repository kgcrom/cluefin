"""`cache financials --period quarter|ttm` reads `financials_ttm`; `cache status` counts quarters."""

from __future__ import annotations

import json
from datetime import datetime

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.financials_ttm import rebuild_ttm
from cluefin_openapi_cli.cache.read import read_financials
from cluefin_openapi_cli.main import run_cli

_TS = datetime(2026, 1, 1)


def _seed(conn) -> None:
    conn.execute(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at) "
        "VALUES ('005930', '2025', '11011', 'CFS', '매출액', 333.0, 'KRW', ?)",
        [_TS],
    )
    conn.executemany(
        "INSERT INTO financials_quarterly (code, year, quarter, reprt_code, basis, account_nm, amount, cum_amount, "
        "prior_cum_amount, currency, loaded_at) VALUES ('005930', ?, ?, ?, 'CFS', '매출액', ?, ?, ?, 'KRW', ?)",
        [
            ("2025", 3, "11014", 86.0, 239.0, None, _TS),
            ("2026", 3, "11014", 195.0, 500.0, 239.0, _TS),
        ],
    )
    rebuild_ttm(conn)


def test_quarter_and_ttm_newest_first() -> None:
    conn = store.open_store(":memory:")
    _seed(conn)

    quarter = read_financials(conn, "005930", period="quarter")
    ttm = read_financials(conn, "005930", period="ttm")

    assert [row["period"] for row in quarter["periods"]] == ["2026Q3", "2025Q4", "2025Q3"]
    assert quarter["periods"][1]["accounts"] == {"매출액": 333.0 - 239.0}
    assert ttm["periods"][0]["accounts"] == {"매출액": 500.0 + 333.0 - 239.0}
    assert ttm["periods"][1]["accounts"] == {"매출액": 333.0}
    assert ttm["period"] == "ttm"
    assert ttm["notes"]


def test_annual_default_is_unchanged() -> None:
    conn = store.open_store(":memory:")
    _seed(conn)

    payload = read_financials(conn, "005930")

    assert [row["year"] for row in payload["years"]] == ["2025"]


def test_cli_period_flag_and_bad_value(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    _seed(conn)
    conn.execute(
        "INSERT INTO financials_quarterly_fetch_log VALUES ('005930', '2026', 3, 'ok', ?)",
        [_TS],
    )
    conn.close()

    result = run_cli(["cache", "financials", "--code", "005930", "--period", "ttm", "--json"])
    assert result.exit_code == 0, result.stdout
    assert json.loads(result.stdout)["periods"][0]["period"] == "2026Q3"

    bad = run_cli(["cache", "financials", "--code", "005930", "--period", "monthly", "--json"])
    assert bad.exit_code == 2

    status = json.loads(run_cli(["cache", "status", "--json"]).stdout)
    assert status["financials_quarterly"]["last_period"] == "2026Q3"
    assert status["financials_quarterly"]["fetch_log"] == {"ok": 1}
