import math
from typing import Iterator, List

import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import cancel_leftover_orders, skip_if_env_blocked
from ._spec_conformance import assert_spec_conformance

TEST_STK_CD = "005930"


def _base_price(client: Client) -> int:
    """ka10006 종가. 가격 필드는 등락 부호가 붙어 나오므로(예: 하락 시 "-249500") 절댓값을 취한다."""
    return abs(int(client.market_conditions.get_stock_price(stk_cd=TEST_STK_CD).body.close_pric))


def _unfillable_buy_price(client: Client, steps_below: int = 0) -> str:
    """체결되지 않을 만큼 낮으면서 가격제한폭(±30%) 안에 드는 매수 지정가를 계산한다.

    1,000원 배수로 내림하면 어느 가격대의 호가단위(1/5/10/50/100/500/1000원)에도 맞는다.
    `steps_below` 만큼 1,000원씩 더 낮춘다 — 정정은 원주문과 같은 가격이면 거부된다(RC4041).
    """
    base = _base_price(client)
    price = (int(base * 0.8) // 1000 - steps_below) * 1000
    if price <= 0:
        pytest.skip(f"기준가가 너무 낮아 미체결 지정가를 만들 수 없다: {base}")
    return str(price)


def _unfillable_sell_price(client: Client) -> str:
    """체결되지 않을 만큼 높으면서 상한가(+30%) 안에 드는 매도 지정가. 1,000원 배수로 올림한다."""
    base = _base_price(client)
    price = math.ceil(base * 1.2 / 1000) * 1000
    if price > base * 1.3:
        pytest.skip(f"기준가가 너무 낮아 상한가 안의 미체결 매도 지정가를 만들 수 없다: {base}")
    return str(price)


@pytest.fixture
def pending_orders(client: Client) -> Iterator[List[str]]:
    """테스트가 접수한 주문번호를 모아 두었다가, 테스트가 실패해도 끝나면 잔량 전부를 취소한다.

    취소·정정으로 원주문이 사라졌으면 테스트가 목록을 고쳐 둔다 (취소는 빼고, 정정은 새 번호로 바꾼다).
    """
    ord_nos: List[str] = []
    yield ord_nos
    cancel_leftover_orders(
        ord_nos,
        lambda ord_no: client.order.request_cancel_order(
            dmst_stex_tp="KRX",
            orig_ord_no=ord_no,
            stk_cd=TEST_STK_CD,
            cncl_qty="0",  # '0' = 잔량 전부 취소
        ),
    )


@pytest.fixture
def pending_buy_order_no(client: Client, pending_orders: List[str]) -> str:
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
    pending_orders.append(ord_no)
    return ord_no


@pytest.mark.integration
@pytest.mark.mutation
def test_request_buy_order(client: Client, pending_orders: List[str]):
    # 시장가(trde_tp="3")는 바로 체결되어 계좌에 주식이 남는다 — 체결되지 않는 지정가로 내고 teardown 에서 취소한다.
    try:
        response = client.order.request_buy_order(
            dmst_stex_tp="KRX",
            stk_cd=TEST_STK_CD,
            ord_qty="1",
            ord_uv=_unfillable_buy_price(client),
            trde_tp="0",
            cond_uv="",
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None
    assert response.body.ord_no
    pending_orders.append(response.body.ord_no)


@pytest.mark.integration
@pytest.mark.mutation
def test_request_sell_order(client: Client, pending_orders: List[str]):
    # 시장가는 보유 주식을 바로 판다 — 체결되지 않는 지정가로 내고 teardown 에서 취소한다.
    try:
        response = client.order.request_sell_order(
            dmst_stex_tp="KRX",
            stk_cd=TEST_STK_CD,
            ord_qty="1",
            ord_uv=_unfillable_sell_price(client),
            trde_tp="0",
            cond_uv="",
        )
    except KiwoomAPIError as e:
        skip_if_env_blocked(e)

    assert response is not None
    assert response.body is not None
    assert response.body.ord_no
    pending_orders.append(response.body.ord_no)


@pytest.mark.integration
@pytest.mark.mutation
def test_request_modify_order(client: Client, pending_buy_order_no: str, pending_orders: List[str]):
    response = client.order.request_modify_order(
        dmst_stex_tp="KRX",
        orig_ord_no=pending_buy_order_no,
        stk_cd=TEST_STK_CD,
        mdfy_qty="1",
        mdfy_uv=_unfillable_buy_price(client, steps_below=1),
        mdfy_cond_uv="",
    )
    # 정정이 받아들여지면 원주문은 사라지고 새 주문번호로 남는다 — teardown 이 새 번호를 취소하게 바꾼다.
    if response.body.ord_no:
        pending_orders[pending_orders.index(pending_buy_order_no)] = response.body.ord_no
    assert_spec_conformance(client, response)
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
@pytest.mark.mutation
def test_request_cancel_order(client: Client, pending_buy_order_no: str, pending_orders: List[str]):
    response = client.order.request_cancel_order(
        dmst_stex_tp="KRX", orig_ord_no=pending_buy_order_no, stk_cd=TEST_STK_CD, cncl_qty="1"
    )
    pending_orders.remove(pending_buy_order_no)  # 취소됐으니 teardown 이 다시 취소하지 않게
    assert_spec_conformance(client, response)
    assert response is not None
    assert response.body is not None
