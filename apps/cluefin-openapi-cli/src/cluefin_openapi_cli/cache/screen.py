"""`cache screen`: a factor table over every stock, filtered by a user `--where` expression.

Decided 2026-11-11 (`docs/plans/investor-toolkit-plan.md` track C). Unlike `cache magic-formula`
(one fixed screen), this is a general table of per-stock factor values — no label, no score, no
built-in preset. The caller supplies the condition (`--where`) or a named preset read from
`research/screens.toml` (gitignored, user-owned — never written by this module).

- Universe: `cache.trend._universe` (그날 상장 보통주, 스팩 제외, KOSPI/KOSDAQ) — **financials
  included**, unlike `cache magic-formula`'s exclusion, because PER/PBR are meaningful for banks
  and insurers too. `--market`/`--sector`/`--industry`/`--code` narrow the output rows only; every
  percentile-based factor (`rs_1m`) is still ranked against the full universe first (same rule as
  `cache rs`), so narrowing the output never changes another row's percentile.
- Financials come from `cache financials` (DART `fnlttMultiAcnt`): each stock's latest cached
  fiscal year whose 사업보고서 was due by ``as_of`` (`cache.magic._last_filed_year`, reused rather
  than redefined). EV and invested capital reuse `cache.magic.enterprise_value`/`invested_capital`
  — the same cash/debt-breakout approximation documented in that module's docstring.
  `earnings_yield`/`roic` are forced to `null` for 금융·증권·보험·전기/가스 (`cache.magic.
  EXCLUDED_SECTORS`) because that approximation does not hold for them — the other factors (per,
  pbr, roe, …) still compute for those sectors, only these two are excluded (narrower than
  `magic-formula`, which drops the sector from the whole table).
- Market cap = that day's raw close × current `company.list_count` (same approximation as
  `cache/magic.py`/`cache/baserate.py` — the cache has no historical share count).
- Price-based factors (`rs_1m`, `ret_3m`/`ret_6m`/`ret_12m`, `high_52w_gap`, `above_ma50`,
  `value_20d`) are computed in one SQL pass per stock using window functions (`lag`, rolling
  `max`/`avg`) — no per-stock query. Prices are **adjusted** (matching `cache rs`/`cache breadth`/
  `cache trend-setup`), `value_20d` (20-day average turnover) uses the raw `value` column (already
  원화, adjustment does not apply to trading value).
- `--where`: comma-separated `factor<op>value` (`< <= > >= = !=`), parsed with one flat regex —
  never `eval`. An unknown factor or a malformed condition is `exit 2` with `issues[]`. A stock
  whose value for a used factor is `null` fails that condition and is counted per-factor in
  `dropped_null` (not folded into the plain fail count, since a screen with many `null`s silently
  shrinking the result is a different failure mode than "the number did not qualify").
- `--preset NAME` reads `research/screens.toml` (same root as `review record`'s `research/` —
  `review.paths.research_root`, so a worktree still reads the **main checkout's** file). Missing
  file or missing preset name is `exit 2` with an example to copy. `--where`/`--sort` together with
  `--preset` is also `exit 2` — one source of truth per call.
- No label, no combined score: only values, `null` for anything undefined, and `notes` for the
  approximations above (same discipline as `quality.py`/`investor_metrics.py`).
"""

from __future__ import annotations

import operator as _operator
import re
from collections.abc import Callable
from datetime import date
from typing import Any

import duckdb
import numpy as np

from cluefin_openapi_cli.cache import trend as cache_trend
from cluefin_openapi_cli.cache.breadth import _percentile_rank, _round_half_up
from cluefin_openapi_cli.cache.magic import EXCLUDED_SECTORS, _last_filed_year, enterprise_value, invested_capital
from cluefin_openapi_cli.errors import EXIT_USAGE, CliError

__all__ = ["DEFAULT_TOP", "FACTORS", "ScreenCondition", "factor_catalog", "parse_where", "screen"]

DEFAULT_TOP = 50

# 21/63/126/252 trading days ~= 1/3/6/12 calendar months of sessions.
_RET_WINDOWS = {"rs_1m": 21, "ret_3m": 63, "ret_6m": 126, "ret_12m": 252}
_HIGH_WINDOW = 250
_SMA_WINDOW = 50
_VALUE_WINDOW = 20

