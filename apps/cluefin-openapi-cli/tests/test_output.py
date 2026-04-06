from __future__ import annotations

from cluefin_openapi_cli.main import _command_summary
from cluefin_openapi_cli.output import dump_json, render_output, to_jsonable
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
