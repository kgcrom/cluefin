"""`review checklist`: compare my own rules against one `review collect` folder, deterministically.

Rules live in `research/principles.toml` (gitignored, mine — never shipped with an example of real thresholds) as
``[[rule]] id, label, metric, op, value, must``. `metric` must be one of `metrics.CATALOG`; `op` is one of
`<`/`<=`/`>`/`>=`/`=`/`!=`, except a string metric (`setup_group`) only allows `=`/`!=`. Every rule file problem
(unknown metric, unknown op, wrong value type for the op) is collected and reported together — one fix round, not
one error at a time.

No score, no verdict: each rule gets `pass`/`fail`/`unknown` and the measured value sits next to the threshold so a
person can see why. `must` only marks which failures matter to the summary (`must_failed`) — it does not change the
per-rule result.
"""

from __future__ import annotations

import json
import operator
import tomllib
from collections.abc import Callable
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.review.metrics import CATALOG, compute

__all__ = [
    "CHECKLIST_FILE",
    "RULES_FILE",
    "evaluate",
    "init_rules_file",
    "load_rules",
]

RULES_FILE = "principles.toml"
CHECKLIST_FILE = "checklist.json"

_OPS: dict[str, Callable[[Any, Any], bool]] = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "=": operator.eq,
    "!=": operator.ne,
}
_STRING_OPS = frozenset({"=", "!="})

_EXAMPLE_TOML = """\
# research/principles.toml — 내 투자 기준표. `review checklist --from <수집 폴더>` 가 raw 파일과 대조한다.
# 아래 규칙은 예시다 — 점수나 매수 신호가 아니라 자기 기준으로 고쳐 쓰는 표다. 지우거나 더해도 된다.
#
# [[rule]]
# id    : 규칙 하나의 짧은 이름. checklist.json·must_failed 에서 이 이름으로 나온다.
# label : 사람이 읽을 설명.
# metric: `review checklist --metrics true` 가 내는 카탈로그 이름 하나.
# op    : <, <=, >, >=, =, != 중 하나. 문자열 metric(setup_group)은 =, != 만 된다.
# value : 문턱값(숫자 또는 문자열).
# must  : true 면 이 규칙이 fail 일 때 summary.must_failed 에 올라간다. 생략하면 false.

[[rule]]
id = "roe_min"
label = "ROE 15% 이상"
metric = "roe"
op = ">="
value = 15

[[rule]]
id = "per_cheap"
label = "TTM PER 15배 이하"
metric = "per_ttm"
op = "<="
value = 15

[[rule]]
id = "not_too_levered"
label = "순차입금비율 100% 이하(순현금이면 음수)"
metric = "net_debt_ratio"
op = "<="
value = 100
must = true

[[rule]]
id = "no_heavy_dilution"
label = "최근 3년 희석 10% 이하"
metric = "dilution_3y_pct"
op = "<="
value = 10

[[rule]]
id = "setup_ready"
label = "추세 셋업이 '없음'이 아님"
metric = "setup_group"
op = "!="
value = "none"
"""


def init_rules_file(path: Path) -> None:
    if path.exists():
        raise CliError(
            f"{path} already exists.", exit_code=EXIT_USAGE, hint="Edit it directly, or pick another --rules path."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_EXAMPLE_TOML, encoding="utf-8")


def _rule_issues(rule: Any, index: int) -> list[str]:
    prefix = f"rule[{index}]"
    if not isinstance(rule, dict):
        return [f"{prefix}: must be a [[rule]] table"]
    rid = rule.get("id")
    tag = f"{prefix} (id={rid!r})" if isinstance(rid, str) and rid else prefix
    issues: list[str] = []
    if not isinstance(rid, str) or not rid.strip():
        issues.append(f"{prefix}: id must be a non-empty string")
    if not isinstance(rule.get("label"), str) or not rule["label"].strip():
        issues.append(f"{tag}: label must be a non-empty string")
    metric = rule.get("metric")
    if metric not in CATALOG:
        issues.append(f"{tag}: unknown metric {metric!r} (see `review checklist --metrics true`)")
        return issues  # op/value type depend on the metric's kind, which we don't have
    spec = CATALOG[metric]
    op = rule.get("op")
    if op not in _OPS:
        issues.append(f"{tag}: unknown op {op!r} (use one of {', '.join(_OPS)})")
    elif spec.kind == "string" and op not in _STRING_OPS:
        issues.append(f"{tag}: {metric!r} is a string metric — only = / != are allowed, not {op!r}")
    value = rule.get("value")
    if spec.kind == "string":
        if not isinstance(value, str):
            issues.append(f"{tag}: value must be a string for metric {metric!r}")
    elif not isinstance(value, int | float) or isinstance(value, bool):
        issues.append(f"{tag}: value must be a number for metric {metric!r}")
    must = rule.get("must", False)
    if not isinstance(must, bool):
        issues.append(f"{tag}: must must be true or false")
    return issues


def load_rules(path: Path) -> list[dict[str, Any]]:
    """Every `[[rule]]` in ``path``, validated all at once — a bad rule file names every problem together."""

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CliError(
            f"No rules file at {path}.", exit_code=EXIT_USAGE, hint="Create one with `review checklist --init`."
        ) from exc
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise CliError(f"{path} is not valid TOML: {exc}.", exit_code=EXIT_USAGE) from exc
    rules = data.get("rule")
    if not isinstance(rules, list) or not rules:
        raise CliError(f"{path} has no [[rule]] entries.", exit_code=EXIT_USAGE)
    issues: list[str] = []
    for index, rule in enumerate(rules):
        issues.extend(_rule_issues(rule, index))
    if issues:
        raise CliError("The rules file has invalid entries.", exit_code=EXIT_USAGE, data={"issues": issues})
    return rules


def evaluate(folder: Path, code: str, rules: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    counts = {"passed": 0, "failed": 0, "unknown": 0}
    must_failed: list[str] = []
    for rule in rules:
        result = compute(folder, code, rule["metric"])
        row: dict[str, Any] = {
            "id": rule["id"],
            "label": rule["label"],
            "metric": rule["metric"],
            "op": rule["op"],
            "threshold": rule["value"],
            "value": result.value,
            "as_of": result.as_of,
        }
        if result.value is None:
            row["result"] = "unknown"
            row["reason"] = result.reason
            counts["unknown"] += 1
        else:
            passed = _OPS[rule["op"]](result.value, rule["value"])
            row["result"] = "pass" if passed else "fail"
            counts["passed" if passed else "failed"] += 1
            if not passed and rule.get("must", False):
                must_failed.append(rule["id"])
        rows.append(row)
    payload = {
        "stock_code": code,
        "rules": rows,
        "summary": {**counts, "must_failed": must_failed},
        "notes": [
            "값·결과만 낸다 — 점수나 매수/매도 라벨은 없다. unknown 은 raw 파일이 없거나 그 계정을 안 쓴 회사(reason 참고).",
        ],
    }
    (folder / CHECKLIST_FILE).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
