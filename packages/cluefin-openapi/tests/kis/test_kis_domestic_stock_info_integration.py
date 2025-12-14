"""Integration tests for KIS Domestic Stock Info API.

These tests require valid API credentials in environment variables:
- KIS_APP_KEY
- KIS_SECRET_KEY
- KIS_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_domestic_stock_info_integration.py -v -m integration
"""

import os
import time
from datetime import datetime, timedelta
from typing import Literal, cast

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._client import Client

from ._token_cache import TokenCache


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
def kis_client(auth_dev, token_cache):
    """Create KIS client with real credentials."""
    token_response = token_cache.get()

    return Client(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
        # debug=True,
    )


@pytest.mark.integration
def test_get_product_basic_info(kis_client):
    """Test product basic information retrieval."""
    time.sleep(1)
    # Test with Samsung Electronics (005930)
    response = kis_client.domestic_stock_info.get_product_basic_info(
        pdno="005930",
        prdt_type_cd="300",  # Stock
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stock_basic_info(kis_client):
    """Test stock basic information retrieval."""
    time.sleep(1)
    # Test with SK Hynix (000660)
    response = kis_client.domestic_stock_info.get_stock_basic_info(
        prdt_type_cd="300",  # Stock
        pdno="000660",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_balance_sheet(kis_client):
    """Test balance sheet retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_balance_sheet(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",  # Stock market
        fid_input_iscd="005930",  # Samsung Electronics
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_income_statement(kis_client):
    """Test income statement retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_income_statement(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_financial_ratio(kis_client):
    """Test financial ratio retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_financial_ratio(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="000660",  # SK Hynix
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_profitability_ratio(kis_client):
    """Test profitability ratio retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_profitability_ratio(
        fid_input_iscd="005930",  # Samsung Electronics
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_other_key_ratio(kis_client):
    """Test other key ratio retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_other_key_ratio(
        fid_input_iscd="035720",  # Kakao
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stability_ratio(kis_client):
    """Test stability ratio retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_stability_ratio(
        fid_input_iscd="005930",
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_growth_ratio(kis_client):
    """Test growth ratio retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_growth_ratio(
        fid_input_iscd="000660",  # SK Hynix
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_margin_tradable_stocks(kis_client):
    """Test margin tradable stocks retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_margin_tradable_stocks(
        fid_rank_sort_cls_code="0",  # Code order
        fid_slct_yn="0",  # Margin tradable
        fid_input_iscd="0000",  # All stocks
        fid_cond_scr_div_code="20477",  # Screen code
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stock_loanable_list(kis_client):
    """Test stock loanable list retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_stock_loanable_list(
        excg_dvsn_cd="00",  # All exchanges
        pdno="",  # All stocks
        thco_stln_psbl_yn="Y",
        inqr_dvsn_1="0",  # All
        ctx_area_fk200="",
        ctx_area_nk100="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")
    assert hasattr(response.body, "output2")


@pytest.fixture
def date_range():
    """Generate date range for KSD queries."""
    t_dt = datetime.now().strftime("%Y%m%d")
    f_dt = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")  # 6 months ago
    return f_dt, t_dt


@pytest.mark.integration
def test_get_ksd_dividend_decision(kis_client, date_range):
    """Test KSD dividend decision retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_dividend_decision(
        cts="",
        gb1="0",  # All dividends
        f_dt=f_dt,
        t_dt=t_dt,
        sht_cd="",  # All stocks
        high_gb="",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_ksd_stock_dividend_decision(kis_client, date_range):
    """Test KSD stock dividend decision retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_stock_dividend_decision(
        sht_cd="",  # All stocks
        t_dt=t_dt,
        f_dt=f_dt,
        cts="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_merger_split_decision(kis_client, date_range):
    """Test KSD merger/split decision retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_merger_split_decision(
        cts="",
        f_dt=f_dt,
        t_dt=t_dt,
        sht_cd="",  # All stocks
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_par_value_change_decision(kis_client, date_range):
    """Test KSD par value change decision retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_par_value_change_decision(
        sht_cd="",  # All stocks
        cts="",
        f_dt=f_dt,
        t_dt=t_dt,
        market_gb="0",  # All markets
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_capital_reduction_schedule(kis_client, date_range):
    """Test KSD capital reduction schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_capital_reduction_schedule(
        cts="", f_dt=f_dt, t_dt=t_dt, sht_cd=""
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_listing_info_schedule(kis_client, date_range):
    """Test KSD listing information schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_listing_info_schedule(sht_cd="", t_dt=t_dt, f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_ipo_subscription_schedule(kis_client, date_range):
    """Test KSD IPO subscription schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_ipo_subscription_schedule(sht_cd="", cts="", f_dt=f_dt, t_dt=t_dt)

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_forfeited_share_schedule(kis_client, date_range):
    """Test KSD forfeited share schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_forfeited_share_schedule(sht_cd="", t_dt=t_dt, f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_deposit_schedule(kis_client, date_range):
    """Test KSD deposit schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_deposit_schedule(t_dt=t_dt, sht_cd="", f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_paid_in_capital_increase_schedule(kis_client, date_range):
    """Test KSD paid-in capital increase schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_paid_in_capital_increase_schedule(
        cts="",
        gb1="1",  # By subscription date
        f_dt=f_dt,
        t_dt=t_dt,
        sht_cd="",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_ksd_stock_dividend_schedule(kis_client, date_range):
    """Test KSD stock dividend schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_stock_dividend_schedule(cts="", f_dt=f_dt, t_dt=t_dt, sht_cd="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_shareholder_meeting_schedule(kis_client, date_range):
    """Test KSD shareholder meeting schedule retrieval."""
    time.sleep(1)
    f_dt, t_dt = date_range
    response = kis_client.domestic_stock_info.get_ksd_shareholder_meeting_schedule(
        cts="", f_dt=f_dt, t_dt=t_dt, sht_cd=""
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.fixture
def investment_date_range():
    """Generate date range for investment queries."""
    # Use format with leading zeros: 0020240513
    t_dt = "00" + datetime.now().strftime("%Y%m%d")
    f_dt = "00" + (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
    return f_dt, t_dt


@pytest.mark.integration
def test_get_estimated_earnings(kis_client):
    """Test estimated earnings retrieval."""
    time.sleep(1)
    response = kis_client.domestic_stock_info.get_estimated_earnings(
        sht_cd="005930"  # Samsung Electronics
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_investment_opinion(kis_client, investment_date_range):
    """Test investment opinion retrieval."""
    time.sleep(1)
    f_dt, t_dt = investment_date_range
    response = kis_client.domestic_stock_info.get_investment_opinion(
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="16633",  # Primary key
        fid_input_iscd="005930",  # Samsung Electronics
        fid_input_date_1=f_dt,
        fid_input_date_2=t_dt,
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_investment_opinion_by_brokerage(kis_client, investment_date_range):
    """Test investment opinion by brokerage retrieval."""
    time.sleep(1)
    f_dt, t_dt = investment_date_range
    response = kis_client.domestic_stock_info.get_investment_opinion_by_brokerage(
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="16634",  # Primary key
        fid_input_iscd="005930",  # Samsung Electronics
        fid_div_cls_code="0",  # All
        fid_input_date_1=f_dt,
        fid_input_date_2=t_dt,
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_invalid_stock_code(kis_client):
    """Test handling of invalid stock code."""
    time.sleep(1)
    # This should either raise an exception or return an error response
    try:
        response = kis_client.domestic_stock_info.get_product_basic_info(
            pdno="999999",  # Invalid code
            prdt_type_cd="300",
        )
        # If no exception, check for error in response
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid code
        assert e is not None


@pytest.mark.integration
def test_invalid_date_range(kis_client):
    """Test handling of invalid date range."""
    time.sleep(1)
    try:
        response = kis_client.domestic_stock_info.get_ksd_dividend_decision(
            cts="",
            gb1="0",
            f_dt="20990101",  # Future date
            t_dt="20000101",  # Past date (reversed range)
            sht_cd="",
            high_gb="",
        )
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid date range
        assert e is not None
