from __future__ import annotations

import pytest

from cluefin_openapi_cli.main import (
    CliError,
    _coerce_value,
    _load_params_json,
    _merge_params,
    _render_leaf_help,
)
from cluefin_openapi_cli.registry import CommandSpec


def _spec(**overrides) -> CommandSpec:
    params = {
        "type": "object",
        "properties": {
            "qty": {"type": "integer", "description": "Quantity"},
            "label": {"type": "string", "description": "Label"},
        },
        "required": ["qty"],
    }
    base = dict(
        broker="kis",
        category="stock",
        name="demo",
        description="Demo command.",
        path_segments=("kis", "stock", "demo"),
        parameters=params,
    )
    base.update(overrides)
    return CommandSpec(**base)


@pytest.mark.parametrize(
    ("raw", "schema", "expected"),
    [
        ("42", {"type": "integer"}, 42),
        ("3.5", {"type": "number"}, 3.5),
        ("true", {"type": "boolean"}, True),
        ("off", {"type": "boolean"}, False),
        ("hello", {"type": "string"}, "hello"),
        ("plain", {}, "plain"),
    ],
)
def test_coerce_value_converts_by_schema_type(raw, schema, expected) -> None:
    assert _coerce_value(raw, schema) == expected


@pytest.mark.parametrize(
    ("raw", "schema"),
    [
        ("abc", {"type": "integer"}),
        ("abc", {"type": "number"}),
        ("maybe", {"type": "boolean"}),
    ],
)
def test_coerce_value_rejects_invalid_input(raw, schema) -> None:
    with pytest.raises(CliError):
        _coerce_value(raw, schema)


def test_load_params_json_handles_empty_valid_and_invalid() -> None:
    assert _load_params_json(None) == {}
    assert _load_params_json('{"a": 1}') == {"a": 1}
    with pytest.raises(CliError):
        _load_params_json("{not json}")
    with pytest.raises(CliError):
        _load_params_json("[1, 2, 3]")


def test_merge_params_coerces_and_passes_booleans() -> None:
    force_json, merged = _merge_params(_spec(), {"json": True, "qty": "7", "label": "x"})
    assert force_json is True
    assert merged == {"qty": 7, "label": "x"}


def test_merge_params_rejects_unknown_option() -> None:
    with pytest.raises(CliError):
        _merge_params(_spec(), {"bogus": "1"})


def test_merge_params_rejects_non_string_params_json() -> None:
    with pytest.raises(CliError):
        _merge_params(_spec(), {"params_json": 123})


def test_merge_params_reports_missing_required() -> None:
    with pytest.raises(CliError):
        _merge_params(_spec(), {"label": "only"})


def test_merge_params_help_renders_and_returns_empty(capsys) -> None:
    force_json, merged = _merge_params(_spec(), {"help": True, "qty": "1"})
    assert merged == {}
    assert force_json is False
    assert capsys.readouterr().out  # leaf help was rendered


def test_render_leaf_help_lists_options(capsys) -> None:
    _render_leaf_help(_spec(), force_json=True)
    out = capsys.readouterr().out
    assert "--qty" in out
    assert "--label" in out
