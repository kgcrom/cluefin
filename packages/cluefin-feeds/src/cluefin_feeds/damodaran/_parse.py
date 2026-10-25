"""Damodaran 파일 파서. 표 구조는 해마다 조금씩 바뀌므로 열은 위치가 아니라 머리 이름으로 찾는다."""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Callable, Sequence
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from typing import Any

from .._exceptions import FeedParseError
from ._types import (
    CompanyIndustry,
    CountryRiskPremium,
    CountryRiskPremiumTable,
    IndustryBeta,
    IndustryBetaTable,
)

# ── ctryprem.html ──────────────────────────────────────────────

# 머리 이름 → 필드. 사이트 머리에 오타가 있어("Sovereignn CDS", "ERP based on sovereign CDSS") 소문자 앞부분으로 찾는다.
_CRP_COLUMNS = (
    ("country", "country"),
    ("moodys_rating", "moody"),
    ("default_spread", "adj. default spread"),
    ("country_risk_premium", "country risk premium"),
    ("equity_risk_premium", "equity risk premium"),
    ("corporate_tax_rate", "corporate tax rate"),
    ("sovereign_cds", "sovereign"),
    ("cds_equity_risk_premium", "erp based on sovereign"),
)
_UPDATED = re.compile(r"Last updated:\s*([A-Za-z]+ \d{1,2}, \d{4})")


