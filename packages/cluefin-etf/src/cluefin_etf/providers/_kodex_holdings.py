from __future__ import annotations

import json
from datetime import date

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfHolding
from cluefin_etf.providers._parsing import (
    compact_raw,
    normalize_space,
    parse_compact_date,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


def kodex_pdf_gijun_ymd(html: str, *, label: str = "KODEX PDF") -> str:
    payload = json.loads(html)
    pdf = payload.get("pdf")
    if not isinstance(pdf, dict):
        raise ValueError(f"{label} 정보가 없습니다")
    value = pdf.get("gijunYMD")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} 기준일이 없습니다")
    return value.strip().replace(".", "")


def validate_kodex_holdings_json(html: str) -> bool:
    try:
        payload = json.loads(html)
    except json.JSONDecodeError:
        return False
    pdf = payload.get("pdf")
    return isinstance(pdf, dict) and isinstance(pdf.get("list"), list)


def parse_kodex_holdings_json(html: str) -> list[EtfHolding]:
    payload = json.loads(html)
    pdf = payload.get("pdf") if isinstance(payload.get("pdf"), dict) else {}
    items = pdf.get("list") if isinstance(pdf, dict) else None
    if not isinstance(items, list):
        return []
    as_of_date = parse_compact_date(pdf.get("gijunYMD")) if isinstance(pdf, dict) else None
    return [
        _holding_from_pdf_item(index, item, as_of_date=as_of_date)
        for index, item in enumerate(items, start=1)
        if isinstance(item, dict)
    ]


def parse_kodex_holdings_html(html: str) -> list[EtfHolding]:
    soup = BeautifulSoup(html, "html.parser")
    table = rendered_kodex_holdings_table(soup)
    if table is None:
        return []

    as_of_date = _rendered_pdf_date(soup)
    holdings: list[EtfHolding] = []
    for index, row in enumerate(table.select("tbody tr"), start=1):
        cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
        if len(cells) < 5:
            continue
        holdings.append(
            EtfHolding(
                rank=index,
                name=cells[0] or None,
                code=cells[1] or None,
                weight=parse_decimal_text(cells[2]),
                quantity=parse_decimal_text(cells[3]),
                valuation_amount=parse_decimal_text(cells[4]),
                as_of_date=as_of_date,
                raw=compact_raw(
                    {
                        "secNm": cells[0],
                        "itmNo": cells[1],
                        "ratio": cells[2],
                        "applyQ": cells[3],
                        "evalA": cells[4],
                    },
                    ("itmNo", "secNm", "applyQ", "evalA", "ratio"),
                ),
            )
        )
    return holdings


def rendered_kodex_holdings_table(soup: BeautifulSoup):
    for table in soup.find_all("table"):
        headers = [normalize_space(node.get_text(" ", strip=True)) for node in table.find_all(["th", "td"])]
        if {"종목명", "종목코드", "비중(%)", "수량", "평가금액(원)"}.issubset(headers):
            return table
    return None


def _rendered_pdf_date(soup: BeautifulSoup) -> date | None:
    for node in soup.find_all("input"):
        value = node.get("value")
        if isinstance(value, str):
            parsed = parse_date_text(value)
            if parsed is not None:
                return parsed

    return parse_date_text(soup.get_text(" ", strip=True))


def _holding_from_pdf_item(index: int, item: dict[str, object], *, as_of_date: date | None) -> EtfHolding:
    return EtfHolding(
        rank=parse_int_text(item.get("rank")) or index,
        code=str(item.get("itmNo")) if item.get("itmNo") is not None else None,
        name=str(item.get("secNm")) if item.get("secNm") is not None else None,
        quantity=parse_decimal_text(str(item.get("applyQ"))) if item.get("applyQ") is not None else None,
        valuation_amount=parse_decimal_text(str(item.get("evalA"))) if item.get("evalA") is not None else None,
        weight=parse_decimal_text(str(item.get("ratio"))) if item.get("ratio") is not None else None,
        as_of_date=as_of_date,
        raw=compact_raw(item, ("rank", "itmNo", "secNm", "applyQ", "evalA", "ratio")),
    )
