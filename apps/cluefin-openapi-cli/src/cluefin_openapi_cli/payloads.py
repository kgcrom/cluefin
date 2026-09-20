"""JSON payload builders for the meta commands.

Every meta command answers with a dict that agents parse, so the shapes live together
here and `main` stays the dispatcher. Nothing in this module parses argv or talks to a
broker: callers hand in already-parsed values.
"""

from __future__ import annotations

import json
from typing import Any

from cluefin_openapi_cli.metadata import (
    BROKER_ORDER,
    BROKER_ROLES,
    broker_rank,
    build_taxonomy_entry,
    category_info,
)
from cluefin_openapi_cli.output import render_output, to_jsonable
from cluefin_openapi_cli.registry import CommandSpec, get_registry
from cluefin_openapi_cli.search import search_commands

APP_NAME = "cluefin-openapi-cli"

#: An unfiltered `list --full` is the whole catalog; cap it rather than refuse it.
_UNFILTERED_FULL_LIMIT = 25

_SEARCH_DEFAULT_LIMIT = 8
_SEARCH_MAX_LIMIT = 50


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


def _broker_role_fields(broker: str) -> dict[str, Any]:
    """`role`/`description` for a broker, in the order the help payload prints them."""
    role = BROKER_ROLES.get(broker)
    return {
        "role": role.role if role is not None else "unknown",
        "description": role.description if role is not None else None,
    }


def _category_fields(name: str) -> dict[str, Any]:
    """`description`/`when_to_use` for a category, or nothing when it is not authored."""
    info = category_info(name)
    if info is None:
        return {}
    return {"description": info.description, "when_to_use": info.when_to_use}


def _help_command_row(command: CommandSpec) -> dict[str, Any]:
    return {
        "name": command.name,
        "description": command.description,
        "required": _required_fields(command),
        "domains": list(command.domains),
        "tags": list(command.tags),
    }


def _render_broker_help(broker: str, positional: list[str], *, force_json: bool) -> bool:
    registry = get_registry()
    if broker == "dart":
        if positional:
            return False
        commands = registry.list_commands(broker=broker)
        render_output(
            {
                "broker": broker,
                **_broker_role_fields(broker),
                "command_count": len(commands),
                "commands": [_help_command_row(command) for command in commands],
            },
            force_json=force_json,
        )
        return True

    if not positional:
        commands = registry.list_commands(broker=broker)
        categories = []
        for name in sorted({command.category for command in commands}):
            in_category = [command for command in commands if command.category == name]
            row: dict[str, Any] = {"name": name, "command_count": len(in_category)}
            row.update(_category_fields(name))
            # Union over the real commands, so this reflects the authored taxonomy.
            row["domains"] = sorted({d for command in in_category for d in command.domains})
            row["tags"] = sorted({t for command in in_category for t in command.tags})
            row["list_command"] = f"uv run {APP_NAME} list --broker {broker} --category {name} --json"
            categories.append(row)
        render_output(
            {
                "broker": broker,
                **_broker_role_fields(broker),
                "command_count": len(commands),
                "categories": categories,
            },
            force_json=force_json,
        )
        return True
    if len(positional) == 1:
        in_category = registry.list_commands(broker=broker, category=positional[0])
        payload: dict[str, Any] = {"broker": broker, "category": positional[0]}
        payload.update(_category_fields(positional[0]))
        payload["command_count"] = len(in_category)
        payload["commands"] = [_help_command_row(command) for command in in_category]
        render_output(payload, force_json=force_json)
        return True
    return False
