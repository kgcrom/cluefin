from __future__ import annotations

import json
from pathlib import Path

import pytest

from cluefin_openapi_cli.audit.check import check_run, parse_spec
from cluefin_openapi_cli.audit.transcript import load_run, load_session, parse_cli_calls, projects_dirs

SPEC = """
## 감사 기준

```audit
subjects: prompt, report
required: ecos macro-snapshot
main: kis stock opinion-summary
each: kis stock current-price
each: dart financial-summary
stop-on-exit3: kis dart
```
"""


def _bash(tool_id: str, command: str, stamp: str) -> dict:
    return {
        "type": "assistant",
        "timestamp": stamp,
        "message": {"content": [{"type": "tool_use", "id": tool_id, "name": "Bash", "input": {"command": command}}]},
    }


def _result(tool_id: str, text: str, *, error: bool = False) -> dict:
    return {
        "type": "user",
        "message": {"content": [{"type": "tool_result", "tool_use_id": tool_id, "content": text, "is_error": error}]},
    }


def _write_run(tmp_path: Path, rows: list[dict], agent: str = "company-review") -> Path:
    folder = tmp_path / "session-1" / "subagents"
    folder.mkdir(parents=True)
    path = folder / "agent-abc.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    (folder / "agent-abc.meta.json").write_text(json.dumps({"agentType": agent, "description": "t"}))
    return path


APP = "uv run cluefin-openapi-cli"


def _rows() -> list[dict]:
    lookup = json.dumps({"data": [{"corp_code": "00126380", "stock_code": "005930"}]})
    return [
        {"type": "user", "timestamp": "t0", "message": {"content": "삼성전자(005930) 검토"}},
        _bash("1", f"{APP} dart corp-code-lookup --stock-code 005930 --json", "t1"),
        _result("1", "WARNING retry\n" + lookup),
        _bash("2", f"{APP} kis stock current-price --stock-code 005930 --json 2>&1 | head", "t2"),
        _result("2", "{}"),
        # The same tool_use repeated by a streamed turn must count once.
        _bash("2", f"{APP} kis stock current-price --stock-code 005930 --json 2>&1 | head", "t2"),
        _bash("3", f"{APP} kis stock current-price --stock-code 005930 --json", "t3"),
        _result("3", "{}"),
        _bash("4", f"{APP} dart financial-summary --corp-code 00126380 --json", "t4"),
        _result("4", "{}"),
        _bash("5", f"{APP} kis stock current-price --stock-code 000660 --json", "t5"),
        _result("5", "Exit code 4\nupstream", error=True),
        _bash("6", f"for p in 1 2; do {APP} dart disclosure-search --page-no $p --json; done", "t6"),
        _result("6", "{}"),
        {
            "type": "assistant",
            "timestamp": "t7",
            "message": {"content": [{"type": "text", "text": "# 리포트\n비교: SK하이닉스(000660), 금액 123456원"}]},
        },
    ]


def test_parse_cli_calls_splits_chains_and_drops_redirects() -> None:
    calls = parse_cli_calls(f"cd /x && {APP} cache rs --code 005930,000660 --json 2>&1 | head -5; {APP} recipes")
    assert calls == [(("cache", "rs"), {"code": "005930,000660", "json": "true"}), (("recipes",), {})]


def test_parse_cli_calls_joins_backslash_continuations() -> None:
    """A call split over lines with `\\` used to lose every flag after the first line."""
    command = f"{APP} kis stock current-price \\\n  --stock-code 005930 \\\n  --json"
    assert parse_cli_calls(command) == [(("kis", "stock", "current-price"), {"stock-code": "005930", "json": "true"})]


