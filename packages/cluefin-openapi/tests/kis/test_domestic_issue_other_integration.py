"""Integration tests for the KIS domestic issue other module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import os
import time
from typing import Literal, cast

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._http_client import HttpClient


@pytest.fixture(scope="module")
def auth_dev():
    """Fixture to create Auth instance for dev environment."""
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("KIS_APP_KEY")
    secret_key = os.getenv("KIS_SECRET_KEY")
    env = cast(Literal["dev", "prod"], os.getenv("KIS_ENV", "dev"))

    if not app_key or not secret_key:
        pytest.skip("KIS API credentials not available in environment variables")

    return Auth(app_key=app_key, secret_key=SecretStr(secret_key), env=env)


@pytest.fixture(scope="module")
def client(auth_dev):
    """Fixture to create KIS Client with valid token."""
    token_response = auth_dev.generate()
    return HttpClient(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
        # debug=True,
    )


# ==================== Sector Index APIs ====================


@pytest.mark.integration
def test_get_sector_current_index(client: HttpClient):
    """Test sector current index inquiry (KOSPI)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_current_index(
            fid_cond_mrkt_div_code="U",
            fid_input_iscd="0001",  # 0001:코스피, 1001:코스닥, 2001:코스피200
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")

    except Exception as e:
        pytest.fail(f"get_sector_current_index failed: {e}")


@pytest.mark.integration
def test_get_sector_daily_index(client: HttpClient):
    """Test sector daily index inquiry (KOSPI daily)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_daily_index(
            fid_period_div_code="D",  # D:일별, W:주별, M:월별
            fid_cond_mrkt_div_code="U",  # 업종 U
            fid_input_iscd="0001",  # 0001:코스피, 1001:코스닥, 2001:코스피200
            fid_input_date_1="20240701",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_daily_index failed: {e}")


@pytest.mark.integration
def test_get_sector_time_index_second(client: HttpClient):
    """Test sector time index by second (KOSPI)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_time_index_second(
            fid_input_iscd="0001",  # 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
            fid_cond_mrkt_div_code="U",  # 업종 U
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_time_index_second failed: {e}")


@pytest.mark.integration
def test_get_sector_time_index_minute(client: HttpClient):
    """Test sector time index by minute (KOSPI 1-minute)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_time_index_minute(
            fid_input_hour_1="60",  # 60:1분, 300:5분, 600:10분
            fid_input_iscd="0001",  # 0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150
            fid_cond_mrkt_div_code="U",  # 업종 U
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_time_index_minute failed: {e}")


@pytest.mark.integration
def test_get_sector_minute_inquiry(client: HttpClient):
    """Test sector minute candle inquiry (KOSPI 1-minute)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_minute_inquiry(
            fid_cond_mrkt_div_code="U",  # U
            fid_etc_cls_code="0",  # 0:기본, 1:장마감,시간외 제외
            fid_input_iscd="0001",  # 0001:종합, 0002:대형주
            fid_input_hour_1="60",  # 30, 60:1분, 600:10분, 3600:1시간
            fid_pw_data_incu_yn="N",  # Y:과거, N:당일
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_minute_inquiry failed: {e}")


@pytest.mark.integration
def test_get_sector_period_quote(client: HttpClient):
    """Test sector period quote (daily/weekly/monthly/yearly)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_period_quote(
            fid_cond_mrkt_div_code="U",  # 업종:U
            fid_input_iscd="0001",  # 0001:종합, 0002:대형주
            fid_input_date_1="20240501",
            fid_input_date_2="20240531",
            fid_period_div_code="D",  # D:일봉, W:주봉, M:월봉, Y:년봉
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_period_quote failed: {e}")


@pytest.mark.integration
def test_get_sector_all_quote_by_category(client: HttpClient):
    """Test sector all quote by category (KOSPI)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_sector_all_quote_by_category(
            fid_cond_mrkt_div_code="U",  # 업종 U
            fid_input_iscd="0001",  # 0001:코스피, 1001:코스닥, 2001:코스피200
            fid_cond_scr_div_code="20214",  # Unique key: 20214
            fid_mrkt_cls_code="K",  # K:거래소, Q:코스닥, K2:코스피200
            fid_blng_cls_code="0",  # 0:전업종, 1:기타구분, 2:자본금/벤처구분, 3:상업별/일반구분
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_sector_all_quote_by_category failed: {e}")


# ==================== Expected Index APIs ====================


@pytest.mark.integration
def test_get_expected_index_trend(client: HttpClient):
    """Test expected index trend (pre-market KOSPI)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_expected_index_trend(
            fid_mkop_cls_code="1",  # 1:장시작전, 2:장마감
            fid_input_hour_1="60",  # 10:10초, 30:30초, 60:1분, 600:10분
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_cond_mrkt_div_code="U",  # 주식 U
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_expected_index_trend failed: {e}")


@pytest.mark.integration
def test_get_expected_index_all(client: HttpClient):
    """Test expected index all (pre-market all indices)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_expected_index_all(
            fid_mrkt_cls_code="0",  # 0:전체, K:거래소, Q:코스닥
            fid_cond_mrkt_div_code="U",  # 업종 U
            fid_cond_scr_div_code="11175",  # Unique key: 11175
            fid_input_iscd="0000",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_mkop_cls_code="1",  # 1:장시작전, 2:장마감
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_expected_index_all failed: {e}")


# ==================== Market Information APIs ====================


@pytest.mark.integration
def test_get_volatility_interruption_status(client: HttpClient):
    """Test volatility interruption (VI) status."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_volatility_interruption_status(
            fid_div_cls_code="0",  # 0:전체, 1:상승, 2:하락
            fid_cond_scr_div_code="20139",  # 20139
            fid_mrkt_cls_code="0",  # 0:전체, K:거래소, Q:코스닥
            fid_input_iscd="",
            fid_rank_sort_cls_code="0",  # 0:전체, 1:정적, 2:동적, 3:정적&동적
            fid_input_date_1="20250109",  # 영업일
            fid_trgt_cls_code="",
            fid_trgt_exls_cls_code="",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_volatility_interruption_status failed: {e}")


@pytest.mark.integration
def test_get_interest_rate_summary(client: HttpClient):
    """Test interest rate summary (domestic bonds/interest rates)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_interest_rate_summary(
            fid_cond_mrkt_div_code="I",  # Unique key: I
            fid_cond_scr_div_code="20702",  # Unique key: 20702
            fid_div_cls_code="1",  # 1:해외금리지표
            fid_div_cls_code1="",  # 공백:전체
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_interest_rate_summary failed: {e}")


@pytest.mark.integration
def test_get_market_announcement_schedule(client: HttpClient):
    """Test market announcement schedule (news titles)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_market_announcement_schedule(
            fid_news_ofer_entp_code="",  # 공백 필수
            fid_cond_mrkt_cls_code="",  # 공백 필수
            fid_input_iscd="",  # 공백:전체, 종목코드:해당코드 뉴스
            fid_titl_cntt="",  # 공백 필수
            fid_input_date_1="",  # 공백:현재기준, 조회일자 ex. 00YYYYMMDD
            fid_input_hour_1="",  # 공백:현재기준, 조회시간 ex. 0000HHMMSS
            fid_rank_sort_cls_code="",  # 공백 필수
            fid_input_srno="",  # 공백 필수
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_market_announcement_schedule failed: {e}")


@pytest.mark.integration
def test_get_holiday_inquiry(client: HttpClient):
    """Test holiday inquiry (domestic market holidays)."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_holiday_inquiry(
            bass_dt="20250101",  # YYYYMMDD
            ctx_area_nk="",  # 공백으로 입력
            ctx_area_fk="",  # 공백으로 입력
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_holiday_inquiry failed: {e}")


@pytest.mark.integration
def test_get_futures_business_day_inquiry(client: HttpClient):
    """Test futures business day inquiry."""
    time.sleep(1)
    try:
        response = client.domestic_issue_other.get_futures_business_day_inquiry()

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_futures_business_day_inquiry failed: {e}")
