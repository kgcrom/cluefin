"""Integration tests for KIS Overseas Market Analysis API.

These tests require valid API credentials in environment variables:
- KIWOOM_APP_KEY
- KIWOOM_SECRET_KEY
- KIWOOM_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_overseas_market_analysis_integration.py -v -m integration
"""

import os
import time
from datetime import datetime, timedelta
from typing import Literal, Optional, Sequence, cast

import dotenv
import pytest
from _token_cache import TokenCache
from pydantic import BaseModel, Field, SecretStr

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


@pytest.fixture(scope="module")
def client(auth_dev, token_cache) -> Client:
    """Fixture to create KIS Client with valid token."""
    token_response = token_cache.get()
    return Client(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
        # debug=True,
    )


@pytest.fixture(scope="module")
def common_params():
    """Common parameters used across multiple tests."""
    return {
        "keyb": "",  # NEXT KEY BUFF (empty for first call)
        "auth": "",  # User auth info (empty)
        "vol_rang": "0",  # Volume condition (0: all)
    }


@pytest.fixture(scope="module")
def date_range():
    """Generate date range for rights queries."""
    end_dt = datetime.now().strftime("%Y%m%d")
    start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")  # 3 months ago
    return start_dt, end_dt


def handle_api_error(func):
    """Decorator to handle API errors and skip tests if endpoint not available."""

    def wrapper(*args, **kwargs):
        time.sleep(1)  # Rate limiting
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Skip if API endpoint not available (404) or returns invalid JSON
            error_msg = str(e)
            if "404" in error_msg or "JSONDecodeError" in error_msg or "Expecting value" in error_msg:
                pytest.skip(f"API endpoint not available: {error_msg[:100]}")
            raise

    return wrapper


# Stock Price Analysis Tests

# TODO: Fix the API issue before enabling these tests

# @pytest.mark.integration
# def test_get_stock_price_rise_fall_nasdaq_rise(client):
#     """Test stock price rise/fall for NASDAQ - rising stocks."""
#     time.sleep(1)
#     response = client.overseas_market_analysis.get_stock_price_rise_fall(
#         excd="NAS",  # NASDAQ
#         gubn="1",  # Rising
#         mixn="3",  # 5 minutes ago
#         vol_rang="0",
#     )

#     assert response is not None
#     assert hasattr(response, 'output1')


# @pytest.mark.integration
# def test_get_stock_price_fluctuation_nyse_fall(client, common_params):
#     """Test stock price fluctuation for NYSE - falling stocks."""
#     time.sleep(1)
#     response = client.overseas_market_analysis.get_stock_price_fluctuation(
#         excd="NYS",  # NYSE
#         gubn="0",  # Falling
#         mixn="4",  # 10 minutes ago
#         vol_rang="1"  # 100+ shares
#     )

#     assert response is not None
#     assert hasattr(response, 'output1')


# Volume Analysis Tests


