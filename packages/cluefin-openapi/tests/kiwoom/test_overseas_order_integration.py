import pytest

from cluefin_openapi.kiwoom._client import Client


@pytest.mark.integration
def test_request_buy_order(client: Client):
    response = client.overseas_order.request_buy_order(
        stex_tp="ND", stk_cd="AAPL", ord_qty="1", trde_tp="00", ord_uv="1.00"
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_sell_order(client: Client):
    response = client.overseas_order.request_sell_order(
        stk_cd="AAPL", stex_tp="ND", ord_qty="1", trde_tp="00", ord_uv="100000.00"
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_modify_order(client: Client):
    response = client.overseas_order.request_modify_order(
        orig_ord_no="0000000", stex_tp="ND", stk_cd="AAPL", mdfy_uv="1.00"
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_cancel_order(client: Client):
    response = client.overseas_order.request_cancel_order(orig_ord_no="0000000", stex_tp="ND", stk_cd="AAPL")
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_get_orderable_quantity(client: Client):
    response = client.overseas_order.get_orderable_quantity(stk_cd="AAPL", uv="1.00", stex_tp="ND")
    assert response is not None
    assert response.body is not None
