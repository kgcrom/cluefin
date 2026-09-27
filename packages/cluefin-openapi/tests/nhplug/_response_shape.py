"""Exact response-key and spec-length checks for NH PLUG integration tests.

`rsp_cd` + one-field checks pass even when a response model is wrong: every NH PLUG model is
`extra="allow"`, so a field the server sends but the model doesn't declare is kept silently in
`model_extra`, and a misnamed block parses as `None`. This compares the server's raw keys against
the model instead — same rules as `tests/kis/_response_shape.py`, plus two NH PLUG specifics:

- `Output_N` blocks and `message` are sent **only when there is data** (spec + live), so a
  top-level block the server omits is not a problem. A misnamed block still fails as `extra`.
- Lengths are checked against `spec_lengths.json`, a snapshot of the spec's `길이 N` values.
  Response models never get length constraints (AGENTS.md); an over-length value fails the
  *test* until it is recorded in `VENDOR_DOC_ERRATA.md` and `known_exceed`.

The raw exchange comes from the `client` fixture, which wraps `HttpClient.post` and keeps the
last request body and parsed response on `client.last_exchange`. Bodies carry account numbers
on inquiry APIs — failure messages print field names and lengths, never values.
"""

import json
import pathlib
import types
import typing
from collections.abc import Iterable, Sequence
from typing import Any

from pydantic import AliasChoices, BaseModel
from pydantic.fields import FieldInfo

from cluefin_openapi.nhplug._model import NHPlugHttpResponse

_SPEC = json.loads((pathlib.Path(__file__).parent / "spec_lengths.json").read_text(encoding="utf-8"))
SPEC_LENGTHS: dict[str, dict[str, dict[str, str]]] = _SPEC["lengths"]
KNOWN_EXCEED: dict[str, dict[str, str]] = _SPEC["known_exceed"]

_OPTIONAL_TOP = ("Output_", "message")


def _wire_names(name: str, field: FieldInfo) -> tuple[str, ...]:
    alias = field.validation_alias
    if isinstance(alias, AliasChoices):
        return tuple(c for c in alias.choices if isinstance(c, str))
    if isinstance(alias, str):
        return (alias,)
    return (field.alias or name,)


def _candidates(annotation: Any) -> list[tuple[str, type[BaseModel] | None]]:
    """Every (kind, nested model) an annotation accepts; kind is "object" | "array" | "scalar"."""
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        out = []
        for arg in typing.get_args(annotation):
            if arg is not type(None):
                out.extend(_candidates(arg))
        return out
    if origin in (list, Sequence):
        return [("array", model) for _, model in _candidates(typing.get_args(annotation)[0])]
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return [("object", annotation)]
    return [("scalar", None)]


_KINDS = {list: "array", dict: "object"}


def response_shape_diff(raw: dict[str, Any], model: type[BaseModel], path: str = "") -> list[str]:
    """Describe every difference between raw response keys and ``model``; empty means exact match.

    Array blocks are compared over the union of all rows' keys. A field typed as a union of an
    object and an array (the spec and server disagree on some blocks) is matched by the kind the
    server actually sent.
    """
    problems: list[str] = []
    claimed: set[str] = set()

    for name, field in model.model_fields.items():
        names = _wire_names(name, field)
        claimed.update(names)
        present = next((n for n in names if n in raw), None)
        label = f"{path}{names[0]}"
        if present is None:
            if not (path == "" and names[0].startswith(_OPTIONAL_TOP)):
                problems.append(f"missing: {label} (model declares it, server did not send it)")
            continue

        value = raw[present]
        cands = [(k, m) for k, m in _candidates(field.annotation) if m is not None]
        if not cands or value is None:
            continue
        actual = _KINDS.get(type(value), "scalar")
        nested = next((m for k, m in cands if k == actual), None)
        if nested is None:
            expected = "/".join(sorted({k for k, _ in cands}))
            problems.append(f"kind: {label} is {actual} on the server, model expects {expected}")
            continue
        rows = value if actual == "array" else [value]
        keys = {key: None for row in rows if isinstance(row, dict) for key in row}
        if keys:  # 빈 배열·빈 객체는 키를 판정할 수 없다
            problems.extend(response_shape_diff(keys, nested, f"{label}."))

    for key in sorted(set(raw) - claimed):
        problems.append(f"extra: {path}{key} (server sent it, model does not declare it)")
    return problems


