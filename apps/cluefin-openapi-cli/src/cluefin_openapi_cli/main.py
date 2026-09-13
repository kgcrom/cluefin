from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Any

from cluefin_openapi_cli.errors import (
    EXIT_CODES,
    EXIT_USAGE,
    CliError,
    classify_exception,
)
from cluefin_openapi_cli.metadata import (
    BROKER_ORDER,
    BROKER_ROLES,
    broker_rank,
    build_taxonomy_entry,
    category_info,
)
from cluefin_openapi_cli.output import (
    attach_truncation,
    limit_rows,
    render_output,
    select_fields,
    stdout_is_tty,
    to_jsonable,
)
from cluefin_openapi_cli.recipes import get_recipe, recipe_summaries
from cluefin_openapi_cli.registry import CommandSpec, get_registry
from cluefin_openapi_cli.search import search_commands

__all__ = ["CLIResult", "CliError", "dispatch", "main", "run_cli"]

APP_NAME = "cluefin-openapi-cli"
META_COMMANDS = ("search", "brokers", "list", "describe", "schema", "domains", "tags", "recipes", "recipe")
_BOOL_FLAGS = {"json", "help", "dry_run", "full", "compact", "explain"}

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


def _required_fields(command: CommandSpec) -> list[str]:
    return list(command.parameters.get("required", []))


def _command_brief(command: CommandSpec) -> dict[str, Any]:
    """The cheapest useful row for `list`: enough to pick a command, not to call it."""

    return {
        "qualified_name": command.qualified_name,
        "path_segments": list(command.path_segments),
        "broker": command.broker,
        "broker_role": command.broker_role,
        "description": command.description,
        "domains": list(command.domains),
        "tags": list(command.tags),
        "required": _required_fields(command),
        "kis_alternatives": list(command.kis_alternatives),
    }


def _command_summary(command: CommandSpec) -> dict[str, Any]:
    return {
        "broker": command.broker,
        "broker_role": command.broker_role,
        "category": command.category,
        "name": command.name,
        "qualified_name": command.qualified_name,
        "path_segments": list(command.path_segments),
        "description": command.description,
        "parameters": command.parameters,
        "returns": command.returns,
        "domains": list(command.domains),
        "tags": list(command.tags),
        "use_cases": list(command.use_cases),
        "examples": list(command.examples),
        "agent_notes": command.agent_notes,
        "required_credentials": list(command.required_credentials),
        "side_effect": command.side_effect,
        "kis_alternatives": list(command.kis_alternatives),
        "has_executor": command.executor is not None,
    }


def _option_rows(command: CommandSpec) -> list[dict[str, Any]]:
    properties = command.parameters.get("properties", {})
    required = set(command.parameters.get("required", []))
    rows = []
    for field_name, schema in properties.items():
        row: dict[str, Any] = {
            "flag": f"--{field_name.replace('_', '-')}",
            "field": field_name,
            "type": schema.get("type", "string"),
            "required": field_name in required,
            "description": schema.get("description"),
        }
        for key in ("enum", "pattern", "default", "minimum", "maximum"):
            if key in schema:
                row[key] = schema[key]
        if schema.get("type") in {"array", "object"}:
            row["pass_via"] = "--params-json"
        rows.append(row)
    return rows


def _invoke_examples(command: CommandSpec) -> dict[str, str]:
    base = " ".join(("uv run", APP_NAME, *command.path_segments))
    properties = command.parameters.get("properties", {})
    required = _required_fields(command)
    sample = {name: _example_value(name, properties.get(name, {})) for name in required}
    flags = " ".join(
        f"--{name.replace('_', '-')} {json.dumps(value, ensure_ascii=False)}" for name, value in sample.items()
    )
    params_json = json.dumps(sample, ensure_ascii=False, separators=(",", ":"))
    flags_command = f"{base} {flags} --json".replace("  ", " ")
    return {
        "flags": flags_command,
        "params_json": f"{base} --params-json '{params_json}' --json",
        "dry_run": f"{base} --params-json '{params_json}' --dry-run --json",
    }


