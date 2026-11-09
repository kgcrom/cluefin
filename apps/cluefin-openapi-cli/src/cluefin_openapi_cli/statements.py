"""Quarterly, annual and latest-period figures out of `dart financial-full-statements` rows.

One report carries three periods: an annual report fills ``thstrm``/``frmtrm``/``bfefrmtrm``
(this year and the two before); a quarterly report fills the quarter in ``thstrm_amount``,
the year-to-date sum in ``thstrm_add_amount``, and the same two for the prior year in
``frmtrm_q_amount``/``frmtrm_add_amount``. Quarters are never filed on their own past Q1,
so Q2–Q4 are year-to-date differences — the 4Q is the annual minus the 9-month sum.

Cash-flow rows in a quarterly report are year-to-date in ``thstrm_amount``.

Ported from cluefin-factory ``scripts/company/statements.mjs`` (archived 2026-10-18); the
definitions were checked there against 192820 and 005930 filings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

from cluefin_openapi_cli.accounts import Item, load_table

QUARTER_OF = {"11013": 1, "11012": 2, "11014": 3, "11011": 4}
PERIOD_LABEL = {1: "Q1", 2: "H1", 3: "9M", 4: "FY"}

INCOME = frozenset({"IS", "CIS"})
BALANCE = frozenset({"BS"})
CASH = frozenset({"CF"})


# Account keys → XBRL ids and labels live in `accounts/common.toml`; file order is output order.
_TABLE = load_table()
# Income-statement items that are summed per quarter.
INCOME_ITEMS: dict[str, Item] = _TABLE["income"]
BALANCE_ITEMS: dict[str, Item] = _TABLE["balance"]
CASH_ITEMS: dict[str, Item] = _TABLE["cash"]

# Bank/insurer/securities accounts (`accounts/financial.toml`), read for every filer: no industry detection.
# They enter the output only when a report has a value for one of the `marker` accounts, which general filers
# never file (a 사채 or FVOCI line alone doesn't make a filer financial).
_FINANCIAL = load_table("financial")
FINANCIAL_BALANCE_ITEMS: dict[str, Item] = _FINANCIAL["balance"]
FINANCIAL_INCOME_ITEMS: dict[str, Item] = _FINANCIAL["income"]
_shared = {*INCOME_ITEMS, *BALANCE_ITEMS, *CASH_ITEMS} & {*FINANCIAL_BALANCE_ITEMS, *FINANCIAL_INCOME_ITEMS}
if _shared:
    raise ValueError(f"financial.toml reuses common account keys: {sorted(_shared)}")
FINANCIAL_MARKERS = frozenset(
    key for items in (FINANCIAL_BALANCE_ITEMS, FINANCIAL_INCOME_ITEMS) for key, item in items.items() if item.marker
)

# Fields in 원 that `to_eok` converts. Ratios and growth reuse item names, so this is explicit.
MONEY_FIELDS = frozenset(
    {
        *INCOME_ITEMS,
        *BALANCE_ITEMS,
        *CASH_ITEMS,
        *FINANCIAL_BALANCE_ITEMS,
        *FINANCIAL_INCOME_ITEMS,
        "borrowings",
        "net_debt",
        "free_cash_flow",
    }
)

EOK = 1e8


@dataclass(frozen=True, slots=True)
class Report:
    """One periodic report's rows as `dart financial-full-statements` returns them."""

    year: int
    reprt_code: str
    rcept_no: str
    rows: list[dict[str, Any]] = field(default_factory=list)

    @property
    def quarter(self) -> int:
        return QUARTER_OF[self.reprt_code]

    @property
    def order(self) -> int:
        return self.year * 10 + self.quarter


def won(text: Any) -> float | None:
    """``"1,234"`` / ``"-5"`` / ``""`` → number or None."""
    if text is None:
        return None
    clean = str(text).replace(",", "").strip()
    if clean in ("", "-"):
        return None
    try:
        return float(clean)
    except ValueError:
        return None


_WHITESPACE = re.compile(r"\s+")


def _squash(text: Any) -> str:
    return _WHITESPACE.sub("", str(text or ""))


Match = Literal["id", "label", "empty", "missing"]


def match_row(rows: list[dict], sections: frozenset[str], item: Item) -> tuple[dict | None, Match]:
    """The row for one item and how it was found: XBRL id first, then the Korean label."""
    in_section = [row for row in rows if row.get("sj_div") in sections]
    for row in in_section:
        if row.get("account_id") in item.ids:
            return row, "id"
    wanted = {_squash(name) for name in item.names}
    for row in in_section:
        if _squash(row.get("account_nm")) in wanted:
            return row, "label"
    return None, "missing"


