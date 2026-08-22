"""NH PLUG 국내주식 주문 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 주문을 접수한다 — kiwoom 주문 통합테스트와
같은 방식. 운영(prod)으로 돌리면 실제 체결되므로 절대 prod 로 실행하지 말 것.
장 운영시간(평일 09:00–15:30 KST)이 아니면 접수 거부 코드로 skip 된다.
"""

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

from ._integration_helpers import skip_if_env_blocked

TEST_IEM_CD = "005930"  # 삼성전자


@pytest.mark.integration
def test_cash_buy_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 매수 접수. 모의투자 계좌라 실손실은 없다."""
    try:
        response = client.krstock_order.cash_buy(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
def test_cash_sell_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 매도 접수. 보유 잔고가 없으면 거부 코드가 나올 수 있다 —
    그 코드도 환경 제약이므로 실측 후 ENV_BLOCKED_CODES 에 등록한다."""
    try:
        response = client.krstock_order.cash_sell(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None
