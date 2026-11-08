"""Collect everything a company review reads into one folder, in parallel stages.

The company-review agent used to call ~15 commands (plus 9 per peer) one Bash call at a time, and every JSON reply
piled up in its context. Fetching is deterministic — the same stock on the same day means the same commands — so
it runs here as a small graph instead, and the agent reads the folder:

    stage 0  gate      kis current-price first (it refreshes the shared KIS token cache), then dart corp-code-lookup
                       and cache status. A kis/dart exit 3 stops the run.
    stage 1  parallel  ecos macro-snapshot, everything that needs only the stock code or the corp code from stage 0,
                       and the peers' corp codes.
    stage 2  parallel  what needs a stage-1 answer: industry outlook (induty code), the latest periodic report's
                       business section and notes (rcept no), DART major indicators (report year/code), and the
                       peers' own data (peer corp code).

Every command runs as its own CLI process, so outputs and exit codes are exactly what a manual call prints. Each
stdout lands in `raw/<node>.json` and each call is one line of `manifest.jsonl`, which `audit` reads instead of the
transcript. Calls are capped per broker so a fan-out does not trip KIS/DART rate limits.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.clock import KST, today_kst

__all__ = [
    "BROKER_LIMITS",
    "CollectResult",
    "Node",
    "NodeResult",
    "Runner",
    "collect",
    "default_root",
    "run_dir",
    "subprocess_runner",
]

logger = logging.getLogger(__name__)

# (exit code, stdout, stderr)
Runner = Callable[[list[str]], tuple[int, str, str]]

# Concurrent calls per broker. KIS allows a handful of requests a second on one app key and DART throttles bursts;
# the local cache is a DuckDB file, so one reader at a time keeps lock errors out.
BROKER_LIMITS: dict[str, int] = {"kis": 3, "dart": 3, "ecos": 2, "cache": 1}
_STOP_BROKERS = frozenset({"kis", "dart"})
_RETRY_EXITS = frozenset({4, 5})
_MAX_ATTEMPTS = 3
_BACKOFF_SECONDS = 2.0
_PERIODIC = ("사업보고서", "반기보고서", "분기보고서")
_NOTE_TITLES = "특수관계자,차입금,우발"
_INDICATOR_CLASSES = ("M210000", "M220000", "M230000")  # 수익성, 안정성, 성장성
_REVIEW_DIR_ENV = "CLUEFIN_REVIEW_DIR"


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    subject: str  # stock code the call is about, or "global"
    broker: str  # which per-broker limit the call counts against
    path: tuple[str, ...]  # command path, e.g. ("kis", "stock", "valuation")
    argv: tuple[str, ...]

    @property
    def command(self) -> str:
        return " ".join(self.path)


@dataclass(frozen=True, slots=True)
class NodeResult:
    node: Node
    exit_code: int
    stdout: str
    stderr: str
    attempts: int
    started: str
    ended: str

    def payload(self) -> Any:
        try:
            return json.loads(self.stdout)
        except ValueError:
            return None


@dataclass(frozen=True, slots=True)
class CollectResult:
    out: Path
    status: str  # ok | partial | stopped
    results: tuple[NodeResult, ...]
    skipped: tuple[dict[str, str], ...]
    stopped_by: dict[str, Any] | None
    corp_codes: dict[str, str] = field(default_factory=dict)


def subprocess_runner(argv: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(  # noqa: S603 — argv is built here from fixed command paths and validated codes
        [sys.executable, "-m", "cluefin_openapi_cli.main", *argv],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    return proc.returncode, proc.stdout, proc.stderr


def default_root() -> Path:
    env = os.environ.get(_REVIEW_DIR_ENV)
    if env:
        return Path(env)
    # macOS resolves /tmp to /private/tmp; use the real path so the folder named in reports matches `ls`.
    base = Path("/private/tmp") if Path("/private/tmp").is_dir() else Path("/tmp")
    return base / "cluefin-review"


def run_dir(root: Path, stock_code: str, day: date) -> Path:
    """`<code>-<YYYYMMDD>`, or `-2`, `-3`… when that folder already holds a run — never overwrite earlier output."""

    stem = f"{stock_code}-{day:%Y%m%d}"
    candidate = root / stem
    n = 2
    while (candidate / "manifest.jsonl").exists():
        candidate = root / f"{stem}-{n}"
        n += 1
    return candidate


def _node(subject: str, broker: str, *argv: str, suffix: str = "") -> Node:
    first_flag = next((i for i, t in enumerate(argv) if t.startswith("--")), len(argv))
    path = tuple(argv[:first_flag])
    stem = "-".join(path) + (f"-{suffix}" if suffix else "")
    return Node(id=f"{subject}__{stem}", subject=subject, broker=broker, path=path, argv=(*argv, "--json"))


# ---------------------------------------------------------------- stage builders


def _gate_first(code: str) -> list[Node]:
    return [_node(code, "kis", "kis", "stock", "current-price", "--stock-code", code)]


def _gate_rest(code: str) -> list[Node]:
    return [
        _node(code, "dart", "dart", "corp-code-lookup", "--stock-code", code),
        _node("global", "cache", "cache", "status"),
    ]


def _stage1(code: str, corp: str, peers: list[str], day: date) -> list[Node]:
    year_ago = (day - timedelta(days=365)).strftime("%Y%m%d")
    nodes = [
        # ECOS exit 3 does not stop a review, so the slow macro snapshot (~8 s) runs here, not in the gate.
        _node("global", "ecos", "ecos", "macro-snapshot"),
        _node(code, "dart", "dart", "financial-summary", "--corp-code", corp),
        _node(code, "kis", "kis", "stock", "valuation", "--stock-code", code, "--corp-code", corp),
        _node(code, "cache", "kis", "stock", "valuation-band", "--stock-code", code, "--corp-code", corp),
        _node(code, "kis", "kis", "stock", "investor-metrics", "--stock-code", code, "--corp-code", corp),
        _node(code, "kis", "kis", "stock", "implied-expectations", "--stock-code", code, "--corp-code", corp),
        _node(code, "kis", "kis", "stock", "opinion-summary", "--stock-code", code),
        _node(code, "kis", "kis", "market", "announcement", "--stock-code", code, "--limit", "40"),
        _node(code, "kis", "kis", "chart", "technical", "--stock-code", code, "--count", "250"),
        _node(code, "kis", "kis", "chart", "trend-setup", "--stock-code", code),
        _node(code, "dart", "dart", "dilution-watch", "--corp-code", corp),
        _node(code, "dart", "dart", "company-overview", "--corp-code", corp),
        _node(
            code,
            "dart",
            "dart",
            "disclosure-search",
            "--corp-code",
            corp,
            "--bgn-de",
            year_ago,
            "--end-de",
            f"{day:%Y%m%d}",
            "--page-count",
            "100",
        ),
        _node(code, "cache", "cache", "rs", "--code", ",".join([code, *peers])),
        _node(code, "cache", "cache", "macro-beta", "--code", code),
        _node(code, "cache", "cache", "base-rate", "--code", code),
    ]
    for peer in peers:
        nodes.append(_node(peer, "dart", "dart", "corp-code-lookup", "--stock-code", peer))
        nodes.append(_node(peer, "kis", "kis", "stock", "current-price", "--stock-code", peer))
    return nodes


def _peer_nodes(peer: str, corp: str) -> list[Node]:
    return [
        _node(peer, "dart", "dart", "financial-summary", "--corp-code", corp),
        _node(peer, "kis", "kis", "stock", "valuation", "--stock-code", peer, "--corp-code", corp),
        _node(peer, "cache", "kis", "stock", "valuation-band", "--stock-code", peer, "--corp-code", corp),
        _node(peer, "kis", "kis", "stock", "investor-metrics", "--stock-code", peer, "--corp-code", corp),
        _node(peer, "kis", "kis", "chart", "technical", "--stock-code", peer, "--count", "250"),
        _node(peer, "kis", "kis", "chart", "trend-setup", "--stock-code", peer),
        _node(peer, "dart", "dart", "dilution-watch", "--corp-code", corp),
    ]


# ---------------------------------------------------------------- reading earlier answers


def corp_code_of(payload: Any) -> str | None:
    rows = payload.get("data") if isinstance(payload, dict) else None
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        value = rows[0].get("corp_code")
        return str(value) if value else None
    return None


def induty_code_of(payload: Any) -> str | None:
    if isinstance(payload, dict):
        value = payload.get("induty_code")
        return str(value) if value else None
    return None


def latest_periodic_of(payload: Any) -> str | None:
    """rcept_no of the newest 사업·반기·분기보고서 in a disclosure-search reply (DART lists newest first)."""

    result = payload.get("result") if isinstance(payload, dict) else None
    rows = result.get("list") if isinstance(result, dict) else None
    for row in rows if isinstance(rows, list) else []:
        name = str(row.get("report_nm", ""))
        if any(kind in name for kind in _PERIODIC):
            return str(row.get("rcept_no")) or None
    return None


def latest_report_of(payload: Any) -> tuple[str, str] | None:
    """(bsns_year, reprt_code) of the newest report financial-summary used."""

    reports = payload.get("reports") if isinstance(payload, dict) else None
    if isinstance(reports, list) and reports and isinstance(reports[-1], dict):
        last = reports[-1]
        if last.get("year") and last.get("reprt_code"):
            return str(last["year"]), str(last["reprt_code"])
    return None


def _stage2(
    code: str, corp: str, by_id: dict[str, NodeResult], peer_corps: dict[str, str]
) -> tuple[list[Node], list[dict[str, str]]]:
    nodes: list[Node] = []
    skipped: list[dict[str, str]] = []

    def payload(stem: str) -> Any:
        hit = by_id.get(f"{code}__{stem}")
        return hit.payload() if hit and hit.exit_code == 0 else None

    induty = induty_code_of(payload("dart-company-overview"))
    if induty:
        nodes.append(_node("global", "ecos", "ecos", "industry-outlook", "--induty-code", induty))
    else:
        skipped.append({"node": "global__ecos-industry-outlook", "reason": "company-overview gave no induty_code"})

    rcept = latest_periodic_of(payload("dart-disclosure-search"))
    if rcept:
        nodes.append(
            _node(
                code,
                "dart",
                "dart",
                "document-section",
                "--corp-code",
                corp,
                "--rcept-no",
                rcept,
                "--section",
                "business",
                "--max-chars",
                "0",
            )  # fmt: skip
        )
        nodes.append(
            _node(
                code,
                "dart",
                "dart",
                "financial-notes",
                "--corp-code",
                corp,
                "--rcept-no",
                rcept,
                "--title-contains",
                _NOTE_TITLES,
            )  # fmt: skip
        )
    else:
        skipped.append({"node": f"{code}__dart-document-section", "reason": "no periodic report in the last year"})
        skipped.append({"node": f"{code}__dart-financial-notes", "reason": "no periodic report in the last year"})

    report = latest_report_of(payload("dart-financial-summary"))
    if report:
        year, reprt = report
        for cls in _INDICATOR_CLASSES:
            nodes.append(
                _node(
                    code,
                    "dart",
                    "dart",
                    "financial-major-indicators",
                    "--corp-code",
                    corp,
                    "--bsns-year",
                    year,
                    "--reprt-code",
                    reprt,
                    "--idx-cl-code",
                    cls,
                    suffix=cls,
                )  # fmt: skip
            )
    else:
        skipped.append({"node": f"{code}__dart-financial-major-indicators", "reason": "financial-summary failed"})

    for peer, peer_corp in peer_corps.items():
        nodes.extend(_peer_nodes(peer, peer_corp))
    return nodes, skipped


# ---------------------------------------------------------------- running


def _now() -> str:
    return datetime.now(KST).isoformat(timespec="seconds")


def _retryable(exit_code: int, stdout: str) -> bool:
    if exit_code not in _RETRY_EXITS:
        return False
    try:
        error = json.loads(stdout).get("error", {})
    except (ValueError, AttributeError):
        return True
    return bool(error.get("retryable", exit_code == 5))


class _Executor:
    def __init__(self, runner: Runner, out: Path, sleep: Callable[[float], None]) -> None:
        self._runner = runner
        self._out = out
        self._sleep = sleep
        self._locks = {broker: threading.Semaphore(limit) for broker, limit in BROKER_LIMITS.items()}
        self._manifest_lock = threading.Lock()

    def run_one(self, node: Node) -> NodeResult:
        started = _now()
        attempts = 0
        exit_code, stdout, stderr = 1, "", ""
        with self._locks.get(node.broker, threading.Semaphore(1)):
            while attempts < _MAX_ATTEMPTS:
                attempts += 1
                exit_code, stdout, stderr = self._runner(list(node.argv))
                if not _retryable(exit_code, stdout) or attempts == _MAX_ATTEMPTS:
                    break
                self._sleep(_BACKOFF_SECONDS * attempts)
        result = NodeResult(node, exit_code, stdout, stderr, attempts, started, _now())
        self._record(result)
        return result

    def run_stage(self, nodes: Iterable[Node]) -> list[NodeResult]:
        nodes = list(nodes)
        if not nodes:
            return []
        workers = max(1, min(len(nodes), sum(BROKER_LIMITS.values())))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(self.run_one, nodes))

    def _record(self, result: NodeResult) -> None:
        file = self._out / "raw" / f"{result.node.id}.json"
        file.write_text(result.stdout, encoding="utf-8")
        line = {
            "node": result.node.id,
            "subject": result.node.subject,
            "command": result.node.command,
            "argv": list(result.node.argv),
            "exit_code": result.exit_code,
            "attempts": result.attempts,
            "started": result.started,
            "ended": result.ended,
            "file": str(file.relative_to(self._out)),
            "bytes": len(result.stdout.encode("utf-8")),
            "stderr": result.stderr[-2000:],
        }
        with self._manifest_lock, (self._out / "manifest.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def _stop_hit(results: Iterable[NodeResult]) -> NodeResult | None:
    """The first kis/dart call that exited 3 (credentials) — the agent file says stop there."""

    return next((r for r in results if r.exit_code == 3 and r.node.path[0] in _STOP_BROKERS), None)


def collect(
    stock_code: str,
    peers: list[str],
    out: Path,
    *,
    runner: Runner = subprocess_runner,
    day: date | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> CollectResult:
    day = day or today_kst()
    (out / "raw").mkdir(parents=True, exist_ok=True)
    ex = _Executor(runner, out, sleep)
    results: list[NodeResult] = []
    skipped: list[dict[str, str]] = []

    def finish(status: str, stopped: NodeResult | None, corps: dict[str, str]) -> CollectResult:
        stopped_by = None
        if stopped is not None:
            stopped_by = {"node": stopped.node.id, "command": stopped.node.command, "exit_code": stopped.exit_code}
        return CollectResult(out, status, tuple(results), tuple(skipped), stopped_by, corps)

    results += ex.run_stage(_gate_first(stock_code))
    results += ex.run_stage(_gate_rest(stock_code))
    stopped = _stop_hit(results)
    if stopped is not None:
        return finish("stopped", stopped, {})
    by_id = {r.node.id: r for r in results}
    lookup = by_id.get(f"{stock_code}__dart-corp-code-lookup")
    corp = corp_code_of(lookup.payload()) if lookup and lookup.exit_code == 0 else None
    if corp is None:
        skipped.append({"node": f"{stock_code}__*", "reason": "no corp_code for the stock; corp-code commands skipped"})
        return finish("stopped", lookup, {})

    results += ex.run_stage(_stage1(stock_code, corp, peers, day))
    stopped = _stop_hit(results)
    if stopped is not None:
        return finish("stopped", stopped, {stock_code: corp})
    by_id = {r.node.id: r for r in results}
    corps = {stock_code: corp}
    peer_corps: dict[str, str] = {}
    for peer in peers:
        hit = by_id.get(f"{peer}__dart-corp-code-lookup")
        peer_corp = corp_code_of(hit.payload()) if hit and hit.exit_code == 0 else None
        if peer_corp:
            peer_corps[peer] = peer_corp
            corps[peer] = peer_corp
        else:
            skipped.append({"node": f"{peer}__*", "reason": "no corp_code for the peer; its data was not fetched"})

    stage2, skipped2 = _stage2(stock_code, corp, by_id, peer_corps)
    skipped += skipped2
    results += ex.run_stage(stage2)
    stopped = _stop_hit(results)
    if stopped is not None:
        return finish("stopped", stopped, corps)
    status = "ok" if all(r.exit_code == 0 for r in results) and not skipped else "partial"
    return finish(status, None, corps)
