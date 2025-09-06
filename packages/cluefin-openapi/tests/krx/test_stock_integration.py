import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._stock_types import (
    StockKonex,
    StockKonexBaseInfo,
    StockKosdaq,
    StockKosdaqBaseInfo,
    StockKospi,
    StockKospiBaseInfo,
    StockSubscriptionWarrant,
    StockWarrant,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


@pytest.mark.integration
def test_get_kospi(client: Client):
    time.sleep(1)
    response = client.stock.get_kospi("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKospi)


@pytest.mark.integration
def test_get_kosdaq(client: Client):
    time.sleep(1)
    response = client.stock.get_kosdaq("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKosdaq)


@pytest.mark.integration
def test_get_konex(client: Client):
    time.sleep(1)
    response = client.stock.get_konex("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKonex)


@pytest.mark.integration
def test_get_warrant(client: Client):
    time.sleep(1)
    response = client.stock.get_warrant("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockWarrant)


@pytest.mark.integration
def test_get_subscription_warrant(client: Client):
    time.sleep(1)
    response = client.stock.get_subscription_warrant("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockSubscriptionWarrant)


@pytest.mark.integration
def test_get_kospi_base_info(client: Client):
    time.sleep(1)
    response = client.stock.get_kospi_base_info("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKospiBaseInfo)


@pytest.mark.integration
def test_get_kosdaq_base_info(client: Client):
    time.sleep(1)
    response = client.stock.get_kosdaq_base_info("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKosdaqBaseInfo)


@pytest.mark.integration
def test_get_konex_base_info(client: Client):
    time.sleep(1)
    response = client.stock.get_konex_base_info("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, StockKonexBaseInfo)
