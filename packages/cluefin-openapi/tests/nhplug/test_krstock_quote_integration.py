"""NH PLUG 국내주식 시세 통합 테스트.

시세 조회 API 는 계좌번호가 필요 없다 — krstock_account fixture 를 쓰지 않는다.
휴일에도 조회된다(2026-08-22 raw 호출 실측 확인).
"""

from datetime import date

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import skip_if_env_blocked

TEST_IEM_CD = "005930"  # 삼성전자
TEST_ETF_IEM_CD = "069500"  # KODEX 200


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


@pytest.mark.integration
def test_current_daily(client: HttpClient):
    """주식현재가 일자별. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_daily(market_cd="KRX", iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_current_investor(client: HttpClient):
    """주식현재가 투자자. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_investor(market_cd="KRX", iem_cd=TEST_IEM_CD, array_cnt="10")
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_period(client: HttpClient):
    """국내주식기간별시세(일/주/월/년). 최근 한 달·일봉(gubun="1") 기준 — 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.period(
            market_cd="KRX",
            iem_cd=TEST_IEM_CD,
            gubun="1",  # 일봉
            edate=date.today().strftime("%Y%m%d"),
            array_cnt="30",  # 최근 한 달치
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_after_hours_current(client: HttpClient):
    """국내주식 시간외현재가. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.after_hours_current(iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_current_after_hours_daily(client: HttpClient):
    """주식현재가 시간외일자별주가. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_after_hours_daily(
            iem_cd=TEST_IEM_CD,
            date=date.today().strftime("%Y%m%d"),
            array_cnt="10",
            maxavg="5",
            gubun="1",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_current_after_hours_execution(client: HttpClient):
    """주식현재가 시간외시간별체결. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.current_after_hours_execution(iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_after_hours_expected(client: HttpClient):
    """주식현재가 시간외시간별예상. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.after_hours_expected(iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_etf_current(client: HttpClient):
    """ETF/ETN 현재가. 대표 ETF(KODEX 200, 069500) 기준 — 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.krstock_quote.etf_current(iem_cd=TEST_ETF_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