def find_row(rows: list[dict], sections: frozenset[str], item: Item) -> dict | None:
    """The row for one item: XBRL id first, then the Korean label."""
    return match_row(rows, sections, item)[0]


_COMMON_GROUPS = ((INCOME, INCOME_ITEMS), (BALANCE, BALANCE_ITEMS), (CASH, CASH_ITEMS))
_FINANCIAL_GROUPS = ((INCOME, FINANCIAL_INCOME_ITEMS), (BALANCE, FINANCIAL_BALANCE_ITEMS))


def match_items(rows: list[dict], column: str, *, financial: bool = False) -> dict[str, Match]:
    """How every table account was found in one report column (common accounts, plus financial ones if asked).

    ``id``/``label`` say which key matched; ``empty`` is a matched row with no amount in ``column``; ``missing``
    is no row. A row-level read can't tell "no such transaction" from "filed under another name" — both are
    ``missing``.
    """
    out: dict[str, Match] = {}
    groups = _COMMON_GROUPS + _FINANCIAL_GROUPS if financial else _COMMON_GROUPS
    for sections, items in groups:
        for key, item in items.items():
            row, how = match_row(rows, sections, item)
            out[key] = "empty" if row is not None and won(row.get(column)) is None else how
    return out


# Borrowings have no single XBRL id: 005930 files 단기차입금 off-taxonomy, 000660 files 차입금
# twice, 192820 lumps everything into 단기/장기금융부채. Sum the borrowing lines by label; when a
# filer has none, fall back to financial liabilities and say so.
# 194370 files "단기차입금 및 사채"/"장기차입금 및 사채" (squashed: 단기차입금및사채), so 및사채 is an optional suffix.
_BORROWING = re.compile(r"^(단기|장기|유동성장기|유동성)?(차입금|사채|차입부채|장기부채)(및사채)?$")
_BORROWING_IDS = (
    "ifrs-full_ShorttermBorrowings",
    "ifrs-full_CurrentBorrowingsAndCurrentPortionOfNoncurrentBorrowings",
    "ifrs-full_CurrentPortionOfLongtermBorrowings",
    "ifrs-full_LongtermBorrowings",
    "ifrs-full_NoncurrentPortionOfNoncurrentBorrowings",
    "ifrs-full_Borrowings",
)
_FINANCIAL_LIABILITY_IDS = ("ifrs-full_CurrentFinancialLiabilities", "ifrs-full_NoncurrentFinancialLiabilities")


def borrowings(rows: list[dict], column: str) -> tuple[float | None, str | None]:
    """(amount, basis) of borrowings on the balance sheet; basis says what was counted."""
    balance = [row for row in rows if row.get("sj_div") == "BS"]
    lines = [
        row for row in balance if _BORROWING.match(_squash(row.get("account_nm"))) and won(row.get(column)) is not None
    ]
    if not lines:  # labels off the pattern, but tagged with a borrowing XBRL id
        lines = [row for row in balance if row.get("account_id") in _BORROWING_IDS and won(row.get(column)) is not None]
    if lines:
        names = "+".join(_squash(row.get("account_nm")) for row in lines)
        return sum(won(row.get(column)) for row in lines), f"차입금·사채 ({names})"
    financial = []
    for account_id in _FINANCIAL_LIABILITY_IDS:
        row = next((r for r in balance if r.get("account_id") == account_id), None)
        if row is not None and won(row.get(column)) is not None:
            financial.append(row)
    if not financial:
        return None, None
    return (
        sum(won(row.get(column)) for row in financial),
        "금융부채(단기+장기) — 차입금 계정이 따로 없어 리스·기타 금융부채가 섞일 수 있다",
    )


def _pick(rows: list[dict], sections: frozenset[str], items: dict[str, Item], column: str) -> dict[str, float | None]:
    out = {}
    for key, item in items.items():
        row = find_row(rows, sections, item)
        out[key] = won(row.get(column)) if row is not None else None
    return out