class _TableCollector(HTMLParser):
    """문서의 모든 <table> 을 [[셀 텍스트]] 로 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "table":
            self.tables.append([])
        elif tag == "tr" and self.tables:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._row is not None and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.tables[-1].append(self._row)
            self._row = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def parse_country_risk_premiums(page: str) -> CountryRiskPremiumTable:
    collector = _TableCollector()
    collector.feed(page)
    table = next((t for t in collector.tables if t and _is_crp_header(t[0])), None)
    if table is None:
        raise FeedParseError("ctryprem.html 에서 Country · Equity Risk Premium 머리 행을 찾지 못했습니다")

    positions = _column_positions(table[0], _CRP_COLUMNS, "ctryprem.html")
    rows = [
        CountryRiskPremium(**_crp_values(cells, positions))
        for cells in table[1:]
        if len(cells) == len(table[0]) and cells[0]
    ]
    match = _UPDATED.search(page)
    updated = dt.datetime.strptime(match.group(1), "%B %d, %Y").date() if match else None
    return CountryRiskPremiumTable(updated=updated, rows=rows)


def _is_crp_header(cells: Sequence[str]) -> bool:
    lowered = [c.lower() for c in cells]
    return bool(lowered) and lowered[0] == "country" and "equity risk premium" in lowered


def _crp_values(cells: Sequence[str], positions: dict[str, int]) -> dict[str, Any]:
    values: dict[str, Any] = {name: cells[index] for name, index in positions.items()}
    for name in positions:
        if name not in ("country", "moodys_rating"):
            values[name] = _percent(values[name])
    return values


def _percent(text: str) -> Decimal | None:
    try:
        return Decimal(text.strip().rstrip("%").replace(",", ""))
    except InvalidOperation:
        return None  # "NA"


# ── beta*.xls / indname.xls ────────────────────────────────────

_BETA_COLUMNS = (
    ("industry_name", "industry name"),
    ("number_of_firms", "number of firms"),
    ("beta", "beta"),
    ("de_ratio", "d/e ratio"),
    ("effective_tax_rate", "effective tax rate"),
    ("unlevered_beta", "unlevered beta"),
    ("cash_firm_value", "cash/firm value"),
    ("unlevered_beta_corrected_for_cash", "unlevered beta corrected for cash"),
    ("hilo_risk", "hilo risk"),
    ("std_equity", "standard deviation of equity"),
    ("std_operating_income", "standard deviation in operating income"),
)
_OPTIONAL_BETA_COLUMNS = {"hilo_risk", "std_equity", "std_operating_income"}

_COMPANY_COLUMNS = (
    ("company_name", "company name"),
    ("exchange_ticker", "exchange:ticker"),
    ("industry_group", "industry group"),
    ("primary_sector", "primary sector"),
    ("sic_code", "sic code"),
    ("country", "country"),
    ("broad_group", "broad group"),
    ("sub_group", "sub group"),
)


def parse_industry_betas(rows: Sequence[Sequence[Any]], to_date: Callable[[float], dt.date]) -> IndustryBetaTable:
    """ "Industry Averages" 시트의 행들(셀 값 목록). to_date 는 엑셀 날짜 일련번호 → date."""
    header_index = next((i for i, row in enumerate(rows) if _label(row) == "industry name"), None)
    if header_index is None:
        raise FeedParseError('업종 β 표에서 "Industry Name" 머리 행을 찾지 못했습니다')
    header = [_text(cell) for cell in rows[header_index]]
    positions = _column_positions(header, _BETA_COLUMNS, "업종 β 표", optional=_OPTIONAL_BETA_COLUMNS)
    year_columns = {i: int(float(h)) for i, h in enumerate(header) if re.fullmatch(r"\d{4}(\.0)?", h)}
    average_column = next((i for i, h in enumerate(header) if h.lower().startswith("average")), None)

    preamble = rows[:header_index]
    updated_cell = _value_after(preamble, "date updated")
    tax_cell = _value_after(preamble, "if marginal tax rate")
    region = _value_after(preamble, "what is this data", last=True)

    industries = []
    for row in rows[header_index + 1 :]:
        name = _text(row[0]) if row else ""
        if not name:
            break
        values: dict[str, Any] = {field: _number(row[i]) for field, i in positions.items()}
        values["industry_name"] = name
        values["number_of_firms"] = int(values["number_of_firms"] or 0)
        values["unlevered_beta_by_year"] = {
            year: v for i, year in year_columns.items() if (v := _number(row[i])) is not None
        }
        values["unlevered_beta_average"] = _number(row[average_column]) if average_column is not None else None
        industries.append(IndustryBeta(**values))

    return IndustryBetaTable(
        region=_text(region) or "",
        updated=to_date(updated_cell) if isinstance(updated_cell, float) else None,
        marginal_tax_rate=_number(tax_cell),
        rows=industries,
    )


def parse_companies(rows: Sequence[Sequence[Any]], country: str | None) -> list[CompanyIndustry]:
    """indname.xls "By industry" 시트의 행들. country 를 주면 그 나라만."""
    if not rows:
        raise FeedParseError("indname.xls 시트가 비었습니다")
    header = [_text(cell) for cell in rows[0]]
    positions = _column_positions(header, _COMPANY_COLUMNS, "indname.xls")
    country_index = positions["country"]
    companies = []
    for row in rows[1:]:
        if country is not None and _text(row[country_index]) != country:
            continue
        values = {field: _text(row[i]) for field, i in positions.items()}
        if values["company_name"]:
            companies.append(CompanyIndustry(**values))
    return companies


# ── 공통 ───────────────────────────────────────────────────────


def _column_positions(header: Sequence[str], columns, source: str, optional=frozenset()) -> dict[str, int]:
    """(필드, 머리 앞부분) 표를 머리 행의 위치로. 여러 열이 같은 앞부분이면 가장 길게 맞는 열을 쓴다."""
    lowered = [h.strip().lower() for h in header]
    positions: dict[str, int] = {}
    for field, prefix in columns:
        candidates = [i for i, h in enumerate(lowered) if h == prefix] or [
            i for i, h in enumerate(lowered) if h.startswith(prefix) and not _claimed_by_longer(h, prefix, columns)
        ]
        if candidates:
            positions[field] = candidates[0]
        elif field not in optional:
            raise FeedParseError(f"{source}: '{prefix}' 열이 없습니다. 머리 행: {list(header)}")
    return positions


def _claimed_by_longer(header: str, prefix: str, columns) -> bool:
    return any(other != prefix and other.startswith(prefix) and header.startswith(other) for _, other in columns)


def _label(row: Sequence[Any]) -> str:
    return _text(row[0]).lower() if row else ""


def _value_after(rows: Sequence[Sequence[Any]], label: str, last: bool = False) -> Any:
    """첫 칸이 label 로 시작하는 행에서 그 뒤 첫(last=True 면 마지막) 비지 않은 값."""
    for row in rows:
        if _label(row).startswith(label):
            filled = [cell for cell in row[1:] if cell not in ("", None)]
            if filled:
                return filled[-1] if last else filled[0]
    return None


def _text(cell: Any) -> str:
    if isinstance(cell, float) and cell.is_integer():
        return str(int(cell))
    return str(cell).strip() if cell is not None else ""


def _number(cell: Any) -> float | None:
    if isinstance(cell, (int, float)) and not isinstance(cell, bool):
        return float(cell)
    try:
        return float(str(cell).strip())
    except ValueError:
        return None
