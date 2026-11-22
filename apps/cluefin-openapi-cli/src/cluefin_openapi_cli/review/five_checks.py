"""`review five-checks`: company-review's five checks judged from one `review collect` folder, deterministically.

The agent used to compute these by hand from raw files (4-quarter sums, margin deltas, FCF signs). The thresholds are
the agent's table, moved here unchanged; the agent now reads `five_checks.json` and only explains it. Like
`metrics.py`, nothing is re-derived that another command already computed — inputs are read from
`dart financial-summary` and `kis stock valuation` raw files.

Each item is 좋음 / 주의 / 보통 / 판정 보류. A caution condition wins as soon as the inputs it needs are present, even
when the inputs for 좋음 are missing; otherwise a missing input gives 판정 보류 with a reason. Only the stock under
review is judged — peers are compared in the agent's peer table, not here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.review.metrics import compute, read_raw

__all__ = ["FIVE_CHECKS_FILE", "evaluate_five_checks"]

FIVE_CHECKS_FILE = "five_checks.json"

GOOD, CAUTION, NEUTRAL, PENDING = "좋음", "주의", "보통", "판정 보류"

_FS = "dart-financial-summary"
_VALUATION = "kis-stock-valuation"

# `statements.growth` gives a string when a side is not positive: revenue that turned to zero or below is a fall.
_GROWTH_SIGN = {"흑전": 1.0, "적전": -1.0}


@dataclass(frozen=True, slots=True)
class Check:
    item: str
    label: str
    rule: str
    result: str
    inputs: dict[str, Any]
    reason: str | None = None


def _get(payload: Any, *path: Any) -> Any:
    node = payload
    for key in path:
        if isinstance(node, dict):
            node = node.get(key)
        elif isinstance(node, list) and isinstance(key, int) and -len(node) <= key < len(node):
            node = node[key]
        else:
            return None
    return node


def _num(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else None


def _growth(value: Any) -> float | None:
    if isinstance(value, str):
        return _GROWTH_SIGN.get(value)
    return _num(value)


def _neg(value: float | None) -> bool:
    return value is not None and value < 0


def _judge(caution: bool, good: bool | None) -> str:
    """`good` is None when its inputs are missing."""

    if caution:
        return CAUTION
    if good is None:
        return PENDING
    return GOOD if good else NEUTRAL


def _growth_check(fs: Any, yoy_4q: float | None) -> Check:
    quarters = _get(fs, "quarters") or []
    last = _growth(_get(quarters, -1, "yoy", "revenue"))
    before = _growth(_get(quarters, -2, "yoy", "revenue"))
    caution = _neg(yoy_4q) or (_neg(last) and _neg(before))
    good = None if yoy_4q is None or last is None else yoy_4q >= 10 and last >= 0
    return Check(
        "growth",
        "성장",
        "좋음: 4분기 매출 YoY ≥ 10% 이고 최근 분기 YoY ≥ 0. 주의: 4분기 YoY < 0, 또는 최근 2개 분기 연속 YoY < 0",
        _judge(caution, good),
        {
            "revenue_yoy_4q": yoy_4q,
            "last_quarter": _get(quarters, -1, "period"),
            "last_quarter_yoy": _get(quarters, -1, "yoy", "revenue"),
            "prior_quarter_yoy": _get(quarters, -2, "yoy", "revenue"),
        },
        None if good is not None or caution else "4분기 매출 YoY 또는 최근 분기 YoY 가 없다",
    )


def _profit_check(fs: Any, opm: float | None) -> Check:
    ttm_oi = _num(_get(fs, "ttm", "operating_income"))
    prior = _num(_get(fs, "annual", -1, "opm"))
    dropped = opm is not None and prior is not None and opm < prior - 2
    caution = _neg(ttm_oi) or (opm is not None and opm < 5) or dropped
    good = None if opm is None or prior is None else opm >= 10 and not dropped
    return Check(
        "profitability",
        "수익성",
        "좋음: TTM 영업이익률 ≥ 10% 이고 직전 연도보다 2%p 넘게 낮지 않음. 주의: TTM 영업적자, 영업이익률 < 5%, "
        "또는 직전 연도보다 2%p 넘게 하락",
        _judge(caution, good),
        {
            "opm_ttm": opm,
            "operating_income_ttm": ttm_oi,
            "opm_prior_year": prior,
            "prior_year": _get(fs, "annual", -1, "year"),
        },
        None if good is not None or caution else "TTM 영업이익률 또는 직전 연도 영업이익률이 없다",
    )


def _cash_check(fs: Any) -> Check:
    years = (_get(fs, "annual") or [])[-3:]
    annual_fcf = [_num(_get(y, "free_cash_flow")) for y in years]
    latest_fcf = _num(_get(fs, "latest", "free_cash_flow"))
    latest_ocf = _num(_get(fs, "latest", "operating_cash_flow"))
    prior_fcf = annual_fcf[-1] if annual_fcf else None
    caution = (_neg(latest_fcf) and _neg(prior_fcf)) or _neg(latest_ocf)
    values = [*annual_fcf, latest_fcf]
    complete = len(annual_fcf) == 3 and all(v is not None for v in values)
    good = all(v >= 0 for v in values if v is not None) if complete else None
    return Check(
        "cash",
        "현금",
        "좋음: 최근 3개 연도와 최근 누적의 FCF 가 모두 ≥ 0. 주의: 최근 누적 FCF < 0 이고 직전 연도 FCF < 0, "
        "또는 최근 누적 영업CF < 0",
        _judge(caution, good),
        {
            "annual_fcf": [
                {"year": _get(y, "year"), "free_cash_flow": v} for y, v in zip(years, annual_fcf, strict=True)
            ],
            "latest_period": _get(fs, "latest", "period"),
            "latest_fcf": latest_fcf,
            "latest_operating_cash_flow": latest_ocf,
        },
        None if good is not None or caution else "3개 연도 또는 최근 누적 FCF 중 빈 값이 있다",
    )


def _debt_check(fs: Any) -> Check:
    net_debt = _num(_get(fs, "latest", "net_debt"))
    coverage = _num(_get(fs, "latest", "interest_coverage"))
    ratio = _num(_get(fs, "latest", "net_debt_ratio"))
    caution = (coverage is not None and coverage < 3) or (ratio is not None and ratio > 200)
    good = None if net_debt is None else net_debt <= 0
    return Check(
        "debt",
        "빚",
        "좋음: 순현금(순차입금 ≤ 0). 주의: 최근 누적 이자보상배율 < 3배, 또는 순차입금비율 > 200%",
        _judge(caution, good),
        {"net_debt": net_debt, "interest_coverage": coverage, "net_debt_ratio": ratio},
        None if good is not None or caution else "순차입금이 없다(차입금 또는 현금 계정 미보고)",
    )


def _price_check(fs: Any, per: float | None) -> Check:
    ttm_ni = _num(_get(fs, "ttm", "net_income_owners"))
    # KIS reports a loss-making TTM as a zero or negative PER.
    loss = _neg(ttm_ni) or (per is not None and per <= 0)
    caution = loss or (per is not None and per >= 30)
    good = None if per is None else per < 10
    return Check(
        "price",
        "가격",
        "좋음: TTM PER < 10배. 주의: TTM 적자, 또는 TTM PER ≥ 30배",
        _judge(caution, good),
        {"per_ttm": per, "net_income_owners_ttm": ttm_ni},
        None if good is not None or caution else "TTM PER 이 없다",
    )


def _row(check: Check) -> dict[str, Any]:
    row: dict[str, Any] = {
        "item": check.item,
        "label": check.label,
        "result": check.result,
        "rule": check.rule,
        "inputs": check.inputs,
    }
    if check.reason is not None:
        row["reason"] = check.reason
    return row


def evaluate_five_checks(folder: Path, code: str) -> dict[str, Any]:
    """Judge the five checks for `code` and write `<folder>/five_checks.json`."""

    fs = read_raw(folder, code, _FS)
    yoy_4q = compute(folder, code, "revenue_yoy_4q")
    opm = compute(folder, code, "opm_ttm")
    per = compute(folder, code, "per_ttm")
    checks = [
        _growth_check(fs, _num(yoy_4q.value)),
        _profit_check(fs, _num(opm.value)),
        _cash_check(fs),
        _debt_check(fs),
        _price_check(fs, _num(per.value)),
    ]
    missing = [stem for stem in (_FS, _VALUATION) if read_raw(folder, code, stem) is None]
    payload = {
        "stock_code": code,
        "as_of": {"financial": _get(fs, "as_of"), "valuation": per.as_of},
        "checks": [_row(c) for c in checks],
        "summary": {label: sum(1 for c in checks if c.result == label) for label in (GOOD, CAUTION, NEUTRAL, PENDING)},
        "missing_raw": missing,
        "notes": [
            "판단을 계산하는 점수가 아니라 판단을 설명하는 표다. 주의 조건이 하나라도 맞으면 주의가 앞선다.",
            "금액은 억원, 비율은 %. 4분기 매출 YoY·TTM 영업이익률은 review checklist 의 revenue_yoy_4q·opm_ttm 과 같은 값이다.",
        ],
    }
    (folder / FIVE_CHECKS_FILE).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
