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
    return value


def dump_json(payload: Any) -> str:
    """Serialize payload to a JSON string with stable formatting."""

    return json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2, default=str)


def render_output(payload: Any, *, force_json: bool = False) -> None:
    """Render payload as JSON or as a compact human-readable view."""

    data = to_jsonable(payload)
    use_json = force_json or not stdout_is_tty()

    if use_json:
        text = dump_json(data)
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

    sys.stdout.write(text)
    sys.stdout.write("\n")
