from __future__ import annotations

import json

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
                domains=("quote", "market"),
                tags=("current-price",),
                examples=(
                    {
                        "description": "Run current price.",
                        "command": 'uv run cluefin-openapi-cli kis stock current-price --params-json \'{"stock_code":"005930"}\' --json',
                    },
                ),
                agent_notes="Use --json for machine-readable current-price output.",
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
                domains=("chart",),
                tags=("tick", "ohlcv"),
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
                domains=("statements",),
                tags=("disclosure",),
                executor=lambda params: {"corp_code": params["corp_code"]},
            ),
            CommandSpec(
                broker="dart",
                category="dart",
                name="failing-command",
                description="Raise an executor error.",
                path_segments=("dart", "failing-command"),
                parameters={"type": "object"},
                returns={"type": "object"},
                domains=("news",),
                tags=("disclosure",),
                executor=lambda params: (_ for _ in ()).throw(RuntimeError("broker unavailable")),
            ),
        ]

    def list_commands(
        self,
        *,
        broker: str | None = None,
        category: str | None = None,
        domain: str | None = None,
        tag: str | None = None,
    ):
        commands = self._commands
        if broker is not None:
            commands = [command for command in commands if command.broker == broker]
        if category is not None:
            commands = [command for command in commands if command.category == category]
        if domain is not None:
            commands = [command for command in commands if domain in command.domains]
        if tag is not None:
            commands = [command for command in commands if tag in command.tags]
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


def test_list_filters_by_domain_and_tag() -> None:
    domain_result = run_cli(["list", "--domain", "chart", "--json"])
    tag_result = run_cli(["list", "--tag", "current-price", "--json"])

    assert domain_result.exit_code == 0
    assert '"domain": "chart"' in domain_result.stdout
    assert '"qualified_name": "kiwoom.chart.tick"' in domain_result.stdout
    assert tag_result.exit_code == 0
    assert '"tag": "current-price"' in tag_result.stdout
    assert '"qualified_name": "kis.stock.current-price"' in tag_result.stdout


def test_domains_and_tags_return_discovery_catalogs() -> None:
    domains = run_cli(["domains", "--json"])
    tags = run_cli(["tags", "--json"])

    assert domains.exit_code == 0
    domains_payload = json.loads(domains.stdout)
    chart_domain = next(item for item in domains_payload["domains"] if item["name"] == "chart")
    assert chart_domain["command_count"] == 1
    assert "OHLCV" in chart_domain["description"]
    assert "technical analysis" in chart_domain["when_to_use"]
    assert "ohlcv" in chart_domain["related_tags"]
    assert chart_domain["example_filter"] == "uv run cluefin-openapi-cli list --domain chart --json"
    assert tags.exit_code == 0
    tags_payload = json.loads(tags.stdout)
    ohlcv_tag = next(item for item in tags_payload["tags"] if item["name"] == "ohlcv")
    assert "Open, high, low, close" in ohlcv_tag["description"]
    assert "technical indicators" in ohlcv_tag["when_to_use"]
    assert "chart" in ohlcv_tag["related_domains"]
    assert ohlcv_tag["example_filter"] == "uv run cluefin-openapi-cli list --tag ohlcv --json"


def test_recipes_and_recipe_return_workflow_metadata() -> None:
    recipes = run_cli(["recipes", "--json"])
    recipe = run_cli(["recipe", "stock-research", "--json"])

    assert recipes.exit_code == 0
    assert '"name": "stock-research"' in recipes.stdout
    assert '"step_count"' in recipes.stdout
    assert recipe.exit_code == 0
    assert '"title": "Stock Research"' in recipe.stdout
    assert '"command"' in recipe.stdout
    assert '"kis"' in recipe.stdout


def test_unknown_recipe_exits_2() -> None:
    result = run_cli(["recipe", "missing", "--json"])

    assert result.exit_code == 2
    assert "Unknown recipe" in result.stdout


def test_describe_returns_command_metadata() -> None:
    result = run_cli(["describe", "kis", "stock", "current-price", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    command = payload["command"]

    assert command["qualified_name"] == "kis.stock.current-price"
    assert command["domains"] == ["quote", "market"]
    assert command["tags"] == ["current-price"]
    assert command["use_cases"] == []
    assert command["examples"]
    assert "cluefin-openapi-cli kis stock current-price" in command["examples"][0]["command"]
    assert command["agent_notes"] == "Use --json for machine-readable current-price output."
    assert command["required_credentials"] == []
    assert command["side_effect"] == "read"


def test_describe_missing_command_exits_2() -> None:
    result = run_cli(["describe", "kis", "stock", "missing"])

    assert result.exit_code == 2


def test_root_help_returns_usage_payload() -> None:
    result = run_cli(["--help", "--json"])

    assert result.exit_code == 0
    assert '"usage"' in result.stdout
    assert "domains [--json]" in result.stdout
    assert "list [--domain DOMAIN] [--tag TAG]" in result.stdout
    assert "recipes [--json]" in result.stdout
    assert "recipe <name> [--json]" in result.stdout


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


def test_leaf_command_reports_invalid_params_json_before_schema_flags() -> None:
    result = run_cli(["dart", "company-overview", "--params-json", "{", "--corp-code", "00126380", "--json"])

    assert result.exit_code == 2
    assert '"error"' in result.stdout
    assert "--params-json" in result.stdout


def test_leaf_command_reports_executor_failure_as_json_error() -> None:
    result = run_cli(["dart", "failing-command", "--json"])

    assert result.exit_code == 1
    assert '"error"' in result.stdout
    assert "dart.failing-command" in result.stdout
    assert "broker unavailable" in result.stdout
