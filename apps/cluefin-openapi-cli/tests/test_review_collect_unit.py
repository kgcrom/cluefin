from __future__ import annotations

import json
import threading
import time
from datetime import date
from pathlib import Path

import pytest

from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.review import collect as rc
from cluefin_openapi_cli.review.cli import run_review, summary

DAY = date(2026, 11, 8)

_DISCLOSURES = {
    "result": {
        "list": [
            {"report_nm": "연결재무제표기준영업(잠정)실적(공정공시)", "rcept_no": "20261104800334"},
            {"report_nm": "반기보고서 (2026.06)", "rcept_no": "20260814004031"},
            {"report_nm": "분기보고서 (2026.03)", "rcept_no": "20260515002698"},
        ]
    }
}


def _reply(argv: list[str]) -> tuple[int, str, str]:
    path = tuple(t for t in argv if not t.startswith("--"))
    joined = " ".join(argv)
    if argv[:2] == ["dart", "corp-code-lookup"]:
        code = argv[argv.index("--stock-code") + 1]
        return 0, json.dumps({"data": [{"corp_code": f"00{code}"}]}), ""
    if argv[:2] == ["dart", "company-overview"]:
        return 0, json.dumps({"induty_code": "71310"}), ""
    if argv[:2] == ["dart", "disclosure-search"]:
        return 0, json.dumps(_DISCLOSURES), ""
    if argv[:2] == ["dart", "financial-summary"]:
        return (
            0,
            json.dumps({"reports": [{"year": 2026, "reprt_code": "11013"}, {"year": 2026, "reprt_code": "11012"}]}),
            "",
        )
    return 0, json.dumps({"ok": joined, "path": list(path)}), ""


class FakeRunner:
    def __init__(self, override=None) -> None:
        self.calls: list[list[str]] = []
        self._override = override or {}
        self._lock = threading.Lock()

    def __call__(self, argv: list[str]) -> tuple[int, str, str]:
        with self._lock:
            self.calls.append(argv)
        for key, value in self._override.items():
            if " ".join(argv).startswith(key):
                return value(argv) if callable(value) else value
        return _reply(argv)


def _manifest(out: Path) -> list[dict]:
    return [json.loads(line) for line in (out / "manifest.jsonl").read_text().splitlines()]


def test_full_graph_writes_raw_and_manifest(tmp_path: Path) -> None:
    runner = FakeRunner()
    result = rc.collect("214320", ["030000"], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)

    assert result.status == "ok"
    assert result.corp_codes == {"214320": "00214320", "030000": "00030000"}
    rows = _manifest(tmp_path)
    commands = {(r["subject"], r["command"]) for r in rows}
    # gate first, alone
    assert runner.calls[0][:3] == ["kis", "stock", "current-price"]
    # audit block: main + each + required
    for cmd in ("kis stock opinion-summary", "kis market announcement", "cache macro-beta", "cache base-rate",
                "kis stock implied-expectations", "kis stock flow-summary"):  # fmt: skip
        assert ("214320", cmd) in commands
    # flow-summary is stage1-only for the stock under review, not the peer (plan A2: "stage1 본 종목만")
    assert ("030000", "kis stock flow-summary") not in commands
    for subject in ("214320", "030000"):
        for cmd in ("dart corp-code-lookup", "kis stock current-price", "dart financial-summary", "kis stock valuation",
                    "kis stock valuation-band", "kis stock investor-metrics", "kis chart technical",
                    "kis chart trend-setup", "dart dilution-watch"):  # fmt: skip
            assert (subject, cmd) in commands, (subject, cmd)
    assert ("global", "ecos macro-snapshot") in commands
    assert ("global", "ecos industry-outlook") in commands
    # stage-2 inputs came from stage-1 answers
    by_node = {r["node"]: r for r in rows}
    assert "--induty-code" in by_node["global__ecos-industry-outlook"]["argv"]
    assert "71310" in by_node["global__ecos-industry-outlook"]["argv"]
    section = by_node["214320__dart-document-section"]["argv"]
    assert section[section.index("--rcept-no") + 1] == "20260814004031"  # the periodic report, not the 잠정실적
    ind = by_node["214320__dart-financial-major-indicators-M220000"]["argv"]
    assert ind[ind.index("--reprt-code") + 1] == "11012"
    # rs once with both codes
    rs = by_node["214320__cache-rs"]["argv"]
    assert rs[rs.index("--code") + 1] == "214320,030000"
    # every call has its raw file, stdout verbatim
    for r in rows:
        assert (tmp_path / r["file"]).read_text() == runner_output(runner, r["argv"])
        assert r["argv"][-1] == "--json"
    assert len(rows) == len(runner.calls)


