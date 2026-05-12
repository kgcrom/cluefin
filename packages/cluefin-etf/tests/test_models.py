import pytest
from pydantic import ValidationError

from cluefin_etf import EtfDetail, EtfHolding, EtfSummary, ProviderName


def test_provider_names_are_normalized_from_strings():
    summary = EtfSummary(
        provider="KODEX",
        code="069500",
        name="KODEX 200",
    )
    detail = EtfDetail(
        provider="tiger",
        code="102110",
        name="TIGER 200",
    )

    assert summary.provider == ProviderName.KODEX
    assert detail.provider == ProviderName.TIGER


def test_model_default_containers_are_isolated():
    first = EtfDetail(provider="kodex", code="069500")
    second = EtfDetail(provider="kodex", code="229200")

    first.holdings.append(EtfHolding(code="005930", name="삼성전자"))
    first.raw["source"] = "first"

    assert second.holdings == []
    assert second.raw == {}


def test_models_are_frozen():
    summary = EtfSummary(provider="kodex", code="069500", name="KODEX 200")

    with pytest.raises(ValidationError):
        summary.code = "229200"
