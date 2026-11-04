"""`financials` table: DART `fnlttMultiAcnt`(다중회사 주요계정), annual report only.

One call covers up to 100 companies' one fiscal year of standard major-account lines
(`fnlttMultiAcnt.json`, ``get_multi_company_major_accounts``) — cheap enough (~26 calls for
the whole universe, one fiscal year) to pull every stock's last five fiscal years, unlike the
per-stock full-statements call used for a single ticker's exact numbers (`dart
financial-summary`, `kis stock valuation-band`). The trade-off, decided 2026-11-04
(`docs/plans/today-bundles-plan.md` B-1b):

- Only the ~12 standard "주요계정" lines DART defines for this endpoint (유동자산·비유동자산·
  자산총계·유동부채·비유동부채·부채총계·자본금·이익잉여금(결손금)·자본총계·매출액·영업이익·
  당기순이익) — no cash-flow line, nothing finer.
- No 지배/비지배(controlling/non-controlling) split — the endpoint does not carry it.
- Annual (`reprt_code` 11011) only, so one row per (code, year, account_nm). A company's own
  filing for that year is kept, not a later year's comparative column (same convention as
  `statements.py`/`financial-summary`).
- 연결(CFS) preferred when a company files both; 별도(OFS) only when there is no CFS row for
  that account. `basis` on each row says which.

This table is a cheap cross-sectional screen (`cache magic-formula`, `cache base-rate`'s PBR
axis). A single ticker that needs exact, restated-aware numbers still goes through `dart
financial-summary`/`financial-full-statements` directly.

Incremental via `financials_fetch_log`: a (code, year) pair logged ``ok``/``empty`` is not
re-asked. A pair logged ``error`` (see "one bad corp_code" below) is retried on every run,
same as an unlogged pair.

One bad corp_code must not drop 99 good ones (2026-11-04 full-universe load: 31/192 batches of
100 failed outright). Two real causes, both now handled:

- **A batch with a duplicate corp_code 302-redirects to an HTML error page instead of JSON**
  (`JSONDecodeError`). A duplicate happens when a preferred share and its common share both
  land in the same 100-code batch — DART only knows the common share's `corp_code`
  (`company.corp_code_for`), so both resolve to the same id. Fixed by de-duplicating the
  `corp_code` list before every call (`_fetch`).
- A single company's filing can still fail pydantic validation (e.g. a field the model
  declared required turns out missing for that filer) or the call can fail outright
  (network). `_fetch` narrows a failing batch by bisection until the one corp_code (or the
  rare case where none remain) is isolated; a single corp_code that still fails is recorded
  as `error` in `financials_fetch_log` and counted in `failed_codes`/`errors`, and every
  other corp_code in the original batch is still written normally.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Any

import duckdb

from cluefin_openapi_cli.clock import now_kst
from cluefin_openapi_cli.statements import won

__all__ = [
    "ANNUAL_REPORT_CODE",
    "BATCH_SIZE",
    "DEFAULT_YEAR_COUNT",
    "FinancialLoadStats",
    "default_years",
    "load_financials",
]

ANNUAL_REPORT_CODE = "11011"
# DART refuses a `fnlttMultiAcnt` call over 100 corp codes with status 021 (COMPANY_LIMIT_EXCEEDED).
BATCH_SIZE = 100
DEFAULT_YEAR_COUNT = 5

_COMPANY_LIMIT_EXCEEDED = "021"
_REQUEST_LIMIT_EXCEEDED = "020"
_NO_DATA = "013"


def default_years(today: date, *, count: int = DEFAULT_YEAR_COUNT) -> tuple[str, ...]:
    """The last ``count`` fiscal years that should already have an annual report filed.

    An FY2025 사업보고서 is filed by March 2026, so a year is "done" once it is in the past —
    this does not try to guess whether the current year's report is out yet.
    """

    end = today.year - 1
    return tuple(str(year) for year in range(end - count + 1, end + 1))


# frozen 아님: 적재하면서 건수를 더해 가는 누적기.
@dataclass(slots=True)
class FinancialLoadStats:
    years: int = 0
    calls: int = 0
    codes_ok: int = 0
    codes_empty: int = 0
    codes_skipped: int = 0
    failed_codes: int = 0
    rows: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "years": self.years,
            "calls": self.calls,
            "codes_fetched": self.codes_ok,
            "codes_empty": self.codes_empty,
            "codes_already_cached": self.codes_skipped,
            "failed_codes": self.failed_codes,
            "rows": self.rows,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _status_of(result: Any) -> str | None:
    holder = getattr(result, "result", result)
    status = getattr(holder, "status", None)
    return str(getattr(status, "value", status)) if status is not None else None


def _is_quota_exception(exc: BaseException) -> bool:
    data = getattr(exc, "response_data", None)
    return isinstance(data, dict) and data.get("status") == _REQUEST_LIMIT_EXCEEDED


@dataclass(frozen=True, slots=True)
class _FetchOutcome:
    items: list[Any]
    quota_exhausted: bool = False
    failed_corp_codes: tuple[str, ...] = ()
    error_samples: tuple[str, ...] = ()
    calls: int = 0


def _fetch(dart: Any, corp_codes: list[str], year: str) -> _FetchOutcome:
    """One or more `fnlttMultiAcnt` calls for ``corp_codes``, narrowing on failure.

    De-duplicates first (see module docstring). A daily-quota hit (020) stops immediately —
    bisecting into it would only spend more of the same exhausted quota. Anything else that
    fails (021 "too many companies", an exception) is narrowed by bisection until either it
    succeeds on a smaller slice or a single corp_code is isolated as unrecoverable.
    """

    codes = list(dict.fromkeys(corp_codes))
    if not codes:
        return _FetchOutcome(items=[])
    try:
        result = dart.periodic_report_financial_statement.get_multi_company_major_accounts(
            corp_code=",".join(codes),
            bsns_year=year,
            reprt_code=ANNUAL_REPORT_CODE,
        )
    except Exception as exc:  # noqa: BLE001 - narrowed below, not swallowed
        if _is_quota_exception(exc):
            return _FetchOutcome(items=[], quota_exhausted=True, calls=1)
        return _narrow(dart, codes, year, calls_so_far=1, error=exc)

    status = _status_of(result)
    if status == _REQUEST_LIMIT_EXCEEDED:
        return _FetchOutcome(items=[], quota_exhausted=True, calls=1)
    if status == _COMPANY_LIMIT_EXCEEDED:
        return _narrow(dart, codes, year, calls_so_far=1, error=None)
    if status == _NO_DATA:
        return _FetchOutcome(items=[], calls=1)
    return _FetchOutcome(items=list(result.result.list or []), calls=1)


def _narrow(dart: Any, codes: list[str], year: str, *, calls_so_far: int, error: BaseException | None) -> _FetchOutcome:
    if len(codes) == 1:
        message = (
            f"{type(error).__name__}: {str(error)[:200]}"
            if error is not None
            else "DART status 021 (021 for a single corp_code)"
        )
        return _FetchOutcome(items=[], failed_corp_codes=(codes[0],), error_samples=(message,), calls=calls_so_far)
    mid = len(codes) // 2
    first = _fetch(dart, codes[:mid], year)
    if first.quota_exhausted:
        return dataclasses.replace(first, calls=calls_so_far + first.calls)
    second = _fetch(dart, codes[mid:], year)
    return _FetchOutcome(
        items=[*first.items, *second.items],
        quota_exhausted=second.quota_exhausted,
        failed_corp_codes=(*first.failed_corp_codes, *second.failed_corp_codes),
        error_samples=(*first.error_samples, *second.error_samples),
        calls=calls_so_far + first.calls + second.calls,
    )


def _batches(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


# DART's standard "주요계정" set for `fnlttMultiAcnt` (fixed by the endpoint, not chosen here).
ACCOUNT_NAMES = (
    "유동자산",
    "비유동자산",
    "자산총계",
    "유동부채",
    "비유동부채",
    "부채총계",
    "자본금",
    "이익잉여금(결손금)",
    "자본총계",
    "매출액",
    "영업이익",
    "당기순이익",
)

_UPSERT_SQL = """
INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (code, year, account_nm) DO UPDATE SET
  reprt_code = excluded.reprt_code, basis = excluded.basis, amount = excluded.amount,
  currency = excluded.currency, loaded_at = excluded.loaded_at