def runner_output(runner: FakeRunner, argv: list[str]) -> str:
    return _reply(argv)[1]


def test_exit3_on_kis_stops_after_gate(tmp_path: Path) -> None:
    err = json.dumps({"error": {"type": "Credentials", "exit_code": 3}})
    runner = FakeRunner({"kis stock current-price": (3, err, "")})
    result = rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    assert result.status == "stopped"
    assert result.stopped_by == {
        "node": "214320__kis-stock-current-price",
        "command": "kis stock current-price",
        "exit_code": 3,
    }
    assert len(runner.calls) == 3  # gate only


def test_exit3_on_ecos_does_not_stop(tmp_path: Path) -> None:
    runner = FakeRunner({"ecos macro-snapshot": (3, "{}", "")})
    result = rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    assert result.status == "partial"
    assert result.stopped_by is None
    assert any(r.node.command == "dart financial-summary" for r in result.results)


def test_retryable_failure_retried_then_recorded(tmp_path: Path) -> None:
    attempts = {"n": 0}

    def flaky(argv: list[str]) -> tuple[int, str, str]:
        attempts["n"] += 1
        if attempts["n"] < 3:
            return 5, json.dumps({"error": {"retryable": True}}), "rate"
        return _reply(argv)

    runner = FakeRunner({"kis stock opinion-summary": flaky})
    sleeps: list[float] = []
    rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=sleeps.append)
    row = next(r for r in _manifest(tmp_path) if r["command"] == "kis stock opinion-summary")
    assert row["exit_code"] == 0
    assert row["attempts"] == 3
    assert sleeps == [2.0, 4.0]


def test_non_retryable_broker_error_not_retried(tmp_path: Path) -> None:
    runner = FakeRunner({"kis stock opinion-summary": (4, json.dumps({"error": {"retryable": False}}), "")})
    rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    row = next(r for r in _manifest(tmp_path) if r["command"] == "kis stock opinion-summary")
    assert row["exit_code"] == 4
    assert row["attempts"] == 1


def test_missing_stage1_answers_skip_dependants(tmp_path: Path) -> None:
    runner = FakeRunner(
        {
            "dart company-overview": (4, "{}", ""),
            "dart disclosure-search": (0, json.dumps({"result": {"list": []}}), ""),
        }
    )
    result = rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    reasons = {s["node"]: s["reason"] for s in result.skipped}
    assert "global__ecos-industry-outlook" in reasons
    assert "214320__dart-document-section" in reasons
    assert result.status == "partial"
    assert not any(r.node.command == "ecos industry-outlook" for r in result.results)


