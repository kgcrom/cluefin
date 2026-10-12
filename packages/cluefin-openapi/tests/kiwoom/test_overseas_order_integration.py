import math
from typing import Iterator, List

import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import cancel_leftover_orders, real_account_only, skip_if_env_blocked
from ._spec_conformance import assert_spec_conformance

TEST_STEX_TP = "ND"  # NASDAQ
TEST_STK_CD = "AAPL"


def _unfillable_buy_price(client: Client, steps_below: int = 0) -> str:
    """체결되지 않을 만큼 낮은 매수 지정가를 계산한다.

    usa20100의 `cur_prc`는 등락 부호가 붙어 나오므로(예: "-213.4500") 절댓값을 취하고,
    미국장 시간 밖이라 현재가가 0이면 전일종가로 대체한다. 소수점 둘째 자리로 내림하면
    $1 이상 종목의 호가단위($0.01)에 맞는다.
    `steps_below` 만큼 $0.01씩 더 낮춘다 — 국내는 원주문과 같은 가격의 정정이 거부됐다(RC4041).
    """
    body = client.overseas_market_condition.get_current_price_stock_info(stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD).body
    base = abs(float(body.cur_prc or 0)) or abs(float(body.base_close_pric or 0))
    price = (math.floor(base * 0.8 * 100) - steps_below) / 100
    if price <= 0:
        pytest.skip(f"기준가를 구할 수 없어 미체결 지정가를 만들 수 없다: cur_prc={body.cur_prc!r}")
    return f"{price:.2f}"


@pytest.fixture
def pending_orders(client: Client) -> Iterator[List[str]]:
    """테스트가 접수한 주문번호를 모아 두었다가, 테스트가 실패해도 끝나면 취소한다.

    취소·정정으로 원주문이 사라졌으면 테스트가 목록을 고쳐 둔다 (취소는 빼고, 정정은 새 번호로 바꾼다).
    """
    ord_nos: List[str] = []
    yield ord_nos
    cancel_leftover_orders(
        ord_nos,
        lambda ord_no: client.overseas_order.request_cancel_order(
            orig_ord_no=ord_no, stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD
        ),
    )


@pytest.fixture
def pending_buy_order_no(client: Client, pending_orders: List[str]) -> str:
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
    pending_orders.append(ord_no)
    return ord_no


@pytest.mark.integration
@pytest.mark.mutation
def test_request_buy_order(client: Client, pending_orders: List[str]):
    # $1.00 지정가라 체결되지 않는다 — 미체결로 남은 주문은 teardown 에서 취소한다.
    try:
        response = client.overseas_order.request_buy_order(
            stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD, ord_qty="1", trde_tp="00", ord_uv="1.00"
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
    # $100,000 지정가라 체결되지 않는다 — 미체결로 남은 주문은 teardown 에서 취소한다.
    try:
        response = client.overseas_order.request_sell_order(
            stk_cd=TEST_STK_CD, stex_tp=TEST_STEX_TP, ord_qty="1", trde_tp="00", ord_uv="100000.00"
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
    response = client.overseas_order.request_modify_order(
        orig_ord_no=pending_buy_order_no,
        stex_tp=TEST_STEX_TP,
        stk_cd=TEST_STK_CD,
        mdfy_uv=_unfillable_buy_price(client, steps_below=1),
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
    response = client.overseas_order.request_cancel_order(
        orig_ord_no=pending_buy_order_no, stex_tp=TEST_STEX_TP, stk_cd=TEST_STK_CD
    )
    pending_orders.remove(pending_buy_order_no)  # 취소됐으니 teardown 이 다시 취소하지 않게
    assert_spec_conformance(client, response)
    assert response is not None
    assert response.body is not None


@pytest.mark.integration
@real_account_only("ust31490", "RC9000:모의투자에서는 해당업무가 제공되지 않습니다")
def test_get_orderable_quantity(client: Client):
    response = client.overseas_order.get_orderable_quantity(stk_cd=TEST_STK_CD, uv="1.00", stex_tp=TEST_STEX_TP)
    assert_spec_conformance(client, response)
    assert response is not None
    assert response.body is not None
