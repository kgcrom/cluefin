from __future__ import annotations

import json

from cluefin_ta_cli.main import run_cli


def test_root_defaults_to_summary_json_when_non_tty() -> None:
    result = run_cli([])

    assert result.exit_code == 0
    assert "cluefin-ta-cli" in result.stdout


def test_list_returns_all_commands() -> None:
    result = run_cli(["list", "--json"])

    assert result.exit_code == 0
    assert '"category": "ta"' in result.stdout
    assert '"count": 11' in result.stdout


def test_list_filters_by_domain_and_tag() -> None:
    domain_result = run_cli(["list", "--domain", "risk-metric", "--json"])
    tag_result = run_cli(["list", "--tag", "moving-average", "--json"])

    assert domain_result.exit_code == 0
    assert '"domain": "risk-metric"' in domain_result.stdout
    assert '"qualified_name": "ta.mdd"' in domain_result.stdout
    assert tag_result.exit_code == 0
    assert '"tag": "moving-average"' in tag_result.stdout
    assert '"qualified_name": "ta.sma"' in tag_result.stdout


def test_domains_and_tags_return_discovery_catalogs() -> None:
    domains = run_cli(["domains", "--json"])
    tags = run_cli(["tags", "--json"])

    assert domains.exit_code == 0
    assert '"name": "technical-indicator"' in domains.stdout
    assert tags.exit_code == 0
    assert '"name": "momentum"' in tags.stdout


def test_describe_returns_command_metadata() -> None:
    result = run_cli(["describe", "ta", "sma", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    command = payload["command"]

    assert command["qualified_name"] == "ta.sma"
    assert command["domains"] == ["technical-indicator"]
    assert command["tags"] == ["moving-average", "trend"]
    assert command["use_cases"]
    assert command["examples"]
    assert "--params-json" in command["examples"][0]["command"]
    assert "ordered oldest to newest" in command["agent_notes"]


def test_ta_help_lists_commands() -> None:
    result = run_cli(["ta", "--help", "--json"])

    assert result.exit_code == 0
    assert '"commands"' in result.stdout
    assert '"sma"' in result.stdout


def test_root_help_mentions_discovery_commands() -> None:
    result = run_cli(["--help", "--json"])

    assert result.exit_code == 0
    assert "domains [--json]" in result.stdout
    assert "list [--domain DOMAIN] [--tag TAG]" in result.stdout


def test_leaf_command_merges_flags_and_params_json() -> None:
    result = run_cli(
        [
            "ta",
            "sma",
            "--params-json",
            '{"close":[1,2,3,4,5]}',
            "--timeperiod",
            "3",
            "--json",
        ]
    )

    assert result.exit_code == 0
    assert '"values"' in result.stdout


def test_leaf_command_reports_missing_required_params_as_json_error() -> None:
    result = run_cli(["ta", "sma", "--json"])

    assert result.exit_code == 2
    assert '"error"' in result.stdout
    assert '"missing"' in result.stdout


def test_array_params_must_use_params_json() -> None:
    result = run_cli(["ta", "sma", "--close", "[1,2,3]", "--json"])

    assert result.exit_code == 2
    assert '"error"' in result.stdout
    assert "--params-json" in result.stdout


def test_extra_positional_arguments_are_rejected() -> None:
    result = run_cli(["ta", "sma", "unexpected", "--params-json", '{"close":[1,2,3]}', "--json"])

    assert result.exit_code == 2
    assert '"error"' in result.stdout
    assert "Unexpected positional arguments" in result.stdout


def test_sma_executes() -> None:
    result = run_cli(["ta", "sma", "--params-json", '{"close":[1,2,3,4,5],"timeperiod":3}', "--json"])

    assert result.exit_code == 0
    assert '"values"' in result.stdout
    assert "2.0" in result.stdout


def test_macd_executes() -> None:
    result = run_cli(
        [
            "ta",
            "macd",
            "--params-json",
            '{"close":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]}',
            "--json",
        ]
    )

    assert result.exit_code == 0
    assert '"macd"' in result.stdout
    assert '"signal"' in result.stdout
    assert '"histogram"' in result.stdout


def test_mdd_executes_scalar_output() -> None:
    result = run_cli(["ta", "mdd", "--params-json", '{"returns":[0.1,-0.2,0.05,-0.1]}', "--json"])

    assert result.exit_code == 0
    assert '"value"' in result.stdout


def test_nan_is_serialized_as_null() -> None:
    result = run_cli(["ta", "sma", "--params-json", '{"close":[1,2],"timeperiod":3}', "--json"])

    assert result.exit_code == 0
    assert "null" in result.stdout
