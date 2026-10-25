"""`theme`·`theme_member` tables: a daily snapshot of Kiwoom's theme groups and their stocks.

Kiwoom answers with today's values only (no as-of argument), so past days exist only for
snapshots taken on them. KIS has no domestic theme API. Measured 2026-10-25: 142 themes in two
ka90001 pages, one ka90002 per theme (max 26 stocks, never a second page), ~50 s in all.

Kiwoom's period returns are on **unadjusted** prices (a 10:1 reverse split showed as +905%)
and a theme's return is the plain mean of its stocks', so they are stored for reference only;
`cache trend-setup` ranks themes on the cache's adjusted returns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any, Callable

import duckdb

from cluefin_openapi_cli.cache.bars import fetch_index_bars

__all__ = ["ThemeLoadStats", "load_theme"]

PERIOD_DAYS = 20
_MAX_PAGES = 10


@dataclass(slots=True)
class ThemeLoadStats:
    as_of: date | None = None
    themes: int = 0
    members: int = 0
    calls: int = 0
    skipped: str | None = None
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat() if self.as_of else None,
            "themes": self.themes,
            "members": self.members,
            "calls": self.calls,
            "skipped": self.skipped,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _number(raw: Any) -> float | None:
    text = str(raw or "").replace(",", "").replace("+", "").strip()
    try:
        return float(text) if text else None
    except ValueError:
        return None


def _count(raw: Any) -> int | None:
    value = _number(raw)
    return int(value) if value is not None else None


def _snapshot_day(kis: Any, last_day: date, stats: ThemeLoadStats) -> date | None:
    """The last trading day up to ``last_day``, from KIS index bars (holidays have none)."""

    stats.calls += 1
    bars = fetch_index_bars(kis, "0001", last_day - timedelta(days=14), last_day)
    return max((bar.date for bar in bars), default=None)


def _groups(kiwoom: Any, stats: ThemeLoadStats) -> list[Any]:
    groups: list[Any] = []
    cont, key = "N", ""
    for _ in range(_MAX_PAGES):
        stats.calls += 1
        response = kiwoom.theme.get_theme_group("0", str(PERIOD_DAYS), "", "1", "1", cont_yn=cont, next_key=key)
        groups.extend(response.body.thema_grp or [])
        if response.headers.cont_yn != "Y":
            break
        cont, key = "Y", response.headers.next_key
    return groups


def load_theme(
    conn: duckdb.DuckDBPyConnection,
    *,
    kiwoom: Any,
    kis: Any,
    today: date,
    last_day: date,
    progress: Callable[[str], None] = lambda _message: None,
) -> ThemeLoadStats:
    """Snapshot every theme and its stocks under the last closed trading day; a rerun replaces it."""

    stats = ThemeLoadStats()
    if today.weekday() < 5 and last_day < today:
        # Before 16:00 KST on a weekday Kiwoom's values are intraday; other parts still run.
        stats.skipped = "intraday"
        return stats
    as_of = _snapshot_day(kis, last_day, stats)
    if as_of is None:
        stats.errors.append({"code": "U0001", "error": f"no index bar up to {last_day.isoformat()}"})
        return stats
    stats.as_of = as_of
    groups = _groups(kiwoom, stats)
    now = datetime.now()
    themes, members = [], []
    for index, group in enumerate(groups, 1):
        code = str(group.thema_grp_cd).strip()
        try:
            stats.calls += 1
            rows = kiwoom.theme.get_theme_group_stocks(code, "1", str(PERIOD_DAYS)).body.thema_comp_stk or []
        except Exception as exc:  # noqa: BLE001 - one bad theme must not stop the snapshot
            stats.errors.append({"code": code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        themes.append(
            (
                as_of,
                code,
                group.thema_nm,
                _count(group.stk_num),
                _number(group.flu_rt),
                _number(group.dt_prft_rt),
                PERIOD_DAYS,
                _count(group.rising_stk_num),
                _count(group.fall_stk_num),
                group.main_stk,
                now,
            )
        )
        members += [
            (as_of, code, str(row.stk_cd).strip(), row.stk_nm, _number(row.flu_rt), _number(row.dt_prft_rt_n))
            for row in rows
        ]
        if index % 50 == 0:
            progress(f"theme: {index}/{len(groups)} themes")
    conn.execute("DELETE FROM theme WHERE as_of = ?", [as_of])
    conn.execute("DELETE FROM theme_member WHERE as_of = ?", [as_of])
    conn.executemany("INSERT INTO theme VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", themes)
    conn.executemany("INSERT OR REPLACE INTO theme_member VALUES (?, ?, ?, ?, ?, ?)", members)
    stats.themes, stats.members = len(themes), len(members)
    progress(f"theme: {len(themes)} themes, {len(members)} members as of {as_of.isoformat()}")
    return stats
