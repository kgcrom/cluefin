"""screens/_guard.py — 실패 문구가 Rich 마크업으로 깨지지 않는지."""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

from rich.text import Text
from textual.css.query import NoMatches
from textual.message_pump import NoActiveAppError

from cluefin_desk.screens import _guard


def test_guarded_failure_message_escapes_markup(monkeypatch):
    """pydantic ValidationError 메시지는 "[type=string_too_long, ...]" 를 담는다 — 그대로 넣으면 태그로 읽혀 사라진다."""
    shown: dict[str, str] = {}
    monkeypatch.setattr(_guard, "set_text", lambda screen, selector, text: shown.__setitem__(selector, text))
    screen = SimpleNamespace(is_attached=True, is_running=True)

    def boom():
        raise ValueError("1 validation error [type=string_too_long, input_value='x']")

    _guard.guarded(screen, "#panel", "뉴스", boom)
    plain = Text.from_markup(shown["#panel"]).plain
    assert "[type=string_too_long, input_value='x']" in plain


class TestScreenGone:
    def test_live_screen_failure_is_a_real_failure(self):
        screen = SimpleNamespace(is_attached=True, is_running=True)
        assert _guard.screen_gone(screen, NoMatches("No nodes match '#panel'")) is False

    def test_no_active_app_is_cancellation(self):
        screen = SimpleNamespace(is_attached=True, is_running=True)
        assert _guard.screen_gone(screen, NoActiveAppError()) is True

    def test_detached_screen_is_cancellation(self):
        screen = SimpleNamespace(is_attached=False, is_running=False)
        assert _guard.screen_gone(screen, NoMatches("No nodes match '#panel'")) is True

    def test_screen_being_removed_is_cancellation(self):
        """pop 직후: 아직 붙어 있지만 펌프가 멈췄고 자식이 지워지는 중 — 2026-10-17 실측 상태."""
        screen = SimpleNamespace(is_attached=True, is_running=False)
        assert _guard.screen_gone(screen, NoMatches("No nodes match '#top-gainers-panel'")) is True


class FakeApp:
    def call_from_thread(self, fn):
        fn()


class TestSetText:
    def test_updates_live_screen(self):
        panel = MagicMock()
        screen = SimpleNamespace(is_attached=True, is_running=True, app=FakeApp(), query_one=lambda *_: panel)
        _guard.set_text(screen, "#panel", "hello")
        panel.update.assert_called_once_with("hello")

    def test_screen_closed_before_callback_runs_is_dropped(self):
        """워커가 검사한 뒤 콜백이 돌기 전에 화면이 내려간 경우 — 예전엔 NoMatches 가 워커를 죽였다."""

        def query_one(*_):
            raise NoMatches("No nodes match '#panel'")

        screen = SimpleNamespace(is_attached=True, is_running=False, app=FakeApp(), query_one=query_one)
        _guard.set_text(screen, "#panel", "hello")  # 예외 없이 버린다

    def test_guarded_on_removed_screen_logs_nothing(self, monkeypatch, caplog):
        caplog.set_level(logging.ERROR, logger="cluefin_desk")
        screen = SimpleNamespace(is_attached=True, is_running=False)

        def boom():
            raise NoMatches("No nodes match '#panel'")

        _guard.guarded(screen, "#panel", "급등", boom)
        assert caplog.records == []
