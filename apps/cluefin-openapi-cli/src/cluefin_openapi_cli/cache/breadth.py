"""`cache rs`/`cache breadth`: cross-sectional relative strength and market-wide breadth.

Both read `ohlcv`/`company` only (no writer, no new table) and share the same universe rule as
`cache trend-setup` (`cache.trend._universe`): common stock listed on the day, no SPACs,
KOSPI/KOSDAQ only. Prices are **adjusted** (`close * adj_factor`), matching `cache trend-setup`
and `cache perf` — never the raw bars `cache ohlcv` defaults to.

## RS (relative strength)

RS(1M) reproduces the stockeasy screen definition reverse-engineered in the
`stockeasy-metric-definitions` memory (2026-10-07, 46-stock sample, correlation 0.998): the
cross-sectional percentile (0-99) of each stock's 21-trading-day adjusted return among every
other stock judged the same day. That memory also notes an IBD-style long-horizon RS (quarterly
weighted) whose exact formula is unconfirmed (only an approximate linear mapping to this
percentile was fit) — it is **not** implemented here; only RS(1M) and the 21-day return it is
built from exist. Sector RS does the same percentile over each sector's median 21-day return
(`company.sector`, 26 coarse groups; `company.industry` is the finer 155-group field and can be
selected with `--by industry` but has thinner per-group samples).

## Market breadth

52-week high/low counts, the share of stocks above their 50-day SMA, advance/decline/unchanged
counts, and two index-level signals from IBD ("How to Make Money in Stocks", O'Neil) methodology:
distribution days and the follow-through day (FTD). Both are approximations of a methodology
that IBD does not publish as a precise, backtestable formula — thresholds and windows are the
commonly cited ones, written down here (not just in code) so a disagreement with a published IBD
reading is diagnosable:

- **Distribution day**: the index closes down >= 0.2% from the previous close, on volume higher
  than the previous session's volume. Counted over the trailing 25 trading days (IBD's own
  rolling window before a stale day "ages out"); this implementation does not apply IBD's
  informal "erased by a 5%+ rally off the low" removal rule, so a count here can run slightly
  higher than a discretionary IBD count after a sharp rebound.
- **Follow-through day**: within an "attempted rally" — starting at day 1, the first day the
  index closes up after the most recent swing low in the trailing `_SWING_WINDOW` (default 50)
  trading days — a day from day 4 through day 10 (IBD's own window; the classic rule was
  days 4-7, later widened) where the index gains >= 1.25% (IBD's current threshold; it was 1%
  before 2015) on volume higher than the prior session. Day 1 itself is searched over the
  trailing `_DAY1_SEARCH_DAYS` (default 60) trading days so a rally already confirmed (or
  already failed) earlier in that span is still reported, not just one starting in the last
  10 days. The first qualifying day is reported; none found means no confirmed rally in the
  window.

Neither signal is a buy/sell rule here, just the dated facts (which day, by how much, on what
volume ratio) a caller can weigh themselves.
"""

from __future__ import annotations

import math
from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.cache import trend as cache_trend

__all__ = ["breadth", "rs"]

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


def _round_half_up(value: float) -> int:
    """Round a percentile for display. Average ranks land on x.5, where `round()` goes to even."""

    return math.floor(value + 0.5)


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
                "rs_1m": _round_half_up(rs_1m[code]) if code in rs_1m else None,
                f"{group_field}_rs": _round_half_up(group_percentile) if group_percentile is not None else None,
            }
        )
    # Sort on the unrounded percentile: two stocks that both display 51 are not tied.
    rows.sort(key=lambda row: (row["code"] not in rs_1m, -rs_1m.get(row["code"], 0.0)))

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


# ---------------------------------------------------------------------------
# market breadth
# ---------------------------------------------------------------------------

_SMA_WINDOW = 50
_HIGH_LOW_WINDOW = 250  # trading days, excluding the day itself (stockeasy-metric-definitions memory)
_DIST_WINDOW = 25
_DIST_DECLINE_PCT = 0.2
_SWING_WINDOW = 50
_DAY1_SEARCH_DAYS = 60  # how far back from `as_of` a still-relevant rally attempt can have started
_FTD_MIN_DAY = 4
_FTD_MAX_DAY = 10
_FTD_GAIN_PCT = 1.25

