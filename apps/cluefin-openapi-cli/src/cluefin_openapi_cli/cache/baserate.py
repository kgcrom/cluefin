"""`cache base-rate`: the outside view for one stock (Mauboussin, *The Base Rate Book*).

"Stocks in the same state as this one, historically, did what over the next N trading
days?" The state cell is trend-setup group (`trend_setup.analyze`'s g1/g2/g3/none, same
rules and same function as `kis chart trend-setup`/`cache trend-setup` — not
re-derived) × a market-cap tercile within that day's cross-section. The PBR axis is
deferred until the cache has historical financials (B-1b); only the two axes above exist.

Computing trend-setup for every stock on every past day is the cost `cache trend-setup`
already pays once (~0.5–1s for the whole market) — too slow to repeat for years of
history on every query. So this is two steps:

- `build()` (`cache base-rate-build`, the only writer here) samples every 5th trading day
  (`SAMPLE_STRIDE`) since the cache's first index bar, judges each stock in the backtest
  universe on that day and writes one row per (sample_date, code) to `setup_state`. It is
  incremental (only sample dates after the table's current max are computed) and
  idempotent (`ON CONFLICT DO NOTHING`); rerunning it with no new trading days is a no-op.
- `query()` (`cache base-rate`) reads `setup_state` only: it classifies the one requested
  stock's current cell (cheap — one stock's `analyze`, plus a plain SQL market-cap
  tercile), pulls the matching historical rows, and for each horizon computes the
  forward excess return (vs. the stock's own market index, adjusted closes, like
  `cache perf`) and, if asked, the touch rate against a target/stop.

Descriptive statistics only — no rule, no label, no recommendation.
"""

from __future__ import annotations

import time
from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.cache import trend as cache_trend
from cluefin_openapi_cli.cache.read import read_company
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["DEFAULT_HORIZONS", "MIN_SAMPLES", "SAMPLE_STRIDE", "build", "query"]

# Every 5th trading day: ~530 sample days over the cache's 2016–2026 span, ~0.5–1s each
# judged (measured against the real cache, see AGENTS.md) — minutes, not hours, to build.
SAMPLE_STRIDE = 5
DEFAULT_HORIZONS = (20, 40, 60)
# Below this many (code, sample_date) rows, merge the cell upward: group×mcap → group → all.
MIN_SAMPLES = 30
_QUANTILES = (0.10, 0.25, 0.50, 0.75, 0.90)

# `trend_setup.classify`'s one decided action/status already encodes the group priority
# (illiquid → g1 → g3 → g2 → none, see `trend_setup._decide`/`_state`) — this only picks the
# label back out of it, it does not re-derive any threshold.
_STATUS_TO_STATE: dict[str, str | None] = {
    "illiquid": None,  # dropped: "거래대금이 얇아 백테스트 대상 밖" — not part of the sampled population either
    "overheated": "g1",
    "setup": "g3",
    "breaking_out": "g3",
    "extended": "g3",
    "far_below_pivot": "g3",
    "g2": "g2",
    "g3_candidate": "g2",
    "no_group": "none",
}

NOTES = (
    "시총은 그날 종가(원주가, 조정 전) × 현재 상장주식수의 근사다 — 캐시에 과거 상장주식수가 없다(결정 2026-11-03).",
    "초과수익은 수정종가(adj_factor 반영) 기준, 지수는 KOSPI U0001/KOSDAQ U1001 — `cache perf`와 같은 관례다.",
    "표본은 거래일 5일 간격 스냅샷이다. horizon 이 60일이면 표본 창이 겹쳐 n은 독립 관측치 수보다 많다 — "
    "distinct_dates 를 함께 봐라.",
    "유니버스는 `cache trend-setup`과 같다: 그날 상장(폐지 포함, 생존편향 없음) · 끝자리 0 · 이름에 '스팩' 없음.",
    "PBR(밸류에이션) 축은 아직 없다 — 캐시에 과거 재무(B-1b)가 들어오기 전까지는 그룹 × 시총 2축이다.",
)


def _trading_calendar(conn: duckdb.DuckDBPyConnection) -> list[date]:
    rows = conn.execute("SELECT DISTINCT date FROM ohlcv WHERE code = 'U0001' ORDER BY date").fetchall()
    return [row[0] for row in rows]


