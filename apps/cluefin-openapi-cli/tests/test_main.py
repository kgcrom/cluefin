from __future__ import annotations

from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import CommandSpec, set_registry_provider


class FakeRegistry:
    def __init__(self) -> None:
        self._commands = [
            CommandSpec(
                broker="kis",
                category="stock",
                name="current-price",
                description="Get current stock price.",
                path_segments=("kis", "stock", "current-price"),
                parameters={"type": "object"},
                returns={"type": "object"},
                executor=lambda params: {"params": params, "source": "kis"},
            ),
            CommandSpec(
                broker="kiwoom",
                category="chart",
                name="tick",
                description="Get tick chart.",
                path_segments=("kiwoom", "chart", "tick"),
                parameters={"type": "object"},
                returns={"type": "object"},
            ),
            CommandSpec(
                broker="dart",
                category="dart",
                name="company-overview",
                description="Get company overview.",
                path_segments=("dart", "company-overview"),
                parameters={
                    "type": "object",
                    "properties": {"corp_code": {"type": "string", "description": "Corp code"}},
                    "required": ["corp_code"],
                },
                returns={"type": "object"},
                executor=lambda params: {"corp_code": params["corp_code"]},
            ),
        ]

    def list_commands(self, *, broker: str | None = None, category: str | None = None):
        commands = self._commands
        if broker is not None:
            commands = [command for command in commands if command.broker == broker]
        if category is not None:
            commands = [command for command in commands if command.category == category]
        return commands

    def get_command(self, broker: str, category: str, name: str):
        for command in self._commands:
            if (command.broker, command.category, command.name) == (broker, category, name):
                return command
        return None

    def resolve_command(self, path_segments: tuple[str, ...]):
        for command in self._commands:
            if command.path_segments == path_segments:
                return command
        return None

    def iter_brokers(self):
        return sorted({command.broker for command in self._commands})

    def invoke_command(self, command: CommandSpec, params: dict[str, object]):
        assert command.executor is not None
        return command.executor(params)


def setup_module() -> None:
    set_registry_provider(FakeRegistry)


def teardown_module() -> None:
    from cluefin_openapi_cli.registry import EmptyRegistry

    set_registry_provider(EmptyRegistry)


def test_root_defaults_to_summary_json_when_non_tty() -> None:
    result = run_cli([])

    assert result.exit_code == 0
    assert "cluefin-openapi-cli" in result.stdout


def test_list_filters_registry_and_emits_json() -> None:
    result = run_cli(["list", "--broker", "kis", "--json"])

    assert result.exit_code == 0
    assert '"broker": "kis"' in result.stdout
    assert '"count": 1' in result.stdout


def test_describe_returns_command_metadata() -> None:
    result = run_cli(["describe", "kis", "stock", "current-price", "--json"])

    assert result.exit_code == 0
    assert '"qualified_name": "kis.stock.current-price"' in result.stdout


def test_describe_missing_command_exits_2() -> None:
    result = run_cli(["describe", "kis", "stock", "missing"])

    assert result.exit_code == 2


def test_root_help_returns_usage_payload() -> None:
    result = run_cli(["--help", "--json"])

    assert result.exit_code == 0
    assert '"usage"' in result.stdout


def test_broker_help_lists_categories() -> None:
    result = run_cli(["kis", "--help", "--json"])

    assert result.exit_code == 0
    assert '"categories"' in result.stdout


def test_category_help_lists_leaf_commands() -> None:
    result = run_cli(["kis", "stock", "--help", "--json"])

    assert result.exit_code == 0
    assert '"current-price"' in result.stdout


def test_leaf_command_merges_flags_and_params_json() -> None:
    result = run_cli(
        [
            "dart",
            "company-overview",
            "--params-json",
            '{"corp_code":"00000000"}',
            "--corp-code",
            "00126380",
            "--json",
        ]
    )

    assert result.exit_code == 0
    assert '"corp_code": "00126380"' in result.stdout


def test_leaf_command_reports_missing_required_params_as_json_error() -> None:
    result = run_cli(["dart", "company-overview", "--json"])

    assert result.exit_code == 2
    assert '"error"' in result.stdout
    assert '"missing"' in result.stdout
