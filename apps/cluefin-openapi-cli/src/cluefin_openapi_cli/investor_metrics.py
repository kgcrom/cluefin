"""Investor-style quality/value metrics for `kis stock investor-metrics`.

Pure functions only — no DART/KIS calls, no buy/sell labels. Inputs come from the handler (market
cap = KIS close × DART common shares, same convention as `stock.valuation`; cash-flow and balance
figures from `statements.annual()`, raw 원). Ratios are scale-invariant so this module does not
care about the unit, but callers must pass every value through in the same unit. Every metric
returns its value alongside a `reason` (or the components, for the richer ones) so a `null` can be
traced back to whichever input was missing — same discipline as `quality.py`. This module never
substitutes 0 for a missing input (an actually-zero figure is a reported `0`, not `None`).

Formulas and sources (also in README/AGENTS, 2026-11-04 결정):

- FCF 수익률 = 잉여현금흐름(statements.py 의 free_cash_flow = 영업활동현금흐름 − 유형자산의취득) ÷ 시가총액.
- 오너 어닝스 = 지배주주순이익 + 감가상각비 + 무형자산상각비 − 유형자산 취득 전액 − 운전자본(유동자산−유동부채)
  증가분. 유지 capex 를 별도로 추정하지 않는 보수적인 정의다 (Warren Buffett, Berkshire Hathaway 1986
  주주서한). 감가상각비·무형자산상각비 가운데 하나라도 None 이면(대형 공시자는 현금흐름표 "조정" 한 줄에
  묶어 내서 전체 재무제표에 D&A 가 따로 없다) 오너 어닝스는 0 으로 메우지 않고 null + 이유를 낸다.
- EV/EBIT, 이익수익률(EBIT/EV) — EBIT 는 영업이익으로 대신한다(dart financial-summary 와 같은 관례).
  (Joel Greenblatt, "The Little Book That Still Beats the Market", 2005 — 마법공식의 이익수익률과 같은 정의.)
- PEG = PER ÷ EPS 성장률(%). 성장률은 두 출처를 각각 낸다: DART 3개년(최신 사업보고서의 당기·전전기) 지배주주
  순이익 ÷ 그 사업연도 말 보통주 발행주식수로 구한 EPS 의 CAGR, 그리고 KIS 종목추정실적의
  `eps_growth_yoy`(한국투자증권 추정, 가장 가까운 추정연도) — 어느 쪽도 다른 쪽을 대신하지 않는다
  (Peter Lynch, "One Up on Wall Street", 1989).
- 주주수익률 = (배당금의 지급 + 자기주식의 취득 − 자기주식의 처분 − 주식의 발행) ÷ 시가총액(윌리엄
  프리스트/Epoch Investment Partners 의 shareholder yield 정의). 현금흐름표가 읽혔으면(영업활동현금흐름이
  있으면) 없는 항목은 그 활동이 없었던 것으로 보고 0 으로 두되 `assumed_zero` 에 이름을 남긴다 — 회사는
  하지 않은 활동의 줄을 공시하지 않는다. 현금흐름표 자체가 없으면 null + 이유.
- Altman Z(시총 원형)는 `quality.altman_z`(quality.py) — 이 모듈은 재사용만 하고 다시 짜지 않는다.
"""

from __future__ import annotations

from typing import Any


def _missing(**fields: Any) -> str:
    names = [name for name, value in fields.items() if value is None]
    return "결측: " + ", ".join(names)


def _yield_on_market_cap(value: float | None, market_cap: float | None, value_label: str) -> dict[str, Any]:
    if value is None or market_cap is None:
        return {
            "value": None,
            value_label: value,
            "market_cap": market_cap,
            "reason": _missing(**{value_label: value, "market_cap": market_cap}),
        }
    if market_cap <= 0:
        return {"value": None, value_label: value, "market_cap": market_cap, "reason": "market_cap 0 이하"}
    return {"value": value / market_cap * 100, value_label: value, "market_cap": market_cap, "reason": None}


def fcf_yield(free_cash_flow: float | None, market_cap: float | None) -> dict[str, Any]:
    """FCF 수익률(%) = 잉여현금흐름 ÷ 시가총액. free_cash_flow 는 statements.py 의 값(영업현금흐름 − capex)."""
    return _yield_on_market_cap(free_cash_flow, market_cap, "free_cash_flow")


def owner_earnings(
    net_income_owners: float | None,
    depreciation: float | None,
    amortization: float | None,
    capex: float | None,
    working_capital_increase: float | None,
) -> dict[str, Any]:
    """오너 어닝스 = 순이익(지배지분) + D&A − 유형자산 취득 전액 − 운전자본 증가. D&A 결측이면 null.

    capex 는 공시 부호가 회사마다 달라(음수·양수) 절댓값을 뺀다. components 에는 공시값을 그대로 둔다.
    """
    components = {
        "net_income_owners": net_income_owners,
        "depreciation": depreciation,
        "amortization": amortization,
        "capex": capex,
        "working_capital_increase": working_capital_increase,
    }
    if depreciation is None or amortization is None:
        return {
            "value": None,
            "components": components,
            "reason": "감가상각비·무형자산상각비 중 결측이 있음 — 대형 공시자는 현금흐름표 조정 한 줄에 "
            "묶어 내서 전체 재무제표에 D&A 가 따로 없다(0 으로 메우지 않는다)",
        }
    if net_income_owners is None or capex is None or working_capital_increase is None:
        return {
            "value": None,
            "components": components,
            "reason": _missing(
                net_income_owners=net_income_owners, capex=capex, working_capital_increase=working_capital_increase
            ),
        }
    value = net_income_owners + depreciation + amortization - abs(capex) - working_capital_increase
    return {"value": value, "components": components, "reason": None}


