import pytest

from cluefin_etf import (
    EtfDetail,
    EtfSummary,
    FetchMetadata,
    FetchResult,
    ProviderCapabilityError,
    ProviderName,
    ProviderNotFoundError,
    get_provider,
    list_providers,
)
from cluefin_etf._provider import EtfProvider
from cluefin_etf._registry import PROVIDER_CLASSES


def test_all_providers_are_registered():
    assert list_providers() == (
        ProviderName.KODEX,
        ProviderName.TIGER,
        ProviderName.RISE,
        ProviderName.ACE,
        ProviderName.SOL,
        ProviderName.KIWOOM,
    )


@pytest.mark.parametrize("provider_name", list(PROVIDER_CLASSES))
def test_provider_names_resolve_consistently(provider_name):
    provider = get_provider(provider_name)

    assert provider.name == provider_name
    assert provider.info.name == provider_name


def test_provider_lookup_accepts_strings():
    assert get_provider("kodex").name == ProviderName.KODEX
    assert get_provider("KODEX").name == ProviderName.KODEX


def test_unknown_provider_raises_provider_not_found():
    with pytest.raises(ProviderNotFoundError):
        get_provider("unknown")


@pytest.mark.parametrize("provider_name", list(PROVIDER_CLASSES))
def test_scaffolded_provider_methods(provider_name):
    provider = get_provider(provider_name)

    with pytest.raises(ProviderCapabilityError):
        provider.fetch_list()

    with pytest.raises(ProviderCapabilityError):
        provider.fetch_detail("069500")


def test_parse_hooks_are_not_implemented_yet():
    provider = get_provider("kodex")

    with pytest.raises(NotImplementedError):
        provider.parse_list_html("<html></html>")

    with pytest.raises(NotImplementedError):
        provider.parse_detail_html("069500", "<html></html>")


class ValidatingProvider(EtfProvider):
    list_url = "https://example.test/list"
    detail_url_template = "https://example.test/detail/{code}"
    info = PROVIDER_CLASSES[ProviderName.KODEX].info

    def validate_list_result(self, result: FetchResult) -> bool:
        return "valid" in result.html

    def validate_detail_result(self, result: FetchResult) -> bool:
        return "valid" in result.html

    def parse_list_html(self, html: str) -> list[EtfSummary]:
        return [EtfSummary(provider=self.name, code="069500", name="KODEX 200", raw={"html": html})]

    def parse_detail_html(self, code: str, html: str) -> EtfDetail:
        return EtfDetail(provider=self.name, code=code, name="KODEX 200", raw={"html": html})


class ValidatorAwareFetcher:
    def __init__(self) -> None:
        self.validators = []

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None) -> FetchResult:
        result = FetchResult(
            html="<html><body>valid provider page content</body></html>",
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.validators.append(validator)
        assert validator is not None
        assert validator(result) is True
        return result


def test_provider_passes_list_and_detail_validators_to_fetcher():
    fetcher = ValidatorAwareFetcher()
    provider = ValidatingProvider(fetcher=fetcher)

    items = provider.fetch_list()
    detail = provider.fetch_detail("069500")

    assert items[0].code == "069500"
    assert detail.code == "069500"
    assert len(fetcher.validators) == 2
