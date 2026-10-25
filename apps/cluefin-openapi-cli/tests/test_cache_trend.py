"""`cache trend-setup`: same verdict as `trend_setup.analyze`, backtest universe, filters and order."""

from __future__ import annotations

import json
from datetime import date, datetime

import pytest
from test_trend_setup import index_of, load, prices_of

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.main import run_cli

_AS_OF = "20261006"


def _day(raw: str) -> date:
    return datetime.strptime(raw, "%Y%m%d").date()


def _bars(code: str, candles: list[dict], *, scale: float = 1.0) -> list[tuple]:
    """Raw prices = adjusted ÷ scale, stored with adj_factor = scale (so adjusted is unchanged)."""

    return [
        (
            code,
            _day(c["date"]),
            c["open"] / scale,
            c["high"] / scale,
            c["low"] / scale,
            c["close"] / scale,
            c["volume"] * scale,
            c["value"],
            scale,
        )
        for c in candles
    ]


# code, fixture, market, name, listed_on, delisted_on, candles slice
_STOCKS = [
    ("000010", "stock-e", "KOSPI", "알파", None, None, slice(None)),  # alert/setup
    ("000020", "stock-d", "KOSDAQ", "베타", None, None, slice(None)),  # overheated
    ("000030", "stock-a", "KOSPI", "감마", None, None, slice(None)),  # no_group
    ("000040", "stock-f", "KOSPI", "델타", None, date(2026, 10, 20), slice(None)),  # delisted later: kept
    ("000015", "stock-e", "KOSPI", "알파우", None, None, slice(None)),  # preferred
    ("000050", "stock-e", "KOSPI", "테스트스팩1호", None, None, slice(None)),  # SPAC
    ("000060", "stock-e", "KOSPI", "신규", date(2026, 10, 7), None, slice(None)),  # listed after as_of
    ("000070", "stock-e", "KOSPI", "정지", None, None, slice(None, -1)),  # no bar on as_of
    ("000080", "stock-e", "KOSPI", "신생", None, None, slice(-200, None)),  # too short
]


@pytest.fixture(scope="module")
def cache_dir(tmp_path_factory):
    """Built once: ~3,500 bars through executemany take seconds, and every test only reads."""

    path = tmp_path_factory.mktemp("trend")
    conn = store.open_store(path / "market.duckdb")
    conn.executemany(
        "INSERT INTO company (code, name, market, listed_on, delisted_on) VALUES (?, ?, ?, ?, ?)",
        [(code, name, market, listed, delisted) for code, _, market, name, listed, delisted, _ in _STOCKS]
        + [("000090", "엡실론", "KOSPI", None, None)],
    )
    rows = [bar for code, fixture, *_, cut in _STOCKS for bar in _bars(code, load(fixture)["candles"][cut])]
    rows += _bars("000090", load("stock-e")["candles"], scale=0.5)  # same adjusted prices, split-like raw
    for code, name in (("U0001", "index-0001"), ("U1001", "index-1001")):
        rows += [(code, _day(r["date"]), None, None, None, r["close"], None, None, 1.0) for r in load(name)["closes"]]
    conn.executemany(
        "INSERT INTO ohlcv (code, date, open, high, low, close, volume, value, adj_factor) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.close()
    return path


@pytest.fixture
def cache(cache_dir, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(cache_dir))
    return cache_dir


def _scan(*extra: str) -> tuple[int, dict]:
    result = run_cli(["cache", "trend-setup", "--as-of", _AS_OF, *extra, "--json"])
    return result.exit_code, json.loads(result.stdout)


def _rows(*extra: str) -> dict[str, dict]:
    return {row["code"]: row for row in _scan("--include-excluded", "true", *extra)[1]["rows"]}


@pytest.mark.parametrize(
    ("code", "fixture"), [("000010", "stock-e"), ("000020", "stock-d"), ("000030", "stock-a"), ("000040", "stock-f")]
)
def test_rows_match_analyze_on_the_same_bars(cache, code: str, fixture: str) -> None:
    reading = trend_setup.analyze(prices_of(fixture).window(start=-260), index_of(load(fixture)["market"]))

    row = _rows()[code]

    assert (row["action"], row["status"], row["groups"]) == (
        reading["setup"]["action"],
        reading["setup"]["status"],
        reading["setup"]["groups"],
    )
    assert row["pivot"] == (reading["pivot"] or {}).get("price")
    assert row["rel"] == reading["strength"]["rel"]


def test_adjusted_prices_are_used(cache) -> None:
    rows = _rows()

    assert rows["000090"]["status"] == rows["000010"]["status"] == "setup"
    assert rows["000090"]["pivot"] == pytest.approx(rows["000010"]["pivot"])


def test_universe_is_the_backtest_one(cache) -> None:
    code, payload = _scan("--include-excluded", "true")
    codes = {row["code"] for row in payload["rows"]}

    assert code == 0
    assert codes == {"000010", "000020", "000030", "000040", "000090"}  # no preferred, SPAC, later listing
    assert payload["universe"] == 7
    assert payload["summary"]["skipped"] == {"no_bar": 1, "insufficient_history": 1}


def test_default_rows_leave_out_excludes_but_count_them(cache) -> None:
    _, payload = _scan()
    counted = sum(value for key, value in payload["summary"].items() if key != "skipped")

    assert {row["action"] for row in payload["rows"]} <= {"alert", "watch"}
    assert counted == payload["universe"] - sum(payload["summary"]["skipped"].values())
    assert payload["summary"]["exclude/overheated"] == 1


def test_status_filter_takes_actions_or_action_status(cache) -> None:
    _, alerts = _scan("--status", "alert")
    _, hot = _scan("--status", "exclude/overheated")

    # 000040 closes on its pivot (0%), the other two sit 7.5% below; ties keep universe order.
    assert [row["code"] for row in alerts["rows"]] == ["000040", "000010", "000090"]
    assert [row["code"] for row in hot["rows"]] == ["000020"]


def test_rows_sorted_actionable_first(cache) -> None:
    statuses = [f"{row['action']}/{row['status']}" for row in _scan("--include-excluded", "true")[1]["rows"]]

    assert statuses.index("alert/setup") < statuses.index("exclude/overheated") < statuses.index("exclude/no_group")


def test_rows_carry_failed_check_ids(cache) -> None:
    assert "g3.rel_band" in _rows()["000030"]["failed"]


def test_holiday_as_of_is_exit_2_with_the_previous_day(cache) -> None:
    result = run_cli(["cache", "trend-setup", "--as-of", "20261004", "--json"])

    assert result.exit_code == 2
    assert "20261002" in json.loads(result.stdout)["error"]["hint"]


def test_default_as_of_is_the_last_index_day(cache) -> None:
    result = run_cli(["cache", "trend-setup", "--json"])

    assert json.loads(result.stdout)["as_of"] == _AS_OF


def test_market_and_code_filters(cache) -> None:
    assert set(_rows("--market", "kosdaq")) == {"000020"}
    assert set(_rows("--code", "000010,000030")) == {"000010", "000030"}
