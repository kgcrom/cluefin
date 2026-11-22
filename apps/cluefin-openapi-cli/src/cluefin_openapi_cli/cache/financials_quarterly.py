"""`financials_quarterly` table: DART `fnlttMultiAcnt` 분기·반기 보고서 주요계정.

The annual table (`cache/financials.py`) holds only 사업보고서; this one holds the other three
periodic reports so the cache can show quarters and trailing twelve months (decided 2026-11-22):

- 1분기 11013, 반기 11012, 3분기 11014 → `quarter` 1/2/3. Quarter 4 is never fetched — it is the
  annual report already in `financials`, and `financials_ttm` derives its three months from there.
- Measured 2026-11-22 (005930): an income-statement line's `thstrm_amount` is that quarter's three
  months, `thstrm_add_amount` the year-to-date total and `frmtrm_add_amount` the prior year's
  same-period year-to-date (restated alongside the current figure). Balance-sheet lines carry only
  `thstrm_amount`, the quarter-end balance. All three are kept: `amount`/`cum_amount`/
  `prior_cum_amount`.
- Same conventions as the annual table: DART `account_nm` verbatim, CFS preferred over OFS per
  account, a batch of 100 corp codes per call, bisection around one bad corp_code (`financials._fetch`).
- Periods: fiscal years `today.year - 4` … `today.year` (five calendar years), only quarters whose
  filing deadline has passed (12월 결산 기준 1Q 5/15, 반기 8/14, 3Q 11/14). Delisted companies are in
  the universe too (`company` keeps them).

Incremental via `financials_quarterly_fetch_log` (code, year, quarter). `ok` is never re-asked.
`empty` is re-asked while the quarter's deadline is under a year old — a late filer, or a company
whose fiscal year does not end in December (its "3분기" is due months later), would otherwise be
stuck as empty. `error` is always retried. A daily-quota hit (020) stops the run where it is;
everything settled so far is already written, so the next run picks up from there.

After loading, `financials_ttm` is rebuilt from both tables (`rebuild_ttm`).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

import duckdb

from cluefin_openapi_cli.cache.financials import BATCH_SIZE, _batches, _fetch, _universe
from cluefin_openapi_cli.cache.financials_ttm import rebuild_ttm
from cluefin_openapi_cli.clock import now_kst
from cluefin_openapi_cli.statements import won

__all__ = [
    "QUARTER_REPORT_CODES",
    "QuarterlyLoadStats",
    "default_quarters",
    "load_financials_quarterly",
    "quarter_due",
]

QUARTER_REPORT_CODES = {1: "11013", 2: "11012", 3: "11014"}
DEFAULT_YEAR_COUNT = 5
# 분기·반기 보고서는 분기 말일부터 45일 안에 낸다(12월 결산 기준). 4Q 는 사업보고서(90일).
_DUE_MONTH_DAY = {1: (5, 15), 2: (8, 14), 3: (11, 14), 4: (3, 31)}
_EMPTY_RETRY_DAYS = 365


def quarter_due(year: int, quarter: int) -> date:
    """Filing deadline of fiscal ``year``'s ``quarter`` report for a December year-end (4 = 사업보고서)."""

    month, day = _DUE_MONTH_DAY[quarter]
    return date(year + 1 if quarter == 4 else year, month, day)


def default_quarters(today: date, *, count: int = DEFAULT_YEAR_COUNT) -> tuple[tuple[str, int], ...]:
    """``(year, quarter)`` for quarters 1–3 of the last ``count`` calendar years, deadline passed by ``today``."""

    return tuple(
        (str(year), quarter)
        for year in range(today.year - count + 1, today.year + 1)
        for quarter in (1, 2, 3)
        if quarter_due(year, quarter) <= today
    )


