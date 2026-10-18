"""`cache load`: the one writer. Runs each part in order, one broker call at a time."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Callable

import duckdb

from cluefin_openapi_cli.cache.bars import load_bars
from cluefin_openapi_cli.cache.company import load_company

__all__ = ["PARTS", "Sources", "run_load"]

PARTS = ("company", "ohlcv")


@dataclass(slots=True)
class Sources:
    """Broker clients, created lazily so `--only` touches only the brokers it needs."""

    factory: Any
    _clients: dict[str, Any] | None = None

    def _get(self, broker: str) -> Any:
        if self._clients is None:
            self._clients = {}
        if broker not in self._clients:
            client = self.factory.create(broker)
            if broker == "kis":
                # EGW00201 is retried by throttle.kis_call after 0.1s, not by the client's 1s+ backoff.
                client.max_retries = 0
            self._clients[broker] = client
        return self._clients[broker]

    @property
    def kis(self) -> Any:
        return self._get("kis")

    @property
    def kiwoom(self) -> Any:
        return self._get("kiwoom")

    @property
    def dart(self) -> Any:
        return self._get("dart")


def run_load(
    conn: duckdb.DuckDBPyConnection,
    sources: Sources,
    *,
    parts: tuple[str, ...],
    since: date,
    today: date,
    last_day: date,
    progress: Callable[[str], None],
    sleep: Callable[[float], None] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for part in parts:
        started = time.perf_counter()
        run_at = datetime.now()
        if part == "company":
            stats = load_company(
                conn,
                kiwoom=sources.kiwoom,
                kis=sources.kis,
                dart=sources.dart,
                today=today,
                since=since,
                progress=progress,
                sleep=sleep,
            )
            summary = stats.as_dict()
            codes, rows, replaced, errors = stats.listed + stats.delisted_found, 0, 0, len(stats.errors)
        elif part == "ohlcv":
            bar_stats = load_bars(conn, kis=sources.kis, since=since, last_day=last_day, progress=progress, sleep=sleep)
            summary = {**bar_stats.as_dict(), "last_day": last_day.isoformat()}
            codes, rows, replaced, errors = bar_stats.loaded, bar_stats.rows, bar_stats.replaced, len(bar_stats.errors)
        else:  # pragma: no cover - PARTS is validated by the caller
            raise ValueError(part)
        seconds = round(time.perf_counter() - started, 1)
        conn.execute(
            "INSERT INTO load_log VALUES (?, ?, ?, ?, ?, ?, ?)", [run_at, part, codes, rows, replaced, errors, seconds]
        )
        result[part] = {**summary, "seconds": seconds}
    return result
