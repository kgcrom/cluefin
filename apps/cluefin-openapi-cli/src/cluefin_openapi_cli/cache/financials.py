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

Incremental via `financials_fetch_log`: a (code, year) pair already asked of DART — whether
it came back with rows or came back empty (not in that batch's response, meaning no filing
that year) — is not re-asked. Only a batch-level error (network, rate limit) leaves a pair
unlogged so it is retried on the next `cache load`.
"""

from __future__ import annotations

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
_SUCCESS = "000"


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
    rows: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "years": self.years,
            "calls": self.calls,
            "codes_fetched": self.codes_ok,
            "codes_empty": self.codes_empty,
            "codes_already_cached": self.codes_skipped,
            "rows": self.rows,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _status_of(result: Any) -> str | None:
    holder = getattr(result, "result", result)
    status = getattr(holder, "status", None)
    return str(getattr(status, "value", status)) if status is not None else None


def _call(dart: Any, corp_codes: list[str], year: str) -> Any:
    """One `fnlttMultiAcnt` call, halving the batch and retrying if DART answers 021.

    Defensive only: callers already batch at `BATCH_SIZE` (100), which DART accepts.
    """

    result = dart.periodic_report_financial_statement.get_multi_company_major_accounts(
        corp_code=",".join(corp_codes),
        bsns_year=year,
        reprt_code=ANNUAL_REPORT_CODE,
    )
    if _status_of(result) != _COMPANY_LIMIT_EXCEEDED or len(corp_codes) <= 1:
        return result
    mid = len(corp_codes) // 2
    first = _call(dart, corp_codes[:mid], year)
    second = _call(dart, corp_codes[mid:], year)
    first_status, second_status = _status_of(first), _status_of(second)
    merged_list = [*(first.result.list or []), *(second.result.list or [])]
    first.result.list = merged_list
    if _REQUEST_LIMIT_EXCEEDED in (first_status, second_status):
        first.result.status = _REQUEST_LIMIT_EXCEEDED
    elif merged_list:
        first.result.status = _SUCCESS
    return first


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
    rows = conn.execute(
        "SELECT c.code FROM company c WHERE c.corp_code IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM financials_fetch_log f WHERE f.code = c.code AND f.year = ?) "
        "ORDER BY c.code",
        [year],
    ).fetchall()
    return [row[0] for row in rows]


def _corp_code_of(conn: duckdb.DuckDBPyConnection, codes: list[str]) -> dict[str, str]:
    rows = conn.execute(
        "SELECT code, corp_code FROM company WHERE code IN (SELECT unnest(?::TEXT[]))", [codes]
    ).fetchall()
    return dict(rows)


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
            if quota_exhausted:
                break
            corp_codes = [corp_code_by_code[code] for code in batch if code in corp_code_by_code]
            if not corp_codes:
                continue
            stats.calls += 1
            try:
                result = _call(dart, corp_codes, year)
            except Exception as exc:  # noqa: BLE001 - one bad batch must not stop the rest
                status = getattr(exc, "response_data", None)
                if isinstance(status, dict) and status.get("status") == _REQUEST_LIMIT_EXCEEDED:
                    quota_exhausted = True
                    stats.errors.append({"year": year, "error": "DART daily quota exhausted mid-load"})
                    break
                stats.errors.append({"year": year, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
                continue
            status = _status_of(result)
            if status == _REQUEST_LIMIT_EXCEEDED:
                quota_exhausted = True
                stats.errors.append({"year": year, "error": "DART daily quota exhausted (status 020)"})
                break
            items = (result.result.list or []) if status != _NO_DATA else []
            by_code = _best_rows(items)
            fetched = set(by_code)
            rows: list[tuple[Any, ...]] = []
            for code, accounts in by_code.items():
                for account_nm, (basis, amount, currency) in accounts.items():
                    rows.append((code, year, ANNUAL_REPORT_CODE, basis or None, account_nm, amount, currency, now))
            if rows:
                conn.executemany(_UPSERT_SQL, rows)
                stats.rows += len(rows)
            conn.executemany(
                _FETCH_LOG_SQL,
                [(code, year, "ok" if code in fetched else "empty", now) for code in batch],
            )
            stats.codes_ok += len(fetched)
            stats.codes_empty += len(batch) - len(fetched)
            if index % 5 == 0 or index == len(batches):
                progress(f"financials: {year} batch {index}/{len(batches)}")

    return stats
