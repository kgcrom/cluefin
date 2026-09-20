from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Any

from cluefin_openapi_cli.cliargs import (
    _merge_params,
    _parse_fields,
    _parse_limit,
    _parse_named_options,
    _str_option,
)
from cluefin_openapi_cli.errors import (
    EXIT_CODES,
    EXIT_USAGE,
    CliError,
    classify_exception,
)
from cluefin_openapi_cli.metadata import (
    BROKER_ROLES,
)
from cluefin_openapi_cli.output import (
    attach_truncation,
    limit_rows,
    render_output,
    select_fields,
    stdout_is_tty,
    to_jsonable,
)
from cluefin_openapi_cli.payloads import (
    _SEARCH_DEFAULT_LIMIT,
    _SEARCH_MAX_LIMIT,
    APP_NAME,
    _brokers_payload,
    _command_summary,
    _discovery_payload,
    _dry_run_payload,
    _global_option_rows,
    _list_payload,
    _render_broker_help,
    _render_leaf_help,
    _schema_payload,
    _search_payload,
)
from cluefin_openapi_cli.recipes import get_recipe, recipe_summaries
from cluefin_openapi_cli.registry import CommandSpec, get_registry

__all__ = ["CLIResult", "CliError", "dispatch", "main", "run_cli"]

META_COMMANDS = ("search", "brokers", "list", "describe", "schema", "domains", "tags", "recipes", "recipe")

# Per-meta-command help. `usage` is the single source of truth for the root `--help`
# listing too (`_run_root`), so the two can never drift apart.
_META_HELP: dict[str, dict[str, Any]] = {
    "search": {
        "description": (
            "Ranked natural-language lookup over every command. Accepts Korean or English task "
            "descriptions and returns a short shortlist. Use this before `list`."
        ),
        "usage": [
            f"{APP_NAME} search <text...> [--limit N] [--broker B] [--domain D] [--tag T] [--json]",
        ],
        "options": [
            {"flag": "--limit N", "meaning": f"How many candidates to return (default {8}, max 50)."},
            {"flag": "--broker B", "meaning": "Restrict candidates to one broker."},
            {"flag": "--domain D", "meaning": "Restrict candidates to one domain."},
            {"flag": "--tag T", "meaning": "Restrict candidates to one tag."},
            {"flag": "--category C", "meaning": "Restrict candidates to one category."},
            {"flag": "--full", "meaning": "Full rows including parameters instead of brief rows."},
            {"flag": "--explain", "meaning": "Include per-term score contributions."},
        ],
        "examples": [
            f"uv run {APP_NAME} search 외국인 순매수 상위 종목 --json",
            f"uv run {APP_NAME} search dividend schedule --limit 5 --compact",
        ],
        "notes": [
            "Never returns an empty result: a miss carries `fallback` with runnable next steps.",
            "Each row carries `next`, the `schema` call for that command.",
        ],
    },
    "brokers": {
        "description": "Broker roles, command counts, and whether each broker's credentials are configured.",
        "usage": [f"{APP_NAME} brokers [--json]"],
        "options": [],
        "examples": [f"uv run {APP_NAME} brokers --json"],
        "notes": ["`credentials.configured` is a boolean; secret values are never echoed."],
    },
    "list": {
        "description": "Catalog of broker commands. Brief rows by default; filterable by broker, category, domain, or tag.",
        "usage": [
            f"{APP_NAME} list [--broker BROKER] [--category CATEGORY] [--json]",
            f"{APP_NAME} list [--domain DOMAIN] [--tag TAG] [--query TEXT] [--full] [--json]",
        ],
        "options": [
            {"flag": "--broker B", "meaning": "Restrict to one broker (kis, kiwoom, dart)."},
            {"flag": "--category C", "meaning": "Restrict to one provider SDK category."},
            {"flag": "--domain D", "meaning": "Restrict to one agent-intent domain; see `domains`."},
            {"flag": "--tag T", "meaning": "Restrict to one capability tag; see `tags`."},
            {"flag": "--query TEXT", "meaning": "Literal substring filter on name and description."},
            {"flag": "--full", "meaning": "Full per-command rows including parameters (large)."},
        ],
        "examples": [
            f"uv run {APP_NAME} list --broker kis --domain chart --json",
            f"uv run {APP_NAME} list --tag dividend --json",
        ],
        "notes": ["Always filter. An unfiltered `list` is the whole catalog."],
    },
    "describe": {
        "description": "Discovery-oriented detail for one command: metadata, use cases, and examples.",
        "usage": [
            f"{APP_NAME} describe <broker> <category> <name> [--json]",
            f"{APP_NAME} describe dart <name> [--json]",
        ],
        "options": [],
        "examples": [f"uv run {APP_NAME} describe kis stock current-price --json"],
        "notes": ["Use `schema` instead when you are about to call the command."],
    },
    "schema": {
        "description": "Execution contract for one command: JSON Schema, per-parameter flags, and runnable invoke strings.",
        "usage": [
            f"{APP_NAME} schema <broker> <category> <name> [--json]",
            f"{APP_NAME} schema dart <name> [--json]",
        ],
        "options": [],
        "examples": [f"uv run {APP_NAME} schema kis stock current-price --json"],
        "notes": ["`invoke.dry_run` is runnable as-is; `enum` and `pattern` are enforced locally."],
    },
    "domains": {
        "description": "Agent-intent domains with when_to_use, avoid_when, and a runnable example_filter.",
        "usage": [f"{APP_NAME} domains [--json]"],
        "options": [],
        "examples": [f"uv run {APP_NAME} domains --json"],
        "notes": [],
    },
    "tags": {
        "description": "Capability tags with when_to_use, avoid_when, and a runnable example_filter.",
        "usage": [f"{APP_NAME} tags [--json]"],
        "options": [],
        "examples": [f"uv run {APP_NAME} tags --json"],
        "notes": [],
    },
    "recipes": {
        "description": "Multi-step workflow guides that combine several commands.",
        "usage": [f"{APP_NAME} recipes [--json]"],
        "options": [],
        "examples": [f"uv run {APP_NAME} recipes --json"],
        "notes": ["Recipes describe an order of exploration; they do not execute commands."],
    },
    "recipe": {
        "description": "One workflow guide, step by step.",
        "usage": [f"{APP_NAME} recipe <name> [--json]"],
        "options": [],
        "examples": [f"uv run {APP_NAME} recipe stock-research --json"],
        "notes": [],
    },
}

