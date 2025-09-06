import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._derivatives_types import (
    DerivativesTradingOfFuturesExcludeStock,
    DerivativesTradingOfKosdaqFutures,
    DerivativesTradingOfKosdaqOption,
    DerivativesTradingOfKospiFutures,
    DerivativesTradingOfKospiOption,
    DerivativesTradingOfOptionExcludeStock,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


@pytest.mark.integration
def test_get_trading_of_futures_exclude_stock(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_futures_exclude_stock("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfFuturesExcludeStock)


@pytest.mark.integration
def test_get_trading_of_kospi_futures(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_kospi_futures("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfKospiFutures)


@pytest.mark.integration
def test_get_trading_of_kosdaq_futures(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_kosdaq_futures("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfKosdaqFutures)


@pytest.mark.integration
def test_get_trading_of_option_exclude_stock(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_option_exclude_stock("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfOptionExcludeStock)


@pytest.mark.integration
def test_get_trading_of_kospi_option(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_kospi_option("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfKospiOption)


@pytest.mark.integration
def test_get_trading_of_kosdaq_option(client: Client):
    time.sleep(1)
    response = client.derivatives.get_trading_of_kosdaq_option("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, DerivativesTradingOfKosdaqOption)
