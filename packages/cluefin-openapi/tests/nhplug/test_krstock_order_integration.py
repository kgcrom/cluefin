"""NH PLUG 국내주식 주문 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 주문을 접수한다 — kiwoom 주문 통합테스트와
같은 방식. 운영(prod)으로 돌리면 실제 체결되므로 절대 prod 로 실행하지 말 것.
장 운영시간(평일 09:00–15:30 KST)이 아니면 접수 거부 코드로 skip 된다.
"""

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

from ._integration_helpers import real_account_only, skip_if_env_blocked

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
@real_account_only("/krstock/order/v1/creditBuy", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_credit_buy_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 신용 매수 접수. 운영에서만 검증 가능 — 실제 신용주문이 체결된다.

    cfd_lon_cd="01"(유통융자)을 사용한다 — 스펙 설명의 신용대출코드 목록(01.유통융자
    02.자기융자 03.유통대주 04.자기대주 10.매입자금대출) 중 신규 매수 신용거래의
    가장 기본 형태(융자·유통물)이고, lon_dt(대출일자)는 스펙상 03·04(대주)일 때만
    필수라 01을 쓰면 추가 입력 없이 호출할 수 있다.
    """
    try:
        response = client.krstock_order.credit_buy(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            cfd_lon_cd="01",  # 유통융자 — lon_dt 불필요
            rmt_mkt_cd="KRX",
            sor_mkt_sli_yn="N",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.output_0 is not None
    assert response.body.output_0.mkt_orr_no is not None


@pytest.mark.integration
@real_account_only("/krstock/order/v1/creditSell", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_credit_sell_market_order(client: HttpClient, krstock_account: str):
    """시장가 1주 신용 매도 접수. 운영에서만 검증 가능 — 실제 신용주문이 체결된다.

    creditSell 스펙은 creditBuy 와 필드·required 구성이 완전히 동일하다(설명 문구의
    쉼표 하나 차이뿐). creditBuy 실측(19999: 모의투자에서는 해당업무가 제공되지 않습니다)을
    신용 계열 API 전체의 공통 제약으로 보고 동일한 skip 을 붙였지만, creditSell 자체는
    아직 실측하지 않은 추정이다 — 운영 검증 시 이 marker 를 다시 확인할 것.

    cfd_lon_cd="01"(유통융자)을 사용한다 — lon_dt(대출일자)는 스펙상 03·04(대주)일
    때만 필수라 01을 쓰면 추가 입력 없이 호출할 수 있다.
    """
    try:
        response = client.krstock_order.credit_sell(
            act_no=krstock_account,
            iem_cd=TEST_IEM_CD,
            orr_qty=1,
            nmn_pr_tp_cd="05",  # 시장가
            cfd_lon_cd="01",  # 유통융자 — lon_dt 불필요
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
