from types import SimpleNamespace

from cluefin_cli.domains.providers.dart import DartProvider
from cluefin_cli.domains.providers.kis import KisProvider


class FakeFactory:
    def __init__(self, client) -> None:
        self.client = client

    def create(self, broker: str):
        return self.client


def test_kis_provider_normalizes_news_headlines() -> None:
    item = SimpleNamespace(
        hts_pbnt_titl_cntt="시장 뉴스",
        data_dt="20260519",
        data_tm="090000",
        iscd1="005930",
        iscd2="",
        iscd3="",
        iscd4="",
        iscd5="",
        dorg="KIS",
        cntt_usiq_srno="1",
    )
    client = SimpleNamespace(
        domestic_issue_other=SimpleNamespace(
            get_market_announcement_schedule=lambda *args: SimpleNamespace(body=SimpleNamespace(output=[item]))
        )
    )

    headlines = KisProvider(FakeFactory(client)).fetch_news(stock_code="005930", days=7, query="시장")

    assert headlines[0].source == "kis"
    assert headlines[0].title == "시장 뉴스"
    assert headlines[0].published_at == "20260519090000"
    assert headlines[0].stock_codes == ["005930"]


def test_dart_provider_normalizes_disclosure_headlines() -> None:
    corp_item = SimpleNamespace(stock_code="005930", corp_code="00126380")
    disclosure_item = SimpleNamespace(
        report_nm="사업보고서",
        rcept_no="20260519000123",
        rcept_dt="20260519",
        corp_code="00126380",
        corp_name="삼성전자",
        stock_code="005930",
    )
    public_disclosure = SimpleNamespace(
        corp_code=lambda: SimpleNamespace(list=[corp_item]),
        public_disclosure_search=lambda **kwargs: SimpleNamespace(result=SimpleNamespace(list=[disclosure_item])),
    )
    client = SimpleNamespace(public_disclosure=public_disclosure)

    disclosures = DartProvider(FakeFactory(client)).fetch_disclosures(stock_code="005930", days=7, query="사업")

    assert disclosures[0].source == "dart"
    assert disclosures[0].report_name == "사업보고서"
    assert disclosures[0].rcept_no == "20260519000123"
