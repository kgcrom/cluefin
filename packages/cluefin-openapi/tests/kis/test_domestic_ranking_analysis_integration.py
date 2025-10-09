"""Integration tests for the KIS domestic ranking analysis module.

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
from cluefin_openapi.kis._client import Client

from _token_cache import TokenCache


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
def token_cache(auth_dev):
    """Fixture to provide persistent token cache."""
    cache = TokenCache(auth_dev)
    yield cache
    # Note: We don't clear the cache on teardown to allow reuse across test runs


@pytest.fixture(scope="module")
def client(auth_dev, token_cache):
    """Fixture to create KIS Client with valid token."""
    token_response = token_cache.get()
    return Client(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
        # debug=True,
    )


# ==================== Volume & Trading APIs ====================


@pytest.mark.integration
def test_get_trading_volume_rank(client: Client):
    """Test trading volume ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_trading_volume_rank(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20171",
            fid_input_iscd="0000",  # 0000:전체, 기타:업종코드
            fid_div_cls_code="0",  # 0:전체, 1:보통주, 2:우선주
            fid_blng_cls_code="0",  # 0:평균거래량, 1:거래증가율, 2:평균거래회전율, 3:거래금액순, 4:평균거래금액회전율
            fid_trgt_cls_code="111111111",  # 1 or 0 9자리
            fid_trgt_exls_cls_code="0000000000",  # 1 or 0 10자리
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_input_date_1=""  # 공란 입력
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_trading_volume_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_fluctuation_rank(client: Client):
    """Test stock fluctuation (rise/fall) ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_fluctuation_rank(
            fid_rsfl_rate2="",  # ~비율
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20170",
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200
            fid_rank_sort_cls_code="0",  # 0:상승율순, 1:하락율순, 2:시가대비상승율, 3:시가대비하락율, 4:변동율
            fid_input_cnt_1="0",  # 0:전체, 누적일수 입력
            fid_prc_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_div_cls_code="0",  # 0:전체
            fid_rsfl_rate1=""  # 비율~
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_fluctuation_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_hoga_quantity_rank(client: Client):
    """Test stock bid/ask quantity ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_hoga_quantity_rank(
            fid_vol_cnt="",  # 거래량~
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20172",
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200
            fid_rank_sort_cls_code="0",  # 0:순매수잔량순, 1:순매도잔량순, 2:매수비율순, 3:매도비율순
            fid_div_cls_code="0",  # 0:전체
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2=""  # ~가격
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_hoga_quantity_rank failed: {e}")


# ==================== Financial Indicator APIs ====================


@pytest.mark.integration
def test_get_stock_profitability_indicator_rank(client: Client):
    """Test stock profitability indicator ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_profitability_indicator_rank(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_trgt_cls_code="0",  # 0:전체
            fid_cond_scr_div_code="20173",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_div_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_input_option_1="2024",  # 회계연도
            fid_input_option_2="3",  # 0:1/4분기, 1:반기, 2:3/4분기, 3:결산
            fid_rank_sort_cls_code="0",  # 0:매출이익, 1:영업이익, 2:경상이익, 3:당기순이익, 4:자산총계, 5:부채총계, 6:자본총계
            fid_blng_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0"  # 0:전체
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_profitability_indicator_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_market_cap_top(client: Client):
    """Test stock market capitalization top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_market_cap_top(
            fid_input_price_2="",  # ~가격
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20174",
            fid_div_cls_code="0",  # 0:전체, 1:보통주, 2:우선주
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_vol_cnt=""  # 거래량~
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_market_cap_top failed: {e}")


@pytest.mark.integration
def test_get_stock_finance_ratio_rank(client: Client):
    """Test stock financial ratio ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_finance_ratio_rank(
            fid_trgt_cls_code="0",  # 0:전체
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20175",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_div_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_input_option_1="2024",  # 회계연도
            fid_input_option_2="3",  # 0:1/4분기, 1:반기, 2:3/4분기, 3:결산
            fid_rank_sort_cls_code="7",  # 7:수익성분석, 11:안정성분석, 15:성장성분석, 20:활동성분석
            fid_blng_cls_code="0",
            fid_trgt_exls_cls_code="0"  # 0:전체
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_finance_ratio_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_market_price_rank(client: Client):
    """Test stock market price (value) ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_market_price_rank(
            fid_trgt_cls_code="0",  # 0:전체
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20179",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_div_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_input_option_1="2024",  # 회계연도
            fid_input_option_2="3",  # 0:1/4분기, 1:반기, 2:3/4분기, 3:결산
            fid_rank_sort_cls_code="23",  # 23:PER, 24:PBR, 25:PCR, 26:PSR, 27:EPS, 28:EVA, 29:EBITDA, 30:EV/EBITDA, 31:EBITDA/금융비율
            fid_blng_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0"  # 0:전체
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_market_price_rank failed: {e}")


# ==================== After Hours Trading APIs ====================


@pytest.mark.integration
def test_get_stock_time_hoga_rank(client: Client):
    """Test stock after-hours bid/ask quantity ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_time_hoga_rank(
            fid_input_price_1="",  # 가격~
            fid_cond_mrkt_div_code="J",  # 주식 J
            fid_cond_scr_div_code="20176",
            fid_rank_sort_cls_code="1",  # 1:장전시간외, 2:장후시간외, 3:매도잔량, 4:매수잔량
            fid_div_cls_code="0",  # 0:전체
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_trgt_cls_code="0",  # 0:전체
            fid_vol_cnt="",  # 거래량~
            fid_input_price_2=""  # ~가격
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_time_hoga_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_after_hours_fluctuation_rank(client: Client):
    """Test stock after-hours fluctuation ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_after_hours_fluctuation_rank(
            fid_cond_mrkt_div_code="J",  # J:주식
            fid_mrkt_cls_code="",  # 공백 입력
            fid_cond_scr_div_code="20234",
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥
            fid_div_cls_code="2",  # 1:상한가, 2:상승률, 3:보합, 4:하한가, 5:하락률
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_trgt_cls_code="",  # 공백 입력
            fid_trgt_exls_cls_code=""  # 공백 입력
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_after_hours_fluctuation_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_after_hours_volume_rank(client: Client):
    """Test stock after-hours volume ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_after_hours_volume_rank(
            fid_cond_mrkt_div_code="J",  # J:주식
            fid_cond_scr_div_code="20235",
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥
            fid_rank_sort_cls_code="2",  # 0:매수잔량, 1:매도잔량, 2:거래량
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_trgt_cls_code="",  # 공백
            fid_trgt_exls_cls_code=""  # 공백
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_after_hours_volume_rank failed: {e}")


# ==================== Specialized Ranking APIs ====================


@pytest.mark.integration
def test_get_stock_preferred_stock_ratio_top(client: Client):
    """Test preferred stock ratio (disparity) top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_preferred_stock_ratio_top(
            fid_vol_cnt="",  # 거래량~
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20177",
            fid_div_cls_code="0",  # 0:전체
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2=""  # ~가격
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_preferred_stock_ratio_top failed: {e}")


@pytest.mark.integration
def test_get_stock_disparity_index_rank(client: Client):
    """Test stock disparity index ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_disparity_index_rank(
            fid_input_price_2="",  # ~가격
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20178",
            fid_div_cls_code="0",  # 0:전체
            fid_rank_sort_cls_code="0",  # 0:이격도상위순, 1:이격도하위순
            fid_hour_cls_code="5",  # 5:이격도5, 10:이격도10, 20:이격도20, 60:이격도60, 120:이격도120
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_vol_cnt=""  # 거래량~
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_disparity_index_rank failed: {e}")


@pytest.mark.integration
def test_get_stock_execution_strength_top(client: Client):
    """Test stock execution strength top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_execution_strength_top(
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20168",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_div_cls_code="0",  # 0:전체, 1:보통주, 2:우선주
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_trgt_cls_code="0"  # 0:전체
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_execution_strength_top failed: {e}")


@pytest.mark.integration
def test_get_stock_watchlist_registration_top(client: Client):
    """Test stock watchlist registration top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_watchlist_registration_top(
            fid_input_iscd_2="000000",  # 000000:필수입력값
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20180",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 가격~
            fid_input_price_2="",  # ~가격
            fid_vol_cnt="",  # 거래량~
            fid_div_cls_code="0",  # 0:전체
            fid_input_cnt_1="1"  # 순위검색 입력값, 1:1위부터, 10:10위부터
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_watchlist_registration_top failed: {e}")


@pytest.mark.integration
def test_get_stock_expected_execution_rise_decline_top(client: Client):
    """Test stock expected execution rise/decline top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_expected_execution_rise_decline_top(
            fid_rank_sort_cls_code="0",  # 0:상승률, 1:상승폭, 2:보합, 3:하락율, 4:하락폭, 5:체결량, 6:거래대금
            fid_cond_mrkt_div_code="J",  # 주식 J
            fid_cond_scr_div_code="20182",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_div_cls_code="0",  # 0:전체, 1:보통주, 2:우선주
            fid_aply_rang_prc_1="",  # 가격~
            fid_vol_cnt="",  # 거래량~
            fid_pbmn="",  # 거래대금~ 천원단위
            fid_blng_cls_code="0",  # 0:전체
            fid_mkop_cls_code="0"  # 0:장전예상, 1:장마감예상
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_expected_execution_rise_decline_top failed: {e}")


@pytest.mark.integration
def test_get_stock_proprietary_trading_top(client: Client):
    """Test stock proprietary trading top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_proprietary_trading_top(
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="20186",
            fid_div_cls_code="0",  # 0:전체
            fid_rank_sort_cls_code="1",  # 0:매도상위, 1:매수상위
            fid_input_date_1="20240701",  # 기간~
            fid_input_date_2="20250109",  # ~기간
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_trgt_cls_code="0",  # 0:전체
            fid_aply_rang_vol="0",  # 0:전체, 100:100주 이상
            fid_aply_rang_prc_2="",  # ~가격
            fid_aply_rang_prc_1=""  # 가격~
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_proprietary_trading_top failed: {e}")


@pytest.mark.integration
def test_get_stock_new_high_low_approaching_top(client: Client):
    """Test stock new high/low approaching top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_new_high_low_approaching_top(
            fid_aply_rang_vol="0",  # 0:전체, 100:100주 이상
            fid_cond_mrkt_div_code="J",  # 주식 J
            fid_cond_scr_div_code="20187",
            fid_div_cls_code="0",  # 0:전체
            fid_input_cnt_1="0",  # 괴리율 최소
            fid_input_cnt_2="100",  # 괴리율 최대
            fid_prc_cls_code="0",  # 0:신고근접, 1:신저근접
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_trgt_cls_code="0",  # 0:전체
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_aply_rang_prc_1="",  # 가격~
            fid_aply_rang_prc_2=""  # ~가격
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_new_high_low_approaching_top failed: {e}")


@pytest.mark.integration
def test_get_stock_dividend_yield_top(client: Client):
    """Test stock dividend yield top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_dividend_yield_top(
            cts_area="",  # 공백
            gb1="1",  # 0:전체, 1:코스피, 2:코스피200, 3:코스닥
            upjong="0001",  # 코스피: 0001:종합, 0002:대형주..0027:제조업, 코스닥: 1001:종합..1041:IT부품
            gb2="0",  # 0:전체, 6:보통주, 7:우선주
            gb3="2",  # 1:주식배당, 2:현금배당
            f_dt="20240101",  # 기준일From (YYYYMMDD)
            t_dt="20241231",  # 기준일To (YYYYMMDD)
            gb4="0"  # 0:전체, 1:결산배당, 2:중간배당
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_dividend_yield_top failed: {e}")


@pytest.mark.integration
def test_get_stock_large_execution_count_top(client: Client):
    """Test stock large execution count top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_large_execution_count_top(
            fid_aply_rang_prc_2="",  # ~가격
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT
            fid_cond_scr_div_code="11909",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200, 4001:KRX100
            fid_rank_sort_cls_code="0",  # 0:매수상위, 1:매도상위
            fid_div_cls_code="0",  # 0:전체
            fid_input_price_1="",  # 건별금액~
            fid_aply_rang_prc_1="",  # 가격~
            fid_input_iscd_2="",  # 공백:전체종목, 개별종목 조회시 종목코드
            fid_trgt_exls_cls_code="0",  # 0:전체
            fid_trgt_cls_code="0",  # 0:전체
            fid_vol_cnt=""  # 거래량~
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_large_execution_count_top failed: {e}")


@pytest.mark.integration
def test_get_stock_credit_balance_top(client: Client):
    """Test stock credit balance top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_credit_balance_top(
            fid_cond_scr_div_code="11701",
            fid_input_iscd="0001",  # 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
            fid_option="7",  # 증가율기간 (2~999)
            fid_cond_mrkt_div_code="J",  # 주식 J
            fid_rank_sort_cls_code="0"  # 융자: 0:잔고비율상위, 1:잔고수량상위, 2:잔고금액상위, 3:잔고비율증가상위, 4:잔고비율감소상위
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_credit_balance_top failed: {e}")


@pytest.mark.integration
def test_get_stock_short_selling_top(client: Client):
    """Test stock short selling top ranking."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_stock_short_selling_top(
            fid_aply_rang_vol="",  # 공백
            fid_cond_mrkt_div_code="J",  # 주식 J
            fid_cond_scr_div_code="20482",
            fid_input_iscd="0001",  # 0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001:KRX100, 3003:코스닥150
            fid_period_div_code="D",  # D:일, M:월
            fid_input_cnt_1="0",  # 조회기간(일수) D: 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, M: 1:1개월, 2:2개월, 3:3개월
            fid_trgt_exls_cls_code="",  # 공백
            fid_trgt_cls_code="",  # 공백
            fid_aply_rang_prc_1="",  # 가격~
            fid_aply_rang_prc_2=""  # ~가격
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_short_selling_top failed: {e}")


@pytest.mark.integration
def test_get_hts_inquiry_top_20(client: Client):
    """Test HTS inquiry top 20 stocks."""
    time.sleep(1)
    try:
        response = client.domestic_ranking_analysis.get_hts_inquiry_top_20()

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_hts_inquiry_top_20 failed: {e}")