# Usage lines for the dynamic broker commands, appended after the meta-command lines.
_DYNAMIC_USAGE = (
    f"{APP_NAME} <broker> <category> <name> [--params-json JSON] [schema options] "
    "[--dry-run] [--fields a,b] [--compact] [--json]",
    f"{APP_NAME} dart <name> [--params-json JSON] [schema options] [--dry-run] [--fields a,b] [--compact] [--json]",
)


@dataclass(slots=True)
class CLIResult:
    exit_code: int
    stdout: str
    stderr: str


# ---------------------------------------------------------------------------
# Payload builders
# ---------------------------------------------------------------------------


#: Rows returned by an unfiltered `list --full`, which is otherwise ~67k tokens.


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Meta commands
# ---------------------------------------------------------------------------


def _run_root(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    force_json = bool(options.get("json", False))
    registry = get_registry()
    brokers = list(registry.iter_brokers())
    payload: dict[str, Any] = {
        "app": APP_NAME,
        "interactive": stdout_is_tty(),
        "brokers": [
            {"name": name, "role": BROKER_ROLES[name].role if name in BROKER_ROLES else "unknown"} for name in brokers
        ],
        "commands": list(META_COMMANDS),
        "workflow": [
            f"uv run {APP_NAME} brokers --json",
            f"uv run {APP_NAME} list --broker kis --json",
            f"uv run {APP_NAME} schema kis stock current-price --json",
            f"uv run {APP_NAME} kis stock current-price --stock-code 005930 --dry-run --json",
            f"uv run {APP_NAME} kis stock current-price --stock-code 005930 --json",
        ],
        "exit_codes": {str(code): meaning for code, meaning in EXIT_CODES.items()},
    }
    if bool(options.get("help", False)):
        payload["usage"] = _all_usage_lines()
        payload["global_options"] = _global_option_rows()
    render_output(payload, force_json=force_json, compact=bool(options.get("compact", False)))


def _all_usage_lines() -> list[str]:
    """Every usage line, meta commands first, built from the one `_META_HELP` table."""

    lines: list[str] = []
    for name in META_COMMANDS:
        lines.extend(_META_HELP[name]["usage"])
    lines.extend(_DYNAMIC_USAGE)
    return lines


def _help_requested(argv: list[str]) -> bool:
    return any(token == "--help" or token.startswith("--help=") or token == "-h" for token in argv)


def _render_meta_help(name: str, argv: list[str]) -> None:
    """Render help for one meta command. Keeps every runner free of help handling."""

    entry = _META_HELP[name]
    _, options = _parse_named_options([token for token in argv if token not in {"--help", "-h"}])
    payload = {
        "command": name,
        "description": entry["description"],
        "usage": list(entry["usage"]),
        "options": list(entry["options"]),
        "global_options": _global_option_rows(),
        "examples": list(entry["examples"]),
        "notes": list(entry["notes"]),
    }
    render_output(
        payload,
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_search(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    query_option = _str_option(options, "query")
    query = " ".join([*positional, *([query_option] if query_option else [])]).strip()
    if not query:
        raise CliError(
            "`search` needs a query.",
            exit_code=EXIT_USAGE,
            hint=f"Try `{APP_NAME} search 외국인 순매수 --json`.",
        )

    registry = get_registry()
    broker = _str_option(options, "broker")
    if broker is not None and broker not in set(registry.iter_brokers()):
        raise CliError(
            f"Unknown broker `{broker}`.",
            exit_code=EXIT_USAGE,
            data={"allowed": list(registry.iter_brokers())},
        )

    raw_limit = _parse_limit(options.get("limit"))
    limit = _SEARCH_DEFAULT_LIMIT if raw_limit is None else max(1, min(raw_limit, _SEARCH_MAX_LIMIT))

    render_output(
        _search_payload(
            query=query,
            limit=limit,
            broker=broker,
            domain=_str_option(options, "domain"),
            tag=_str_option(options, "tag"),
            category=_str_option(options, "category"),
            full=bool(options.get("full", False)),
            explain=bool(options.get("explain", False)),
        ),
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_brokers(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`brokers` does not accept positional arguments.", exit_code=EXIT_USAGE)
    render_output(
        _brokers_payload(),
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_list(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`list` does not accept positional arguments.", exit_code=EXIT_USAGE)

    broker = _str_option(options, "broker")
    registry = get_registry()
    if broker is not None and broker not in set(registry.iter_brokers()):
        raise CliError(
            f"Unknown broker `{broker}`.",
            exit_code=EXIT_USAGE,
            data={"allowed": list(registry.iter_brokers())},
        )

    render_output(
        _list_payload(
            broker=broker,
            category=_str_option(options, "category"),
            domain=_str_option(options, "domain"),
            tag=_str_option(options, "tag"),
            query=_str_option(options, "query"),
            full=bool(options.get("full", False)),
            limit=_parse_limit(options.get("limit")),
        ),
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_domains(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`domains` does not accept positional arguments.", exit_code=EXIT_USAGE)
    render_output(_discovery_payload("domains"), force_json=bool(options.get("json", False)))


def _run_tags(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`tags` does not accept positional arguments.", exit_code=EXIT_USAGE)
    render_output(_discovery_payload("tags"), force_json=bool(options.get("json", False)))


def _run_recipes(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`recipes` does not accept positional arguments.", exit_code=EXIT_USAGE)
    summaries = recipe_summaries()
    render_output({"recipes": summaries, "count": len(summaries)}, force_json=bool(options.get("json", False)))


def _run_recipe(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if len(positional) != 1:
        raise CliError("Usage: recipe <name>.", exit_code=EXIT_USAGE)

    recipe = get_recipe(positional[0])
    if recipe is None:
        raise CliError(f"Unknown recipe `{positional[0]}`.", exit_code=EXIT_USAGE)

    render_output({"recipe": to_jsonable(recipe)}, force_json=bool(options.get("json", False)))


def _resolve_positional_path(verb: str, positional: list[str]) -> tuple[str, ...]:
    usage = f"Usage: {verb} <broker> <category> <name> (or `{verb} dart <name>`)."
    if not positional:
        raise CliError(usage, exit_code=EXIT_USAGE)

    broker = positional[0]
    path_parts = positional[1:]
    if broker == "dart" and len(path_parts) == 1:
        return (broker, path_parts[0])
    if len(path_parts) == 2:
        return (broker, path_parts[0], path_parts[1])
    raise CliError(usage, exit_code=EXIT_USAGE)


def _lookup_command(path: tuple[str, ...]) -> CommandSpec:
    registry = get_registry()
    command = registry.resolve_command(path)
    if command is None:
        raise CliError(
            f"Unknown command path: {' '.join(path)}",
            exit_code=EXIT_USAGE,
            hint=f"Run `list --broker {path[0]} --json` to see valid paths." if path else None,
        )
    return command


def _run_describe(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    command = _lookup_command(_resolve_positional_path("describe", positional))
    render_output(
        {"command": _command_summary(command)},
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_schema(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    command = _lookup_command(_resolve_positional_path("schema", positional))
    render_output(
        _schema_payload(command),
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


# ---------------------------------------------------------------------------
# Broker commands
# ---------------------------------------------------------------------------


def _run_dynamic(argv: list[str]) -> None:
    if not argv:
        _run_root([])
        return

    registry = get_registry()
    broker = argv[0]
    if broker not in set(registry.iter_brokers()):
        raise CliError(
            f"Unknown top-level command `{broker}`.",
            exit_code=EXIT_USAGE,
            data={"meta_commands": list(META_COMMANDS), "brokers": list(registry.iter_brokers())},
        )

    positional, options = _parse_named_options(argv[1:])
    help_requested = bool(options.get("help", False))
    force_json_flag = bool(options.get("json", False))

    if help_requested and _render_broker_help(broker, positional, force_json=force_json_flag):
        return

    if broker == "dart":
        if len(positional) < 1:
            raise CliError(f"Usage: {APP_NAME} dart <name> [options]", exit_code=EXIT_USAGE)
        path: tuple[str, ...] = (broker, positional[0])
    else:
        if len(positional) < 2:
            raise CliError(f"Usage: {APP_NAME} {broker} <category> <name> [options]", exit_code=EXIT_USAGE)
        path = (broker, positional[0], positional[1])

    command = _lookup_command(path)

    if help_requested:
        _render_leaf_help(command, force_json=force_json_flag)
        return

    compact = bool(options.pop("compact", False))
    fields = _parse_fields(options.pop("fields", None))
    dry_run = bool(options.pop("dry_run", False))
    limit = _parse_limit(options.pop("limit", None))

    force_json, params = _merge_params(command, options)

    if dry_run:
        payload = _dry_run_payload(command, params)
        render_output(select_fields(payload, fields), force_json=force_json, compact=compact)
        return

    try:
        result = registry.invoke_command(command, params)
    except CliError:
        raise
    except Exception as exc:
        raise classify_exception(exc, command=command.qualified_name, broker=command.broker) from exc

    data = to_jsonable(result)
    if fields:
        data = select_fields(data, fields)
    if limit is not None:
        data, notes = limit_rows(data, limit)
        data = attach_truncation(data, limit, notes)
    render_output(data, force_json=force_json, compact=compact)


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


def _json_requested(argv: list[str]) -> bool:
    return "--json" in argv or not stdout_is_tty()


def _emit_error(exc: CliError, *, force_json: bool, compact: bool) -> None:
    if force_json:
        render_output(exc.to_payload(), force_json=True, compact=compact)
        return
    sys.stderr.write(exc.message)
    if exc.hint:
        sys.stderr.write(f"\n  hint: {exc.hint}")
    sys.stderr.write("\n")


def dispatch(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] == "-h" or args[0].startswith("--"):
        _run_root(["--help", *args[1:]] if args and args[0] == "-h" else args)
        return

    runners = {
        "search": _run_search,
        "brokers": _run_brokers,
        "list": _run_list,
        "describe": _run_describe,
        "schema": _run_schema,
        "domains": _run_domains,
        "tags": _run_tags,
        "recipes": _run_recipes,
        "recipe": _run_recipe,
    }
    runner = runners.get(args[0])
    if runner is not None:
        rest = args[1:]
        if _help_requested(rest):
            _render_meta_help(args[0], rest)
            return
        runner(rest)
        return

    _run_dynamic(args)


def _quiet_client_logging() -> None:
    """Keep stderr clean for agents: client DEBUG/INFO chatter only with CLUEFIN_OPENAPI_DEBUG."""

    import os

    if os.environ.get("CLUEFIN_OPENAPI_DEBUG", "0").lower() in {"1", "true", "yes", "on"}:
        return
    try:
        from loguru import logger

        logger.remove()
        logger.add(sys.stderr, level="WARNING")
    except Exception:  # pragma: no cover - loguru is a transitive dependency; never fail on it
        return


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    _quiet_client_logging()
    try:
        dispatch(args)
    except CliError as exc:
        _emit_error(exc, force_json=_json_requested(args), compact="--compact" in args)
        raise SystemExit(exc.exit_code) from exc


def run_cli(argv: list[str] | None = None) -> CLIResult:
    stdout = io.StringIO()
    stderr = io.StringIO()
    old_argv = sys.argv[:]
    sys.argv = [old_argv[0] if old_argv else APP_NAME, *(argv or [])]

    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                main()
                exit_code = 0
            except SystemExit as exc:
                exit_code = int(getattr(exc, "code", 0) or 0)
    finally:
        sys.argv = old_argv

    return CLIResult(exit_code=exit_code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


if __name__ == "__main__":
    main()
