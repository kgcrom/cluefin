"""JSON-RPC 2.0 protocol helpers.

Handles serialization, deserialization, and validation of JSON-RPC messages.
All output goes to stdout as newline-delimited JSON.
"""

from __future__ import annotations

import json
import sys
from typing import Any

# Standard JSON-RPC 2.0 error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603

# Custom error codes
AUTH_ERROR = -32001
RATE_LIMIT_ERROR = -32002
BROKER_API_ERROR = -32003
SESSION_ERROR = -32004


def write_response(payload: dict) -> None:
    """Write a JSON-RPC response to stdout."""
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def write_error(
    request_id: int | str | None,
    code: int,
    message: str,
    data: Any = None,
) -> None:
    """Write a JSON-RPC error response to stdout."""
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    payload = {"jsonrpc": "2.0", "id": request_id, "error": error}
    write_response(payload)


def parse_request(line: str) -> dict:
    """Parse and validate a JSON-RPC 2.0 request.

    Raises:
        ValueError: If the line is not valid JSON or not a valid JSON-RPC 2.0 request.
    """
    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("Request must be a JSON object")

    if data.get("jsonrpc") != "2.0":
        raise ValueError("Missing or invalid 'jsonrpc' field (must be '2.0')")

    if "method" not in data:
        raise ValueError("Missing 'method' field")

    if not isinstance(data["method"], str):
        raise ValueError("'method' must be a string")

    params = data.get("params")
    if params is not None and not isinstance(params, (dict, list)):
        raise ValueError("'params' must be an object or array")

    return data
