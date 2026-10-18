"""`ohlcv` table: unadjusted KIS daily bars for every `company` row plus three indices.

Unadjusted prices never change after the fact, so a daily run only appends — except that
each run re-fetches a stock's last 60 stored days and, if any close differs (a vendor
correction), replaces that stock's whole history. The bar's own corporate-action markers
(`flng_cls_code`, `prtt_rate`, `revl_issu_reas`) are stored as sent: they are what was known
on that day.

KIS `chart.period` has no cursor: at most 100 rows per call inside a date window (indices: 50),
newest first. Windows walk backwards from the end, never stopping on an empty window — a
long trading halt is an empty window in the middle of a history, not its start.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any, Callable

import duckdb

from cluefin_openapi_cli.cache.throttle import kis_call
from cluefin_openapi_cli.ohlcv import adj_price_flag

__all__ = ["INDICES", "Bar", "BarLoadStats", "fetch_index_bars", "fetch_stock_bars", "load_bars"]

_STOCK_WINDOW_DAYS = 140  # ~95 trading days, under the 100-row cap
_INDEX_WINDOW_DAYS = 70  # ~48 trading days, under the 50-row cap
RECHECK_ROWS = 60
_INSERT_CHUNK = 500
# Cache code -> KIS sector code (FID_INPUT_ISCD with market U).
INDICES: tuple[tuple[str, str], ...] = (("U0001", "0001"), ("U1001", "1001"), ("U2001", "2001"))

_COLUMNS = (
    "code",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "value",
    "lock_code",
    "prtt_rate",
    "reval_code",
    "loaded_at",
)


@dataclass(frozen=True, slots=True)
class Bar:
    date: date
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    volume: float | None
    value: float | None
    lock_code: str | None = None
    prtt_rate: float | None = None
    reval_code: str | None = None


@dataclass(slots=True)
class BarLoadStats:
    codes: int = 0
    loaded: int = 0
    skipped: int = 0
    rows: int = 0
    replaced: int = 0
    calls: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "codes": self.codes,
            "loaded": self.loaded,
            "skipped": self.skipped,
            "rows": self.rows,
            "replaced": self.replaced,
            "calls": self.calls,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _number(raw: Any, *, price: bool = False) -> float | None:
    text = str(raw if raw is not None else "").strip().replace(",", "")
    if not text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if math.isnan(value) or math.isinf(value):
        return None
    # A zero price is a missing value (halted days), never a crash to zero.
    return None if price and value <= 0 else value


def _code_text(raw: Any) -> str | None:
    text = str(raw or "").strip()
    return text or None


def _day(raw: Any) -> date | None:
    text = str(raw or "").strip()
    try:
        return datetime.strptime(text, "%Y%m%d").date() if len(text) == 8 else None
    except ValueError:
        return None


def _stock_bar(item: Any) -> Bar | None:
    day = _day(item.stck_bsop_date)
    if day is None:
        return None
    return Bar(
        date=day,
        open=_number(item.stck_oprc, price=True),
        high=_number(item.stck_hgpr, price=True),
        low=_number(item.stck_lwpr, price=True),
        close=_number(item.stck_clpr, price=True),
        volume=_number(item.acml_vol),
        value=_number(item.acml_tr_pbmn),
        lock_code=_code_text(item.flng_cls_code),
        prtt_rate=_number(item.prtt_rate),
        reval_code=_code_text(item.revl_issu_reas),
    )


def _index_bar(item: Any) -> Bar | None:
    day = _day(item.stck_bsop_date)
    if day is None:
        return None
    return Bar(
        date=day,
        open=_number(item.bstp_nmix_oprc, price=True),
        high=_number(item.bstp_nmix_hgpr, price=True),
        low=_number(item.bstp_nmix_lwpr, price=True),
        close=_number(item.bstp_nmix_prpr, price=True),
        volume=_number(item.acml_vol),
        value=_number(item.acml_tr_pbmn),
    )


def _walk(fetch_page: Callable[[date, date], list[Bar]], start: date, end: date, window_days: int) -> list[Bar]:
    by_date: dict[date, Bar] = {}
    window_end = end
    while window_end >= start:
        window_start = max(start, window_end - timedelta(days=window_days))
        page = fetch_page(window_start, window_end)
        for bar in page:
            if start <= bar.date <= end:
                by_date[bar.date] = bar
        oldest = min((bar.date for bar in page), default=None)
        # A page at the row cap ends inside the window: continue from the day before its oldest row.
        window_end = (oldest if oldest is not None and oldest > window_start else window_start) - timedelta(days=1)
    return [by_date[day] for day in sorted(by_date)]


def fetch_stock_bars(
    kis: Any, code: str, start: date, end: date, *, adjusted: bool = False, stats: BarLoadStats | None = None, **call
) -> list[Bar]:
    flag = adj_price_flag("chart.period", adjusted=adjusted)

    def page(window_start: date, window_end: date) -> list[Bar]:
        if stats is not None:
            stats.calls += 1
        response = kis_call(
            kis.domestic_basic_quote.get_stock_period_quote,
            "J",
            code,
            window_start.strftime("%Y%m%d"),
            window_end.strftime("%Y%m%d"),
            "D",
            flag,
            **call,
        )
        return [bar for bar in map(_stock_bar, getattr(response.body, "output2", None) or []) if bar]

    return _walk(page, start, end, _STOCK_WINDOW_DAYS)


def fetch_index_bars(
    kis: Any, sector_code: str, start: date, end: date, *, stats: BarLoadStats | None = None, **call
) -> list[Bar]:
    def page(window_start: date, window_end: date) -> list[Bar]:
        if stats is not None:
            stats.calls += 1
        response = kis_call(
            kis.domestic_issue_other.get_sector_period_quote,
            "U",
            sector_code,
            window_start.strftime("%Y%m%d"),
            window_end.strftime("%Y%m%d"),
            "D",
            **call,
        )
        return [bar for bar in map(_index_bar, getattr(response.body, "output2", None) or []) if bar]

    return _walk(page, start, end, _INDEX_WINDOW_DAYS)


def _insert(conn: duckdb.DuckDBPyConnection, code: str, bars: list[Bar], loaded_at: datetime) -> None:
    placeholders = "(" + ", ".join("?" * len(_COLUMNS)) + ")"
    for offset in range(0, len(bars), _INSERT_CHUNK):
        chunk = bars[offset : offset + _INSERT_CHUNK]
        values: list[Any] = []
        for bar in chunk:
            values.extend(
                (
                    code,
                    bar.date,
                    bar.open,
                    bar.high,
                    bar.low,
                    bar.close,
                    bar.volume,
                    bar.value,
                    bar.lock_code,
                    bar.prtt_rate,
                    bar.reval_code,
                    loaded_at,
                )
            )
        conn.execute(
            f"INSERT INTO ohlcv ({', '.join(_COLUMNS)}) VALUES " + ", ".join([placeholders] * len(chunk)),
            values,
        )


@dataclass(frozen=True, slots=True)
class _Target:
    code: str
    start: date
    end: date
    delisted_on: date | None


def _targets(conn: duckdb.DuckDBPyConnection, *, since: date, last_day: date) -> list[_Target]:
    rows = conn.execute("SELECT code, listed_on, delisted_on FROM company ORDER BY code").fetchall()
    targets = []
    for code, listed_on, delisted_on in rows:
        start = max(since, listed_on) if listed_on else since
        end = min(last_day, delisted_on) if delisted_on else last_day
        targets.append(_Target(code, start, end, delisted_on))
    return targets


def _sync(
    conn: duckdb.DuckDBPyConnection,
    code: str,
    start: date,
    end: date,
    fetch: Callable[[date, date], list[Bar]],
    stats: BarLoadStats,
    now: datetime,
) -> None:
    """Append new bars; replace the code's history when a re-fetched recent close differs."""

    recent = conn.execute(
        "SELECT date, close FROM ohlcv WHERE code = ? ORDER BY date DESC LIMIT ?", [code, RECHECK_ROWS]
    ).fetchall()
    if not recent:
        bars = fetch(start, end)
        replace = False
    else:
        recheck_from = recent[-1][0]
        fresh = fetch(recheck_from, end)
        by_date = {bar.date: bar.close for bar in fresh}
        replace = any(by_date.get(day, float("nan")) != close for day, close in recent if close is not None)
        if replace:
            bars = fetch(start, end)
        else:
            last = recent[0][0]
            bars = [bar for bar in fresh if bar.date > last]
    conn.begin()
    try:
        if replace:
            conn.execute("DELETE FROM ohlcv WHERE code = ?", [code])
            # The re-inserted bars carry the default factor; make the next adj run start over.
            conn.execute("DELETE FROM adj_log WHERE code = ?", [code])
            stats.replaced += 1
        _insert(conn, code, bars, now)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    stats.rows += len(bars)
    stats.loaded += 1


