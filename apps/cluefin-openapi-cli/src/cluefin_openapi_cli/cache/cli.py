"""`cache <sub>` meta command: the only commands that read a local file instead of a broker."""

from __future__ import annotations

from typing import Callable

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cliargs import _parse_named_options
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
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


SUBCOMMANDS: dict[str, Callable[[list[str]], None]] = {
    "status": _run_status,
}


def run_cache(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            "Usage: cache <" + "|".join(SUBCOMMANDS) + "> [options].",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
