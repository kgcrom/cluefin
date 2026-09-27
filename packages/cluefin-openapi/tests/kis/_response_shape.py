"""Exact response-key check for KIS integration tests.

`isinstance`/`hasattr` checks pass even when a response model is wrong: pydantic drops
keys the model doesn't declare and fills defaults for keys the server never sent, so a
misnamed block (`output` vs `output1`) silently parses as an empty list. This compares
the server's raw keys against the model instead — the TS suite's `assertResponseShape`
does the same.

The raw body comes from the debug artifact `HttpClient` writes for every response
(`last_response_debug["artifact_path"]`); the in-memory preview is truncated.
Artifacts contain unredacted bodies (account numbers on account TRs) — never print them.
"""

import json
import types
import typing
from collections.abc import Iterable, Sequence
from typing import Any

from pydantic import AliasChoices, BaseModel
from pydantic.fields import FieldInfo

from cluefin_openapi.kis._http_client import HttpClient
from cluefin_openapi.kis._model import KisHttpResponse


def _wire_names(name: str, field: FieldInfo) -> tuple[str, ...]:
    alias = field.validation_alias
    if isinstance(alias, AliasChoices):
        return tuple(c for c in alias.choices if isinstance(c, str))
    if isinstance(alias, str):
        return (alias,)
    return (field.alias or name,)


def _unwrap(annotation: Any) -> tuple[str, type[BaseModel] | None]:
    """Return ("object" | "array" | "scalar", nested model) for a field annotation."""
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return _unwrap(args[0])
        return "scalar", None
    if origin in (list, Sequence):
        _, item = _unwrap(typing.get_args(annotation)[0])
        return "array", item
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return "object", annotation
    return "scalar", None


def _raw_kind(value: Any) -> str:
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "scalar"


def _merge_rows(value: Any) -> dict[str, Any]:
    """An object as-is, or an array's rows merged into one (rows can omit keys).

    The first non-empty value per key is kept so blocks nested inside rows can be checked too.
    """
    rows = value if isinstance(value, list) else [value]
    merged: dict[str, Any] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key, item in row.items():
            if merged.get(key) in (None, "", [], {}):
                merged[key] = item
    return merged


def response_shape_diff(raw: dict[str, Any], model: type[BaseModel], path: str = "") -> list[str]:
    """Describe every difference between raw response keys and ``model``; empty means exact match."""
    problems: list[str] = []
    raw_keys = set(raw)
    claimed: set[str] = set()

    for name, field in model.model_fields.items():
        names = _wire_names(name, field)
        claimed.update(names)
        present = next((n for n in names if n in raw_keys), None)
        label = f"{path}{names[0]}"
        if present is None:
            problems.append(f"missing: {label} (model declares it, server did not send it)")
            continue

        kind, nested = _unwrap(field.annotation)
        value = raw[present]
        if nested is None:
            continue
        if _raw_kind(value) != kind:
            problems.append(f"kind: {label} is {_raw_kind(value)} on the server, model expects {kind}")
            continue
        merged = _merge_rows(value)
        if not merged:
            continue  # 빈 배열·빈 객체는 키를 판정할 수 없다
        problems.extend(response_shape_diff(merged, nested, f"{label}."))

    for key in sorted(raw_keys - claimed):
        problems.append(f"extra: {path}{key} (server sent it, model does not declare it)")
    return problems


def _load_raw_body(client: HttpClient) -> dict[str, Any]:
    debug = client.last_response_debug or {}
    artifact_path = debug.get("artifact_path")
    if not artifact_path:
        raise AssertionError("no KIS debug artifact for the last response; cannot compare raw keys")
    with open(artifact_path, encoding="utf-8") as f:
        body = json.load(f)["response"]["body"]
    if not isinstance(body, dict):
        raise AssertionError(f"last KIS response body is not a JSON object: {type(body).__name__}")
    return body


def assert_response_shape(
    client: HttpClient,
    response: KisHttpResponse,
    *,
    ignore: Iterable[str] = (),
) -> None:
    """Fail unless the last raw response's keys match ``response.body``'s model exactly.

    ``ignore`` takes dotted wire paths (``"output.acml_vol"``) for divergences already
    measured and recorded in the errata — keep each one justified at the call site.
    """
    raw = _load_raw_body(client)
    ignored = set(ignore)
    problems = [p for p in response_shape_diff(raw, type(response.body)) if p.split(" ", 2)[1] not in ignored]
    assert not problems, f"{type(response.body).__name__} does not match the server response:\n" + "\n".join(
        f"  - {p}" for p in problems
    )
