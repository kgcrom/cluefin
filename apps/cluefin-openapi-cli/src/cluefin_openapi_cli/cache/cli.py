"""`cache <sub>` meta command. `load` writes from brokers; every other subcommand only reads the file."""

from __future__ import annotations

import sys
from datetime import date, datetime
from typing import Any, Callable

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.load import PARTS, Sources, run_load
from cluefin_openapi_cli.cliargs import _parse_named_options, _str_option
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError, classify_exception
from cluefin_openapi_cli.output import render_output

__all__ = ["SUBCOMMANDS", "run_cache"]


def _run_status(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache status` does not accept positional arguments.", exit_code=EXIT_USAGE)
    path = store.cache_path()
    conn = store.open_store(path, read_only=True)
    try:
        payload = {"path": str(path), "size_bytes": path.stat().st_size, **store.status(conn)}
    finally:
        conn.close()
    render_output(payload, force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False)))


_DEFAULT_SINCE = "20160101"


def _client_factory() -> Any:
    # Imported here so offline subcommands never load client code; tests replace this function.
    from cluefin_openapi.client_factory import BrokerClientFactory

    return BrokerClientFactory()


def _parse_day(raw: str, option: str) -> date:
    try:
        return datetime.strptime(raw, "%Y%m%d").date()
    except ValueError:
        raise CliError(f"`--{option}` must be YYYYMMDD, got `{raw}`.", exit_code=EXIT_USAGE) from None


def _parse_parts(raw: str | None) -> tuple[str, ...]:
    if raw is None or raw == "all":
        return PARTS
    parts = tuple(part.strip() for part in raw.split(",") if part.strip())
    unknown = [part for part in parts if part not in PARTS]
    if unknown or not parts:
        raise CliError(
            f"`--only` takes {', '.join(PARTS)} or all; got `{raw}`.",
            exit_code=EXIT_USAGE,
            data={"parts": list(PARTS)},
        )
    return tuple(part for part in PARTS if part in parts)


def _progress(message: str) -> None:
    sys.stderr.write(f"[cache load] {datetime.now():%H:%M:%S} {message}\n")
    sys.stderr.flush()


def _run_load(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`cache load` does not accept positional arguments.", exit_code=EXIT_USAGE)
    parts = _parse_parts(_str_option(options, "only"))
    since = _parse_day(_str_option(options, "since") or _DEFAULT_SINCE, "since")
    path = store.cache_path()
    conn = store.open_store(path)
    try:
        result = run_load(
            conn,
            Sources(factory=_client_factory()),
            parts=parts,
            since=since,
            today=date.today(),
            progress=_progress,
        )
    except CliError:
        raise
    except Exception as exc:
        raise classify_exception(exc, command="cache.load", broker="cache") from exc
    finally:
        conn.close()
    render_output(
        {"path": str(path), "since": since.isoformat(), "parts": result},
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


SUBCOMMANDS: dict[str, Callable[[list[str]], None]] = {
    "status": _run_status,
    "load": _run_load,
}


def run_cache(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            "Usage: cache <" + "|".join(SUBCOMMANDS) + "> [options].",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
