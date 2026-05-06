import json
from datetime import date
from decimal import Decimal

import pytest

from cluefin_etf import (
    EtfDetail,
    EtfSummary,
    FetchError,
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
    [
        name
        for name in PROVIDER_CLASSES
        if name not in {ProviderName.KODEX, ProviderName.TIGER, ProviderName.ACE, ProviderName.SOL, ProviderName.KIWOOM}
    ],
)
def test_scaffolded_provider_list_methods(provider_name):
    provider = get_provider(provider_name)

    with pytest.raises(ProviderCapabilityError):
        provider.fetch_list()


@pytest.mark.parametrize("provider_name", list(PROVIDER_CLASSES))
def test_scaffolded_provider_detail_methods(provider_name):
    if provider_name is not ProviderName.RISE:
        pytest.skip("detail fetching is implemented for non-RISE providers")

    provider = get_provider(provider_name)

    with pytest.raises(ProviderCapabilityError):
        provider.fetch_detail("069500")


def test_parse_hooks_are_not_implemented_yet():
    provider = get_provider("rise")

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


def _kiwoom_fetch_result(payload: dict) -> FetchResult:
    return FetchResult(
        html=json.dumps(payload, ensure_ascii=False),
        metadata=FetchMetadata(provider=ProviderName.KIWOOM, url="https://example.test/kiwoom", strategy="http"),
    )


def _fetch_result(provider_name: ProviderName, html: str) -> FetchResult:
    return FetchResult(
        html=html,
        metadata=FetchMetadata(
            provider=provider_name, url=f"https://example.test/{provider_name.value}", strategy="http"
        ),
    )


def test_kiwoom_list_validator_rejects_empty_json_object():
    provider = get_provider("kiwoom")

    assert provider.validate_list_result(_kiwoom_fetch_result({})) is False


def test_kiwoom_list_validator_rejects_empty_items_with_positive_total_count():
    provider = get_provider("kiwoom")

    result = _kiwoom_fetch_result({"totalCnt": 1, "searchVO": {"pageNo": 1, "endPage": 1}, "etfList": []})

    assert provider.validate_list_result(result) is False


def test_kiwoom_list_validator_rejects_items_missing_required_fields():
    provider = get_provider("kiwoom")

    result = _kiwoom_fetch_result(
        {"totalCnt": 1, "searchVO": {"pageNo": 1, "endPage": 1}, "etfList": [{"gcode": "253250"}]}
    )

    assert provider.validate_list_result(result) is False


def test_kiwoom_list_validator_rejects_positive_total_count_without_end_page():
    provider = get_provider("kiwoom")

    result = _kiwoom_fetch_result(
        {
            "totalCnt": 1,
            "searchVO": {"pageNo": 1},
            "etfList": [{"gcode": "253250", "goodsNm": "KIWOOM 200선물레버리지"}],
        }
    )

    assert provider.validate_list_result(result) is False


class AceListFetcher:
    page_url = "https://www.aceetf.co.kr/modal/allfund"
    chunk_url = "https://www.aceetf.co.kr/_next/static/chunks/pages/modal/allfund-test.js"

    def __init__(self) -> None:
        self.calls = []
        self.responses = {
            self.page_url: (
                '<html><script src="/_next/static/chunks/pages/modal/allfund-test.js" defer=""></script></html>'
            ),
            self.chunk_url: (
                'children:["국내주식/대표지수",(0,l.jsx)("span",{className:"cnt",children:"2건"})]'
                'onClick:()=>goPage(t.G.FundDetail,"KR5101877748"),className:"txt",children:"ACE 200"})}),'
                '(0,l.jsx)("span",{className:"type1",children:"개인연금"}),'
                '(0,l.jsx)("span",{className:"type2",children:"퇴직연금"})'
                'onClick:()=>goPage(t.G.FundDetail,"K55101CT6711"),className:"txt",children:"ACE 200TR"})})'
                'children:["국내채권",(0,l.jsx)("span",{className:"cnt",children:"1건"})]'
                'onClick:()=>goPage(t.G.FundDetail,"K55101B26297"),className:"txt",children:"ACE 국고채10년"})}),'
                '(0,l.jsx)("span",{className:"type2",children:"퇴직연금"})'
            ),
        }

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html=self.responses[url],
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_ace_fetch_list_loads_allfund_chunk_and_maps_summaries():
    fetcher = AceListFetcher()
    provider = get_provider("ace", fetcher=fetcher)

    items = provider.fetch_list()

    assert [call[0] for call in fetcher.calls] == [fetcher.page_url, fetcher.chunk_url]
    assert len(items) == 3
    assert items[0].provider == ProviderName.ACE
    assert items[0].code == "KR5101877748"
    assert items[0].isin == "KR5101877748"
    assert items[0].name == "ACE 200"
    assert items[0].category == "국내주식/대표지수"
    assert items[0].detail_url == "https://www.aceetf.co.kr/fund/KR5101877748"
    assert items[0].raw["fundCode"] == "KR5101877748"
    assert items[0].raw["pensionFlags"] == ["개인연금", "퇴직연금"]
    assert items[1].raw["pensionFlags"] == []
    assert items[2].category == "국내채권"
    assert items[2].raw["pensionFlags"] == ["퇴직연금"]


