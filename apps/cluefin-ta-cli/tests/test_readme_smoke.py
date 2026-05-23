from __future__ import annotations

import json
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
    assert "`domains`: 업무 영역" in content
    assert "`tags`: 세부 기능" in content
    assert "`recipes`: 이 CLI에는 별도 recipe 명령이 없습니다" in content
    assert "description" in content
    assert "when_to_use" in content
    assert "avoid_when" in content
    assert "example_filter" in content


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


def test_readme_taxonomy_examples_match_json_shape() -> None:
    domains = json.loads(run_cli(["domains", "--json"]).stdout)
    tags = json.loads(run_cli(["tags", "--json"]).stdout)

    technical_indicator = next(item for item in domains["domains"] if item["name"] == "technical-indicator")
    moving_average = next(item for item in tags["tags"] if item["name"] == "moving-average")

    assert technical_indicator["description"]
    assert technical_indicator["when_to_use"]
    assert "portfolio-metric" in technical_indicator["avoid_when"]
    assert "moving-average" in technical_indicator["related_tags"]
    assert technical_indicator["example_filter"] == "uv run cluefin-ta-cli list --domain technical-indicator --json"
    assert moving_average["related_domains"] == ["technical-indicator"]
    assert moving_average["example_filter"] == "uv run cluefin-ta-cli list --tag moving-average --json"