def _complete_delisted(conn: duckdb.DuckDBPyConnection, target: _Target) -> bool:
    """A delisted code whose bars were loaded after its delisting needs nothing more."""

    if target.delisted_on is None:
        return False
    row = conn.execute("SELECT max(loaded_at) FROM ohlcv WHERE code = ?", [target.code]).fetchone()
    return bool(row and row[0] is not None and row[0].date() > target.delisted_on)


def load_bars(
    conn: duckdb.DuckDBPyConnection,
    *,
    kis: Any,
    since: date,
    last_day: date,
    progress: Callable[[str], None] = lambda _message: None,
    sleep: Callable[[float], None] | None = None,
) -> BarLoadStats:
    """Stocks in `company` then the indices, one KIS call at a time; each code commits on its own."""

    stats = BarLoadStats()
    call = {"sleep": sleep} if sleep is not None else {}
    targets = _targets(conn, since=since, last_day=last_day)
    stats.codes = len(targets) + len(INDICES)
    started = time.perf_counter()
    for index, target in enumerate(targets, 1):
        if target.start > target.end or _complete_delisted(conn, target):
            stats.skipped += 1
            continue
        try:
            now = datetime.now()
            _sync(
                conn,
                target.code,
                target.start,
                target.end,
                lambda s, e, code=target.code: fetch_stock_bars(kis, code, s, e, stats=stats, **call),
                stats,
                now,
            )
            if target.delisted_on is not None:
                # Mark the history complete even when nothing new arrived (see _complete_delisted).
                conn.execute(
                    "UPDATE ohlcv SET loaded_at = ? WHERE code = ? AND date = (SELECT max(date) FROM ohlcv WHERE code = ?)",
                    [now, target.code, target.code],
                )
        except Exception as exc:  # noqa: BLE001 - one bad code must not stop a bulk load
            stats.errors.append({"code": target.code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
        if index % 100 == 0:
            elapsed = time.perf_counter() - started
            eta = elapsed / index * (len(targets) - index)
            progress(
                f"ohlcv: {index}/{len(targets)} codes, {stats.rows} rows, {stats.calls} calls, "
                f"{elapsed / 60:.1f} min, ~{eta / 60:.0f} min left"
            )
    for cache_code, sector_code in INDICES:
        try:
            _sync(
                conn,
                cache_code,
                since,
                last_day,
                lambda s, e, sector=sector_code: fetch_index_bars(kis, sector, s, e, stats=stats, **call),
                stats,
                datetime.now(),
            )
        except Exception as exc:  # noqa: BLE001
            stats.errors.append({"code": cache_code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
    return stats
