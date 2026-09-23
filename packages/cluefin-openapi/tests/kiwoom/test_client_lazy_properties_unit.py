"""``Client`` 의 도메인 lazy property (account/chart/.../overseas_*) 테스트."""

import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_account import DomesticAccount
from cluefin_openapi.kiwoom._domestic_chart import DomesticChart
from cluefin_openapi.kiwoom._domestic_etf import DomesticETF
from cluefin_openapi.kiwoom._domestic_foreign import DomesticForeign
from cluefin_openapi.kiwoom._domestic_market_condition import DomesticMarketCondition
from cluefin_openapi.kiwoom._domestic_order import DomesticOrder
from cluefin_openapi.kiwoom._domestic_rank_info import DomesticRankInfo
from cluefin_openapi.kiwoom._domestic_sector import DomesticSector
from cluefin_openapi.kiwoom._domestic_stock_info import DomesticStockInfo
from cluefin_openapi.kiwoom._domestic_theme import DomesticTheme
from cluefin_openapi.kiwoom._overseas_account import OverseasAccount
from cluefin_openapi.kiwoom._overseas_chart import OverseasChart
from cluefin_openapi.kiwoom._overseas_exchange import OverseasExchange
from cluefin_openapi.kiwoom._overseas_investment_info import OverseasInvestmentInfo
from cluefin_openapi.kiwoom._overseas_market_condition import OverseasMarketCondition
from cluefin_openapi.kiwoom._overseas_order import OverseasOrder
from cluefin_openapi.kiwoom._overseas_rank_info import OverseasRankInfo
from cluefin_openapi.kiwoom._overseas_sector import OverseasSector
from cluefin_openapi.kiwoom._overseas_stock_info import OverseasStockInfo
from cluefin_openapi.kiwoom._overseas_watchlist import OverseasWatchlist

PROPERTY_CASES = [
    ("account", DomesticAccount),
    ("chart", DomesticChart),
    ("etf", DomesticETF),
    ("foreign", DomesticForeign),
    ("market_conditions", DomesticMarketCondition),
    ("order", DomesticOrder),
    ("rank_info", DomesticRankInfo),
    ("sector", DomesticSector),
    ("stock_info", DomesticStockInfo),
    ("theme", DomesticTheme),
    ("overseas_account", OverseasAccount),
    ("overseas_chart", OverseasChart),
    ("overseas_exchange", OverseasExchange),
    ("overseas_investment_info", OverseasInvestmentInfo),
    ("overseas_market_condition", OverseasMarketCondition),
    ("overseas_order", OverseasOrder),
    ("overseas_rank_info", OverseasRankInfo),
    ("overseas_sector", OverseasSector),
    ("overseas_stock_info", OverseasStockInfo),
    ("overseas_watchlist", OverseasWatchlist),
]


@pytest.fixture
def client() -> Client:
    return Client(token="test_token", env="dev")


@pytest.mark.parametrize("property_name,expected_cls", PROPERTY_CASES, ids=[c[0] for c in PROPERTY_CASES])
def test_property_returns_expected_domain_class(client, property_name, expected_cls):
    instance = getattr(client, property_name)
    assert isinstance(instance, expected_cls)
    assert instance.client is client


@pytest.mark.xfail(
    strict=True,
    reason=(
        "버그: Client의 도메인 property들(account/chart/... )은 매 접근마다 "
        "`return DomesticXxx(self)`로 새 인스턴스를 만들 뿐 캐싱하지 않는다. "
        "docstring/네이밍은 'lazy property'지만 실제로는 매번 재생성된다."
    ),
)
@pytest.mark.parametrize("property_name,expected_cls", PROPERTY_CASES, ids=[c[0] for c in PROPERTY_CASES])
def test_property_returns_same_instance_on_repeated_access(client, property_name, expected_cls):
    first = getattr(client, property_name)
    second = getattr(client, property_name)
    assert first is second