"""

_FETCH_LOG_SQL = """
INSERT INTO financials_fetch_log (code, year, status, fetched_at) VALUES (?, ?, ?, ?)
ON CONFLICT (code, year) DO UPDATE SET status = excluded.status, fetched_at = excluded.fetched_at
"""


def _best_rows(items: list[Any]) -> dict[str, dict[str, tuple[str, float | None, str]]]:
    """``stock_code -> {account_nm: (basis, amount, currency)}``, CFS preferred over OFS."""

    by_code: dict[str, dict[str, tuple[str, float | None, str]]] = {}
    for item in items:
        code = str(item.stock_code or "").strip()
        if not code:
            continue
        basis = str(item.fs_div or "").strip().upper()
        account_nm = str(item.account_nm or "").strip()
        existing = by_code.setdefault(code, {})
        current = existing.get(account_nm)
        if current is not None and current[0] == "CFS" and basis != "CFS":
            continue  # keep the already-chosen CFS row
        existing[account_nm] = (basis, won(item.thstrm_amount), str(item.currency or ""))
    return by_code


def _universe(conn: duckdb.DuckDBPyConnection) -> list[str]:
    return [row[0] for row in conn.execute("SELECT code FROM company WHERE corp_code IS NOT NULL").fetchall()]


def _candidates(conn: duckdb.DuckDBPyConnection, year: str) -> list[str]:
    """Codes still worth asking for ``year``: never asked, or asked and left `error`.

    `ok`/`empty` are a settled answer and are not re-asked; `error` is not (see module
    docstring) so a `cache load` keeps retrying only the handful DART keeps rejecting.
    """

    rows = conn.execute(
        "SELECT c.code FROM company c WHERE c.corp_code IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM financials_fetch_log f WHERE f.code = c.code AND f.year = ? "
        "AND f.status != 'error') "
        "ORDER BY c.code",
        [year],
    ).fetchall()
    return [row[0] for row in rows]


def _corp_code_of(conn: duckdb.DuckDBPyConnection, codes: list[str]) -> dict[str, str]:
    rows = conn.execute(
        "SELECT code, corp_code FROM company WHERE code IN (SELECT unnest(?::TEXT[]))", [codes]
    ).fetchall()
    return dict(rows)


def _process_batch(
    conn: duckdb.DuckDBPyConnection,
    *,
    dart: Any,
    batch: list[str],
    corp_code_by_code: dict[str, str],
    year: str,
    now: Any,
    stats: FinancialLoadStats,
) -> bool:
    """One batch. Returns ``True`` if the daily quota is exhausted (caller should stop)."""

    codes_by_corp: dict[str, list[str]] = {}
    for code in batch:
        corp_code = corp_code_by_code.get(code)
        if corp_code:
            codes_by_corp.setdefault(corp_code, []).append(code)
    if not codes_by_corp:
        return False

    outcome = _fetch(dart, list(codes_by_corp), year)
    stats.calls += outcome.calls

    by_code = _best_rows(outcome.items)
    fetched = set(by_code)
    rows: list[tuple[Any, ...]] = []
    for code, accounts in by_code.items():
        for account_nm, (basis, amount, currency) in accounts.items():
            rows.append((code, year, ANNUAL_REPORT_CODE, basis or None, account_nm, amount, currency, now))
    if rows:
        conn.executemany(_UPSERT_SQL, rows)
        stats.rows += len(rows)

    error_codes: set[str] = set()
    for corp_code in outcome.failed_corp_codes:
        error_codes.update(codes_by_corp.get(corp_code, []))
    if error_codes:
        conn.executemany(_FETCH_LOG_SQL, [(code, year, "error", now) for code in error_codes])
        stats.failed_codes += len(error_codes)
        stats.errors.extend(
            {"year": year, "code": code, "error": message}
            for code, message in zip(sorted(error_codes), outcome.error_samples, strict=False)
        )

    if outcome.quota_exhausted:
        # Codes neither fetched nor confirmed failed are of unknown status (quota hit before
        # they were asked) — leave them unlogged so a later run (quota resets daily) retries.
        stats.errors.append({"year": year, "error": "DART daily quota exhausted (status 020)"})
        return True

    empty_codes = set(batch) - fetched - error_codes
    settled = [(code, year, "ok", now) for code in fetched] + [(code, year, "empty", now) for code in empty_codes]
    if settled:
        conn.executemany(_FETCH_LOG_SQL, settled)
    stats.codes_ok += len(fetched)
    stats.codes_empty += len(empty_codes)
    return False


def load_financials(
    conn: duckdb.DuckDBPyConnection,
    *,
    dart: Any,
    years: tuple[str, ...],
    progress: Callable[[str], None] = lambda _message: None,
) -> FinancialLoadStats:
    stats = FinancialLoadStats(years=len(years))
    now = now_kst()
    quota_exhausted = False
    universe_size = len(_universe(conn))

    for year in years:
        if quota_exhausted:
            break
        candidates = _candidates(conn, year)
        stats.codes_skipped += universe_size - len(candidates)
        if not candidates:
            progress(f"financials: {year} already cached for every known code")
            continue
        corp_code_by_code = _corp_code_of(conn, candidates)
        batches = _batches(candidates, BATCH_SIZE)
        for index, batch in enumerate(batches, 1):
            quota_exhausted = _process_batch(
                conn, dart=dart, batch=batch, corp_code_by_code=corp_code_by_code, year=year, now=now, stats=stats
            )
            if quota_exhausted:
                break
            if index % 5 == 0 or index == len(batches):
                progress(f"financials: {year} batch {index}/{len(batches)}")

    return stats
