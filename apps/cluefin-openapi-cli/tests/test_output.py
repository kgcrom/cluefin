from __future__ import annotations

from cluefin_openapi_cli.output import dump_json, render_output, to_jsonable
from cluefin_openapi_cli.payloads import _command_summary
from cluefin_openapi_cli.registry import CommandSpec


def test_to_jsonable_handles_dataclass() -> None:
    spec = CommandSpec(
        broker="dart",
        category="dart",
        name="company-overview",
        description="Company overview",
        path_segments=("dart", "company-overview"),
    )

    data = to_jsonable(_command_summary(spec))

    assert data["broker"] == "dart"
    assert data["qualified_name"] == "dart.company-overview"


def test_render_output_pretty_mode(monkeypatch, capsys) -> None:
    monkeypatch.setattr("cluefin_openapi_cli.output.stdout_is_tty", lambda: True)

    render_output({"app": "cluefin-openapi-cli", "count": 2})

    captured = capsys.readouterr()
    assert "app: cluefin-openapi-cli" in captured.out
    assert "count: 2" in captured.out
    assert captured.err == ""


def test_dump_json_is_stable() -> None:
    assert dump_json({"a": 1}) == '{\n  "a": 1\n}'


def test_limit_rows_truncates_nested_lists_and_reports_totals() -> None:
    from cluefin_openapi_cli.output import limit_rows

    data = {"output2": [{"a": i} for i in range(300)], "meta": {"ok": True}}
    trimmed, notes = limit_rows(data, 20)

    assert len(trimmed["output2"]) == 20
    assert trimmed["meta"] == {"ok": True}
    assert notes == [{"path": "output2", "returned": 20, "total": 300}]


def test_limit_rows_is_a_no_op_when_nothing_exceeds_the_limit() -> None:
    from cluefin_openapi_cli.output import limit_rows

    data = {"rows": [1, 2, 3]}
    trimmed, notes = limit_rows(data, 20)

    assert trimmed == data
    assert notes == []


def test_limit_zero_means_no_limit() -> None:
    from cluefin_openapi_cli.output import limit_rows

    data = {"rows": list(range(100))}
    trimmed, notes = limit_rows(data, 0)

    assert trimmed == data
    assert notes == []


def test_top_level_list_is_wrapped_only_when_truncated() -> None:
    from cluefin_openapi_cli.output import attach_truncation, limit_rows

    rows = [{"a": i} for i in range(50)]
    trimmed, notes = limit_rows(rows, 10)
    wrapped = attach_truncation(trimmed, 10, notes)

    assert wrapped["_truncated"]["paths"][0]["total"] == 50
    assert len(wrapped["items"]) == 10

    untouched, no_notes = limit_rows(rows, 0)
    assert attach_truncation(untouched, 0, no_notes) == rows


def test_field_mask_is_applied_before_the_row_limit() -> None:
    from cluefin_openapi_cli.output import limit_rows, select_fields

    data = {"output2": [{"keep": i, "drop": "x" * 50} for i in range(30)]}
    masked = select_fields(data, ["output2.keep"])
    trimmed, notes = limit_rows(masked, 5)

    assert trimmed["output2"] == [{"keep": i} for i in range(5)]
    assert notes[0]["total"] == 30