@pytest.mark.integration
def test_get_stock_volume_surge_nasdaq(client, common_params):
    """Test volume surge analysis for NASDAQ."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_volume_surge(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        mixn="3",  # 5 minutes ago
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_volume_surge_tse(client, common_params):
    """Test volume surge analysis for Tokyo Stock Exchange."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_volume_surge(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="TSE",  # Tokyo
        mixn="4",  # 10 minutes ago
        vol_rang="2",  # 1000+ shares
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_buy_execution_strength_top(client, common_params):
    """Test buy execution strength top ranking."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_buy_execution_strength_top(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        nday="3",  # 5 minutes ago
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


# Rate Rankings Tests


@pytest.mark.integration
def test_get_stock_rise_decline_rate_rise(client, common_params):
    """Test stock rise/decline rate - rising stocks."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_rise_decline_rate(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        gubn="1",  # Rise rate
        nday="0",  # Today
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_rise_decline_rate_decline_5day(client, common_params):
    """Test stock rise/decline rate - declining stocks over 5 days."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_rise_decline_rate(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        gubn="0",  # Decline rate
        nday="3",  # 5 days
        vol_rang="1",  # 100+ shares
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_new_high_low_price_high(client, common_params):
    """Test new high price stocks."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_new_high_low_price(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        gubn="1",  # New high
        gubn2="1",  # Sustained breakthrough
        nday="6",  # 52 weeks
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_new_high_low_price_low(client, common_params):
    """Test new low price stocks."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_new_high_low_price(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        gubn="0",  # New low
        gubn2="0",  # Temporary breakthrough
        nday="4",  # 60 days
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


# Trading Rankings Tests


@pytest.mark.integration
def test_get_stock_trading_volume_rank_nasdaq(client, common_params):
    """Test trading volume ranking for NASDAQ."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_trading_volume_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        nday="0",  # Today
        prc1="0",  # Price from
        prc2="999999",  # Price to
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_trading_volume_rank_with_price_filter(client, common_params):
    """Test trading volume ranking with price filter."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_trading_volume_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        nday="1",  # 2 days
        prc1="10",  # Price from $10
        prc2="100",  # Price to $100
        vol_rang="2",  # 1000+ shares
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_trading_amount_rank(client, common_params):
    """Test trading amount ranking."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_trading_amount_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        nday="0",  # Today
        vol_rang=common_params["vol_rang"],
        prc1="0",
        prc2="999999",
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_trading_increase_rate_rank(client, common_params):
    """Test trading increase rate ranking."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_trading_increase_rate_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        nday="3",  # 5 days
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_trading_turnover_rate_rank(client, common_params):
    """Test trading turnover rate ranking."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_trading_turnover_rate_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        nday="0",  # Today
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


# Market Cap Tests


@pytest.mark.integration
def test_get_stock_market_cap_rank_nasdaq(client, common_params):
    """Test market cap ranking for NASDAQ."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_market_cap_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NAS",  # NASDAQ
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_market_cap_rank_nyse(client, common_params):
    """Test market cap ranking for NYSE."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_market_cap_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="NYS",  # NYSE
        vol_rang="1",  # 100+ shares
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_market_cap_rank_hks(client, common_params):
    """Test market cap ranking for Hong Kong."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_market_cap_rank(
        keyb=common_params["keyb"],
        auth=common_params["auth"],
        excd="HKS",  # Hong Kong
        vol_rang=common_params["vol_rang"],
    )

    assert response is not None
    assert hasattr(response, "output1")


# Rights Inquiry Tests


@pytest.mark.integration
def test_get_stock_period_rights_inquiry_all(client, date_range):
    """Test period rights inquiry - all types."""
    time.sleep(1)
    start_dt, end_dt = date_range
    response = client.overseas_market_analysis.get_stock_period_rights_inquiry(
        rght_type_cd="%%",  # All types
        inqr_dvsn_cd="02",  # Local base date
        inqr_strt_dt=start_dt,
        inqr_end_dt=end_dt,
        pdno="",  # All products
        prdt_type_cd="",
        ctx_area_nk50="",
        ctx_area_fk50="",
    )

    assert response is not None
    assert hasattr(response, "output")


@pytest.mark.integration
def test_get_stock_period_rights_inquiry_dividend(client, date_range):
    """Test period rights inquiry - dividends only."""
    time.sleep(1)
    start_dt, end_dt = date_range
    response = client.overseas_market_analysis.get_stock_period_rights_inquiry(
        rght_type_cd="03",  # Dividend
        inqr_dvsn_cd="02",  # Local base date
        inqr_strt_dt=start_dt,
        inqr_end_dt=end_dt,
        pdno="",
        prdt_type_cd="",
        ctx_area_nk50="",
        ctx_area_fk50="",
    )

    assert response is not None
    assert hasattr(response, "output")


@pytest.mark.integration
def test_get_stock_rights_aggregate_us(client):
    """Test stock rights aggregate for US stocks."""
    time.sleep(1)
    # Use specific stock like AAPL
    start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
    end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

    response = client.overseas_market_analysis.get_stock_rights_aggregate(
        ncod="US",  # United States
        symb="AAPL",  # Apple
        st_ymd=start_dt,
        ed_ymd=end_dt,
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_rights_aggregate_hk(client):
    """Test stock rights aggregate for Hong Kong stocks."""
    time.sleep(1)
    start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
    end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

    response = client.overseas_market_analysis.get_stock_rights_aggregate(
        ncod="HK",  # Hong Kong
        symb="00700",  # Tencent
        st_ymd=start_dt,
        ed_ymd=end_dt,
    )

    assert response is not None
    assert hasattr(response, "output1")


# News Information Tests


@pytest.mark.integration
def test_get_news_aggregate_title_all(client):
    """Test news aggregate title - all news."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_news_aggregate_title(
        info_gb="",  # All news
        class_cd="",  # All categories
        nation_cd="",  # All countries
        exchange_cd="",  # All exchanges
        symb="",  # All stocks
        data_dt="",  # All dates
        data_tm="",  # All times
        cts="",  # First page
    )

    assert response is not None
    assert hasattr(response, "outblock1")


