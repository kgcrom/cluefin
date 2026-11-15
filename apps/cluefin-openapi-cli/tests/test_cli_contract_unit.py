"""전체 command 표면의 기계적 계약 검증.

- 모든 command가 `schema`가 유효한 JSON Schema를 내고, 그 안의 `invoke.dry_run`
  예시 문자열이 그대로 실행돼 exit 0 이어야 한다 (예시가 깨지면 agent 가 첫 호출부터 실패한다).
- 모든 command 의 dry-run 은 broker client 를 만들지 않아야 한다.
- README·AGENTS 코드 블록의 `uv run cluefin-openapi-cli ...` 줄은 전부 실행 가능해야 한다: 네트워크가 필요 없는
  것(discovery meta command, --dry-run)은 그대로, broker command 는 --dry-run 을 붙여서. `cache`·`audit`·`review` 줄은
  하위 명령 이름만 본다.
"""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path

import pytest

from cluefin_openapi_cli import registry as registry_module
from cluefin_openapi_cli.audit.cli import SUBCOMMANDS as AUDIT_SUBCOMMANDS
from cluefin_openapi_cli.cache.cli import SUBCOMMANDS as CACHE_SUBCOMMANDS
from cluefin_openapi_cli.main import META_COMMANDS, run_cli
from cluefin_openapi_cli.registry import EmptyRegistry, RpcRegistry, build_cli_registry, set_registry_provider
from cluefin_openapi_cli.review.cli import SUBCOMMANDS as REVIEW_SUBCOMMANDS

README = Path("apps/cluefin-openapi-cli/README.md")
AGENTS = Path("apps/cluefin-openapi-cli/AGENTS.md")
EXAMPLE_PREFIX = "uv run cluefin-openapi-cli"
# Discovery meta commands: offline by construction, so a documented line runs as written.
META = {"search", "brokers", "list", "describe", "schema", "domains", "tags", "recipes", "recipe"}
# Meta commands that read or write local state (the cache file, research/, transcripts) or call brokers themselves
# (`cache load`, `review collect`). Most of them ignore `--dry-run` — `review collect --dry-run` really collects — so
# a documented line is checked for a real subcommand and never executed.
LOCAL_STATE = {"cache": set(CACHE_SUBCOMMANDS), "audit": set(AUDIT_SUBCOMMANDS), "review": set(REVIEW_SUBCOMMANDS)}


class _ExplodingFactory:
    """client 가 만들어지면 즉시 실패 — dry-run/meta 경로가 네트워크를 건드리지 않음을 보장."""

    def create(self, broker: str):
        raise AssertionError(f"broker client for `{broker}` must not be created here")


@pytest.fixture(autouse=True)
def _registry_without_network(monkeypatch):
    monkeypatch.setattr(registry_module, "BrokerClientFactory", _ExplodingFactory)
    set_registry_provider(lambda: RpcRegistry(client_factory=_ExplodingFactory()))
    yield
    set_registry_provider(EmptyRegistry)


def _argv_from_example(command: str) -> list[str]:
    tokens = shlex.split(command)
    assert tokens[:3] == ["uv", "run", "cluefin-openapi-cli"], command
    return tokens[3:]


ALL_PATHS = sorted(build_cli_registry())


@pytest.mark.parametrize("path", ALL_PATHS, ids=[".".join(p) for p in ALL_PATHS])
def test_every_command_schema_is_valid_and_its_dry_run_example_runs(path: tuple[str, ...]) -> None:
    schema_result = run_cli(["schema", *path, "--json"])
    assert schema_result.exit_code == 0, schema_result.stdout
    schema = json.loads(schema_result.stdout)

    parameters = schema["parameters"]
    assert parameters["type"] == "object"
    assert parameters["additionalProperties"] is False
    properties = parameters.get("properties", {})
    for required in parameters.get("required", []):
        assert required in properties, f"{schema['command']}: required `{required}` has no property"
    for name, prop in properties.items():
        assert prop.get("type") in {"string", "integer", "number", "boolean", "array", "object"}, (
            schema["command"],
            name,
        )
        if "pattern" in prop:
            re.compile(prop["pattern"])
    assert {row["field"] for row in schema["options"]} == set(properties)
    assert schema["broker_role"] in {"primary", "auxiliary", "reference"}
    if schema["broker"] != "kiwoom":
        assert schema["kis_alternatives"] == []

    dry = run_cli(_argv_from_example(schema["invoke"]["dry_run"]))
    assert dry.exit_code == 0, dry.stdout
    payload = json.loads(dry.stdout)
    assert payload["dry_run"] is True
    assert payload["validation"] == "ok"
    assert set(payload["params"]) == set(parameters.get("required", []))
    assert payload["command"] == schema["command"]

    execute = run_cli([*_argv_from_example(payload["execute"])[:-1], "--dry-run", "--json"])
    assert execute.exit_code == 0, execute.stdout