def test_ace_validators_reject_missing_or_malformed_payloads():
    provider = get_provider("ace")

    assert provider.validate_list_result(_fetch_result(ProviderName.ACE, "<html></html>")) is False
    assert provider._validate_chunk_result(_fetch_result(ProviderName.ACE, "children:[]")) is False
    assert provider._validate_detail_page_result(_fetch_result(ProviderName.ACE, "<html></html>")) is False
    assert provider.validate_detail_result(_fetch_result(ProviderName.ACE, "{")) is False
    assert provider.validate_detail_result(_fetch_result(ProviderName.ACE, '{"fundCd":"KR5101877748"}')) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.ACE, "{")) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.ACE, '{"pdfList":{}}')) is False


class AceDetailFetcher:
    page_url = "https://www.aceetf.co.kr/fund/KR5101877748"
    api_url = "https://papi.aceetf.co.kr/api/funds/KR5101877748"
    holdings_url = "https://papi.aceetf.co.kr/api/funds/KR5101877748/pdf"

    def __init__(self) -> None:
        self.calls = []
        self.responses = {
            self.page_url: '<script id="__NEXT_DATA__">{"page":"/fund/[fundCode]"}</script>',
            self.api_url: json.dumps(
                {
                    "fundCd": "KR5101877748",
                    "stockCd": "105190",
                    "fundNm": "ACE 200",
                    "fundWhlNm": "한국투자ACE200증권상장지수투자신탁(주식)",
                    "stdDt": 20260504,
                    "stpr": 105997.65,
                    "nastAmt": 1685362580416,
                    "lstdDt": 20081020,
                    "summaryContent": "코스피 200을 추종합니다.",
                    "noticeContent": "투자 전 주의사항 원문",
                    "badge": {
                        "assetTypeNames": ["주식"],
                        "regionTypeNames": ["국내"],
                        "themeTypeNames": ["대표지수", "한국투자"],
                        "stockCode": "105190",
                    },
                },
                ensure_ascii=False,
            ),
            self.holdings_url: json.dumps(
                {
                    "pdfList": [
                        {
                            "rank": 1,
                            "jm_KSC_CD": "005930",
                            "sec_NM": "삼성전자",
                            "cu_ITEM_CNT": "6918",
                            "val_AM": 1608435000,
                            "wg": 30.67,
                            "std_DT": "2026-05-06",
                        }
                    ]
                },
                ensure_ascii=False,
            ),
        }

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html=self.responses[url],
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_ace_fetch_detail_loads_page_then_api_and_maps_detail():
    fetcher = AceDetailFetcher()
    provider = get_provider("ace", fetcher=fetcher)

    detail = provider.fetch_detail("KR5101877748")

    assert [call[0] for call in fetcher.calls] == [fetcher.page_url, fetcher.api_url, fetcher.holdings_url]
    assert fetcher.calls[1][2]["headers"] == {"Accept": "application/json"}
    assert fetcher.calls[2][2]["headers"] == {"Accept": "application/json"}
    assert detail.provider == ProviderName.ACE
    assert detail.code == "KR5101877748"
    assert detail.isin == "KR5101877748"
    assert detail.name == "ACE 200"
    assert detail.category == "국내 / 주식 / 대표지수 / 한국투자"
    assert detail.listing_date == date(2008, 10, 20)
    assert detail.nav == Decimal("105997.65")
    assert detail.aum == Decimal("1685362580416")
    assert detail.as_of_date == date(2026, 5, 4)
    assert detail.holdings_url == fetcher.holdings_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].rank == 1
    assert detail.holdings[0].code == "005930"
    assert detail.holdings[0].name == "삼성전자"
    assert detail.holdings[0].quantity == Decimal("6918")
    assert detail.holdings[0].valuation_amount == Decimal("1608435000")
    assert detail.holdings[0].weight == Decimal("30.67")
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert detail.raw["badge"]["stockCode"] == "105190"
    assert "noticeContent" not in detail.raw
    assert set(detail.raw) == {
        "fundCd",
        "stockCd",
        "fundNm",
        "fundWhlNm",
        "stdDt",
        "stpr",
        "nastAmt",
        "lstdDt",
        "badge",
        "summaryContent",
    }
    assert set(detail.holdings[0].raw) == {"rank", "jm_KSC_CD", "sec_NM", "cu_ITEM_CNT", "val_AM", "wg", "std_DT"}


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


def test_sol_validators_reject_missing_or_malformed_payloads():
    provider = get_provider("sol")

    assert provider.validate_list_result(_fetch_result(ProviderName.SOL, "<html></html>")) is False
    assert provider.validate_detail_result(_fetch_result(ProviderName.SOL, "<html></html>")) is False
    assert provider.validate_holdings_page_result(_fetch_result(ProviderName.SOL, "<html></html>")) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.SOL, "{")) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.SOL, '{"pdfList":[]}')) is False


