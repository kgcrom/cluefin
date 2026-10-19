"""Damodaran Online 데이터 (NYU Stern, API 없음 — 공개 HTML·xls 파일).

국가 위험 프리미엄은 의존성 없이, 업종 β·종목 업종(xls)은 `pip install 'cluefin-feeds[damodaran]'`.
https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html
"""

from cluefin_feeds.damodaran._client import Client, Region
from cluefin_feeds.damodaran._types import (
    CompanyIndustry,
    CountryRiskPremium,
    CountryRiskPremiumTable,
    IndustryBeta,
    IndustryBetaTable,
)

__all__ = [
    "Client",
    "CompanyIndustry",
    "CountryRiskPremium",
    "CountryRiskPremiumTable",
    "IndustryBeta",
    "IndustryBetaTable",
    "Region",
]
