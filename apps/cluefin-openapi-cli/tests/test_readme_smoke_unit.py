from __future__ import annotations

import json
from pathlib import Path

from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import RpcRegistry, set_registry_provider

README = Path("apps/cluefin-openapi-cli/README.md")
AGENTS = Path("apps/cluefin-openapi-cli/AGENTS.md")


def test_discovery_commands_execute() -> None:
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
    """README·AGENTS 와 discovery JSON(avoid_when/agent_notes)은 에이전트가 그대로 따르는 안내다.
    cluefin-cli 는 desk 로 흡수돼 삭제됐다 — 다시 등장하면 에이전트를 실패 경로로 보낸다."""
    set_registry_provider(RpcRegistry)
    for doc in (README, AGENTS):
        text = doc.read_text(encoding="utf-8")
        assert "cluefin-cli" not in text, doc
        assert "SKILL.md" not in text, doc
    # `recipes --json` 은 요약만 낸다 — agent_notes 는 레시피 상세에만 있다
    recipe_names = [r["name"] for r in json.loads(run_cli(["recipes", "--json"]).stdout)["recipes"]]
    for argv in [["domains", "--json"], ["tags", "--json"], *(["recipe", n, "--json"] for n in recipe_names)]:
        assert "cluefin-cli" not in run_cli(argv).stdout, argv


def test_taxonomy_entries_carry_guidance_and_a_runnable_filter() -> None:
    """문서는 domain·tag 를 설명하지 않고 `domains --json`·`tags --json` 으로 보낸다 — 그 응답이 스스로 설명해야 한다."""
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


def test_readme_and_agents_explain_roles_dry_run_and_error_branching() -> None:
    """두 문서가 계속 설명해야 하는 낱말이다. 문장은 고정하지 않는다."""
    readme = README.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")

    for text in (readme, agents):
        assert "primary" in text
        assert "auxiliary" in text
        assert "kis_alternatives" in text
        assert "--dry-run" in text
        assert "--fields" in text
        assert "brokers --json" in text
        assert "schema kis stock current-price --json" in text
        assert "retryable" in text
    assert "| 5 |" in readme  # exit-code table
