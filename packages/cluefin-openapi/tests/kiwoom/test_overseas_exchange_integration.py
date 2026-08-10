import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_exchange_types import (
    OverseasExchangeEstimatedAmount,
    OverseasExchangeRate,
    OverseasExchangeRequest,
)

from ._integration_helpers import real_account_only


@pytest.mark.integration
@real_account_only("ust31300", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_estimated_exchange_amount(client: Client):
    response = client.overseas_exchange.get_estimated_exchange_amount(exch_tp="1", fc_exmn_amt="10")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeEstimatedAmount)


@pytest.mark.integration
@real_account_only("ust31301", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_exchange_rate(client: Client):
    response = client.overseas_exchange.get_exchange_rate(exch_tp="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeRate)


@pytest.mark.integration
@real_account_only("ust31302 환전신청", "rc=7, '1999:...실패사유=모의투자에서는 해당업무가 제공되지 않습니다.'")
def test_request_exchange(client: Client):
    # NOTE: ust31302 actually executes a currency exchange, so this test uses a
    # small amount to minimize impact.
    response = client.overseas_exchange.request_exchange(exch_tp="1", fc_exmn_amt="10")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasExchangeRequest)