_ACCOUNTS = ("영업이익", "자산총계", "유동부채", "부채총계", "자본총계", "매출액", "당기순이익")
# `cache financials` stores DART's `fnlttMultiAcnt` `account_nm` verbatim (not normalized against
# `cache.financials.ACCOUNT_NAMES`) — the live cache has **no** bare "당기순이익" row at all, only
# "당기순이익(손실)" (2026-11-11 실측, 12,595 rows), and a 241-row minority of "영업이익(손실)"
# alongside the 12,364-row bare "영업이익". Fetch both spellings and fold the suffixed one onto the
# canonical name (bare always wins if both are present for the same code/year).
_ACCOUNT_ALIASES = {"영업이익(손실)": "영업이익", "당기순이익(손실)": "당기순이익"}
_QUERY_ACCOUNTS = (*_ACCOUNTS, *_ACCOUNT_ALIASES)

# (factor, definition) — the source of `cache screen --factors true`. Order is display order.
FACTORS: tuple[tuple[str, str], ...] = (
    ("mcap", "시총 = 그날 원주가 × 현재 company.list_count 근사 (원)."),
    ("value_20d", "20거래일 평균 거래대금 (원, 원주가 value 컬럼 그대로)."),
    ("per", "시총 / 당기순이익(최신 사업연도). 당기순이익<=0 이면 null."),
    ("pbr", "시총 / 자본총계(최신 사업연도). 자본총계<=0 이면 null."),
    ("psr", "시총 / 매출액(최신 사업연도). 매출액<=0 이면 null."),
    ("earnings_yield", "영업이익 / EV(cache.magic.enterprise_value). 금융·증권·보험·전기가스는 null."),
    ("roe", "당기순이익 / 자본총계 * 100 (%). 자본총계<=0 이면 null."),
    ("opm", "영업이익 / 매출액 * 100 (%). 매출액<=0 이면 null."),
    ("debt_ratio", "부채총계 / 자본총계 * 100 (%). 자본총계<=0 이면 null."),
    ("roic", "영업이익 / 투하자본(cache.magic.invested_capital). 금융·증권·보험·전기가스는 null."),
    ("revenue_yoy", "최근 두 공시연도 매출액 증감률(%) — 연속 연도가 아닐 수 있다."),
    ("op_yoy", "최근 두 공시연도 영업이익 증감률(%) — 연속 연도가 아닐 수 있다."),
    ("revenue_cagr_3y", "최근 공시연도와 그 3번째 전 공시연도 매출액의 연평균 성장률(%) — 4개 연도 미만이면 null."),
    ("rs_1m", "21거래일 수정주가 수익률의 전 종목(cache rs 와 같은 유니버스) 횡단면 백분위 (0~99)."),
    ("ret_3m", "63거래일 수정주가 수익률(%)."),
    ("ret_6m", "126거래일 수정주가 수익률(%)."),
    ("ret_12m", "252거래일 수정주가 수익률(%)."),
    ("high_52w_gap", "(수정종가 / 당일 제외 직전 250거래일 최고 수정고가 − 1) * 100 (%, 음수)."),
    ("above_ma50", "수정종가 >= 50거래일 단순이동평균(수정종가)이면 1, 아니면 0. 데이터 50거래일 미만이면 null."),
)
FACTOR_NAMES = frozenset(name for name, _ in FACTORS)
# Factors that reuse cache.magic's EV/invested-capital approximation and are null for its excluded sectors.
_EV_BASED_FACTORS = ("earnings_yield", "roic")

_NOTES = (
    "유니버스는 cache.trend._universe(그날 상장 보통주, 스팩 제외, KOSPI/KOSDAQ) — 금융 포함(PER/PBR 은 금융도 "
    "의미가 있다). --market/--sector/--industry/--code 는 출력 행만 좁히고, rs_1m 백분위는 항상 전 종목 기준이다.",
    "시총 = 그날 원주가 × 현재 company.list_count 근사다 — 캐시에 과거 상장주식수가 없다.",
    "재무는 cache financials(DART fnlttMultiAcnt)의 종목별 최신 사업연도 1개년이다. EV·투하자본은 cache/magic.py "
    "의 근사(현금·이자부채 구분 없음)를 그대로 쓴다 — earnings_yield·roic 는 금융·증권·보험·전기/가스에서 null.",
    "가격은 수정주가(close * adj_factor)다 — cache rs/breadth/trend-setup 과 같은 관례. value_20d 만 원주가 "
    "거래대금(조정 불필요)이다.",
    "revenue_yoy/op_yoy/revenue_cagr_3y 는 연속된 연도를 보장하지 않는다 — 캐시에 있는 공시연도 중 최근 "
    "것들의 비교다. 공시연도가 모자라면 null.",
)

