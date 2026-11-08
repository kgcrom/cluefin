"""`cache macro-beta`: weekly OLS of a stock's return on KOSPI, USD/KRW and KTB 3Y/10Y, from synthetic data."""

from __future__ import annotations

import json
from datetime import date, timedelta

import numpy as np
import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.macro_beta import read_macro_beta
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.main import run_cli

_ALPHA = 0.0015
_BETA_MARKET = 1.2
_BETA_FX = -0.35
_BETA_RATE3 = -0.0015
_BETA_RATE10 = 0.0009
_N_RETURNS = 60  # weeks of returns; needs N+1 weekly levels


def _synthetic_weeks() -> list[date]:
    start = date(2024, 1, 1)  # a Monday
    return [start + timedelta(weeks=i) for i in range(_N_RETURNS + 1)]


def _build_series(rng: np.random.Generator, *, drift: float, scale: float, start: float) -> np.ndarray:
    """Weekly fractional changes (for a stock/FX-style level) with no serial structure."""

    changes = rng.normal(drift, scale, size=_N_RETURNS)
    levels = [start]
    for change in changes:
        levels.append(levels[-1] * (1 + change))
    return np.array(levels), changes


def _build_rate(rng: np.random.Generator, *, start: float, scale_bp: float) -> tuple[np.ndarray, np.ndarray]:
    """Weekly levels (annual percent) whose week-over-week change in bp is returned alongside."""

    bp_changes = rng.normal(0.0, scale_bp, size=_N_RETURNS)
    levels = [start]
    for bp in bp_changes:
        levels.append(levels[-1] + bp / 100)
    return np.array(levels), bp_changes


@pytest.fixture
def synthetic_cache(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    rng = np.random.default_rng(20261104)
    weeks = _synthetic_weeks()

    market_levels, market_ret = _build_series(rng, drift=0.0005, scale=0.015, start=2500.0)
    fx_levels, fx_chg = _build_series(rng, drift=0.0, scale=0.006, start=1350.0)
    rate3_levels, rate3_bp = _build_rate(rng, start=3.2, scale_bp=4.0)
    rate10_levels, rate10_bp = _build_rate(rng, start=3.6, scale_bp=4.5)

    noise = rng.normal(0.0, 0.0003, size=_N_RETURNS)
    stock_ret = (
        _ALPHA
        + _BETA_MARKET * market_ret
        + _BETA_FX * fx_chg
        + _BETA_RATE3 * rate3_bp
        + _BETA_RATE10 * rate10_bp
        + noise
    )
    stock_levels = [10000.0]
    for ret in stock_ret:
        stock_levels.append(stock_levels[-1] * (1 + ret))
    stock_levels = np.array(stock_levels)

    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [("005930", day, price) for day, price in zip(weeks, stock_levels, strict=True)]
        + [("U0001", day, price) for day, price in zip(weeks, market_levels, strict=True)],
    )
    conn.executemany(
        "INSERT INTO rates (series, date, value) VALUES (?, ?, ?)",
        [("usdkrw", day, value) for day, value in zip(weeks, fx_levels, strict=True)]
        + [("ktb3y", day, value) for day, value in zip(weeks, rate3_levels, strict=True)]
        + [("ktb10y", day, value) for day, value in zip(weeks, rate10_levels, strict=True)],
    )
    conn.close()
    return tmp_path, weeks


def test_regression_recovers_known_coefficients(synthetic_cache) -> None:
    tmp_path, weeks = synthetic_cache
    conn = store.open_store(store.cache_path(), read_only=True)
    try:
        payload = read_macro_beta(conn, "005930", since=weeks[0], until=weeks[-1])
    finally:
        conn.close()

    assert payload["weeks"] == _N_RETURNS
    assert payload["r_squared"] is not None
    assert payload["r_squared"] > 0.95

    coefficients = payload["coefficients"]
    assert coefficients["intercept"]["beta"] == pytest.approx(_ALPHA, abs=0.002)
    assert coefficients["market"]["beta"] == pytest.approx(_BETA_MARKET, abs=0.15)
    assert coefficients["fx"]["beta"] == pytest.approx(_BETA_FX, abs=0.15)
    assert coefficients["rate_3y_bp"]["beta"] == pytest.approx(_BETA_RATE3, abs=0.0015)
    assert coefficients["rate_10y_bp"]["beta"] == pytest.approx(_BETA_RATE10, abs=0.0015)
    # The dominant factor (market) should show a large, clearly-signed t-value against pure noise.
    assert coefficients["market"]["t"] is not None
    assert coefficients["market"]["t"] > 5


