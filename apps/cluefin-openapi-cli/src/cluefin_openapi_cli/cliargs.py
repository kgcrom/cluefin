"""argv parsing: named options, value coercion, and the schema-flag merge.

Everything here runs before a client exists, so a bad invocation costs an exit code and
nothing else. Failures raise `CliError` with EXIT_USAGE.
"""

from __future__ import annotations

import json
from typing import Any

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.payloads import _render_leaf_help
from cluefin_openapi_cli.registry import CommandSpec

#: Options that are flags, not values: `--json`, not `--json true`.
_BOOL_FLAGS = {"json", "help", "dry_run", "full", "compact", "explain"}


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


def _str_option(options: dict[str, str | bool], key: str) -> str | None:
    value = options.get(key)
    return value if isinstance(value, str) else None