def test_peer_without_corp_code_is_skipped(tmp_path: Path) -> None:
    runner = FakeRunner({"dart corp-code-lookup --stock-code 030000": (0, json.dumps({"data": []}), "")})
    result = rc.collect("214320", ["030000"], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    assert "030000__*" in {s["node"] for s in result.skipped}
    assert not any(r.node.subject == "030000" and r.node.command == "dart financial-summary" for r in result.results)


def test_broker_limit_caps_concurrency(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(rc.BROKER_LIMITS, "kis", 2)
    live = {"kis": 0, "max": 0}
    lock = threading.Lock()

    def slow(argv: list[str]) -> tuple[int, str, str]:
        if "valuation-band" in argv:  # counts against the cache limit
            return _reply(argv)
        with lock:
            live["kis"] += 1
            live["max"] = max(live["max"], live["kis"])
        time.sleep(0.02)
        with lock:
            live["kis"] -= 1
        return _reply(argv)

    runner = FakeRunner({"kis": slow})
    rc.collect("214320", ["030000", "005930"], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    assert live["max"] == 2


def test_run_dir_never_reuses_a_run(tmp_path: Path) -> None:
    first = rc.run_dir(tmp_path, "214320", DAY)
    assert first.name == "214320-20261108"
    first.mkdir()
    (first / "manifest.jsonl").write_text("")
    assert rc.run_dir(tmp_path, "214320", DAY).name == "214320-20261108-2"


def test_summary_counts_failures(tmp_path: Path) -> None:
    runner = FakeRunner({"kis chart technical": (4, "{}", "")})
    result = rc.collect("214320", [], tmp_path, runner=runner, day=DAY, sleep=lambda s: None)
    out = summary(result)
    assert out["status"] == "partial"
    assert out["counts"]["failed"] == 1
    assert out["failed"][0]["command"] == "kis chart technical"
    assert out["counts"]["calls"] == out["counts"]["ok"] + out["counts"]["failed"]


@pytest.mark.parametrize(
    "argv",
    [
        ["collect"],
        ["collect", "--stock-code", "21432"],
        ["collect", "--stock-code", "214320", "--peers", "1,2"],
        ["collect", "--stock-code", "214320", "--peers", "000001,000002,000003,000004"],
        ["nope"],
    ],
)
def test_usage_errors(argv: list[str]) -> None:
    with pytest.raises(CliError) as exc:
        run_review(argv)
    assert exc.value.exit_code == 2


def test_out_with_existing_run_refused(tmp_path: Path) -> None:
    (tmp_path / "manifest.jsonl").write_text("")
    with pytest.raises(CliError):
        run_review(["collect", "--stock-code", "214320", "--out", str(tmp_path)])


def test_add_peers_appends_only_peer_calls(tmp_path: Path) -> None:
    rc.collect("214320", ["030000"], tmp_path, runner=FakeRunner(), day=DAY, sleep=lambda s: None)
    before = len(_manifest(tmp_path))
    runner = FakeRunner()
    result = rc.add_peers(tmp_path, ["030000", "214320", "005930"], runner=runner, sleep=lambda s: None)

    assert {s["node"] for s in result.skipped} == {"030000__*", "214320__*"}
    assert result.corp_codes == {"005930": "00005930"}
    rows = _manifest(tmp_path)[before:]
    assert {r["subject"] for r in rows} == {"005930", "214320"}  # 214320 only for the peers' RS call
    rs = next(r for r in rows if r["command"] == "cache rs")
    assert rs["argv"][rs["argv"].index("--code") + 1] == "005930"
    assert rs["node"] == "214320__cache-rs-peers-005930"
    assert len({r["node"] for r in _manifest(tmp_path)}) == len(_manifest(tmp_path))  # no raw file overwritten
    assert json.loads((tmp_path / "run.json").read_text())["peers"] == ["030000", "005930"]
    assert result.status == "ok"


def test_process_runner_matches_cli_output() -> None:
    from cluefin_openapi_cli.main import run_cli

    with rc.process_runner() as runner:
        code, out, _ = runner(["brokers", "--json"])
        bad, _, _ = runner(["review", "collect", "--json"])
    assert code == 0
    assert json.loads(out) == json.loads(run_cli(["brokers", "--json"]).stdout)
    assert bad == 2


def test_add_peers_needs_a_run_folder(tmp_path: Path) -> None:
    with pytest.raises(CliError):
        run_review(["collect", "--into", str(tmp_path), "--peers", "005930"])
    with pytest.raises(ValueError, match="run.json"):
        rc.add_peers(tmp_path, ["005930"], runner=FakeRunner(), sleep=lambda s: None)
