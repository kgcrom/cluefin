"""`financials_ttm` table: quarter (3-month) and trailing-twelve-month figures, derived — never fetched.

Rebuilt whole from `financials` (사업보고서) and `financials_quarterly` (분기·반기) after every
quarterly load. One row per (code, fiscal year, quarter 1–4, folded account name):

- Income-statement lines (`FLOW_ACCOUNTS`):
  - quarters 1–3: `quarter_amount` is the filing's own three months; `ttm_amount` = year-to-date
    + prior fiscal year's annual − prior year's same-period year-to-date. The prior year-to-date is
    the same filing's comparative (`prior_cum_amount`, restated with the current figure) and falls
    back to the prior year's own quarterly filing.
  - quarter 4: `quarter_amount` = annual − Q3 year-to-date, `ttm_amount` = annual.
  - A TTM or Q4 figure whose parts mix 연결(CFS) and 별도(OFS) is `null` — adding a consolidated year
    to a separate-only quarter is not a twelve-month figure of anything.
- Balance-sheet lines: both columns are the period-end balance (quarter 4 = the annual report).

Account names are folded the same way readers fold the annual table (`financials.ACCOUNT_ALIASES`;
the bare spelling wins when a filer has both).
"""

from __future__ import annotations

import duckdb

from cluefin_openapi_cli.cache.financials import ACCOUNT_ALIASES

__all__ = ["FLOW_ACCOUNTS", "rebuild_ttm"]

FLOW_ACCOUNTS = ("매출액", "영업이익", "당기순이익")


def _canonical_sql(column: str) -> str:
    whens = " ".join(f"WHEN '{alias}' THEN '{canonical}'" for alias, canonical in ACCOUNT_ALIASES.items())
    return f"CASE {column} {whens} ELSE {column} END"


_FLOWS = ", ".join(f"'{name}'" for name in FLOW_ACCOUNTS)

_REBUILD_SQL = f"""
INSERT INTO financials_ttm (code, year, quarter, account_nm, quarter_amount, ttm_amount, basis)
WITH q AS (
  SELECT code, year, quarter, basis, amount, cum_amount, prior_cum_amount,
    {_canonical_sql("account_nm")} AS canonical
  FROM financials_quarterly
  QUALIFY row_number() OVER (
    PARTITION BY code, year, quarter, canonical ORDER BY (account_nm = canonical) DESC
  ) = 1
),
a AS (
  SELECT code, year, basis, amount, {_canonical_sql("account_nm")} AS canonical
  FROM financials
  QUALIFY row_number() OVER (PARTITION BY code, year, canonical ORDER BY (account_nm = canonical) DESC) = 1
),
quarters AS (
  SELECT q.code, q.year, q.quarter, q.canonical AS account_nm, q.amount AS quarter_amount,
    CASE
      WHEN q.canonical NOT IN ({_FLOWS}) THEN q.amount
      WHEN prev.basis = q.basis AND (q.prior_cum_amount IS NOT NULL OR qp.basis = q.basis)
        THEN coalesce(q.cum_amount, CASE WHEN q.quarter = 1 THEN q.amount END)
          + prev.amount - coalesce(q.prior_cum_amount, qp.cum_amount)
    END AS ttm_amount,
    q.basis
  FROM q
  LEFT JOIN a prev
    ON prev.code = q.code AND prev.year = CAST(CAST(q.year AS INTEGER) - 1 AS TEXT) AND prev.canonical = q.canonical
  LEFT JOIN q qp
    ON qp.code = q.code AND qp.year = CAST(CAST(q.year AS INTEGER) - 1 AS TEXT) AND qp.quarter = q.quarter
    AND qp.canonical = q.canonical
),
fourth AS (
  SELECT a.code, a.year, 4 AS quarter, a.canonical AS account_nm,
    CASE
      WHEN a.canonical NOT IN ({_FLOWS}) THEN a.amount
      WHEN q3.basis = a.basis THEN a.amount - q3.cum_amount
    END AS quarter_amount,
    a.amount AS ttm_amount,
    a.basis
  FROM a
  LEFT JOIN q q3 ON q3.code = a.code AND q3.year = a.year AND q3.quarter = 3 AND q3.canonical = a.canonical
)
SELECT * FROM quarters
UNION ALL
SELECT * FROM fourth
"""


def rebuild_ttm(conn: duckdb.DuckDBPyConnection) -> int:
    """Replace `financials_ttm` with a fresh derivation. Returns the row count."""

    conn.execute("BEGIN TRANSACTION")
    try:
        conn.execute("DELETE FROM financials_ttm")
        conn.execute(_REBUILD_SQL)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    row = conn.execute("SELECT count(*) FROM financials_ttm").fetchone()
    return int(row[0]) if row else 0
