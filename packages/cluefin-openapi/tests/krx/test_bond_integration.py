import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._bond_types import (
    BondGeneralBondMarket,
    BondKoreaTreasuryBondMarket,
    BondSmallBondMarket,
)
from cluefin_openapi.krx._client import Client


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY") or "")


@pytest.mark.integration
def test_get_korea_treasury_bond_market(client: Client):
    time.sleep(1)
    response = client.bond.get_korea_treasury_bond_market("20250721")

    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, BondKoreaTreasuryBondMarket)


@pytest.mark.integration
def test_get_general_bond_market(client: Client):
    time.sleep(1)
    response = client.bond.get_general_bond_market("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, BondGeneralBondMarket)


@pytest.mark.integration
def test_get_small_bond_market(client: Client):
    time.sleep(1)
    response = client.bond.get_small_bond_market("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, BondSmallBondMarket)
