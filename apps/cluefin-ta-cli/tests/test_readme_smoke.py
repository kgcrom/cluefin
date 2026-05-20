from __future__ import annotations

from pathlib import Path

from cluefin_ta_cli.main import run_cli

README = Path("apps/cluefin-ta-cli/README.md")


def test_readme_mentions_agent_discovery_commands() -> None:
    content = README.read_text(encoding="utf-8")

    assert "list --domain technical-indicator --json" in content
    assert "list --tag momentum --json" in content
    assert "domains --json" in content
    assert "tags --json" in content
    assert "agent_notes" in content
    assert "cluefin-cli" in content


def test_readme_discovery_examples_execute() -> None:
    examples = [
        ["list", "--domain", "technical-indicator", "--json"],
        ["list", "--tag", "momentum", "--json"],
        ["domains", "--json"],
        ["tags", "--json"],
        ["describe", "ta", "rsi", "--json"],
    ]

    for argv in examples:
        result = run_cli(argv)
        assert result.exit_code == 0, argv
        assert result.stdout.strip().startswith("{"), argv
