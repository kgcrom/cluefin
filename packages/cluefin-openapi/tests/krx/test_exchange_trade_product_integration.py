import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._exchange_traded_product_types import (
    ExchangeTradedELW,
    ExchangeTradedETF,
    ExchangeTradedETN,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


@pytest.mark.integration
def test_get_etf(client: Client):
    time.sleep(1)
    response = client.exchange_traded_product.get_etf("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, ExchangeTradedETF)


@pytest.mark.integration
def test_get_etn(client: Client):
    time.sleep(1)
    response = client.exchange_traded_product.get_etn("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, ExchangeTradedETN)


@pytest.mark.integration
def test_get_elw(client: Client):
    time.sleep(1)
    response = client.exchange_traded_product.get_elw("20250721")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, ExchangeTradedELW)
