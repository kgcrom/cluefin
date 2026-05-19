import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from cluefin_cli.domains.models import MarketRankItem
from cluefin_cli.main import cli


def test_market_subcommands_are_registered() -> None:
    result = CliRunner().invoke(cli, ["market", "--help"])

    assert result.exit_code == 0
    for subcommand in ["volume", "ranking", "theme", "sector"]:
        assert subcommand in result.output


@patch("cluefin_cli.commands.market.MarketService")
def test_market_subcommands_emit_json(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.return_value = [
        MarketRankItem(
            source="kis", category="volume", rank=1, stock_code="005930", stock_name="삼성전자", value="1000"
        )
    ]
    mock_service_cls.return_value = service

    for subcommand in ["volume", "ranking", "theme", "sector"]:
        result = CliRunner().invoke(cli, ["market", subcommand, "--limit", "1", "--json"])

        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["ok"] is True
        assert payload["command"] == f"market {subcommand}"
        assert payload["data"]["items"][0]["stock_code"] == "005930"

    assert service.fetch.call_count == 4


def test_readme_domain_examples_match_registered_commands() -> None:
    readme = Path("apps/cluefin-cli/README.md").read_text()
    expected_examples = [
        "cluefin-cli statements 005930 --json",
        "cluefin-cli chart 005930 --indicators --json",
        "cluefin-cli news 005930 --source all --json",
        "cluefin-cli trading-flow 005930 --json",
        "cluefin-cli market volume --json",
        "cluefin-cli market ranking --json",
        "cluefin-cli market theme --json",
        "cluefin-cli market sector --json",
    ]
    for example in expected_examples:
        assert example in readme

    runner = CliRunner()
    for command in ["statements", "chart", "news", "trading-flow", "market"]:
        assert runner.invoke(cli, [command, "--help"]).exit_code == 0