@pytest.mark.parametrize(
    ("command", "to_file"),
    [
        (f"{APP} recipes --json > out.json", True),
        (f"{APP} recipes --json>out.json", True),
        (f"{APP} recipes --json 1>out.json", True),
        (f"{APP} recipes --json 2>err.log", False),
        (f"{APP} recipes --json 2>&1 | head", False),
        (f"{APP} recipes --json > /dev/null", False),
        (f"{APP} recipes --json | python3 -c 'print(1 if 2>1 else 0)'", False),
        (f"{APP} recipes --json | python3 -c 'import sys; a, b = 2, 1; print(a>b)'", False),
    ],
)
def test_to_file_detection(tmp_path: Path, command: str, to_file: bool) -> None:
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "x"}},
        _bash("1", command, "t1"),
        _result("1", ""),
    ]
    run = load_run(_write_run(tmp_path, rows))
    assert run.calls[0].to_file is to_file
    assert run.calls[0].args.get("json") == "true"


def test_shell_heredoc_curl_is_a_direct_api_call(tmp_path: Path) -> None:
    spec = parse_spec("company-review", "```audit\n```")
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", "bash <<'EOF'\ncurl -s https://openapi.koreainvestment.com:9443/uapi/order\nEOF", "t1"),
        _result("1", "{}"),
        _bash("2", "cat > notes.md <<'EOF'\ncurl is mentioned in a note\nEOF", "t2"),
        _result("2", ""),
    ]
    found = [f for f in check_run(spec, load_run(_write_run(tmp_path, rows)))["findings"]]
    direct = [f for f in found if f["type"] == "off_cli_direct_api"]
    assert len(direct) == 1
    assert direct[0]["shell"].startswith("bash")
    assert any(f["type"] == "off_cli_order" for f in found)


def test_load_run_reads_calls_exit_codes_and_report(tmp_path: Path) -> None:
    run = load_run(_write_run(tmp_path, _rows()))
    assert run.agent == "company-review"
    assert [c.command for c in run.calls][:3] == [
        "dart corp-code-lookup",
        "kis stock current-price",
        "kis stock current-price",
    ]
    assert [c.exit_code for c in run.calls if c.command == "kis stock current-price"] == [0, 0, 4]
    assert run.report.startswith("# 리포트")


def test_check_run_finds_missing_duplicate_failure_and_loop(tmp_path: Path) -> None:
    run = load_run(_write_run(tmp_path, _rows()))
    result = check_run(parse_spec("company-review", SPEC), run, valid=frozenset({"005930", "000660"}))
    assert result["main"] == "005930"
    # 123456 is an amount, not a listed code.
    assert result["subjects"] == ["005930", "000660"]
    found = {(f["type"], f.get("command"), f.get("code")) for f in result["findings"]}
    assert ("missing_required", "ecos macro-snapshot", None) in found
    assert ("missing_main", "kis stock opinion-summary", "005930") in found
    # financial-summary was called by corp code; the lookup output maps it back to 005930.
    assert ("missing_each", "dart financial-summary", "005930") not in found
    assert ("missing_each", "dart financial-summary", "000660") in found
    assert ("duplicate", "kis stock current-price", None) in found
    assert ("failed_not_retried", "kis stock current-price", None) in found
    assert any(f["type"] == "shell_expansion" for f in result["findings"])


def test_exit3_stop_rule(tmp_path: Path) -> None:
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} kis stock current-price --stock-code 005930 --json", "t1"),
        _result("1", "Exit code 3\nkey", error=True),
        _bash("2", f"{APP} dart corp-code-lookup --stock-code 005930 --json", "t2"),
        _result("2", "{}"),
    ]
    result = check_run(parse_spec("company-review", SPEC), load_run(_write_run(tmp_path, rows)))
    stop = [f for f in result["findings"] if f["type"] == "continued_after_exit3"]
    assert stop
    assert stop[0]["later_calls"] == ["dart corp-code-lookup"]


