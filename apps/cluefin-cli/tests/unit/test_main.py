from __future__ import annotations

from click.testing import CliRunner

from cluefin_cli.main import cli


def test_cli_help_lists_subcommands() -> None:
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "xbrl" in result.output
    assert "Commands:" in result.output


def test_cli_version() -> None:
    result = CliRunner().invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_callback_runs_setup(capsys) -> None:
    # Invoke the group callback directly to exercise its body.
    cli.callback(debug=True)
    out = capsys.readouterr().out
    assert "Cluefin CLI" in out
