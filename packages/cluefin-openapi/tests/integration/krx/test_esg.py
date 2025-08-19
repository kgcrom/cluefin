import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._esg_types import EsgSociallyResponsibleInvestmentBond


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


def test_get_socially_responsible_investment_bond(client: Client):
    time.sleep(1)
    response = client.esg.get_socially_responsible_investment_bond("20250721")

    assert response is not None
    assert response.body is not None

    assert isinstance(response.body, EsgSociallyResponsibleInvestmentBond)