def test_sol_parse_detail_html_maps_server_rendered_detail_page():
    provider = get_provider("sol")
    html = """
    <html>
      <body>
        <span class="i-bdg-g">
          <span class="i-bdg ty-1-2">국내주식</span>
          <span class="i-bdg ty-1-3">소부장</span>
          <span class="i-bdg ty-1-3">패시브</span>
          <span class="i-bdg ty-1-1">개인연금</span>
        </span>
        <h1 class="fv-name">SOL  AI반도체소부장 (455850)</h1>
        <div class="fv-exp">
          <dl><dt><strong>시장가격</strong>(원)</dt><dd class="fd-pri">31,800</dd></dl>
          <dl><dt><strong>기준가격</strong>(원)</dt><dd class="fd-pri">31,789.71</dd></dl>
        </div>
        <div class="cont-col">
          <div class="cc-title"><h3 class="g-title">기초지수정보</h3></div>
          <div class="cc-cont"><dl class="g-conts"><dt>FnGuide AI 반도체 소부장 지수</dt><dd>설명</dd></dl></div>
        </div>
        <div class="cont-col">
          <div class="cc-title"><h3 class="g-title">기본정보</h3></div>
          <div class="cc-cont">
            <dl class="def"><dt>순자산 총액</dt><dd>1조 3,272억원</dd></dl>
            <dl class="def"><dt>상장일</dt><dd>2023.04.25</dd></dl>
            <dl class="def"><dt>총보수</dt><dd>0.45%(집합투자: 0.4%)</dd></dl>
          </div>
        </div>
        <a href="/ko/fund/etf/210980">상품</a>
      </body>
    </html>
    """

    detail = provider.parse_detail_html("210980", html)

    assert detail.provider == ProviderName.SOL
    assert detail.code == "455850"
    assert detail.name == "SOL AI반도체소부장"
    assert detail.category == "국내주식 / 소부장 / 패시브"
    assert detail.benchmark == "FnGuide AI 반도체 소부장 지수"
    assert detail.listing_date == date(2023, 4, 25)
    assert detail.nav == Decimal("31789.71")
    assert detail.aum == Decimal("13272")
    assert detail.expense_ratio == Decimal("0.45")
    assert detail.raw["pensionFlags"] == ["개인연금"]


class SolDetailFetcher:
    list_url = "https://www.soletf.com/ko/fund"
    detail_url = "https://www.soletf.com/ko/fund/etf/210980"
    holdings_page_url = "https://www.soletf.com/ko/fund/etf/210980?tabIndex=3"
    holdings_url = "https://www.soletf.com/api/fund/pdfList?fund_cd=210980&work_dt=20260506"

    def __init__(self) -> None:
        self.calls = []
        self.responses = {
            self.list_url: """
            <table class="fd-list"><tbody><tr id="tr_210980">
              <td class="tb-subj"><a href="/ko/fund/etf/210980" class="fd-link">
                <span class="fd-name">SOL AI반도체소부장 <br> (455850)</span>
              </a></td><td>31,789.71</td><td>13,272</td>
            </tr></tbody></table>
            """,
            self.detail_url: """
            <html><body>
              <h1 class="fv-name">SOL AI반도체소부장 (455850)</h1>
              <div class="fv-exp"><dl><dt>기준가격</dt><dd class="fd-pri">31,789.71</dd></dl></div>
              <div class="notice">투자 유의사항 원문은 화면 안내용입니다.</div>
              <a href="/ko/fund/etf/210980">상품</a>
            </body></html>
            """,
            self.holdings_page_url: """
            <html><body>
              <input type="text" id="f-pdf-calendar" value="2026-05-06"/>
              <table id="pdf-table"><tbody><tr><td>1</td><td>한미반도체</td><td>981</td><td>370,818,000</td><td>23.33%</td></tr></tbody></table>
            </body></html>
            """,
            self.holdings_url: json.dumps(
                [
                    {
                        "SEQ_NO": 7,
                        "STOCK_CODE": "042700",
                        "SEC_NM": "한미반도체",
                        "QTY": 981,
                        "PRICE": 370818000,
                        "WT_DISP": "23.33%",
                        "WORK_DT": "20260506",
                    }
                ],
                ensure_ascii=False,
            ),
        }

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html=self.responses[url],
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_sol_fetch_detail_fetches_pdf_holdings():
    fetcher = SolDetailFetcher()
    provider = get_provider("sol", fetcher=fetcher)

    detail = provider.fetch_detail("455850")

    assert [call[0] for call in fetcher.calls] == [
        fetcher.list_url,
        fetcher.detail_url,
        fetcher.holdings_page_url,
        fetcher.holdings_url,
    ]
    assert detail.holdings_url == fetcher.holdings_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].rank == 1
    assert detail.holdings[0].code == "042700"
    assert detail.holdings[0].name == "한미반도체"
    assert detail.holdings[0].quantity == Decimal("981")
    assert detail.holdings[0].valuation_amount == Decimal("370818000")
    assert detail.holdings[0].weight == Decimal("23.33")
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert set(detail.holdings[0].raw) == {"WORK_DT", "SEQ_NO", "STOCK_CODE", "SEC_NM", "QTY", "PRICE", "WT_DISP"}
    assert "유의사항" not in str(detail.raw)