def _example_value(field_name: str, schema: dict[str, Any]) -> Any:
    from cluefin_openapi_cli.metadata import _sample_value

    return _sample_value(field_name, schema)


def _schema_payload(command: CommandSpec) -> dict[str, Any]:
    parameters = dict(command.parameters)
    parameters.setdefault("type", "object")
    parameters.setdefault("additionalProperties", False)
    return {
        "command": command.qualified_name,
        "path_segments": list(command.path_segments),
        "broker": command.broker,
        "broker_role": command.broker_role,
        "description": command.description,
        "side_effect": command.side_effect,
        "required_credentials": list(command.required_credentials),
        "kis_alternatives": list(command.kis_alternatives),
        "parameters": parameters,
        "returns": command.returns,
        "options": _option_rows(command),
        "global_options": _global_option_rows(),
        "invoke": _invoke_examples(command),
        "agent_notes": command.agent_notes,
    }


def _global_option_rows() -> list[dict[str, str]]:
    return [
        {"flag": "--json", "meaning": "Force JSON output (default when stdout is not a TTY)."},
        {"flag": "--compact", "meaning": "Single-line JSON; cheapest to read back into context."},
        {"flag": "--fields a,b.c", "meaning": "Field mask on the result: top-level keys or dotted paths."},
        {
            "flag": "--limit N",
            "meaning": "Cap every result array at N rows; adds `_truncated` when data was cut. 0 = no limit.",
        },
        {"flag": "--params-json '{...}'", "meaning": "Whole parameter object; flags override its keys."},
        {"flag": "--dry-run", "meaning": "Validate locally and echo the resolved request; no network call."},
        {"flag": "--help", "meaning": "Command help as JSON."},
    ]


def _credentials_status(broker: str) -> dict[str, Any]:
    """Report whether a broker is configured without ever echoing a secret."""

    role = BROKER_ROLES.get(broker)
    required = list(role.credentials) if role else []
    try:
        from cluefin_openapi import BrokerClientConfig

        config = BrokerClientConfig.from_env()
    except Exception:  # pragma: no cover - defensive: config loading should not break discovery
        return {"required": required, "configured": None, "env": None}

    values = {
        "kis": (config.kis_app_key, config.kis_secret_key),
        "kiwoom": (config.kiwoom_app_key, config.kiwoom_secret_key),
        "dart": (config.dart_auth_key,),
    }.get(broker, ())
    envs = {"kis": config.kis_env, "kiwoom": config.kiwoom_env}
    return {
        "required": required,
        "configured": bool(values) and all(bool(value) for value in values),
        "env": envs.get(broker),
    }


def _brokers_payload() -> dict[str, Any]:
    registry = get_registry()
    commands = registry.list_commands()
    known = set(registry.iter_brokers())
    rows = []
    for name in BROKER_ORDER:
        if name not in known:
            continue
        role = BROKER_ROLES[name]
        broker_commands = [command for command in commands if command.broker == name]
        row: dict[str, Any] = {
            "name": name,
            "role": role.role,
            "description": role.description,
            "when_to_use": role.when_to_use,
            "command_count": len(broker_commands),
            "credentials": _credentials_status(name),
            "list_command": f"uv run {APP_NAME} list --broker {name} --json",
        }
        if role.role == "auxiliary":
            exclusive = [command.qualified_name for command in broker_commands if not command.kis_alternatives]
            row["kiwoom_only_commands"] = exclusive
            row["kiwoom_only_count"] = len(exclusive)
        rows.append(row)
    return {"brokers": rows, "count": len(rows), "order": [row["name"] for row in rows]}


#: Rows returned by an unfiltered `list --full`, which is otherwise ~67k tokens.
_UNFILTERED_FULL_LIMIT = 25


