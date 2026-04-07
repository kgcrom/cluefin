from __future__ import annotations

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


def test_describe_returns_command_metadata() -> None:
    result = run_cli(["describe", "ta", "sma", "--json"])

    assert result.exit_code == 0
    assert '"qualified_name": "ta.sma"' in result.stdout


def test_ta_help_lists_commands() -> None:
    result = run_cli(["ta", "--help", "--json"])

    assert result.exit_code == 0
    assert '"commands"' in result.stdout
    assert '"sma"' in result.stdout


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
