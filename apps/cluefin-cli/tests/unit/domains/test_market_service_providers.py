from types import SimpleNamespace

from cluefin_cli.domains.market import MarketService
from cluefin_cli.domains.models import MarketRankItem
from cluefin_cli.domains.providers.kis import KisProvider
from cluefin_cli.domains.providers.kiwoom import KiwoomProvider


class Response:
    def __init__(self, body: object):
        self.body = body


class FakeMarketProvider:
    def __init__(self, source: str):
        self.source = source

    def fetch_market_volume(self, *, limit: int) -> list[MarketRankItem]:
        return [MarketRankItem(source=self.source, category="volume", rank=1, stock_code="005930", value=limit)]

    def fetch_market_ranking(self, *, limit: int) -> list[MarketRankItem]:
        return [MarketRankItem(source=self.source, category="ranking", rank=1, stock_code="005930", value=limit)]

    def fetch_market_theme(self, *, limit: int) -> list[MarketRankItem]:
        return [MarketRankItem(source=self.source, category="theme", rank=1, stock_name="반도체", value=limit)]

    def fetch_market_sector(self, *, limit: int) -> list[MarketRankItem]:
        return [MarketRankItem(source=self.source, category="sector", rank=1, stock_name="전기전자", value=limit)]


def test_market_service_uses_default_sources() -> None:
    service = MarketService(kiwoom_provider=FakeMarketProvider("kiwoom"), kis_provider=FakeMarketProvider("kis"))

    assert service.fetch(category="volume")[0].source == "kis"
    assert service.fetch(category="ranking")[0].source == "kis"
    assert service.fetch(category="sector")[0].source == "kis"
    assert service.fetch(category="theme")[0].source == "kiwoom"


def test_market_service_all_combines_available_providers() -> None:
    service = MarketService(kiwoom_provider=FakeMarketProvider("kiwoom"), kis_provider=FakeMarketProvider("kis"))

    items = service.fetch(category="volume", source="all", limit=3)

    assert [item.source for item in items] == ["kis", "kiwoom"]


def test_kis_provider_normalizes_market_volume() -> None:
    provider = KisProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        domestic_ranking_analysis=SimpleNamespace(
            get_trading_volume_rank=lambda *_: Response(
                SimpleNamespace(
                    output=[
                        SimpleNamespace(
                            data_rank="1",
                            mksc_shrn_iscd="005930",
                            hts_kor_isnm="삼성전자",
                            acml_vol="1000",
                            prdy_ctrt="1.2",
                        )
                    ]
                )
            )
        )
    )

    items = provider.fetch_market_volume(limit=1)

    assert items[0].source == "kis"
    assert items[0].rank == 1
    assert items[0].stock_code == "005930"
    assert items[0].value == "1000"


def test_kiwoom_provider_normalizes_market_theme() -> None:
    provider = KiwoomProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        theme=SimpleNamespace(
            get_theme_group=lambda *_: Response(
                SimpleNamespace(
                    thema_grp=[
                        SimpleNamespace(
                            thema_grp_cd="100",
                            thema_nm="반도체",
                            dt_prft_rt="3.1",
                            flu_rt="1.5",
                        )
                    ]
                )
            )
        )
    )

    items = provider.fetch_market_theme(limit=1)

    assert items[0].source == "kiwoom"
    assert items[0].stock_code == "100"
    assert items[0].stock_name == "반도체"
    assert items[0].change_rate == "1.5"
