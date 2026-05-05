import json
from datetime import date
from decimal import Decimal

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


@pytest.mark.parametrize("provider_name", [name for name in PROVIDER_CLASSES if name is not ProviderName.KIWOOM])
def test_scaffolded_provider_list_methods(provider_name):
    provider = get_provider(provider_name)

    with pytest.raises(ProviderCapabilityError):
        provider.fetch_list()


@pytest.mark.parametrize("provider_name", list(PROVIDER_CLASSES))
def test_scaffolded_provider_detail_methods(provider_name):
    provider = get_provider(provider_name)

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


class KiwoomListFetcher:
    def __init__(self) -> None:
        self.calls = []
        self.pages = {
            "1": {
                "totalCnt": 2,
                "searchVO": {"pageNo": 1, "endPage": 2},
                "etfList": [
                    {
                        "gcode": "253250",
                        "goodsNm": "KIWOOM 200선물레버리지",
                        "goodsTypeNm": "국내주식",
                        "bsisIdex": "KOSPI 200 선물",
                        "idexNm": "ignored benchmark",
                        "setdate": "2016.09.09",
                        "standardprice": 104902,
                        "fundtotalamount": 56647551523,
                        "etcFlags": ["레버리지/인버스"],
                    }
                ],
            },
            "2": {
                "totalCnt": 2,
                "searchVO": {"pageNo": 2, "endPage": 2},
                "etfList": [
                    {
                        "gcode": "354500",
                        "goodsNm": "KIWOOM 코스닥150",
                        "goodsTypeNm": "국내주식",
                        "idexNm": "코스닥 150",
                        "setdate": "2020.08.07",
                        "standardprice": 12345,
                        "fundtotalamount": 987654321,
                    }
                ],
            },
        }

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        page_no = kwargs["data"]["pageNo"]
        html = json.dumps(self.pages[page_no], ensure_ascii=False)
        result = FetchResult(
            html=html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_kiwoom_fetch_list_collects_all_pages_and_maps_summaries():
    fetcher = KiwoomListFetcher()
    provider = get_provider("kiwoom", fetcher=fetcher)

    items = provider.fetch_list()

    assert [call[2]["data"]["pageNo"] for call in fetcher.calls] == ["1", "2"]
    assert all(call[2]["method"] == "POST" for call in fetcher.calls)
    assert all(call[2]["referrer"] == "https://www.kiwoometf.com/service/etf/KO02010100M" for call in fetcher.calls)
    assert all(call[2]["headers"]["X-Requested-With"] == "XMLHttpRequest" for call in fetcher.calls)
    assert len(items) == 2
    assert items[0].provider == ProviderName.KIWOOM
    assert items[0].code == "253250"
    assert items[0].name == "KIWOOM 200선물레버리지"
    assert items[0].category == "국내주식"
    assert items[0].benchmark == "KOSPI 200 선물"
    assert items[0].listing_date == date(2016, 9, 9)
    assert items[0].nav == Decimal("104902")
    assert items[0].aum == Decimal("56647551523")
    assert items[0].detail_url == "https://www.kiwoometf.com/service/etf/KO02010200M?gcode=253250"
    assert items[0].raw["etcFlags"] == ["레버리지/인버스"]
    assert items[1].benchmark == "코스닥 150"
