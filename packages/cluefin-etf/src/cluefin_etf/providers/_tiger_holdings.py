from __future__ import annotations

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfHolding
from cluefin_etf.providers._parsing import compact_raw, normalize_space
from cluefin_etf.providers._tiger_models import TigerHoldingItem


def validate_tiger_holdings_page(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("#formPdfList") is not None or soup.select_one("input[name='fixDate']") is not None


def validate_tiger_holdings(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("tr[data-tot-cnt]") is not None


def parse_tiger_holdings_html(html: str, *, as_of_date=None) -> list[EtfHolding]:
    soup = BeautifulSoup(html, "html.parser")
    holdings: list[EtfHolding] = []
    for index, row in enumerate(soup.select("tr[data-tot-cnt]"), start=1):
        cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all("td")]
        if len(cells) < 5:
            continue
        item = TigerHoldingItem(
            rank=index,
            code=cells[0],
            name=cells[1],
            quantity=cells[2],
            valuation_amount=cells[3],
            weight=cells[4],
            as_of_date=as_of_date,
            raw=compact_raw(
                {
                    "code": cells[0],
                    "name": cells[1],
                    "quantity": cells[2],
                    "valuationAmount": cells[3],
                    "weight": cells[4],
                    "return": cells[5] if len(cells) > 5 else None,
                },
                ("code", "name", "quantity", "valuationAmount", "weight", "return"),
            ),
        )
        holdings.append(
            EtfHolding(
                rank=item.rank,
                code=item.code,
                name=item.name,
                quantity=item.quantity,
                valuation_amount=item.valuation_amount,
                weight=item.weight,
                as_of_date=item.as_of_date,
                raw=item.raw,
            )
        )
    return holdings
