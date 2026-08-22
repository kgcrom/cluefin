"""NH PLUG 국내주식 조회 통합 테스트.

모의투자(NHPLUG_ENV=dev)에서 실제 조회를 수행한다. 조회 API 는 주문과 달리 장 운영
시간·영업일 제약이 없어 휴일에도 성공해야 한다(2026-08-22 raw 호출 실측 확인).
"""

from datetime import date, timedelta

import pytest

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError
from cluefin_openapi.nhplug._http_client import HttpClient
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._integration_helpers import real_account_only, skip_if_env_blocked


@pytest.mark.integration
def test_asset_status(client: HttpClient, krstock_account: str):
    """투자계좌자산현황조회. 조회 API 라 성공을 기대한다."""
    try:
        response = client.krstock_inquiry.asset_status(
            act_no=krstock_account,
            eal_aly_cd="2",  # 시가평가
            aet_bse="1",  # 순자산
            qut_dit_cd="UNT",  # 통합시세
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
@real_account_only("/krstock/inquiry/v1/integratedMargin", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_integrated_margin(client: HttpClient, krstock_account: str):
    """주식통합증거금 현황. 조회 API 라 성공을 기대한다."""
    try:
        response = client.krstock_inquiry.integrated_margin(act_no=krstock_account)
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


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


@pytest.mark.integration
def test_buyable_quantity(client: HttpClient, krstock_account: str):
    """매수가능수량조회 (005930, 현금).

    nmn_pr_tp_cd="05"(시장가)를 사용해 orr_pr(주문가격) 입력을 피한다 — 스펙상
    orr_pr 은 지정가 계열일 때만 의미가 있고, 시장가에는 필요 없다(고정 가격을
    임의로 넣지 않기 위함).
    """
    try:
        response = client.krstock_inquiry.buyable_quantity(
            act_no=krstock_account,
            iem_cd="005930",
            ost_dit_cd="1",  # 현금
            nmn_pr_tp_cd="05",  # 시장가 — orr_pr 불필요
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
@real_account_only("/krstock/inquiry/v1/reservedInquiry", "19999: 모의투자에서는 해당업무가 제공되지 않습니다")
def test_reserved_inquiry(client: HttpClient, krstock_account: str):
    """주식예약주문조회. reservedOrder 접수가 모의 미지원이라 목록은 비어있을 것으로
    예상하지만, 조회 자체의 성공/미지원 여부가 관전 포인트라 실측 결과 그대로
    검증한다(rsp_cd 위주, Output_1 존재는 단정하지 않음)."""
    try:
        response = client.krstock_inquiry.reserved_inquiry(
            act_no=krstock_account,
            sby_dit_cd="0",  # 전체
            bkg_orr_tp_cd="0",  # 전체
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_daily_pnl(client: HttpClient, krstock_account: str):
    """실현손익일별합산조회. 최근 한 달(오늘 포함) 범위로 조회 — 조회 API 라 성공을 기대한다."""
    today = date.today()
    try:
        response = client.krstock_inquiry.daily_pnl(
            act_no=krstock_account,
            iqr_sta_dt=(today - timedelta(days=30)).strftime("%Y%m%d"),
            iqr_end_dt=today.strftime("%Y%m%d"),
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_realized_pnl(client: HttpClient, krstock_account: str):
    """주식잔고조회_실현손익. 조회 API 라 성공을 기대한다."""
    try:
        response = client.krstock_inquiry.realized_pnl(
            act_no=krstock_account,
            iqr_dit_cd1="0",  # 전체
            fee_dit_cd="1",  # 온라인
            qut_dit_cd="UNT",  # 통합시세
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_trading_pnl(client: HttpClient, krstock_account: str):
    """종목별실현손익현황조회. 최근 한 달(오늘 포함) 범위로 조회 — 조회 API 라 성공을 기대한다."""
    today = date.today()
    try:
        response = client.krstock_inquiry.trading_pnl(
            act_no=krstock_account,
            iqr_sta_dt=(today - timedelta(days=30)).strftime("%Y%m%d"),
            iqr_end_dt=today.strftime("%Y%m%d"),
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES


@pytest.mark.integration
def test_sellable_quantity(client: HttpClient, krstock_account: str):
    """매도가능수량조회 (005930, 현금/신용 잔고).

    cfd_lon_cd="00"(일반거래=현금)을 사용한다 — 스펙 설명의 신용대출코드 목록 중
    보유 잔고 유무와 무관하게 항상 유효한 가장 기본 형태다. 보유 잔고가 없어
    매도가능수량이 0이어도 조회 자체는 성공할 것으로 예상한다.
    """
    try:
        response = client.krstock_inquiry.sellable_quantity(
            act_no=krstock_account,
            iem_cd="005930",
            cfd_lon_cd="00",  # 일반거래(현금)
        )
    except NHPlugAPIError as e:
        skip_if_env_blocked(e)

    assert response.body.rsp_cd in SUCCESS_RSP_CODES