def _list_payload(
    *,
    broker: str | None,
    category: str | None,
    domain: str | None,
    tag: str | None,
    query: str | None,
    full: bool,
    limit: int | None = None,
) -> dict[str, Any]:
    registry = get_registry()
    commands = registry.list_commands(broker=broker, category=category, domain=domain, tag=tag)
    if query:
        needle = query.lower()
        commands = [
            command
            for command in commands
            if needle in command.qualified_name.lower() or needle in command.description.lower()
        ]
    commands = sorted(commands, key=lambda command: (broker_rank(command.broker), command.path_segments))
    total = len(commands)

    narrowed = any(value is not None for value in (broker, category, domain, tag, query))
    effective = limit
    if effective is None and full and not narrowed:
        effective = _UNFILTERED_FULL_LIMIT
    if effective is not None and effective > 0:
        commands = commands[:effective]

    builder = _command_summary if full else _command_brief
    payload: dict[str, Any] = {
        "broker": broker,
        "category": category,
        "domain": domain,
        "tag": tag,
        "query": query,
        "detail": "full" if full else "brief",
        "count": total,
        "returned": len(commands),
        "commands": [to_jsonable(builder(command)) for command in commands],
    }
    if len(commands) < total:
        payload["truncated"] = True
        payload["hint"] = (
            f"{total} commands matched; {len(commands)} returned. "
            "Narrow with --broker/--domain/--tag/--query, or pass --limit 0 for all rows."
        )
    if query:
        payload.setdefault(
            "hint",
            "`--query` is a literal substring filter. For a natural-language or Korean task "
            "description use `search <text>`.",
        )
    return payload


def _discovery_payload(kind: str) -> dict[str, Any]:
    registry = get_registry()
    commands = registry.list_commands()
    values = sorted({value for command in commands for value in getattr(command, kind)})
    return {
        kind: [
            build_taxonomy_entry(
                kind=kind,
                name=value,
                command_count=sum(value in getattr(command, kind) for command in commands),
                app_name=APP_NAME,
            )
            for value in values
        ],
        "count": len(values),
    }


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def _parse_named_options(argv: list[str]) -> tuple[list[str], dict[str, str | bool]]:
    positional: list[str] = []
    options: dict[str, str | bool] = {}
    index = 0

    while index < len(argv):
        token = argv[index]
        if not token.startswith("--"):
            positional.append(token)
            index += 1
            continue

        name, has_inline, inline_value = token[2:].partition("=")
        key = name.replace("-", "_")

        if key in _BOOL_FLAGS and not has_inline:
            options[key] = True
            index += 1
            continue

        if has_inline:
            options[key] = inline_value
            index += 1
            continue

        if index + 1 >= len(argv):
            raise CliError(f"Option `{token}` requires a value.", exit_code=EXIT_USAGE)

        options[key] = argv[index + 1]
        index += 2

    return positional, options


def _load_params_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CliError(
            "`--params-json` must be valid JSON.",
            exit_code=EXIT_USAGE,
            data={"position": exc.pos, "detail": exc.msg},
        ) from exc

    if not isinstance(payload, dict):
        raise CliError("`--params-json` must decode to an object.", exit_code=EXIT_USAGE)

    return payload


def _coerce_value(raw_value: str, schema: dict[str, Any]) -> Any:
    schema_type = schema.get("type", "string")
    if schema_type == "integer":
        try:
            return int(raw_value)
        except ValueError as exc:
            raise CliError(f"Invalid integer value `{raw_value}`.", exit_code=EXIT_USAGE) from exc
    if schema_type == "number":
        try:
            return float(raw_value)
        except ValueError as exc:
            raise CliError(f"Invalid number value `{raw_value}`.", exit_code=EXIT_USAGE) from exc
    if schema_type == "boolean":
        lowered = raw_value.lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
        raise CliError(f"Invalid boolean value `{raw_value}`.", exit_code=EXIT_USAGE)
    if schema_type in {"array", "object"}:
        try:
            decoded = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            raise CliError(
                f"Value for a {schema_type} field must be JSON (or use --params-json).",
                exit_code=EXIT_USAGE,
            ) from exc
        return decoded
    return raw_value


