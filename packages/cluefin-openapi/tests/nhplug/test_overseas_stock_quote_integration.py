"""NH PLUG 해외주식 시세 통합 테스트.

시세 조회 API 는 계좌번호가 필요 없다 — gbstock_account fixture 를 쓰지 않는다.
4종 모두 모의투자(moapi)에서 제공되지 않아 운영(NHPLUG_ENV=prod)에서만 검증된다.
"""

from datetime import date

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import real_account_only, skip_if_env_blocked

TEST_IEM_CD = "AAPL"  # 애플
TEST_SYMBOL_CD = "SPX"  # S&P 500 지수


@pytest.mark.integration
@real_account_only(
    "/gbstock/quote/v1/current", "IGW40019: 종목코드(iem_cd)를 확인해주세요 — 모의투자는 어떤 코드도 거부"
)
def test_current(client: HttpClient):
    """해외주식 현재가상세. 계좌번호 없이 성공을 기대한다."""
    try:
        response = client.overseas_stock_quote.current(iem_cd=TEST_IEM_CD)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
@real_account_only("/gbstock/quote/v1/executionTrend", "IGW40019: 모의투자에서 제공되지 않는 서비스")
def test_execution_trend(client: HttpClient):
    """해외주식 체결추이. 일별(period_type="2") 기준으로 조회한다."""
    try:
        response = client.overseas_stock_quote.execution_trend(
            period_type="2",  # 일별
            req_cnt=10,
            iem_cd=TEST_IEM_CD,
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
@real_account_only("/gbstock/quote/v1/period", "IGW40019: 모의투자에서 제공되지 않는 서비스")
def test_period(client: HttpClient):
    """해외주식 기간별시세(개별종목). 최근 한 달·일봉(gubun="3") 기준으로 조회한다."""
    try:
        response = client.overseas_stock_quote.period(
            iem_cd=TEST_IEM_CD,
            end_dt=date.today().strftime("%Y%m%d"),
            count="0030",  # 최근 한 달치
            maxavg="005",
            gubun="3",  # 일
            xtick="0001",
            today_cls="1",  # 당일조회
            market_cls="1",  # 정규장
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
@real_account_only("/gbstock/quote/v1/symbolIndexFxPeriod", "IGW40019: 모의투자에서 제공되지 않는 서비스")
def test_symbol_index_fx_period(client: HttpClient):
    """해외주식 기간별시세(지수·환율). 지수코드·일봉(gubun="1") 기준으로 조회한다."""
    try:
        response = client.overseas_stock_quote.symbol_index_fx_period(
            iem_cd=TEST_SYMBOL_CD,
            end_dt=date.today().strftime("%Y%m%d"),
            array_cnt="0030",  # 최근 한 달치
            maxavg="005",
            gubun="1",  # 일
            today_cls="0",  # 전체조회
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
