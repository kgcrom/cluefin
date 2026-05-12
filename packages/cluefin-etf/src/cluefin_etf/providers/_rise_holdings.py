from __future__ import annotations

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfHolding
from cluefin_etf.providers._parsing import compact_raw, normalize_space
from cluefin_etf.providers._rise_models import RiseHoldingItem


def parse_rise_holdings_html(html: str, *, as_of_date=None) -> list[EtfHolding]:
    soup = BeautifulSoup(html, "html.parser")
    holdings: list[EtfHolding] = []
    for row in soup.select('tbody[data-class="tab3PdfList"] tr'):
        cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
        if len(cells) < 6:
            continue
        item = RiseHoldingItem(
            rank=cells[0],
            name=cells[1],
            code=cells[2],
            quantity=cells[3],
            weight=cells[4],
            valuation_amount=cells[5],
            as_of_date=as_of_date,
            raw=compact_raw(
                {
                    "rank": cells[0],
                    "name": cells[1],
                    "code": cells[2],
                    "quantity": cells[3],
                    "weight": cells[4],
                    "valuationAmount": cells[5],
                },
                ("rank", "name", "code", "quantity", "weight", "valuationAmount"),
            ),
        )
        holdings.append(
            EtfHolding(
                rank=item.rank,
                name=item.name,
                code=item.code,
                quantity=item.quantity,
                weight=item.weight,
                valuation_amount=item.valuation_amount,
                as_of_date=item.as_of_date,
                raw=item.raw,
            )
        )
    return holdings
