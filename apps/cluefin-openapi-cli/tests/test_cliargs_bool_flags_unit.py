"""Schema boolean flags (`--include-today`) used bare, without swallowing the next token."""

from __future__ import annotations

import json

from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import CommandSpec, EmptyRegistry, set_registry_provider

_TREND_SETUP = CommandSpec(
    broker="kis",
    category="chart",
    name="trend-setup",
    description="Judge a setup.",
    path_segments=("kis", "chart", "trend-setup"),
    parameters={
        "type": "object",
        "properties": {"stock_code": {"type": "string"}, "include_today": {"type": "boolean"}},
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    executor=lambda params, _client: {"params": params},
)


class _Registry(EmptyRegistry):
    def iter_brokers(self):
        return ["kis"]

    def resolve_command(self, path_segments: tuple[str, ...]):
        return _TREND_SETUP if path_segments == _TREND_SETUP.path_segments else None

    def invoke_command(self, command: CommandSpec, params: dict[str, object]):
        assert command.executor is not None
        return command.executor(params, None)


def setup_module() -> None:
    set_registry_provider(_Registry)


def teardown_module() -> None:
    set_registry_provider(EmptyRegistry)


def _params(*flags: str) -> dict[str, object]:
    result = run_cli(["kis", "chart", "trend-setup", *flags, "--json"])
    assert result.exit_code == 0, result.stdout
    return json.loads(result.stdout)["params"]


def test_bare_schema_boolean_does_not_swallow_the_next_option() -> None:
    assert _params("--include-today", "--stock-code", "005930") == {"include_today": True, "stock_code": "005930"}


def test_bare_schema_boolean_as_the_last_option() -> None:
    assert _params("--stock-code", "005930", "--include-today") == {"include_today": True, "stock_code": "005930"}


def test_schema_boolean_still_takes_an_explicit_value() -> None:
    assert _params("--include-today", "false", "--stock-code", "005930")["include_today"] is False
    assert _params("--include-today=no", "--stock-code", "005930")["include_today"] is False


def test_value_option_followed_by_another_option_is_a_usage_error() -> None:
    result = run_cli(["kis", "chart", "trend-setup", "--stock-code", "--include-today", "--json"])

    assert result.exit_code == 2
    assert "requires a value" in result.stdout
