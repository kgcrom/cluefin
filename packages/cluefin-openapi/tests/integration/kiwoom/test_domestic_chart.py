import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
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


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    """Create a Client instance for testing.

    Args:
        auth (Auth): The authenticated Auth instance.

    Returns:
        Client: A configured Client instance.
    """
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_foreign_investor_trading_trend_by_stock(client: Client):
    time.sleep(1)

    response = client.chart.get_individual_stock_institutional_chart("20250630", "005930", "1", "0", "1000")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndividualStockInstitutional)


def test_get_intraday_investor_trading(client: Client):
    time.sleep(1)

    response = client.chart.get_individual_stock_institutional_chart("20250630", "005930", "1", "0", "1000")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndividualStockInstitutional)


def test_intraday_investor_trading(client: Client):
    time.sleep(1)

    response = client.chart.get_intraday_investor_trading("0000", "1", "0", "005930")

    assert response is not None
    assert isinstance(response.body, DomesticChartIntradayInvestorTrading)


def test_get_stock_tick(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_tick("005930", "1", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockTick)


def test_get_stock_minute(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_minute("005930", "1", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockMinute)


def test_get_stock_daily(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_daily("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockDaily)


def test_get_stock_weekly(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_weekly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockWeekly)


def test_get_stock_monthly(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_monthly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockMonthly)


def test_get_stock_yearly(client: Client):
    time.sleep(1)

    response = client.chart.get_stock_yearly("005930", "20250630", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartStockYearly)


def test_get_industry_tick(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_tick("001", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryTick)


def test_get_industry_minute(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_minute("001", "1")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryMinute)


def test_get_industry_daily(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_daily("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryDaily)


def test_get_industry_weekly(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_weekly("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryWeekly)


def test_get_industry_monthly(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_monthly("002", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryMonthly)


def test_get_industry_yearly(client: Client):
    time.sleep(1)

    response = client.chart.get_industry_yearly("001", "20250630")

    assert response is not None
    assert isinstance(response.body, DomesticChartIndustryYearly)
