from cluefin_etf._fetchers import PageFetcher, create_default_fetcher
from cluefin_etf._models import EtfDetail, EtfSummary, ProviderName
from cluefin_etf._registry import get_provider


class EtfClient:
    """Small convenience client that delegates to a registered ETF provider."""

    def __init__(self, provider: ProviderName | str, fetcher: PageFetcher | None = None) -> None:
        self.provider = get_provider(provider, fetcher=fetcher or create_default_fetcher())

    def fetch_list(self) -> list[EtfSummary]:
        return self.provider.fetch_list()

    def fetch_detail(self, code: str) -> EtfDetail:
        return self.provider.fetch_detail(code)
