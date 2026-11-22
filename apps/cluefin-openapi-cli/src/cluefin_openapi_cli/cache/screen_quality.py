"""Value and balance-sheet factors for `cache screen` from the quarter panel (decided 2026-11-22).

All read `screen_ttm.ttm_by_code`'s panel: flows are TTM, balances the latest due quarter-end and the
same quarter a year earlier.

- `roa_ttm`/`asset_turnover_ttm` divide by the average of the latest and year-earlier 자산총계; with
  either end missing they are `null` (no fallback to a single balance — decision 2).
- `peg_ttm` = `per_ttm` / growth, growth being `ni_cagr_3y` or, when that is null, `ni_yoy_ttm`;
  non-positive growth is `null`.
- `earnings_yield_ttm` reuses `cache.magic.enterprise_value` (시총 + 부채총계, no cash split) and is
  `null` for `cache.magic.EXCLUDED_SECTORS`, same as `earnings_yield`.
- `retained_ratio` (유보율 근사) = 이익잉여금 / 자본금; filers spell the line "이익잉여금" or
  "이익잉여금(결손금)", both are read.
"""

from __future__ import annotations

from typing import Any

from cluefin_openapi_cli.cache.magic import EXCLUDED_SECTORS, enterprise_value

__all__ = ["QUALITY_FACTORS", "quality_factors"]

QUALITY_FACTORS: tuple[tuple[str, str], ...] = (
    ("roa_ttm", "TTM 당기순이익 / (최근 분기말 + 1년 전 분기말) 평균 자산총계 * 100 (%). 한쪽이 없으면 null."),
    ("npm_ttm", "TTM 당기순이익 / TTM 매출액 * 100 (%). 매출액<=0 이면 null."),
    ("asset_turnover_ttm", "TTM 매출액 / 평균 자산총계(roa_ttm 과 같은 평균) (배)."),
    ("peg_ttm", "per_ttm / 이익 성장률(ni_cagr_3y, 없으면 ni_yoy_ttm). 성장률<=0 이면 null. 성장 대비 주가."),
    ("earnings_yield_ttm", "TTM 영업이익 / EV(시총 + 최근 분기말 부채총계) * 100 (%). 금융·증권·보험·전기가스는 null."),
    ("current_ratio", "최근 분기말 유동자산 / 유동부채 * 100 (%)."),
    ("debt_ratio_mrq", "최근 분기말 부채총계 / 자본총계 * 100 (%). 자본총계<=0 이면 null."),
    ("ncav_ratio", "(최근 분기말 유동자산 − 부채총계) / 시총 (배). 그레이엄 순유동자산 — 1 이상이면 넷넷."),
    ("retained_ratio", "최근 분기말 이익잉여금 / 자본금 * 100 (%). 유보율 근사(자본잉여금 제외)."),
    ("capital_impairment", "최근 분기말 자본총계 < 자본금이면 1(부분 자본잠식), 아니면 0."),
    ("equity_yoy", "최근 분기말 자본총계의 1년 전 분기말 대비 증감률(%)."),
    (
        "noncurrent_asset_yoy",
        "최근 분기말 비유동자산의 1년 전 분기말 대비 증감률(%). 설비·투자 확대 근사(M&A·재평가 포함).",
    ),
    (
        "ni_to_op_ttm",
        "TTM 당기순이익 / TTM 영업이익 (배). 1보다 크게 높으면 일회성 이익일 수 있다. 영업이익<=0 이면 null.",
    ),
)
_FIELDS = tuple(name for name, _ in QUALITY_FACTORS)


def _get(panel: dict, period: tuple[int, int], account: str) -> float | None:
    values = panel.get(period, {}).get(account)
    return values[1] if values else None


def _div(numerator: float | None, denominator: float | None, scale: float = 1.0) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return round(numerator / denominator * scale, 2)


def _pct_change(now: float | None, before: float | None) -> float | None:
    if now is None or before is None or before <= 0:
        return None
    return round((now / before - 1) * 100, 2)


def _average(now: float | None, before: float | None) -> float | None:
    return (now + before) / 2 if now is not None and before is not None else None


def _balance_factors(panel: dict, latest: tuple[int, int]) -> dict[str, Any]:
    year_ago = (latest[0] - 1, latest[1])
    equity = _get(panel, latest, "자본총계")
    capital = _get(panel, latest, "자본금")
    retained = _get(panel, latest, "이익잉여금")
    if retained is None:
        retained = _get(panel, latest, "이익잉여금(결손금)")
    out: dict[str, Any] = {
        "current_ratio": _div(_get(panel, latest, "유동자산"), _get(panel, latest, "유동부채"), 100),
        "debt_ratio_mrq": _div(_get(panel, latest, "부채총계"), equity, 100),
        "retained_ratio": _div(retained, capital, 100),
        "equity_yoy": _pct_change(equity, _get(panel, year_ago, "자본총계")),
        "noncurrent_asset_yoy": _pct_change(_get(panel, latest, "비유동자산"), _get(panel, year_ago, "비유동자산")),
    }
    if equity is not None and capital is not None:
        out["capital_impairment"] = int(equity < capital)
    return out


def _market_factors(
    panel: dict, latest: tuple[int, int], mcap: float, per_ttm: float | None, growth: float | None, sector: str | None
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    current_assets = _get(panel, latest, "유동자산")
    total_liab = _get(panel, latest, "부채총계")
    if current_assets is not None and total_liab is not None and mcap > 0:
        out["ncav_ratio"] = round((current_assets - total_liab) / mcap, 2)
    ebit = _get(panel, latest, "영업이익")
    if sector not in EXCLUDED_SECTORS and ebit is not None and total_liab is not None:
        out["earnings_yield_ttm"] = _div(ebit, enterprise_value(mcap, total_liab), 100)
    if per_ttm is not None and growth is not None and growth > 0:
        out["peg_ttm"] = round(per_ttm / growth, 2)
    return out


def quality_factors(
    entry: dict[str, Any] | None,
    mcap: float | None,
    *,
    per_ttm: float | None,
    growth: float | None,
    sector: str | None,
) -> dict[str, Any]:
    """`QUALITY_FACTORS` for one stock; `growth` is the % used by `peg_ttm`."""

    out: dict[str, Any] = dict.fromkeys(_FIELDS, None)
    if not entry:
        return out
    panel, latest = entry["panel"], entry["period"]
    avg_assets = _average(_get(panel, latest, "자산총계"), _get(panel, (latest[0] - 1, latest[1]), "자산총계"))
    net_income, revenue, ebit = (_get(panel, latest, name) for name in ("당기순이익", "매출액", "영업이익"))
    out["roa_ttm"] = _div(net_income, avg_assets, 100)
    out["npm_ttm"] = _div(net_income, revenue, 100)
    out["asset_turnover_ttm"] = _div(revenue, avg_assets)
    out["ni_to_op_ttm"] = _div(net_income, ebit)
    out.update(_balance_factors(panel, latest))
    if mcap is not None:
        out.update(_market_factors(panel, latest, mcap, per_ttm, growth, sector))
    return out
