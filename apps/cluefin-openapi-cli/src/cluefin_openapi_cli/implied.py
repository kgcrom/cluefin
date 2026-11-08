"""RIM(잔여이익모델) 내재 ROE, 역DCF 내재 매출성장률 — 순수 계산, I/O 없음.

모든 비율은 **소수(0.08 = 8%)** 로 받고 돌려준다. 퍼센트 단위 변환은 호출부(핸들러)의 몫이다.

RIM: 장부가 B0 에서 출발해 초과 ROE(ROE − 자기자본비용)가 `fade_years` 년에 걸쳐 선형으로 0 에
수렴한다고 두고, 잔여이익의 현재가치를 더한 값이 오늘 시총과 같아지는 시작 ROE 를 이분법으로 찾는다.
배당성향만큼 순이익이 장부가에 재투자된다(청산잉여관계, clean surplus). `fade_years` 해를 넘는
구간은 초과 ROE 가 정확히 0 이라 가정하므로 별도의 터미널 값이 없다.

역DCF: 올해 매출에서 출발해 `horizon_years` 년 동안 매년 같은 비율로 성장한다고 두고, 그 뒤는
`terminal_growth` 로 영구 성장한다고 가정해 FCFF 의 현재가치 합이 오늘 EV 와 같아지는 성장률을
이분법으로 찾는다. 재투자는 매출증분 ÷ sales-to-capital 로 어림한다(Damodaran 관행).
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "BisectionResult",
    "after_tax_cost_of_debt",
    "bisect",
    "cost_of_equity",
    "reverse_dcf_ev",
    "implied_growth",
    "implied_roe",
    "rim_value",
    "wacc",
]

# Bisection search ranges: ROE/growth outside these are not reported, only flagged as unsolved.
_ROE_RANGE = (-0.5, 1.5)
_GROWTH_RANGE = (-0.5, 2.0)
_TOLERANCE = 1e-7
_MAX_ITER = 200


def cost_of_equity(risk_free: float, beta: float, erp: float) -> float:
    """CAPM 자기자본비용 = 무위험이자율 + beta × ERP. 모든 입력·출력은 소수."""
    return risk_free + beta * erp


def after_tax_cost_of_debt(cost_of_debt: float, tax_rate: float) -> float:
    return cost_of_debt * (1 - tax_rate)


def wacc(market_cap: float, debt: float, cost_of_equity: float, after_tax_cost_of_debt: float) -> float | None:
    """시가총액·차입금의 시장가치 가중평균. 분모가 0 이하면 계산할 수 없다(None)."""
    total = market_cap + debt
    if total <= 0:
        return None
    equity_weight = market_cap / total
    debt_weight = debt / total
    return equity_weight * cost_of_equity + debt_weight * after_tax_cost_of_debt


@dataclass(frozen=True, slots=True)
class BisectionResult:
    value: float | None
    reason: str | None  # None이면 value가 해, 아니면 못 찾은 이유


def bisect(
    f, target: float, lo: float, hi: float, *, tol: float = _TOLERANCE, max_iter: int = _MAX_ITER
) -> BisectionResult:
    """f(x) = target 을 [lo, hi] 안에서 찾는다. f 는 단조 증가/감소 어느 쪽이든 된다.

    f(lo), f(hi) 중 하나라도 None 이거나 두 끝값이 target 을 사이에 두지 않으면 해가 없다고 본다.
    """
    f_lo = f(lo)
    f_hi = f(hi)
    if f_lo is None or f_hi is None:
        return BisectionResult(None, "f_undefined_at_bracket")
    d_lo = f_lo - target
    d_hi = f_hi - target
    if d_lo == 0:
        return BisectionResult(lo, None)
    if d_hi == 0:
        return BisectionResult(hi, None)
    if (d_lo > 0) == (d_hi > 0):
        return BisectionResult(None, "no_solution_in_range")

    mid = (lo + hi) / 2
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if f_mid is None:
            return BisectionResult(None, "f_undefined_inside_range")
        d_mid = f_mid - target
        if abs(d_mid) < tol or (hi - lo) < tol:
            return BisectionResult(mid, None)
        if (d_mid > 0) == (d_lo > 0):
            lo, d_lo = mid, d_mid
        else:
            hi, d_hi = mid, d_mid
    return BisectionResult(mid, None)


def rim_value(b0: float, roe0: float, cost_of_equity: float, fade_years: int, payout_ratio: float) -> float:
    """B0 + 잔여이익의 현재가치. `roe0` 는 올해(1년차) ROE, 그 뒤 `fade_years` 년에 걸쳐 자기자본비용으로
    선형 수렴한다(1년차 100% 초과분 → fade_years 년차 1/fade_years 초과분 → 그 다음은 0).
    """
    if fade_years <= 0:
        return b0
    book = b0
    pv_sum = 0.0
    excess0 = roe0 - cost_of_equity
    for t in range(1, fade_years + 1):
        remaining = (fade_years - t + 1) / fade_years
        roe_t = cost_of_equity + excess0 * remaining
        residual_income = (roe_t - cost_of_equity) * book
        pv_sum += residual_income / (1 + cost_of_equity) ** t
        book = book * (1 + roe_t * (1 - payout_ratio))
    return b0 + pv_sum


def implied_roe(
    market_cap: float,
    b0: float,
    cost_of_equity: float,
    fade_years: int,
    payout_ratio: float,
    *,
    lo: float = _ROE_RANGE[0],
    hi: float = _ROE_RANGE[1],
) -> BisectionResult:
    """시총을 RIM 가치와 같게 만드는 1년차 ROE. b0 가 0 이하면 계산할 수 없다."""
    if b0 <= 0:
        return BisectionResult(None, "non_positive_book_equity")

    def f(roe0: float) -> float:
        return rim_value(b0, roe0, cost_of_equity, fade_years, payout_ratio)

    return bisect(f, market_cap, lo, hi)


def reverse_dcf_ev(
    revenue0: float,
    growth: float,
    operating_margin: float,
    tax_rate: float,
    sales_to_capital: float,
    wacc_rate: float,
    horizon_years: int,
    terminal_growth: float,
) -> float | None:
    """`horizon_years` 년 동안 매년 `growth` 로 성장, 그 뒤 `terminal_growth` 영구성장을 가정한 EV.

    FCFF = 매출 × 영업이익률 × (1 − 세율) − 재투자, 재투자 = 매출증분 ÷ sales_to_capital.
    wacc_rate <= terminal_growth 면(터미널 가치가 발산) None.
    sales_to_capital 은 양수여야 한다 — 0 을 "재투자 없음"으로 읽으면 0 에 가까울수록 커져야 할 재투자가
    사라져 EV 가 부푼다.
    """
    if sales_to_capital <= 0:
        raise ValueError(f"sales_to_capital must be positive, got {sales_to_capital}")
    revenue = revenue0
    pv = 0.0
    for t in range(1, horizon_years + 1):
        new_revenue = revenue * (1 + growth)
        delta = new_revenue - revenue
        nopat = new_revenue * operating_margin * (1 - tax_rate)
        reinvestment = delta / sales_to_capital
        fcff = nopat - reinvestment
        pv += fcff / (1 + wacc_rate) ** t
        revenue = new_revenue

    if wacc_rate <= terminal_growth:
        return None
    terminal_revenue = revenue * (1 + terminal_growth)
    terminal_delta = terminal_revenue - revenue
    terminal_nopat = terminal_revenue * operating_margin * (1 - tax_rate)
    terminal_reinvestment = terminal_delta / sales_to_capital
    terminal_fcff = terminal_nopat - terminal_reinvestment
    terminal_value = terminal_fcff / (wacc_rate - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc_rate) ** horizon_years
    return pv + pv_terminal


def implied_growth(
    ev_target: float,
    revenue0: float,
    operating_margin: float,
    tax_rate: float,
    sales_to_capital: float,
    wacc_rate: float,
    horizon_years: int,
    terminal_growth: float,
    *,
    lo: float = _GROWTH_RANGE[0],
    hi: float = _GROWTH_RANGE[1],
) -> BisectionResult:
    """오늘 EV 를 역DCF 가치와 같게 만드는 명시적 구간 매출성장률."""
    if revenue0 <= 0:
        return BisectionResult(None, "non_positive_revenue")
    if wacc_rate <= terminal_growth:
        return BisectionResult(None, "wacc_not_above_terminal_growth")

    def f(growth: float) -> float | None:
        return reverse_dcf_ev(
            revenue0, growth, operating_margin, tax_rate, sales_to_capital, wacc_rate, horizon_years, terminal_growth
        )

    return bisect(f, ev_target, lo, hi)
