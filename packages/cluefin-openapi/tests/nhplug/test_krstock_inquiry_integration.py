"""NH PLUG 국내주식 조회 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 조회를 수행한다. 조회 API 는 주문과 달리 장 운영
시간·영업일 제약이 없어 휴일에도 성공해야 한다(2026-08-22 raw 호출 실측 확인).
"""

from datetime import date

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import skip_if_env_blocked


@pytest.mark.integration
def test_balance(client: HttpClient, krstock_account: str):
    """주식잔고조회. 조회 API 라 성공을 기대한다."""
    try:
        response = client.krstock_inquiry.balance(
            act_no=krstock_account,
            bnc_bse_cd="1",  # 주식관련 총 평가(체결기준)
            ltg_aot_dit_cd="9",  # 전체
            aet_bse="1",  # 순자산
            qut_dit_cd="UNT",  # 통합시세
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
    assert response.header.cts_flag is not None


@pytest.mark.integration
def test_daily_order_execution(client: HttpClient, krstock_account: str):
    """주식일별주문체결조회. 오늘 날짜로 조회 — 주문 이력이 없어도 조회 자체는 성공한다.

    Output_0/Output_1 은 데이터가 있을 때만 내려오므로(스펙 설명) 존재를 단정하지
    않고 rsp_cd 위주로 검증한다.
    """
    try:
        response = client.krstock_inquiry.daily_order_execution(
            act_no=krstock_account,
            orr_dt=date.today().strftime("%Y%m%d"),
            ost_cns_dit="0",  # 전체
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    # 모의서버는 성공에 XA102("모의투자 조회가 완료되었습니다")를 반환한다 (2026-08-22 실측).
    assert response.body.rsp_cd in SUCCESS_RSP_CODES
