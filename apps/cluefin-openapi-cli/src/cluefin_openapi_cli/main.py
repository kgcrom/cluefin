from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Any

from cluefin_openapi_cli.output import render_output, stdout_is_tty, to_jsonable
from cluefin_openapi_cli.registry import CommandSpec, get_registry


@dataclass(slots=True)
class CLIResult:
    exit_code: int
    stdout: str
    stderr: str


class CliError(Exception):
    def __init__(self, message: str, *, exit_code: int = 1, data: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.data = data or {}


def _command_summary(command: CommandSpec) -> dict[str, Any]:
    return {
        "broker": command.broker,
        "category": command.category,
        "name": command.name,
        "qualified_name": command.qualified_name,
        "path_segments": list(command.path_segments),
        "description": command.description,
        "parameters": command.parameters,
        "returns": command.returns,
        "has_executor": command.executor is not None,
    }


def _json_requested(argv: list[str]) -> bool:
    return "--json" in argv or not stdout_is_tty()


def _write_stderr(message: str) -> None:
    sys.stderr.write(message)
    sys.stderr.write("\n")


def _emit_error(exc: CliError, *, force_json: bool) -> None:
    if force_json:
        render_output(
            {
                "error": {
                    "type": type(exc).__name__,
                    "message": exc.message,
                    "data": to_jsonable(exc.data),
                }
            },
            force_json=True,
        )
        return

    _write_stderr(exc.message)


def _list_payload(broker: str | None = None, category: str | None = None) -> dict[str, Any]:
    registry = get_registry()
    commands = registry.list_commands(broker=broker, category=category)
    return {
        "broker": broker,
        "category": category,
        "count": len(commands),
        "commands": [to_jsonable(_command_summary(command)) for command in commands],
    }


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

        if token in {"--json", "--help"}:
            options[token[2:].replace("-", "_")] = True
            index += 1
            continue

        if index + 1 >= len(argv):
            raise CliError(f"Option `{token}` requires a value.", exit_code=2)

        options[token[2:].replace("-", "_")] = argv[index + 1]
        index += 2

    return positional, options


def _load_params_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CliError("`--params-json` must be valid JSON.", exit_code=2) from exc

    if not isinstance(payload, dict):
        raise CliError("`--params-json` must decode to an object.", exit_code=2)

    return payload


def _coerce_value(raw_value: str, schema: dict[str, Any]) -> Any:
    schema_type = schema.get("type", "string")
    if schema_type == "integer":
        try:
            return int(raw_value)
        except ValueError as exc:
            raise CliError(f"Invalid integer value `{raw_value}`.", exit_code=2) from exc
    if schema_type == "number":
        try:
            return float(raw_value)
        except ValueError as exc:
            raise CliError(f"Invalid number value `{raw_value}`.", exit_code=2) from exc
    if schema_type == "boolean":
        lowered = raw_value.lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
        raise CliError(f"Invalid boolean value `{raw_value}`.", exit_code=2)
    return raw_value


def _render_leaf_help(command: CommandSpec, *, force_json: bool) -> None:
    properties = command.parameters.get("properties", {})
    options = []
    for field_name, schema in properties.items():
        options.append(
            {
                "name": f"--{field_name.replace('_', '-')}",
                "type": schema.get("type", "string"),
                "description": schema.get("description"),
                "required": field_name in set(command.parameters.get("required", [])),
            }
        )

    render_output(
        {
            "command": _command_summary(command),
            "options": options,
            "supports_params_json": True,
        },
        force_json=force_json,
    )


def _merge_params(command: CommandSpec, options: dict[str, str | bool]) -> tuple[bool, dict[str, Any]]:
    force_json = bool(options.pop("json", False))
    help_requested = bool(options.pop("help", False))
    params_json = options.pop("params_json", None)
    if params_json is not None and not isinstance(params_json, str):
        raise CliError("`--params-json` requires a string value.", exit_code=2)

    merged = _load_params_json(params_json if isinstance(params_json, str) else None)
    properties = command.parameters.get("properties", {})

    for field_name, raw_value in options.items():
        if field_name not in properties:
            raise CliError(
                f"Unknown option `--{field_name.replace('_', '-')}` for `{command.qualified_name}`.",
                exit_code=2,
            )
        if isinstance(raw_value, bool):
            merged[field_name] = raw_value
        else:
            merged[field_name] = _coerce_value(raw_value, properties[field_name])

    required = set(command.parameters.get("required", []))
    missing = [key for key in required if merged.get(key) is None]
    if missing:
        raise CliError("Missing required parameters.", exit_code=2, data={"missing": missing})

    if help_requested:
        _render_leaf_help(command, force_json=force_json)
        return force_json, {}

    return force_json, merged


def _run_root(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    force_json = bool(options.get("json", False))
    registry = get_registry()
    payload = {
        "app": "cluefin-openapi-cli",
        "interactive": stdout_is_tty(),
        "brokers": list(registry.iter_brokers()),
        "commands": ["list", "describe"],
    }
    if bool(options.get("help", False)):
        payload["usage"] = [
            "cluefin-openapi-cli list [--broker BROKER] [--category CATEGORY] [--json]",
            "cluefin-openapi-cli describe <broker> <category> <name> [--json]",
            "cluefin-openapi-cli describe dart <name> [--json]",
            "cluefin-openapi-cli <broker> <category> <name> [--params-json JSON] [schema options] [--json]",
            "cluefin-openapi-cli dart <name> [--params-json JSON] [schema options] [--json]",
        ]
    render_output(payload, force_json=force_json)


def _run_list(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    if positional:
        raise CliError("`list` does not accept positional arguments.", exit_code=2)

    broker = options.get("broker")
    category = options.get("category")
    force_json = bool(options.get("json", False))
    render_output(
        _list_payload(
            broker=broker if isinstance(broker, str) else None,
            category=category if isinstance(category, str) else None,
        ),
        force_json=force_json,
    )


def _run_describe(argv: list[str]) -> None:
    positional, options = _parse_named_options(argv)
    force_json = bool(options.get("json", False))

    if not positional:
        raise CliError("Usage: describe <broker> <category> <name> (or `describe dart <name>`).", exit_code=2)

    broker = positional[0]
    path_parts = positional[1:]
    if broker == "dart" and len(path_parts) == 1:
        path = (broker, path_parts[0])
    elif len(path_parts) == 2:
        path = (broker, path_parts[0], path_parts[1])
    else:
        raise CliError("Usage: describe <broker> <category> <name> (or `describe dart <name>`).", exit_code=2)

    registry = get_registry()
    command = registry.resolve_command(path)
    if command is None:
        raise CliError(f"Unknown command path: {' '.join(path)}", exit_code=2)

    render_output({"command": _command_summary(command)}, force_json=force_json)


def _run_dynamic(argv: list[str]) -> None:
    if not argv:
        _run_root([])
        return

    registry = get_registry()
    broker = argv[0]
    if broker not in set(registry.iter_brokers()):
        raise CliError(f"Unknown top-level command `{broker}`.", exit_code=2)

    positional, options = _parse_named_options(argv[1:])
    help_requested = bool(options.get("help", False))

    if broker == "dart":
        if help_requested and not positional:
            render_output(
                {
                    "broker": broker,
                    "commands": [command.name for command in registry.list_commands(broker=broker)],
                },
                force_json=bool(options.get("json", False)),
            )
            return
        if len(positional) < 1:
            raise CliError("Usage: cluefin-openapi-cli dart <name> [options]", exit_code=2)
        path = (broker, positional[0])
    else:
        if help_requested and not positional:
            render_output(
                {
                    "broker": broker,
                    "categories": sorted({command.category for command in registry.list_commands(broker=broker)}),
                },
                force_json=bool(options.get("json", False)),
            )
            return
        if help_requested and len(positional) == 1:
            render_output(
                {
                    "broker": broker,
                    "category": positional[0],
                    "commands": [
                        command.name for command in registry.list_commands(broker=broker, category=positional[0])
                    ],
                },
                force_json=bool(options.get("json", False)),
            )
            return
        if len(positional) < 2:
            raise CliError(f"Usage: cluefin-openapi-cli {broker} <category> <name> [options]", exit_code=2)
        path = (broker, positional[0], positional[1])

    command = registry.resolve_command(path)
    if command is None:
        raise CliError(f"Unknown command path: {' '.join(path)}", exit_code=2)

    if help_requested:
        _render_leaf_help(command, force_json=bool(options.get("json", False)))
        return

    force_json, params = _merge_params(command, options)
    try:
        result = registry.invoke_command(command, params)
    except Exception as exc:
        raise CliError(
            f"Command `{command.qualified_name}` failed: {exc}",
            data={"command": command.qualified_name},
        ) from exc
    render_output(result, force_json=force_json)


def dispatch(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"--help", "-h"}:
        _run_root(args)
        return

    command = args[0]
    if command == "list":
        _run_list(args[1:])
        return
    if command == "describe":
        _run_describe(args[1:])
        return

    _run_dynamic(args)


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        dispatch(args)
    except CliError as exc:
        _emit_error(exc, force_json=_json_requested(args))
        raise SystemExit(exc.exit_code) from exc


def run_cli(argv: list[str] | None = None) -> CLIResult:
    stdout = io.StringIO()
    stderr = io.StringIO()
    old_argv = sys.argv[:]
    sys.argv = [old_argv[0] if old_argv else "cluefin-openapi-cli", *(argv or [])]

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
