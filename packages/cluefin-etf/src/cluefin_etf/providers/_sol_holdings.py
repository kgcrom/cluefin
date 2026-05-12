from __future__ import annotations

import re
from datetime import date

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfHolding
from cluefin_etf.providers._parsing import (
    compact_raw,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


def sol_holdings_work_date(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one("#f-pdf-calendar")
    value = node.get("value") if node is not None else None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.replace("-", "").replace(".", "")


def parse_sol_holdings_json_items(payload: object) -> list[EtfHolding]:
    if not isinstance(payload, list):
        return []
    return [
        _holding_from_pdf_item(index, item) for index, item in enumerate(payload, start=1) if isinstance(item, dict)
    ]


def parse_sol_holdings_html(html: str) -> list[EtfHolding]:
    soup = BeautifulSoup(html, "html.parser")
    holdings: list[EtfHolding] = []
    for row in soup.select("#pdf-table tbody tr"):
        cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
        if len(cells) < 5:
            continue
        holdings.append(
            EtfHolding(
                rank=parse_int_text(cells[0]),
                name=cells[1] or None,
                quantity=parse_decimal_text(cells[2]),
                valuation_amount=parse_decimal_text(cells[3]),
                weight=parse_decimal_text(cells[4]),
                as_of_date=parse_date_text(sol_holdings_work_date(html)),
                raw=compact_raw(
                    {
                        "rank": cells[0],
                        "name": cells[1],
                        "quantity": cells[2],
                        "valuationAmount": cells[3],
                        "weight": cells[4],
                    },
                    ("rank", "name", "quantity", "valuationAmount", "weight"),
                ),
            )
        )
    return holdings


def _holding_from_pdf_item(index: int, item: dict[str, object]) -> EtfHolding:
    return EtfHolding(
        rank=index,
        code=str(item.get("STOCK_CODE")) if item.get("STOCK_CODE") is not None else None,
        name=str(item.get("SEC_NM")) if item.get("SEC_NM") is not None else None,
        quantity=parse_decimal_text(str(item.get("QTY"))) if item.get("QTY") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("PRICE"))) if item.get("PRICE") is not None else None,
        weight=parse_decimal_text(str(item.get("WT_DISP"))) if item.get("WT_DISP") is not None else None,
        as_of_date=_parse_compact_sol_date(item.get("WORK_DT")),
        raw=compact_raw(item, ("WORK_DT", "SEQ_NO", "STOCK_CODE", "SEC_NM", "QTY", "PRICE", "WT_DISP")),
    )


def _parse_compact_sol_date(value: object) -> date | None:
    if value is None:
        return None
    text = str(value)
    if re.fullmatch(r"\d{8}", text):
        return parse_date_text(f"{text[:4]}.{text[4:6]}.{text[6:8]}")
    return parse_date_text(text)
