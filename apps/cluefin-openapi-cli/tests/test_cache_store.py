"""`cache` store: path, schema, read-only opening, lock message, and `cache status`."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, datetime

import pytest

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.main import run_cli


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    return tmp_path


def test_cache_path_defaults_under_home_cache(monkeypatch) -> None:
    monkeypatch.delenv(store.CACHE_DIR_ENV, raising=False)

    path = store.cache_path()

    assert path.parts[-3:] == (".cache", "cluefin", "market.duckdb")


def test_cache_path_follows_env(cache_dir) -> None:
    assert store.cache_path() == cache_dir / "market.duckdb"


def test_writer_creates_file_and_schema(cache_dir) -> None:
    conn = store.open_store()
    tables = {row[0] for row in conn.execute("SELECT table_name FROM information_schema.tables").fetchall()}
    conn.close()

    assert tables == {"company", "ohlcv", "load_log", "probe_log"}
    assert store.cache_path().exists()


def test_reader_without_file_is_cache_missing(cache_dir) -> None:
    with pytest.raises(CliError) as excinfo:
        store.open_store(read_only=True)

    assert excinfo.value.error_type == "CacheMissing"
    assert excinfo.value.exit_code == 2


def test_reader_while_another_process_writes_is_cache_locked(cache_dir) -> None:
    store.open_store().close()
    holder = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import duckdb, sys, time; c = duckdb.connect(sys.argv[1]); print('ready', flush=True); time.sleep(30)",
            str(store.cache_path()),
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert holder.stdout is not None and holder.stdout.readline().strip() == "ready"
        with pytest.raises(CliError) as excinfo:
            store.open_store(read_only=True)
    finally:
        holder.kill()
        holder.wait()

    assert excinfo.value.error_type == "CacheLocked"
    assert excinfo.value.retryable is True


def test_status_counts_on_memory_store() -> None:
    conn = store.open_store(":memory:")
    conn.execute(
        "INSERT INTO company (code, name, delisted_on) VALUES ('005930', 'A', NULL), ('117930', 'B', DATE '2017-03-07')"
    )
    conn.execute(
        "INSERT INTO ohlcv (code, date, close) VALUES "
        "('005930', DATE '2016-01-04', 1.0), ('005930', DATE '2026-10-16', 2.0), ('U0001', DATE '2026-10-16', 3.0)"
    )
    conn.execute("INSERT INTO load_log (run_at, kind) VALUES (?, 'ohlcv')", [datetime(2026, 10, 18, 16, 0)])

    result = store.status(conn)

    assert result["company"] == {"listed": 1, "delisted": 1}
    assert result["ohlcv"] == {"rows": 3, "codes": 2, "first_date": "2016-01-04", "last_date": "2026-10-16"}
    assert result["last_load"] == {"ohlcv": "2026-10-18T16:00:00"}


def test_cache_status_command(cache_dir) -> None:
    conn = store.open_store()
    conn.execute("INSERT INTO ohlcv (code, date, close) VALUES ('005930', ?, 1.0)", [date(2026, 10, 16)])
    conn.close()

    result = run_cli(["cache", "status", "--json"])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["path"] == str(cache_dir / "market.duckdb")
    assert payload["ohlcv"]["rows"] == 1


def test_cache_status_without_file_exits_2(cache_dir) -> None:
    result = run_cli(["cache", "status", "--json"])

    assert result.exit_code == 2
    assert json.loads(result.stdout)["error"]["type"] == "CacheMissing"


def test_cache_unknown_subcommand_exits_2() -> None:
    result = run_cli(["cache", "nope", "--json"])

    assert result.exit_code == 2
    assert "status" in json.loads(result.stdout)["error"]["data"]["subcommands"]
