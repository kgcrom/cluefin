"""Financial-quality metrics computed from `statements.annual()` output.

Pure functions only — no DART calls, no labels, no buy/sell verdicts. Every metric returns its
value alongside the components the formula used, so a caller can re-derive it without re-reading
this module. Inputs are the three-year list `statements.annual()` returns (already in 억원 once
`statements.to_eok` has run — ratios are scale-invariant so this module does not care about the
unit, but callers should pass the same unit throughout).

A classified balance sheet (유동/비유동 구분) is not required by K-IFRS for banks, insurers and
securities firms, so `current_assets`/`current_liabilities`/`revenue` (and often `cash`, filed as
예치금 rather than 현금및현금성자산) come back `None` for them from `statements.py` — this module
never substitutes 0 for a missing input. `altman_z_double_prime` and `piotroski_f_score` name the
missing field in `missing`/`incomplete`; `roic`/`dupont`/`accrual_ratio` instead echo every raw
input they used (`invested_capital`, `nopat`, `avg_assets`, …), so a `null` value can be traced to
whichever of those components is itself `null`.

Formulas and sources (also in README/AGENTS):

- ROIC = 세후 영업이익 ÷ 투하자본, 세율은 실효세율(법인세비용 ÷ 세전이익)을 0~40%로 자른다.
  투하자본 = 자기자본(지배지분) + 차입금 − 현금. 전기 값이 있으면 당기·전기 평균을 쓴다.
  (Bruce Greenwald, "Value Investing"; Joel Greenblatt 의 마법공식과 같은 세후 영업이익 정의.)
- DuPont 3단계 분해: ROE = 순이익률 × 총자산회전율 × 레버리지(평균자산 ÷ 평균자기자본).
  (Donaldson Brown, DuPont Corporation, 1910s-20s; 표준 3-factor 분해.)
- 발생액 비율(accruals ratio) = (순이익 − 영업현금흐름) ÷ 평균총자산.
  (Richard Sloan, "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about
  Future Earnings?", The Accounting Review, 1996.)
- Piotroski F-Score 9항목(수익성 4·재무구조 3·효율성 2), 항목마다 0/1/결측.
  (Joseph Piotroski, "Value Investing: The Use of Historical Financial Statement Information to
  Separate Winners from Losers", Journal of Accounting Research, 2000.)
- Altman Z''(장부가, 비제조업·이머징마켓 변형) = 6.56·X1 + 3.26·X2 + 6.72·X3 + 1.05·X4.
  (Edward Altman, Hartzell & Peck, "Emerging Markets Corporate Bonds: A Scoring System", 1995.)
- Altman Z(원형, 시가총액 버전) = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5. X1~X3 은 Z''와 같고,
  X4 는 장부가 자기자본 대신 시가총액 ÷ 부채총계, X5 는 매출액 ÷ 자산총계다. `kis stock investor-metrics`
  가 시가총액을 들고 와 `altman_z`를 호출한다 — 이 모듈은 Z''의 x1~x3 계산을 재사용만 한다.
  (Edward Altman, "Financial Ratios, Discriminant Analysis and the Prediction of Corporate
  Bankruptcy", The Journal of Finance, 1968.)
"""

from __future__ import annotations

from typing import Any

MIN_TAX_RATE = 0.0
MAX_TAX_RATE = 0.40


def _avg(current: float | None, previous: float | None) -> tuple[float | None, bool]:
    """(average-or-point value, whether an average was used)."""
    if current is None:
        return None, False
    if previous is None:
        return current, False
    return (current + previous) / 2, True


def effective_tax_rate(income_tax_expense: float | None, pretax_income: float | None) -> float | None:
    """법인세비용 ÷ 세전이익, 0~40%(0.0~0.4)로 자른다. 세전이익이 0 이하면 계산하지 않는다."""
    if income_tax_expense is None or pretax_income is None or pretax_income <= 0:
        return None
    rate = income_tax_expense / pretax_income
    return max(MIN_TAX_RATE, min(MAX_TAX_RATE, rate))


