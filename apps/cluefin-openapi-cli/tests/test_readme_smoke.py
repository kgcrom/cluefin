from __future__ import annotations

import json
from pathlib import Path

from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import RpcRegistry, set_registry_provider

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
    assert "`domains`: 업무 영역" in content
    assert "`tags`: 세부 기능" in content
    assert "`recipes`: 여러 command를 조합하는 workflow guide" in content
    assert "description" in content
    assert "when_to_use" in content
    assert "avoid_when" in content
    assert "example_filter" in content


def test_readme_discovery_examples_execute() -> None:
    set_registry_provider(RpcRegistry)
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


def test_readme_taxonomy_examples_match_json_shape() -> None:
    set_registry_provider(RpcRegistry)
    domains = json.loads(run_cli(["domains", "--json"]).stdout)
    tags = json.loads(run_cli(["tags", "--json"]).stdout)

    chart = next(item for item in domains["domains"] if item["name"] == "chart")
    ohlcv = next(item for item in tags["tags"] if item["name"] == "ohlcv")

    assert chart["description"]
    assert chart["when_to_use"]
    assert chart["avoid_when"]
    assert "ohlcv" in chart["related_tags"]
    assert chart["example_filter"] == "uv run cluefin-openapi-cli list --domain chart --json"
    assert ohlcv["related_domains"] == ["chart"]
    assert ohlcv["example_filter"] == "uv run cluefin-openapi-cli list --tag ohlcv --json"
