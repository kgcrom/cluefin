from __future__ import annotations

import json
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, EtfHolding, EtfSummary, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers._parsing import (
    compact_raw,
    normalize_space,
    parse_date_text,
    parse_decimal_text,
    parse_int_text,
)


class RiseProvider(EtfProvider):
    list_url = "https://www.riseetf.co.kr/prod/finder/listJquery"
    detail_url_base = "https://www.riseetf.co.kr/prod/finderDetail"
    detail_url_template = f"{detail_url_base}/{{code}}"
    list_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    max_list_pages = 50

    info = ProviderInfo(
        name=ProviderName.RISE,
        display_name="RISE",
        homepage_url="https://www.riseetf.co.kr/",
    )

    def fetch_list(self) -> list[EtfSummary]:
        page = 1
        items: list[EtfSummary] = []
        total_count: int | None = None

        while page <= self.max_list_pages:
            result = self.fetcher.fetch(
                self.list_url,
                provider=self.name,
                validator=self.validate_list_result,
                method="POST",
                headers=self.list_headers,
                data=self._list_request_data(page),
                referrer="https://www.riseetf.co.kr/prod/finder",
            )
            page_items = self.parse_list_html(result.html)
            if not page_items:
                break

            if len(page_items) <= len(items):
                break

            items = page_items
            total_count = _list_total_count(result.html) or total_count
            if total_count is not None and len(items) >= total_count:
                break

            page += 1

        return items[:total_count] if total_count is not None else items

    def fetch_detail(self, code: str) -> EtfDetail:
        product_id = self._resolve_product_id(code) if _looks_like_ticker(code) else code
        url = f"{self.detail_url_base}/{product_id}"
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        detail = self.parse_detail_html(code, result.html)
        holdings = self.parse_holdings_html(result.html, as_of_date=detail.as_of_date)
        return detail.model_copy(update={"holdings_url": f"{url}#pdf", "holdings": holdings})

    def validate_list_result(self, result: FetchResult) -> bool:
        return bool(self.parse_list_html(result.html))

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        soup = BeautifulSoup(html, "html.parser")
        return [summary for row in soup.select('[data-class="dataList"]') if (summary := self._to_summary(row))]

    def validate_detail_result(self, result: FetchResult) -> bool:
        detail = self.parse_detail_html("", result.html)
        return bool(detail.code and detail.name)

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select_one("h2.prod_title") or _first_title(soup)
        name, ticker = _parse_name_and_code(normalize_space(title.get_text(" ", strip=True)) if title else "")
        info = _detail_info(soup)

        return EtfDetail(
            provider=self.name,
            code=ticker or code,
            name=name,
            category=_detail_category(soup),
            benchmark=info.get("기초지수"),
            listing_date=parse_date_text(info.get("상장일")),
            nav=parse_decimal_text(info.get("기준가격(NAV)")),
            aum=parse_decimal_text(info.get("순 자산 규모(원)")),
            expense_ratio=parse_decimal_text(info.get("총 보수(%)") or info.get("총보수(%)")),
            as_of_date=_as_of_date(soup),
            detail_url=_canonical_detail_url(soup, ticker or code),
            raw=compact_raw(
                {
                    "inputCode": code,
                    "productId": _product_id_from_html(html),
                    "tags": _detail_tags(soup),
                    "info": info,
                },
                ("inputCode", "productId", "tags", "info"),
            ),
        )

    def validate_holdings_result(self, result: FetchResult) -> bool:
        return bool(BeautifulSoup(result.html, "html.parser").select_one('tbody[data-class="tab3PdfList"] tr'))

    def parse_holdings_html(self, html: str, *, as_of_date=None) -> list[EtfHolding]:
        soup = BeautifulSoup(html, "html.parser")
        holdings: list[EtfHolding] = []
        for row in soup.select('tbody[data-class="tab3PdfList"] tr'):
            cells = [normalize_space(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
            if len(cells) < 6:
                continue
            holdings.append(
                EtfHolding(
                    rank=parse_int_text(cells[0]),
                    name=cells[1] or None,
                    code=cells[2] or None,
                    quantity=parse_decimal_text(cells[3]),
                    weight=parse_decimal_text(cells[4]),
                    valuation_amount=parse_decimal_text(cells[5]),
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
            )
        return holdings

    def _list_request_data(self, page: int) -> dict[str, str]:
        return {
            "searchType1": "",
            "searchType2": "",
            "page": str(page),
            "searchOrder": "",
            "searchBoardType": "",
            "searchText": "",
            "searchFieldType": "list",
        }

    def _resolve_product_id(self, code: str) -> str:
        for summary in self.fetch_list():
            if summary.code == code and summary.raw.get("productId"):
                return str(summary.raw["productId"])
        return code

    def _to_summary(self, row) -> EtfSummary | None:
        link = row.select_one('a[href*="/prod/finderDetail/"]')
        name = normalize_space(link.get_text(" ", strip=True) if link else "")
        code = _code_from_row(row)
        if link is None or not name or not code:
            return None

        href = str(link.get("href") or "")
        tags = _row_tags(row)
        returns = _row_returns(row)
        cells = row.find_all("td", recursive=False)

        return EtfSummary(
            provider=self.name,
            code=code,
            name=name,
            category=_row_category(row),
            listing_date=parse_date_text(_cell_text(cells, 8)),
            nav=parse_decimal_text(_cell_text(cells, 0)),
            expense_ratio=parse_decimal_text(_cell_text(cells, 1)),
            detail_url=urljoin("https://www.riseetf.co.kr", href),
            raw=compact_raw(
                {
                    "productId": _product_id_from_href(href),
                    "tags": tags,
                    "returns": returns,
                },
                ("productId", "tags", "returns"),
            ),
        )


def _cell_text(cells, index: int) -> str | None:
    if index >= len(cells):
        return None
    return normalize_space(cells[index].get_text(" ", strip=True))


def _row_tags(row) -> list[str]:
    return [
        normalize_space(node.get_text(" ", strip=True))
        for node in row.select('[class^="tag_type"]')
        if normalize_space(node.get_text(" ", strip=True))
    ]


def _row_category(row) -> str | None:
    tags = [
        normalize_space(node.get_text(" ", strip=True))
        for node in row.select(".tag_type01, .tag_type02")
        if normalize_space(node.get_text(" ", strip=True))
    ]
    return " / ".join(tags) if tags else None


def _row_returns(row) -> dict[str, str | None]:
    labels = ("1개월", "3개월", "6개월", "1년", "3년", "상장이후")
    cells = row.find_all("td", recursive=False)
    returns: dict[str, str | None] = {}
    for label, cell in zip(labels, cells[2:8], strict=False):
        value = normalize_space(cell.get_text(" ", strip=True))
        value = value.replace(" 상승", "").replace(" 하락", "")
        returns[label] = None if value == "-" else value
    return returns


def _list_total_count(html: str) -> int | None:
    soup = BeautifulSoup(html, "html.parser")
    node = soup.select_one('[data-class="more"]')
    return _total_count_from_node(node)


def _total_count_from_node(node) -> int | None:
    if node is None:
        return None
    value = node.get("data-value")
    if not isinstance(value, str):
        return None
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return parse_int_text(payload.get("totalCount"))


def _code_from_row(row) -> str | None:
    node = row.select_one(".code")
    match = re.search(r"\((?P<code>[^)]+)\)", normalize_space(node.get_text(" ", strip=True) if node else ""))
    return match.group("code").strip() if match else None


def _product_id_from_href(href: str) -> str | None:
    match = re.search(r"/prod/finderDetail/(?P<product_id>[^/?#]+)", href)
    return match.group("product_id") if match else None


def _looks_like_ticker(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9]{6}", value.strip(), flags=re.IGNORECASE))


def _parse_name_and_code(value: str) -> tuple[str | None, str | None]:
    match = re.search(r"^(?P<name>.+?)\s*\((?P<code>[^)]+)\)", value)
    if match is None:
        return (value or None), None
    return match.group("name").strip(), match.group("code").strip()


def _first_title(soup: BeautifulSoup):
    for node in soup.find_all(["h1", "h2"]):
        if re.search(r"\([A-Z0-9]{6}\)", node.get_text(" ", strip=True), flags=re.IGNORECASE):
            return node
    return soup.find(["h1", "h2"])


def _detail_tags(soup: BeautifulSoup) -> list[str]:
    tag_area = soup.select_one(".prod_detail_visual .tag_area") or soup.select_one(".tag_area")
    if tag_area is None:
        return []
    return [
        normalize_space(node.get_text(" ", strip=True))
        for node in tag_area.select('[class^="tag_type"]')
        if normalize_space(node.get_text(" ", strip=True))
    ]


def _detail_category(soup: BeautifulSoup) -> str | None:
    tags = [tag for tag in _detail_tags(soup) if tag not in {"패시브", "액티브", "개인연금", "퇴직연금"}]
    return " / ".join(tags) if tags else None


def _detail_info(soup: BeautifulSoup) -> dict[str, str]:
    info: dict[str, str] = {}
    for table in soup.find_all("table"):
        rows = table.find_all("tr", recursive=False) or table.select("tbody > tr")
        for index, row in enumerate(rows[:-1]):
            headers = [_clean_label(cell.get_text(" ", strip=True)) for cell in row.find_all("th", recursive=False)]
            if not headers:
                continue
            value_row = rows[index + 1]
            values = [
                normalize_space(cell.get_text(" ", strip=True))
                for cell in value_row.find_all(["td", "th"], recursive=False)
            ]
            for key, value in zip(headers, values, strict=False):
                if key and value and key not in info:
                    info[key] = value
    return info


def _clean_label(value: str) -> str:
    return normalize_space(value).replace("툴팁 열기 ", "").replace("툴팁 닫기 ", "").strip()


def _as_of_date(soup: BeautifulSoup):
    node = soup.select_one(".prod_detail_visual .date_info") or soup.select_one(".date_info")
    if node is not None:
        parsed = parse_date_text(node.get_text(" ", strip=True))
        if parsed is not None:
            return parsed
    match = re.search(r"(?P<date>\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})\s*기준", soup.get_text(" ", strip=True))
    return parse_date_text(match.group("date")) if match else None


def _canonical_detail_url(soup: BeautifulSoup, code: str) -> str | None:
    og_url = soup.find("meta", property="og:url")
    content = og_url.get("content") if og_url is not None else None
    if isinstance(content, str) and "/prod/finderDetail/" in content:
        return normalize_space(content)
    product_id = _product_id_from_html(str(soup))
    return f"https://www.riseetf.co.kr/prod/finderDetail/{product_id or code}"


def _product_id_from_html(html: str) -> str | None:
    match = re.search(r"/prod/finderDetail/(?P<product_id>[A-Z0-9]+)", html)
    return match.group("product_id") if match else None
