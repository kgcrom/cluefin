import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_market_condition_types import (
    DomesticMarketConditionAfterHoursSinglePrice,
    DomesticMarketConditionAfterMarketTradingByInvestor,
    DomesticMarketConditionDailyInstitutionalTrading,
    DomesticMarketConditionDailyStockPrice,
    DomesticMarketConditionExecutionIntensityTrendByDate,
    DomesticMarketConditionExecutionIntensityTrendByTime,
    DomesticMarketConditionInstitutionalTradingTrendByStock,
    DomesticMarketConditionIntradayTradingByInvestor,
    DomesticMarketConditionMarketSentimentInfo,
    DomesticMarketConditionNewStockWarrantPrice,
    DomesticMarketConditionProgramTradingArbitrageBalanceTrend,
    DomesticMarketConditionProgramTradingCumulativeTrend,
    DomesticMarketConditionProgramTradingTrendByDate,
    DomesticMarketConditionProgramTradingTrendByStockAndDate,
    DomesticMarketConditionProgramTradingTrendByStockAndTime,
    DomesticMarketConditionProgramTradingTrendByTime,
    DomesticMarketConditionSecuritiesFirmTradingTrendByStock,
    DomesticMarketConditionStockPrice,
    DomesticMarketConditionStockQuote,
    DomesticMarketConditionStockQuoteByDate,
)


@pytest.mark.integration
def test_get_stock_quote(client: Client):
    response = client.market_conditions.get_stock_quote("005930")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionStockQuote)


@pytest.mark.integration
def test_get_stock_quote_by_date(client: Client):
    response = client.market_conditions.get_stock_quote_by_date("005930")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionStockQuoteByDate)


@pytest.mark.integration
def test_get_stock_price(client: Client):
    response = client.market_conditions.get_stock_price("005930")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionStockPrice)


@pytest.mark.integration
def test_get_market_sentiment_info(client: Client):
    response = client.market_conditions.get_market_sentiment_info("005930")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionMarketSentimentInfo)


@pytest.mark.integration
def test_get_new_stock_warrant_price(client: Client):
    response = client.market_conditions.get_new_stock_warrant_price("00")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionNewStockWarrantPrice)


@pytest.mark.integration
def test_get_daily_institutional_trading_items(client: Client):
    response = client.market_conditions.get_daily_institutional_trading_items("20241106", "20241107", "1", "001", "3")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionDailyInstitutionalTrading)


@pytest.mark.integration
def test_get_institutional_trading_trend_by_stock(client: Client):
    response = client.market_conditions.get_institutional_trading_trend_by_stock(
        "005930", "20241101", "20241107", "1", "1"
    )

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionInstitutionalTradingTrendByStock)


@pytest.mark.integration
def test_get_execution_intensity_trend_by_time(client: Client):
    response = client.market_conditions.get_execution_intensity_trend_by_time("005930", "20241107", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionExecutionIntensityTrendByTime)


@pytest.mark.integration
def test_get_execution_intensity_trend_by_date(client: Client):
    response = client.market_conditions.get_execution_intensity_trend_by_date("005930", "20241107")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionExecutionIntensityTrendByDate)


@pytest.mark.integration
def test_get_intraday_trading_by_investor(client: Client):
    response = client.market_conditions.get_intraday_trading_by_investor("000", "1", "6", "1", "1", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionIntradayTradingByInvestor)


@pytest.mark.integration
def test_get_after_market_trading_by_investor(client: Client):
    response = client.market_conditions.get_after_market_trading_by_investor("000", "1", "0", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionAfterMarketTradingByInvestor)


@pytest.mark.integration
def test_get_securities_firm_trading_trend_by_stock(client: Client):
    response = client.market_conditions.get_securities_firm_trading_trend_by_stock(
        "001", "005930", "20241101", "20241107"
    )

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionSecuritiesFirmTradingTrendByStock)


@pytest.mark.integration
def test_get_daily_stock_price(client: Client):
    response = client.market_conditions.get_daily_stock_price("005930", "20241125", "0")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DomesticMarketConditionDailyStockPrice)


@pytest.mark.integration
def test_get_after_hours_single_price(client: Client):
    response = client.market_conditions.get_after_hours_single_price("039490")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionAfterHoursSinglePrice)


@pytest.mark.integration
def test_get_program_trading_trend_by_time(client: Client):
    response = client.market_conditions.get_program_trading_trend_by_time("20250101", "1", "P00101", "0", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByTime)


@pytest.mark.integration
def test_get_program_trading_arbitrage_balance_trend(client: Client):
    response = client.market_conditions.get_program_trading_arbitrage_balance_trend("20250101", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingArbitrageBalanceTrend)


@pytest.mark.integration
def test_get_program_trading_cumulative_trend(client: Client):
    response = client.market_conditions.get_program_trading_cumulative_trend("20250101", "1", "0", "1")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingCumulativeTrend)


@pytest.mark.integration
def test_get_program_trading_trend_by_stock_and_time(client: Client):
    response = client.market_conditions.get_program_trading_trend_by_stock_and_time("1", "039490", "20250101")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByStockAndTime)


@pytest.mark.integration
def test_get_program_trading_trend_by_date(client: Client):
    response = client.market_conditions.get_program_trading_trend_by_date("20250101", "1", "P00101", "0", "1")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByDate)


@pytest.mark.integration
def test_get_program_trading_trend_by_stock_and_date(client: Client):
    response = client.market_conditions.get_program_trading_trend_by_stock_and_date("1", "039490", "20250101")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticMarketConditionProgramTradingTrendByStockAndDate)
