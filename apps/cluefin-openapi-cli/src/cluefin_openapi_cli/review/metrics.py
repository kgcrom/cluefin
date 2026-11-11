"""The metric catalog `review checklist` compares a rule against.

Every metric reads **one** `review collect` raw file (`<out>/raw/<code>__<stem>.json`) and reads a field this app's
other commands already computed — nothing here recomputes a ratio or re-derives a rule (the same discipline as
`quality.py`/`investor_metrics.py`). A missing raw file, a failed call, or a field the filer didn't report all come
back as ``value=None`` with a ``reason`` — never 0.

Field paths were checked against a real `review collect` run (2026-11-11, one large-cap manufacturer; metric values
and the company itself are not named anywhere in code or tests — only the shape of the JSON matters here).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cluefin_openapi_cli.cache.baserate import _STATUS_TO_STATE  # the one place that maps trend-setup status -> group

__all__ = ["CATALOG", "STRING_METRICS", "MetricResult", "catalog_rows", "compute", "raw_path", "read_raw"]


@dataclass(frozen=True, slots=True)
class MetricResult:
    value: Any
    as_of: str | None
    reason: str | None = None


# A `review checklist` rule may only compare a string metric with `=`/`!=` (never `<`/`>`/...).
STRING_METRICS = frozenset({"setup_group"})

# `kis chart technical`'s `stop_sizing.levels` holds one width per horizon; a single-value metric needs one pick —
# the shortest horizon (20 trading days) is the one a checklist gates entries on, not a multi-month forecast.
_STOP_WIDTH_HORIZON_DAYS = 20


def _get(payload: Any, *path: str) -> Any:
    node = payload
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def _as_of(payload: Any, fallback_key: str = "as_of") -> str | None:
    value = _get(payload, fallback_key)
    return str(value) if value else None


def _reason(payload: Any, *path: str) -> str | None:
    value = _get(payload, *path)
    return str(value) if value else None


def _financial_summary_metric(
    field_path: tuple[str, ...], *, reason_path: tuple[str, ...] = ()
) -> Callable[[Any], MetricResult]:
    def extract(payload: Any) -> MetricResult:
        value = _get(payload, *field_path)
        as_of = _as_of(payload)
        if value is None:
            reason = _reason(payload, *reason_path) if reason_path else "statement does not report this account"
            return MetricResult(None, as_of, reason)
        return MetricResult(value, as_of)

    return extract


def _quality_year(payload: Any, *path: str) -> Any:
    years = _get(payload, "quality", "years")
    if not isinstance(years, list) or not years:
        return None
    return _get(years[-1], *path)


def _extract_revenue_yoy_4q(payload: Any) -> MetricResult:
    quarters = _get(payload, "quarters")
    as_of = _as_of(payload)
    if not isinstance(quarters, list) or len(quarters) < 8:
        return MetricResult(None, as_of, "fewer than 8 quarters of revenue in financial-summary")
    revenues = [q.get("revenue") for q in quarters[-8:]]
    if any(r is None for r in revenues):
        return MetricResult(None, as_of, "a quarter's revenue is missing")
    prior4, last4 = sum(revenues[:4]), sum(revenues[4:])
    if prior4 == 0:
        return MetricResult(None, as_of, "the prior 4 quarters summed to 0")
    return MetricResult(round((last4 / prior4 - 1) * 100, 4), as_of)


def _extract_opm_ttm(payload: Any) -> MetricResult:
    revenue, operating_income = _get(payload, "ttm", "revenue"), _get(payload, "ttm", "operating_income")
    as_of = _as_of(payload)
    if revenue is None or operating_income is None or revenue == 0:
        return MetricResult(None, as_of, "ttm revenue or operating_income missing")
    return MetricResult(round(operating_income / revenue * 100, 4), as_of)


def _extract_roe(payload: Any) -> MetricResult:
    value = _quality_year(payload, "dupont", "roe_reported")
    as_of = _as_of(payload)
    if value is None:
        return MetricResult(None, as_of, "roe_reported missing (no reported ROE for the latest year)")
    return MetricResult(value, as_of)


def _extract_roic(payload: Any) -> MetricResult:
    value = _quality_year(payload, "roic", "value")
    as_of = _as_of(payload)
    if value is None:
        return MetricResult(None, as_of, "quality.years[-1].roic missing")
    return MetricResult(value, as_of)


def _extract_f_score(payload: Any) -> MetricResult:
    value = _get(payload, "quality", "f_score", "total")
    as_of = _as_of(payload)
    if value is None:
        return MetricResult(None, as_of, "quality.f_score missing")
    return MetricResult(value, as_of)


def _extract_altman_z2(payload: Any) -> MetricResult:
    value = _quality_year(payload, "altman_z_double_prime", "value")
    as_of = _as_of(payload)
    if value is None:
        return MetricResult(None, as_of, "quality.years[-1].altman_z_double_prime missing")
    return MetricResult(value, as_of)


def _extract_dilution_3y_pct(payload: Any) -> MetricResult:
    rows = _get(payload, "rows")
    as_of = str(_get(payload, "end_de") or "") or None
    if not isinstance(rows, list):
        return MetricResult(None, as_of, "dilution-watch rows missing")
    positive = [r.get("pct_of_shares") for r in rows if isinstance(r, dict) and (r.get("pct_of_shares") or 0) > 0]
    return MetricResult(round(sum(positive), 6), as_of)


def _extract_investor_metric(field: str) -> Callable[[Any], MetricResult]:
    def extract(payload: Any) -> MetricResult:
        value = _get(payload, field, "value")
        as_of = _as_of(payload)
        if value is None:
            reason = _reason(payload, field, "reason") or f"{field} is null"
            return MetricResult(None, as_of, reason)
        return MetricResult(value, as_of)

    return extract


def _extract_valuation_field(field: str) -> Callable[[Any], MetricResult]:
    def extract(payload: Any) -> MetricResult:
        value = _get(payload, field)
        as_of = _as_of(payload)
        if value is None:
            return MetricResult(None, as_of, f"kis stock valuation did not report {field}")
        return MetricResult(value, as_of)

    return extract


def _extract_band_percentile(field: str) -> Callable[[Any], MetricResult]:
    def extract(payload: Any) -> MetricResult:
        value = _get(payload, field, "current_percentile")
        as_of = _as_of(payload)
        if value is None:
            return MetricResult(None, as_of, f"valuation-band has no {field}.current_percentile for this filer")
        return MetricResult(value, as_of)

    return extract


def _row_for(payload: Any, code: str) -> dict[str, Any] | None:
    rows = _get(payload, "rows")
    if not isinstance(rows, list):
        return None
    for row in rows:
        if isinstance(row, dict) and str(row.get("code")) == code:
            return row
    return None


def _extract_cache_rs_field(field: str) -> Callable[[Any, str], MetricResult]:
    def extract(payload: Any, code: str) -> MetricResult:
        as_of = _as_of(payload)
        row = _row_for(payload, code)
        value = row.get(field) if row else None
        if value is None:
            return MetricResult(None, as_of, f"cache rs has no row for {code} (not in today's universe, or dropped)")
        return MetricResult(value, as_of)

    return extract


def _extract_setup_group(payload: Any, code: str) -> MetricResult:  # noqa: ARG001 - keeps the two-arg extractor shape
    status = _get(payload, "setup", "status")
    as_of = _as_of(payload)
    if status is None:
        return MetricResult(None, as_of, "trend-setup gave no setup.status")
    state = _STATUS_TO_STATE.get(str(status))
    if state is None:
        return MetricResult(None, as_of, f"setup.status={status!r} has no trend-setup group (illiquid)")
    return MetricResult(state, as_of)


def _extract_stop_width_pct(payload: Any, code: str) -> MetricResult:  # noqa: ARG001
    levels = _get(payload, "stop_sizing", "levels")
    as_of = _as_of(payload)
    if not isinstance(levels, list):
        return MetricResult(None, as_of, "technical gave no stop_sizing.levels")
    level = next((lv for lv in levels if lv.get("horizon_days") == _STOP_WIDTH_HORIZON_DAYS), None)
    if level is None or level.get("width_pct") is None:
        return MetricResult(None, as_of, f"no stop_sizing level for horizon_days={_STOP_WIDTH_HORIZON_DAYS}")
    return MetricResult(level["width_pct"], as_of)


def _one_arg(fn: Callable[[Any], MetricResult]) -> Callable[[Any, str], MetricResult]:
    def wrapped(payload: Any, code: str) -> MetricResult:  # noqa: ARG001
        return fn(payload)

    return wrapped


@dataclass(frozen=True, slots=True)
class MetricSpec:
    id: str
    raw: str  # raw file stem, e.g. "dart-financial-summary"
    kind: str  # "number" | "string"
    description: str
    extract: Callable[[Any, str], MetricResult]


def _spec(
    id_: str, raw: str, description: str, fn: Callable[[Any], MetricResult], *, kind: str = "number"
) -> MetricSpec:
    return MetricSpec(id=id_, raw=raw, kind=kind, description=description, extract=_one_arg(fn))


CATALOG: dict[str, MetricSpec] = {
    spec.id: spec
    for spec in (
        _spec(
            "revenue_yoy_4q",
            "dart-financial-summary",
            "최근 4분기 매출 합 ÷ 그 앞 4분기 합 − 1 (%), company-review 다섯 가지 체크와 같은 식",
            _extract_revenue_yoy_4q,
        ),
        _spec(
            "opm_ttm",
            "dart-financial-summary",
            "TTM 영업이익률 (%) = ttm.operating_income / ttm.revenue",
            _extract_opm_ttm,
        ),
        _spec(
            "roe",
            "dart-financial-summary",
            "최신 사업연도 ROE (%), quality.years[-1].dupont.roe_reported",
            _extract_roe,
        ),
        _spec("roic", "dart-financial-summary", "최신 사업연도 ROIC (%), quality.years[-1].roic", _extract_roic),
        _spec("f_score", "dart-financial-summary", "Piotroski F-Score (0~9), quality.f_score.total", _extract_f_score),
        _spec(
            "altman_z2",
            "dart-financial-summary",
            "Altman Z'' (장부가), quality.years[-1].altman_z_double_prime",
            _extract_altman_z2,
        ),
        _spec(
            "fcf_yield",
            "kis-stock-investor-metrics",
            "FCF 수익률 (%), investor-metrics.fcf_yield",
            _extract_investor_metric("fcf_yield"),
        ),
        _spec(
            "net_debt_ratio",
            "dart-financial-summary",
            "최근 누적 순차입금비율 (%), latest.net_debt_ratio (음수면 순현금)",
            _financial_summary_metric(("latest", "net_debt_ratio")),
        ),
        _spec(
            "interest_coverage",
            "dart-financial-summary",
            "최근 누적 이자보상배율 (배), latest.interest_coverage",
            _financial_summary_metric(("latest", "interest_coverage")),
        ),
        _spec("per_ttm", "kis-stock-valuation", "TTM PER (배)", _extract_valuation_field("per_ttm")),
        _spec("pbr", "kis-stock-valuation", "PBR (배)", _extract_valuation_field("pbr")),
        _spec(
            "per_band_pct",
            "kis-stock-valuation-band",
            "5년 PER 분위 (0~100), per.current_percentile",
            _extract_band_percentile("per"),
        ),
        _spec(
            "pbr_band_pct",
            "kis-stock-valuation-band",
            "5년 PBR 분위 (0~100), pbr.current_percentile",
            _extract_band_percentile("pbr"),
        ),
        _spec(
            "ev_ebit",
            "kis-stock-investor-metrics",
            "EV/EBIT (배), investor-metrics.ev_ebit",
            _extract_investor_metric("ev_ebit"),
        ),
        _spec(
            "shareholder_yield",
            "kis-stock-investor-metrics",
            "주주수익률 (%), investor-metrics.shareholder_yield",
            _extract_investor_metric("shareholder_yield"),
        ),
        MetricSpec(
            id="dilution_3y_pct",
            raw="dart-dilution-watch",
            kind="number",
            description="최근 3년 희석 비율 합 (%), dilution-watch.rows 의 양수 pct_of_shares 합(환원은 뺀다)",
            extract=_one_arg(_extract_dilution_3y_pct),
        ),
        MetricSpec(
            id="rs_1m",
            raw="cache-rs",
            kind="number",
            description="RS(1M) 백분위 (0~99), cache rs 의 본 종목 행",
            extract=_extract_cache_rs_field("rs_1m"),
        ),
        MetricSpec(
            id="sector_rs",
            raw="cache-rs",
            kind="number",
            description="업종 RS 백분위 (0~99), cache rs 의 본 종목 행",
            extract=_extract_cache_rs_field("sector_rs"),
        ),
        MetricSpec(
            id="setup_group",
            raw="kis-chart-trend-setup",
            kind="string",
            description="trend-setup 관심종목 그룹: g1/g2/g3/none (문자열, = · != 만 쓸 수 있다)",
            extract=_extract_setup_group,
        ),
        MetricSpec(
            id="stop_width_pct",
            raw="kis-chart-technical",
            kind="number",
            description=f"손절폭 (%, horizon_days={_STOP_WIDTH_HORIZON_DAYS}), technical.stop_sizing.levels",
            extract=_extract_stop_width_pct,
        ),
    )
}


def raw_path(folder: Path, code: str, raw_stem: str) -> Path:
    return folder / "raw" / f"{code}__{raw_stem}.json"


def read_raw(folder: Path, code: str, raw_stem: str) -> Any | None:
    """The parsed JSON a `review collect` call wrote, or ``None`` if the file is missing or not valid JSON/an error."""

    path = raw_path(folder, code, raw_stem)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict) and "error" in payload:
        return None
    return payload


def compute(folder: Path, code: str, metric_id: str) -> MetricResult:
    spec = CATALOG[metric_id]
    payload = read_raw(folder, code, spec.raw)
    if payload is None:
        return MetricResult(None, None, f"no raw/{code}__{spec.raw}.json (missing, unreadable, or the call failed)")
    return spec.extract(payload, code)


def catalog_rows() -> list[dict[str, Any]]:
    return [
        {"metric": spec.id, "kind": spec.kind, "raw": spec.raw, "description": spec.description}
        for spec in CATALOG.values()
    ]
