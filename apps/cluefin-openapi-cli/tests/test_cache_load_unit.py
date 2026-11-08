"""`cache load` orchestration: lazy broker clients, part order, and one `load_log` row per part."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from cluefin_openapi_cli.cache import load as load_module
from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.load import PARTS, Sources, run_load


class _Stats(SimpleNamespace):
    def as_dict(self) -> dict:
        return {"part": self.part}


def _stats(part: str, **counts: int) -> _Stats:
    return _Stats(part=part, errors=[], **counts)


@pytest.fixture
def conn(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    connection = store.open_store()
    yield connection
    connection.close()


@pytest.fixture
def fake_parts(monkeypatch) -> list[tuple[str, dict]]:
    """Replace each part loader with one that records its keyword arguments."""

    seen: list[tuple[str, dict]] = []

    def fake(part: str, **counts: int):
        def loader(_conn, **kwargs):
            seen.append((part, kwargs))
            return _stats(part, **counts)

        return loader

    monkeypatch.setattr(load_module, "load_company", fake("company", listed=10, delisted_found=2))
    monkeypatch.setattr(load_module, "load_bars", fake("ohlcv", loaded=5, rows=50, replaced=1))
    monkeypatch.setattr(load_module, "load_adjustments", fake("adj", codes=3, recomputed=2))
    monkeypatch.setattr(load_module, "load_rates", fake("rates", series=3, rows=30))
    monkeypatch.setattr(load_module, "load_theme", fake("theme", themes=4, members=40))
    monkeypatch.setattr(load_module, "load_financials", fake("financials", codes_ok=6, rows=60))
    return seen


def test_runs_every_part_in_order_and_logs_each(conn, fake_parts) -> None:
    factory = MagicMock()
    result = run_load(
        conn,
        Sources(factory),
        parts=PARTS,
        since=date(2026, 1, 1),
        today=date(2026, 11, 8),
        last_day=date(2026, 11, 6),
        progress=lambda _msg: None,
    )

    assert list(result) == list(PARTS)
    assert [part for part, _ in fake_parts] == list(PARTS)
    assert result["ohlcv"]["last_day"] == "2026-11-06"
    assert all("seconds" in summary for summary in result.values())
    logged = conn.execute("SELECT kind, codes, rows, replaced, errors FROM load_log ORDER BY rowid").fetchall()
    assert logged == [
        ("company", 12, 0, 0, 0),
        ("ohlcv", 5, 50, 1, 0),
        ("adj", 3, 0, 2, 0),
        ("rates", 3, 30, 0, 0),
        ("theme", 4, 40, 0, 0),
        ("financials", 6, 60, 0, 0),
    ]


def test_only_creates_the_brokers_a_part_needs(conn, fake_parts) -> None:
    factory = MagicMock()
    run_load(
        conn,
        Sources(factory),
        parts=("rates",),
        since=date(2026, 1, 1),
        today=date(2026, 11, 8),
        last_day=date(2026, 11, 6),
        progress=lambda _msg: None,
    )
    assert [c.args for c in factory.create.call_args_list] == [("ecos",)]


def test_kis_client_does_its_own_retries_off(conn) -> None:
    """EGW00201 is retried by `throttle.kis_call`; the client's slower backoff must not stack on top."""

    factory = MagicMock()
    sources = Sources(factory)
    kis = sources.kis
    assert kis.max_retries == 0
    assert sources.kis is kis
    assert factory.create.call_count == 1