def _render_leaf_help(command: CommandSpec, *, force_json: bool) -> None:
    render_output(
        {
            "command": _command_summary(command),
            "options": _option_rows(command),
            "global_options": _global_option_rows(),
            "invoke": _invoke_examples(command),
            "supports_params_json": True,
        },
        force_json=force_json,
    )


def _merge_params(command: CommandSpec, options: dict[str, str | bool]) -> tuple[bool, dict[str, Any]]:
    """Merge --params-json with schema flags, coerce, and validate.

    Returns ``(force_json, params)``. Output-only options (compact/fields/dry_run) are
    dropped here; callers extract them before merging.
    """

    force_json = bool(options.pop("json", False))
    help_requested = bool(options.pop("help", False))
    for key in ("compact", "fields", "dry_run", "full", "limit"):
        options.pop(key, None)
    params_json = options.pop("params_json", None)
    if params_json is not None and not isinstance(params_json, str):
        raise CliError("`--params-json` requires a string value.", exit_code=EXIT_USAGE)

    if help_requested:
        _render_leaf_help(command, force_json=force_json)
        return force_json, {}

    merged = _load_params_json(params_json if isinstance(params_json, str) else None)
    properties = command.parameters.get("properties", {})

    for field_name, raw_value in options.items():
        if field_name not in properties:
            raise CliError(
                f"Unknown option `--{field_name.replace('_', '-')}` for `{command.qualified_name}`.",
                exit_code=EXIT_USAGE,
                data={"allowed": sorted(f"--{name.replace('_', '-')}" for name in properties)},
                hint=f"Run `schema {' '.join(command.path_segments)} --json` for the accepted options.",
            )
        if isinstance(raw_value, bool):
            merged[field_name] = raw_value
        else:
            merged[field_name] = _coerce_value(raw_value, properties[field_name])

    from cluefin_openapi_cli.validation import validate_params

    report = validate_params(merged, command.parameters)
    if not report.ok:
        missing = [issue.field for issue in report.issues if issue.problem == "required"]
        raise CliError(
            "Parameter validation failed.",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"command": command.qualified_name, "missing": missing, "issues": report.to_list()},
            hint=f"Run `schema {' '.join(command.path_segments)} --json` and fix the listed fields.",
        )

    return force_json, merged


def _parse_fields(raw: str | bool | None) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _parse_limit(raw: str | bool | None) -> int | None:
    """Parse ``--limit N``. ``None`` means the flag was absent; ``0`` means no limit."""

    if raw is None or raw is False:
        return None
    if raw is True:
        raise CliError("`--limit` requires an integer value.", exit_code=EXIT_USAGE)
    try:
        return int(str(raw).strip())
    except ValueError as exc:
        raise CliError(
            f"`--limit` requires an integer value, got `{raw}`.",
            exit_code=EXIT_USAGE,
            hint="Use `--limit 20`, or `--limit 0` for no limit.",
        ) from exc


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


_SEARCH_DEFAULT_LIMIT = 8
_SEARCH_MAX_LIMIT = 50