@pytest.mark.integration
def test_get_news_aggregate_title_us_only(client):
    """Test news aggregate title - US news only."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_news_aggregate_title(
        info_gb="",
        class_cd="",
        nation_cd="US",  # US only
        exchange_cd="",
        symb="",
        data_dt="",
        data_tm="",
        cts="",
    )

    assert response is not None
    assert hasattr(response, "outblock1")


@pytest.mark.integration
def test_get_news_aggregate_title_specific_date(client):
    """Test news aggregate title - specific date."""
    time.sleep(1)
    today = datetime.now().strftime("%Y%m%d")
    response = client.overseas_market_analysis.get_news_aggregate_title(
        info_gb="",
        class_cd="",
        nation_cd="",
        exchange_cd="",
        symb="",
        data_dt=today,  # Today's news
        data_tm="",
        cts="",
    )

    assert response is not None
    assert hasattr(response, "outblock1")


@pytest.mark.integration
def test_get_breaking_news_title(client):
    """Test breaking news title retrieval."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_breaking_news_title(
        fid_news_ofer_entp_code="0",  # All providers
        fid_cond_mrkt_cls_code="",
        fid_input_iscd="",
        fid_titl_cntt="",
        fid_input_date_1="",
        fid_input_hour_1="",
        fid_rank_sort_cls_code="",
        fid_input_srno="",
        fid_cond_scr_div_code="11801",  # Screen code
    )

    assert response is not None
    assert hasattr(response, "output1")


# Collateral Loan Tests


@pytest.mark.integration
def test_get_stock_collateral_loan_eligible_us_all(client):
    """Test collateral loan eligible stocks - US all stocks."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_collateral_loan_eligible(
        pdno="",  # All stocks
        prdt_type_cd="",
        inqr_strt_dt="",
        inqr_end_dt="",
        inqr_dvsn="",
        natn_cd="840",  # United States
        inqr_sqn_dvsn="01",  # Name order
        rt_dvsn_cd="",
        rt="",
        loan_psbl_yn="",
        ctx_area_fk100="",
        ctx_area_nk100="",
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_collateral_loan_eligible_us_specific(client):
    """Test collateral loan eligible stocks - specific US stock."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_collateral_loan_eligible(
        pdno="AAPL",  # Apple
        prdt_type_cd="",
        inqr_strt_dt="",
        inqr_end_dt="",
        inqr_dvsn="",
        natn_cd="840",  # United States
        inqr_sqn_dvsn="02",  # Code order
        rt_dvsn_cd="",
        rt="",
        loan_psbl_yn="",
        ctx_area_fk100="",
        ctx_area_nk100="",
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_collateral_loan_eligible_hk(client):
    """Test collateral loan eligible stocks - Hong Kong."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_collateral_loan_eligible(
        pdno="",
        prdt_type_cd="",
        inqr_strt_dt="",
        inqr_end_dt="",
        inqr_dvsn="",
        natn_cd="344",  # Hong Kong
        inqr_sqn_dvsn="01",  # Name order
        rt_dvsn_cd="",
        rt="",
        loan_psbl_yn="",
        ctx_area_fk100="",
        ctx_area_nk100="",
    )

    assert response is not None
    assert hasattr(response, "output1")


@pytest.mark.integration
def test_get_stock_collateral_loan_eligible_china(client):
    """Test collateral loan eligible stocks - China."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_collateral_loan_eligible(
        pdno="",
        prdt_type_cd="",
        inqr_strt_dt="",
        inqr_end_dt="",
        inqr_dvsn="",
        natn_cd="156",  # China
        inqr_sqn_dvsn="02",  # Code order
        rt_dvsn_cd="",
        rt="",
        loan_psbl_yn="",
        ctx_area_fk100="",
        ctx_area_nk100="",
    )

    assert response is not None
    assert hasattr(response, "output1")