def value_length(value: Any, spec: str) -> str | None:
    """Return a description of how ``value`` exceeds ``spec`` ("N" or "N.M"), or None if it fits.

    Numbers: the sign is not counted; "N.M" allows N-M integer digits and M fraction digits.
    Strings: CP949 byte length — the spec's lengths come from fixed-width CP949 records
    (same encoding as the `.mst` instrument files), so a Korean character counts as 2. Counted as
    "non-ASCII = 2", which equals CP949 for every encodable character and matches the TS helper
    (Node has no CP949 encoder) for the rest — e.g. the U+FFFD garbage some fields carry.
    """
    if value is None or value == "" or isinstance(value, bool):
        return None
    if "." in spec:
        total, frac = (int(x) for x in spec.split("."))
        text = str(value).lstrip("+-")
        whole, _, fraction = text.partition(".")
        whole = whole.lstrip("0") or "0"
        if len(whole) > total - frac or len(fraction) > frac:
            return f"{len(whole)}.{len(fraction)}"  # nosemgrep
        return None
    if isinstance(value, (int, float)):
        text = str(value).lstrip("+-")
        if isinstance(value, float) and text.endswith(".0"):
            text = text[:-2]
        size = len(text.replace(".", ""))
    else:
        size = sum(2 if ord(ch) > 0x7F else 1 for ch in str(value))
    return str(size) if size > int(spec) else None


def _size(length: str) -> tuple[int, ...]:
    return tuple(int(x) for x in length.split("."))


def length_violations(api_path: str, request: dict[str, Any], raw: dict[str, Any]) -> list[str]:
    """Every request/response value longer than the spec says, minus ``known_exceed``."""
    spec = SPEC_LENGTHS.get(api_path)
    if spec is None:
        return []
    known = KNOWN_EXCEED.get(api_path, {})
    problems: list[str] = []
    for field, length in spec["req"].items():
        over = value_length(request.get(field), length)
        if over and f"req.{field}" not in known:
            problems.append(f"length: request {field} is {over}, spec says {length}")
    worst: dict[str, str] = {}
    for key, length in spec["res"].items():
        block, _, field = key.partition(".")
        value = raw.get(block)
        rows = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
        for row in rows:  # 배열은 전 행을 본다 — 첫 행만 보면 긴 값을 놓친다
            over = value_length(row.get(field), length) if isinstance(row, dict) else None
            if over and key not in known and (key not in worst or _size(over) > _size(worst[key])):
                worst[key] = over
    problems.extend(f"length: {key} is up to {over}, spec says {spec['res'][key]}" for key, over in worst.items())
    return problems


def assert_matches_spec(
    client: Any,
    response: NHPlugHttpResponse,
    *,
    ignore: Iterable[str] = (),
) -> None:
    """Fail unless the last exchange matches ``response.body``'s model exactly and fits the spec lengths.

    ``ignore`` takes dotted wire paths (``"Output_0.iem_nm"``) for key divergences already measured
    and recorded in the errata — justify each one at the call site. Length exceptions go in
    ``spec_lengths.json`` ``known_exceed`` instead, so the TS suite shares them.
    """
    exchange = getattr(client, "last_exchange", None)
    if not exchange or not isinstance(exchange.get("response"), dict):
        raise AssertionError("no captured NH PLUG exchange; use the integration `client` fixture")
    raw = exchange["response"]
    ignored = set(ignore)
    problems = [p for p in response_shape_diff(raw, type(response.body)) if p.split(" ", 2)[1] not in ignored]
    problems += length_violations(exchange["path"], exchange["request"], raw)
    assert not problems, f"{type(response.body).__name__} does not match the spec/server:\n" + "\n".join(
        f"  - {p}" for p in problems
    )