_OP_FUNCS: dict[str, Callable[[float, float], bool]] = {
    "<=": _operator.le,
    ">=": _operator.ge,
    "!=": _operator.ne,
    "<": _operator.lt,
    ">": _operator.gt,
    "=": _operator.eq,
}
# Longest operators first so `<=`/`>=`/`!=` are not cut short by the single-character alternatives.
_CONDITION_RE = re.compile(r"^([a-z][a-z0-9_]*)(<=|>=|!=|<|>|=)(-?\d+(?:\.\d+)?)$")


class ScreenCondition:
    """One parsed `--where` clause: ``factor op value``."""

    __slots__ = ("factor", "op", "value")

    def __init__(self, factor: str, op: str, value: float) -> None:
        self.factor = factor
        self.op = op
        self.value = value

    def test(self, row_value: Any) -> bool:
        if row_value is None:
            return False
        if isinstance(row_value, bool):
            row_value = int(row_value)
        return _OP_FUNCS[self.op](float(row_value), self.value)


def factor_catalog() -> dict[str, Any]:
    return {"factors": [{"factor": name, "definition": definition} for name, definition in FACTORS]}


def parse_where(raw: str) -> list[ScreenCondition]:
    """Parse ``factor<op>value,factor<op>value`` — never `eval`. Raises `CliError` (exit 2) with `issues[]`."""

    conditions: list[ScreenCondition] = []
    issues: list[dict[str, str]] = []
    for clause in (part.strip() for part in raw.split(",") if part.strip()):
        match = _CONDITION_RE.match(clause)
        if match is None:
            issues.append({"clause": clause, "problem": "expected `factor<op>value` with op in < <= > >= = !="})
            continue
        factor, op, value_text = match.groups()
        if factor not in FACTOR_NAMES:
            issues.append({"clause": clause, "problem": f"unknown factor `{factor}`"})
            continue
        conditions.append(ScreenCondition(factor, op, float(value_text)))
    if issues:
        raise CliError(
            "`--where` has invalid clauses.",
            exit_code=EXIT_USAGE,
            data={"issues": issues},
            hint="Run `cache screen --factors true` for the factor list.",
        )
    return conditions


# One window-function pass per stock: `rn = 1` (the most recent bar) carries the lagged closes for
# each return horizon and the rolling max/avg needed for the 52-week gap, 50-day SMA and 20-day
# average turnover — no per-stock query (same spirit as `cache.trend._series`'s one columnar read).
_PRICE_SQL = """
WITH adj AS (
  SELECT code, date,
         close * COALESCE(NULLIF(adj_factor, 0), 1) AS adj_close,
         high * COALESCE(NULLIF(adj_factor, 0), 1) AS adj_high,
         volume, value
  FROM ohlcv
  WHERE code IN (SELECT unnest(?::TEXT[])) AND date <= ? AND close > 0
),
windowed AS (
  SELECT *,
    row_number() OVER (PARTITION BY code ORDER BY date DESC) AS rn,
    lag(adj_close, ?) OVER w AS close_1m,
    lag(adj_close, ?) OVER w AS close_3m,
    lag(adj_close, ?) OVER w AS close_6m,
    lag(adj_close, ?) OVER w AS close_12m,
    max(adj_high) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND 1 PRECEDING) AS high_250,
    avg(adj_close) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS sma50,
    count(*) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS sma50_n,
    avg(value) OVER (PARTITION BY code ORDER BY date ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS value_20d
  FROM adj
  WINDOW w AS (PARTITION BY code ORDER BY date)
)
SELECT code, adj_close, close_1m, close_3m, close_6m, close_12m, high_250, sma50, sma50_n, value_20d
FROM windowed WHERE rn = 1
"""

_MCAP_SQL = (
    "SELECT o.code, o.close, c.list_count FROM ohlcv o JOIN company c ON c.code = o.code "
    "WHERE o.date = ? AND o.code IN (SELECT unnest(?::TEXT[])) AND o.close > 0 AND c.list_count IS NOT NULL"
)

_FINANCIALS_SQL = """
SELECT code, year, account_nm, amount
FROM financials
WHERE code IN (SELECT unnest(?::TEXT[])) AND account_nm IN (SELECT unnest(?::TEXT[])) AND year <= ?
"""


