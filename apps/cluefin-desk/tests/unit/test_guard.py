"""screens/_guard.py — 실패 문구가 Rich 마크업으로 깨지지 않는지."""

from types import SimpleNamespace

from rich.text import Text

from cluefin_desk.screens import _guard


def test_guarded_failure_message_escapes_markup(monkeypatch):
    """pydantic ValidationError 메시지는 "[type=string_too_long, ...]" 를 담는다 — 그대로 넣으면 태그로 읽혀 사라진다."""
    shown: dict[str, str] = {}
    monkeypatch.setattr(_guard, "set_text", lambda screen, selector, text: shown.__setitem__(selector, text))
    screen = SimpleNamespace(is_attached=True)

    def boom():
        raise ValueError("1 validation error [type=string_too_long, input_value='x']")

    _guard.guarded(screen, "#panel", "뉴스", boom)
    plain = Text.from_markup(shown["#panel"]).plain
    assert "[type=string_too_long, input_value='x']" in plain