def _state_for(reading: dict[str, Any]) -> str | None:
    return _STATUS_TO_STATE.get(reading["setup"]["status"])


# ---------------------------------------------------------------------------
# build: write `setup_state`, one sample day at a time
# ---------------------------------------------------------------------------


def _judge_universe(conn: duckdb.DuckDBPyConnection, d: date) -> list[tuple[str, str, str, float, int]]:
    """``(code, market, state, adj_close, list_count)`` for every judged, liquid stock on ``d``."""

    universe = cache_trend._universe(conn, d, None, None)
    if not universe:
        return []
    indices = cache_trend._indices(conn, d)
    series = cache_trend._series(conn, [row["code"] for row in universe], d)
    day = d.strftime("%Y%m%d")
    out: list[tuple[str, str, str, float, int]] = []
    for company in universe:
        prices = series.get(company["code"])
        if prices is None or prices.dates[-1] != day:
            continue
        index = indices.get(cache_trend._INDEX_FOR.get(company["market"], ""))
        if index is None or company["list_count"] is None:
            continue
        try:
            reading = trend_setup.analyze(prices.window(start=-trend_setup.WINDOW), index)
        except trend_setup.InsufficientHistory:
            continue
        state = _state_for(reading)
        if state is None:
            continue
        out.append((company["code"], company["market"], state, reading["close"], company["list_count"]))
    return out


def _mcap_buckets(values: list[float]) -> tuple[float, float]:
    array = np.array(values, dtype=np.float64)
    cut1, cut2 = np.quantile(array, [1 / 3, 2 / 3])
    return float(cut1), float(cut2)


def _bucket_of(mcap: float, cut1: float, cut2: float) -> int:
    if mcap <= cut1:
        return 0
    if mcap <= cut2:
        return 1
    return 2


_INSERT_SQL = (
    "INSERT INTO setup_state (sample_date, code, market, state, mcap_bucket, mcap, adj_close, index_code, "
    "index_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (sample_date, code) DO NOTHING"
)


def _build_date(conn: duckdb.DuckDBPyConnection, d: date) -> list[tuple[Any, ...]]:
    judged = _judge_universe(conn, d)
    if not judged:
        return []
    codes = [item[0] for item in judged]
    raw_close = dict(
        conn.execute(
            "SELECT code, close FROM ohlcv WHERE date = ? AND code IN (SELECT unnest(?::TEXT[]))",
            [d, codes],
        ).fetchall()
    )
    mcaps: dict[str, float] = {}
    for code, _market, _state, _adj_close, list_count in judged:
        close = raw_close.get(code)
        if close is not None and close > 0:
            mcaps[code] = close * list_count
    if not mcaps:
        return []
    cut1, cut2 = _mcap_buckets(list(mcaps.values()))

    day = d.strftime("%Y%m%d")
    index_by_market: dict[str, tuple[str, float]] = {}
    indices = cache_trend._indices(conn, d)
    for market, index_code in cache_trend._INDEX_FOR.items():
        index = indices.get(index_code)
        if index is not None and day in index.dates:
            index_by_market[market] = (index_code, float(index.closes[index.dates.index(day)]))

    rows = []
    for code, market, state, adj_close, _list_count in judged:
        mcap = mcaps.get(code)
        pair = index_by_market.get(market)
        if mcap is None or pair is None:
            continue
        index_code, index_close = pair
        rows.append((d, code, market, state, _bucket_of(mcap, cut1, cut2), mcap, adj_close, index_code, index_close))
    return rows


def build(conn: duckdb.DuckDBPyConnection, *, stride: int = SAMPLE_STRIDE, until: date | None = None) -> dict[str, Any]:
    """Incremental, idempotent: only sample dates after the table's current max are computed."""

    start = time.monotonic()
    calendar = _trading_calendar(conn)
    if until is not None:
        calendar = [d for d in calendar if d <= until]
    sample_dates = calendar[::stride]
    existing_row = conn.execute("SELECT max(sample_date) FROM setup_state").fetchone()
    existing_max = existing_row[0] if existing_row else None
    new_dates = [d for d in sample_dates if existing_max is None or d > existing_max]

    rows_added = 0
    for d in new_dates:
        rows = _build_date(conn, d)
        if rows:
            conn.executemany(_INSERT_SQL, rows)
            rows_added += len(rows)

    totals = conn.execute("SELECT count(*), count(DISTINCT sample_date), max(sample_date) FROM setup_state").fetchone()
    total_rows, total_dates, last_date = totals if totals else (0, 0, None)
    return {
        "stride": stride,
        "sample_dates": len(sample_dates),
        "dates_added": len(new_dates),
        "rows_added": rows_added,
        "seconds": round(time.monotonic() - start, 1),
        "table": {
            "rows": total_rows,
            "dates": total_dates,
            "last_sample_date": last_date.isoformat() if last_date else None,
        },
    }