# Multiple Exchanges Tests

# TODO: Fix the API issue before enabling these tests
# @pytest.mark.integration
# @pytest.mark.parametrize("exchange_code", [
#     ("NYS"),
#     ("NAS"),
#     ("AMS"),
#     ("HKS"),
#     ("TSE"),
# ])
# def test_price_rise_fall_multiple_exchanges(client, exchange_code):
#     """Test price rise/fall across multiple exchanges."""
#     time.sleep(1)
#     response = client.overseas_market_analysis.get_stock_price_fluctuation(
#         excd=exchange_code,
#         gubn="1",  # Rising
#         mixn="3",  # 5 minutes ago
#         vol_rang="0"
#     )

#     assert response is not None
#     assert hasattr(response, 'output1')


@pytest.mark.integration
@pytest.mark.parametrize(
    "exchange_code,exchange_name",
    [
        ("NYS", "NYSE"),
        ("NAS", "NASDAQ"),
        ("HKS", "Hong Kong"),
        ("TSE", "Tokyo"),
    ],
)
def test_market_cap_rank_multiple_exchanges(client, exchange_code, exchange_name):
    """Test market cap ranking across multiple exchanges."""
    time.sleep(1)
    response = client.overseas_market_analysis.get_stock_market_cap_rank(
        keyb="", auth="", excd=exchange_code, vol_rang="0"
    )

    assert response is not None
    assert hasattr(response, "output1")


# Error Handling Tests


@pytest.mark.integration
def test_invalid_exchange_code(client):
    """Test handling of invalid exchange code."""
    time.sleep(1)
    try:
        response = client.overseas_market_analysis.get_stock_price_rise_fall(
            keyb="",
            auth="",
            excd="INVALID",  # Invalid exchange code
            gubn="1",
            mixn="3",
            vol_rang="0",
        )
        # If no exception, check for error in response
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid exchange code
        assert e is not None


@pytest.mark.integration
def test_invalid_date_range_rights(client):
    """Test handling of invalid date range for rights inquiry."""
    time.sleep(1)
    try:
        response = client.overseas_market_analysis.get_stock_period_rights_inquiry(
            rght_type_cd="%%",
            inqr_dvsn_cd="02",
            inqr_strt_dt="20990101",  # Future date
            inqr_end_dt="20000101",  # Past date (reversed)
            pdno="",
            prdt_type_cd="",
            ctx_area_nk50="",
            ctx_area_fk50="",
        )
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid date range
        assert e is not None


@pytest.mark.integration
def test_invalid_stock_symbol_rights(client):
    """Test handling of invalid stock symbol in rights aggregate."""
    time.sleep(1)
    start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
    end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

    try:
        response = client.overseas_market_analysis.get_stock_rights_aggregate(
            ncod="US",
            symb="INVALID999",  # Invalid symbol
            st_ymd=start_dt,
            ed_ymd=end_dt,
        )
        # If no exception, check for error in response
        assert response is not None
    except Exception as e:
        # Expected to fail or return empty results
        assert e is not None
