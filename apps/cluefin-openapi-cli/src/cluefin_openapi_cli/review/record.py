"""`review record`: append one review verdict to `research/verdicts.jsonl` so it can be checked against prices later.

A verdict lives in a run folder under /tmp or only inside an HTML report, so nothing could be tracked once the
session ended. Each verdict becomes one line here; lines are never rewritten. `review track` reads this file.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = [
    "SOURCES",
    "VERDICTS_FILE",
    "Recorded",
    "build_record",
    "load_verdict",
    "read_records",
    "record_verdict",
    "validate",
]

VERDICTS_FILE = "verdicts.jsonl"
VERDICT_FILE = "verdict.json"
SOURCES = ("main", "company-review")
_VERDICTS = ("buy", "hold", "sell", "watch")
_CONFIDENCE = ("low", "medium", "high")
_CODE_RE = re.compile(r"^\d{6}$")


@dataclass(frozen=True, slots=True)
class Recorded:
    record: dict[str, Any]
    file: Path


def _is_price(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and value > 0


def _is_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def load_verdict(src: Path) -> dict[str, Any]:
    """`src` is a verdict.json, or a folder holding one."""

    path = src / VERDICT_FILE if src.is_dir() else src
    if not path.is_file():
        raise CliError(f"{path} does not exist.", exit_code=EXIT_USAGE)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CliError(f"{path} is not valid JSON: {exc}.", exit_code=EXIT_USAGE) from exc
    if not isinstance(data, dict):
        raise CliError(f"{path} must hold one JSON object.", exit_code=EXIT_USAGE)
    return data


def _price_problems(verdict: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    ref = verdict.get("reference_price")
    if not isinstance(ref, dict) or not _is_price(ref.get("close")) or not _is_date(ref.get("date")):
        problems.append("reference_price needs close (> 0) and date (YYYY-MM-DD)")
    elif not isinstance(ref.get("adjusted"), bool):
        problems.append("reference_price.adjusted must be true or false")
    label = verdict.get("verdict")
    if label in ("watch", "hold"):
        trigger = verdict.get("trigger")
        if not isinstance(trigger, dict) or not any(_is_price(trigger.get(k)) for k in ("entry_above", "exit_below")):
            problems.append(f"{label} needs trigger.entry_above or trigger.exit_below (> 0)")
        elif trigger.get("recheck_on") is not None and not _is_date(trigger.get("recheck_on")):
            problems.append("trigger.recheck_on must be YYYY-MM-DD")
    if label in ("buy", "sell"):
        problems.extend(f"{label} needs {k} (> 0)" for k in ("target", "stop") if not _is_price(verdict.get(k)))
    return problems


def validate(verdict: dict[str, Any]) -> list[str]:
    """Every problem at once, so one fix round is enough."""

    problems: list[str] = []
    if not isinstance(verdict.get("stock_code"), str) or not _CODE_RE.match(verdict["stock_code"]):
        problems.append('stock_code must be a 6-digit string ("030000", not 30000)')
    if not isinstance(verdict.get("stock_name"), str) or not verdict["stock_name"].strip():
        problems.append("stock_name is required")
    if verdict.get("verdict") not in _VERDICTS:
        problems.append(f"verdict must be one of {', '.join(_VERDICTS)}")
    if verdict.get("confidence") not in _CONFIDENCE:
        problems.append(f"confidence must be one of {', '.join(_CONFIDENCE)}")
    horizon = verdict.get("horizon_days")
    if not isinstance(horizon, int) or isinstance(horizon, bool) or horizon <= 0:
        problems.append("horizon_days must be a positive integer (trading days)")
    invalidation = verdict.get("invalidation", [])
    if not isinstance(invalidation, list) or not all(isinstance(x, str) for x in invalidation):
        problems.append("invalidation must be a list of strings")
    return problems + _price_problems(verdict)


def read_records(file: Path) -> list[dict[str, Any]]:
    """Every line of the verdict log; a hand-edited broken line is a usage error naming its line number."""

    records: list[dict[str, Any]] = []
    for number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise CliError(f"{file} line {number} is not valid JSON: {exc}.", exit_code=EXIT_USAGE) from exc
    return records


def _existing_ids(file: Path) -> set[str]:
    return {r.get("id", "") for r in read_records(file)} if file.is_file() else set()


def _next_id(existing: set[str], code: str, ref_date: str) -> str:
    stem = f"{code}-{ref_date.replace('-', '')}"
    n = 1
    while f"{stem}-{n}" in existing:
        n += 1
    return f"{stem}-{n}"


def build_record(
    verdict: dict[str, Any], *, record_id: str, source: str, report: str | None, recorded_at: date
) -> dict[str, Any]:
    trigger = verdict.get("trigger") or {}
    return {
        "id": record_id,
        "stock_code": verdict["stock_code"],
        "stock_name": verdict["stock_name"],
        "recorded_at": recorded_at.isoformat(),
        "source": source,
        "report": report,
        "verdict": verdict["verdict"],
        "confidence": verdict["confidence"],
        "horizon_days": verdict["horizon_days"],
        "reference_price": {k: verdict["reference_price"][k] for k in ("close", "date", "adjusted")},
        "trigger": {k: trigger.get(k) for k in ("entry_above", "exit_below", "recheck_on")},
        "target": verdict.get("target"),
        "stop": verdict.get("stop"),
        "invalidation": list(verdict.get("invalidation", [])),
    }


def _report_path(report: Path | None, root: Path) -> str | None:
    if report is None:
        return None
    resolved = report.expanduser().resolve()
    if not resolved.is_file():
        raise CliError(f"--report {report} does not exist.", exit_code=EXIT_USAGE)
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise CliError(
            f"--report must be under {root} so the link survives.",
            exit_code=EXIT_USAGE,
            hint=f"Move it to {root / 'reports'} first.",
        ) from exc


def record_verdict(src: Path, *, root: Path, source: str, report: Path | None, today: date) -> Recorded:
    if source not in SOURCES:
        raise CliError(f"--source must be one of {', '.join(SOURCES)}.", exit_code=EXIT_USAGE)
    verdict = load_verdict(src)
    problems = validate(verdict)
    if problems:
        raise CliError(
            "The verdict is missing or has invalid fields.", exit_code=EXIT_USAGE, data={"problems": problems}
        )
    report_rel = _report_path(report, root)
    file = root / VERDICTS_FILE
    record_id = _next_id(_existing_ids(file), verdict["stock_code"], verdict["reference_price"]["date"])
    record = build_record(verdict, record_id=record_id, source=source, report=report_rel, recorded_at=today)
    root.mkdir(parents=True, exist_ok=True)
    with file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return Recorded(record=record, file=file)