def owner_earnings_yield(owner_earnings_value: float | None, market_cap: float | None) -> dict[str, Any]:
    """오너 어닝스 수익률(%) = 오너 어닝스 ÷ 시가총액."""
    return _yield_on_market_cap(owner_earnings_value, market_cap, "owner_earnings")


def ev_ebit(ev: float | None, ebit: float | None) -> dict[str, Any]:
    """EV/EBIT. EBIT 는 영업이익 대용. 분모가 0 이하면 계산하지 않는다."""
    if ev is None or ebit is None:
        return {"value": None, "ev": ev, "ebit": ebit, "reason": _missing(ev=ev, ebit=ebit)}
    if ebit <= 0:
        return {"value": None, "ev": ev, "ebit": ebit, "reason": "ebit 0 이하 — 배수가 의미 없다"}
    return {"value": ev / ebit, "ev": ev, "ebit": ebit, "reason": None}


def earnings_yield(ebit: float | None, ev: float | None) -> dict[str, Any]:
    """이익수익률(%) = EBIT ÷ EV (Greenblatt 마법공식과 같은 정의, EV/EBIT 의 역수)."""
    if ebit is None or ev is None:
        return {"value": None, "ebit": ebit, "ev": ev, "reason": _missing(ebit=ebit, ev=ev)}
    if ev <= 0:
        return {"value": None, "ebit": ebit, "ev": ev, "reason": "ev 0 이하 — 배수가 의미 없다"}
    return {"value": ebit / ev * 100, "ebit": ebit, "ev": ev, "reason": None}


def eps_cagr(eps_start: float | None, eps_end: float | None, years: int | None) -> dict[str, Any]:
    """두 시점 EPS 의 연복리 성장률(%). 둘 중 하나라도 0 이하면 부호 전환이라 계산하지 않는다."""
    if eps_start is None or eps_end is None or not years:
        return {
            "value": None,
            "eps_start": eps_start,
            "eps_end": eps_end,
            "years": years,
            "reason": _missing(eps_start=eps_start, eps_end=eps_end, years=years),
        }
    if eps_start <= 0 or eps_end <= 0:
        return {
            "value": None,
            "eps_start": eps_start,
            "eps_end": eps_end,
            "years": years,
            "reason": "적자 구간 포함 — 부호가 바뀌는 CAGR 은 계산하지 않는다",
        }
    value = ((eps_end / eps_start) ** (1 / years) - 1) * 100
    return {"value": value, "eps_start": eps_start, "eps_end": eps_end, "years": years, "reason": None}


def peg(per: float | None, growth_pct: float | None, growth_source: str) -> dict[str, Any]:
    """PEG = PER ÷ EPS 성장률(%). 성장률이 0 이하(역성장·적자전환)면 Lynch 공식은 적용하지 않는다."""
    if per is None or growth_pct is None:
        return {
            "value": None,
            "per": per,
            "growth_pct": growth_pct,
            "growth_source": growth_source,
            "reason": _missing(per=per, growth_pct=growth_pct),
        }
    if per <= 0:
        return {
            "value": None,
            "per": per,
            "growth_pct": growth_pct,
            "growth_source": growth_source,
            "reason": "per 0 이하",
        }
    if growth_pct <= 0:
        return {
            "value": None,
            "per": per,
            "growth_pct": growth_pct,
            "growth_source": growth_source,
            "reason": "성장률 0 이하 — Lynch PEG 는 양의 성장만 쓴다",
        }
    return {
        "value": per / growth_pct,
        "per": per,
        "growth_pct": growth_pct,
        "growth_source": growth_source,
        "reason": None,
    }


def shareholder_yield(
    dividends_paid: float | None,
    treasury_shares_acquired: float | None,
    treasury_shares_disposed: float | None,
    proceeds_from_share_issuance: float | None,
    market_cap: float | None,
    *,
    cash_flow_statement_present: bool = False,
) -> dict[str, Any]:
    """주주수익률(%) = (배당금 지급 + 자기주식 취득 − 자기주식 처분 − 주식 발행) ÷ 시가총액.

    ``cash_flow_statement_present`` (영업활동현금흐름이 읽혔다)면 없는 항목을 그 활동이 없었던 것으로 보고 0 으로
    계산하고 `assumed_zero` 에 이름을 남긴다. 아니면 None 이 "활동 없음"인지 "표를 못 읽음"인지 알 수 없어
    항목이 하나라도 없으면 null + 이유다.
    """
    items = {
        "dividends_paid": dividends_paid,
        "treasury_shares_acquired": treasury_shares_acquired,
        "treasury_shares_disposed": treasury_shares_disposed,
        "proceeds_from_share_issuance": proceeds_from_share_issuance,
    }
    components = {**items, "market_cap": market_cap}
    missing_items = [name for name, value in items.items() if value is None]
    if market_cap is None or (missing_items and not cash_flow_statement_present):
        return {"value": None, "components": components, "assumed_zero": [], "reason": _missing(**components)}
    if market_cap <= 0:
        return {"value": None, "components": components, "assumed_zero": [], "reason": "market_cap 0 이하"}
    amounts = {name: abs(value or 0.0) for name, value in items.items()}
    net_return = (
        amounts["dividends_paid"]
        + amounts["treasury_shares_acquired"]
        - amounts["treasury_shares_disposed"]
        - amounts["proceeds_from_share_issuance"]
    )
    return {
        "value": net_return / market_cap * 100,
        "components": components,
        "assumed_zero": missing_items,
        "reason": None,
    }
