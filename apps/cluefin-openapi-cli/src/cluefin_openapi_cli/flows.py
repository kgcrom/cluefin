"""Window stats for `kis stock flow-summary` — who is buying/selling one stock, by window.

Pure functions only — no KIS calls, no buy/sell labels (same discipline as `investor_metrics.py`/
`quality.py`). The handler passes each series' rows **as the KIS client returns them**: every row is
still `str`-valued (pydantic passthrough), and every one of the five series is sorted **newest first**
(verified on three stocks — large-, small-cap and a financial — 2026-11-11). A `None` means the field
was empty or the row was missing, never 0.

Unit quirks measured the same day (not in the portal docs, only in the live body):

- `investor-trade-by-stock-daily` (FHPTJ04160001): `*_ntby_qty` is 주 (shares, raw), `*_ntby_tr_pbmn`
  is **백만원**, but `acml_tr_pbmn` (turnover) in the *same row* is **raw 원** — two units in one
  endpoint. Confirmed on all three sampled stocks: `frgn_ntby_qty × close ≈ frgn_ntby_tr_pbmn × 1e6`.
  Only **30** rows come back per call and there is no continuation key — the handler pages by date
  (`_dated_pages`: the day before the oldest row).
- `program-trade-by-stock-daily` (FHPPG04650201): `*_tr_pbmn` is raw 원 (`whol_smtn_ntby_qty × close ≈
  whol_smtn_ntby_tr_pbmn`). Also 30 rows a call, paged by date the same way.
- `credit-balance-trend-daily` (FHPST04760000): `*_amt` is 만원, matching the field `description` —
  confirmed by order of magnitude against `rmnd_stcn × close`. 30 rows a call, paged by date. Its `deal_date` lags
  (T+2 vs. the other series' `stck_bsop_date`) — confirmed: querying with today's date still returned a
  most-recent row several calendar days back (settlement, not quote, basis).
- `stock-loan-trend-daily` (existing handler, FHPST04773000-style `analysis.stock_loan_trend`):
  `rmnd_amt` is **백만원** — confirmed exactly (`rmnd_stcn × close ÷ 1e6 == rmnd_amt`). Row count follows
  the requested `start_date`/`end_date` window (the handler already supports `cts` paging).
- `short-selling-trend-daily` (existing handler, `analysis.short_selling_trend`): `*_tr_pbmn` is raw 원.
  Up to **100** rows come back in one call.

None of the five series carries a 상장주식수/발행주식 분모 or an 외국인 지분율 field, so
`foreign_ownership` and the "상장주식 대비 %" parts of `stock_loan`/`credit` are always `null` with a
`reason` — this module never reaches outside the response for a missing denominator.
"""

from __future__ import annotations

from typing import Any


def to_number(raw: str | None) -> float | None:
    """KIS numeric fields are strings; empty string/None means missing, never 0."""

    if raw is None:
        return None
    text = raw.strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _field(row: dict[str, Any], name: str) -> float | None:
    return to_number(row.get(name))


def window_flow_stats(
    rows: list[dict[str, Any]],
    *,
    pbmn_field: str,
    pbmn_scale: float,
    turnover_field: str,
    turnover_scale: float,
    window: int,
) -> dict[str, Any]:
    """순매수 금액 합·창 거래대금 대비 %·순매수일 비율, over the first `window` rows (newest first)."""

    window_rows = rows[:window]
    net_buys = [_field(r, pbmn_field) for r in window_rows]
    turnovers = [_field(r, turnover_field) for r in window_rows]
    usable_net = [v for v in net_buys if v is not None]
    usable_turnover = [v for v in turnovers if v is not None]
    net_buy_amount = sum(v * pbmn_scale for v in usable_net) if usable_net else None
    window_turnover = sum(v * turnover_scale for v in usable_turnover) if usable_turnover else None
    pct_of_turnover = None
    if net_buy_amount is not None and window_turnover:
        pct_of_turnover = net_buy_amount / window_turnover * 100
    net_buy_day_ratio = None
    if usable_net:
        net_buy_day_ratio = sum(1 for v in usable_net if v > 0) / len(usable_net) * 100
    return {
        "net_buy_amount": net_buy_amount,
        "window_turnover": window_turnover,
        "pct_of_window_turnover": pct_of_turnover,
        "net_buy_day_ratio": net_buy_day_ratio,
        "rows_used": len(usable_net),
        "rows_requested": window,
    }


