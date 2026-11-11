"""`review due`: which recorded verdicts are worth a second look today, and what's coming up for the open ones.

Only one verdict per stock matters here — a changed mind gets a new line in `verdicts.jsonl`, so the latest
`recorded_at`/`id` per `stock_code` is the judgment that is still live. `track.track` (cache only, no broker calls)
supplies the price facts; this module only adds *why* a verdict is worth another look:

    crossed          track's first_cross is set — a trigger/target/stop price was hit on a daily close
    recheck_passed   trigger.recheck_on (carried on the track row since 2026-11-11) is today or earlier
    recheck_within   trigger.recheck_on falls within the next `--days`
    horizon_ending   status is still "open" and horizon_days - days_seen falls within `--days`
    closed           the horizon has already passed in the cache

A verdict with none of these is just counted, not listed — `review due` is a filter, not a dump of every holding.

`--events true` goes further: for every verdict still *open* (regardless of whether it's "due"), it checks KIS's
12 `schedule.*` commands (shared calls — one per command, `stock_code` left blank, filtered to these codes locally)
and DART's disclosures, and computes the next statutory periodic-report deadline from `company.settle_month` (a pure
date calculation, no call). KIS schedule calls echo no continuation key, so a reply exactly at the 100-row
page cap is marked ``possibly_truncated`` rather than assumed complete (confirmed empirically 2026-11-11: a wide
date window returns exactly 100 rows and silently drops the rest; a 14-day window did not hit the cap).
"""

from __future__ import annotations

import calendar
import json
from datetime import date, timedelta
from typing import Any

import duckdb

from cluefin_openapi_cli.review.collect import Runner
from cluefin_openapi_cli.review.track import track

__all__ = [
    "DEFAULT_DAYS",
    "SCHEDULE_COMMANDS",
    "due",
    "gather_events",
    "latest_per_stock",
    "next_periodic_deadline",
    "tracked_rows",
]

DEFAULT_DAYS = 14

# The 12 KSD/KIS schedule commands (excludes `kis market holiday` and `dart major-event`, which also match a
# "schedule" search but are not this family) — confirmed via `list --json --query schedule` (2026-11-11).
SCHEDULE_COMMANDS: tuple[str, ...] = (
    "bonus-issue",
    "capital-increase",
    "capital-reduction",
    "deposit",
    "dividend",
    "forfeited-share",
    "ipo-subscription",
    "listing",
    "merger-split",
    "par-value-change",
    "shareholder-meeting",
    "stock-dividend",
)
_SCHEDULE_PAGE_CAP = 100  # observed 2026-11-11: a wide window returns exactly 100 rows with no cts echoed back

# 분기/반기보고서는 45일, 사업보고서(사업연도말)는 90일 — 자본시장법 정기보고서 제출기한.
_DEADLINE_DAYS: tuple[int, ...] = (45, 45, 45, 90)
_KIND: tuple[str, ...] = ("분기보고서", "반기보고서", "분기보고서", "사업보고서")


