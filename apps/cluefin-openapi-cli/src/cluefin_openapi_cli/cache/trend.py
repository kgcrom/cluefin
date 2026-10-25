"""`cache trend-setup`: the trend-setup judgement for every stock in the cache on one day.

No rule lives here — each stock goes through `trend_setup.analyze`, the same function
`kis chart trend-setup` calls, and a contract test holds the two to the same answer. This
module only reads the cache, picks the universe and summarizes rows.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.cache.read import read_company

__all__ = ["latest_index_date", "scan"]

# Matches `kis chart trend-setup` (260 bars); ~380 calendar days, read with slack.
_BARS = 260
_LOOKBACK_DAYS = 500
_INDEX_FOR = {"KOSPI": "U0001", "KOSDAQ": "U1001"}

# Adjusted like `read_ohlcv(adjusted=True)`; NULL prices (KIS 0) drop the bar, as in the backtest.
_BARS_SQL = """
SELECT code, date,
       open * f, high * f, low * f, close * f, volume / f, value
FROM (
  SELECT *, COALESCE(NULLIF(adj_factor, 0), 1) AS f FROM ohlcv
  WHERE code IN (SELECT unnest(?::TEXT[])) AND date BETWEEN ? AND ?
)
WHERE high > 0 AND low > 0 AND close > 0
ORDER BY code, date
"""
_INDEX_SQL = "SELECT code, date, close FROM ohlcv WHERE code IN ('U0001', 'U1001') AND date <= ? ORDER BY code, date"

# Row order: actionable first, then by distance to the pivot (closest above first).
_STATUS_ORDER = (
    "alert/setup",
    "watch/breaking_out",
    "watch/g3_candidate",
    "watch/g2",
    "watch/extended",
    "watch/far_below_pivot",
    "exclude/overheated",
    "exclude/no_group",
    "exclude/illiquid",
)
_NOTES = (
    "가격은 캐시의 KIS 원주가 × adj_factor(수정주가)다 — kis chart trend-setup 과 같은 기준.",
    "company.market 은 현재 값이다 — 시장을 옮긴 종목은 과거 날짜에서 비교 지수가 틀릴 수 있다.",
)


def latest_index_date(conn: duckdb.DuckDBPyConnection) -> date | None:
    row = conn.execute("SELECT max(date) FROM ohlcv WHERE code = 'U0001'").fetchone()
    return row[0] if row else None


def _universe(
    conn: duckdb.DuckDBPyConnection, as_of: date, market: str | None, codes: list[str] | None
) -> list[dict[str, Any]]:
    """Listed on ``as_of`` (later delistings included), common shares only, no SPACs — as the backtest."""

    companies = read_company(conn, as_of=as_of, market=market)["companies"]
    wanted = set(codes) if codes else None
    return [
        row
        for row in companies
        if row["code"].endswith("0")
        and "스팩" not in (row["name"] or "")
        and row["market"] in _INDEX_FOR
        and (wanted is None or row["code"] in wanted)
    ]


def _indices(conn: duckdb.DuckDBPyConnection, as_of: date) -> dict[str, trend_setup.IndexCloses]:
    by_code: dict[str, list[tuple[date, float]]] = {}
    for code, day, close in conn.execute(_INDEX_SQL, [as_of]).fetchall():
        by_code.setdefault(code, []).append((day, close))
    return {code: trend_setup.IndexCloses.from_pairs(pairs) for code, pairs in by_code.items()}


def _series(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, trend_setup.PriceArrays]:
    """Each code's last ``_BARS`` bars up to ``as_of``, split from one columnar read."""

    cols = conn.execute(_BARS_SQL, [codes, as_of - timedelta(days=_LOOKBACK_DAYS), as_of]).fetchnumpy()
    names = list(cols)
    if len(cols[names[0]]) == 0:
        return {}
    code_col = np.asarray(cols[names[0]])
    dates = np.char.replace(np.datetime_as_string(np.asarray(cols[names[1]]), unit="D"), "-", "")
    prices = [np.asarray(cols[name], dtype=np.float64) for name in names[2:8]]
    bounds = np.flatnonzero(code_col[1:] != code_col[:-1]) + 1
    out = {}
    for start, stop in zip(np.r_[0, bounds], np.r_[bounds, len(code_col)], strict=True):
        cut = slice(max(start, stop - _BARS), stop)
        out[str(code_col[start])] = trend_setup.PriceArrays(
            dates=tuple(dates[cut].tolist()),
            open=prices[0][cut],
            high=prices[1][cut],
            low=prices[2][cut],
            close=prices[3][cut],
            volume=prices[4][cut],
            value=prices[5][cut],
        )
    return out


def _failed(setup: dict[str, Any]) -> list[str]:
    """Check ids that kept the stock out of groups 2 and 3 — why it is not a setup, from the row alone."""

    checks = setup["checks"]
    return [check["id"] for check in (*checks["g2"], *checks["g3"]) if not check["pass"]]