def test_load_session_starts_at_first_call_for_code(tmp_path: Path) -> None:
    rows = [
        _bash("0", f"{APP} kis stock current-price --stock-code 111111 --json", "t0"),
        _result("0", "{}"),
        *_rows()[1:],
    ]
    path = tmp_path / "s.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    run = load_session(path, "005930")
    assert run.calls[0].command == "dart corp-code-lookup"
    assert "111111" not in {code for c in run.calls for code in c.codes()}
    result = check_run(parse_spec("company-review", SPEC), run, main_code="005930")
    # In a session slice peers come from calls of `each` commands, not from prose.
    assert result["subjects"] == ["005930", "000660"]


def test_parse_spec_rejects_unknown_lines() -> None:
    with pytest.raises(ValueError, match="unknown audit line"):
        parse_spec("x", "```audit\nwhatever: a\n```")
    with pytest.raises(ValueError, match="no ```audit block"):
        parse_spec("x", "no block")


def test_projects_dirs_matches_repo_and_worktree_slugs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    base = tmp_path / "projects"
    slug = "".join(ch if ch.isalnum() else "-" for ch in str(repo.resolve()))
    (base / slug).mkdir(parents=True)
    (base / f"{slug}--claude-worktrees-a").mkdir()
    (base / "other").mkdir()
    assert [p.name for p in projects_dirs(repo, base)] == [slug, f"{slug}--claude-worktrees-a"]


def test_to_file_off_cli_and_report_contract(tmp_path: Path) -> None:
    spec = parse_spec(
        "company-review",
        "```audit\nreport-has: data_as_of\nreport-has: 무효화\nreport-lacks: 목표가|확신도\n```",
    )
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} dart financial-major-indicators --corp-code 00126380 --json > /tmp/a.json", "t1"),
        _result("1", ""),
        _bash("2", "cat .env | grep KIS", "t2"),
        _result("2", "x"),
        _bash("3", "python3 -c 'from cluefin_openapi.kis import x; x.place_order()'", "t3"),
        _result("3", "x"),
        {
            "type": "assistant",
            "timestamp": "t4",
            "message": {"content": [{"type": "text", "text": "무효화 2개, 목표가 1"}]},
        },
    ]
    run = load_run(_write_run(tmp_path, rows))
    assert run.calls[0].to_file
    found = {f["type"] for f in check_run(spec, run)["findings"]}
    assert {"output_to_file", "off_cli_secret", "off_cli_direct_api", "off_cli_order"} <= found
    assert "report_lacks_required" in found
    assert "report_has_forbidden" in found


def test_duplicate_marks_different_outputs(tmp_path: Path) -> None:
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} dart financial-notes --corp-code 1 --json", "t1"),
        _result("1", '{"a": 1}'),
        _bash("2", f"{APP} dart financial-notes --corp-code 1 --json", "t2"),
        _result("2", '{"a": 2}'),
    ]
    result = check_run(parse_spec("x", "```audit\nsubjects: prompt\n```"), load_run(_write_run(tmp_path, rows)))
    dup = next(f for f in result["findings"] if f["type"] == "duplicate")
    assert dup["calls"] == [0, 1]
    assert dup["same_output"] is False


def _collect_folder(folder: Path) -> Path:
    raw = folder / "raw"
    raw.mkdir(parents=True)
    lookup = json.dumps({"data": [{"corp_code": "00126380", "stock_code": "005930"}]})
    lines = [
        (["kis", "stock", "current-price", "--stock-code", "005930", "--json"], 0, "{}"),
        (["dart", "corp-code-lookup", "--stock-code", "005930", "--json"], 0, lookup),
        (["ecos", "macro-snapshot", "--json"], 0, "{}"),
        (["kis", "stock", "opinion-summary", "--stock-code", "005930", "--json"], 0, "{}"),
        (["dart", "financial-summary", "--corp-code", "00126380", "--json"], 0, '{"x": 1}'),
        (["ecos", "industry-outlook", "--induty-code", "71310", "--json"], 2, '{"error": {}}'),
    ]
    with (folder / "manifest.jsonl").open("w") as fh:
        for i, (argv, code, out) in enumerate(lines):
            (raw / f"n{i}.json").write_text(out)
            fh.write(json.dumps({"argv": argv, "exit_code": code, "file": f"raw/n{i}.json", "started": f"s{i}"}) + "\n")
    return folder