def latest_per_stock(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One record per `stock_code` — the latest by (`recorded_at`, `id`); a changed verdict is a newer line."""

    best: dict[str, dict[str, Any]] = {}
    for record in records:
        code = record["stock_code"]
        key = (record.get("recorded_at", ""), record.get("id", ""))
        current = best.get(code)
        if current is None or key >= (current.get("recorded_at", ""), current.get("id", "")):
            best[code] = record
    return list(best.values())


def _reasons(row: dict[str, Any], today: date, days: int) -> list[dict[str, Any]]:
    reasons: list[dict[str, Any]] = []
    cross = row.get("first_cross")
    if cross:
        reasons.append({"type": "crossed", **cross})
    recheck_on = row.get("recheck_on")
    if recheck_on:
        recheck_date = date.fromisoformat(recheck_on)
        if recheck_date <= today:
            reasons.append({"type": "recheck_passed", "recheck_on": recheck_on})
        elif (recheck_date - today).days <= days:
            reasons.append(
                {"type": "recheck_within", "recheck_on": recheck_on, "days_left": (recheck_date - today).days}
            )
    if row.get("status") == "open" and row.get("days_seen") is not None:
        remaining = row["horizon_days"] - row["days_seen"]
        if 0 <= remaining <= days:
            reasons.append({"type": "horizon_ending", "days_left": remaining})
    if row.get("status") == "closed":
        reasons.append({"type": "closed"})
    return reasons


def tracked_rows(
    conn: duckdb.DuckDBPyConnection, records: list[dict[str, Any]], *, codes: list[str]
) -> tuple[list[dict[str, Any]], str | None]:
    """The latest verdict per stock, tracked against the cache, with `recorded_at` zipped back in.

    `track()` doesn't carry `recorded_at` (it isn't needed for price tracking), but `gather_events` needs it to
    bound the disclosure-search window — and `track()` preserves order 1:1 with its input, so a zip is enough.
    Shared by `due()` and `--events true` so both read the cache and run `track` exactly once.
    """

    latest = latest_per_stock(records)
    if codes:
        latest = [r for r in latest if r["stock_code"] in codes]
    tracked = track(conn, latest)
    rows = [
        {**row, "recorded_at": record["recorded_at"]} for row, record in zip(tracked["verdicts"], latest, strict=True)
    ]
    return rows, tracked["cache_as_of"]


def due(rows: list[dict[str, Any]], cache_as_of: str | None, *, days: int, today: date) -> dict[str, Any]:
    due_rows: list[dict[str, Any]] = []
    by_reason: dict[str, int] = {}
    for row in rows:
        reasons = _reasons(row, today, days)
        if not reasons:
            continue
        due_rows.append({**row, "due_reasons": reasons})
        for reason in reasons:
            by_reason[reason["type"]] = by_reason.get(reason["type"], 0) + 1
    return {
        "as_of": cache_as_of,
        "days": days,
        "watched": len(rows),
        "due_count": len(due_rows),
        "due": due_rows,
        "by_reason": by_reason,
        "notes": [
            "종목별 가장 최근 판단 하나만 본다(판단을 바꾸면 새로 기록하므로). 사유 없는 판단은 watched 에만 들어간다.",
            "crossed: 트리거/목표가/손절가가 닿음. recheck_passed/recheck_within: trigger.recheck_on. "
            "horizon_ending: horizon_days 안에서 --days 이내 남음. closed: horizon 이 이미 지남.",
        ],
    }


# ---------------------------------------------------------------- --events true


def _period_end(month: int, year: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[1])


def next_periodic_deadline(settle_month: int, today: date) -> dict[str, Any]:
    """The nearest upcoming periodic-report statutory deadline for a filer whose fiscal year ends `settle_month`.

    Pure date arithmetic — no DART call. The four reporting periods of a fiscal year ending in `settle_month` end
    9/6/3/0 months before it; the first three are 분기/반기보고서 (45-day deadline), the fiscal year end itself is
    사업보고서 (90-day deadline). Checked against today's real date (2026-11-11, 사업연도말=12): with no filing
    pending the fiscal year's 분기보고서(Q3, 기말 2026-09-30) is due 2026-11-14 — 3 days out.
    """

    if not 1 <= settle_month <= 12:
        raise ValueError("settle_month must be 1..12")
    period_end_months = tuple((settle_month - back - 1) % 12 + 1 for back in (9, 6, 3, 0))
    candidates: list[tuple[date, date, str]] = []
    for idx, month in enumerate(period_end_months):
        for year in (today.year - 1, today.year, today.year + 1):
            period_end = _period_end(month, year)
            deadline = period_end + timedelta(days=_DEADLINE_DAYS[idx])
            if deadline >= today:
                candidates.append((deadline, period_end, _KIND[idx]))
    deadline, period_end, kind = min(candidates, key=lambda c: c[0])
    return {
        "kind": kind,
        "period_end": period_end.isoformat(),
        "deadline": deadline.isoformat(),
        "days_left": (deadline - today).days,
    }


def _ymd(day: date) -> str:
    return day.strftime("%Y%m%d")


def _company_lookup(conn: duckdb.DuckDBPyConnection, codes: list[str]) -> dict[str, tuple[str | None, int | None]]:
    """code -> (corp_code, settle_month), from the local cache only."""

    if not codes:
        return {}
    placeholders = ",".join("?" * len(codes))
    rows = conn.execute(f"SELECT code, corp_code, settle_month FROM company WHERE code IN ({placeholders})", codes)
    return {code: (corp, settle) for code, corp, settle in rows.fetchall()}


def _call(runner: Runner, argv: list[str]) -> Any:
    exit_code, stdout, _stderr = runner(argv)
    if exit_code != 0:
        return None
    try:
        return json.loads(stdout)
    except ValueError:
        return None


def _schedule_events(runner: Runner, codes: set[str], today: date, days: int) -> dict[str, Any]:
    start, end = _ymd(today), _ymd(today + timedelta(days=days))
    by_code: dict[str, list[dict[str, Any]]] = {code: [] for code in codes}
    truncated: list[str] = []
    for name in SCHEDULE_COMMANDS:
        payload = _call(runner, ["kis", "schedule", name, "--start-date", start, "--end-date", end, "--json"])
        rows = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            continue
        if len(rows) == _SCHEDULE_PAGE_CAP:
            truncated.append(name)
        for row in rows:
            if not isinstance(row, dict):
                continue
            code = str(row.get("sht_cd", "")).strip()
            if code in by_code:
                by_code[code].append({"command": name, **row})
    return {"checked": list(SCHEDULE_COMMANDS), "possibly_truncated": truncated, "by_code": by_code}


def _disclosure_events(
    runner: Runner, open_rows: list[dict[str, Any]], lookup: dict[str, tuple[str | None, int | None]], today: date
) -> dict[str, Any]:
    by_code: dict[str, Any] = {}
    for row in open_rows:
        code = row["stock_code"]
        corp, _settle = lookup.get(code, (None, None))
        if not corp:
            by_code[code] = {"count": None, "recent_titles": [], "reason": "no corp_code cached for this stock"}
            continue
        recorded_at = row.get("recorded_at")
        bgn_de = recorded_at.replace("-", "") if recorded_at else _ymd(today - timedelta(days=365))
        payload = _call(
            runner,
            [
                "dart",
                "disclosure-search",
                "--corp-code",
                corp,
                "--bgn-de",
                bgn_de,
                "--end-de",
                _ymd(today),
                "--page-count",
                "100",
                "--json",
            ],
        )
        result = payload.get("result") if isinstance(payload, dict) else None
        if not isinstance(result, dict):
            by_code[code] = {"count": None, "recent_titles": [], "reason": "disclosure-search failed"}
            continue
        items = result.get("list")
        # DART status 013 ("조회된 데이타가 없습니다") answers `list: null` for a clean empty window — not a failure.
        if items is None and result.get("status") == "013":
            items = []
        if not isinstance(items, list):
            by_code[code] = {"count": None, "recent_titles": [], "reason": "disclosure-search failed"}
            continue
        by_code[code] = {
            "count": len(items),
            "recent_titles": [str(item.get("report_nm")) for item in items[:5] if isinstance(item, dict)],
            "since": bgn_de,
        }
    return by_code


def gather_events(
    runner: Runner,
    conn: duckdb.DuckDBPyConnection,
    rows: list[dict[str, Any]],
    *,
    days: int,
    today: date,
) -> dict[str, Any]:
    """Schedules, disclosures and the next statutory deadline for every verdict still open — not only the due ones."""

    open_rows = [row for row in rows if row.get("status") == "open"]
    codes = sorted({row["stock_code"] for row in open_rows})
    if not codes:
        return {"open_codes": [], "schedule": None, "disclosures": {}, "next_periodic_deadline": {}, "notes": []}
    lookup = _company_lookup(conn, codes)
    schedule = _schedule_events(runner, set(codes), today, days)
    disclosures = _disclosure_events(runner, open_rows, lookup, today)
    deadlines: dict[str, Any] = {}
    for code in codes:
        _corp, settle_month = lookup.get(code, (None, None))
        deadlines[code] = next_periodic_deadline(settle_month, today) if settle_month else None
    return {
        "open_codes": codes,
        "schedule": schedule,
        "disclosures": disclosures,
        "next_periodic_deadline": deadlines,
        "notes": [
            "kis schedule 12종을 stock_code 없이 기간 한 번씩 불러 코드로 거른다(종목마다 부르지 않는다). 응답이 100행이면 "
            "cts 이어받기를 이 CLI 가 노출하지 않아 더 있을 수 있다 — possibly_truncated 를 본다.",
            "disclosures 는 각 종목의 recorded_at 이후 공시 수와 최근 제목 5개(dart disclosure-search). corp_code 가 "
            "캐시에 없으면 그 종목은 reason 으로 남는다.",
            "next_periodic_deadline 은 company.settle_month(캐시) 로 계산한 순수 날짜 계산이다 — DART 호출 없음.",
        ],
    }
