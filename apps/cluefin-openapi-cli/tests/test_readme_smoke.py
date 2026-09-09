from __future__ import annotations

import json
from pathlib import Path

from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import RpcRegistry, set_registry_provider

README = Path("apps/cluefin-openapi-cli/README.md")
SKILL = Path("apps/cluefin-openapi-cli/SKILL.md")


def test_readme_mentions_agent_discovery_commands() -> None:
    content = README.read_text(encoding="utf-8")

    assert "list --domain chart --json" in content
    assert "list --tag ohlcv --json" in content
    assert "domains --json" in content
    assert "tags --json" in content
    assert "recipes --json" in content
    assert "recipe stock-research --json" in content
    assert "agent_notes" in content
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
        ["brokers", "--json"],
        ["list", "--broker", "kis", "--json"],
        ["list", "--query", "theme", "--json"],
        ["list", "--full", "--json"],
        ["schema", "kis", "stock", "current-price", "--json"],
        ["kis", "stock", "current-price", "--stock-code", "005930", "--dry-run", "--json"],
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


def test_agent_guidance_does_not_point_at_deleted_commands() -> None:
    """README 와 discovery JSON(avoid_when/agent_notes)은 에이전트가 그대로 따르는 안내다.
    cluefin-cli 는 desk 로 흡수돼 삭제됐다 — 다시 등장하면 에이전트를 실패 경로로 보낸다."""
    set_registry_provider(RpcRegistry)
    assert "cluefin-cli" not in README.read_text(encoding="utf-8")
    # `recipes --json` 은 요약만 낸다 — agent_notes 는 레시피 상세에만 있다
    recipe_names = [r["name"] for r in json.loads(run_cli(["recipes", "--json"]).stdout)["recipes"]]
    for argv in [["domains", "--json"], ["tags", "--json"], *(["recipe", n, "--json"] for n in recipe_names)]:
        assert "cluefin-cli" not in run_cli(argv).stdout, argv


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


def test_readme_and_skill_document_roles_dry_run_and_exit_codes() -> None:
    readme = README.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")

    for text in (readme, skill):
        assert "primary" in text and "auxiliary" in text
        assert "kis_alternatives" in text
        assert "--dry-run" in text
        assert "--fields" in text
        assert "brokers --json" in text
        assert "schema kis stock current-price --json" in text
        assert "retryable" in text
    assert "| 5 |" in readme  # exit-code table
    assert skill.startswith("---\nname: cluefin-openapi-cli\n")
    assert "cluefin-cli" not in skill
