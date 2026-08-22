"""NH PLUG 국내주식 시세 통합 테스트.

시세 조회 API 는 계좌번호가 필요 없다 — krstock_account fixture 를 쓰지 않는다.
휴일에도 조회된다(2026-08-22 raw 호출 실측 확인).
"""

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import skip_if_env_blocked

TEST_IEM_CD = "005930"  # 삼성전자


@pytest.mark.integration
def test_current_price(client: HttpClient):
    """주식현재가 시세. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_price(market_cd="KRX", iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
    assert response.body.output_0 is not None
    assert response.body.output_0.stck_prpr is not None


@pytest.mark.integration
def test_current_execution(client: HttpClient):
    """주식현재가 체결. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_execution(market_cd="KRX", iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