def _financial_figures(rows: list[dict], columns: tuple[str, ...]) -> list[dict[str, float | None]]:
    """Financial-account figures per column, or empty dicts when no marker account has a value (a general filer)."""
    picked = [
        {
            **_pick(rows, INCOME, FINANCIAL_INCOME_ITEMS, column),
            **_pick(rows, BALANCE, FINANCIAL_BALANCE_ITEMS, column),
        }
        for column in columns
    ]
    if not any(figures[key] is not None for figures in picked for key in FINANCIAL_MARKERS):
        return [{} for _ in columns]
    return picked


def _ratio(num: float | None, den: float | None) -> float | None:
    if num is None or den is None or den == 0:
        return None
    return num / den


def _pct(num: float | None, den: float | None) -> float | None:
    r = _ratio(num, den)
    return None if r is None else r * 100


def _first(*values: float | None) -> float | None:
    for value in values:
        if value is not None:
            return value
    return None


def year_to_date(reports: list[Report]) -> dict[int, dict[int, dict[str, float]]]:
    """Year-to-date sums per year and quarter for every income item.

    A year's own report wins over the comparative column of next year's report: reports are
    walked oldest first and a slot is filled only once.
    """
    ytd: dict[int, dict[int, dict[str, float]]] = {}

    def put(year: int, quarter: int, key: str, value: float | None) -> None:
        if value is None:
            return
        slot = ytd.setdefault(year, {1: {}, 2: {}, 3: {}, 4: {}})[quarter]
        slot.setdefault(key, value)

    for report in sorted(reports, key=lambda r: r.order):
        quarter = report.quarter
        for key, item in INCOME_ITEMS.items():
            row = find_row(report.rows, INCOME, item)
            if row is None:
                continue
            if quarter == 4:
                put(report.year, 4, key, won(row.get("thstrm_amount")))
                put(report.year - 1, 4, key, won(row.get("frmtrm_amount")))
                put(report.year - 2, 4, key, won(row.get("bfefrmtrm_amount")))
            else:
                put(report.year, quarter, key, _first(won(row.get("thstrm_add_amount")), won(row.get("thstrm_amount"))))
                put(
                    report.year - 1,
                    quarter,
                    key,
                    _first(won(row.get("frmtrm_add_amount")), won(row.get("frmtrm_q_amount"))),
                )
    return ytd


def growth(current: float | None, previous: float | None) -> float | str | None:
    """Signed change: a number when both sides are positive, otherwise 흑전/적전/적지."""
    if current is None or previous is None:
        return None
    if previous > 0 and current > 0:
        return (current / previous - 1) * 100
    if previous <= 0 < current:
        return "흑전"
    if previous > 0 >= current:
        return "적전"
    return "적지"


def quarters(reports: list[Report]) -> list[dict[str, Any]]:
    """Single quarters, oldest first, with YoY against the same quarter a year earlier."""
    ytd = year_to_date(reports)
    keys = list(INCOME_ITEMS)
    single: dict[str, dict[str, Any]] = {}
    for year, by_quarter in ytd.items():
        for quarter in (1, 2, 3, 4):
            now = by_quarter[quarter]
            before = by_quarter[quarter - 1] if quarter > 1 else None
            values: dict[str, float | None] = {}
            for key in keys:
                if key not in now:
                    values[key] = None
                elif quarter == 1:
                    values[key] = now[key]
                else:
                    values[key] = None if key not in before else now[key] - before[key]
            # Banks and insurers have no revenue line; keep a quarter that has any headline figure.
            if any(values[key] is not None for key in ("revenue", "operating_income", "net_income")):
                single[f"{year}Q{quarter}"] = {"year": year, "quarter": quarter, **values}

    out = []
    for period in sorted(single):
        q = single[period]
        prior = single.get(f"{q['year'] - 1}Q{q['quarter']}")
        out.append(
            {
                "period": period,
                **{key: q[key] for key in keys},
                "gpm": _pct(q["gross_profit"], q["revenue"]),
                "opm": _pct(q["operating_income"], q["revenue"]),
                "yoy": None
                if prior is None
                else {
                    "revenue": growth(q["revenue"], prior["revenue"]),
                    "operating_income": growth(q["operating_income"], prior["operating_income"]),
                    "net_income_owners": growth(q["net_income_owners"], prior["net_income_owners"]),
                },
            }
        )
    return out


