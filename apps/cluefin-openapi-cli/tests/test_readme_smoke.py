from __future__ import annotations

from pathlib import Path

from cluefin_openapi_cli.main import run_cli

README = Path("apps/cluefin-openapi-cli/README.md")


def test_readme_mentions_agent_discovery_commands() -> None:
    content = README.read_text(encoding="utf-8")

    assert "list --domain chart --json" in content
    assert "list --tag ohlcv --json" in content
    assert "domains --json" in content
    assert "tags --json" in content
    assert "recipes --json" in content
    assert "recipe stock-research --json" in content
    assert "agent_notes" in content
    assert "cluefin-cli" in content


def test_readme_discovery_examples_execute() -> None:
    examples = [
        ["list", "--domain", "chart", "--json"],
        ["list", "--tag", "ohlcv", "--json"],
        ["domains", "--json"],
        ["tags", "--json"],
        ["recipes", "--json"],
        ["recipe", "stock-research", "--json"],
    ]

    for argv in examples:
        result = run_cli(argv)
        assert result.exit_code == 0, argv
        assert result.stdout.strip().startswith("{"), argv