def _search_payload(
    *,
    query: str,
    limit: int,
    broker: str | None,
    domain: str | None,
    tag: str | None,
    category: str | None,
    full: bool,
    explain: bool,
) -> dict[str, Any]:
    registry = get_registry()
    result = search_commands(
        registry,
        query,
        limit=limit,
        broker=broker,
        domain=domain,
        tag=tag,
        category=category,
        explain=explain,
    )
    builder = _command_summary if full else _command_brief
    rows = []
    for hit in result.hits:
        row = to_jsonable(builder(hit.command))
        row["score"] = hit.score
        row["relative"] = hit.relative
        row["matched"] = list(hit.matched)
        row["next"] = f"uv run {APP_NAME} schema {' '.join(hit.command.path_segments)} --json"
        rows.append(row)

    payload: dict[str, Any] = {
        "query": query,
        "expanded": list(result.expanded),
        "unmatched_terms": list(result.unmatched_terms),
        "filters": {"broker": broker, "domain": domain, "tag": tag, "category": category},
        "limit": limit,
        "confidence": result.confidence,
        "count": len(rows),
        "commands": rows,
    }
    if result.fallback is not None:
        payload["fallback"] = result.fallback
    if explain and result.per_term:
        payload["scoring"] = {"model": "bm25f", "per_term": result.per_term}
    return payload


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


def _str_option(options: dict[str, str | bool], key: str) -> str | None:
    value = options.get(key)
    return value if isinstance(value, str) else None


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


def _render_broker_help(broker: str, positional: list[str], *, force_json: bool) -> bool:
    registry = get_registry()
    if broker == "dart":
        if positional:
            return False
        commands = registry.list_commands(broker=broker)
        render_output(
            {
                "broker": broker,
                "role": BROKER_ROLES[broker].role,
                "description": BROKER_ROLES[broker].description,
                "command_count": len(commands),
                "commands": [
                    {
                        "name": command.name,
                        "description": command.description,
                        "required": _required_fields(command),
                        "domains": list(command.domains),
                        "tags": list(command.tags),
                    }
                    for command in commands
                ],
            },
            force_json=force_json,
        )
        return True

    if not positional:
        commands = registry.list_commands(broker=broker)
        categories = []
        for name in sorted({command.category for command in commands}):
            in_category = [command for command in commands if command.category == name]
            info = category_info(name)
            row: dict[str, Any] = {"name": name, "command_count": len(in_category)}
            if info is not None:
                row["description"] = info.description
                row["when_to_use"] = info.when_to_use
            # Union over the real commands, so this reflects the authored taxonomy.
            row["domains"] = sorted({d for command in in_category for d in command.domains})
            row["tags"] = sorted({t for command in in_category for t in command.tags})
            row["list_command"] = f"uv run {APP_NAME} list --broker {broker} --category {name} --json"
            categories.append(row)
        render_output(
            {
                "broker": broker,
                "role": BROKER_ROLES[broker].role if broker in BROKER_ROLES else "unknown",
                "description": BROKER_ROLES[broker].description if broker in BROKER_ROLES else None,
                "command_count": len(commands),
                "categories": categories,
            },
            force_json=force_json,
        )
        return True
    if len(positional) == 1:
        in_category = registry.list_commands(broker=broker, category=positional[0])
        info = category_info(positional[0])
        payload: dict[str, Any] = {"broker": broker, "category": positional[0]}
        if info is not None:
            payload["description"] = info.description
            payload["when_to_use"] = info.when_to_use
        payload["command_count"] = len(in_category)
        payload["commands"] = [
            {
                "name": command.name,
                "description": command.description,
                "required": _required_fields(command),
                "domains": list(command.domains),
                "tags": list(command.tags),
            }
            for command in in_category
        ]
        render_output(payload, force_json=force_json)
        return True
    return False


def _dry_run_payload(command: CommandSpec, params: dict[str, Any]) -> dict[str, Any]:
    return {
        "dry_run": True,
        "command": command.qualified_name,
        "path_segments": list(command.path_segments),
        "broker": command.broker,
        "broker_role": command.broker_role,
        "side_effect": command.side_effect,
        "params": params,
        "validation": "ok",
        "credentials": _credentials_status(command.broker),
        "kis_alternatives": list(command.kis_alternatives),
        "execute": " ".join(
            (
                "uv run",
                APP_NAME,
                *command.path_segments,
                "--params-json",
                "'" + json.dumps(params, ensure_ascii=False, separators=(",", ":")) + "'",
                "--json",
            )
        ),
    }


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
