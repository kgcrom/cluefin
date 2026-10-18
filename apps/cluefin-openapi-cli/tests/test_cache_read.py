"""`cache ohlcv` / `cache company`: adjusted view, default window, point-in-time universe."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.main import run_cli


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO company (code, name, market, listed_on, delisted_on) VALUES (?, ?, ?, ?, ?)",
        [
            ("005930", "삼성전자", "KOSPI", date(1975, 6, 11), None),
            ("117930", "한진해운", "KOSPI", date(2009, 12, 10), date(2017, 3, 7)),
            ("035720", "카카오", "KOSDAQ", date(2017, 7, 10), None),
        ],
    )
    conn.executemany(
        "INSERT INTO ohlcv (code, date, open, high, low, close, volume, adj_factor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("005930", date(2018, 5, 3), 2650000.0, 2650000.0, 2650000.0, 2650000.0, 10.0, 0.02),
            ("005930", date(2018, 5, 4), 53000.0, 53900.0, 51800.0, 51900.0, 500.0, 1.0),
        ],
    )
    conn.close()
    return tmp_path


def _json(args):
    result = run_cli([*args, "--json"])
    return result.exit_code, json.loads(result.stdout)


def test_ohlcv_unadjusted_by_default(cache) -> None:
    code, payload = _json(["cache", "ohlcv", "--code", "005930", "--since", "20180101", "--until", "20181231"])

    assert code == 0
    assert payload["adjusted"] is False
    assert [bar["close"] for bar in payload["bars"]] == [2650000.0, 51900.0]


def test_ohlcv_adjusted_scales_prices_and_volume(cache) -> None:
    _, payload = _json(
        ["cache", "ohlcv", "--code", "005930", "--since", "20180101", "--until", "20181231", "--adjusted", "true"]
    )

    first = payload["bars"][0]
    assert first["close"] == pytest.approx(53000.0) and first["volume"] == pytest.approx(500.0)


def test_ohlcv_default_window_is_a_year_back_from_until(cache) -> None:
    _, payload = _json(["cache", "ohlcv", "--code", "005930", "--until", "20180601"])

    assert payload["since"] == (date(2018, 6, 1) - timedelta(days=365)).isoformat()
    assert payload["count"] == 2


def test_ohlcv_empty_range_hints(cache) -> None:
    _, payload = _json(["cache", "ohlcv", "--code", "000000", "--since", "20180101", "--until", "20181231"])

    assert payload["count"] == 0 and "hint" in payload


def test_ohlcv_requires_code_and_valid_bool(cache) -> None:
    assert run_cli(["cache", "ohlcv", "--json"]).exit_code == 2
    assert run_cli(["cache", "ohlcv", "--code", "005930", "--adjusted", "maybe", "--json"]).exit_code == 2


def test_company_lists_listed_only_by_default(cache) -> None:
    _, payload = _json(["cache", "company"])

    assert [row["code"] for row in payload["companies"]] == ["005930", "035720"]


def test_company_as_of_is_point_in_time(cache) -> None:
    _, in_2016 = _json(["cache", "company", "--as-of", "20160104"])
    _, in_2018 = _json(["cache", "company", "--as-of", "20180102"])

    assert [row["code"] for row in in_2016["companies"]] == ["005930", "117930"]  # 카카오 not yet, 한진해운 still
    assert [row["code"] for row in in_2018["companies"]] == ["005930", "035720"]


def test_company_by_code_includes_delisted(cache) -> None:
    _, payload = _json(["cache", "company", "--code", "117930"])

    assert payload["companies"][0]["delisted_on"] == "2017-03-07"


def test_company_market_filter_and_limit(cache) -> None:
    _, kosdaq = _json(["cache", "company", "--market", "kosdaq"])
    _, limited = _json(["cache", "company", "--include-delisted", "true", "--limit", "1"])

    assert [row["code"] for row in kosdaq["companies"]] == ["035720"]
    assert limited["_truncated"]["paths"][0]["total"] == 3