# ---------------------------------------------------------------------------
# query: current cell, merge-up, forward excess return and touch rate
# ---------------------------------------------------------------------------

_CELL_SQL = {
    "group_mcap": (
        "SELECT sample_date, code, market, index_code, adj_close, index_close FROM setup_state "
        "WHERE state = ? AND mcap_bucket = ?"
    ),
    "group": "SELECT sample_date, code, market, index_code, adj_close, index_close FROM setup_state WHERE state = ?",
    "all": "SELECT sample_date, code, market, index_code, adj_close, index_close FROM setup_state",
}


def _resolve_cell(conn: duckdb.DuckDBPyConnection, state: str, bucket: int) -> tuple[str, list[tuple[Any, ...]]]:
    params_by_level = {"group_mcap": [state, bucket], "group": [state], "all": []}
    chosen: tuple[str, list[tuple[Any, ...]]] = ("all", [])
    for level in ("group_mcap", "group", "all"):
        rows = conn.execute(_CELL_SQL[level], params_by_level[level]).fetchall()
        chosen = (level, rows)
        if len(rows) >= MIN_SAMPLES:
            break
    return chosen


def _current_state(conn: duckdb.DuckDBPyConnection, code: str, market: str, as_of: date) -> str | None:
    series = cache_trend._series(conn, [code], as_of)
    prices = series.get(code)
    day = as_of.strftime("%Y%m%d")
    if prices is None or prices.dates[-1] != day:
        return None
    index = cache_trend._indices(conn, as_of).get(cache_trend._INDEX_FOR.get(market, ""))
    if index is None:
        return None
    try:
        reading = trend_setup.analyze(prices.window(start=-trend_setup.WINDOW), index)
    except trend_setup.InsufficientHistory:
        return None
    return _state_for(reading)


def _current_bucket(conn: duckdb.DuckDBPyConnection, code: str, as_of: date) -> dict[str, Any] | None:
    """Market-cap tercile of ``code`` within the whole ``as_of`` universe (pre-liquidity-filter).

    Fast on purpose: unlike ``build()``, this does not judge every stock's trend-setup (that
    is the ~0.5–1s `cache trend-setup` cost) — it is a plain close×shares join, so the cutoffs
    are computed over a slightly wider population than the historical cells (those drop
    illiquid stocks first). Noted in the output.
    """

    universe = cache_trend._universe(conn, as_of, None, None)
    codes = [row["code"] for row in universe]
    if code not in codes:
        return None
    rows = conn.execute(
        "SELECT o.code, o.close, c.list_count FROM ohlcv o JOIN company c ON c.code = o.code "
        "WHERE o.date = ? AND o.code IN (SELECT unnest(?::TEXT[])) AND o.close > 0 AND c.list_count IS NOT NULL",
        [as_of, codes],
    ).fetchall()
    mcaps = {row[0]: row[1] * row[2] for row in rows}
    if code not in mcaps or len(mcaps) < 3:
        return None
    cut1, cut2 = _mcap_buckets(list(mcaps.values()))
    return {
        "bucket": _bucket_of(mcaps[code], cut1, cut2),
        "mcap": mcaps[code],
        "universe_n": len(mcaps),
        "cut1": cut1,
        "cut2": cut2,
    }


def _forward_dates(calendar: list[date], horizon: int) -> dict[date, date]:
    return {d: calendar[i + horizon] for i, d in enumerate(calendar) if i + horizon < len(calendar)}


def _round(value: float | None, digits: int = 4) -> float | None:
    return None if value is None or not np.isfinite(value) else round(float(value), digits)


