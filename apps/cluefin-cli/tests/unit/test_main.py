import json

from click.testing import CliRunner

from cluefin_cli.main import cli


def test_root_json_emits_parseable_envelope_without_banner() -> None:
    result = CliRunner().invoke(cli, ["--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "root"
    assert payload["data"]["app"] == "cluefin-cli"
    assert "Cluefin CLI - Stock Analysis Tool" not in result.output


def test_legacy_commands_are_marked_deprecated_in_help() -> None:
    runner = CliRunner()

    for command in ["ta", "fa", "xbrl"]:
        result = runner.invoke(cli, [command, "--help"])

        assert result.exit_code == 0
        assert "DEPRECATED" in result.output
