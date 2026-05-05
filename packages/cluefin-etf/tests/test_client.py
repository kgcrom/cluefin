import pytest

import cluefin_etf._client as client_module
from cluefin_etf import EtfClient, EtfDetail, EtfSummary, ProviderName, ProviderNotFoundError


class FakeProvider:
    name = ProviderName.KODEX

    def __init__(self) -> None:
        self.detail_codes: list[str] = []

    def fetch_list(self) -> list[EtfSummary]:
        return [
            EtfSummary(
                provider=self.name,
                code="069500",
                name="KODEX 200",
                raw={"source": "fake-provider"},
            )
        ]

    def fetch_detail(self, code: str) -> EtfDetail:
        self.detail_codes.append(code)
        return EtfDetail(
            provider=self.name,
            code=code,
            name="KODEX 200",
            raw={"source": "fake-provider"},
        )


class FakeFetcher:
    pass


def test_client_resolves_provider_with_supplied_fetcher(monkeypatch):
    provider = FakeProvider()
    fetcher = FakeFetcher()
    calls = []

    def get_provider(name, *, fetcher=None):
        calls.append((name, fetcher))
        return provider

    monkeypatch.setattr(client_module, "get_provider", get_provider)

    client = EtfClient("kodex", fetcher=fetcher)

    assert client.provider is provider
    assert calls == [("kodex", fetcher)]


def test_client_fetch_list_delegates_to_provider(monkeypatch):
    provider = FakeProvider()
    monkeypatch.setattr(client_module, "get_provider", lambda name, *, fetcher=None: provider)

    items = EtfClient(ProviderName.KODEX, fetcher=FakeFetcher()).fetch_list()

    assert items == [
        EtfSummary(
            provider=ProviderName.KODEX,
            code="069500",
            name="KODEX 200",
            raw={"source": "fake-provider"},
        )
    ]


def test_client_fetch_detail_delegates_code_to_provider(monkeypatch):
    provider = FakeProvider()
    monkeypatch.setattr(client_module, "get_provider", lambda name, *, fetcher=None: provider)

    detail = EtfClient(ProviderName.KODEX, fetcher=FakeFetcher()).fetch_detail("069500")

    assert detail == EtfDetail(
        provider=ProviderName.KODEX,
        code="069500",
        name="KODEX 200",
        raw={"source": "fake-provider"},
    )
    assert provider.detail_codes == ["069500"]


def test_client_propagates_unknown_provider_error(monkeypatch):
    def get_provider(name, *, fetcher=None):
        raise ProviderNotFoundError(f"Unknown ETF provider: {name}")

    monkeypatch.setattr(client_module, "get_provider", get_provider)

    with pytest.raises(ProviderNotFoundError, match="unknown"):
        EtfClient("unknown", fetcher=FakeFetcher())
