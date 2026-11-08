"""`review track`: check each recorded verdict against the cache's daily bars.

For every line of `research/verdicts.jsonl` it walks the trading days after the reference date, up to the horizon,
and reports which price level was crossed first (watch: re-check / exit price; buy·sell: target / stop), the return
since the reference close, the excess over the stock's market index and the best/worst close on the way. Only the
local cache is read — no broker calls — so the answer is as fresh as the last `cache load`.

Prices: bars are adjusted (`close × adj_factor`, as `read_ohlcv(adjusted=True)`), and recorded levels, written in
the reference day's prices, are scaled by that day's factor so a later split or dividend does not move them.
Levels are checked on daily closes, not intraday highs/lows.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import duckdb

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["Bar", "load_records", "summarize", "track", "track_record"]

_INDEX_FOR = {"KOSPI": "U0001", "KOSDAQ": "U1001"}
# (level name, field holding the price, True when crossing means close >= price)
_LEVELS: dict[str, tuple[tuple[str, str, bool], ...]] = {
    "watch": (("entry_above", "trigger", True), ("exit_below", "trigger", False)),
    "hold": (("entry_above", "trigger", True), ("exit_below", "trigger", False)),
    "buy": (("target", "", True), ("stop", "", False)),
    "sell": (("target", "", False), ("stop", "", True)),
}
_BARS_SQL = (
    "SELECT date, close * COALESCE(NULLIF(adj_factor, 0), 1), COALESCE(NULLIF(adj_factor, 0), 1) FROM ohlcv "
    "WHERE code = ? AND date >= ? AND close > 0 ORDER BY date LIMIT ?"
)
_INDEX_SQL = "SELECT date, close FROM ohlcv WHERE code = ? AND date BETWEEN ? AND ? AND close > 0"


@dataclass(frozen=True, slots=True)
class Bar:
    day: date
    close: float  # adjusted
    factor: float


def load_records(file: Path) -> list[dict[str, Any]]:
    if not file.is_file():
        raise CliError(f"No verdict log at {file}.", exit_code=EXIT_USAGE, hint="Add verdicts with `review record`.")
    return [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]


def _pct(now: float, base: float) -> float:
    return round((now / base - 1) * 100, 2)


def _levels(record: dict[str, Any], factor: float) -> list[tuple[str, float, bool]]:
    out: list[tuple[str, float, bool]] = []
    for name, holder, upward in _LEVELS.get(record["verdict"], ()):
        source = (record.get(holder) or {}) if holder else record
        price = source.get(name)
        if isinstance(price, int | float) and price > 0:
            out.append((name, price * factor, upward))
    return out


def _first_cross(bars: list[Bar], levels: list[tuple[str, float, bool]]) -> dict[str, Any] | None:
    for bar in bars:
        for name, price, upward in levels:
            if (bar.close >= price) if upward else (bar.close <= price):
                return {"level": name, "on": bar.day.isoformat(), "close": round(bar.close, 2)}
    return None


def track_record(
    record: dict[str, Any], bars: list[Bar], index_close: dict[date, float], cache_as_of: date | None
) -> dict[str, Any]:
    """``bars`` start at the reference date (inclusive); ``index_close`` covers the same days."""

    ref_day = date.fromisoformat(record["reference_price"]["date"])
    row: dict[str, Any] = {
        "id": record["id"],
        "stock_code": record["stock_code"],
        "stock_name": record["stock_name"],
        "verdict": record["verdict"],
        "horizon_days": record["horizon_days"],
    }
    if not bars or bars[0].day != ref_day:
        as_of = cache_as_of.isoformat() if cache_as_of else None
        return row | {"status": "no_data", "cache_as_of": as_of}
    ref, path = bars[0], bars[1 : record["horizon_days"] + 1]
    last = path[-1] if path else ref
    row |= {
        "status": "closed" if len(path) >= record["horizon_days"] else "open",
        "days_seen": len(path),
        "as_of": last.day.isoformat(),
        "return_pct": _pct(last.close, ref.close),
        "max_up_pct": _pct(max((b.close for b in path), default=ref.close), ref.close),
        "max_down_pct": _pct(min((b.close for b in path), default=ref.close), ref.close),
        "first_cross": None,
    }
    index_ref, index_last = index_close.get(ref.day), index_close.get(last.day)
    if index_ref and index_last:
        row["index_return_pct"] = _pct(index_last, index_ref)
        row["excess_pct"] = round(row["return_pct"] - row["index_return_pct"], 2)
    cross = _first_cross(path, _levels(record, ref.factor))
    if cross is not None:
        cross["return_after_pct"] = _pct(last.close, cross["close"])
        row["first_cross"] = cross
    return row


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Per verdict label: counts, how often each level was crossed first, mean excess of closed verdicts."""

    out: dict[str, Any] = {}
    for row in rows:
        label = out.setdefault(
            row["verdict"], {"count": 0, "closed": 0, "open": 0, "no_data": 0, "first_cross": {}, "_excess": []}
        )
        label["count"] += 1
        label[row["status"]] += 1
        cross = row.get("first_cross")
        if cross:
            label["first_cross"][cross["level"]] = label["first_cross"].get(cross["level"], 0) + 1
        if row["status"] == "closed" and "excess_pct" in row:
            label["_excess"].append(row["excess_pct"])
    for label in out.values():
        excess = label.pop("_excess")
        label["mean_excess_pct_closed"] = round(sum(excess) / len(excess), 2) if excess else None
    return out


def _market(conn: duckdb.DuckDBPyConnection, code: str) -> str | None:
    row = conn.execute("SELECT market FROM company WHERE code = ?", [code]).fetchone()
    return row[0] if row else None


def _rows_for(conn: duckdb.DuckDBPyConnection, record: dict[str, Any], cache_as_of: date | None) -> dict[str, Any]:
    ref_day = date.fromisoformat(record["reference_price"]["date"])
    raw = conn.execute(_BARS_SQL, [record["stock_code"], ref_day, record["horizon_days"] + 1]).fetchall()
    bars = [Bar(day=d, close=c, factor=f) for d, c, f in raw]
    index_close: dict[date, float] = {}
    index_code = _INDEX_FOR.get(_market(conn, record["stock_code"]) or "")
    if bars and index_code:
        rows = conn.execute(_INDEX_SQL, [index_code, bars[0].day, bars[-1].day]).fetchall()
        index_close = dict(rows)
    row = track_record(record, bars, index_close, cache_as_of)
    row["index"] = index_code
    return row


def track(conn: duckdb.DuckDBPyConnection, records: list[dict[str, Any]]) -> dict[str, Any]:
    cache_as_of = conn.execute("SELECT max(date) FROM ohlcv WHERE code = 'U0001'").fetchone()
    as_of = cache_as_of[0] if cache_as_of else None
    rows = [_rows_for(conn, record, as_of) for record in records]
    return {
        "cache_as_of": as_of.isoformat() if as_of else None,
        "summary": summarize(rows),
        "verdicts": rows,
        "notes": [
            "Adjusted closes; recorded levels are scaled by the reference day's adj_factor. Levels are checked on "
            "daily closes, not intraday highs/lows.",
            "status open: the horizon has not passed in the cache yet. no_data: the cache has no bar on the "
            "reference date (load the cache past it, or the stock is not in it).",
            "excess_pct = return_pct − the stock's market index (KOSPI U0001 / KOSDAQ U1001) over the same days.",
        ],
    }
