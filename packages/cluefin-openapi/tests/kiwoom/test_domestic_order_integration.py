import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import skip_if_env_blocked

TEST_STK_CD = "005930"


def _unfillable_buy_price(client: Client) -> str:
    """체결되지 않을 만큼 낮으면서 가격제한폭(±30%) 안에 드는 매수 지정가를 계산한다.

    ka10006의 가격 필드는 등락 부호가 붙어 나오므로(예: 하락 시 "-249500") 절댓값을 취한다.
    1,000원 배수로 내림하면 어느 가격대의 호가단위(1/5/10/50/100/500/1000원)에도 맞는다.
    """
    close_pric = client.market_conditions.get_stock_price(stk_cd=TEST_STK_CD).body.close_pric
    base = abs(int(close_pric))
    price = (int(base * 0.8) // 1000) * 1000
    if price <= 0:
        pytest.skip(f"기준가가 너무 낮아 미체결 지정가를 만들 수 없다: {close_pric}")
    return str(price)


@pytest.fixture
def pending_buy_order_no(client: Client) -> str:
    """정정/취소 대상이 될 미체결 매수주문을 실제로 접수하고 그 주문번호를 반환한다.

    주문번호를 하드코딩하면 "RC4032:모의투자 원주문번호가 존재하지 않습니다"로 항상 실패한다.
    모의투자 영업일/장 운영시간이 아니면 주문 접수 자체가 거부되므로 그때는 skip 한다.
    """
    ord_uv = _unfillable_buy_price(client)
    try:
        response = client.order.request_buy_order(
            dmst_stex_tp="KRX",
            stk_cd=TEST_STK_CD,
            ord_qty="1",
            trde_tp="0",  # 보통(지정가) — 시장가는 즉시 체결되어 정정/취소 대상이 될 수 없다
            ord_uv=ord_uv,
            cond_uv="",
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    ord_no = response.body.ord_no
    assert ord_no, "매수주문 응답에 주문번호가 없다"
    return ord_no


@pytest.mark.integration
def test_request_buy_order(client: Client):
    try:
        response = client.order.request_buy_order(
            dmst_stex_tp="KRX", stk_cd=TEST_STK_CD, ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None
    assert response.body.ord_no is not None


@pytest.mark.integration
def test_request_sell_order(client: Client):
    try:
        response = client.order.request_sell_order(
            dmst_stex_tp="KRX", stk_cd=TEST_STK_CD, ord_qty="1", ord_uv="", trde_tp="3", cond_uv=""
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_modify_order(client: Client, pending_buy_order_no: str):
    response = client.order.request_modify_order(
        dmst_stex_tp="KRX",
        orig_ord_no=pending_buy_order_no,
        stk_cd=TEST_STK_CD,
        mdfy_qty="1",
        mdfy_uv=_unfillable_buy_price(client),
        mdfy_cond_uv="",
    )
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
def test_request_cancel_order(client: Client, pending_buy_order_no: str):
    response = client.order.request_cancel_order(
        dmst_stex_tp="KRX", orig_ord_no=pending_buy_order_no, stk_cd=TEST_STK_CD, cncl_qty="1"
    )
    assert response is not None
    assert response.body is not None