class SolRenderedHoldingsFallbackFetcher(SolDetailFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.responses[self.holdings_page_url] = """
        <html><body>
          <table id="pdf-table">
            <tbody>
              <tr><td>1</td><td>한미반도체</td><td>981</td><td>370,818,000</td><td>23.33%</td></tr>
            </tbody>
          </table>
        </body></html>
        """


def test_sol_fetch_detail_uses_rendered_holdings_table_when_work_date_is_missing():
    fetcher = SolRenderedHoldingsFallbackFetcher()
    provider = get_provider("sol", fetcher=fetcher)

    detail = provider.fetch_detail("455850")

    assert [call[0] for call in fetcher.calls] == [
        fetcher.list_url,
        fetcher.detail_url,
        fetcher.holdings_page_url,
    ]
    assert detail.holdings_url == fetcher.holdings_page_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].rank == 1
    assert detail.holdings[0].code is None
    assert detail.holdings[0].name == "한미반도체"
    assert detail.holdings[0].quantity == Decimal("981")
    assert detail.holdings[0].valuation_amount == Decimal("370818000")
    assert detail.holdings[0].weight == Decimal("23.33")
    assert detail.holdings[0].as_of_date is None
    assert set(detail.holdings[0].raw) == {"rank", "name", "quantity", "valuationAmount", "weight"}


def test_kiwoom_parse_detail_html_maps_server_rendered_detail_page():
    provider = get_provider("kiwoom")
    html = """
    <html>
      <body>
        <div class="fund-title">
          국내주식 레버리지/인버스
          <h2>KIWOOM 200선물레버리지</h2>
          <p class="fund-code">(종목코드 : 253250)</p>
        </div>
        <div class="fund-info-wrap">
          <p class="note">2026.05.05 기준</p>
          <dl class="summary">
            <div><dt>기준가</dt><dd>115,862.00<span class="unit">원</span></dd></div>
            <div><dt>순자산 규모</dt><dd><strong>625.66<span class="unit">억원</span></strong></dd></div>
          </dl>
        </div>
        <div class="fund-detail-info">
          <dl>
            <div><dt>상품명</dt><dd>키움 KIWOOM 200 선물 레버리지 증권상장지수투자신탁[주식-파생형]</dd></div>
            <div><dt>기초지수</dt><dd>F-KOSPI200</dd></div>
            <div><dt>설정일(상장일)</dt><dd>2016년 9월 9일 ( 2016년 9월 12일)</dd></div>
            <div><dt>보수(연)</dt><dd><pre>연 0.46% (판매 연0.05%)</pre></dd></div>
          </dl>
        </div>
      </body>
    </html>
    """

    detail = provider.parse_detail_html("253250", html)

    assert detail.provider == ProviderName.KIWOOM
    assert detail.code == "253250"
    assert detail.name == "KIWOOM 200선물레버리지"
    assert detail.category == "국내주식 레버리지/인버스 (종목코드 : 253250)"
    assert detail.benchmark == "F-KOSPI200"
    assert detail.listing_date == date(2016, 9, 9)
    assert detail.nav == Decimal("115862.00")
    assert detail.aum == Decimal("625.66")
    assert detail.expense_ratio == Decimal("0.46")
    assert detail.as_of_date == date(2026, 5, 5)


class KiwoomDetailFetcher:
    detail_url = "https://www.kiwoometf.com/service/etf/KO02010200M?gcode=253250"
    holdings_url = "https://www.kiwoometf.com/service/etf/KO02010200MAjax4"

    def __init__(self) -> None:
        self.calls = []
        self.detail_html = """
        <html>
          <body>
            <div class="fund-title">
              국내주식 레버리지/인버스
              <h2>KIWOOM 200선물레버리지</h2>
              <p class="fund-code">(종목코드 : 253250)</p>
            </div>
            <input id="pdfDt" value="2026-05-06"/>
            <div class="fund-info-wrap">
              <p class="note">2026.05.06 기준</p>
              <dl class="summary">
                <div><dt>기준가</dt><dd>115,862.00<span class="unit">원</span></dd></div>
              </dl>
            </div>
            <ul class="notice"><li>투자원금의 손실이 발생할 수 있습니다.</li></ul>
          </body>
        </html>
        """
        self.holdings_json = json.dumps(
            {
                "pdfList": [
                    {
                        "gcode": "KR7069660009",
                        "businessDate": "2026.05.06",
                        "fundcode": "005930",
                        "itemCode": "005930",
                        "itemTitle": "삼성전자",
                        "volume": "7,039",
                        "assessment": "1,636,567,500",
                        "ratio": "31.02%",
                    }
                ]
            },
            ensure_ascii=False,
        )

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        html = self.detail_html if url == self.detail_url else self.holdings_json
        result = FetchResult(
            html=html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_kiwoom_fetch_detail_fetches_pdf_holdings():
    fetcher = KiwoomDetailFetcher()
    provider = get_provider("kiwoom", fetcher=fetcher)

    detail = provider.fetch_detail("253250")

    assert [call[0] for call in fetcher.calls] == [fetcher.detail_url, fetcher.holdings_url]
    assert fetcher.calls[1][2]["method"] == "POST"
    assert fetcher.calls[1][2]["data"] == {"schGubun1": "253250", "startDate": "20260506"}
    assert detail.holdings_url == fetcher.holdings_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].code == "005930"
    assert detail.holdings[0].name == "삼성전자"
    assert detail.holdings[0].quantity == Decimal("7039")
    assert detail.holdings[0].valuation_amount == Decimal("1636567500")
    assert detail.holdings[0].weight == Decimal("31.02")
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert "투자원금" not in str(detail.raw)
    assert set(detail.holdings[0].raw) == {
        "businessDate",
        "itemCode",
        "gcode",
        "fundcode",
        "itemTitle",
        "volume",
        "assessment",
        "ratio",
    }


