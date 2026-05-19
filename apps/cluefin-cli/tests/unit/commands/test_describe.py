import json

from click.testing import CliRunner

from cluefin_cli.main import cli


def test_describe_json_lists_domain_commands_without_banner() -> None:
    result = CliRunner().invoke(cli, ["describe", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "describe"
    assert "Cluefin CLI - Stock Analysis Tool" not in result.output
    assert {item["name"] for item in payload["data"]["commands"]} == {
        "statements",
        "chart",
        "news",
        "trading-flow",
        "market",
    }


def test_describe_json_can_select_one_command() -> None:
    result = CliRunner().invoke(cli, ["describe", "chart", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    commands = payload["data"]["commands"]
    assert len(commands) == 1
    assert commands[0]["name"] == "chart"
    assert commands[0]["usage"] == "cluefin-cli chart STOCK_CODE [OPTIONS]"
    assert any(option["name"] == "--indicators" for option in commands[0]["options"])


def test_describe_market_json_includes_subcommands() -> None:
    result = CliRunner().invoke(cli, ["describe", "market", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    market = payload["data"]["commands"][0]
    assert [item["name"] for item in market["subcommands"]] == ["volume", "ranking", "theme", "sector"]


def test_root_json_mentions_describe_discovery_command() -> None:
    result = CliRunner().invoke(cli, ["--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert "describe" in payload["data"]["discovery_commands"]
