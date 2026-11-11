"""`cache peers`: deterministic comparable-company picks for one stock.

Decided 2026-11-11 (`docs/plans/investor-toolkit-plan.md` track C). A company-review's "비교 기업"
step today is picked by hand from the filing text or the agent's own memory — not reproducible.
This command instead picks candidates from the same `company.industry` group (falling back to
`company.sector` when fewer than 3 peers share the industry — `_MIN_PEERS`), and ranks them by two
signals, same as the "순위의 합" convention `cache magic-formula` uses:

- **Size closeness**: ``abs(log(candidate_mcap / target_mcap))`` — 0 for an identical market cap,
  growing either way it differs. Ranked ascending (closest size first).
- **Return correlation**: Pearson correlation of daily adjusted-close returns over the trailing
  250 trading days, on the dates both stocks have a bar. Fewer than 120 overlapping days (`
  _MIN_OVERLAP_DAYS`) is `null` — too short a window to mean anything. Ranked descending (most
  correlated first).

Both ranks are **ordinal** (1..N, average rank for ties) — not `cache.breadth._percentile_rank`'s
0-99 percentile, because there is no fixed-scale cross-section here, just N candidates to order.
A candidate missing one signal (no cached mcap, or too few overlapping days) gets that rank's worst
value (N+1) rather than being dropped — it still shows up, just sinks to the bottom on that signal.

Every row also carries `cache.screen`'s own factor table for that stock (reused, not
recomputed) — "비교 기업" is only useful next to the same numbers `cache screen` already produces.

`industry`/`sector` grouping is **current, not point-in-time** — `notes` says so on every call
(same caveat as `cache/magic.py`'s/`cache/baserate.py`'s current-share-count approximation).
"""

from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.cache import trend as cache_trend
from cluefin_openapi_cli.cache.read import read_company
from cluefin_openapi_cli.cache.screen import DEFAULT_TOP as _SCREEN_DEFAULT_TOP
from cluefin_openapi_cli.cache.screen import screen
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["DEFAULT_TOP", "peers"]

DEFAULT_TOP = 5
_MIN_PEERS = 3
_RETURN_WINDOW = 250
_MIN_OVERLAP_DAYS = 120
# Trading-day window padded to calendar days (same ~1.45x ratio `cache.trend` uses for its own lookback).
_LOOKBACK_DAYS = 400

_NOTES = (
    "업종 분류는 현재 값(PIT 아님) — company.industry/sector 는 캐시가 아는 최신 값이다.",
    "시총 근접도 = |log(candidate 시총 / 대상 시총)| 오름차순 순위, 수익률 상관 = 최근 250거래일 겹치는 날의 "
    "일간 수정주가 수익률 피어슨 상관 내림차순 순위 — 둘의 순위 합으로 정렬한다(ordinal rank, 평균순위 동점 "
    "처리). 겹치는 날이 120일 미만이면 상관은 null 이고 그 신호는 최하위 순위로 처리한다.",
    "각 행의 나머지 값은 cache screen 의 팩터 표를 그대로 재사용한다(다시 계산하지 않는다).",
)

_SERIES_SQL = """
SELECT code, date, close * COALESCE(NULLIF(adj_factor, 0), 1) AS adj_close
FROM ohlcv
WHERE code IN (SELECT unnest(?::TEXT[])) AND date <= ? AND date >= ? AND close > 0
ORDER BY code, date
"""


def _ordinal_rank(values: np.ndarray) -> np.ndarray:
    """Average rank in [1, n] ascending (smallest value gets rank 1), ties sharing the mean rank."""

    n = len(values)
    if n == 0:
        return np.array([], dtype=np.float64)
    if n == 1:
        return np.array([1.0])
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    is_new = np.r_[True, sorted_values[1:] != sorted_values[:-1]]
    group_id = np.cumsum(is_new) - 1
    group_start = np.flatnonzero(is_new)
    group_end = np.r_[group_start[1:], n]
    avg_rank_by_group = (group_start + group_end - 1) / 2.0 + 1  # 1-based average rank
    sorted_ranks = avg_rank_by_group[group_id]
    ranks = np.empty(n, dtype=np.float64)
    ranks[order] = sorted_ranks
    return ranks


