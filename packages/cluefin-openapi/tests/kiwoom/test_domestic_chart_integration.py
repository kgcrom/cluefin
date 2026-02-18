import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_chart_types import (
    DomesticChartIndividualStockInstitutional,
    DomesticChartIndustryDaily,
    DomesticChartIndustryMinute,
    DomesticChartIndustryMonthly,
    DomesticChartIndustryTick,
    DomesticChartIndustryWeekly,
    DomesticChartIndustryYearly,
    DomesticChartIntradayInvestorTrading,
    DomesticChartStockDaily,
    DomesticChartStockMinute,
    DomesticChartStockMonthly,
    DomesticChartStockTick,
    DomesticChartStockWeekly,
    DomesticChartStockYearly,
)


@pytest.mark.integration
def test_get_foreign_investor_trading_trend_by_stock(client: Client):
    response = client.chart.get_individual_stock_institutional_chart("20250630", "005930", "1", "0", "1000")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndividualStockInstitutional)


@pytest.mark.integration
def test_get_intraday_investor_trading(client: Client):
    response = client.chart.get_individual_stock_institutional_chart("20250630", "005930", "1", "0", "1000")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndividualStockInstitutional)


@pytest.mark.integration
def test_intraday_investor_trading(client: Client):
    response = client.chart.get_intraday_investor_trading("000", "1", "0", "005930")

    assert response is not None
    assert isinstance(response.body, DomesticChartIntradayInvestorTrading)


@pytest.mark.integration
def test_get_stock_tick(client: Client):
    response = client.chart.get_stock_tick("005930", "1", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockTick)


@pytest.mark.integration
def test_get_stock_minute(client: Client):
    response = client.chart.get_stock_minute("005930", "1", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockMinute)


@pytest.mark.integration
def test_get_stock_daily(client: Client):
    response = client.chart.get_stock_daily("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockDaily)


@pytest.mark.integration
def test_get_stock_weekly(client: Client):
    response = client.chart.get_stock_weekly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockWeekly)


@pytest.mark.integration
def test_get_stock_monthly(client: Client):
    response = client.chart.get_stock_monthly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockMonthly)


@pytest.mark.integration
def test_get_stock_yearly(client: Client):
    response = client.chart.get_stock_yearly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockYearly)


@pytest.mark.integration
def test_get_industry_tick(client: Client):
    response = client.chart.get_industry_tick("001", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryTick)


@pytest.mark.integration
def test_get_industry_minute(client: Client):
    response = client.chart.get_industry_minute("001", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryMinute)


@pytest.mark.integration
def test_get_industry_daily(client: Client):
    response = client.chart.get_industry_daily("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryDaily)


@pytest.mark.integration
def test_get_industry_weekly(client: Client):
    response = client.chart.get_industry_weekly("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryWeekly)


@pytest.mark.integration
def test_get_industry_monthly(client: Client):
    response = client.chart.get_industry_monthly("002", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryMonthly)


@pytest.mark.integration
def test_get_industry_yearly(client: Client):
    response = client.chart.get_industry_yearly("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryYearly)