# frozen 아님: 적재하면서 건수를 더해 가는 누적기.
@dataclass(slots=True)
class QuarterlyLoadStats:
    periods: int = 0
    calls: int = 0
    codes_ok: int = 0
    codes_empty: int = 0
    codes_skipped: int = 0
    failed_codes: int = 0
    rows: int = 0
    ttm_rows: int = 0
    quota_exhausted: bool = False
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "periods": self.periods,
            "calls": self.calls,
            "codes_fetched": self.codes_ok,
            "codes_empty": self.codes_empty,
            "codes_already_cached": self.codes_skipped,
            "failed_codes": self.failed_codes,
            "rows": self.rows,
            "ttm_rows": self.ttm_rows,
            "quota_exhausted": self.quota_exhausted,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


_UPSERT_SQL = """
INSERT INTO financials_quarterly (code, year, quarter, reprt_code, basis, account_nm, amount, cum_amount,
  prior_cum_amount, currency, loaded_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (code, year, quarter, account_nm) DO UPDATE SET
  reprt_code = excluded.reprt_code, basis = excluded.basis, amount = excluded.amount,
  cum_amount = excluded.cum_amount, prior_cum_amount = excluded.prior_cum_amount,
  currency = excluded.currency, loaded_at = excluded.loaded_at
"""

_FETCH_LOG_SQL = """
INSERT INTO financials_quarterly_fetch_log (code, year, quarter, status, fetched_at) VALUES (?, ?, ?, ?, ?)
ON CONFLICT (code, year, quarter) DO UPDATE SET status = excluded.status, fetched_at = excluded.fetched_at
"""

_Row = tuple[str, float | None, float | None, float | None, str]


def _best_rows(items: list[Any]) -> dict[str, dict[str, _Row]]:
    """``stock_code -> {account_nm: (basis, amount, cum, prior_cum, currency)}``, CFS preferred over OFS."""

    by_code: dict[str, dict[str, _Row]] = {}
    for item in items:
        code = str(item.stock_code or "").strip()
        if not code:
            continue
        basis = str(item.fs_div or "").strip().upper()
        account_nm = str(item.account_nm or "").strip()
        existing = by_code.setdefault(code, {})
        current = existing.get(account_nm)
        if current is not None and current[0] == "CFS" and basis != "CFS":
            continue
        existing[account_nm] = (
            basis,
            won(item.thstrm_amount),
            won(getattr(item, "thstrm_add_amount", None)),
            won(getattr(item, "frmtrm_add_amount", None)),
            str(item.currency or ""),
        )
    return by_code


def _candidates(conn: duckdb.DuckDBPyConnection, year: str, quarter: int, *, retry_empty: bool) -> list[str]:
    settled = "('ok')" if retry_empty else "('ok', 'empty')"
    rows = conn.execute(
        "SELECT c.code FROM company c WHERE c.corp_code IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM financials_quarterly_fetch_log f WHERE f.code = c.code AND f.year = ? "
        f"AND f.quarter = ? AND f.status IN {settled}) "
        "ORDER BY c.code",
        [year, quarter],
    ).fetchall()
    return [row[0] for row in rows]


@dataclass(frozen=True, slots=True)
class _Period:
    year: str
    quarter: int

    @property
    def reprt_code(self) -> str:
        return QUARTER_REPORT_CODES[self.quarter]

    @property
    def label(self) -> str:
        return f"{self.year}Q{self.quarter}"


