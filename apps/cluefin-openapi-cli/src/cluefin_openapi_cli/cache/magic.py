"""`cache magic-formula`: Greenblatt's Magic Formula over the cache's cross-section.

Earnings yield (EBIT/EV) and return on invested capital, ranked and summed — Joel Greenblatt's
screen (*The Little Book That Beats the Market*). Universe and inputs decided 2026-11-04
(`docs/plans/today-bundles-plan.md` B-22):

- Universe excludes financials/insurance/utilities (Greenblatt's own exclusion — their EV and
  capital structure are not comparable), 관리종목(`company.is_admin`)·거래정지
  (`company.is_halted`), and the bottom 20% of the remaining universe by market cap. Sector
  comes from Kiwoom's 26-group `company.sector` (the same field `cache rs`'s `--by sector`
  groups on): `금융`·`증권`·`보험`·`전기/가스` are dropped. Otherwise the same universe rule as
  `cache trend-setup`/`cache rs` (`cache.trend._universe`): common stock listed on the day, no
  SPACs, KOSPI/KOSDAQ only.
- Financials come from `cache financials` (DART `fnlttMultiAcnt`, see `cache/financials.py`):
  each stock's latest cached fiscal year whose 사업보고서 was due by ``as_of`` (March 31 of the next
  year — a past ``--as-of`` must not see a later filing), 영업이익(operating profit) standing in for EBIT — the
  endpoint has no EBIT line, same substitution as `dart financial-summary`'s `quality` block.
  Market cap is that day's raw close (pre-adjustment) × current `company.list_count` (same
  approximation as `cache/baserate.py`; the cache has no historical share count).
- **Accounts are limited — this is not Greenblatt's exact definition.** `financials` has no
  cash line and no interest-bearing-debt breakout (only 유동부채/비유동부채/부채총계 totals,
  which include non-interest-bearing items like trade payables). So, documented in every
  payload's `notes`:
  - EV = market cap + 부채총계(total liabilities) — a net-debt proxy with no cash netted out.
    Overstates EV for cash-rich firms (depresses their earnings yield).
  - Invested capital = 자산총계 − 유동부채. Algebraically this is (유동자산 − 유동부채) +
    비유동자산 — Greenblatt's net working capital + net fixed assets, since
    유동자산 + 비유동자산 = 자산총계. Overstates both legs a little: 유동자산 still carries
    cash/short-term investments that Greenblatt's "excess cash" adjustment would strip out of
    working capital, and 비유동자산 carries intangibles/investments beyond net PP&E.
- Ranking reuses `cache.breadth._percentile_rank` (0-99, average-rank ties) on each of the two
  metrics and sums them — not Greenblatt's ordinal 1..N rank sum, so here higher is better (a
  0-198 percentile sum) rather than lower is better (an ordinal sum). Sorted descending;
  `--top N` (default 30) trims the output, not the ranking population.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.cache import trend as cache_trend
from cluefin_openapi_cli.cache.breadth import _percentile_rank, _round_half_up

__all__ = ["DEFAULT_TOP", "screen"]

DEFAULT_TOP = 30

# Kiwoom's `company.sector` (upName, 26 coarse groups) — Greenblatt excludes financials and
# utilities because their EV/invested-capital ratios are not comparable to operating companies.
_EXCLUDED_SECTORS = frozenset({"금융", "증권", "보험", "전기/가스"})
_BOTTOM_MCAP_PCT = 0.20

_ACCOUNTS = ("영업이익", "자산총계", "유동부채", "부채총계")

_FINANCIALS_SQL = """
WITH ranked AS (
  SELECT code, year, account_nm, amount,
         dense_rank() OVER (PARTITION BY code ORDER BY year DESC) AS yr_rank
  FROM financials
  WHERE code IN (SELECT unnest(?::TEXT[])) AND account_nm IN (SELECT unnest(?::TEXT[])) AND year <= ?
)
SELECT code, year, account_nm, amount FROM ranked WHERE yr_rank = 1
"""

_MCAP_SQL = (
    "SELECT o.code, o.close, c.list_count FROM ohlcv o JOIN company c ON c.code = o.code "
    "WHERE o.date = ? AND o.code IN (SELECT unnest(?::TEXT[])) AND o.close > 0 AND c.list_count IS NOT NULL"
)

_NOTES = (
    "유니버스는 cache.trend._universe(그날 상장 보통주, 스팩 제외, KOSPI/KOSDAQ)에서 금융·증권·보험·전기/가스 "
    "업종(company.sector), 관리종목(is_admin)·거래정지(is_halted)를 빼고, 남은 종목의 시총 하위 20% 를 더 뺀 "
    "것이다(Greenblatt 원칙, 결정 2026-11-04).",
    "재무는 `cache financials`(DART fnlttMultiAcnt)의 종목별 최신 사업연도 1개년이다 — EBIT 는 영업이익으로 "
    "대신한다(영업외손익 구분이 없다). 사업보고서 마감(3월 31일) 전의 as_of 에는 전전 사업연도까지만 쓴다(미래 정보 차단).",
    "시총 = 그날 원주가(수정 전) × 현재 company.list_count 근사다 — 캐시에 과거 상장주식수가 없다 "
    "(cache/baserate.py 와 같은 근사).",
    "EV = 시총 + 부채총계 — `financials` 에 현금·이자부채 구분이 없어 현금을 빼지 못한 근사다. 현금이 많은 "
    "회사일수록 이익수익률이 실제보다 낮게 나온다.",
    "투하자본 = 자산총계 − 유동부채 (순운전자본+순고정자산과 대수적으로 같다, 유동자산+비유동자산=자산총계) — "
    "Greenblatt 의 '초과현금 제외'·'순유형고정자산'을 적용하지 못한 근사다.",
    "두 지표의 순위는 cache.breadth._percentile_rank(0~99, 평균순위 동점 처리)의 합이다 — 원래 마법공식의 "
    "오름차순 서수 합이 아니라 내림차순 백분위 합이다(높을수록 좋음, 0~198).",
    "EBIT<=0, 투하자본<=0, EV<=0 인 종목은 이익수익률·ROIC 를 정의할 수 없어 빼고 `excluded` 로 센다.",
)


def _mcap_by_code(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, float]:
    if not codes:
        return {}
    rows = conn.execute(_MCAP_SQL, [as_of, codes]).fetchall()
    return {code: close * list_count for code, close, list_count in rows}


def _last_filed_year(as_of: date) -> int:
    """The latest fiscal year whose 사업보고서 was due by ``as_of`` (filed within 90 days, i.e. by March 31).

    Without this cap a past ``--as-of`` would rank on a year that was not public yet (look-ahead).
    """

    return as_of.year - 1 if as_of >= date(as_of.year, 4, 1) else as_of.year - 2


def _financials_by_code(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, dict[str, Any]]:
    if not codes:
        return {}
    rows = conn.execute(_FINANCIALS_SQL, [codes, list(_ACCOUNTS), str(_last_filed_year(as_of))]).fetchall()
    by_code: dict[str, dict[str, Any]] = {}
    for code, year, account_nm, amount in rows:
        entry = by_code.setdefault(code, {"year": year, "accounts": {}})
        entry["accounts"][account_nm] = amount
    return by_code


def screen(conn: duckdb.DuckDBPyConnection, as_of: date, *, top: int = DEFAULT_TOP) -> dict[str, Any]:
    """Earnings-yield/ROIC Magic Formula screen for every stock in the universe on ``as_of``."""

    universe = cache_trend._universe(conn, as_of, None, None)
    sector_filtered = [
        row
        for row in universe
        if row["sector"] not in _EXCLUDED_SECTORS and not row["is_admin"] and not row["is_halted"]
    ]

    mcaps = _mcap_by_code(conn, [row["code"] for row in sector_filtered], as_of)
    priced = [row for row in sector_filtered if row["code"] in mcaps]
    no_price = len(sector_filtered) - len(priced)

    # A quantile over a single price is that price itself, which would exclude the only
    # candidate (`>` against its own value) — nothing to call "bottom 20%" of one stock.
    if len(priced) > 1:
        cutoff = float(np.quantile([mcaps[row["code"]] for row in priced], _BOTTOM_MCAP_PCT))
        sized = [row for row in priced if mcaps[row["code"]] > cutoff]
    else:
        sized = list(priced)
    below_cutoff = len(priced) - len(sized)

    financials = _financials_by_code(conn, [row["code"] for row in sized], as_of)

    candidates: list[dict[str, Any]] = []
    metrics: list[tuple[float, float]] = []
    excluded_no_financials = 0
    excluded_non_positive = 0
    for row in sized:
        code = row["code"]
        fin = financials.get(code)
        accounts = fin["accounts"] if fin else {}
        ebit = accounts.get("영업이익")
        assets = accounts.get("자산총계")
        current_liab = accounts.get("유동부채")
        total_liab = accounts.get("부채총계")
        if fin is None or None in (ebit, assets, current_liab, total_liab):
            excluded_no_financials += 1
            continue
        invested_capital = assets - current_liab
        ev = mcaps[code] + total_liab
        if ebit <= 0 or invested_capital <= 0 or ev <= 0:
            excluded_non_positive += 1
            continue
        candidates.append(
            {
                "code": code,
                "name": row["name"],
                "market": row["market"],
                "sector": row["sector"],
                "mcap": round(mcaps[code], 0),
                "fiscal_year": fin["year"],
                "ebit": ebit,
                "ev": round(ev, 0),
                "invested_capital": round(invested_capital, 0),
            }
        )
        metrics.append((ebit / ev, ebit / invested_capital))

    if candidates:
        ey_rank = _percentile_rank(np.array([ey for ey, _ in metrics]))
        roic_rank = _percentile_rank(np.array([roic for _, roic in metrics]))
        combined = ey_rank + roic_rank
        for row, (ey, roic), ey_r, roic_r, both in zip(candidates, metrics, ey_rank, roic_rank, combined, strict=True):
            row["earnings_yield_pct"] = round(ey * 100, 2)
            row["roic_pct"] = round(roic * 100, 2)
            row["earnings_yield_rank"] = _round_half_up(ey_r)
            row["roic_rank"] = _round_half_up(roic_r)
            # Rounded from the unrounded sum, so it can differ by 1 from the two displayed ranks added.
            row["combined_rank"] = _round_half_up(both)
        # Sort on the unrounded sum; rounding each rank first reorders x.5 ties.
        order = sorted(range(len(candidates)), key=lambda i: (-combined[i], candidates[i]["code"]))
        candidates = [candidates[i] for i in order]

    rows = candidates[:top]
    return {
        "as_of": as_of.isoformat(),
        "top": top,
        "universe": len(universe),
        "after_sector_admin_halt": len(sector_filtered),
        "after_mcap_filter": len(sized),
        "ranked": len(candidates),
        "excluded": {
            "no_price_or_list_count": no_price,
            "bottom_mcap_20pct": below_cutoff,
            "no_financials_or_missing_accounts": excluded_no_financials,
            "non_positive_ebit_or_capital_or_ev": excluded_non_positive,
        },
        "count": len(rows),
        "rows": rows,
        "notes": list(_NOTES),
    }