class KiwoomRenderedHoldingsFallbackFetcher(KiwoomDetailFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.detail_html = (
            self.detail_html
            + """
            <table>
              <caption>구성종목(PDF) 정보 테이블입니다.</caption>
              <thead>
                <tr><th>NO.</th><th>종목명</th><th>종목코드</th><th>비중</th></tr>
              </thead>
              <tbody>
                <tr><td>1</td><td>설정현금액</td><td>CASH00000001</td><td>-</td></tr>
                <tr><td>2</td><td>현금</td><td>KRD010010001</td><td>-</td></tr>
                <tr><td>3</td><td>KIWOOM 200</td><td>KR7069660009</td><td>17.20%</td></tr>
                <tr><td>4</td><td>선물2026년06월물</td><td>KR4A01660005</td><td>0.00%</td></tr>
              </tbody>
            </table>
            """
        )

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        if url == self.holdings_url:
            raise FetchError("Kiwoom holdings API failed")
        return super().fetch(url, provider=provider, validator=validator, **kwargs)


def test_kiwoom_fetch_detail_falls_back_to_rendered_pdf_table_when_api_fails():
    fetcher = KiwoomRenderedHoldingsFallbackFetcher()
    provider = get_provider("kiwoom", fetcher=fetcher)

    detail = provider.fetch_detail("253250")

    assert [call[0] for call in fetcher.calls] == [fetcher.detail_url]
    assert detail.holdings_url == f"{fetcher.detail_url}#pdf"
    assert len(detail.holdings) == 4
    assert detail.holdings[0].rank == 1
    assert detail.holdings[0].code == "CASH00000001"
    assert detail.holdings[0].name == "설정현금액"
    assert detail.holdings[0].weight is None
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert detail.holdings[2].rank == 3
    assert detail.holdings[2].code == "KR7069660009"
    assert detail.holdings[2].name == "KIWOOM 200"
    assert detail.holdings[2].weight == Decimal("17.20")
    assert detail.holdings[2].quantity is None
    assert detail.holdings[2].valuation_amount is None
    assert set(detail.holdings[2].raw) == {"rank", "itemCode", "itemTitle", "ratio"}


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


def test_kodex_validators_reject_missing_or_malformed_payloads():
    provider = get_provider("kodex")

    assert provider.validate_list_result(_fetch_result(ProviderName.KODEX, "{")) is False
    assert (
        provider.validate_list_result(
            _fetch_result(ProviderName.KODEX, json.dumps([{"fNm": "KODEX AI전력핵심설비"}], ensure_ascii=False))
        )
        is False
    )
    assert provider.validate_detail_result(_fetch_result(ProviderName.KODEX, "<html></html>")) is False
    assert provider.validate_product_result(_fetch_result(ProviderName.KODEX, '{"pdf":{}}')) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.KODEX, "{")) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.KODEX, '{"pdf":{}}')) is False
    assert provider.validate_rendered_holdings_result(_fetch_result(ProviderName.KODEX, "<table></table>")) is False


