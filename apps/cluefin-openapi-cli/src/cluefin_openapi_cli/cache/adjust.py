"""`ohlcv.adj_factor`: per-day ratio of KIS's adjusted close to the stored unadjusted close.

Adjusted price = close × adj_factor reproduces KIS `chart.period` adjusted prices exactly. The
factor is past-dependent on future events (a split today rescales every earlier day), so it is
recomputed for a whole stock when a new event shows up, while the unadjusted bars stay put.

To spare calls, a stock is first probed with one adjusted window at the start of its history:
if every adjusted close there equals the unadjusted close, nothing between then and now was
adjusted and the factor stays 1.0 (an event exactly undone by a later one would slip through —
accepted). Otherwise its full adjusted history is fetched. A daily run re-fetches the last 60
stored days and compares with the stored factor; KIS rounds adjusted prices to the won, so a
difference above half a won means a new event and the stock is recomputed.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

import duckdb

from cluefin_openapi_cli.cache.bars import RECHECK_ROWS, BarLoadStats, fetch_stock_bars
from cluefin_openapi_cli.clock import now_kst

__all__ = ["AdjustStats", "load_adjustments"]

_PROBE_DAYS = 100  # ~70 trading days: always a single call under the 100-row cap
_ROUNDING = 0.5
_UPDATE_SQL = (
    "UPDATE ohlcv SET adj_factor = f.factor "
    "FROM (SELECT unnest(?::DATE[]) AS day, unnest(?::DOUBLE[]) AS factor) AS f "
    "WHERE ohlcv.code = ? AND ohlcv.date = f.day"
)


# frozen 아님: 적재하면서 건수를 더해 가는 누적기.
@dataclass(slots=True)
class AdjustStats:
    codes: int = 0
    probed_flat: int = 0
    recomputed: int = 0
    extended: int = 0
    skipped: int = 0
    calls: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "codes": self.codes,
            "no_events": self.probed_flat,
            "recomputed": self.recomputed,
            "extended": self.extended,
            "skipped": self.skipped,
            "calls": self.calls,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _factors(stored: list[tuple[date, float | None]], adjusted: dict[date, float | None]) -> list[tuple[date, float]]:
    """Factor per stored day; a day without both closes takes the next (newer) day's factor."""

    result: list[tuple[date, float]] = []
    carry = 1.0
    for day, close in sorted(stored, reverse=True):
        adj = adjusted.get(day)
        if close and adj:
            carry = adj / close
        result.append((day, carry))
    return result


def _write(conn: duckdb.DuckDBPyConnection, code: str, factors: list[tuple[date, float]]) -> None:
    if factors:
        conn.execute(_UPDATE_SQL, [[day for day, _ in factors], [factor for _, factor in factors], code])


def _stored(conn: duckdb.DuckDBPyConnection, code: str, since: date | None = None) -> list[tuple[Any, ...]]:
    if since is None:
        return conn.execute("SELECT date, close, adj_factor FROM ohlcv WHERE code = ? ORDER BY date", [code]).fetchall()
    return conn.execute(
        "SELECT date, close, adj_factor FROM ohlcv WHERE code = ? AND date >= ? ORDER BY date", [code, since]
    ).fetchall()


def _closes(bars: list[Any]) -> dict[date, float | None]:
    return {bar.date: bar.close for bar in bars}


def _recompute(conn, kis, code, first: date, last: date, stats, bar_stats, call) -> None:
    adjusted = _closes(fetch_stock_bars(kis, code, first, last, adjusted=True, stats=bar_stats, **call))
    rows = _stored(conn, code)
    conn.begin()
    try:
        _write(conn, code, _factors([(day, close) for day, close, _ in rows], adjusted))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    stats.recomputed += 1


def _first_time(conn, kis, code, first: date, last: date, stats, bar_stats, call) -> None:
    probe_end = min(last, first + timedelta(days=_PROBE_DAYS))
    adjusted = _closes(fetch_stock_bars(kis, code, first, probe_end, adjusted=True, stats=bar_stats, **call))
    stored = {day: close for day, close, _ in _stored(conn, code) if day <= probe_end}
    flat = all(adjusted.get(day) == close for day, close in stored.items() if close and adjusted.get(day))
    if flat:
        conn.execute("UPDATE ohlcv SET adj_factor = 1.0 WHERE code = ? AND adj_factor IS DISTINCT FROM 1.0", [code])
        stats.probed_flat += 1
        return
    _recompute(conn, kis, code, first, last, stats, bar_stats, call)


def _incremental(conn, kis, code, first: date, last: date, checked_through: date, stats, bar_stats, call) -> None:
    recent = conn.execute(
        "SELECT date FROM ohlcv WHERE code = ? AND date <= ? ORDER BY date DESC LIMIT ?",
        [code, checked_through, RECHECK_ROWS],
    ).fetchall()
    window_start = recent[-1][0] if recent else first
    adjusted = _closes(fetch_stock_bars(kis, code, window_start, last, adjusted=True, stats=bar_stats, **call))
    rows = _stored(conn, code, window_start)
    moved = any(
        abs(adjusted[day] - close * factor) > _ROUNDING
        for day, close, factor in rows
        if day <= checked_through and close and factor and adjusted.get(day)
    )
    if moved:
        _recompute(conn, kis, code, first, last, stats, bar_stats, call)
        return
    newer = [(day, close) for day, close, _ in rows if day > checked_through]
    if newer:
        _write(conn, code, _factors(newer, adjusted))
    stats.extended += 1


def load_adjustments(
    conn: duckdb.DuckDBPyConnection,
    *,
    kis: Any,
    progress: Callable[[str], None] = lambda _message: None,
    sleep: Callable[[float], None] | None = None,
) -> AdjustStats:
    """Bring `adj_factor` up to each stock's last stored bar, one KIS call at a time."""

    stats = AdjustStats()
    bar_stats = BarLoadStats()
    call = {"sleep": sleep} if sleep is not None else {}
    rows = conn.execute(
        "SELECT o.code, min(o.date), max(o.date), a.checked_through FROM ohlcv o "
        "JOIN company c ON c.code = o.code LEFT JOIN adj_log a ON a.code = o.code "
        "GROUP BY o.code, a.checked_through ORDER BY o.code"
    ).fetchall()
    stats.codes = len(rows)
    started = time.perf_counter()
    for index, (code, first, last, checked_through) in enumerate(rows, 1):
        if checked_through is not None and checked_through >= last:
            stats.skipped += 1
            continue
        try:
            if checked_through is None:
                _first_time(conn, kis, code, first, last, stats, bar_stats, call)
            else:
                _incremental(conn, kis, code, first, last, checked_through, stats, bar_stats, call)
            conn.execute(
                "INSERT INTO adj_log VALUES (?, ?, ?) ON CONFLICT (code) DO UPDATE SET "
                "checked_through = excluded.checked_through, computed_at = excluded.computed_at",
                [code, last, now_kst()],
            )
        except Exception as exc:  # noqa: BLE001 - one bad code must not stop a bulk load
            stats.errors.append({"code": code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
        if index % 100 == 0:
            elapsed = time.perf_counter() - started
            eta = elapsed / index * (len(rows) - index)
            progress(
                f"adj: {index}/{len(rows)} codes, {stats.recomputed} recomputed, {bar_stats.calls} calls, "
                f"{elapsed / 60:.1f} min, ~{eta / 60:.0f} min left"
            )
    stats.calls = bar_stats.calls
    return stats