_BREADTH_INDEX_SQL = """
SELECT code, date, open * f, high * f, low * f, close * f, volume / f
FROM (SELECT *, COALESCE(NULLIF(adj_factor, 0), 1) AS f FROM ohlcv WHERE code = ? AND date <= ? ORDER BY date DESC
      LIMIT ?)
ORDER BY date
"""

# One pass over every judged stock's last `_HIGH_LOW_WINDOW + 1` adjusted closes and 50-day SMA
# window, done in SQL window functions rather than per-stock Python loops (same spirit as
# `cache.trend._series`'s one columnar read for the whole universe).
_BREADTH_STOCK_SQL = """
WITH adj AS (
  SELECT code, date, close * COALESCE(NULLIF(adj_factor, 0), 1) AS close,
         high * COALESCE(NULLIF(adj_factor, 0), 1) AS high,
         low * COALESCE(NULLIF(adj_factor, 0), 1) AS low
  FROM ohlcv
  WHERE code IN (SELECT unnest(?::TEXT[])) AND date <= ? AND close > 0
),
windowed AS (
  SELECT *,
    row_number() OVER (PARTITION BY code ORDER BY date DESC) AS rn,
    max(high) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND 1 PRECEDING) AS prior_high_max,
    min(low) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND 1 PRECEDING) AS prior_low_min,
    avg(close) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS sma,
    count(*) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS sma_n,
    lag(close) OVER (PARTITION BY code ORDER BY date) AS prev_close
  FROM adj
)
SELECT code, date, close, high, low, prior_high_max, prior_low_min, sma, sma_n, prev_close
FROM windowed WHERE rn = 1
"""


