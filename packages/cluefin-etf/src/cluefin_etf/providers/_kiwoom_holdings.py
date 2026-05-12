from __future__ import annotations

import json
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


def validate_kiwoom_holdings_json(html: str) -> bool:
    try:
        payload = json.loads(html)
    except json.JSONDecodeError:
        return False
    return isinstance(payload.get("pdfList"), list)


def parse_kiwoom_holdings_json(html: str) -> list[EtfHolding]:
    payload = json.loads(html)
    items = payload.get("pdfList")
    if not isinstance(items, list):
        return []
    return [_holding_from_pdf_item(index, item) for index, item in enumerate(items, start=1) if isinstance(item, dict)]


def parse_kiwoom_holdings_html(html: str, *, as_of_date: date | None = None) -> list[EtfHolding]:
    table = rendered_kiwoom_holdings_table(BeautifulSoup(html, "html.parser"))
    if table is None:
        return []

    holdings: list[EtfHolding] = []
    for row in table.select("tbody tr"):
        cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
        if len(cells) < 4:
            continue
        holdings.append(
            EtfHolding(
                rank=parse_int_text(cells[0]),
                code=cells[2] or None,
                name=cells[1] or None,
                weight=parse_decimal_text(cells[3]),
                as_of_date=as_of_date,
                raw=compact_raw(
                    {
                        "rank": cells[0],
                        "itemTitle": cells[1],
                        "itemCode": cells[2],
                        "ratio": cells[3],
                    },
                    ("rank", "itemCode", "itemTitle", "ratio"),
                ),
            )
        )
    return holdings


def rendered_kiwoom_holdings_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        headers = [normalize_space(node.get_text(" ", strip=True)) for node in table.find_all(["th", "td"])]
        if {"NO.", "종목명", "종목코드", "비중"}.issubset(headers):
            return table
    return None


def _holding_from_pdf_item(index: int, item: dict[str, object]) -> EtfHolding:
    code = item.get("itemCode") or item.get("gcode") or item.get("fundcode")
    return EtfHolding(
        rank=index,
        code=str(code) if code is not None else None,
        name=str(item.get("itemTitle")) if item.get("itemTitle") is not None else None,
        quantity=parse_decimal_text(str(item.get("volume"))) if item.get("volume") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("assessment")))
        if item.get("assessment") is not None
        else None,
        weight=parse_decimal_text(str(item.get("ratio"))) if item.get("ratio") is not None else None,
        as_of_date=parse_date_text(str(item.get("businessDate"))) if item.get("businessDate") is not None else None,
        raw=compact_raw(
            item,
            ("businessDate", "itemCode", "gcode", "fundcode", "itemTitle", "volume", "assessment", "ratio"),
        ),
    )
