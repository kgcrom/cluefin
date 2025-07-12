import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv()
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_request_buy_order(client: Client):
    time.sleep(1)

    response = client.order.request_buy_order(
        dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
    )
    assert response is not None
    assert response.body is not None
    assert response.body.ord_no is not None


def test_request_sell_order(client: Client):
    time.sleep(1)

    response = client.order.request_sell_order(
        dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
    )
    assert response is not None
    assert response.body is not None


def test_request_modify_order(client: Client):
    time.sleep(1)

    response = client.order.request_modify_order(
        dmst_stex_tp="KRX", orig_ord_no="0000139", stk_cd="005930", mdfy_qty="1", mdfy_uv="199700", mdfy_cond_uv=""
    )
    assert response is not None
    assert response.body is not None


def test_request_cancel_order(client: Client):
    time.sleep(1)

    response = client.order.request_cancel_order(
        dmst_stex_tp="KRX", orig_ord_no="0000140", stk_cd="005930", cncl_qty="1"
    )
    assert response is not None
    assert response.body is not None
