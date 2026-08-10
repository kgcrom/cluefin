import math

import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import real_account_only, skip_if_env_blocked

TEST_STEX_TP = "ND"  # NASDAQ
TEST_STK_CD = "AAPL"


def _unfillable_buy_price(client: Client) -> str:
    """체결되지 않을 만큼 낮은 매수 지정가를 계산한다.

    usa20100의 `cur_prc`는 등락 부호가 붙어 나오므로(예: "-213.4500") 절댓값을 취하고,
    미국장 시간 밖이라 현재가가 0이면 전일종가로 대체한다. 소수점 둘째 자리로 내림하면
    $1 이상 종목의 호가단위($0.01)에 맞는다.
    """
    body = client.overseas_market_condition.get_current_price_stock_info(stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD).body
    base = abs(float(body.cur_prc or 0)) or abs(float(body.base_close_pric or 0))
    price = math.floor(base * 0.8 * 100) / 100
    if price <= 0:
        pytest.skip(f"기준가를 구할 수 없어 미체결 지정가를 만들 수 없다: cur_prc={body.cur_prc!r}")
    return f"{price:.2f}"


@pytest.fixture
def pending_buy_order_no(client: Client) -> str:
    """정정/취소 대상이 될 미체결 매수주문을 실제로 접수하고 그 주문번호를 반환한다.

    주문번호를 하드코딩하면 "RC4061:모의투자 주문번호를 확인하세요"로 항상 실패한다.
    해외 모의투자 계좌가 만료됐거나 미국장 운영시간이 아니면 접수 자체가 거부되므로 skip 한다.
    """
    try:
        response = client.overseas_order.request_buy_order(
            stex_tp=TEST_STEX_TP,
            stk_cd=TEST_STK_CD,
            ord_qty="1",
            trde_tp="00",  # 지정가 — 시장가는 즉시 체결되어 정정/취소 대상이 될 수 없다
            ord_uv=_unfillable_buy_price(client),
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    ord_no = response.body.ord_no
    assert ord_no, "매수주문 응답에 주문번호가 없다"
    return ord_no


@pytest.mark.integration
def test_request_buy_order(client: Client):
    try:
        response = client.overseas_order.request_buy_order(
            stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD, ord_qty="1", trde_tp="00", ord_uv="1.00"
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_sell_order(client: Client):
    try:
        response = client.overseas_order.request_sell_order(
            stk_cd=TEST_STK_CD, stex_tp=TEST_STEX_TP, ord_qty="1", trde_tp="00", ord_uv="100000.00"
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_modify_order(client: Client, pending_buy_order_no: str):
    response = client.overseas_order.request_modify_order(
        orig_ord_no=pending_buy_order_no,
        stex_tp=TEST_STEX_TP,
        stk_cd=TEST_STK_CD,
        mdfy_uv=_unfillable_buy_price(client),
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_cancel_order(client: Client, pending_buy_order_no: str):
    response = client.overseas_order.request_cancel_order(
        orig_ord_no=pending_buy_order_no, stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
@real_account_only("ust31490", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_orderable_quantity(client: Client):
    response = client.overseas_order.get_orderable_quantity(stk_cd=TEST_STK_CD, uv="1.00", stex_tp=TEST_STEX_TP)
    assert response is not None
    assert response.body is not None