def _price_factors(conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date) -> dict[str, dict[str, Any]]:
    if not codes:
        return {}
    rows = conn.execute(
        _PRICE_SQL,
        [
            codes,
            as_of,
            _RET_WINDOWS["rs_1m"],
            _RET_WINDOWS["ret_3m"],
            _RET_WINDOWS["ret_6m"],
            _RET_WINDOWS["ret_12m"],
            _HIGH_WINDOW,
            _SMA_WINDOW - 1,
            _SMA_WINDOW - 1,
            _VALUE_WINDOW - 1,
        ],
    ).fetchall()
    out: dict[str, dict[str, Any]] = {}
    for code, adj_close, close_1m, close_3m, close_6m, close_12m, high_250, sma50, sma50_n, value_20d in rows:
        out[code] = {
            "adj_close": adj_close,
            "ret_1m": (adj_close / close_1m - 1) if close_1m else None,
            "ret_3m": (adj_close / close_3m - 1) * 100 if close_3m else None,
            "ret_6m": (adj_close / close_6m - 1) * 100 if close_6m else None,
            "ret_12m": (adj_close / close_12m - 1) * 100 if close_12m else None,
            "high_52w_gap": (adj_close / high_250 - 1) * 100 if high_250 else None,
            "above_ma50": int(adj_close >= sma50) if sma50_n == _SMA_WINDOW and sma50 is not None else None,
            "value_20d": value_20d,
        }
    return out


def _financials_by_code(
    conn: duckdb.DuckDBPyConnection, codes: list[str], as_of: date
) -> dict[str, list[tuple[str, dict[str, float]]]]:
    """``{code: [(year, {account: amount}), ...]}``, most recent cached fiscal year first."""

    if not codes:
        return {}
    rows = conn.execute(_FINANCIALS_SQL, [codes, list(_QUERY_ACCOUNTS), str(_last_filed_year(as_of))]).fetchall()
    by_code: dict[str, dict[str, dict[str, float]]] = {}
    for code, year, account_nm, amount in rows:
        canonical = _ACCOUNT_ALIASES.get(account_nm, account_nm)
        year_accounts = by_code.setdefault(code, {}).setdefault(year, {})
        # The bare (canonical) spelling always wins over the "(손실)" alias, regardless of row order.
        if canonical not in year_accounts or account_nm not in _ACCOUNT_ALIASES:
            year_accounts[canonical] = amount
    return {code: sorted(years.items(), key=lambda item: item[0], reverse=True) for code, years in by_code.items()}


_RATIO_FIELDS = (
    "fiscal_year",
    "ebit",
    "total_liab",
    "equity",
    "revenue",
    "net_income",
    "roe",
    "opm",
    "debt_ratio",
    "roic",
    "revenue_yoy",
    "op_yoy",
    "revenue_cagr_3y",
)


def _financial_ratios(years: list[tuple[str, dict[str, float]]], sector: str | None) -> dict[str, Any]:
    """Ratios from the latest cached fiscal year, plus the raw accounts the caller needs for per/pbr/psr/EV.

    `per`/`pbr`/`psr`/`earnings_yield` are left to the caller — they need `mcap`, which this function
    (given only `financials` rows) does not have.
    """

    out: dict[str, Any] = dict.fromkeys(_RATIO_FIELDS, None)
    if not years:
        return out
    latest_year, latest = years[0]
    ebit, assets, current_liab, total_liab, equity, revenue, net_income = (
        latest.get(name)
        for name in ("영업이익", "자산총계", "유동부채", "부채총계", "자본총계", "매출액", "당기순이익")
    )
    out.update(
        fiscal_year=latest_year, ebit=ebit, total_liab=total_liab, equity=equity, revenue=revenue, net_income=net_income
    )
    if equity and equity > 0:
        if net_income is not None:
            out["roe"] = round(net_income / equity * 100, 2)
        if total_liab is not None:
            out["debt_ratio"] = round(total_liab / equity * 100, 2)
    if revenue and revenue > 0 and ebit is not None:
        out["opm"] = round(ebit / revenue * 100, 2)
    if sector not in EXCLUDED_SECTORS and ebit is not None and assets is not None and current_liab is not None:
        ic = invested_capital(assets, current_liab)
        if ic > 0:
            out["roic"] = round(ebit / ic * 100, 2)
    if len(years) >= 2:
        _prior_year, prior = years[1]
        prior_revenue = prior.get("매출액")
        prior_ebit = prior.get("영업이익")
        if prior_revenue and prior_revenue > 0 and revenue is not None:
            out["revenue_yoy"] = round((revenue / prior_revenue - 1) * 100, 2)
        if prior_ebit and prior_ebit > 0 and ebit is not None:
            out["op_yoy"] = round((ebit / prior_ebit - 1) * 100, 2)
    if len(years) >= 4:
        oldest_year, oldest = years[3]
        oldest_revenue = oldest.get("매출액")
        span = int(latest_year) - int(oldest_year)
        if oldest_revenue and oldest_revenue > 0 and revenue is not None and revenue > 0 and span > 0:
            out["revenue_cagr_3y"] = round(((revenue / oldest_revenue) ** (1 / span) - 1) * 100, 2)
    return out


