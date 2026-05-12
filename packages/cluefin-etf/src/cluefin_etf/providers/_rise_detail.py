from __future__ import annotations

import re

from bs4 import BeautifulSoup

from cluefin_etf._models import EtfDetail, ProviderName
from cluefin_etf.providers._parsing import compact_raw, normalize_space, parse_date_text
from cluefin_etf.providers._rise_models import RiseEtfDetailData


def looks_like_rise_ticker(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Z0-9]{6}", value.strip(), flags=re.IGNORECASE))


def parse_rise_detail_html(code: str, html: str, provider: ProviderName) -> EtfDetail:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one("h2.prod_title") or _first_title(soup)
    name, ticker = _parse_name_and_code(normalize_space(title.get_text(" ", strip=True)) if title else "")
    info = _detail_info(soup)
    item = RiseEtfDetailData(
        code=ticker or code,
        name=name,
        category=_detail_category(soup),
        benchmark=info.get("기초지수"),
        listing_date=info.get("상장일"),
        nav=info.get("기준가격(NAV)"),
        aum=info.get("순 자산 규모(원)"),
        expense_ratio=info.get("총 보수(%)") or info.get("총보수(%)"),
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

    return EtfDetail(
        provider=provider,
        code=item.code,
        name=item.name,
        category=item.category,
        benchmark=item.benchmark,
        listing_date=item.listing_date,
        nav=item.nav,
        aum=item.aum,
        expense_ratio=item.expense_ratio,
        as_of_date=item.as_of_date,
        detail_url=item.detail_url,
        raw=item.raw,
    )


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
            values = [
                normalize_space(cell.get_text(" ", strip=True))
                for cell in rows[index + 1].find_all(["td", "th"], recursive=False)
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
