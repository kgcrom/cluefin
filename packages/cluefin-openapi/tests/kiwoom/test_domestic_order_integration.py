import pytest

from cluefin_openapi.kiwoom._client import Client


@pytest.mark.integration
def test_request_buy_order(client: Client):
    response = client.order.request_buy_order(
        dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
    )
    assert response is not None
    assert response.body is not None
    assert response.body.ord_no is not None


@pytest.mark.integration
def test_request_sell_order(client: Client):
    response = client.order.request_sell_order(
        dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_modify_order(client: Client):
    response = client.order.request_modify_order(
        dmst_stex_tp="KRX", orig_ord_no="0000139", stk_cd="005930", mdfy_qty="1", mdfy_uv="199700", mdfy_cond_uv=""
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_cancel_order(client: Client):
    response = client.order.request_cancel_order(
        dmst_stex_tp="KRX", orig_ord_no="0000140", stk_cd="005930", cncl_qty="1"
    )
    assert response is not None
    assert response.body is not None
