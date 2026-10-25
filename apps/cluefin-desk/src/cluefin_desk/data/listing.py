"""Stock code/name search index built from Kiwoom's stock list (ka10099).

Market type ``0`` already includes the exchange's ETFs, ETNs and REITs, so two calls
(``0`` and ``10``) cover every listing desk can open. Codes are six characters but not
always digits: newer listings and preferred shares use letters (``0001A0``, ``00088K``).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

# (Kiwoom mrkt_tp, market label)
MARKETS: tuple[tuple[str, str], ...] = (("0", "KOSPI"), ("10", "KOSDAQ"))
_MARKET_ORDER = {label: idx for idx, (_, label) in enumerate(MARKETS)}
_FUND_KINDS = frozenset({"ETF", "ETN", "ETN(변동성)"})
_CODE_PATTERN = re.compile(r"^[0-9A-Z]{6}$")
_MAX_PAGES = 20

# Match tiers for suggest(): lower sorts first.
_EXACT, _PREFIX, _PARTIAL = 0, 1, 2


@dataclass(frozen=True, slots=True)
class ListedStock:
    code: str
    name: str
    market: str  # "KOSPI" | "KOSDAQ"
    kind: str  # Kiwoom marketName: 거래소 · 코스닥 · ETF · ETN · 리츠 …
    sector: str  # upName, "" for ETF/ETN


def is_stock_code(text: str) -> bool:
    """True for a six-character code (digits and upper-case letters)."""
    return bool(_CODE_PATTERN.match(text))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


class StockListing:
    def __init__(self, rows: Iterable[ListedStock]):
        self._rows = tuple(rows)
        self._by_code = {row.code: row for row in self._rows}
        self._keyed = tuple((row, _normalize(row.name)) for row in self._rows)

    def __len__(self) -> int:
        return len(self._rows)

    def get(self, code: str) -> ListedStock | None:
        return self._by_code.get(code.strip().upper())

    def resolve(self, text: str) -> ListedStock | None:
        """The one stock ``text`` names, or None when it names none or several.

        A code matches exactly; a name tries exact, then ignoring spaces and case,
        then a unique partial match (same order as cluefin-factory's resolver).
        """
        query = text.strip()
        if not query:
            return None
        by_code = self.get(query)
        if by_code is not None:
            return by_code
        wanted = _normalize(query)
        for matches in (
            [row for row in self._rows if row.name == query],
            [row for row, key in self._keyed if key == wanted],
            [row for row, key in self._keyed if wanted in key],
        ):
            if len(matches) == 1:
                return matches[0]
        return None

    def suggest(self, text: str, limit: int = 20) -> list[ListedStock]:
        """Candidates for ``text``: exact, then prefix, then partial (name or code).

        Within a tier, stocks come before ETF/ETN, KOSPI before KOSDAQ, then by name.
        """
        wanted = _normalize(text)
        if not wanted:
            return []
        code_query = wanted.upper()
        ranked = []
        for row, key in self._keyed:
            tier = _match_tier(key, row.code, wanted, code_query)
            if tier is not None:
                ranked.append(
                    ((tier, row.kind in _FUND_KINDS, _MARKET_ORDER.get(row.market, len(MARKETS)), row.name), row)
                )
        ranked.sort(key=lambda item: item[0])
        return [row for _, row in ranked[:limit]]


def _match_tier(key: str, code: str, wanted: str, code_query: str) -> int | None:
    if key == wanted or code == code_query:
        return _EXACT
    if key.startswith(wanted) or code.startswith(code_query):
        return _PREFIX
    if wanted in key:
        return _PARTIAL
    return None


def _to_listed(item: Any, market: str) -> ListedStock | None:
    code = (item.code or "").strip()
    name = (item.name or "").strip()
    if not code or not name:
        return None
    return ListedStock(code=code, name=name, market=market, kind=item.marketName or "", sector=item.upName or "")


def load_listing(kiwoom_client: Any) -> StockListing:
    """Fetch KOSPI (with ETF/ETN/REIT) and KOSDAQ listings, following continuation keys."""
    rows: list[ListedStock] = []
    for mrkt_tp, market in MARKETS:
        cont_yn, next_key = "N", ""
        for _ in range(_MAX_PAGES):
            response = kiwoom_client.stock_info.get_stock_info_summary(mrkt_tp, cont_yn=cont_yn, next_key=next_key)
            rows.extend(stock for stock in (_to_listed(item, market) for item in response.body.list) if stock)
            if response.headers.cont_yn != "Y" or not response.headers.next_key:
                break
            cont_yn, next_key = "Y", response.headers.next_key
    return StockListing(rows)
