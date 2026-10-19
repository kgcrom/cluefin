"""한국은행 ECOS(경제통계시스템) Open API 클라이언트.

키 없이도 공개 시험 키 `sample`로 쓸 수 있다(한 번에 10행, 쪽 넘김으로 이어 받음).
명세: https://ecos.bok.or.kr/api/#/DevGuide/DevSpeciflcation
"""

from cluefin_openapi.ecos._client import SAMPLE_AUTH_KEY, Client
from cluefin_openapi.ecos._constants import (
    CD_91D,
    CORP_BOND_3Y_AA_MINUS,
    CORP_BOND_3Y_BBB_MINUS,
    CPI_TOTAL,
    KTB_1Y,
    KTB_3Y,
    KTB_5Y,
    KTB_10Y,
    KTB_20Y,
    KTB_30Y,
    MARKET_RATES,
    MSB_91D,
    USD_KRW,
    EcosSeries,
)
from cluefin_openapi.ecos._exceptions import (
    EcosAPIError,
    EcosAuthenticationError,
    EcosNetworkError,
    EcosNotFoundError,
    EcosRateLimitError,
    EcosRequestError,
    EcosSampleLimitError,
    EcosServerError,
    EcosTimeoutError,
)
from cluefin_openapi.ecos._model import EcosPage
from cluefin_openapi.ecos._statistic_catalog import StatisticCatalog
from cluefin_openapi.ecos._statistic_catalog_types import KeyStatistic, StatisticItem, StatisticTable
from cluefin_openapi.ecos._statistic_glossary import StatisticGlossary
from cluefin_openapi.ecos._statistic_glossary_types import StatisticMetaItem, StatisticWord
from cluefin_openapi.ecos._statistic_search import StatisticSearch
from cluefin_openapi.ecos._statistic_search_types import StatisticObservation

__all__ = [
    "Client",
    "SAMPLE_AUTH_KEY",
    "EcosPage",
    "EcosSeries",
    "KeyStatistic",
    "StatisticCatalog",
    "StatisticGlossary",
    "StatisticItem",
    "StatisticMetaItem",
    "StatisticObservation",
    "StatisticSearch",
    "StatisticTable",
    "StatisticWord",
    "CD_91D",
    "CORP_BOND_3Y_AA_MINUS",
    "CORP_BOND_3Y_BBB_MINUS",
    "CPI_TOTAL",
    "KTB_1Y",
    "KTB_3Y",
    "KTB_5Y",
    "KTB_10Y",
    "KTB_20Y",
    "KTB_30Y",
    "MARKET_RATES",
    "MSB_91D",
    "USD_KRW",
    "EcosAPIError",
    "EcosAuthenticationError",
    "EcosNetworkError",
    "EcosNotFoundError",
    "EcosRateLimitError",
    "EcosRequestError",
    "EcosSampleLimitError",
    "EcosServerError",
    "EcosTimeoutError",
]