def invested_capital(equity_owners: float | None, borrowings: float | None, cash: float | None) -> float | None:
    """자기자본(지배지분) + 차입금 − 현금."""
    if equity_owners is None or borrowings is None or cash is None:
        return None
    return equity_owners + borrowings - cash


def roic(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    """ROIC = 세후 영업이익 ÷ 투하자본(가능하면 평균). value 는 %."""
    tax_rate = effective_tax_rate(current.get("income_tax_expense"), current.get("pretax_income"))
    operating_income = current.get("operating_income")
    nopat = None if operating_income is None or tax_rate is None else operating_income * (1 - tax_rate)

    ic_now = invested_capital(current.get("equity_owners"), current.get("borrowings"), current.get("cash"))
    ic_prev = (
        invested_capital(previous.get("equity_owners"), previous.get("borrowings"), previous.get("cash"))
        if previous is not None
        else None
    )
    ic, averaged = _avg(ic_now, ic_prev)

    value = None if nopat is None or ic is None or ic == 0 else nopat / ic * 100
    return {
        "value": value,
        "nopat": nopat,
        "invested_capital": ic,
        "invested_capital_averaged": averaged,
        "effective_tax_rate": None if tax_rate is None else tax_rate * 100,
        "operating_income": operating_income,
        # Raw inputs so a null invested_capital can be traced to whichever of these is missing
        # (financial holding companies often file cash as 예치금, not 현금및현금성자산).
        "equity_owners": current.get("equity_owners"),
        "borrowings": current.get("borrowings"),
        "cash": current.get("cash"),
    }


def dupont(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    """ROE = 순이익률 × 총자산회전율 × 레버리지(평균자산/평균자기자본). `roe_check` 가 곱의 결과."""
    revenue = current.get("revenue")
    net_income = current.get("net_income_owners")
    assets_now, equity_now = current.get("assets"), current.get("equity_owners")
    assets_prev = previous.get("assets") if previous is not None else None
    equity_prev = previous.get("equity_owners") if previous is not None else None

    avg_assets, _ = _avg(assets_now, assets_prev)
    avg_equity, _ = _avg(equity_now, equity_prev)

    net_margin = None if net_income is None or revenue is None or revenue == 0 else net_income / revenue
    asset_turnover = None if revenue is None or avg_assets is None or avg_assets == 0 else revenue / avg_assets
    leverage = None if avg_assets is None or avg_equity is None or avg_equity == 0 else avg_assets / avg_equity

    roe_check = None
    if net_margin is not None and asset_turnover is not None and leverage is not None:
        roe_check = net_margin * asset_turnover * leverage * 100

    return {
        "net_margin": None if net_margin is None else net_margin * 100,
        "asset_turnover": asset_turnover,
        "leverage": leverage,
        "roe_check": roe_check,
        "roe_reported": current.get("roe"),
        # Raw inputs: asset_turnover is null without `revenue` (banks/insurers file 이자수익 instead).
        "revenue": revenue,
        "net_income_owners": net_income,
        "avg_assets": avg_assets,
        "avg_equity_owners": avg_equity,
    }


def accrual_ratio(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    """(순이익 − 영업현금흐름) ÷ 평균총자산. value 는 %."""
    net_income = current.get("net_income")
    cfo = current.get("operating_cash_flow")
    avg_assets, averaged = _avg(current.get("assets"), previous.get("assets") if previous is not None else None)

    accrual = None if net_income is None or cfo is None else net_income - cfo
    value = None if accrual is None or avg_assets is None or avg_assets == 0 else accrual / avg_assets * 100
    return {
        "value": value,
        "accruals": accrual,
        "net_income": net_income,
        "operating_cash_flow": cfo,
        "avg_assets": avg_assets,
        "avg_assets_averaged": averaged,
    }


def altman_z_double_prime(year: dict[str, Any]) -> dict[str, Any]:
    """Z'' = 6.56·X1 + 3.26·X2 + 6.72·X3 + 1.05·X4 (장부가, 비제조업 변형). 결측 성분은 null + 이유."""
    assets = year.get("assets")
    current_assets, current_liabilities = year.get("current_assets"), year.get("current_liabilities")
    retained_earnings = year.get("retained_earnings")
    operating_income = year.get("operating_income")
    equity, liabilities = year.get("equity"), year.get("liabilities")

    missing: list[str] = []

    x1 = None
    if assets is None or assets == 0 or current_assets is None or current_liabilities is None:
        missing.append(
            "x1(운전자본/자산): current_assets/current_liabilities 없음 — 유동/비유동 구분이 없는 업종(은행·보험·증권)"
        )
    else:
        x1 = (current_assets - current_liabilities) / assets

    x2 = None
    if assets is None or assets == 0 or retained_earnings is None:
        missing.append("x2(이익잉여금/자산): retained_earnings 없음")
    else:
        x2 = retained_earnings / assets

    x3 = None
    if assets is None or assets == 0 or operating_income is None:
        missing.append("x3(EBIT/자산): operating_income 을 EBIT 대용으로 쓴다")
    else:
        x3 = operating_income / assets

    x4 = None
    if liabilities is None or liabilities == 0 or equity is None:
        missing.append("x4(자본/부채): equity 또는 liabilities 없음")
    else:
        x4 = equity / liabilities

    value = None
    if None not in (x1, x2, x3, x4):
        value = 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4

    return {"value": value, "x1": x1, "x2": x2, "x3": x3, "x4": x4, "missing": missing}


def altman_z(year: dict[str, Any], market_cap: float | None) -> dict[str, Any]:
    """Z(원형, 시가총액 버전) = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5.

    X1~X3 은 `altman_z_double_prime`과 같은 운전자본·이익잉여금·EBIT 비율이다 — 다시 계산하지 않고
    그 결과를 재사용한다. X4(시가총액 ÷ 부채총계)·X5(매출액 ÷ 자산총계)만 이 함수가 새로 낸다.
    `market_cap`은 호출부가 같은 단위(원 또는 억원)로 `year`의 금액과 맞춰 넘겨야 한다.
    """
    prime = altman_z_double_prime(year)
    x1, x2, x3 = prime["x1"], prime["x2"], prime["x3"]
    # x4 메시지만 뺀다 — Z''의 x4(자기자본/부채, 장부가)는 이 Z(시가총액 버전)의 x4와 다른 성분이다.
    missing = [item for item in prime["missing"] if not item.startswith("x4")]

    assets = year.get("assets")
    liabilities = year.get("liabilities")
    revenue = year.get("revenue")

    x4 = None
    if market_cap is None or liabilities is None or liabilities == 0:
        missing.append("x4(시가총액/부채): market_cap 또는 liabilities 없음")
    else:
        x4 = market_cap / liabilities

    x5 = None
    if assets is None or assets == 0 or revenue is None:
        missing.append("x5(매출/자산): revenue 없음 — 금융업(은행·보험·증권)은 매출 항목이 없다")
    else:
        x5 = revenue / assets

    value = None
    if None not in (x1, x2, x3, x4, x5):
        value = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5

    return {"value": value, "x1": x1, "x2": x2, "x3": x3, "x4": x4, "x5": x5, "missing": missing}


def _flag(condition: bool | None) -> int | None:
    if condition is None:
        return None
    return 1 if condition else 0


def _delta(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None:
        return None
    return current - previous


def piotroski_f_score(current: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    """9항목 0/1(결측은 null)과 합계. 결측이 하나라도 있으면 `incomplete: true`.

    장기부채비율은 noncurrent_liabilities/assets 로 근사한다 — financial-summary 는 만기별
    차입금을 따로 내지 않는다(차입금은 단기+장기 합계 하나뿐). 신주 발행 여부는 현금흐름표의
    `proceeds_from_share_issuance` 가 0(또는 결측, 발행이 없다는 뜻으로 0 취급)인지로 본다.
    """
    if previous is None:
        items = dict.fromkeys(
            [
                "roa_positive",
                "cfo_positive",
                "roa_improved",
                "cfo_exceeds_net_income",
                "leverage_decreased",
                "current_ratio_improved",
                "no_new_shares",
                "gross_margin_improved",
                "asset_turnover_improved",
            ],
            None,
        )
        return {"items": items, "total": None, "incomplete": True}

    def roa(year: dict[str, Any]) -> float | None:
        ni, assets = year.get("net_income"), year.get("assets")
        return None if ni is None or assets is None or assets == 0 else ni / assets

    def current_ratio(year: dict[str, Any]) -> float | None:
        ca, cl = year.get("current_assets"), year.get("current_liabilities")
        return None if ca is None or cl is None or cl == 0 else ca / cl

    def leverage(year: dict[str, Any]) -> float | None:
        ncl, assets = year.get("noncurrent_liabilities"), year.get("assets")
        return None if ncl is None or assets is None or assets == 0 else ncl / assets

    def gross_margin(year: dict[str, Any]) -> float | None:
        gp, rev = year.get("gross_profit"), year.get("revenue")
        return None if gp is None or rev is None or rev == 0 else gp / rev

    def asset_turnover(year: dict[str, Any]) -> float | None:
        rev, assets = year.get("revenue"), year.get("assets")
        return None if rev is None or assets is None or assets == 0 else rev / assets

    roa_now, roa_prev = roa(current), roa(previous)
    cfo_now = current.get("operating_cash_flow")
    net_income_now = current.get("net_income")
    shares_issued = current.get("proceeds_from_share_issuance") or 0

    items = {
        "roa_positive": _flag(None if roa_now is None else roa_now > 0),
        "cfo_positive": _flag(None if cfo_now is None else cfo_now > 0),
        "roa_improved": _flag(None if (d := _delta(roa_now, roa_prev)) is None else d > 0),
        "cfo_exceeds_net_income": _flag(
            None if cfo_now is None or net_income_now is None else cfo_now > net_income_now
        ),
        "leverage_decreased": _flag(None if (d := _delta(leverage(current), leverage(previous))) is None else d < 0),
        "current_ratio_improved": _flag(
            None if (d := _delta(current_ratio(current), current_ratio(previous))) is None else d > 0
        ),
        "no_new_shares": _flag(shares_issued <= 0),
        "gross_margin_improved": _flag(
            None if (d := _delta(gross_margin(current), gross_margin(previous))) is None else d > 0
        ),
        "asset_turnover_improved": _flag(
            None if (d := _delta(asset_turnover(current), asset_turnover(previous))) is None else d > 0
        ),
    }
    values = list(items.values())
    incomplete = any(v is None for v in values)
    total = sum(v for v in values if v is not None) if any(v is not None for v in values) else None
    return {"items": items, "total": total, "incomplete": incomplete}


def compute(years: list[dict[str, Any]]) -> dict[str, Any]:
    """The whole `quality` block from `statements.annual()`'s three fiscal years, oldest first."""
    by_year = []
    for i, year in enumerate(years):
        previous = years[i - 1] if i > 0 else None
        by_year.append(
            {
                "year": year["year"],
                "roic": roic(year, previous),
                "dupont": dupont(year, previous),
                "accrual_ratio": accrual_ratio(year, previous),
                "altman_z_double_prime": altman_z_double_prime(year),
            }
        )
    f_score = piotroski_f_score(years[-1], years[-2]) if len(years) >= 2 else piotroski_f_score(years[-1], None)
    return {
        "years": by_year,
        "f_score": f_score,
        "notes": [
            "라벨·판정 없음 — 값과 구성요소만. 금융업(은행·보험·증권)은 유동/비유동 구분이 없어 "
            "x1·current_ratio·gross_margin·asset_turnover 관련 항목이 null 이다(이유는 altman_z_double_prime.missing).",
            "ROIC 투하자본 = 자기자본(지배지분) + 차입금 − 현금, 전기 값이 있으면 평균. 세율은 "
            "실효세율(법인세비용/세전이익)을 0~40%로 자른다.",
            "DuPont 의 roe_check 가 roe_reported 와 다르면 평균자산/평균자기자본 반올림이나 지배·비지배 "
            "순이익 구분 차이다 — net_income_owners 로 계산하고 reported 는 그대로 둔다.",
            "F-Score 의 장기부채비율은 noncurrent_liabilities/assets 근사다 — financial-summary 는 만기별 "
            "차입금을 나누지 않는다. 가장 오래된 해는 전기가 없어 전 항목 null, incomplete:true.",
        ],
    }
