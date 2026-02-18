"""Integration tests for the KIS domestic market analysis module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import os

import pytest

from cluefin_openapi.kis._http_client import HttpClient

# ==================== Condition Search APIs ====================


@pytest.mark.integration
def test_get_condition_search_list(client: HttpClient):
    """Test condition search list inquiry."""
    try:
        # Note: This requires a valid HTS ID with saved conditions
        response = client.domestic_market_analysis.get_condition_search_list(
            user_id="test_user"  # Replace with actual HTS ID if testing
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        # This may fail if user_id doesn't have saved conditions
        pytest.skip(f"get_condition_search_list requires valid HTS ID: {e}")


@pytest.mark.integration
def test_get_condition_search_result(client: HttpClient):
    """Test condition search result inquiry."""
    try:
        # Note: This requires a valid HTS ID and seq from condition list
        response = client.domestic_market_analysis.get_condition_search_result(
            user_id="test_user",  # Replace with actual HTS ID
            seq="0",  # First condition
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        # This may fail if user_id doesn't have saved conditions
        pytest.skip(f"get_condition_search_result requires valid HTS ID and seq: {e}")


# ==================== Watchlist APIs ====================


@pytest.mark.integration
def test_get_watchlist_groups(client: HttpClient):
    """Test watchlist groups inquiry."""
    # Get user ID from environment variable, fallback to "test_user"
    user_id = os.getenv("KIS_HTS_USER_ID", "test_user")

    try:
        response = client.domestic_market_analysis.get_watchlist_groups(
            interest_type="1",  # Unique key: 1
            fid_etc_cls_code="00",  # Unique key: 00
            user_id=user_id,  # Use environment variable or fallback
        )

        # Verify response type
        assert response is not None
        assert response.body.rt_cd == "0"

    except Exception as e:
        # This may fail if user_id doesn't have watchlists
        pytest.skip(f"get_watchlist_groups requires valid HTS ID: {e}")


@pytest.mark.integration
def test_get_watchlist_multi_quote(client: HttpClient):
    """Test watchlist multi-stock quote inquiry."""
    try:
        # Query for Samsung Electronics (005930) only, rest are empty
        response = client.domestic_market_analysis.get_watchlist_multi_quote(
            fid_cond_mrkt_div_code_1="J",
            fid_input_iscd_1="005930",  # Samsung Electronics
            fid_cond_mrkt_div_code_2="",
            fid_input_iscd_2="",
            fid_cond_mrkt_div_code_3="",
            fid_input_iscd_3="",
            fid_cond_mrkt_div_code_4="",
            fid_input_iscd_4="",
            fid_cond_mrkt_div_code_5="",
            fid_input_iscd_5="",
            fid_cond_mrkt_div_code_6="",
            fid_input_iscd_6="",
            fid_cond_mrkt_div_code_7="",
            fid_input_iscd_7="",
            fid_cond_mrkt_div_code_8="",
            fid_input_iscd_8="",
            fid_cond_mrkt_div_code_9="",
            fid_input_iscd_9="",
            fid_cond_mrkt_div_code_10="",
            fid_input_iscd_10="",
            fid_cond_mrkt_div_code_11="",
            fid_input_iscd_11="",
            fid_cond_mrkt_div_code_12="",
            fid_input_iscd_12="",
            fid_cond_mrkt_div_code_13="",
            fid_input_iscd_13="",
            fid_cond_mrkt_div_code_14="",
            fid_input_iscd_14="",
            fid_cond_mrkt_div_code_15="",
            fid_input_iscd_15="",
            fid_cond_mrkt_div_code_16="",
            fid_input_iscd_16="",
            fid_cond_mrkt_div_code_17="",
            fid_input_iscd_17="",
            fid_cond_mrkt_div_code_18="",
            fid_input_iscd_18="",
            fid_cond_mrkt_div_code_19="",
            fid_input_iscd_19="",
            fid_cond_mrkt_div_code_20="",
            fid_input_iscd_20="",
            fid_cond_mrkt_div_code_21="",
            fid_input_iscd_21="",
            fid_cond_mrkt_div_code_22="",
            fid_input_iscd_22="",
            fid_cond_mrkt_div_code_23="",
            fid_input_iscd_23="",
            fid_cond_mrkt_div_code_24="",
            fid_input_iscd_24="",
            fid_cond_mrkt_div_code_25="",
            fid_input_iscd_25="",
            fid_cond_mrkt_div_code_26="",
            fid_input_iscd_26="",
            fid_cond_mrkt_div_code_27="",
            fid_input_iscd_27="",
            fid_cond_mrkt_div_code_28="",
            fid_input_iscd_28="",
            fid_cond_mrkt_div_code_29="",
            fid_input_iscd_29="",
            fid_cond_mrkt_div_code_30="",
            fid_input_iscd_30="",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_watchlist_multi_quote failed: {e}")


# ==================== Investor Trading Trend APIs ====================


@pytest.mark.integration
def test_get_investor_trading_trend_by_stock_daily(client: HttpClient):
    """Test investor trading trend by stock (daily)."""
    try:
        response = client.domestic_market_analysis.get_investor_trading_trend_by_stock_daily(
            fid_cond_mrkt_div_code="J",  # Market: J
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1="20251001",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_investor_trading_trend_by_stock_daily failed: {e}")


@pytest.mark.integration
def test_get_investor_trading_trend_by_market_intraday(client: HttpClient):
    """Test investor trading trend by market (intraday)."""
    try:
        response = client.domestic_market_analysis.get_investor_trading_trend_by_market_intraday(
            fid_input_iscd="KSP",  # KSP:KOSPI, KSQ:KOSDAQ
            fid_input_iscd_2="0001",  # Sector code (0001:KOSPI Total)
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_investor_trading_trend_by_market_intraday failed: {e}")


@pytest.mark.integration
def test_get_investor_trading_trend_by_market_daily(client: HttpClient):
    """Test investor trading trend by market (daily)."""
    try:
        response = client.domestic_market_analysis.get_investor_trading_trend_by_market_daily(
            fid_cond_mrkt_div_code="U",  # U:Sector
            fid_input_iscd="0001",  # Sector classification code
            fid_input_date_1="20240701",  # Date
            fid_input_iscd_1="KSP",  # KSP:KOSPI, KSQ:KOSDAQ
            fid_input_date_2="20240701",  # Same as date_1
            fid_input_iscd_2="0001",  # Sector classification code
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_investor_trading_trend_by_market_daily failed: {e}")


# ==================== Foreign/Member Trading APIs ====================


@pytest.mark.integration
def test_get_foreign_brokerage_trading_aggregate(client: HttpClient):
    """Test foreign brokerage trading aggregate."""
    try:
        response = client.domestic_market_analysis.get_foreign_brokerage_trading_aggregate(
            fid_input_iscd="0000",  # 0000:All, 0001:KOSPI, 1001:KOSDAQ
            fid_rank_sort_cls_code="0",  # 0:Net buy, 1:Net sell
            fid_rank_sort_cls_code_2="0",
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_foreign_brokerage_trading_aggregate failed: {e}")


@pytest.mark.integration
def test_get_foreign_net_buy_trend_by_stock(client: HttpClient):
    """Test foreign net buy trend by stock."""
    try:
        response = client.domestic_market_analysis.get_foreign_net_buy_trend_by_stock(
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_iscd_2="99999",  # 99999:All foreign brokerages
            fid_cond_mrkt_div_code="J",  # J:KRX
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_foreign_net_buy_trend_by_stock failed: {e}")


@pytest.mark.integration
def test_get_member_trading_trend_tick(client: HttpClient):
    """Test member trading trend (tick)."""
    try:
        response = client.domestic_market_analysis.get_member_trading_trend_tick(
            fid_cond_scr_div_code="20432",  # Primary key
            fid_cond_mrkt_div_code="J",  # J:Fixed
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_iscd_2="99999",  # 99999:All members
            fid_mrkt_cls_code="",  # Empty when using fid_input_iscd
            fid_vol_cnt="",  # Empty for all volumes
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_member_trading_trend_tick failed: {e}")


@pytest.mark.integration
def test_get_member_trading_trend_by_stock(client: HttpClient):
    """Test member trading trend by stock."""
    try:
        response = client.domestic_market_analysis.get_member_trading_trend_by_stock(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_iscd_2="",  # Member code (empty for all)
            fid_input_date_1="20240701",  # From date
            fid_input_date_2="20240731",  # To date
            fid_sctn_cls_code="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_member_trading_trend_by_stock failed: {e}")


@pytest.mark.integration
def test_get_foreign_institutional_estimate_by_stock(client: HttpClient):
    """Test foreign/institutional estimate by stock."""
    try:
        response = client.domestic_market_analysis.get_foreign_institutional_estimate_by_stock(
            mksc_shrn_iscd="005930"  # Samsung Electronics
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_foreign_institutional_estimate_by_stock failed: {e}")


# ==================== Program Trading APIs ====================


@pytest.mark.integration
def test_get_program_trading_trend_by_stock_intraday(client: HttpClient):
    """Test program trading trend by stock (intraday)."""
    try:
        response = client.domestic_market_analysis.get_program_trading_trend_by_stock_intraday(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_input_iscd="005930",  # Samsung Electronics
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_program_trading_trend_by_stock_intraday failed: {e}")


@pytest.mark.integration
def test_get_program_trading_trend_by_stock_daily(client: HttpClient):
    """Test program trading trend by stock (daily)."""
    try:
        response = client.domestic_market_analysis.get_program_trading_trend_by_stock_daily(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1="",  # Empty for today
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_program_trading_trend_by_stock_daily failed: {e}")


@pytest.mark.integration
def test_get_program_trading_summary_intraday(client: HttpClient):
    """Test program trading summary (intraday)."""
    try:
        response = client.domestic_market_analysis.get_program_trading_summary_intraday(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_mrkt_cls_code="K",  # K:KOSPI, Q:KOSDAQ
            fid_sctn_cls_code="",  # Empty
            fid_input_iscd="",  # Empty
            fid_cond_mrkt_div_code1="",  # Empty
            fid_input_hour_1="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_program_trading_summary_intraday failed: {e}")


@pytest.mark.integration
def test_get_program_trading_summary_daily(client: HttpClient):
    """Test program trading summary (daily)."""
    try:
        response = client.domestic_market_analysis.get_program_trading_summary_daily(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_mrkt_cls_code="K",  # K:KOSPI, Q:KOSDAQ
            fid_input_date_1="",  # Empty (8 months max)
            fid_input_date_2="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_program_trading_summary_daily failed: {e}")


@pytest.mark.integration
def test_get_program_trading_investor_trend_today(client: HttpClient):
    """Test program trading investor trend (today)."""
    try:
        response = client.domestic_market_analysis.get_program_trading_investor_trend_today(
            exch_div_cls_code="J",  # J:KRX, NX:NXT, UN:Integrated
            mrkt_div_cls_code="1",  # 1:KOSPI, 4:KOSDAQ
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_program_trading_investor_trend_today failed: {e}")


# ==================== Market Analysis APIs ====================


@pytest.mark.integration
def test_get_buy_sell_volume_by_stock_daily(client: HttpClient):
    """Test buy/sell volume by stock (daily)."""
    try:
        response = client.domestic_market_analysis.get_buy_sell_volume_by_stock_daily(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1="20240701",  # From date
            fid_input_date_2="20240731",  # To date
            fid_period_div_code="D",  # D:Daily
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_buy_sell_volume_by_stock_daily failed: {e}")


@pytest.mark.integration
def test_get_credit_balance_trend_daily(client: HttpClient):
    """Test credit balance trend (daily)."""
    try:
        response = client.domestic_market_analysis.get_credit_balance_trend_daily(
            fid_cond_mrkt_div_code="J",  # J:Stock
            fid_cond_scr_div_code="20476",  # Unique key
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1="20240701",  # Settlement date
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_credit_balance_trend_daily failed: {e}")


@pytest.mark.integration
def test_get_expected_price_trend(client: HttpClient):
    """Test expected price trend."""
    try:
        response = client.domestic_market_analysis.get_expected_price_trend(
            fid_mkop_cls_code="0",  # 0:All, 4:Exclude zero volume
            fid_cond_mrkt_div_code="J",  # J:Stock
            fid_input_iscd="005930",  # Samsung Electronics
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_expected_price_trend failed: {e}")


@pytest.mark.integration
def test_get_short_selling_trend_daily(client: HttpClient):
    """Test short selling trend (daily)."""
    try:
        response = client.domestic_market_analysis.get_short_selling_trend_daily(
            fid_input_date_2="20240731",  # To date
            fid_cond_mrkt_div_code="J",  # J:Stock
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1="20240701",  # From date
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_short_selling_trend_daily failed: {e}")


@pytest.mark.integration
def test_get_after_hours_expected_fluctuation(client: HttpClient):
    """Test after hours expected fluctuation."""
    try:
        response = client.domestic_market_analysis.get_after_hours_expected_fluctuation(
            fid_cond_mrkt_div_code="J",  # J:Stock
            fid_cond_scr_div_code="11186",  # Unique key
            fid_input_iscd="0000",  # 0000:All, 0001:KOSPI, 1001:KOSDAQ
            fid_rank_sort_cls_code="0",  # 0:Rise rate, 1:Rise amount, etc.
            fid_div_cls_code="0",  # 0:All, 1:Managed, etc.
            fid_input_price_1="",  # Empty
            fid_input_price_2="",  # Empty
            fid_input_vol_1="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_after_hours_expected_fluctuation failed: {e}")


@pytest.mark.integration
def test_get_trading_weight_by_amount(client: HttpClient):
    """Test trading weight by amount."""
    try:
        response = client.domestic_market_analysis.get_trading_weight_by_amount(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_cond_scr_div_code="11119",  # Unique key
            fid_input_iscd="005930",  # Samsung Electronics
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_trading_weight_by_amount failed: {e}")


@pytest.mark.integration
def test_get_market_fund_summary(client: HttpClient):
    """Test market fund summary."""
    try:
        response = client.domestic_market_analysis.get_market_fund_summary(
            fid_input_date_1="20240701"  # Date
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_market_fund_summary failed: {e}")


@pytest.mark.integration
def test_get_stock_loan_trend_daily(client: HttpClient):
    """Test stock loan trend (daily)."""
    try:
        response = client.domestic_market_analysis.get_stock_loan_trend_daily(
            mrkt_div_cls_code="3",  # 1:KOSPI, 2:KOSDAQ, 3:Stock
            mksc_shrn_iscd="005930",  # Samsung Electronics
            start_date="20240701",  # From date
            end_date="20240731",  # To date
            cts="",  # Empty for first call
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_stock_loan_trend_daily failed: {e}")


@pytest.mark.integration
def test_get_limit_price_stocks(client: HttpClient):
    """Test limit price stocks (upper/lower limit)."""
    try:
        response = client.domestic_market_analysis.get_limit_price_stocks(
            fid_cond_mrkt_div_code="J",  # J:Market
            fid_cond_scr_div_code="11300",  # Unique key
            fid_prc_cls_code="0",  # 0:Upper, 1:Lower
            fid_div_cls_code="0",  # 0:At limit, 1-6:Near limit percentages
            fid_input_iscd="0000",  # 0000:All, 0001:KOSPI, 1001:KOSDAQ
            fid_trgt_cls_code="",  # Empty
            fid_trgt_exls_cls_code="",  # Empty
            fid_input_price_1="",  # Empty
            fid_input_price_2="",  # Empty
            fid_vol_cnt="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_limit_price_stocks failed: {e}")


@pytest.mark.integration
def test_get_resistance_level_trading_weight(client: HttpClient):
    """Test resistance level trading weight."""
    try:
        response = client.domestic_market_analysis.get_resistance_level_trading_weight(
            fid_cond_mrkt_div_code="J",  # J:KRX, NX:NXT, UN:Integrated
            fid_input_iscd="005930",  # Samsung Electronics
            fid_cond_scr_div_code="20113",  # Unique key
            fid_input_hour_1="",  # Empty
        )

        # Verify response type
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")

    except Exception as e:
        pytest.fail(f"get_resistance_level_trading_weight failed: {e}")
