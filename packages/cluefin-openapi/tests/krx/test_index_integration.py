import os
import time

import dotenv
import pytest

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._index_types import (
    IndexBond,
    IndexDerivatives,
    IndexKosdaq,
    IndexKospi,
    IndexKrx,
)


@pytest.fixture
def client() -> Client:
    time.sleep(1)
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Client(auth_key=os.getenv("KRX_AUTH_KEY", ""))


@pytest.mark.integration
def test_get_krx(client: Client):
    time.sleep(1)
    response = client.index.get_krx("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, IndexKrx)


@pytest.mark.integration
def test_get_kospi(client: Client):
    time.sleep(1)
    response = client.index.get_kospi("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, IndexKospi)


@pytest.mark.integration
def test_get_kosdaq(client: Client):
    time.sleep(1)
    response = client.index.get_kosdaq("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, IndexKosdaq)


@pytest.mark.integration
def test_get_bond(client: Client):
    time.sleep(1)
    response = client.index.get_bond("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, IndexBond)


@pytest.mark.integration
def test_get_derivatives(client: Client):
    time.sleep(1)
    response = client.index.get_derivatives("20250721")
    assert response is not None
    assert response.body is not None
    assert isinstance(response.body, IndexDerivatives)
