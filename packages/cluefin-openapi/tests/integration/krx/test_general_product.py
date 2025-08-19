import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._general_product_types import (
    GeneralProductEmissionsMarket,
    GeneralProductGoldMarket,
    GeneralProductOilMarket,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


def test_get_oil_market(client: Client):
    time.sleep(1)
    response = client.general_product.get_oil_market("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, GeneralProductOilMarket)


def test_get_gold_market(client: Client):
    time.sleep(1)
    response = client.general_product.get_gold_market("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, GeneralProductGoldMarket)


def test_get_emissions_market(client: Client):
    time.sleep(1)
    response = client.general_product.get_emissions_market("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, GeneralProductEmissionsMarket)
