from __future__ import annotations

import pytest

from cluefin_ta_cli.main import (
    CliError,
    _coerce_value,
    _emit_error,
    _load_params_json,
    _merge_params,
    _render_leaf_help,
    _write_stderr,
)
from cluefin_ta_cli.registry import CommandSpec


def _spec(**overrides) -> CommandSpec:
    params = {
        "type": "object",
        "properties": {
            "timeperiod": {"type": "integer", "description": "Window"},
            "label": {"type": "string", "description": "Label"},
        },
        "required": ["timeperiod"],
    }
    base = dict(
        category="ta",
        name="demo",
        description="Demo indicator.",
        path_segments=("ta", "demo"),
        parameters=params,
    )
    base.update(overrides)
    return CommandSpec(**base)


@pytest.mark.parametrize(
    ("raw", "schema", "expected"),
    [
        ("42", {"type": "integer"}, 42),
        ("3.5", {"type": "number"}, 3.5),
        ("yes", {"type": "boolean"}, True),
        ("no", {"type": "boolean"}, False),
        ("text", {"type": "string"}, "text"),
    ],
)
def test_coerce_value_converts_by_schema_type(raw, schema, expected) -> None:
    assert _coerce_value(raw, schema) == expected


@pytest.mark.parametrize(
    ("raw", "schema"),
    [("x", {"type": "integer"}), ("x", {"type": "number"}), ("x", {"type": "boolean"})],
)
def test_coerce_value_rejects_invalid(raw, schema) -> None:
    with pytest.raises(CliError):
        _coerce_value(raw, schema)


def test_load_params_json_variants() -> None:
    assert _load_params_json(None) == {}
    assert _load_params_json('{"a": 1}') == {"a": 1}
    with pytest.raises(CliError):
        _load_params_json("{bad}")
    with pytest.raises(CliError):
        _load_params_json("[1]")


def test_merge_params_coerces_values() -> None:
    force_json, merged = _merge_params(_spec(), {"json": True, "timeperiod": "9", "label": "x"})
    assert force_json is True
    assert merged == {"timeperiod": 9, "label": "x"}


def test_merge_params_rejects_unknown_option() -> None:
    with pytest.raises(CliError):
        _merge_params(_spec(), {"bogus": "1"})


def test_merge_params_reports_missing_required() -> None:
    with pytest.raises(CliError):
        _merge_params(_spec(), {"label": "x"})


def test_merge_params_help_renders_and_returns_empty(capsys) -> None:
    _, merged = _merge_params(_spec(), {"help": True, "timeperiod": "1"})
    assert merged == {}
    assert capsys.readouterr().out


def test_render_leaf_help_lists_options(capsys) -> None:
    _render_leaf_help(_spec(), force_json=True)
    out = capsys.readouterr().out
    assert "--timeperiod" in out


def test_emit_error_human_readable_writes_stderr(capsys) -> None:
    _emit_error(CliError("boom", exit_code=2), force_json=False)
    err = capsys.readouterr().err
    assert "boom" in err


def test_emit_error_json_mode(capsys) -> None:
    _emit_error(CliError("kaboom", data={"k": "v"}), force_json=True)
    out = capsys.readouterr().out
    assert '"kaboom"' in out


def test_write_stderr_appends_newline(capsys) -> None:
    _write_stderr("hello")
    assert capsys.readouterr().err == "hello\n"
