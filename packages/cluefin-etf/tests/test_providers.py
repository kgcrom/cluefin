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


@pytest.mark.parametrize(
    "provider_name",
    [name for name in PROVIDER_CLASSES if name not in {ProviderName.KODEX, ProviderName.SOL, ProviderName.KIWOOM}],
)
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
    provider = get_provider("tiger")

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


class SolListFetcher:
    list_url = "https://www.soletf.com/ko/fund"

    def __init__(self) -> None:
        self.calls = []
        self.html = """
        <html>
          <body>
            <table class="fd-list">
              <tbody>
                <tr id="tr_210980">
                  <td class="tb-subj">
                    <a href="/ko/fund/etf/210980" class="fd-link">
                      <span class="i-bdg-g">
                        <span class="i-bdg ty-1-2">국내주식</span>
                        <span class="i-bdg ty-1-3">소부장</span>
                        <span class="i-bdg ty-1-3">패시브</span>
                        <span class="i-bdg ty-1-1">개인연금</span>
                        <span class="i-bdg ty-1-1">퇴직연금</span>
                      </span>
                      <span class="fd-name">SOL  AI반도체소부장 <br> (455850)</span>
                    </a>
                  </td>
                  <td>31,789.71</td>
                  <td>13,272</td>
                  <td class="short">0.57</td>
                  <td class="short">32.62</td>
                  <td class="short">43.34</td>
                  <td class="short">84.93</td>
                  <td class="short">89.62</td>
                  <td class="long">211.87</td>
                  <td class="long">225.48</td>
                  <td class="long">-</td>
                  <td class="long">226.83</td>
                  <td></td>
                </tr>
                <tr id="tr_211106">
                  <td class="tb-subj">
                    <a href="/ko/fund/etf/211106" class="fd-link">
                      <span class="i-bdg-g">
                        <span class="i-bdg ty-1-2">국내주식</span>
                        <span class="i-bdg ty-1-3">메가트렌드</span>
                      </span>
                      <span class="fd-name">SOL AI반도체TOP2플러스 <br> (0167A0)</span>
                    </a>
                  </td>
                  <td>12,345.67</td>
                  <td>987</td>
                  <td class="short">1.23</td>
                  <td class="short">4.56</td>
                  <td class="short">7.89</td>
                  <td class="short">10.11</td>
                  <td class="short">12.13</td>
                  <td class="long">14.15</td>
                  <td class="long">16.17</td>
                  <td class="long">18.19</td>
                  <td class="long">20.21</td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </body>
        </html>
        """

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html=self.html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_sol_fetch_list_parses_server_rendered_table_and_maps_summaries():
    fetcher = SolListFetcher()
    provider = get_provider("sol", fetcher=fetcher)

    items = provider.fetch_list()

    assert [call[0] for call in fetcher.calls] == [fetcher.list_url]
    assert len(items) == 2
    assert items[0].provider == ProviderName.SOL
    assert items[0].code == "455850"
    assert items[0].name == "SOL AI반도체소부장"
    assert items[0].category == "국내주식 / 소부장 / 패시브"
    assert items[0].nav == Decimal("31789.71")
    assert items[0].aum == Decimal("13272")
    assert items[0].detail_url == "https://www.soletf.com/ko/fund/etf/210980"
    assert items[0].raw["fundCode"] == "210980"
    assert items[0].raw["etfCode"] == "455850"
    assert items[0].raw["pensionFlags"] == ["개인연금", "퇴직연금"]
    assert items[0].raw["returns"]["month_1"] == "32.62"
    assert items[0].raw["returns"]["year_5"] == "-"
    assert items[1].code == "0167A0"
    assert items[1].category == "국내주식 / 메가트렌드"


class KodexListFetcher:
    def __init__(self) -> None:
        self.calls = []
        self.pages = {
            "1": [
                {
                    "fNm": "KODEX AI전력핵심설비",
                    "stkTicker": "487240",
                    "fId": "2ETFN7",
                    "typeLnm": "국내주식",
                    "typeNm": "테마",
                    "listD": "20240709",
                    "gijunYMD": "20260430",
                    "basp": "57890.35",
                    "nav": "35789",
                    "curp": "58355",
                    "risep": "5535",
                    "risepRt": "10.48",
                    "basrp": "1919.99",
                    "basrpRt": "3.78",
                    "yieldWeek": "23.74",
                    "yieldMon1": "79.43",
                    "yieldMon3": "85.69",
                    "yieldMon6": "111.63",
                    "yieldYear1": "430.32",
                    "yieldYear3": None,
                    "yieldYear": "129.82",
                    "yieldList": "413.65",
                    "dcYn": "개인연금",
                    "irpYn": "퇴직연금",
                    "totalCnt": "21",
                }
            ]
            * 20,
            "2": [
                {
                    "fNm": "KODEX WTI원유선물(H)",
                    "stkTicker": "261220",
                    "fId": "2ETF72",
                    "typeLnm": "원자재 및 통화",
                    "listD": "20161227",
                    "gijunYMD": "20260430",
                    "basp": "26736.55",
                    "nav": "808",
                    "totalCnt": "21",
                }
            ],
        }

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        page_no = url.rsplit("pageNo=", maxsplit=1)[1]
        html = json.dumps(self.pages[page_no], ensure_ascii=False)
        result = FetchResult(
            html=html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_kodex_fetch_list_collects_all_pages_and_maps_summaries():
    fetcher = KodexListFetcher()
    provider = get_provider("kodex", fetcher=fetcher)

    items = provider.fetch_list()

    assert [call[0].rsplit("pageNo=", maxsplit=1)[1] for call in fetcher.calls] == ["1", "2"]
    assert all(call[2]["headers"] == {"Accept": "application/json"} for call in fetcher.calls)
    assert len(items) == 21
    assert items[0].provider == ProviderName.KODEX
    assert items[0].code == "487240"
    assert items[0].name == "KODEX AI전력핵심설비"
    assert items[0].category == "국내주식"
    assert items[0].listing_date == date(2024, 7, 9)
    assert items[0].as_of_date == date(2026, 4, 30)
    assert items[0].nav == Decimal("57890.35")
    assert items[0].aum == Decimal("35789")
    assert items[0].detail_url == "https://www.samsungfund.com/etf/product/view.do?id=2ETFN7"
    assert items[0].raw["curp"] == "58355"
    assert items[0].raw["yieldWeek"] == "23.74"
    assert items[0].raw["dcYn"] == "개인연금"
    assert items[0].raw["irpYn"] == "퇴직연금"
    assert items[-1].code == "261220"