def _return_series(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, dict[date, float]]:
    """``{code: {date: daily_return}}`` from adjusted closes over the trailing window."""

    since = as_of - timedelta(days=_LOOKBACK_DAYS)
    rows = conn.execute(_SERIES_SQL, [codes, as_of, since]).fetchall()
    closes: dict[str, list[tuple[date, float]]] = {}
    for code, day, adj_close in rows:
        closes.setdefault(code, []).append((day, adj_close))
    returns: dict[str, dict[date, float]] = {}
    for code, pairs in closes.items():
        tail = pairs[-(_RETURN_WINDOW + 1) :]
        series: dict[date, float] = {}
        for (_prev_day, prev_close), (day, close) in zip(tail, tail[1:], strict=False):
            if prev_close:
                series[day] = close / prev_close - 1
        returns[code] = series
    return returns


def _correlation(target: dict[date, float], candidate: dict[date, float]) -> tuple[float | None, int]:
    shared = sorted(set(target) & set(candidate))
    if len(shared) < _MIN_OVERLAP_DAYS:
        return None, len(shared)
    target_values = np.array([target[day] for day in shared], dtype=np.float64)
    candidate_values = np.array([candidate[day] for day in shared], dtype=np.float64)
    if np.std(target_values) == 0 or np.std(candidate_values) == 0:
        return None, len(shared)
    corr = float(np.corrcoef(target_values, candidate_values)[0, 1])
    return corr, len(shared)


def peers(conn: duckdb.DuckDBPyConnection, as_of: date, code: str, *, top: int = DEFAULT_TOP) -> dict[str, Any]:
    """Deterministic comparable-company picks for ``code``, ranked by size closeness + return correlation."""

    code = code.strip().upper()
    target_rows = read_company(conn, code=code)["companies"]
    if not target_rows:
        raise CliError(f"`{code}` is not in `cache company`.", exit_code=EXIT_USAGE, hint="Run `cache load` first.")
    target = target_rows[0]

    universe = cache_trend._universe(conn, as_of, None, None)
    by_code = {row["code"]: row for row in universe}

    group_field = "industry"
    same_group = [row for row in universe if row["code"] != code and row.get(group_field) == target.get(group_field)]
    if len(same_group) < _MIN_PEERS:
        group_field = "sector"
        same_group = [
            row for row in universe if row["code"] != code and row.get(group_field) == target.get(group_field)
        ]
    candidate_codes = [row["code"] for row in same_group]

    factor_payload = screen(
        conn, as_of, codes=[code, *candidate_codes], top=max(len(candidate_codes) + 1, _SCREEN_DEFAULT_TOP)
    )
    factor_rows = {row["code"]: row for row in factor_payload["rows"]}
    target_factor = factor_rows.get(code)
    target_mcap = target_factor["mcap"] if target_factor else None

    returns = _return_series(conn, [code, *candidate_codes], as_of)
    target_returns = returns.get(code, {})

    log_ratios: dict[str, float] = {}
    correlations: dict[str, float] = {}
    overlap_days: dict[str, int] = {}
    for peer_code in candidate_codes:
        peer_factor = factor_rows.get(peer_code)
        peer_mcap = peer_factor["mcap"] if peer_factor else None
        if target_mcap and peer_mcap:
            log_ratios[peer_code] = abs(math.log(peer_mcap / target_mcap))
        corr, overlap = _correlation(target_returns, returns.get(peer_code, {}))
        overlap_days[peer_code] = overlap
        if corr is not None:
            correlations[peer_code] = corr

    size_rank = dict(zip(log_ratios, _ordinal_rank(np.array(list(log_ratios.values()), dtype=np.float64)), strict=True))
    corr_rank = dict(
        zip(correlations, _ordinal_rank(-np.array(list(correlations.values()), dtype=np.float64)), strict=True)
    )
    worst_size_rank = len(log_ratios) + 1
    worst_corr_rank = len(correlations) + 1

    rows: list[dict[str, Any]] = []
    for peer_code in candidate_codes:
        row = dict(factor_rows.get(peer_code, {"code": peer_code, "name": by_code[peer_code]["name"]}))
        row["size_rank"] = size_rank.get(peer_code, worst_size_rank)
        row["corr_rank"] = corr_rank.get(peer_code, worst_corr_rank)
        row["combined_rank"] = row["size_rank"] + row["corr_rank"]
        row["return_correlation"] = round(correlations[peer_code], 4) if peer_code in correlations else None
        row["overlap_days"] = overlap_days[peer_code]
        rows.append(row)
    rows.sort(key=lambda row: (row["combined_rank"], row["code"]))

    return {
        "code": code,
        "as_of": as_of.isoformat(),
        "group_by": group_field,
        "group_value": target.get(group_field),
        "candidates": len(candidate_codes),
        "count": min(len(rows), top),
        "rows": rows[:top],
        "notes": list(_NOTES),
    }