def test_too_few_weeks_is_null_regression_with_a_hint(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    days = [date(2024, 1, 1) + timedelta(weeks=i) for i in range(5)]
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [("005930", day, 100.0 + i) for i, day in enumerate(days)]
        + [("U0001", day, 2500.0 + i) for i, day in enumerate(days)],
    )
    conn.executemany(
        "INSERT INTO rates (series, date, value) VALUES (?, ?, ?)",
        [("usdkrw", day, 1350.0 + i) for i, day in enumerate(days)]
        + [("ktb3y", day, 3.2) for day in days]
        + [("ktb10y", day, 3.6) for day in days],
    )
    conn.close()

    conn = store.open_store(store.cache_path(), read_only=True)
    try:
        payload = read_macro_beta(conn, "005930", since=days[0], until=days[-1])
    finally:
        conn.close()

    assert payload["weeks"] < 30
    assert payload["regression"] is None
    assert "hint" in payload


def test_collinear_factors_are_null_betas_with_a_hint(tmp_path, monkeypatch) -> None:
    """Both KTB yields flat for the whole window: their weekly changes are all zero, the design matrix is
    singular, and `np.linalg.inv` used to raise LinAlgError out of the command."""
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    rng = np.random.default_rng(7)
    days = [date(2024, 1, 1) + timedelta(weeks=i) for i in range(40)]
    conn = store.open_store()
    conn.executemany(
        "INSERT INTO ohlcv (code, date, close, adj_factor) VALUES (?, ?, ?, 1.0)",
        [("005930", day, 100.0 + rng.normal()) for day in days]
        + [("U0001", day, 2500.0 + rng.normal() * 10) for day in days],
    )
    conn.executemany(
        "INSERT INTO rates (series, date, value) VALUES (?, ?, ?)",
        [("usdkrw", day, 1350.0 + rng.normal()) for day in days]
        + [("ktb3y", day, 3.2) for day in days]
        + [("ktb10y", day, 3.6) for day in days],
    )
    conn.close()

    conn = store.open_store(store.cache_path(), read_only=True)
    try:
        payload = read_macro_beta(conn, "005930", since=days[0], until=days[-1])
    finally:
        conn.close()

    assert all(c == {"beta": None, "t": None} for c in payload["coefficients"].values())
    assert "collinear" in payload["hint"]
    json.dumps(payload, allow_nan=False)


def test_since_after_until_is_a_usage_error() -> None:
    conn = store.open_store(":memory:")
    try:
        with pytest.raises(CliError, match="--since"):
            read_macro_beta(conn, "005930", since=date(2024, 2, 1), until=date(2024, 1, 1))
    finally:
        conn.close()


def _json(args):
    result = run_cli([*args, "--json"])
    return result.exit_code, json.loads(result.stdout)


def test_cli_wiring_matches_direct_call(synthetic_cache) -> None:
    tmp_path, weeks = synthetic_cache

    code, payload = _json(
        [
            "cache",
            "macro-beta",
            "--code",
            "005930",
            "--since",
            weeks[0].strftime("%Y%m%d"),
            "--until",
            weeks[-1].strftime("%Y%m%d"),
        ]
    )

    assert code == 0
    assert payload["code"] == "005930"
    assert payload["benchmark"] == "U0001"
    assert payload["weeks"] == _N_RETURNS
    assert set(payload["coefficients"]) == {"intercept", "market", "fx", "rate_3y_bp", "rate_10y_bp"}


def test_cli_requires_code() -> None:
    result = run_cli(["cache", "macro-beta", "--json"])

    assert result.exit_code == 2
