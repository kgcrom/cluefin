"""Local request validation and input hardening for agent-supplied parameters.

Agents hallucinate values. Everything here runs before any network call so a bad
input fails fast with a structured, field-addressed error instead of a broker
round-trip (which costs a token issue, a rate-limit slot, and an opaque message).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_FORBIDDEN_CHARS = {"%": "pre-URL-encoded text", "?": "embedded query string", "#": "URL fragment"}
_TRAVERSAL = re.compile(r"(^|[\\/])\.\.($|[\\/])")

# schema type -> (accepted types, rejected types, hint). `bool` is an `int` in Python, so
# the numeric rules reject it explicitly. Only the container rules carry a hint, and those
# deliberately leave `value` out of the issue payload.
_TYPE_RULES: dict[str, tuple[tuple[type, ...], tuple[type, ...], str | None]] = {
    "string": ((str,), (), None),
    "integer": ((int,), (bool,), None),
    "number": ((int, float), (bool,), None),
    "boolean": ((bool,), (), None),
    "array": ((list,), (), "Use --params-json for arrays."),
    "object": ((dict,), (), "Use --params-json for objects."),
}


@dataclass(slots=True)
class ValidationIssue:
    field: str
    problem: str
    value: Any = None
    allowed: list[Any] | None = None
    hint: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"field": self.field, "problem": self.problem}
        if self.value is not None:
            payload["value"] = self.value
        if self.allowed is not None:
            payload["allowed"] = self.allowed
        if self.hint:
            payload["hint"] = self.hint
        return payload


@dataclass(slots=True)
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)

    def to_list(self) -> list[dict[str, Any]]:
        return [issue.to_dict() for issue in self.issues]


def harden_string(path: str, value: str, report: ValidationReport) -> None:
    """Reject strings that only make sense as an injection or an encoding mistake."""

    if any(ord(char) < 0x20 for char in value):
        report.add(ValidationIssue(path, "contains control characters", hint="Pass plain text without escapes."))
        return
    if _TRAVERSAL.search(value):
        report.add(ValidationIssue(path, "looks like a path traversal", value=value))
        return
    for char, meaning in _FORBIDDEN_CHARS.items():
        if char in value:
            report.add(
                ValidationIssue(
                    path,
                    f"contains `{char}` ({meaning})",
                    value=value,
                    hint="Pass the raw value; the CLI encodes it for the broker.",
                )
            )
            return


def _walk_strings(path: str, value: Any, report: ValidationReport) -> None:
    if isinstance(value, str):
        harden_string(path, value, report)
    elif isinstance(value, dict):
        for key, item in value.items():
            _walk_strings(f"{path}.{key}" if path else str(key), item, report)
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _walk_strings(f"{path}[{index}]", item, report)


def _check_type(name: str, value: Any, schema_type: Any, report: ValidationReport) -> bool:
    """Report a JSON-Schema type mismatch. Returns True when the value is the wrong type.

    An unknown (or absent) type falls through to the enum/pattern/bounds rules, which is
    what the per-type `if` chain this replaces did.
    """
    rule = _TYPE_RULES.get(schema_type)
    if rule is None:
        return False
    allowed, rejected, hint = rule
    if isinstance(value, allowed) and not isinstance(value, rejected):
        return False
    # Only the container types carry a hint, and those omit `value` from the payload.
    report.add(
        ValidationIssue(
            name,
            f"expected {schema_type}, got {type(value).__name__}",
            value=None if hint else value,
            hint=hint,
        )
    )
    return True


def _check_scalar(name: str, value: Any, schema: dict[str, Any], report: ValidationReport) -> None:
    schema_type = schema.get("type")
    if _check_type(name, value, schema_type, report):
        return

    enum = schema.get("enum")
    if enum and value not in enum:
        report.add(ValidationIssue(name, "not one of the allowed values", value=value, allowed=list(enum)))
        return

    pattern = schema.get("pattern")
    if pattern and isinstance(value, str) and re.fullmatch(pattern, value) is None:
        report.add(
            ValidationIssue(
                name,
                f"does not match pattern {pattern}",
                value=value,
                hint=schema.get("description"),
            )
        )
        return

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and value < minimum:
            report.add(ValidationIssue(name, f"below minimum {minimum}", value=value))
        if maximum is not None and value > maximum:
            report.add(ValidationIssue(name, f"above maximum {maximum}", value=value))

    if isinstance(value, str):
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length is not None and len(value) < min_length:
            report.add(ValidationIssue(name, f"shorter than minLength {min_length}", value=value))
        if max_length is not None and len(value) > max_length:
            report.add(ValidationIssue(name, f"longer than maxLength {max_length}", value=value))


def validate_params(params: dict[str, Any], parameters_schema: dict[str, Any]) -> ValidationReport:
    """Validate merged params against the command's JSON Schema plus hardening rules.

    Checks required fields, unknown fields, scalar types, ``enum``, ``pattern``,
    numeric and length bounds, and rejects strings carrying control characters,
    traversal, or URL syntax anywhere in the payload (nested values included).
    """

    report = ValidationReport()
    properties: dict[str, Any] = parameters_schema.get("properties", {})
    required = list(parameters_schema.get("required", []))

    missing = [name for name in required if params.get(name) is None]
    for name in missing:
        report.add(ValidationIssue(name, "required", hint=properties.get(name, {}).get("description")))

    for name in params:
        if name not in properties:
            report.add(
                ValidationIssue(
                    name,
                    "unknown parameter",
                    allowed=sorted(properties),
                    hint="Run `schema <command>` to see accepted parameters.",
                )
            )

    for name, value in params.items():
        if value is None or name not in properties:
            continue
        _check_scalar(name, value, properties[name], report)

    _walk_strings("", params, report)
    return report
