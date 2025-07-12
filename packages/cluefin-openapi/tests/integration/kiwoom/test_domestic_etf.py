import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_etf_types import (
    DomesticEtfDailyExecution,
    DomesticEtfDailyTrend,
    DomesticEtfFullPrice,
    DomesticEtfHourlyExecution,
    DomesticEtfHourlyExecutionV2,
    DomesticEtfHourlyTrend,
    DomesticEtfHourlyTrendV2,
    DomesticEtfItemInfo,
    DomesticEtfReturnRate,
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
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_etf_return_rate(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_return_rate("069500", "001", "0")
    assert response is not None
    assert isinstance(response.body, DomesticEtfReturnRate)


def test_get_etf_item_info(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_item_info("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfItemInfo)


def test_get_etf_daily_trend(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_daily_trend("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfDailyTrend)


def test_get_etf_full_price(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_full_price("0", "0", "0000", "0", "0", "1")
    assert response is not None
    assert isinstance(response.body, DomesticEtfFullPrice)


def test_get_etf_hourly_trend(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_hourly_trend("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfHourlyTrend)


def test_get_etf_hourly_execution(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_hourly_execution("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfHourlyExecution)


def test_get_etf_daily_execution(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_daily_execution("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfDailyExecution)


def test_get_etf_hourly_execution_v2(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_hourly_execution_v2("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfHourlyExecutionV2)


def test_get_etf_hourly_trend_v2(client: Client):
    time.sleep(1)

    response = client.etf.get_etf_hourly_trend_v2("069500")
    assert response is not None
    assert isinstance(response.body, DomesticEtfHourlyTrendV2)
