import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import (
    DomesticStockInfoBasic,
    DomesticStockInfoBasicV1,
    DomesticStockInfoChangeRateFromOpen,
    DomesticStockInfoDailyPreviousDayConclusion,
    DomesticStockInfoDailyPreviousDayExecutionVolume,
    DomesticStockInfoDailyTradingDetails,
    DomesticStockInfoDailyTradingItemsByInvestor,
    DomesticStockInfoExecution,
    DomesticStockInfoHighLowPriceApproach,
    DomesticStockInfoHighPer,
    DomesticStockInfoIndustryCode,
    DomesticStockInfoInstitutionalInvestorByStock,
    DomesticStockInfoInterestStockInfo,
    DomesticStockInfoMarginTradingTrend,
    DomesticStockInfoMemberCompany,
    DomesticStockInfoNewHighLowPrice,
    DomesticStockInfoPriceVolatility,
    DomesticStockInfoProgramTradingStatusByStock,
    DomesticStockInfoSummary,
    DomesticStockInfoSupplyDemandConcentration,
    DomesticStockInfoTop50ProgramNetBuy,
    DomesticStockInfoTotalInstitutionalInvestorByStock,
    DomesticStockInfoTradingMember,
    DomesticStockInfoTradingMemberInstantVolume,
    DomesticStockInfoTradingMemberSupplyDemandAnalysis,
    DomesticStockInfoTradingVolumeRenewal,
    DomesticStockInfoUpperLowerLimitPrice,
    DomesticStockInfoVolatilityControlEvent,
)


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    """Create a Client instance for testing.

    Args:
        auth (Auth): The authenticated Auth instance.

    Returns:
        Client: A configured Client instance.
    """
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_stock_info(client: Client):
    time.sleep(1)

    response = client.stock_info.get_stock_info("005930")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoBasic)


def test_get_stock_trading_member(client: Client):
    time.sleep(1)

    response = client.stock_info.get_stock_trading_member("005930")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTradingMember)


def test_get_execution_info(client: Client):
    time.sleep(1)

    response = client.stock_info.get_execution("005930")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoExecution)


def test_get_margin_trading_trend(client: Client):
    time.sleep(1)

    response = client.stock_info.get_margin_trading_trend(stk_cd="005930", dt="20250701", qry_tp="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoMarginTradingTrend)


def test_get_daily_trading_details(client: Client):
    time.sleep(1)

    response = client.stock_info.get_daily_trading_details(stk_cd="005930", strt_dt="20250701")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoDailyTradingDetails)


def test_get_new_high_low_price(client: Client):
    time.sleep(1)

    response = client.stock_info.get_new_high_low_price(
        mrkt_tp="001",  # KOSPI
        ntl_tp="1",  # 신고가
        high_low_close_tp="1",  # 고저기준
        stk_cnd="0",  # 전체조회
        trde_qty_tp="00000",  # 전체조회
        crd_cnd="0",  # 전체조회
        updown_incls="0",  # 미포함
        dt="5",  # 5일
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoNewHighLowPrice)


def test_get_upper_lower_limit_price(client: Client):
    time.sleep(1)

    response = client.stock_info.get_upper_lower_limit_price(
        mrkt_tp="001",  # KOSPI
        updown_tp="1",  # 상한
        sort_tp="1",  # 종목코드순
        stk_cnd="0",  # 전체조회
        trde_qty_tp="00000",  # 전체조회
        crd_cnd="0",  # 전체조회
        trde_gold_tp="0",  # 전체조회
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoUpperLowerLimitPrice)


def test_get_high_low_price_approach(client: Client):
    time.sleep(1)

    response = client.stock_info.get_high_low_price_approach(
        high_low_tp="1",  # 고가
        alacc_rt="05",  # 0.5%
        mrkt_tp="001",  # KOSPI
        trde_qty_tp="00000",  # 전체조회
        stk_cnd="0",  # 전체조회
        crd_cnd="0",  # 전체조회
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoHighLowPriceApproach)


def test_get_price_volatility(client: Client):
    time.sleep(1)

    response = client.stock_info.get_price_volatility(
        mrkt_tp="000",
        flu_tp="1",  # 상위
        tm_tp="1",
        tm="60",
        trde_qty_tp="00000",  # 전체조회
        stk_cnd="0",  # 전체조회
        crd_cnd="0",  # 전체조회
        pric_cnd="0",  # 전체조회
        updown_incls="1",  # 포함
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoPriceVolatility)


def test_get_trading_volume_renewal(client: Client):
    time.sleep(1)

    response = client.stock_info.get_trading_volume_renewal(
        mrkt_tp="001",  # KOSPI
        cycle_tp="5",  # 5일
        trde_qty_tp="5",  # 5천주이상
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTradingVolumeRenewal)


def test_get_supply_demand_concentration(client: Client):
    time.sleep(1)

    response = client.stock_info.get_supply_demand_concentration(
        mrkt_tp="001",  # KOSPI
        prps_cnctr_rt="50",  # 매물집중비율 50%
        cur_prc_entry="0",  # 현재가 매물대 진입 포함안함
        prpscnt="10",  # 매물대수 10개
        cycle_tp="100",  # 100일
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoSupplyDemandConcentration)


def test_get_high_per(client: Client):
    time.sleep(1)

    response = client.stock_info.get_high_per(
        pertp="4",  # 고PER
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoHighPer)


