"""`review collect` runs the company-review fetch graph; `record` and `track` keep and check its verdicts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cliargs import _parse_named_options, _str_option
from cluefin_openapi_cli.clock import today_kst
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.output import render_output
from cluefin_openapi_cli.review.checklist import RULES_FILE, evaluate, init_rules_file, load_rules
from cluefin_openapi_cli.review.collect import (
    CollectResult,
    add_peers,
    collect,
    default_root,
    process_runner,
    read_run_info,
    run_dir,
)
from cluefin_openapi_cli.review.due import DEFAULT_DAYS, due, gather_events, tracked_rows
from cluefin_openapi_cli.review.metrics import catalog_rows
from cluefin_openapi_cli.review.paths import research_root
from cluefin_openapi_cli.review.record import VERDICTS_FILE, record_verdict
from cluefin_openapi_cli.review.track import load_records, track

__all__ = ["SUBCOMMANDS", "run_review", "summary"]

_CODE_RE = re.compile(r"^\d{6}$")
_MAX_PEERS = 3


def _codes(raw: str | None, flag: str) -> list[str]:
    codes = [c.strip() for c in (raw or "").split(",") if c.strip()]
    bad = [c for c in codes if not _CODE_RE.match(c)]
    if bad:
        raise CliError(f"{flag} takes 6-digit stock codes; got {', '.join(bad)}.", exit_code=EXIT_USAGE)
    return codes


def summary(result: CollectResult) -> dict[str, Any]:
    failed = [
        {"node": r.node.id, "command": r.node.command, "exit_code": r.exit_code, "attempts": r.attempts}
        for r in result.results
        if r.exit_code != 0
    ]
    return {
        "out": str(result.out),
        "status": result.status,
        "stopped_by": result.stopped_by,
        "corp_codes": result.corp_codes,
        "counts": {
            "calls": len(result.results),
            "ok": sum(1 for r in result.results if r.exit_code == 0),
            "failed": len(failed),
            "skipped": len(result.skipped),
        },
        "failed": failed,
        "skipped": list(result.skipped),
        "files": {"manifest": "manifest.jsonl", "raw": "raw/<node>.json"},
        "notes": [
            "Each raw file is the command's stdout exactly; manifest.jsonl has one line per call (argv, exit_code, "
            "attempts, file). Read the files with jq instead of calling the commands again.",
            "status ok: every call exited 0. partial: some failed or were skipped (see failed/skipped). stopped: a "
            "kis/dart call exited 3 (credentials) or the stock has no corp code — fix that before reviewing.",
        ],
    }


def _run_collect(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    into = _str_option(options, "into")
    if into:
        if _str_option(options, "stock_code") or _str_option(options, "out"):
            raise CliError("--into adds peers to a run; drop --stock-code/--out.", exit_code=EXIT_USAGE)
        peers = _codes(_str_option(options, "peers"), "--peers")
        if not peers or len(peers) > _MAX_PEERS:
            raise CliError(f"--into needs --peers with 1 to {_MAX_PEERS} codes.", exit_code=EXIT_USAGE)
        if read_run_info(Path(into)) is None:
            raise CliError(f"{into} is not a review collect folder (no run.json).", exit_code=EXIT_USAGE)
        with process_runner() as runner:
            result = add_peers(Path(into), peers, runner=runner)
        render_output(
            summary(result), force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False))
        )
        return
    codes = _codes(_str_option(options, "stock_code"), "--stock-code")
    if len(codes) != 1:
        raise CliError("review collect needs one --stock-code.", exit_code=EXIT_USAGE)
    stock = codes[0]
    peers = [p for p in _codes(_str_option(options, "peers"), "--peers") if p != stock]
    if len(peers) > _MAX_PEERS:
        raise CliError(f"--peers takes at most {_MAX_PEERS} codes.", exit_code=EXIT_USAGE)
    out_opt = _str_option(options, "out")
    out = Path(out_opt) if out_opt else run_dir(default_root(), stock, today_kst())
    if (out / "manifest.jsonl").exists():
        raise CliError(f"{out} already holds a run.", exit_code=EXIT_USAGE, hint="Pick another --out or omit it.")
    with process_runner() as runner:
        result = collect(stock, peers, out, runner=runner)
    render_output(
        summary(result), force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False))
    )


def _run_record(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    src = _str_option(options, "from")
    if not src:
        raise CliError("review record needs --from <verdict.json or its folder>.", exit_code=EXIT_USAGE)
    report = _str_option(options, "report")
    root = research_root()
    done = record_verdict(
        Path(src),
        root=root,
        source=_str_option(options, "source") or "main",
        report=Path(report) if report else None,
        today=today_kst(),
    )
    render_output(
        {"file": str(done.file), "record": done.record},
        force_json=bool(options.get("json", False)),
        compact=bool(options.get("compact", False)),
    )


def _run_track(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    records = load_records(research_root() / VERDICTS_FILE)
    codes = _codes(_str_option(options, "code"), "--code")
    if codes:
        records = [r for r in records if r["stock_code"] in codes]
    conn = store.open_store(read_only=True)
    try:
        payload = track(conn, records)
    finally:
        conn.close()
    render_output(payload, force_json=bool(options.get("json", False)), compact=bool(options.get("compact", False)))


def _run_checklist(argv: list[str]) -> None:
    _, options = _parse_named_options(argv, bool_flags={"init"})
    force_json = bool(options.get("json", False))
    compact = bool(options.get("compact", False))

    if bool(options.get("dry_run", False)):
        render_output(
            {
                "dry_run": True,
                "would": {
                    "init": bool(options.get("init", False)),
                    "metrics": _str_option(options, "metrics") == "true",
                    "rules": _str_option(options, "rules"),
                    "from": _str_option(options, "from"),
                },
            },
            force_json=force_json,
            compact=compact,
        )
        return

    if _str_option(options, "metrics") == "true":
        render_output({"metrics": catalog_rows()}, force_json=force_json, compact=compact)
        return

    rules_opt = _str_option(options, "rules")
    rules_path = Path(rules_opt) if rules_opt else research_root() / RULES_FILE
    init_flag = bool(options.get("init", False))
    if init_flag:
        init_rules_file(rules_path)

    from_opt = _str_option(options, "from")
    if not from_opt:
        if init_flag:
            render_output({"created": str(rules_path)}, force_json=force_json, compact=compact)
            return
        raise CliError(
            "review checklist needs --from <review collect folder> (or --init / --metrics true).",
            exit_code=EXIT_USAGE,
        )

    folder = Path(from_opt)
    info = read_run_info(folder)
    if info is None:
        raise CliError(f"{folder} is not a review collect folder (no run.json).", exit_code=EXIT_USAGE)
    code = str(info["stock_code"])
    rules = load_rules(rules_path)
    payload = evaluate(folder, code, rules)
    render_output(payload, force_json=force_json, compact=compact)


def _run_due(argv: list[str]) -> None:
    _, options = _parse_named_options(argv)
    force_json = bool(options.get("json", False))
    compact = bool(options.get("compact", False))
    events_flag = _str_option(options, "events") == "true"
    codes = _codes(_str_option(options, "code"), "--code")
    days_opt = _str_option(options, "days")

    if bool(options.get("dry_run", False)):
        render_output(
            {"dry_run": True, "would": {"days": days_opt, "code": codes, "events": events_flag}},
            force_json=force_json,
            compact=compact,
        )
        return

    if days_opt is not None:
        try:
            days = int(days_opt)
        except ValueError as exc:
            raise CliError(f"--days must be an integer, got {days_opt!r}.", exit_code=EXIT_USAGE) from exc
        if days <= 0:
            raise CliError("--days must be a positive integer.", exit_code=EXIT_USAGE)
    else:
        days = DEFAULT_DAYS

    records = load_records(research_root() / VERDICTS_FILE)
    conn = store.open_store(read_only=True)
    try:
        rows, cache_as_of = tracked_rows(conn, records, codes=codes)
        today = today_kst()
        payload = due(rows, cache_as_of, days=days, today=today)
        if events_flag:
            with process_runner() as runner:
                payload["events"] = gather_events(runner, conn, rows, days=days, today=today)
    finally:
        conn.close()
    render_output(payload, force_json=force_json, compact=compact)


SUBCOMMANDS = {
    "collect": _run_collect,
    "record": _run_record,
    "track": _run_track,
    "checklist": _run_checklist,
    "due": _run_due,
}


def run_review(argv: list[str]) -> None:
    if not argv or argv[0] not in SUBCOMMANDS:
        raise CliError(
            f"`review` takes one of: {', '.join(SUBCOMMANDS)}.",
            exit_code=EXIT_USAGE,
            data={"subcommands": list(SUBCOMMANDS)},
        )
    SUBCOMMANDS[argv[0]](argv[1:])
