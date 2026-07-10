from __future__ import annotations

import pytest

from cluefin_cli.config.logging import is_debug_mode, set_debug_mode, setup_logging


@pytest.fixture(autouse=True)
def _restore_debug_mode():
    original = is_debug_mode()
    yield
    set_debug_mode(original)


def test_set_and_is_debug_mode() -> None:
    set_debug_mode(True)
    assert is_debug_mode() is True
    set_debug_mode(False)
    assert is_debug_mode() is False


@pytest.mark.parametrize("debug", [True, False])
def test_setup_logging_sets_debug_flag(debug) -> None:
    setup_logging(debug=debug)
    assert is_debug_mode() is debug