class TigerListFetcher:
    search_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/list.ajax"

    def __init__(self) -> None:
        self.calls = []
        self.html = """
        <div class="c-data-row" data-tot-cnt="225" data-period-type="short" data-ksd-fund="KR7243880002">
          <div class="category">
            <span class="each">주식</span>
            <span class="each">섹터</span>
            <span class="each">개인연금</span>
            <span class="each">퇴직연금 70%</span>
          </div>
          <div class="title"><a>TIGER 200 IT레버리지</a></div>
          <div class="code">(243880)</div>
          <div class="c-pair-group">
            <div class="c-pair"><span class="key">순자산 (억원)</span><span class="value">3,148</span></div>
            <div class="c-pair"><span class="key">기준가 (원)</span><span class="value">443,263.65원</span></div>
            <div class="c-pair"><span class="key">상장일</span><span class="value">2016.05.13</span></div>
          </div>
          <div class="variations shortPeriod">
            <div class="each"><span class="lead">1주</span><span class="variance"><span class="val">17.06</span></span></div>
            <div class="each"><span class="lead">1개월</span><span class="variance"><span class="val">141.13</span></span></div>
            <div class="each"><span class="lead">3년</span><span class="variance"><span class="val">-</span></span></div>
          </div>
        </div>
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


def test_tiger_fetch_list_maps_search_rows_to_summaries():
    fetcher = TigerListFetcher()
    provider = get_provider("tiger", fetcher=fetcher)

    items = provider.fetch_list()

    assert [call[0] for call in fetcher.calls] == [fetcher.search_url]
    assert fetcher.calls[0][2]["method"] == "POST"
    assert fetcher.calls[0][2]["data"]["q"] == ""
    assert fetcher.calls[0][2]["data"]["listCnt"] == "500"
    assert items == [
        EtfSummary(
            provider=ProviderName.TIGER,
            code="243880",
            isin="KR7243880002",
            name="TIGER 200 IT레버리지",
            category="주식 / 섹터",
            listing_date=date(2016, 5, 13),
            nav=Decimal("443263.65"),
            aum=Decimal("3148"),
            detail_url="https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7243880002",
            raw={
                "ksdFund": "KR7243880002",
                "categories": ["주식", "섹터", "개인연금", "퇴직연금 70%"],
                "pensionFlags": ["개인연금", "퇴직연금 70%"],
                "returns": {"1주": "17.06", "1개월": "141.13", "3년": None},
                "totalCount": 225,
            },
        )
    ]


def test_tiger_validators_reject_missing_payloads():
    provider = get_provider("tiger")

    assert provider.validate_list_result(_fetch_result(ProviderName.TIGER, "<html></html>")) is False
    assert provider.validate_detail_result(_fetch_result(ProviderName.TIGER, "<html></html>")) is False
    assert provider.validate_holdings_page_result(_fetch_result(ProviderName.TIGER, "<html></html>")) is False
    assert provider.validate_holdings_result(_fetch_result(ProviderName.TIGER, "<table></table>")) is False
    assert provider._validate_search_result(_fetch_result(ProviderName.TIGER, "<html></html>")) is False


class KodexDetailFetcher:
    detail_url = "https://www.samsungfund.com/etf/product/view.do?id=2ETFN7"
    product_url = "https://www.samsungfund.com/api/v1/kodex/product/2ETFN7.do"
    holdings_url = "https://www.samsungfund.com/api/v1/kodex/product-pdf/2ETFN7.do?gijunYMD=20260506"

    def __init__(self) -> None:
        self.calls = []
        self.responses = {}
        self.responses[self.detail_url] = """
        <html>
          <head>
            <meta name="description"
              content="KODEX AI전력핵심설비 ETF는 국내주식형 ETF이며 기초지수는 iSelect AI전력핵심설비 지수(Price Return)입니다. 상품정보, 수익률, 구성종목, 보수, 분배금 및 투자 유의사항을 확인하세요."/>
            <script type="application/ld+json">
            {
              "@context": "https://schema.org",
              "@type": "InvestmentFund",
              "name": "KODEX AI전력핵심설비",
              "tickerSymbol": "487240",
              "identifier": "487240",
              "url": "https://www.samsungfund.com/etf/product/view.do?id=2ETFN7",
              "feesAndCommissionsSpecification": "0.390% (지정참가회사 : 0.001%)"
            }
            </script>
          </head>
        </html>
        """
        self.responses[self.product_url] = json.dumps(
            {"pdf": {"gijunYMD": "20260506", "totalCnt": 13}},
            ensure_ascii=False,
        )
        self.responses[self.holdings_url] = json.dumps(
            {
                "pdf": {
                    "gijunYMD": "20260506",
                    "list": [
                        {
                            "rank": 1,
                            "itmNo": "010120",
                            "secNm": "LS ELECTRIC",
                            "applyQ": "4840",
                            "evalA": "1422960000",
                            "ratio": "24.6",
                        }
                    ],
                }
            },
            ensure_ascii=False,
        )

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html=self.responses[url],
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_kodex_fetch_detail_parses_json_ld_detail_page():
    fetcher = KodexDetailFetcher()
    provider = get_provider("kodex", fetcher=fetcher)

    detail = provider.fetch_detail("2ETFN7")

    assert [call[0] for call in fetcher.calls] == [fetcher.detail_url, fetcher.product_url, fetcher.holdings_url]
    assert detail.provider == ProviderName.KODEX
    assert detail.code == "487240"
    assert detail.name == "KODEX AI전력핵심설비"
    assert detail.category == "국내주식형 ETF"
    assert detail.benchmark == "iSelect AI전력핵심설비 지수(Price Return)"
    assert detail.expense_ratio == Decimal("0.390")
    assert detail.detail_url == "https://www.samsungfund.com/etf/product/view.do?id=2ETFN7"
    assert set(detail.raw) == {"inputCode", "jsonLd"}
    assert "description" not in detail.raw["jsonLd"]
    assert "유의사항" not in str(detail.raw)
    assert detail.holdings_url == fetcher.holdings_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].code == "010120"
    assert detail.holdings[0].name == "LS ELECTRIC"
    assert detail.holdings[0].quantity == Decimal("4840")
    assert detail.holdings[0].valuation_amount == Decimal("1422960000")
    assert detail.holdings[0].weight == Decimal("24.6")
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert set(detail.holdings[0].raw) == {"rank", "itmNo", "secNm", "applyQ", "evalA", "ratio"}


class KodexTickerResolveDetailFetcher(KodexDetailFetcher):
    list_url_page_1 = (
        "https://www.samsungfund.com/api/v1/kodex/product.do?srchTerm=w&ordrSort=DESC&ordrColm=YIELD_WEEK&pageNo=1"
    )

    def __init__(self) -> None:
        super().__init__()
        self.responses[self.list_url_page_1] = json.dumps(
            [
                {
                    "fNm": "KODEX AI전력핵심설비",
                    "stkTicker": "487240",
                    "fId": "2ETFN7",
                    "totalCnt": 1,
                }
            ],
            ensure_ascii=False,
        )


def test_kodex_fetch_detail_resolves_ticker_to_fund_id_before_fetching_detail():
    fetcher = KodexTickerResolveDetailFetcher()
    provider = get_provider("kodex", fetcher=fetcher)

    detail = provider.fetch_detail("487240")

    assert [call[0] for call in fetcher.calls] == [
        fetcher.list_url_page_1,
        fetcher.detail_url,
        fetcher.product_url,
        fetcher.holdings_url,
    ]
    assert detail.provider == ProviderName.KODEX
    assert detail.code == "487240"
    assert detail.name == "KODEX AI전력핵심설비"
    assert detail.holdings_url == fetcher.holdings_url
    assert detail.holdings[0].code == "010120"


class KodexRenderedHoldingsFallbackFetcher(KodexDetailFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.detail_fetch_count = 0
        self.rendered_detail_html = (
            self.responses[self.detail_url]
            + """
            <section id="pdf">
              <input value="2026.05.06"/>
              <table>
                <thead>
                  <tr><th>종목명</th><th>종목코드</th><th>비중(%)</th><th>수량</th><th>평가금액(원)</th></tr>
                </thead>
                <tbody>
                  <tr><td>원화예금</td><td>KRD010010001</td><td>-</td><td>5,457,620</td><td>5,457,620</td></tr>
                  <tr><td>LS ELECTRIC</td><td>010120</td><td>24.60</td><td>4,840</td><td>1,422,960,000</td></tr>
                </tbody>
              </table>
            </section>
            """
        )

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        if url == self.product_url:
            raise FetchError("HTTP product API failed")

        if url == self.detail_url:
            self.detail_fetch_count += 1
            html = self.responses[self.detail_url] if self.detail_fetch_count == 1 else self.rendered_detail_html
        else:
            html = self.responses[url]

        result = FetchResult(
            html=html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="playwright"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_kodex_fetch_detail_falls_back_to_rendered_pdf_table_when_api_fails():
    fetcher = KodexRenderedHoldingsFallbackFetcher()
    provider = get_provider("kodex", fetcher=fetcher)

    detail = provider.fetch_detail("2ETFN7")

    assert [call[0] for call in fetcher.calls] == [fetcher.detail_url, fetcher.detail_url]
    assert detail.holdings_url == f"{fetcher.detail_url}#pdf"
    assert len(detail.holdings) == 2
    assert detail.holdings[0].name == "원화예금"
    assert detail.holdings[0].code == "KRD010010001"
    assert detail.holdings[0].quantity == Decimal("5457620")
    assert detail.holdings[0].valuation_amount == Decimal("5457620")
    assert detail.holdings[0].weight is None
    assert detail.holdings[0].as_of_date == date(2026, 5, 6)
    assert detail.holdings[1].name == "LS ELECTRIC"
    assert detail.holdings[1].code == "010120"
    assert detail.holdings[1].weight == Decimal("24.60")
    assert detail.holdings[1].quantity == Decimal("4840")
    assert detail.holdings[1].valuation_amount == Decimal("1422960000")
    assert set(detail.holdings[1].raw) == {"itmNo", "secNm", "applyQ", "evalA", "ratio"}


class TigerDetailFetcher:
    search_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/list.ajax"
    detail_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7102110004"
    pdf_page_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/pdf.ajax"
    holdings_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/pdfListAjax.ajax"

    def __init__(self) -> None:
        self.calls = []
        self.search_html = """
        <div class="c-data-row" data-tot-cnt="1" data-ksd-fund="KR7102110004">
          <div class="title"><a>TIGER 200</a></div>
          <div class="code">(102110)</div>
        </div>
        """
        self.detail_html = """
        <html>
          <head><meta property="og:url"
            content="https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7102110004"/></head>
          <body>
            <div class="category"><span>주식</span><span>대표지수</span><span>개인연금</span></div>
            <div class="fund-title"><h1>TIGER 200 (102110)</h1></div>
            <div class="lead-main">
              <div class="each"><div class="title">기준가격(NAV)</div><div class="desc"><span class="amount">113,589.59</span></div></div>
              <div class="each net-worth"><div class="title">순자산 규모</div><div class="desc"><span class="amount">92,538</span></div></div>
            </div>
            <div class="lead-closer">
              <div class="each"><div class="title">상장일</div><div class="desc">2008-04-03</div></div>
              <div class="each"><div class="title">벤치마크</div><div class="desc">코스피 200</div></div>
            </div>
            <div class="c-card"><div class="c-card-header">총보수</div><div class="c-card-content"><p>연 0.05%</p></div></div>
            <div class="pop-header-info">기준일 2026.05.06 16:55:34</div>
            <div class="warning">투자 유의사항 및 기타비용 안내</div>
          </body>
        </html>
        """
        self.pdf_page_html = """
        <form id="formPdfList">
          <input type="text" name="fixDate" value="2026.05.04"/>
        </form>
        """
        self.holdings_html = """
        <tr data-tot-cnt="201">
          <td>005930</td>
          <td>삼성전자</td>
          <td>7,039</td>
          <td>1,636,567,500</td>
          <td>31.02</td>
          <td><div class="color-up">3.56</div></td>
        </tr>
        """

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        html = {
            self.search_url: self.search_html,
            self.detail_url: self.detail_html,
            self.pdf_page_url: self.pdf_page_html,
            self.holdings_url: self.holdings_html,
        }[url]
        result = FetchResult(
            html=html,
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        assert validator(result) is True
        return result


def test_tiger_fetch_detail_resolves_short_code_and_parses_detail_page():
    fetcher = TigerDetailFetcher()
    provider = get_provider("tiger", fetcher=fetcher)

    detail = provider.fetch_detail("102110")

    assert [call[0] for call in fetcher.calls] == [
        fetcher.search_url,
        fetcher.detail_url,
        fetcher.pdf_page_url,
        fetcher.holdings_url,
    ]
    assert fetcher.calls[0][2]["method"] == "POST"
    assert fetcher.calls[0][2]["data"]["q"] == "102110"
    assert fetcher.calls[2][2]["method"] == "POST"
    assert fetcher.calls[2][2]["data"] == {"ksdFund": "KR7102110004"}
    assert fetcher.calls[3][2]["method"] == "POST"
    assert fetcher.calls[3][2]["data"] == {
        "ksdFund": "KR7102110004",
        "fixDate": "",
        "prfPrd": "",
        "order": "",
        "pageIndex": "1",
        "firstIndex": "0",
        "listCnt": "999",
    }
    assert detail.provider == ProviderName.TIGER
    assert detail.code == "102110"
    assert detail.name == "TIGER 200"
    assert detail.category == "주식 / 대표지수"
    assert detail.benchmark == "코스피 200"
    assert detail.listing_date == date(2008, 4, 3)
    assert detail.nav == Decimal("113589.59")
    assert detail.aum == Decimal("92538")
    assert detail.expense_ratio == Decimal("0.05")
    assert detail.as_of_date == date(2026, 5, 6)
    assert detail.holdings_url == fetcher.holdings_url
    assert len(detail.holdings) == 1
    assert detail.holdings[0].code == "005930"
    assert detail.holdings[0].name == "삼성전자"
    assert detail.holdings[0].quantity == Decimal("7039")
    assert detail.holdings[0].valuation_amount == Decimal("1636567500")
    assert detail.holdings[0].weight == Decimal("31.02")
    assert detail.holdings[0].as_of_date == date(2026, 5, 4)
    assert "유의사항" not in str(detail.raw)
    assert set(detail.holdings[0].raw) == {"code", "name", "quantity", "valuationAmount", "weight", "return"}


class TigerEmptySearchFetcher:
    search_url = "https://investments.miraeasset.com/tigeretf/ko/product/search/list.ajax"

    def __init__(self) -> None:
        self.calls = []

    def fetch(self, url: str, *, provider: ProviderName | str, validator=None, **kwargs) -> FetchResult:
        result = FetchResult(
            html="<html></html>",
            metadata=FetchMetadata(provider=ProviderName(provider), url=url, strategy="http"),
        )
        self.calls.append((url, provider, kwargs))
        assert validator is not None
        if validator(result) is False:
            raise FetchError("Fallback fetch result was rejected")
        return result


def test_tiger_fetch_detail_raises_fetch_error_when_short_code_search_has_no_rows():
    fetcher = TigerEmptySearchFetcher()
    provider = get_provider("tiger", fetcher=fetcher)

    with pytest.raises(FetchError):
        provider.fetch_detail("102110")

    assert [call[0] for call in fetcher.calls] == [fetcher.search_url]
    assert fetcher.calls[0][2]["data"]["q"] == "102110"
