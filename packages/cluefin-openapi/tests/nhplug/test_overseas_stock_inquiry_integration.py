"""NH PLUG 해외주식 조회 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 조회를 수행한다. 조회 API 는 주문과 달리 장 운영
시간·영업일 제약이 없어 휴일에도 성공해야 한다. 주문 카테고리(gbstock order)는
실제 체결이 발생하므로 통합 테스트를 두지 않는다.
"""

from datetime import date, timedelta

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import skip_if_env_blocked

TEST_IEM_CD = "AAPL"  # 애플
US_NATION_CD = "200"  # 미국


@pytest.mark.integration
def test_balance(client: HttpClient, gbstock_account: str):
    """해외주식 잔고. 조회 API 라 성공을 기대한다."""
    try:
        response = client.overseas_stock_inquiry.balance(
            act_no=gbstock_account,
            qut_iqr_dit_cd="9",  # 전체
            fc_sec_trd_nat_cd=US_NATION_CD,
            cur_cd="KRW",  # 전체
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_buyable_amount(client: HttpClient, gbstock_account: str):
    """해외주식 매수가능금액 조회. 조회 API 라 성공을 기대한다."""
    try:
        response = client.overseas_stock_inquiry.buyable_amount(
            act_no=gbstock_account,
            pcs_dit="1",  # 매수가능금액조회
            fc_sec_trd_nat_cd=US_NATION_CD,
            iem_cd=TEST_IEM_CD,
            wtm_cur_knd_cd="2",  # 원화
            oss_orr_knd_cd="1",  # GTS(미국시장주문)
            ahi_nmn_pr_tp_cd="03",  # 시장가
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_unexecuted(client: HttpClient, gbstock_account: str):
    """해외주식 주문체결내역. 당일 전체 주문을 조회한다 — 주문이 없어도 성공해야 한다."""
    try:
        response = client.overseas_stock_inquiry.unexecuted(
            orr_dt=date.today().strftime("%Y%m%d"),
            act_no=gbstock_account,
            oss_sby_dit_cd="0",  # 전체
            sot_dit="0",  # 주문번호순
            ost_cns_dit="0",  # 전체
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_reserved_inquiry(client: HttpClient, gbstock_account: str):
    """해외주식 예약주문조회. 당일 전체 예약주문을 조회한다."""
    try:
        response = client.overseas_stock_inquiry.reserved_inquiry(
            fc_mkt_dit_cd="000",  # 전체
            bkg_orr_dt=date.today().strftime("%Y%m%d"),
            act_no=gbstock_account,
            sby_dit_cd="0",  # 전체
            bkg_orr_can_yn="0",  # 전체
            oss_orr_knd_cd="0",  # 전체
            bkg_orr_tp_cd="0",  # 전체
            wtm_cur_knd_cd="0",  # 전체
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_daily_transaction(client: HttpClient, gbstock_account: str):
    """해외주식 일별거래내역. 최근 한 달(오늘 포함) 범위로 조회한다."""
    try:
        response = client.overseas_stock_inquiry.daily_transaction(
            act_no=gbstock_account,
            iqr_sta_dt=(date.today() - timedelta(days=30)).strftime("%Y%m%d"),
            iqr_end_dt=date.today().strftime("%Y%m%d"),
            act_trd_cfc_cd="00",  # 전체
            iem_mlf_cd="00001",  # 외화주식
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_period_pnl(client: HttpClient, gbstock_account: str):
    """해외주식 기간손익. 최근 한 달(오늘 포함) 범위로 조회한다."""
    try:
        response = client.overseas_stock_inquiry.period_pnl(
            act_no=gbstock_account,
            iqr_dit="2",  # 원화기준
            sta_orr_dt=(date.today() - timedelta(days=30)).strftime("%Y%m%d"),
            end_orr_dt=date.today().strftime("%Y%m%d"),
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_period_pnl_detail(client: HttpClient, gbstock_account: str):
    """해외주식 기간손익 상세. 오늘 주문일자 기준 — 거래가 없어도 성공해야 한다."""
    try:
        response = client.overseas_stock_inquiry.period_pnl_detail(
            act_no=gbstock_account,
            iqr_dit="2",  # 원화기준
            orr_dt=date.today().strftime("%Y%m%d"),
            fc_sec_trd_nat_cd=US_NATION_CD,
            trd_cur_cd="USD",
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_margin(client: HttpClient, gbstock_account: str):
    """해외증거금 통화별조회. 조회 API 라 성공을 기대한다."""
    try:
        response = client.overseas_stock_inquiry.margin(act_no=gbstock_account)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
