"""Damodaran Online 데이터 파일 (NYU Stern). API 가 아니라 공개 HTML·xls 파일을 받아 읽는다."""

from __future__ import annotations

import datetime as dt
from typing import Any, List, Literal, Optional

from .._exceptions import FeedParseError
from .._http import HttpClient
from ._parse import parse_companies, parse_country_risk_premiums, parse_industry_betas
from ._types import CompanyIndustry, CountryRiskPremiumTable, IndustryBetaTable

BASE_URL = "https://pages.stern.nyu.edu/~adamodar"
CTRYPREM_URL = f"{BASE_URL}/New_Home_Page/datafile/ctryprem.html"
INDNAME_URL = f"{BASE_URL}/pc/datasets/indname.xls"

Region = Literal["us", "europe", "japan", "rest", "emerging", "china", "india", "global"]
# 지역 → 파일 이름. US 는 접미사 없음, "rest" = Australia·NZ·Canada. 한국은 emerging (Broad Group "Emerging Markets").
_BETA_FILES = {
    "us": "betas.xls",
    "europe": "betaEurope.xls",
    "japan": "betaJapan.xls",
    "rest": "betaRest.xls",
    "emerging": "betaemerg.xls",
    "china": "betaChina.xls",
    "india": "betaIndia.xls",
    "global": "betaGlobal.xls",
}


class Client:
    """국가 위험 프리미엄(HTML), 업종 β·종목 업종(xls). xls 는 `cluefin-feeds[damodaran]`(xlrd)이 필요하다.

    표는 1년에 한두 번(1월, ERP 는 7월에도) 바뀐다. 매일 받지 말고 쓰는 쪽에서 저장해 둔다.
    """

    def __init__(self, http: Optional[HttpClient] = None):
        self.http = http or HttpClient(timeout=120)

    def country_risk_premiums(self) -> CountryRiskPremiumTable:
        """국가별 신용등급·부도 스프레드·CRP·ERP·법인세율 (ctryprem.html, 약 180개국)."""
        response = self.http.get(CTRYPREM_URL)
        return parse_country_risk_premiums(response.content.decode("latin-1"))

    def industry_betas(self, region: Region = "emerging") -> IndustryBetaTable:
        """지역별 업종 β 표. 한국 상장사는 Damodaran 분류상 emerging(신흥국)."""
        filename = _BETA_FILES.get(region)
        if filename is None:
            raise ValueError(f"region 은 {sorted(_BETA_FILES)} 중 하나입니다. 받은 값: {region!r}")
        url = f"{BASE_URL}/pc/datasets/{filename}"
        book = _open_workbook(self.http.get(url).content, url)
        sheet = _sheet(book, "Industry Averages", url)
        rows = [sheet.row_values(r) for r in range(sheet.nrows)]
        return parse_industry_betas(rows, lambda serial: _excel_date(serial, book.datemode))

    def companies(self, country: Optional[str] = "South Korea") -> List[CompanyIndustry]:
        """종목 → 업종 분류 (indname.xls, 약 22MB·4만 8천 종목). country=None 이면 전체.

        한국은 "South Korea" (2026-01 기준 2,660종목·88업종). `krx_code` 로 6자리 코드를 얻는다.
        """
        book = _open_workbook(self.http.get(INDNAME_URL).content, INDNAME_URL)
        sheet = _sheet(book, "By industry", INDNAME_URL)
        rows = [sheet.row_values(r) for r in range(sheet.nrows)]
        return parse_companies(rows, country)


def _open_workbook(content: bytes, url: str) -> Any:
    try:
        import xlrd
    except ImportError as exc:  # pragma: no cover - extra 없이 설치한 경우
        raise ImportError(
            "Damodaran xls 를 읽으려면 xlrd 가 필요합니다: pip install 'cluefin-feeds[damodaran]'"
        ) from exc
    try:
        return xlrd.open_workbook(file_contents=content)
    except xlrd.XLRDError as exc:
        raise FeedParseError(f"xls 를 열지 못했습니다: {exc}", url=url) from exc


def _sheet(book: Any, name: str, url: str) -> Any:
    if name not in book.sheet_names():
        raise FeedParseError(f"'{name}' 시트가 없습니다. 시트: {book.sheet_names()}", url=url)
    return book.sheet_by_name(name)


def _excel_date(serial: float, datemode: int) -> dt.date:
    import xlrd

    return xlrd.xldate_as_datetime(serial, datemode).date()