def _with_ratios(figures: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    def avg(key: str) -> float | None:
        if previous is None or figures.get(key) is None or previous.get(key) is None:
            return None
        return (figures[key] + previous[key]) / 2

    net_debt = (
        None if figures["borrowings"] is None or figures["cash"] is None else figures["borrowings"] - figures["cash"]
    )
    # Filers sign 유형자산의취득 either way (outflow shown negative or as a positive amount); it is always an outflow.
    fcf = (
        None
        if figures["operating_cash_flow"] is None or figures["capex"] is None
        else figures["operating_cash_flow"] - abs(figures["capex"])
    )
    return {
        **figures,
        "net_debt": net_debt,
        "free_cash_flow": fcf,
        "gpm": _pct(figures["gross_profit"], figures["revenue"]),
        "opm": _pct(figures["operating_income"], figures["revenue"]),
        "debt_ratio": _pct(figures["liabilities"], figures["equity"]),
        "net_debt_ratio": _pct(net_debt, figures["equity"]),
        "interest_coverage": _ratio(figures["operating_income"], figures["interest_expense"]),
        "roe": _pct(figures["net_income_owners"], avg("equity_owners")),
        "roa": _pct(figures["net_income"], avg("assets")),
    }


_ANNUAL_COLUMNS = ("bfefrmtrm_amount", "frmtrm_amount", "thstrm_amount")


def annual(report: Report) -> list[dict[str, Any]]:
    """Three fiscal years out of one annual report, oldest first. ROE/ROA need the year before, so the oldest has none."""
    years = []
    financial = _financial_figures(report.rows, _ANNUAL_COLUMNS)
    for offset, column in enumerate(_ANNUAL_COLUMNS):
        amount, basis = borrowings(report.rows, column)
        years.append(
            {
                "year": report.year - 2 + offset,
                **_pick(report.rows, INCOME, INCOME_ITEMS, column),
                **_pick(report.rows, BALANCE, BALANCE_ITEMS, column),
                **_pick(report.rows, CASH, CASH_ITEMS, column),
                **financial[offset],
                "borrowings": amount,
                "borrowings_basis": basis,
            }
        )
    return [_with_ratios(figures, years[i - 1] if i > 0 else None) for i, figures in enumerate(years)]


def _year_to_date_pick(report: Report, items: dict[str, Item]) -> dict[str, float | None]:
    """Income figures of one report, year-to-date: a quarterly report's cumulative column, else this period."""
    out: dict[str, float | None] = {}
    for key, item in items.items():
        row = find_row(report.rows, INCOME, item)
        if row is None:
            out[key] = None
        elif report.quarter == 4:
            out[key] = won(row.get("thstrm_amount"))
        else:
            out[key] = _first(won(row.get("thstrm_add_amount")), won(row.get("thstrm_amount")))
    return out


def latest(report: Report) -> dict[str, Any]:
    """The latest filed period: balance sheet at its end, income and cash flow year-to-date."""
    amount, basis = borrowings(report.rows, "thstrm_amount")
    financial = {
        **_year_to_date_pick(report, FINANCIAL_INCOME_ITEMS),
        **_pick(report.rows, BALANCE, FINANCIAL_BALANCE_ITEMS, "thstrm_amount"),
    }
    has_financial = any(financial[key] is not None for key in FINANCIAL_MARKERS)
    figures = {
        **_year_to_date_pick(report, INCOME_ITEMS),
        **_pick(report.rows, BALANCE, BALANCE_ITEMS, "thstrm_amount"),
        **_pick(report.rows, CASH, CASH_ITEMS, "thstrm_amount"),
        **(financial if has_financial else {}),
        "borrowings": amount,
        "borrowings_basis": basis,
    }
    with_ratios = _with_ratios(figures, None)
    with_ratios.pop("roe")
    with_ratios.pop("roa")
    return {
        "period": f"{report.year}{PERIOD_LABEL[report.quarter]}",
        "reprt_code": report.reprt_code,
        **with_ratios,
        "account_match": match_items(report.rows, "thstrm_amount", financial=has_financial),
    }


def trailing(quarter_list: list[dict[str, Any]], key: str) -> float | None:
    """Sum of the last four quarters, or None when any is missing."""
    last = quarter_list[-4:]
    if len(last) < 4 or any(q.get(key) is None for q in last):
        return None
    return sum(q[key] for q in last)


def to_eok(figures: dict[str, Any] | None) -> dict[str, Any] | None:
    """원 → 억원 for the money fields of one figures dict. Not recursive: ``yoy`` reuses item names for percentages."""
    if figures is None:
        return None
    return {
        key: value / EOK if key in MONEY_FIELDS and isinstance(value, (int, float)) else value
        for key, value in figures.items()
    }