def _row(company: dict[str, Any], reading: dict[str, Any]) -> dict[str, Any]:
    setup, pivot, strength = reading["setup"], reading["pivot"], reading["strength"]
    return {
        "code": company["code"],
        "name": company["name"],
        "market": company["market"],
        "close": reading["close"],
        "action": setup["action"],
        "status": setup["status"],
        "groups": setup["groups"],
        "reason": setup["reason"],
        "pivot": pivot["price"] if pivot else None,
        "to_pivot_pct": pivot["to_pivot_pct"] if pivot else None,
        "rel": strength["rel"],
        "contractions": pivot["contractions"] if pivot else 0,
        "last_contraction_pct": pivot["last_contraction_pct"] if pivot else None,
        "range_10d_pct": reading["volatility"]["range_10d_pct"],
        "gap_to_high_pct": reading["range_52w"]["gap_to_high_pct"],
        "g2_score": setup["g2_score"]["score"],
        "traded_value_20d_eok": reading["volume"]["traded_value_20d_eok"],
        "levels": reading["levels"],
        "failed": _failed(setup),
    }


def _sort_key(row: dict[str, Any]) -> tuple[int, float]:
    key = f"{row['action']}/{row['status']}"
    rank = _STATUS_ORDER.index(key) if key in _STATUS_ORDER else len(_STATUS_ORDER)
    to_pivot = row["to_pivot_pct"]
    return rank, -to_pivot if to_pivot is not None else float("inf")


def _wanted(row: dict[str, Any], statuses: list[str] | None, include_excluded: bool) -> bool:
    if statuses:
        return row["action"] in statuses or f"{row['action']}/{row['status']}" in statuses
    return include_excluded or row["action"] != "exclude"


# README "trend-setup 규칙과 근거" (theme): a theme is hot when its median 20-session adjusted return ranks in the top
# 20% of themes with at least 5 stocks; a stock leads its theme when it is among the theme's top 3 by
# 20-day traded value or one of Kiwoom's main stocks, and its rel is at least the theme's median rel.
_THEME_MIN_STOCKS = 5
_THEME_HOT_PCT = 20
_THEME_LEADER_TOP = 3
_THEME_SHOWN = 3
_THEME_PERIOD = 20


@dataclass(frozen=True, slots=True)
class _Judged:
    company: dict[str, Any]
    reading: dict[str, Any]
    return_20d_pct: float | None


def _theme_snapshot(conn: duckdb.DuckDBPyConnection, as_of: date) -> tuple[list[tuple], list[tuple]] | None:
    themes = conn.execute("SELECT theme_code, name, main_stocks FROM theme WHERE as_of = ?", [as_of]).fetchall()
    if not themes:
        return None
    members = conn.execute("SELECT theme_code, code, name FROM theme_member WHERE as_of = ?", [as_of]).fetchall()
    return themes, members


def _nearest_snapshot(conn: duckdb.DuckDBPyConnection, as_of: date) -> date | None:
    row = conn.execute(
        "SELECT as_of FROM (SELECT DISTINCT as_of FROM theme) ORDER BY abs(date_diff('day', as_of, ?::DATE)) LIMIT 1",
        [as_of],
    ).fetchone()
    return row[0] if row else None


def _median(values: list[float]) -> float | None:
    return float(np.median(values)) if values else None


def _theme_tags(themes: list[tuple], members: list[tuple], judged: dict[str, _Judged]) -> dict[str, dict[str, Any]]:
    """Per stock code, the theme block of its rows. Ranks use every judged stock, not just shown rows."""

    by_theme: dict[str, list[tuple[str, str]]] = {}
    for theme_code, code, name in members:
        by_theme.setdefault(theme_code, []).append((code, name or ""))
    stats = []
    for theme_code, name, main_stocks in themes:
        stocks = [(code, stock_name) for code, stock_name in by_theme.get(theme_code, []) if code in judged]
        returns = [r for r in (judged[code].return_20d_pct for code, _ in stocks) if r is not None]
        stats.append((theme_code, name, main_stocks or "", stocks, _median(returns)))
    eligible = sorted(
        (item for item in stats if len(item[3]) >= _THEME_MIN_STOCKS and item[4] is not None),
        key=lambda item: -item[4],
    )
    rank_pct = {item[0]: (rank / len(eligible)) * 100 for rank, item in enumerate(eligible, 1)}
    tags: dict[str, list[dict[str, Any]]] = {}
    for theme_code, name, main_stocks, stocks, median_return in stats:
        if not stocks:
            continue
        main_names = {part.strip() for part in main_stocks.split(",") if part.strip()}
        rels = {code: judged[code].reading["strength"]["rel"] for code, _ in stocks}
        median_rel = _median([rel for rel in rels.values() if rel is not None])
        by_value = sorted(stocks, key=lambda item: -(judged[item[0]].reading["volume"]["traded_value_20d_eok"] or 0))
        top = {code for code, _ in by_value[:_THEME_LEADER_TOP]}
        rank = rank_pct.get(theme_code)
        hot = rank is not None and rank <= _THEME_HOT_PCT
        for code, stock_name in stocks:
            leader_by = [
                reason
                for reason, hit in (("traded_value_top3", code in top), ("main_stock", stock_name in main_names))
                if hit
            ]
            rel = rels[code]
            strong = rel is not None and median_rel is not None and rel >= median_rel
            tags.setdefault(code, []).append(
                {
                    "code": theme_code,
                    "name": name,
                    "return_20d_median_pct": round(median_return, 2) if median_return is not None else None,
                    "rank_pct": round(rank, 1) if rank is not None else None,
                    "hot": hot,
                    "leader": bool(leader_by) and strong,
                    "leader_by": leader_by,
                    "rel_vs_theme_median": round(rel / median_rel, 4) if rel and median_rel else None,
                }
            )
    blocks = {}
    for code, entries in tags.items():
        entries.sort(key=lambda entry: (not entry["hot"], -(entry["return_20d_median_pct"] or -1e9)))
        blocks[code] = {
            "hot": any(entry["hot"] for entry in entries),
            "leader": any(entry["leader"] for entry in entries),
            "pass": any(entry["hot"] and entry["leader"] for entry in entries),
            "themes": entries[:_THEME_SHOWN],
        }
    return blocks


