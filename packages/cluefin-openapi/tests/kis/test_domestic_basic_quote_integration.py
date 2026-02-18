"""Integration tests for the KIS domestic basic quote module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import pytest

from cluefin_openapi.kis._http_client import HttpClient

# ==================== Stock Current Price APIs ====================


@pytest.mark.integration
def test_get_stock_current_price(client: HttpClient):
    """Test basic stock current price inquiry (Samsung Electronics)."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")

    except Exception as e:
        pytest.fail(f"get_stock_current_price failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_2(client: HttpClient):
    """Test alternative stock current price endpoint (Kakao)."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_2(
            fid_cond_mrkt_div_code="J", fid_input_iscd="035720"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_2 failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_conclusion(client: HttpClient):
    """Test stock current price conclusion with execution info."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_daily(client: HttpClient):
    """Test stock current price daily/weekly/monthly quotes."""
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
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_daily failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_asking_expected_conclusion(client: HttpClient):
    """Test stock current price bid/ask and expected execution."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_asking_expected_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_asking_expected_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_investor(client: HttpClient):
    """Test stock current price investor trading information."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_investor(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_investor failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_member(client: HttpClient):
    """Test stock current price member firm trading information."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_member(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_member failed: {e}")


# ==================== Time Series & Chart APIs ====================


@pytest.mark.integration
def test_get_stock_period_quote(client: HttpClient):
    """Test stock period quote (daily/weekly/monthly/yearly)."""
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
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_period_quote failed: {e}")


@pytest.mark.integration
def test_get_stock_today_minute_chart(client: HttpClient):
    """Test stock today's minute chart."""
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
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_today_minute_chart failed: {e}")


@pytest.mark.integration
def test_get_stock_daily_minute_chart(client: HttpClient):
    """Test stock daily minute chart."""
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
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_daily_minute_chart failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_time_item_conclusion(client: HttpClient):
    """Test stock current price intraday time-based execution."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_time_item_conclusion(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930", fid_input_hour_1="090000"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_time_item_conclusion failed: {e}")


# ==================== Overtime Trading APIs ====================


@pytest.mark.integration
def test_get_stock_current_price_daily_overtime_price(client: HttpClient):
    """Test stock current price daily overtime prices."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_daily_overtime_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_daily_overtime_price failed: {e}")


@pytest.mark.integration
def test_get_stock_current_price_overtime_conclusion(client: HttpClient):
    """Test stock current price overtime execution by time."""
    try:
        response = client.domestic_basic_quote.get_stock_current_price_overtime_conclusion(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_current_price_overtime_conclusion failed: {e}")


@pytest.mark.integration
def test_get_stock_overtime_current_price(client: HttpClient):
    """Test stock overtime current price."""
    try:
        response = client.domestic_basic_quote.get_stock_overtime_current_price(
            fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_overtime_current_price failed: {e}")


@pytest.mark.integration
def test_get_stock_overtime_asking_price(client: HttpClient):
    """Test stock overtime bid/ask prices."""
    try:
        response = client.domestic_basic_quote.get_stock_overtime_asking_price(
            fid_input_iscd="005930", fid_cond_mrkt_div_code="J"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_overtime_asking_price failed: {e}")


# ==================== Market-wide APIs ====================


@pytest.mark.integration
def test_get_stock_closing_expected_price(client: HttpClient):
    """Test market closing expected prices."""
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
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_closing_expected_price failed: {e}")


# ==================== ETF/ETN APIs ====================


@pytest.mark.integration
def test_get_etfetn_current_price(client: HttpClient):
    """Test ETF/ETN current price (KODEX 200)."""
    try:
        response = client.domestic_basic_quote.get_etfetn_current_price(
            fid_input_iscd="069500", fid_cond_mrkt_div_code="J"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etfetn_current_price failed: {e}")


@pytest.mark.integration
def test_get_etf_component_stock_price(client: HttpClient):
    """Test ETF component stock prices (KODEX 200)."""
    try:
        response = client.domestic_basic_quote.get_etf_component_stock_price(
            fid_input_iscd="069500", fid_cond_mrkt_div_code="J", fid_cond_scr_div_code="11216"
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_component_stock_price failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_trend(client: HttpClient):
    """Test ETF NAV comparison trend at stock level."""
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_trend(
            fid_input_iscd="069500",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_trend failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_daily_trend(client: HttpClient):
    """Test ETF NAV comparison daily trend."""
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_daily_trend(
            fid_input_iscd="069500",
            fid_input_date_1="20240701",
            fid_input_date_2="20240731",
            fid_cond_mrkt_div_code="J",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_daily_trend failed: {e}")


@pytest.mark.integration
def test_get_etf_nav_comparison_time_trend(client: HttpClient):
    """Test ETF NAV comparison time (minute) trend."""
    try:
        response = client.domestic_basic_quote.get_etf_nav_comparison_time_trend(
            fid_hour_cls_code="60",
            fid_input_iscd="069500",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_etf_nav_comparison_time_trend failed: {e}")