def test_review_collect_manifest_counts_as_calls(tmp_path: Path) -> None:
    folder = _collect_folder(tmp_path / "214-20261108")
    summary = json.dumps({"out": str(folder), "status": "partial"})
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "삼성전자(005930) 검토"}},
        _bash("1", f"{APP} review collect --stock-code 005930 --json", "t1"),
        _result("1", "WARNING retry\n" + summary),
    ]
    run = load_run(_write_run(tmp_path, rows))
    assert [c.command for c in run.calls][:3] == ["review collect", "kis stock current-price", "dart corp-code-lookup"]
    fs = next(c for c in run.calls if c.command == "dart financial-summary")
    assert fs.output == '{"x": 1}'
    assert fs.via == str(folder)
    assert [c.index for c in run.calls] == list(range(len(run.calls)))
    result = check_run(parse_spec("company-review", SPEC), run, valid=frozenset({"005930"}))
    types = {(f["type"], f.get("command")) for f in result["findings"]}
    assert not any(t in {"missing_required", "missing_main", "missing_each"} for t, _ in types)
    assert ("failed_not_retried", "ecos industry-outlook") in types
    assert "output_to_file" not in {t for t, _ in types}


def test_report_md_in_collect_folder_is_the_report(tmp_path: Path) -> None:
    folder = _collect_folder(tmp_path / "214-20261108")
    (folder / "report.md").write_text("# 리포트\nhorizon_days: 60\n데이터 출처")
    summary = json.dumps({"out": str(folder), "status": "ok"})
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} review collect --stock-code 005930 --json", "t1"),
        _result("1", summary),
        {"type": "assistant", "timestamp": "t2", "message": {"content": [{"type": "text", "text": "폴더: watch"}]}},
    ]
    run = load_run(_write_run(tmp_path, rows))
    assert run.report.startswith("# 리포트")
    assert run.report.endswith("폴더: watch")
    spec = parse_spec("x", "```audit\nsubjects: prompt\nreport-has: horizon_days\nreport-has: 데이터 출처\n```")
    assert not any(f["type"] == "report_lacks_required" for f in check_run(spec, run)["findings"])


def test_review_collect_into_same_folder_not_counted_twice(tmp_path: Path) -> None:
    folder = _collect_folder(tmp_path / "214-20261108")
    summary = json.dumps({"out": str(folder), "status": "ok"})
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} review collect --stock-code 005930 --json", "t1"),
        _result("1", summary),
        _bash("2", f"{APP} review collect --into {folder} --peers 000660 --json", "t2"),
        _result("2", summary),
    ]
    run = load_run(_write_run(tmp_path, rows))
    result = check_run(parse_spec("company-review", SPEC), run, valid=frozenset({"005930"}))
    assert not any(f["type"] == "duplicate" for f in result["findings"])
    assert sum(1 for c in run.calls if c.command == "dart financial-summary") == 1


def test_review_collect_without_manifest_is_flagged(tmp_path: Path) -> None:
    summary = json.dumps({"out": str(tmp_path / "gone"), "status": "ok"})
    rows = [
        {"type": "user", "timestamp": "t0", "message": {"content": "005930"}},
        _bash("1", f"{APP} review collect --stock-code 005930 --json", "t1"),
        _result("1", summary),
    ]
    run = load_run(_write_run(tmp_path, rows))
    assert [c.command for c in run.calls] == ["review collect"]
    result = check_run(parse_spec("company-review", SPEC), run, valid=frozenset({"005930"}))
    assert any(f["type"] == "collect_manifest_missing" for f in result["findings"])