def _horizon_stats(
    conn: duckdb.DuckDBPyConnection,
    rows: list[tuple[Any, ...]],
    calendar: list[date],
    horizon: int,
    *,
    target_pct: float | None,
    stop_pct: float | None,
) -> dict[str, Any]:
    forward = _forward_dates(calendar, horizon)
    usable = [row for row in rows if row[0] in forward]
    empty = {
        "n": 0,
        "distinct_dates": 0,
        "p10": None,
        "p25": None,
        "p50": None,
        "p75": None,
        "p90": None,
        "mean": None,
        "share_positive": None,
        "touch": None,
    }
    if not usable:
        return empty
    # The touch rate only needs the high/low path, not the forward close — compute it even
    # when no sample has both a forward stock and index close (e.g. a thin index history).
    touch = (
        _touch_rates(conn, usable, forward, target_pct, stop_pct)
        if target_pct is not None and stop_pct is not None
        else None
    )
    codes = [row[1] for row in usable]
    fwd_dates = [forward[row[0]] for row in usable]
    idx = list(range(len(usable)))
    stock_fwd = dict(
        conn.execute(
            "SELECT u.i, o.close * COALESCE(NULLIF(o.adj_factor, 0), 1) FROM "
            "(SELECT unnest(?::INT[]) AS i, unnest(?::TEXT[]) AS code, unnest(?::DATE[]) AS d) u "
            "JOIN ohlcv o ON o.code = u.code AND o.date = u.d",
            [idx, codes, fwd_dates],
        ).fetchall()
    )
    index_codes = [row[3] for row in usable]
    index_fwd = dict(
        conn.execute(
            "SELECT u.i, o.close * COALESCE(NULLIF(o.adj_factor, 0), 1) FROM "
            "(SELECT unnest(?::INT[]) AS i, unnest(?::TEXT[]) AS code, unnest(?::DATE[]) AS d) u "
            "JOIN ohlcv o ON o.code = u.code AND o.date = u.d",
            [idx, index_codes, fwd_dates],
        ).fetchall()
    )
    excess: list[float] = []
    dates_seen: set[date] = set()
    for i, row in enumerate(usable):
        sample_date, _code, _market, _index_code, base_close, base_index = row
        fwd_close = stock_fwd.get(i)
        fwd_index = index_fwd.get(i)
        if fwd_close is None or fwd_index is None or not base_close or not base_index:
            continue
        stock_ret = fwd_close / base_close - 1
        index_ret = fwd_index / base_index - 1
        excess.append(stock_ret - index_ret)
        dates_seen.add(sample_date)
    if not excess:
        return {**empty, "touch": touch}
    array = np.array(excess, dtype=np.float64)
    quantiles = np.quantile(array, _QUANTILES)
    return {
        "n": len(excess),
        "distinct_dates": len(dates_seen),
        "p10": _round(float(quantiles[0])),
        "p25": _round(float(quantiles[1])),
        "p50": _round(float(quantiles[2])),
        "p75": _round(float(quantiles[3])),
        "p90": _round(float(quantiles[4])),
        "mean": _round(float(array.mean())),
        "share_positive": _round(float((array > 0).mean())),
        "touch": touch,
    }


def _touch_rates(
    conn: duckdb.DuckDBPyConnection,
    usable: list[tuple[Any, ...]],
    forward: dict[date, date],
    target_pct: float,
    stop_pct: float,
) -> dict[str, Any]:
    """Share of samples whose adjusted high reached +target before the low reached −stop.

    A same-day hit of both is counted as a stop (the conservative read — stop-outs are
    marked as realized losses, not netted against an intraday high that may have come first).
    """

    idx = list(range(len(usable)))
    codes = [row[1] for row in usable]
    starts = [row[0] for row in usable]
    ends = [forward[row[0]] for row in usable]
    bars = conn.execute(
        "SELECT u.i, o.date, o.high * COALESCE(NULLIF(o.adj_factor, 0), 1), o.low * COALESCE(NULLIF(o.adj_factor, 0), 1) "
        "FROM (SELECT unnest(?::INT[]) AS i, unnest(?::TEXT[]) AS code, unnest(?::DATE[]) AS s, "
        "unnest(?::DATE[]) AS e) u "
        "JOIN ohlcv o ON o.code = u.code AND o.date > u.s AND o.date <= u.e "
        "ORDER BY u.i, o.date",
        [idx, codes, starts, ends],
    ).fetchall()
    by_sample: dict[int, list[tuple[date, float, float]]] = {}
    for i, day, high, low in bars:
        by_sample.setdefault(i, []).append((day, high, low))

    target_hits = stop_hits = neither = 0
    n = 0
    for i, row in enumerate(usable):
        base_close = row[4]
        if not base_close:
            continue
        path = by_sample.get(i)
        if not path:
            continue
        n += 1
        target_price = base_close * (1 + target_pct / 100)
        stop_price = base_close * (1 - stop_pct / 100)
        target_date = next((day for day, high, _low in path if high is not None and high >= target_price), None)
        stop_date = next((day for day, _high, low in path if low is not None and low <= stop_price), None)
        if target_date is None and stop_date is None:
            neither += 1
        elif stop_date is not None and (target_date is None or stop_date <= target_date):
            stop_hits += 1
        else:
            target_hits += 1
    if n == 0:
        return {
            "target_pct": target_pct,
            "stop_pct": stop_pct,
            "n": 0,
            "target_rate": None,
            "stop_rate": None,
            "neither_rate": None,
        }
    return {
        "target_pct": target_pct,
        "stop_pct": stop_pct,
        "n": n,
        "target_rate": _round(target_hits / n),
        "stop_rate": _round(stop_hits / n),
        "neither_rate": _round(neither / n),
    }