def screen(
    conn: duckdb.DuckDBPyConnection,
    as_of: date,
    *,
    market: str | None = None,
    sector: str | None = None,
    industry: str | None = None,
    codes: list[str] | None = None,
    where: list[ScreenCondition] | None = None,
    sort: str | None = None,
    top: int | None = None,
) -> dict[str, Any]:
    """Factor table for every stock in the universe, filtered to ``--market``/``--sector``/`` --industry``/``--code``."""

    full_universe = cache_trend._universe(conn, as_of, None, None)
    all_codes = [row["code"] for row in full_universe]

    prices = _price_factors(conn, all_codes, as_of)
    rs_codes = [code for code in all_codes if code in prices and prices[code]["ret_1m"] is not None]
    rs_values = np.array([prices[code]["ret_1m"] for code in rs_codes], dtype=np.float64)
    rs_rank = dict(zip(rs_codes, _percentile_rank(rs_values), strict=True))

    mcap_rows = conn.execute(_MCAP_SQL, [as_of, all_codes]).fetchall() if all_codes else []
    mcaps = {code: close * list_count for code, close, list_count in mcap_rows}

    financials = _financials_by_code(conn, all_codes, as_of)

    wanted_codes = set(codes) if codes else None
    selected = [
        row
        for row in full_universe
        if (market is None or row["market"] == market)
        and (sector is None or row["sector"] == sector)
        and (industry is None or row["industry"] == industry)
        and (wanted_codes is None or row["code"] in wanted_codes)
    ]

    candidates: list[dict[str, Any]] = []
    for row in selected:
        code = row["code"]
        mcap = mcaps.get(code)
        price = prices.get(code, {})
        fin = _financial_ratios(financials.get(code, []), row["sector"])
        ebit, total_liab, equity, revenue, net_income = (
            fin.pop("ebit"),
            fin.pop("total_liab"),
            fin.pop("equity"),
            fin.pop("revenue"),
            fin.pop("net_income"),
        )

        candidate: dict[str, Any] = {
            "code": code,
            "name": row["name"],
            "market": row["market"],
            "sector": row["sector"],
            "industry": row["industry"],
            "mcap": round(mcap, 0) if mcap is not None else None,
            "value_20d": round(price.get("value_20d"), 0) if price.get("value_20d") is not None else None,
            "per": None,
            "pbr": None,
            "psr": None,
            "earnings_yield": None,
            "rs_1m": _round_half_up(rs_rank[code]) if code in rs_rank else None,
            "ret_3m": round(price["ret_3m"], 2) if price.get("ret_3m") is not None else None,
            "ret_6m": round(price["ret_6m"], 2) if price.get("ret_6m") is not None else None,
            "ret_12m": round(price["ret_12m"], 2) if price.get("ret_12m") is not None else None,
            "high_52w_gap": round(price["high_52w_gap"], 2) if price.get("high_52w_gap") is not None else None,
            "above_ma50": price.get("above_ma50"),
            **fin,
        }
        if mcap is not None:
            if net_income is not None and net_income > 0:
                candidate["per"] = round(mcap / net_income, 2)
            if equity is not None and equity > 0:
                candidate["pbr"] = round(mcap / equity, 2)
            if revenue is not None and revenue > 0:
                candidate["psr"] = round(mcap / revenue, 2)
            if total_liab is not None and ebit is not None and row["sector"] not in EXCLUDED_SECTORS:
                ev = enterprise_value(mcap, total_liab)
                if ev > 0:
                    candidate["earnings_yield"] = round(ebit / ev * 100, 2)
        candidates.append(candidate)

    dropped_null: dict[str, int] = {}
    if where:
        kept = []
        for row in candidates:
            ok = True
            for condition in where:
                value = row.get(condition.factor)
                if value is None:
                    dropped_null[condition.factor] = dropped_null.get(condition.factor, 0) + 1
                    ok = False
                elif not condition.test(value):
                    ok = False
            if ok:
                kept.append(row)
        candidates = kept

    if sort is not None:
        candidates.sort(key=lambda row: (row.get(sort) is None, -(row.get(sort) or 0)))
    else:
        candidates.sort(key=lambda row: row["code"])

    rows = candidates[: top if top is not None else DEFAULT_TOP]
    return {
        "as_of": as_of.isoformat(),
        "universe": len(full_universe),
        "matched": len(candidates),
        "where": [f"{c.factor}{c.op}{c.value:g}" for c in (where or [])],
        "dropped_null": dropped_null,
        "sort": sort,
        "count": len(rows),
        "rows": rows,
        "notes": list(_NOTES),
    }