def _process_batch(
    conn: duckdb.DuckDBPyConnection,
    *,
    dart: Any,
    batch: list[str],
    corp_code_by_code: dict[str, str],
    period: _Period,
    now: Any,
    stats: QuarterlyLoadStats,
) -> bool:
    """One batch. Returns ``True`` if the daily quota is exhausted (caller should stop)."""

    codes_by_corp: dict[str, list[str]] = {}
    for code in batch:
        corp_code = corp_code_by_code.get(code)
        if corp_code:
            codes_by_corp.setdefault(corp_code, []).append(code)
    if not codes_by_corp:
        return False

    outcome = _fetch(dart, list(codes_by_corp), period.year, period.reprt_code)
    stats.calls += outcome.calls

    by_code = _best_rows(outcome.items)
    rows = [
        (code, period.year, period.quarter, period.reprt_code, basis or None, account_nm, amount, cum, prior, cur, now)
        for code, accounts in by_code.items()
        for account_nm, (basis, amount, cum, prior, cur) in accounts.items()
    ]
    if rows:
        conn.executemany(_UPSERT_SQL, rows)
        stats.rows += len(rows)

    error_codes: set[str] = set()
    for corp_code in outcome.failed_corp_codes:
        error_codes.update(codes_by_corp.get(corp_code, []))
    if error_codes:
        conn.executemany(_FETCH_LOG_SQL, [(code, period.year, period.quarter, "error", now) for code in error_codes])
        stats.failed_codes += len(error_codes)
        stats.errors.extend(
            {"period": period.label, "code": code, "error": message}
            for code, message in zip(sorted(error_codes), outcome.error_samples, strict=False)
        )

    if outcome.quota_exhausted:
        # Codes not yet asked stay unlogged so the next run (quota resets daily) asks them.
        stats.errors.append({"period": period.label, "error": "DART daily quota exhausted (status 020)"})
        return True

    fetched = set(by_code)
    empty_codes = set(batch) - fetched - error_codes
    settled = [(code, period.year, period.quarter, "ok", now) for code in fetched]
    settled += [(code, period.year, period.quarter, "empty", now) for code in empty_codes]
    if settled:
        conn.executemany(_FETCH_LOG_SQL, settled)
    stats.codes_ok += len(fetched)
    stats.codes_empty += len(empty_codes)
    return False


def _load_period(
    conn: duckdb.DuckDBPyConnection,
    *,
    dart: Any,
    period: _Period,
    today: date,
    universe_size: int,
    now: Any,
    stats: QuarterlyLoadStats,
    progress: Callable[[str], None],
) -> bool:
    """Every pending code for one quarter. Returns ``True`` if the daily quota is exhausted."""

    retry_empty = today - quarter_due(int(period.year), period.quarter) < timedelta(days=_EMPTY_RETRY_DAYS)
    candidates = _candidates(conn, period.year, period.quarter, retry_empty=retry_empty)
    stats.codes_skipped += universe_size - len(candidates)
    if not candidates:
        progress(f"financials_quarterly: {period.label} already cached for every known code")
        return False
    rows = conn.execute(
        "SELECT code, corp_code FROM company WHERE code IN (SELECT unnest(?::TEXT[]))", [candidates]
    ).fetchall()
    corp_code_by_code = dict(rows)
    batches = _batches(candidates, BATCH_SIZE)
    for index, batch in enumerate(batches, 1):
        if _process_batch(
            conn, dart=dart, batch=batch, corp_code_by_code=corp_code_by_code, period=period, now=now, stats=stats
        ):
            progress(
                f"financials_quarterly: {period.label} stopped at batch {index}/{len(batches)} — DART daily quota "
                f"exhausted after {stats.calls} calls; run again tomorrow to continue"
            )
            return True
        if index % 5 == 0 or index == len(batches):
            progress(f"financials_quarterly: {period.label} batch {index}/{len(batches)} (calls {stats.calls})")
    return False


def load_financials_quarterly(
    conn: duckdb.DuckDBPyConnection,
    *,
    dart: Any,
    today: date,
    quarters: tuple[tuple[str, int], ...] | None = None,
    progress: Callable[[str], None] = lambda _message: None,
) -> QuarterlyLoadStats:

    periods = [_Period(year, quarter) for year, quarter in (quarters or default_quarters(today))]
    stats = QuarterlyLoadStats(periods=len(periods))
    now = now_kst()
    universe_size = len(_universe(conn))
    for period in periods:
        if _load_period(
            conn,
            dart=dart,
            period=period,
            today=today,
            universe_size=universe_size,
            now=now,
            stats=stats,
            progress=progress,
        ):
            stats.quota_exhausted = True
            break
    stats.ttm_rows = rebuild_ttm(conn)
    progress(f"financials_quarterly: financials_ttm rebuilt ({stats.ttm_rows} rows)")
    return stats
