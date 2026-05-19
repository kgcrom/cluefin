"""Structured output helpers for cluefin-cli."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any


def to_jsonable(value: Any) -> Any:
    """Convert common project objects into JSON-safe structures."""
    if is_dataclass(value):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if hasattr(value, "model_dump"):
        return to_jsonable(value.model_dump())
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, set):
        return [to_jsonable(item) for item in sorted(value, key=str)]
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def success_envelope(
    *,
    command: str,
    data: Any,
    source: str | None = None,
    params: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a stable success envelope for agent-facing JSON output."""
    return {
        "ok": True,
        "command": command,
        "source": source,
        "params": params or {},
        "data": data,
        "warnings": warnings or [],
        "meta": meta or {},
    }


def error_envelope(
    *,
    command: str,
    error_type: str,
    message: str,
    warnings: list[str] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a stable error envelope for agent-facing JSON output."""
    return {
        "ok": False,
        "command": command,
        "error": {
            "type": error_type,
            "message": message,
        },
        "warnings": warnings or [],
        "meta": meta or {},
    }


def dump_json(payload: Any) -> str:
    """Serialize payload with stable formatting."""
    return json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2, default=str)


def write_json(payload: Any) -> None:
    """Write JSON payload to stdout."""
    sys.stdout.write(dump_json(payload))
    sys.stdout.write("\n")