def query(
    conn: duckdb.DuckDBPyConnection,
    code: str,
    *,
    as_of: date | None = None,
    horizons: tuple[int, ...] = DEFAULT_HORIZONS,
    target_pct: float | None = None,
    stop_pct: float | None = None,
) -> dict[str, Any]:
    calendar = _trading_calendar(conn)
    if not calendar:
        raise CliError("The cache has no index bars.", exit_code=EXIT_USAGE, hint="Run `cache load` first.")
    if as_of is None:
        as_of = calendar[-1]
    elif as_of not in set(calendar):
        raise CliError(
            f"No KOSPI bar on {as_of:%Y%m%d} in the cache (holiday, or not loaded yet).",
            exit_code=EXIT_USAGE,
        )
    companies = read_company(conn, code=code)["companies"]
    if not companies:
        raise CliError(f"`{code}` is not in `cache company`.", exit_code=EXIT_USAGE, hint="Run `cache load` first.")
    company = companies[0]
    market = company["market"]
    payload: dict[str, Any] = {
        "code": code,
        "as_of": as_of.isoformat(),
        "market": market,
        "notes": list(NOTES),
    }
    if market not in cache_trend._INDEX_FOR:
        payload["cell"] = None
        payload["hint"] = "KOSPI/KOSDAQ 종목만 지원한다."
        return payload

    build_row = conn.execute("SELECT count(*) FROM setup_state").fetchone()
    if not build_row or not build_row[0]:
        payload["cell"] = None
        payload["hint"] = "`cache base-rate-build` 를 먼저 돌린다."
        return payload

    state = _current_state(conn, code, market, as_of)
    bucket_info = _current_bucket(conn, code, as_of)
    if state is None or bucket_info is None:
        payload["cell"] = None
        payload["state"] = state
        payload["hint"] = "현재 상태를 판정할 수 없다(거래대금 미달·신규상장·결측 상장주식수 등)."
        return payload

    bucket = bucket_info["bucket"]
    payload["state"] = {"state": state, "mcap_bucket": bucket, "mcap": _round(bucket_info["mcap"], 0)}
    payload["notes"].append(f"현재 시총 3분위는 {bucket_info['universe_n']}종목(유동성 필터 전 유니버스) 기준이다.")

    level, rows = _resolve_cell(conn, state, bucket)
    distinct_all = {(r[0], r[1]) for r in rows}
    payload["cell"] = {
        "level": level,
        "state_filter": state if level != "all" else None,
        "mcap_bucket_filter": bucket if level == "group_mcap" else None,
        "n": len(rows),
        "distinct_codes": len({r[1] for r in rows}),
        "distinct_dates": len({r[0] for r in rows}),
    }
    if len(distinct_all) < MIN_SAMPLES:
        payload["notes"].append(f"칸을 '{level}' 수준까지 합쳐도 표본이 {MIN_SAMPLES}개 미만이다.")

    payload["horizons"] = {
        str(h): _horizon_stats(conn, rows, calendar, h, target_pct=target_pct, stop_pct=stop_pct) for h in horizons
    }
    return payload
