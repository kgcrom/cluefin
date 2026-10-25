"""`cache perf`: adjusted closes, dates shared with the benchmark, calendar-year CAGR."""

from __future__ import annotations

import json
from datetime import date

import numpy as np
import pytest
from cluefin_ta import PERFORMANCE, PERIODIC_RATE

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.main import run_cli

_DAYS = [date(2018, 5, 2), date(2018, 5, 3), date(2018, 5, 4), date(2018, 5, 8), date(2018, 5, 9)]
# 50:1 split on 05-04: raw closes jump down, adjusted closes are 52000, 53000, 51900, 52500, 53500.
_STOCK = [
    (2600000.0, 0.02),
    (2650000.0, 0.02),
    (51900.0, 1.0),
    (52500.0, 1.0),
    (53500.0, 1.0),
]
_KOSPI = [2500.0, 2480.0, 2460.0, 2470.0, 2490.0]


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, ?)",
        [("005930", day, close, factor) for day, (close, factor) in zip(_DAYS, _STOCK, strict=True)]
        + [("U0001", day, close, 1.0) for day, close in zip(_DAYS, _KOSPI, strict=True)]
        # KOSDAQ misses 05-08, so a comparison with it drops that day.
        + [("U1001", day, 880.0 + i, 1.0) for i, day in enumerate(_DAYS) if day != date(2018, 5, 8)],
    )
    conn.close()
    return tmp_path


def _json(args):
    result = run_cli([*args, "--json"])
    return result.exit_code, json.loads(result.stdout)


def _perf(*extra: str):
    return _json(["cache", "perf", "--code", "005930", "--since", "20180101", "--until", "20181231", *extra])


def test_perf_matches_performance_on_adjusted_closes(cache) -> None:
    code, payload = _perf("--risk-free", "0.03")

    stock = np.array([close * factor for close, factor in _STOCK])
    kospi = np.array(_KOSPI)
    years = (_DAYS[-1] - _DAYS[0]).days / 365.25
    expected = PERFORMANCE(stock, benchmark=kospi, risk_free=PERIODIC_RATE(0.03), years=years)
    assert code == 0
    assert payload["benchmark"] == "U0001" and payload["count"] == 5
    assert (payload["first"], payload["last"]) == ("2018-05-02", "2018-05-09")
    assert payload["performance"].keys() == expected.keys()
    for name, value in expected.items():
        assert payload["performance"][name] == pytest.approx(value, abs=1e-4), name
    assert payload["benchmark_performance"]["cagr"] == pytest.approx(PERFORMANCE(kospi, years=years)["cagr"], abs=1e-4)
    assert "beta" not in payload["benchmark_performance"]


def test_perf_keeps_only_dates_both_codes_have(cache) -> None:
    _, payload = _perf("--bench", "u1001")

    assert payload["benchmark"] == "U1001" and payload["count"] == 4


def test_perf_without_shared_bars_hints(cache) -> None:
    _, payload = _perf("--bench", "U2001")

    assert payload["count"] == 0 and payload["performance"] is None and "hint" in payload


def test_perf_rejects_percent_risk_free_and_missing_code(cache) -> None:
    assert _perf("--risk-free", "3.5")[0] == 2
    assert _perf("--risk-free", "abc")[0] == 2
    assert run_cli(["cache", "perf", "--json"]).exit_code == 2
