import time

import pytest

from cluefin_etf import EtfDetail, EtfHolding, EtfSummary, ProviderName, get_provider, list_providers

DETAIL_CASES = {
    ProviderName.KODEX: ("2ETFN7", "487240"),
    ProviderName.TIGER: ("102110", "102110"),
    ProviderName.RISE: ("252400", "252400"),
    ProviderName.ACE: ("KR5101877748", "KR5101877748"),
    ProviderName.SOL: ("210980", "455850"),
    ProviderName.KIWOOM: ("253250", "253250"),
}


@pytest.fixture(autouse=True)
def _provider_site_rate_limit(request):
    """Rate-limit guard for public ETF provider pages."""
    if request.node.get_closest_marker("integration"):
        time.sleep(1)


@pytest.mark.integration
@pytest.mark.parametrize("provider_name", list_providers())
def test_provider_fetch_list_integration(provider_name: ProviderName) -> None:
    provider = get_provider(provider_name)

    items = provider.fetch_list()

    assert items, f"{provider_name.value} ETF list is empty"
    for item in items[:3]:
        _assert_summary_shape(provider_name, item)


@pytest.mark.integration
@pytest.mark.parametrize("provider_name", list_providers())
def test_provider_fetch_detail_integration(provider_name: ProviderName) -> None:
    input_code, expected_code = DETAIL_CASES[provider_name]
    provider = get_provider(provider_name)

    detail = provider.fetch_detail(input_code)

    _assert_detail_shape(provider_name, detail, expected_code=expected_code)


def _assert_summary_shape(provider_name: ProviderName, item: EtfSummary) -> None:
    assert item.provider == provider_name
    assert item.code
    assert item.name
    assert item.detail_url


def _assert_detail_shape(provider_name: ProviderName, detail: EtfDetail, *, expected_code: str) -> None:
    assert detail.provider == provider_name
    assert detail.code == expected_code
    assert detail.name
    assert detail.detail_url
    assert detail.holdings, f"{provider_name.value} ETF detail has no holdings"
    _assert_holding_shape(detail.holdings[0])


def _assert_holding_shape(holding: EtfHolding) -> None:
    assert holding.name or holding.code
