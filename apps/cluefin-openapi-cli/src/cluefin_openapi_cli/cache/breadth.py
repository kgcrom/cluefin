"""`cache rs`: cross-sectional relative strength (RS percentile, RS(1M), sector/industry RS).

Reads `ohlcv`/`company` only (no writer, no new table) and shares the same universe rule as
`cache trend-setup` (`cache.trend._universe`): common stock listed on the day, no SPACs,
KOSPI/KOSDAQ only. Prices are **adjusted** (`close * adj_factor`), matching `cache trend-setup`
and `cache perf` — never the raw bars `cache ohlcv` defaults to.

RS(1M) reproduces the stockeasy screen definition reverse-engineered in the
`stockeasy-metric-definitions` memory (2026-10-07, 46-stock sample, correlation 0.998): the
cross-sectional percentile (0-99) of each stock's 21-trading-day adjusted return among every
other stock judged the same day. That memory also notes an IBD-style long-horizon RS (quarterly
weighted) whose exact formula is unconfirmed (only an approximate linear mapping to this
percentile was fit) — it is **not** implemented here; only RS(1M) and the 21-day return it is
built from exist. Sector RS does the same percentile over each sector's median 21-day return
(`company.sector`, 26 coarse groups; `company.industry` is the finer 155-group field and can be
selected with `--by industry` but has thinner per-group samples).
"""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.cache import trend as cache_trend

__all__ = ["rs"]

# 21 trading days ~= 1 calendar month of sessions (stockeasy-metric-definitions memory).
_RS_LOOKBACK = 21
_MIN_SECTOR_STOCKS = 3

_NOTES_RS = (
    "RS(1M) = 21거래일 수정주가 수익률의 코스피+코스닥 보통주 횡단면 백분위(0~99) — "
    "memory stockeasy-metric-definitions 2026-10-07 역산(상관 0.998).",
    "IBD식 장기 가중 RS(최근 분기 2배)는 정확한 공식이 미확인이라 내지 않는다 — RS(1M)만 있다.",
    "업종 RS = 그룹(기본 company.sector) 중앙값 21거래일 수익률의 그룹 간 백분위. 표본 "
    f"{_MIN_SECTOR_STOCKS}종목 미만인 그룹은 null.",
    "유니버스는 `cache trend-setup`과 같다: 그날 상장(폐지 포함) · 끝자리 0 · 이름에 '스팩' 없음.",
)


def _percentile_rank(values: np.ndarray) -> np.ndarray:
    """Average-rank percentile in [0, 99], ties sharing the mean rank of their group.

    `n == 1` is defined as 0 (there is no cross-section to rank against); documented by the
    caller when it matters (single-stock sectors are dropped before this is called for RS).
    """

    n = len(values)
    if n == 0:
        return np.array([], dtype=np.float64)
    if n == 1:
        return np.array([0.0])
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    # Average rank for tied values (scipy.stats.rankdata's "average" method, inlined to avoid
    # a scipy dependency this package does not otherwise have).
    is_new = np.r_[True, sorted_values[1:] != sorted_values[:-1]]
    group_id = np.cumsum(is_new) - 1
    group_start = np.flatnonzero(is_new)
    group_end = np.r_[group_start[1:], n]
    avg_rank_by_group = (group_start + group_end - 1) / 2.0  # 0-based average rank
    sorted_ranks = avg_rank_by_group[group_id]
    ranks = np.empty(n, dtype=np.float64)
    ranks[order] = sorted_ranks
    return ranks / (n - 1) * 99


_RETURN_SQL = """
WITH ranked AS (
  SELECT code, date, close * COALESCE(NULLIF(adj_factor, 0), 1) AS adj_close,
         row_number() OVER (PARTITION BY code ORDER BY date DESC) AS rn
  FROM ohlcv
  WHERE code IN (SELECT unnest(?::TEXT[])) AND date <= ? AND close > 0
)
SELECT code,
       max(CASE WHEN rn = 1 THEN date END) AS last_date,
       max(CASE WHEN rn = 1 THEN adj_close END) AS close_now,
       max(CASE WHEN rn = ? THEN adj_close END) AS close_then
FROM ranked
WHERE rn IN (1, ?)
GROUP BY code
"""


def _returns(
    conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date, lookback: int
) -> dict[str, tuple[float, date]]:
    """``{code: (return_pct, last_date)}`` for codes with both ends of the window and a bar on ``as_of``."""

    rows = conn.execute(_RETURN_SQL, [codes, as_of, lookback + 1, lookback + 1]).fetchall()
    out: dict[str, tuple[float, date]] = {}
    for code, last_date, close_now, close_then in rows:
        if last_date != as_of or not close_now or not close_then:
            continue
        out[code] = (close_now / close_then - 1, last_date)
    return out


def rs(
    conn: duckdb.DuckDBPyConnection,
    as_of: date,
    *,
    market: str | None = None,
    codes: list[str] | None = None,
    group_by: str = "sector",
) -> dict[str, Any]:
    """RS(1M) percentile for every judged stock, plus a sector/industry percentile on top."""

    universe = cache_trend._universe(conn, as_of, None, None)
    all_codes = [row["code"] for row in universe]
    returns = _returns(conn, all_codes, as_of, _RS_LOOKBACK)
    by_code = {row["code"]: row for row in universe}

    judged_codes = list(returns)
    judged_values = np.array([returns[code][0] for code in judged_codes], dtype=np.float64)
    rs_1m = dict(zip(judged_codes, _percentile_rank(judged_values), strict=True))

    group_field = "industry" if group_by == "industry" else "sector"
    groups: dict[str, list[str]] = {}
    for code in judged_codes:
        key = by_code[code].get(group_field)
        if key:
            groups.setdefault(key, []).append(code)
    group_medians = {
        key: float(np.median([returns[code][0] for code in members]))
        for key, members in groups.items()
        if len(members) >= _MIN_SECTOR_STOCKS
    }
    group_names = list(group_medians)
    group_rank = dict(
        zip(group_names, _percentile_rank(np.array([group_medians[name] for name in group_names])), strict=True)
    )

    wanted_codes = set(codes) if codes else None
    rows = []
    for company in universe:
        code = company["code"]
        if market is not None and company["market"] != market:
            continue
        if wanted_codes is not None and code not in wanted_codes:
            continue
        ret = returns.get(code)
        group_key = company.get(group_field)
        group_percentile = group_rank.get(group_key) if group_key else None
        rows.append(
            {
                "code": code,
                "name": company["name"],
                "market": company["market"],
                "sector": company["sector"],
                "industry": company["industry"],
                "return_1m_pct": round(ret[0] * 100, 2) if ret else None,
                "rs_1m": round(float(rs_1m[code])) if code in rs_1m else None,
                f"{group_field}_rs": round(float(group_percentile)) if group_percentile is not None else None,
            }
        )
    rows.sort(key=lambda row: (row["rs_1m"] is None, -(row["rs_1m"] or 0)))

    return {
        "as_of": as_of.isoformat(),
        "group_by": group_field,
        "universe": len(universe),
        "judged": len(judged_codes),
        "skipped": len(universe) - len(judged_codes),
        "groups": {
            name: {"median_return_1m_pct": round(group_medians[name] * 100, 2), "n": len(groups[name])}
            for name in group_names
        },
        "count": len(rows),
        "rows": rows,
        "notes": list(_NOTES_RS),
    }
