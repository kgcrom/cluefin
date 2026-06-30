from __future__ import annotations

from dataclasses import dataclass

from cluefin_ta_cli.output import dump_json, render_output, stdout_is_tty, to_jsonable


@dataclass
class _Sample:
    name: str
    values: list[int]


def test_to_jsonable_handles_dataclass_dict_set_and_tuple() -> None:
    payload = {
        "spec": _Sample(name="sma", values=[1, 2]),
        "pair": (1, 2),
        "labels": {"b", "a"},
    }
    result = to_jsonable(payload)
    assert result["spec"] == {"name": "sma", "values": [1, 2]}
    assert result["pair"] == [1, 2]
    assert result["labels"] == ["a", "b"]  # sets sorted by str


def test_dump_json_is_stable_and_unicode_friendly() -> None:
    text = dump_json({"name": "한글", "n": 1})
    assert '"한글"' in text
    assert '"n": 1' in text


def test_render_output_json_mode(capsys) -> None:
    render_output({"values": [1, 2, 3]}, force_json=True)
    out = capsys.readouterr().out
    assert '"values"' in out
    assert out.endswith("\n")


def test_render_output_human_readable_dict(monkeypatch, capsys) -> None:
    monkeypatch.setattr("cluefin_ta_cli.output.stdout_is_tty", lambda: True)
    render_output({"scalar": 5, "nested": {"a": 1}, "items": [1, 2]}, force_json=False)
    out = capsys.readouterr().out
    assert "scalar: 5" in out
    assert "nested:" in out
    assert "items:" in out


def test_render_output_human_readable_non_dict(monkeypatch, capsys) -> None:
    monkeypatch.setattr("cluefin_ta_cli.output.stdout_is_tty", lambda: True)
    render_output([1, 2, 3], force_json=False)
    out = capsys.readouterr().out
    assert "[" in out


def test_stdout_is_tty_returns_bool() -> None:
    assert isinstance(stdout_is_tty(), bool)
