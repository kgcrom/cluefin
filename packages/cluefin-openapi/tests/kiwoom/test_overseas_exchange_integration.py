import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_exchange_types import (
    OverseasExchangeEstimatedAmount,
    OverseasExchangeRate,
    OverseasExchangeRequest,
)


@pytest.mark.integration
def test_get_estimated_exchange_amount(client: Client):
    response = client.overseas_exchange.get_estimated_exchange_amount(exch_tp="1", fc_exmn_amt="10")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeEstimatedAmount)


@pytest.mark.integration
def test_get_exchange_rate(client: Client):
    response = client.overseas_exchange.get_exchange_rate(exch_tp="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeRate)


@pytest.mark.integration
def test_request_exchange(client: Client):
    # NOTE: ust31302 actually executes a currency exchange, so this test relies on
    # the mock-trading (dev) environment configured via the ``client`` fixture
    # (KIWOOM_ENV=dev) and uses a small amount to minimize impact.
    response = client.overseas_exchange.request_exchange(exch_tp="1", fc_exmn_amt="10")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeRequest)