def test_every_leaf_help_and_describe_render() -> None:
    for path in ALL_PATHS:
        assert run_cli([*path, "--help", "--json"]).exit_code == 0, path
        assert run_cli(["describe", *path, "--json"]).exit_code == 0, path


def _doc_commands(text: str) -> list[list[str]]:
    """Every example line inside a fenced block, whatever language the fence names.

    Fences are paired line by line. A regex over ```` ```bash … ``` ```` lost its place after the first ```` ```env ````
    or ```` ```json ```` block (the closing fence read as an opening one) and skipped every block after it.
    """

    commands: list[list[str]] = []
    in_fence = False
    pending = ""
    for raw in text.splitlines():
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            pending = ""
            continue
        if not in_fence:
            continue
        line = pending + raw
        if line.endswith("\\"):
            pending = line[:-1] + " "
            continue
        pending = ""
        line = line.split("#", 1)[0].strip()
        if line.startswith(EXAMPLE_PREFIX):
            commands.append(_argv_from_example(line))
    return commands


def _needs_network(argv: list[str]) -> bool:
    if not argv or argv[0].startswith("-") or argv[0] in META:
        return False
    return "--dry-run" not in argv


def test_every_meta_command_is_classified() -> None:
    """A meta command in neither set would have its documented lines re-run with `--dry-run` appended."""

    assert META | set(LOCAL_STATE) == set(META_COMMANDS)


def test_doc_commands_reads_every_fenced_block() -> None:
    text = "\n".join(
        [
            "```env",
            "KEY=...",
            "```",
            "```bash",
            f"{EXAMPLE_PREFIX} brokers --json   # comment",
            f"{EXAMPLE_PREFIX} kis analysis watchlist-multi-quote \\",
            "  --params-json '{}' --json",
            "```",
            f"{EXAMPLE_PREFIX} outside --json",
            "```",
            f"{EXAMPLE_PREFIX} recipes --json",
            "```",
        ]
    )

    assert _doc_commands(text) == [
        ["brokers", "--json"],
        ["kis", "analysis", "watchlist-multi-quote", "--params-json", "{}", "--json"],
        ["recipes", "--json"],
    ]


@pytest.mark.parametrize("doc", [README, AGENTS], ids=["README", "AGENTS"])
def test_documented_offline_commands_execute(doc: Path) -> None:
    text = doc.read_text(encoding="utf-8")
    commands = _doc_commands(text)
    # An example outside a fenced block is never checked, so there must be none.
    assert len(commands) == sum(line.strip().startswith(EXAMPLE_PREFIX) for line in text.splitlines()), doc

    local = [argv for argv in commands if argv and argv[0] in LOCAL_STATE]
    rest = [argv for argv in commands if not argv or argv[0] not in LOCAL_STATE]
    offline = [argv for argv in rest if not _needs_network(argv)]
    online = [argv for argv in rest if _needs_network(argv)]
    assert offline, doc

    for argv in local:
        assert len(argv) > 1, argv
        assert argv[1] in LOCAL_STATE[argv[0]], argv

    for argv in offline:
        result = run_cli(argv)
        assert result.exit_code == 0, (argv, result.stdout)
        assert result.stdout.lstrip().startswith("{"), argv

    # 네트워크가 필요한 예시도 최소한 경로·parameter 가 유효해야 한다: --dry-run 으로 바꿔 검증
    for argv in online:
        stripped = _drop_fields_value(argv)
        result = run_cli([*stripped, "--dry-run", "--json"])
        assert result.exit_code == 0, (argv, result.stdout)


def _drop_fields_value(argv: list[str]) -> list[str]:
    out: list[str] = []
    skip = False
    for token in argv:
        if skip:
            skip = False
            continue
        if token in {"--fields", "--limit"}:
            skip = True
            continue
        if token in {"--json", "--compact"} or token.startswith(("--fields=", "--limit=")):
            continue
        out.append(token)
    return out


def test_readme_exit_code_table_matches_errors_module() -> None:
    from cluefin_openapi_cli.errors import EXIT_CODES

    readme = README.read_text(encoding="utf-8")
    for code in EXIT_CODES:
        assert f"| {code} |" in readme, f"exit code {code} missing from README table"
    root = json.loads(run_cli(["--json"]).stdout)
    assert set(root["exit_codes"]) == {str(code) for code in EXIT_CODES}
