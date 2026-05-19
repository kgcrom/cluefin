from cluefin_cli.domains.models import DisclosureHeadline, NewsHeadline, StatementSnapshot
from cluefin_cli.domains.news import NewsService
from cluefin_cli.domains.statements import StatementsService


class FakeDartProvider:
    def __init__(self) -> None:
        self.statement_calls = []

    def fetch_statement_snapshot(self, **kwargs):
        self.statement_calls.append(kwargs)
        return StatementSnapshot(stock_code=kwargs["stock_code"], source="dart")

    def fetch_disclosures(self, **kwargs):
        return [DisclosureHeadline(source="dart", report_name=kwargs["query"] or "공시")]


class FakeKisProvider:
    def __init__(self) -> None:
        self.statement_calls = []

    def fetch_statement_snapshot(self, **kwargs):
        self.statement_calls.append(kwargs)
        return StatementSnapshot(stock_code=kwargs["stock_code"], source="kis")

    def fetch_news(self, **kwargs):
        return [NewsHeadline(source="kis", title=kwargs["query"] or "뉴스")]


def test_statements_service_fetches_dart_and_kis_for_all_source() -> None:
    dart = FakeDartProvider()
    kis = FakeKisProvider()
    service = StatementsService(dart_provider=dart, kis_provider=kis)

    snapshots = service.fetch(stock_code="005930", source="all", year="2024", report="q1", include_xbrl=True)

    assert [snapshot.source for snapshot in snapshots] == ["dart", "kis"]
    assert dart.statement_calls[0]["report_code"] == "11013"
    assert dart.statement_calls[0]["include_xbrl"] is True
    assert kis.statement_calls[0]["div_cls_code"] == "1"


def test_news_service_combines_sources_for_all_source() -> None:
    service = NewsService(dart_provider=FakeDartProvider(), kis_provider=FakeKisProvider())

    data = service.fetch(stock_code="005930", source="all", days=3, query="배당")

    assert data["news"][0].title == "배당"
    assert data["disclosures"][0].report_name == "배당"