def current_streak(rows: list[dict[str, Any]], pbmn_field: str) -> int | None:
    """Consecutive net-buy(+)/net-sell(-) days ending at `rows[0]` (the most recent row).

    Independent of any display window — it runs over every row the series has until the sign
    changes or a row is missing the field. `None` if the first row itself is missing.
    """

    if not rows:
        return None
    first = _field(rows[0], pbmn_field)
    if first is None or first == 0:
        return None
    sign = 1 if first > 0 else -1
    count = 0
    for row in rows:
        value = _field(row, pbmn_field)
        if value is None or (value > 0) != (sign > 0) or value == 0:
            break
        count += 1
    return count * sign


def level_window_stats(
    rows: list[dict[str, Any]],
    *,
    value_field: str,
    scale: float,
    window: int,
) -> dict[str, Any]:
    """잔고(주식 수·금액) 최근값과 창 시작 대비 변화율. `rows` is newest first."""

    if not rows:
        return {"latest": None, "window_start": None, "change_pct": None, "rows_used": 0, "rows_requested": window}
    latest = _field(rows[0], value_field)
    window_rows = rows[:window]
    window_start = _field(window_rows[-1], value_field) if window_rows else None
    change_pct = None
    if latest is not None and window_start is not None and window_start != 0:
        change_pct = (latest - window_start) / abs(window_start) * 100
    latest_scaled = None if latest is None else latest * scale
    start_scaled = None if window_start is None else window_start * scale
    return {
        "latest": latest_scaled,
        "window_start": start_scaled,
        "change_pct": change_pct,
        "rows_used": len(window_rows),
        "rows_requested": window,
    }


def _percentile_rank(values: list[float], target: float) -> float:
    """0~99 백분위, 평균순위로 동점 처리 (cache/breadth._percentile_rank 와 같은 관례, numpy 없이)."""

    n = len(values)
    if n == 0:
        return 0.0
    less = sum(1 for v in values if v < target)
    equal = sum(1 for v in values if v == target)
    return (less + (equal - 1) / 2) / n * 100 if n > 1 else 0.0


def short_selling_stats(rows: list[dict[str, Any]], *, ratio_field: str, window: int) -> dict[str, Any]:
    """공매도 비중(%) 최근값·창 평균·받은 구간(전체 받은 행) 내 백분위."""

    population = [_field(r, ratio_field) for r in rows]
    usable_population = [v for v in population if v is not None]
    if not usable_population:
        return {"latest": None, "window_avg": None, "percentile": None, "rows_used": 0, "rows_requested": window}
    latest = usable_population[0] if population and population[0] is not None else None
    window_values = [v for v in population[:window] if v is not None]
    window_avg = sum(window_values) / len(window_values) if window_values else None
    percentile = _percentile_rank(usable_population, latest) if latest is not None else None
    return {
        "latest": latest,
        "window_avg": window_avg,
        "percentile": percentile,
        "rows_used": len(window_values),
        "rows_requested": window,
    }


def program_window_stats(
    rows: list[dict[str, Any]],
    *,
    pbmn_field: str,
    scale: float,
    window: int,
) -> dict[str, Any]:
    """창별 순매수 금액 합만 (프로그램 매매는 별도 투자자 구분이 없다)."""

    window_rows = rows[:window]
    values = [_field(r, pbmn_field) for r in window_rows]
    usable = [v for v in values if v is not None]
    net_buy_amount = sum(v * scale for v in usable) if usable else None
    return {"net_buy_amount": net_buy_amount, "rows_used": len(usable), "rows_requested": window}
