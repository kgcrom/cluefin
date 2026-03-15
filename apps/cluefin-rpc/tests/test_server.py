"""Tests for server CLI options: --list-methods category filtering."""

from __future__ import annotations

import io
import subprocess
import sys

import pytest
from loguru import logger

from cluefin_rpc.dispatcher import Dispatcher
from cluefin_rpc.server import _build_dispatcher, _print_methods


@pytest.fixture()
def dispatcher() -> Dispatcher:
    return _build_dispatcher()


@pytest.fixture()
def log_capture():
    """loguru 출력을 캡처하는 fixture."""
    sink = io.StringIO()
    handler_id = logger.add(sink, format="{message}")
    yield sink
    logger.remove(handler_id)


# ---------------------------------------------------------------------------
# _print_methods unit tests
# ---------------------------------------------------------------------------


class TestPrintMethodsCategoryFilter:
    """_print_methods(dispatcher, category=...) 동작 검증."""

    def test_all_methods_without_category(self, dispatcher, log_capture):
        """category=None이면 전체 메서드를 출력한다."""
        _print_methods(dispatcher)
        output = log_capture.getvalue()
        assert "[stock]" in output
        assert "[ta]" in output

    def test_filter_by_valid_category(self, dispatcher, log_capture):
        """유효한 카테고리를 지정하면 해당 카테고리만 출력한다."""
        _print_methods(dispatcher, category="stock")
        output = log_capture.getvalue()
        assert "[stock]" in output
        assert "[ta]" not in output
        assert "[chart]" not in output

    def test_invalid_category_shows_guidance(self, dispatcher, log_capture):
        """존재하지 않는 카테고리를 지정하면 안내 메시지를 출력한다."""
        _print_methods(dispatcher, category="nonexistent")
        output = log_capture.getvalue()
        assert "nonexistent" in output
        assert "--list-categories" in output

    def test_filter_returns_only_matching_methods(self, dispatcher):
        """필터링된 메서드가 모두 지정 카테고리에 속하는지 확인."""
        methods = dispatcher.list_methods(category="stock")
        assert len(methods) > 0
        for m in methods:
            assert m["category"] == "stock"


# ---------------------------------------------------------------------------
# CLI argument parsing (subprocess)
# ---------------------------------------------------------------------------


class TestListMethodsCLI:
    """--list-methods CLI 인자 파싱 검증 (subprocess)."""

    def _run_cli(self, *extra_args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "cluefin_rpc", *extra_args],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_list_methods_no_arg(self):
        """--list-methods (인자 없음) → 전체 메서드 출력."""
        result = self._run_cli("--list-methods")
        assert result.returncode == 0
        assert "[stock]" in result.stderr
        assert "[ta]" in result.stderr

    def test_list_methods_with_category(self):
        """--list-methods stock → stock 카테고리만 출력."""
        result = self._run_cli("--list-methods", "stock")
        assert result.returncode == 0
        assert "[stock]" in result.stderr
        assert "[ta]" not in result.stderr

    def test_list_methods_invalid_category(self):
        """--list-methods xyz → 안내 메시지 출력."""
        result = self._run_cli("--list-methods", "xyz")
        assert result.returncode == 0
        assert "xyz" in result.stderr
        assert "--list-categories" in result.stderr
