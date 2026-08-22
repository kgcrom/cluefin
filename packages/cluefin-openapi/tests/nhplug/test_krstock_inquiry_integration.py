"""NH PLUG 국내주식 조회 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 조회를 수행한다. 조회 API 는 주문과 달리 장 운영
시간·영업일 제약이 없어 휴일에도 성공해야 한다(2026-08-22 raw 호출 실측 확인).
"""

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient

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

    assert response.body.rsp_cd == "00000"
    assert response.header.cts_flag is not None
