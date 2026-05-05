from cluefin_etf._errors import ProviderCapabilityError
from cluefin_etf._fetchers import PageFetcher, create_default_fetcher
from cluefin_etf._models import EtfDetail, EtfSummary, FetchResult, ProviderInfo, ProviderName


class EtfProvider:
    """Base provider scaffold for one ETF issuer page."""

    info: ProviderInfo
    list_url: str | None = None
    detail_url_template: str | None = None

    def __init__(self, fetcher: PageFetcher | None = None) -> None:
        self.fetcher = fetcher or create_default_fetcher()

    @property
    def name(self) -> ProviderName:
        return self.info.name

    def fetch_list(self) -> list[EtfSummary]:
        if self.list_url is None:
            raise ProviderCapabilityError(f"{self.name.value} ETF list URL is not implemented yet")

        result = self.fetcher.fetch(self.list_url, provider=self.name, validator=self.validate_list_result)
        return self.parse_list_html(result.html)

    def fetch_detail(self, code: str) -> EtfDetail:
        if self.detail_url_template is None:
            raise ProviderCapabilityError(f"{self.name.value} ETF detail URL is not implemented yet")

        url = self.detail_url_template.format(code=code)
        result = self.fetcher.fetch(url, provider=self.name, validator=self.validate_detail_result)
        return self.parse_detail_html(code, result.html)

    def validate_list_result(self, result: FetchResult) -> bool:
        return True

    def validate_detail_result(self, result: FetchResult) -> bool:
        return True

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        raise NotImplementedError("ETF list parsing is not implemented yet")

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        raise NotImplementedError("ETF detail parsing is not implemented yet")