def test_get_change_rate_from_open(client: Client):
    time.sleep(1)

    response = client.stock_info.get_change_rate_from_open(
        sort_tp="1",  # 시가
        trde_qty_cnd="0000",  # 전체조회
        mrkt_tp="001",  # KOSPI
        updown_incls="0",  # 불 포함
        stk_cnd="0",  # 전체조회
        crd_cnd="0",  # 전체조회
        trde_prica_cnd="0",  # 전체조회
        flu_cnd="1",  # 상위
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoChangeRateFromOpen)


def test_get_trading_member_supply_demand_analysis(client: Client):
    time.sleep(1)

    response = client.stock_info.get_trading_member_supply_demand_analysis(
        stk_cd="005930",  # 종목코드
        strt_dt="20250701",  # 시작일자
        end_dt="20250731",  # 종료일자
        qry_dt_tp="0",  # 기간으로 조회
        pot_tp="0",  # 당일
        dt="10",  # 10일
        sort_base="1",  # 종가순
        mmcm_cd="001",  # 회원사코드 (예시)
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTradingMemberSupplyDemandAnalysis)


def test_get_trading_member_instant_volume(client: Client):
    time.sleep(1)

    response = client.stock_info.get_trading_member_instant_volume(
        mmcm_cd="001",  # 회원사코드 (예시)
        stk_cd="005930",  # 종목코드
        mrkt_tp="0",  # 전체
        qty_tp="0",  # 전체
        pric_tp="0",  # 전체
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTradingMemberInstantVolume)


def test_get_volatility_control_event(client: Client):
    time.sleep(1)

    response = client.stock_info.get_volatility_control_event(
        mrkt_tp="001",  # KOSPI
        bf_mkrt_tp="0",  # 전체
        motn_tp="0",  # 전체
        skip_stk="000000000",  # 전종목포함 조회
        trde_qty_tp="0",  # 사용안함
        min_trde_qty="",  # 공백허용
        max_trde_qty="",  # 공백허용
        trde_prica_tp="0",  # 사용안함
        min_trde_prica="",  # 공백허용
        max_trde_prica="",  # 공백허용
        motn_drc="0",  # 전체
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoVolatilityControlEvent)


def test_get_daily_previous_day_execution_volume(client: Client):
    time.sleep(1)

    response = client.stock_info.get_daily_previous_day_execution_volume(
        stk_cd="005930",  # 종목코드
        tdy_pred="1",  # 당일
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoDailyPreviousDayExecutionVolume)


def test_get_daily_trading_items_by_investor(client: Client):
    time.sleep(1)

    response = client.stock_info.get_daily_trading_items_by_investor(
        strt_dt="20250701",  # 시작일자
        end_dt="20250731",  # 종료일자
        trde_tp="2",  # 순매수
        mrkt_tp="001",  # KOSPI
        invsr_tp="8000",  # 개인
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoDailyTradingItemsByInvestor)


def test_get_institutional_investor_by_stock(client: Client):
    time.sleep(1)

    response = client.stock_info.get_institutional_investor_by_stock(
        dt="20250701",  # 일자
        stk_cd="005930",  # 종목코드
        amt_qty_tp="1",  # 금액
        trde_tp="0",  # 순매수
        unit_tp="1000",  # 천주
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoInstitutionalInvestorByStock)


def test_get_total_institutional_investor_by_stock(client: Client):
    time.sleep(1)

    response = client.stock_info.get_total_institutional_investor_by_stock(
        stk_cd="005930",  # 종목코드
        strt_dt="20250701",  # 시작일자
        end_dt="20250731",  # 종료일자
        amt_qty_tp="1",  # 금액
        trde_tp="0",  # 순매수
        unit_tp="1000",  # 천주
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTotalInstitutionalInvestorByStock)


def test_get_daily_previous_day_conclusion(client: Client):
    time.sleep(1)

    response = client.stock_info.get_daily_previous_day_conclusion(
        stk_cd="005930",  # 종목코드
        tdy_pred="1",  # 당일
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoDailyPreviousDayConclusion)


def test_get_interest_stock_info(client: Client):
    time.sleep(1)

    response = client.stock_info.get_interest_stock_info(
        stk_cd="005930|000660",  # 여러 종목코드 입력시 | 로 구분
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoInterestStockInfo)


def test_get_stock_info_summary(client: Client):
    time.sleep(1)

    response = client.stock_info.get_stock_info_summary(
        mrkt_tp="0",  # KOSPI
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoSummary)  # Assuming the response is a list of stock info objects


def test_get_stock_info_v1(client: Client):
    time.sleep(1)

    response = client.stock_info.get_stock_info_v1(
        stk_cd="005930",  # 종목코드
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoBasicV1)


def test_get_industry_code(client: Client):
    time.sleep(1)

    response = client.stock_info.get_industry_code(
        mrkt_tp="0",  # KOSPI
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(
        response.body, DomesticStockInfoIndustryCode
    )  # Assuming the response is a list of industry code objects


def test_get_member_company(client: Client):
    time.sleep(1)

    response = client.stock_info.get_member_company()

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(
        response.body, DomesticStockInfoMemberCompany
    )  # Assuming the response is a list of member company objects


def test_get_top_50_program_net_buy(client: Client):
    time.sleep(1)

    response = client.stock_info.get_top_50_program_net_buy(
        trde_upper_tp="2",  # 순매수상위
        amt_qty_tp="1",  # 금액
        mrkt_tp="P00101",  # KOSPI
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoTop50ProgramNetBuy)


def test_get_program_trading_status_by_stock(client: Client):
    time.sleep(1)

    response = client.stock_info.get_program_trading_status_by_stock(
        dt="20250701",  # 일자
        mrkt_tp="P00101",  # KOSPI
        stex_tp="1",  # KRX
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticStockInfoProgramTradingStatusByStock)
