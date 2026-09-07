from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from typing import Any


def stdout_is_tty() -> bool:
    """Return True when stdout is attached to an interactive terminal."""

    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses and nested objects into JSON-safe structures."""

    if is_dataclass(value):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, set):
        return [to_jsonable(item) for item in sorted(value, key=str)]
    if hasattr(value, "model_dump"):
        return to_jsonable(value.model_dump())
    return value


def dump_json(payload: Any, *, compact: bool = False) -> str:
    """Serialize payload to a JSON string with stable formatting.

    ``compact`` emits one line with no insignificant whitespace — the cheapest form
    for an agent to read back into context.
    """

    data = to_jsonable(payload)
    if compact:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str)
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def _pick_path(item: Any, path: str) -> tuple[bool, Any]:
    current = item
    for segment in path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            return False, None
    return True, current


def _apply_mask(item: Any, fields: list[str]) -> Any:
    if not isinstance(item, dict):
        return item
    picked: dict[str, Any] = {}
    for field in fields:
        found, value = _pick_path(item, field)
        if found:
            picked[field] = value
    return picked


def select_fields(data: Any, fields: list[str]) -> Any:
    """Apply a field mask to a JSON-safe payload.

    Each field is a top-level key or a dotted path (``output.stck_prpr``). Dict
    payloads keep only the requested paths; list payloads mask each element; when a
    requested path points at a list of dicts, its elements are masked with the
    remaining fields under that prefix. Keys that don't exist are silently dropped,
    so a wrong field name never fails the call — check the returned keys.
    """

    if not fields:
        return data
    if isinstance(data, list):
        return [select_fields(item, fields) for item in data]
    if not isinstance(data, dict):
        return data

    result: dict[str, Any] = {}
    direct = [field for field in fields if "." not in field]
    nested = [field for field in fields if "." in field]

    for field in direct:
        if field in data:
            result[field] = data[field]

    by_prefix: dict[str, list[str]] = {}
    for field in nested:
        prefix, _, rest = field.partition(".")
        by_prefix.setdefault(prefix, []).append(rest)

    for prefix, sub_fields in by_prefix.items():
        if prefix not in data:
            continue
        value = data[prefix]
        if isinstance(value, list):
            result[prefix] = [_apply_mask(item, sub_fields) for item in value]
        elif isinstance(value, dict):
            result[prefix] = select_fields(value, sub_fields)
        else:
            result[prefix] = value

    return result


def render_output(
    payload: Any,
    *,
    force_json: bool = False,
    console: Any | None = None,
    compact: bool = False,
) -> None:
    """Render payload as JSON or as a compact human-readable view."""

    data = to_jsonable(payload)
    use_json = force_json or not stdout_is_tty()

    if use_json:
        text = dump_json(data, compact=compact)
    elif isinstance(data, dict):
        rows = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                rendered = json.dumps(value, ensure_ascii=False, default=str)
            else:
                rendered = str(value)
            rows.append(f"{key}: {rendered}")
        text = "\n".join(rows)
    else:
        text = dump_json(data)

    if console is not None and hasattr(console, "print"):
        console.print(text)
    else:
        sys.stdout.write(text)
        sys.stdout.write("\n")
