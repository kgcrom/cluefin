import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_order_types import (
    DomesticOrderBuy,
    DomesticOrderCancel,
    DomesticOrderModify,
    DomesticOrderSell,
)


@pytest.fixture
def client() -> Client:
    return Client(token="test_token", env="dev")


def test_request_buy_order(client: Client):
    expected_data = {"ord_no": "00024", "return_code": 0, "return_msg": "정상적으로 처리되었습니다"}
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/ordr",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt10000"},
        )

        response = client.order.request_buy_order(
            dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
        )
        assert response is not None
        assert isinstance(response.body, DomesticOrderBuy)
        assert response.body.ord_no == "00024"


def test_request_sell_order(client: Client):
    expected_data = {
        "ord_no": "0000138",
        "dmst_stex_tp": "KRX",
        "return_code": 0,
        "return_msg": "매도주문이 완료되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/ordr",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt10001"},
        )

        response = client.order.request_sell_order(
            dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", trde_tp="3",
        )
        assert response is not None
        assert isinstance(response.body, DomesticOrderSell)
        assert response.body.dmst_stex_tp == "KRX"


def test_request_modify_order(client: Client):
    expected_data = {
        "ord_no": "0000140",
        "base_orig_ord_no": "0000139",
        "mdfy_qty": "000000000001",
        "dmst_stex_tp": "KRX",
        "return_code": 0,
        "return_msg": "매수정정 주문입력이 완료되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/ordr",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt10002"},
        )

        response = client.order.request_modify_order(
            dmst_stex_tp="KRX", orig_ord_no="0000139", stk_cd="005930", mdfy_qty="1", mdfy_uv="199700", mdfy_cond_uv=""
        )
        assert response is not None
        assert isinstance(response.body, DomesticOrderModify)
        assert response.body.mdfy_qty == "000000000001"


def test_request_cancel_order(client: Client):
    expected_data = {
        "ord_no": "0000141",
        "base_orig_ord_no": "0000139",
        "cncl_qty": "000000000001",
        "return_code": 0,
        "return_msg": "매수취소 주문입력이 완료되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/ordr",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "kt10003"},
        )
        response = client.order.request_cancel_order(
            dmst_stex_tp="KRX", orig_ord_no="0000140", stk_cd="005930", cncl_qty="1"
        )
        assert response is not None
        assert isinstance(response.body, DomesticOrderCancel)
        assert response.body.cncl_qty == "000000000001"