def _breadth_rows(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> list[tuple[Any, ...]]:
    return conn.execute(
        _BREADTH_STOCK_SQL,
        [codes, as_of, _HIGH_LOW_WINDOW, _HIGH_LOW_WINDOW, _SMA_WINDOW - 1, _SMA_WINDOW - 1],
    ).fetchall()


def _distribution_days(conn: duckdb.DuckDBPyConnection, index_code: str, as_of: date) -> dict[str, Any]:
    bars = conn.execute(_BREADTH_INDEX_SQL, [index_code, as_of, _DIST_WINDOW + 1]).fetchall()
    days = []
    for i in range(1, len(bars)):
        _code, day, _o, _h, _l, close, volume = bars[i]
        _prev_code, _prev_day, _po, _ph, _pl, prev_close, prev_volume = bars[i - 1]
        if close is None or prev_close is None or volume is None or prev_volume is None:
            continue
        change_pct = (close / prev_close - 1) * 100
        if change_pct <= -_DIST_DECLINE_PCT and volume > prev_volume:
            days.append({"date": day.isoformat(), "change_pct": round(change_pct, 2)})
    return {"window": _DIST_WINDOW, "count": len(days), "days": days}


def _follow_through_day(conn: duckdb.DuckDBPyConnection, index_code: str, as_of: date) -> dict[str, Any]:
    lookback = _SWING_WINDOW + _DAY1_SEARCH_DAYS
    bars = conn.execute(_BREADTH_INDEX_SQL, [index_code, as_of, lookback]).fetchall()
    result: dict[str, Any] = {
        "swing_window": _SWING_WINDOW,
        "day1_search_days": _DAY1_SEARCH_DAYS,
        "day_range": [_FTD_MIN_DAY, _FTD_MAX_DAY],
        "gain_threshold_pct": _FTD_GAIN_PCT,
        "rally_day1": None,
        "found": False,
        "date": None,
        "gain_pct": None,
        "day_number": None,
    }
    if len(bars) < _SWING_WINDOW + 2:
        return result
    closes = [row[5] for row in bars]
    volumes = [row[6] for row in bars]
    dates = [row[1] for row in bars]
    # Most recent swing low within the trailing `_SWING_WINDOW` sessions before each candidate
    # day1, scanned over the trailing `_DAY1_SEARCH_DAYS` up to the day before `as_of` — a rally
    # that started further back than 10 sessions ago but confirmed (or failed) since is still found.
    day1_idx = None
    for i in range(_SWING_WINDOW, len(closes)):
        window = closes[i - _SWING_WINDOW : i]
        if closes[i - 1] is None or any(c is None for c in window):
            continue
        if closes[i - 1] == min(window) and closes[i] is not None and closes[i] > closes[i - 1]:
            day1_idx = i  # keep the most recent one found
    if day1_idx is None:
        return result
    result["rally_day1"] = dates[day1_idx].isoformat()
    for offset in range(_FTD_MIN_DAY, _FTD_MAX_DAY + 1):
        i = day1_idx + offset - 1
        if i >= len(closes) or i == 0:
            continue
        if closes[i] is None or closes[i - 1] is None or volumes[i] is None or volumes[i - 1] is None:
            continue
        gain_pct = (closes[i] / closes[i - 1] - 1) * 100
        if gain_pct >= _FTD_GAIN_PCT and volumes[i] > volumes[i - 1]:
            result.update(
                {"found": True, "date": dates[i].isoformat(), "gain_pct": round(gain_pct, 2), "day_number": offset}
            )
            break
    return result


_NOTES_BREADTH = (
    "52주 신고가·신저가 = 당일 수정 고가·저가가 당일 제외 직전 250거래일 범위를 갱신한 종목 수 "
    "(memory stockeasy-metric-definitions 와 같은 창).",
    "50일선 위 비율 = 수정종가가 50일 단순이동평균 이상인 종목 수 ÷ 50일 데이터가 다 찬 종목 수.",
    "상승·하락·보합은 전일 대비 수정종가 기준.",
    "distribution day·follow-through day 는 지수(U0001/U1001/U2001) 기준 IBD 방법론의 근사다 — "
    "정확한 공식은 비공개라 이 모듈 docstring 의 정의·문턱값을 쓴다. 매수·매도 신호가 아니다.",
)


def breadth(conn: duckdb.DuckDBPyConnection, as_of: date, *, market: str | None = None) -> dict[str, Any]:
    """Market-wide breadth for one day: highs/lows, %>50dma, advance/decline, FTD/distribution days."""

    universe = cache_trend._universe(conn, as_of, market, None)
    codes = [row["code"] for row in universe]
    rows = _breadth_rows(conn, codes, as_of) if codes else []

    new_high = new_low = above_50dma = advancing = declining = unchanged = 0
    judged_50dma = 0
    for _code, day, close, high, low, prior_high_max, prior_low_min, sma, sma_n, prev_close in rows:
        if day != as_of:
            continue
        if prior_high_max is not None and high is not None and high >= prior_high_max:
            new_high += 1
        if prior_low_min is not None and low is not None and low <= prior_low_min:
            new_low += 1
        if sma_n == _SMA_WINDOW and sma is not None and close is not None:
            judged_50dma += 1
            if close >= sma:
                above_50dma += 1
        if prev_close is not None and close is not None:
            if close > prev_close:
                advancing += 1
            elif close < prev_close:
                declining += 1
            else:
                unchanged += 1

    indices = {}
    for index_code in ("U0001", "U1001", "U2001"):
        indices[index_code] = {
            "distribution_days": _distribution_days(conn, index_code, as_of),
            "follow_through_day": _follow_through_day(conn, index_code, as_of),
        }

    return {
        "as_of": as_of.isoformat(),
        "market": market,
        "universe": len(universe),
        "new_52w_high": new_high,
        "new_52w_low": new_low,
        "above_50dma": above_50dma,
        "above_50dma_pct": round(above_50dma / judged_50dma * 100, 1) if judged_50dma else None,
        "above_50dma_judged": judged_50dma,
        "advancing": advancing,
        "declining": declining,
        "unchanged": unchanged,
        "indices": indices,
        "notes": list(_NOTES_BREADTH),
    }