_NO_THEME = {"hot": False, "leader": False, "pass": False, "themes": []}


def _return_20d(prices: trend_setup.PriceArrays) -> float | None:
    close = prices.close
    return float((close[-1] / close[-1 - _THEME_PERIOD] - 1) * 100) if len(close) > _THEME_PERIOD else None


def scan(
    conn: duckdb.DuckDBPyConnection,
    as_of: date,
    *,
    market: str | None = None,
    codes: list[str] | None = None,
    statuses: list[str] | None = None,
    include_excluded: bool = False,
    theme_filter: bool = False,
) -> dict[str, Any]:
    """Judge every stock listed on ``as_of``; rows for the wanted market/codes/statuses, counts for those.

    Every stock is judged even when ``market``/``codes`` narrow the rows, because theme
    leadership ranks a stock against all of its theme's stocks.
    """

    universe = _universe(conn, as_of, None, None)
    indices = _indices(conn, as_of)
    series = _series(conn, [row["code"] for row in universe], as_of)
    day = as_of.strftime("%Y%m%d")
    wanted_codes = set(codes) if codes else None
    shown = [
        row
        for row in universe
        if (market is None or row["market"] == market) and (wanted_codes is None or row["code"] in wanted_codes)
    ]
    shown_codes = {row["code"] for row in shown}
    judged: dict[str, _Judged] = {}
    skipped: Counter[str] = Counter()
    for company in universe:
        prices = series.get(company["code"])
        counted = company["code"] in shown_codes
        if prices is None or prices.dates[-1] != day:
            skipped["no_bar"] += counted
            continue
        try:
            reading = trend_setup.analyze(prices, indices[_INDEX_FOR[company["market"]]])
        except trend_setup.InsufficientHistory:
            skipped["insufficient_history"] += counted
            continue
        judged[company["code"]] = _Judged(company, reading, _return_20d(prices))

    snapshot = _theme_snapshot(conn, as_of)
    themes = _theme_tags(*snapshot, judged) if snapshot else None
    notes = list(_NOTES)
    if snapshot is None:
        nearest = _nearest_snapshot(conn, as_of)
        notes.append(
            f"테마 스냅샷 없음(가장 가까운 스냅샷 {nearest:%Y%m%d})"
            if nearest
            else "테마 스냅샷 없음(`cache load --only theme`)"
        )
    counts: Counter[str] = Counter()
    rows = []
    for company in shown:
        entry = judged.get(company["code"])
        if entry is None:
            continue
        row = _row(company, entry.reading)
        row["theme"] = themes.get(company["code"], _NO_THEME) if themes is not None else None
        counts[f"{row['action']}/{row['status']}"] += 1
        counts["theme_pass"] += bool(row["theme"] and row["theme"]["pass"])
        if _wanted(row, statuses, include_excluded) and (not theme_filter or (row["theme"] or {}).get("pass")):
            rows.append(row)
    rows.sort(key=_sort_key)
    summary: dict[str, Any] = {key: counts[key] for key in _STATUS_ORDER if counts[key]}
    if themes is not None:
        summary["theme_pass"] = counts["theme_pass"]
    summary["skipped"] = {"no_bar": skipped["no_bar"], "insufficient_history": skipped["insufficient_history"]}
    caveats = list(trend_setup.CAVEATS)
    if themes is not None:
        caveats.append(
            "테마 표시·필터는 백테스트가 없다 — 키움 테마 분류는 편집된 목록이고 스냅샷이 쌓인 날부터만 쓸 수 있다."
        )
    return {
        "as_of": day,
        "universe": len(shown),
        "summary": summary,
        "count": len(rows),
        "rows": rows,
        "notes": notes,
        "caveats": caveats,
    }
