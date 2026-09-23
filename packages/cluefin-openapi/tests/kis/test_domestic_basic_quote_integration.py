"""Integration tests for the KIS domestic basic quote module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import pytest

from cluefin_openapi.kis._http_client import HttpClient

# ==================== Stock Current Price APIs ====================


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "fid_input_iscd"),
    [
        ("get_stock_current_price", "005930"),  # Samsung Electronics
        ("get_stock_current_price_2", "035720"),  # Kakao
    ],
)
def test_get_stock_current_price_variants(client: HttpClient, method_name: str, fid_input_iscd: str):
    """Test stock current price inquiry across both current-price endpoints."""
    response = getattr(client.domestic_basic_quote, method_name)(
        fid_cond_mrkt_div_code="J", fid_input_iscd=fid_input_iscd
    )

    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_current_price_conclusion(client: HttpClient):
    """Test stock current price conclusion with execution info."""
    response = client.domestic_basic_quote.get_stock_current_price_conclusion(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_current_price_daily(client: HttpClient):
    """Test stock current price daily/weekly/monthly quotes."""
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


@pytest.mark.integration
def test_get_stock_current_price_asking_expected_conclusion(client: HttpClient):
    """Test stock current price bid/ask and expected execution."""
    response = client.domestic_basic_quote.get_stock_current_price_asking_expected_conclusion(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_current_price_investor(client: HttpClient):
    """Test stock current price investor trading information."""
    response = client.domestic_basic_quote.get_stock_current_price_investor(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_current_price_member(client: HttpClient):
    """Test stock current price member firm trading information."""
    response = client.domestic_basic_quote.get_stock_current_price_member(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


# ==================== Time Series & Chart APIs ====================


@pytest.mark.integration
def test_get_stock_period_quote(client: HttpClient):
    """Test stock period quote (daily/weekly/monthly/yearly)."""
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


@pytest.mark.integration
def test_get_stock_today_minute_chart(client: HttpClient):
    """Test stock today's minute chart."""
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


@pytest.mark.integration
def test_get_stock_daily_minute_chart(client: HttpClient):
    """Test stock daily minute chart."""
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


@pytest.mark.integration
def test_get_stock_current_price_time_item_conclusion(client: HttpClient):
    """Test stock current price intraday time-based execution."""
    response = client.domestic_basic_quote.get_stock_current_price_time_item_conclusion(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930", fid_input_hour_1="090000"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


# ==================== Overtime Trading APIs ====================


@pytest.mark.integration
def test_get_stock_current_price_daily_overtime_price(client: HttpClient):
    """Test stock current price daily overtime prices."""
    response = client.domestic_basic_quote.get_stock_current_price_daily_overtime_price(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_current_price_overtime_conclusion(client: HttpClient):
    """Test stock current price overtime execution by time."""
    response = client.domestic_basic_quote.get_stock_current_price_overtime_conclusion(
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930",
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_overtime_current_price(client: HttpClient):
    """Test stock overtime current price."""
    response = client.domestic_basic_quote.get_stock_overtime_current_price(
        fid_cond_mrkt_div_code="J", fid_input_iscd="005930"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_stock_overtime_asking_price(client: HttpClient):
    """Test stock overtime bid/ask prices."""
    response = client.domestic_basic_quote.get_stock_overtime_asking_price(
        fid_input_iscd="005930", fid_cond_mrkt_div_code="J"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


# ==================== Market-wide APIs ====================


@pytest.mark.integration
def test_get_stock_closing_expected_price(client: HttpClient):
    """Test market closing expected prices."""
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


# ==================== ETF/ETN APIs ====================


@pytest.mark.integration
def test_get_etfetn_current_price(client: HttpClient):
    """Test ETF/ETN current price (KODEX 200)."""
    response = client.domestic_basic_quote.get_etfetn_current_price(fid_input_iscd="069500", fid_cond_mrkt_div_code="J")

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_etf_component_stock_price(client: HttpClient):
    """Test ETF component stock prices (KODEX 200)."""
    response = client.domestic_basic_quote.get_etf_component_stock_price(
        fid_input_iscd="069500", fid_cond_mrkt_div_code="J", fid_cond_scr_div_code="11216"
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_etf_nav_comparison_trend(client: HttpClient):
    """Test ETF NAV comparison trend at stock level."""
    response = client.domestic_basic_quote.get_etf_nav_comparison_trend(
        fid_input_iscd="069500",
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")


@pytest.mark.integration
def test_get_etf_nav_comparison_daily_trend(client: HttpClient):
    """Test ETF NAV comparison daily trend."""
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


@pytest.mark.integration
def test_get_etf_nav_comparison_time_trend(client: HttpClient):
    """Test ETF NAV comparison time (minute) trend."""
    response = client.domestic_basic_quote.get_etf_nav_comparison_time_trend(
        fid_hour_cls_code="60",
        fid_input_iscd="069500",
    )

    # Verify response type
    assert response is not None
    assert hasattr(response.body, "rt_cd")
    assert hasattr(response.body, "msg_cd")
