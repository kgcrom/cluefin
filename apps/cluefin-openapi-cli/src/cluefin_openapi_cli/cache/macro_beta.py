"""`cache macro-beta`: one stock's weekly-return sensitivity to KOSPI, USD/KRW and KTB yields.

Weekly series come from the last cached observation in each ISO week (DuckDB `date_trunc('week', ...)`,
Monday-anchored) — one value per week per input, not an average. The regression is OLS with an intercept
over the weeks every input has a value for (``weeks`` in the payload is that overlap, which can be smaller
than either series' own span: KOSPI only trades when KRX is open, ECOS rates publish on banking days, and a
long ECOS outage or a thin cache both show up here as fewer weeks, not an error).

Regressors: KOSPI weekly return (fraction), USD/KRW weekly change (fraction), and KTB 3Y/10Y weekly change in
basis points (the `rates` table stores yields as annual percent, so a 0.10 point move is 10bp). Coefficients,
t-values (OLS standard errors from the residual variance) and R² describe the whole window — this is a
diagnostic regression, not a forecast, and nothing here is annualized.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["read_macro_beta"]

_BENCHMARK = "U0001"
_FX_SERIES = "usdkrw"
_RATE_SERIES = ("ktb3y", "ktb10y")
# 5 parameters (intercept + 4 regressors) need more than 5 weeks to fit at all; well under this and the
# t-values are not worth reporting.
_MIN_WEEKS = 30

_WEEKLY_OHLCV_SQL = """
WITH weekly AS (
  SELECT date_trunc('week', date)::DATE AS week, date,
         close * COALESCE(NULLIF(adj_factor, 0), 1) AS price,
         row_number() OVER (PARTITION BY date_trunc('week', date) ORDER BY date DESC) AS rn
  FROM ohlcv
  WHERE code = ? AND date BETWEEN ? AND ? AND close IS NOT NULL
)
SELECT week, price FROM weekly WHERE rn = 1 ORDER BY week
"""

_WEEKLY_RATE_SQL = """
WITH weekly AS (
  SELECT date_trunc('week', date)::DATE AS week, date, value,
         row_number() OVER (PARTITION BY date_trunc('week', date) ORDER BY date DESC) AS rn
  FROM rates
  WHERE series = ? AND date BETWEEN ? AND ?
)
SELECT week, value FROM weekly WHERE rn = 1 ORDER BY week
"""


def _weekly_levels(conn: duckdb.DuckDBPyConnection, sql: str, params: list[Any]) -> dict[date, float]:
    rows = conn.execute(sql, params).fetchall()
    return {week: float(value) for week, value in rows if value is not None}


def _pct_changes(levels: dict[date, float]) -> dict[date, float]:
    weeks = sorted(levels)
    return {
        curr: (levels[curr] - levels[prev]) / levels[prev]
        for prev, curr in zip(weeks, weeks[1:], strict=False)
        if levels[prev]
    }


def _bp_changes(levels: dict[date, float]) -> dict[date, float]:
    """Difference in percentage points × 100, since the stored value is already annual percent."""

    weeks = sorted(levels)
    return {curr: (levels[curr] - levels[prev]) * 100 for prev, curr in zip(weeks, weeks[1:], strict=False)}


def _ols(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Coefficients, their t-values, and R² for ``y = x @ beta``; ``x``'s first column is the intercept."""

    coef, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    residuals = y - x @ coef
    n, k = x.shape
    dof = n - k
    ss_res = float(residuals @ residuals)
    sigma2 = ss_res / dof if dof > 0 else float("nan")
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r_squared = 1 - ss_res / ss_tot if ss_tot else float("nan")
    if np.linalg.matrix_rank(x) < k:
        # Collinear factors (e.g. a rate held flat for the whole window): the betas are not identified,
        # so neither they nor their t-values mean anything. `inv` raised LinAlgError here.
        return np.full(k, np.nan), np.full(k, np.nan), r_squared
    xtx_inv = np.linalg.inv(x.T @ x)
    with np.errstate(invalid="ignore", divide="ignore"):
        se = np.sqrt(sigma2 * np.diag(xtx_inv))
        t_values = coef / se
    return coef, t_values, r_squared


_FACTOR_NAMES = ("intercept", "market", "fx", "rate_3y_bp", "rate_10y_bp")


def read_macro_beta(conn: duckdb.DuckDBPyConnection, code: str, *, since: date, until: date) -> dict[str, Any]:
    """Weekly OLS of ``code``'s return on KOSPI return, USD/KRW change and KTB 3Y/10Y yield change (bp)."""

    if since > until:
        raise CliError("`--since` is after `--until`.", exit_code=EXIT_USAGE)
    stock = _pct_changes(_weekly_levels(conn, _WEEKLY_OHLCV_SQL, [code, since, until]))
    market = _pct_changes(_weekly_levels(conn, _WEEKLY_OHLCV_SQL, [_BENCHMARK, since, until]))
    fx = _pct_changes(_weekly_levels(conn, _WEEKLY_RATE_SQL, [_FX_SERIES, since, until]))
    rate_3y = _bp_changes(_weekly_levels(conn, _WEEKLY_RATE_SQL, [_RATE_SERIES[0], since, until]))
    rate_10y = _bp_changes(_weekly_levels(conn, _WEEKLY_RATE_SQL, [_RATE_SERIES[1], since, until]))

    weeks = sorted(set(stock) & set(market) & set(fx) & set(rate_3y) & set(rate_10y))
    payload: dict[str, Any] = {
        "code": code,
        "benchmark": _BENCHMARK,
        "since": since.isoformat(),
        "until": until.isoformat(),
        "weeks": len(weeks),
    }
    if len(weeks) < _MIN_WEEKS:
        payload["regression"] = None
        payload["hint"] = (
            f"Fewer than {_MIN_WEEKS} weeks with a value for the stock, KOSPI, USD/KRW and both KTB series. "
            "Check `cache ohlcv --code` for the stock and KOSPI, and run `cache load --only rates` "
            "(needs ECOS_AUTH_KEY) for the FX and rate series."
        )
        return payload

    y = np.array([stock[week] for week in weeks], dtype=np.float64)
    x = np.column_stack(
        [
            np.ones(len(weeks)),
            [market[week] for week in weeks],
            [fx[week] for week in weeks],
            [rate_3y[week] for week in weeks],
            [rate_10y[week] for week in weeks],
        ]
    )
    coef, t_values, r_squared = _ols(x, y)
    payload["first_week"] = weeks[0].isoformat()
    payload["last_week"] = weeks[-1].isoformat()
    payload["r_squared"] = None if np.isnan(r_squared) else round(float(r_squared), 4)
    payload["coefficients"] = {
        name: {
            "beta": None if np.isnan(beta) else round(float(beta), 6),
            "t": None if np.isnan(t) else round(float(t), 3),
        }
        for name, beta, t in zip(_FACTOR_NAMES, coef, t_values, strict=True)
    }
    if np.isnan(coef).all():
        payload["hint"] = (
            "The factors are collinear over these weeks (a series that never moved, or two that moved "
            "in lockstep), so no beta is identified. Widen the window with `--since`."
        )
    return payload


# Three years of weeks gives the 4-factor regression enough room above `_MIN_WEEKS` without reaching back
# past most listings; callers can widen it with `--since`.
DEFAULT_SINCE_DAYS = 365 * 3
