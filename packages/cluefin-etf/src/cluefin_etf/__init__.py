"""ETF page scraping scaffolds for Korean asset managers."""

from importlib.metadata import PackageNotFoundError, version

from cluefin_etf._client import EtfClient
from cluefin_etf._errors import CluefinEtfError, FetchError, ProviderCapabilityError, ProviderNotFoundError
from cluefin_etf._fetchers import (
    FallbackFetcher,
    PageValidator,
    PlaywrightBrowserSession,
    PlaywrightFetcher,
    SimpleHttpFetcher,
)
from cluefin_etf._models import EtfDetail, EtfSummary, FetchMetadata, FetchResult, ProviderInfo, ProviderName
from cluefin_etf._registry import get_provider, list_providers

try:
    __version__ = version("cluefin-etf")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "CluefinEtfError",
    "EtfClient",
    "EtfDetail",
    "EtfSummary",
    "FallbackFetcher",
    "FetchError",
    "FetchMetadata",
    "FetchResult",
    "PlaywrightFetcher",
    "PlaywrightBrowserSession",
    "ProviderInfo",
    "ProviderName",
    "PageValidator",
    "ProviderCapabilityError",
    "ProviderNotFoundError",
    "SimpleHttpFetcher",
    "get_provider",
    "list_providers",
]
