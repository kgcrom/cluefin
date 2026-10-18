"""The local DuckDB file behind `cache *`: where it lives, its schema, and how it is opened.

DuckDB allows one writing process per file, and while it writes no other process can open
the file at all — not even read-only. `cache load` is the only writer; every other command
opens with ``read_only=True`` and turns the lock error into a message instead of a trace.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import duckdb

from cluefin_openapi_cli.errors import EXIT_UNEXPECTED, EXIT_USAGE, CliError

__all__ = ["CACHE_DIR_ENV", "SCHEMA", "cache_path", "open_store", "status"]

CACHE_DIR_ENV = "CLUEFIN_CACHE_DIR"
_FILE_NAME = "market.duckdb"

SCHEMA = (
    # 기업정보: one row per stock, delisted ones kept (survivorship).
    """
    CREATE TABLE IF NOT EXISTS company (
      code TEXT PRIMARY KEY,
      name TEXT,
      market TEXT,
      kind TEXT,
      sector TEXT,
      industry TEXT,
      corp_code TEXT,
      settle_month SMALLINT,
      listed_on DATE,
      delisted_on DATE,
      list_count BIGINT,
      is_admin BOOLEAN,
      is_halted BOOLEAN,
      seen_on DATE,
      updated_at TIMESTAMP
    )
    """,
    # 차트: stock and index daily bars; unadjusted prices, adjusted = close * adj_factor.
    """
    CREATE TABLE IF NOT EXISTS ohlcv (
      code TEXT,
      date DATE,
      open DOUBLE,
      high DOUBLE,
      low DOUBLE,
      close DOUBLE,
      volume DOUBLE,
      value DOUBLE,
      adj_factor DOUBLE DEFAULT 1.0,
      loaded_at TIMESTAMP,
      PRIMARY KEY (code, date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS load_log (
      run_at TIMESTAMP,
      kind TEXT,
      codes INTEGER,
      rows INTEGER,
      replaced INTEGER,
      errors INTEGER,
      seconds DOUBLE
    )
    """,
    # Codes already checked as delisting candidates, so basic-info is not asked twice.
    """
    CREATE TABLE IF NOT EXISTS probe_log (
      code TEXT PRIMARY KEY,
      mket_id_cd TEXT,
      scty_grp_id_cd TEXT,
      delisted_on DATE,
      checked_at TIMESTAMP
    )
    """,
)


def cache_path() -> Path:
    """`$CLUEFIN_CACHE_DIR/market.duckdb`, defaulting to `~/.cache/cluefin/`."""

    base = os.environ.get(CACHE_DIR_ENV, "").strip()
    directory = Path(base).expanduser() if base else Path.home() / ".cache" / "cluefin"
    return directory / _FILE_NAME


def open_store(path: Path | str | None = None, *, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """Open the cache. Writers create the file and schema; readers need an existing file.

    ``path=":memory:"`` gives an empty in-memory store with the schema (tests).
    """

    if path == ":memory:":
        conn = duckdb.connect(":memory:")
        _apply_schema(conn)
        return conn

    target = Path(path) if path is not None else cache_path()
    if read_only and not target.exists():
        raise CliError(
            f"No cache at {target}.",
            exit_code=EXIT_USAGE,
            error_type="CacheMissing",
            hint="Run `cache load` first (it needs broker credentials and takes a while).",
            data={"path": str(target)},
        )
    if not read_only:
        target.parent.mkdir(parents=True, exist_ok=True)
    try:
        conn = duckdb.connect(str(target), read_only=read_only)
    except duckdb.IOException as exc:
        if "lock" not in str(exc).lower():
            raise
        raise CliError(
            f"The cache at {target} is locked by another process.",
            exit_code=EXIT_UNEXPECTED,
            error_type="CacheLocked",
            retryable=True,
            hint="A `cache load` is probably running; DuckDB allows no readers while it writes. Retry after it ends.",
            data={"path": str(target)},
        ) from exc
    if not read_only:
        _apply_schema(conn)
    return conn


def _apply_schema(conn: duckdb.DuckDBPyConnection) -> None:
    for statement in SCHEMA:
        conn.execute(statement)


def _scalar_row(conn: duckdb.DuckDBPyConnection, sql: str) -> tuple[Any, ...]:
    row = conn.execute(sql).fetchone()
    return tuple(row) if row else ()


def _iso(value: Any) -> str | None:
    return value.isoformat() if value is not None else None


def status(conn: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    """Row counts, date span and the last load per kind."""

    listed, delisted = _scalar_row(
        conn,
        "SELECT count(*) FILTER (WHERE delisted_on IS NULL), count(*) FILTER (WHERE delisted_on IS NOT NULL) "
        "FROM company",
    )
    rows, codes, first, last = _scalar_row(
        conn, "SELECT count(*), count(DISTINCT code), min(date), max(date) FROM ohlcv"
    )
    loads = conn.execute(
        "SELECT kind, max(run_at) FROM load_log GROUP BY kind ORDER BY kind",
    ).fetchall()
    return {
        "company": {"listed": listed, "delisted": delisted},
        "ohlcv": {"rows": rows, "codes": codes, "first_date": _iso(first), "last_date": _iso(last)},
        "last_load": {kind: _iso(run_at) for kind, run_at in loads},
    }
