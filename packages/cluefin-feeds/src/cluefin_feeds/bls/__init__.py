"""미 노동통계국 BLS Public Data API (키 없이 v1, 등록 키가 있으면 v2).

https://www.bls.gov/developers/
"""

from cluefin_feeds.bls._client import BlsAPIError, BlsDailyLimitError, Client
from cluefin_feeds.bls._types import BlsFootnote, BlsObservation, BlsResponse, BlsSeries

# CPI-U 전 품목, 비계절조정 (1982-84=100). dartrail 이 2015년 달러 환산에 썼다.
CPI_U_ALL_ITEMS = "CUUR0000SA0"

__all__ = [
    "BlsAPIError",
    "BlsDailyLimitError",
    "BlsFootnote",
    "BlsObservation",
    "BlsResponse",
    "BlsSeries",
    "CPI_U_ALL_ITEMS",
    "Client",
]
