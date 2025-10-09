"""Integration tests for the KIS domestic basic quote module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import os
import time
from typing import Literal, cast

import dotenv
import pytest
from _token_cache import TokenCache
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._client import Client


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


# ==================== Stock Current Price APIs ====================


@pytest.mark.integration
def test_get_stock_current_price(client: Client):
    """Test basic stock current price inquiry (Samsung Electronics)."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")
        assert hasattr(response, "msg1")

    except Exception as e:
        pytest.fail(f"get_stock_current_price failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_2(client: Client):
    """Test alternative stock current price endpoint (Kakao)."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_2(
            fid_cond_mrkt_div_code="J", fid_input_iscd="035720"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_2 failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_conclusion(client: Client):
    """Test stock current price conclusion with execution info."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_daily(client: Client):
    """Test stock current price daily/weekly/monthly quotes."""
    time.sleep(1)
    try:
        # Test daily quotes
        response = client.domestic_basic_quote.get_stock_current_price_daily(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
            fid_period_div_code="D",
            fid_org_adj_prc="0",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_daily failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_asking_expected_conclusion(client: Client):
    """Test stock current price bid/ask and expected execution."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_asking_expected_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_asking_expected_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_investor(client: Client):
    """Test stock current price investor trading information."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_investor(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_investor failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_member(client: Client):
    """Test stock current price member firm trading information."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_member(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_member failed: {e}")


# ==================== Time Series & Chart APIs ====================


@pytest.mark.integration
def test_get_stock_period_quote(client: Client):
    """Test stock period quote (daily/weekly/monthly/yearly)."""
    time.sleep(1)
    try:
        # Test daily period quotes for the last 30 days
        response = client.domestic_basic_quote.get_stock_period_quote(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
            fid_input_date_1="20240701",
            fid_input_date_2="20240731",
            fid_period_div_code="D",
            fid_org_adj_prc="0",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_period_quote failed: {e}")


@pytest.mark.integration
def test_get_stock_today_minute_chart(client: Client):
    """Test stock today's minute chart."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_today_minute_chart(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
            fid_input_hour_1="090000",
            fid_pw_data_incu_yn="Y",
            fid_etc_cls_code="",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_today_minute_chart failed: {e}")


@pytest.mark.integration
def test_get_stock_daily_minute_chart(client: Client):
    """Test stock daily minute chart."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_daily_minute_chart(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
            fid_input_hour_1="153000",
            fid_input_date_1="20240701",
            fid_pw_data_incu_yn="Y",
            fid_fake_tick_incu_yn="",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_daily_minute_chart failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_time_item_conclusion(client: Client):
    """Test stock current price intraday time-based execution."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_time_item_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930", fid_input_hour_1="090000"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_time_item_conclusion failed: {e}")


# ==================== Overtime Trading APIs ====================


@pytest.mark.integration
def test_get_stock_current_price_daily_overtime_price(client: Client):
    """Test stock current price daily overtime prices."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_daily_overtime_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_daily_overtime_price failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_overtime_conclusion(client: Client):
    """Test stock current price overtime execution by time."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_current_price_overtime_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930", fid_input_hour_1="080000"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_overtime_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_overtime_current_price(client: Client):
    """Test stock overtime current price."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_overtime_current_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_overtime_current_price failed: {e}")


@pytest.mark.integration
def test_get_stock_overtime_asking_price(client: Client):
    """Test stock overtime bid/ask prices."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_overtime_asking_price(
            fid_input_iscd="005930", fid_cond_mrkt_div_code="J"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_overtime_asking_price failed: {e}")


# ==================== Market-wide APIs ====================


@pytest.mark.integration
def test_get_stock_closing_expected_price(client: Client):
    """Test market closing expected prices."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_stock_closing_expected_price(
            fid_rank_sort_cls_code="0",
            fid_input_iscd="0000",
            fid_blng_cls_code="0",
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="11173",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_closing_expected_price failed: {e}")


# ==================== ETF/ETN APIs ====================


@pytest.mark.integration
def test_get_etfetn_current_price(client: Client):
    """Test ETF/ETN current price (KODEX 200)."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_etfetn_current_price(
            fid_input_iscd="069500", fid_cond_mrkt_div_code="J"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etfetn_current_price failed: {e}")


@pytest.mark.integration
def test_get_etf_component_stock_price(client: Client):
    """Test ETF component stock prices (KODEX 200)."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_etf_component_stock_price(
            fid_input_iscd="069500", fid_cond_mrkt_div_code="J", fid_cond_scr_div_code="11216"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_component_stock_price failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_trend(client: Client):
    """Test ETF NAV comparison trend at stock level."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_trend(
            fid_input_iscd="069500",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_trend failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_daily_trend(client: Client):
    """Test ETF NAV comparison daily trend."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_daily_trend(
            fid_input_iscd="069500",
            fid_input_date_1="20240701",
            fid_input_date_2="20240731",
            fid_cond_mrkt_div_code="J",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_daily_trend failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_time_trend(client: Client):
    """Test ETF NAV comparison time (minute) trend."""
    time.sleep(1)
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_time_trend(
            fid_hour_cls_code="60",
            fid_input_iscd="069500",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response, "rt_cd")
        assert hasattr(response, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_time_trend failed: {e}")
