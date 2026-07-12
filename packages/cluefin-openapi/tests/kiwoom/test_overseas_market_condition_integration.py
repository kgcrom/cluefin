import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_market_condition_types import (
    OverseasMarketConditionCurrentPriceStockInfo,
    OverseasMarketConditionCurrentPriceTenQuotes,
    OverseasMarketConditionDailyExecutionHistory,
    OverseasMarketConditionDailyStockPrice,
    OverseasMarketConditionDetailedExecutionHistory,
)


@pytest.mark.integration
def test_get_current_price_stock_info(client: Client):
    response = client.overseas_market_condition.get_current_price_stock_info(stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasMarketConditionCurrentPriceStockInfo)


@pytest.mark.integration
def test_get_current_price_ten_quotes(client: Client):
    response = client.overseas_market_condition.get_current_price_ten_quotes(stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasMarketConditionCurrentPriceTenQuotes)


@pytest.mark.integration
def test_get_detailed_execution_history(client: Client):
    response = client.overseas_market_condition.get_detailed_execution_history(stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasMarketConditionDetailedExecutionHistory)


@pytest.mark.integration
def test_get_daily_execution_history(client: Client):
    response = client.overseas_market_condition.get_daily_execution_history(
        stex_tp="ND", stk_cd="AAPL", base_dt="20240102"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasMarketConditionDailyExecutionHistory)


@pytest.mark.integration
def test_get_daily_stock_price(client: Client):
    response = client.overseas_market_condition.get_daily_stock_price(stex_tp="ND", stk_cd="AAPL", base_dt="20240102")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasMarketConditionDailyStockPrice)
