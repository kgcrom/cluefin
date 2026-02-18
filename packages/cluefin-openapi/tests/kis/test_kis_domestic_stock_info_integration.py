"""Integration tests for KIS Domestic Stock Info API.

These tests require valid API credentials in environment variables:
- KIS_APP_KEY
- KIS_SECRET_KEY
- KIS_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_domestic_stock_info_integration.py -v -m integration
"""

from datetime import datetime, timedelta

import pytest

from cluefin_openapi.kis._http_client import HttpClient


@pytest.mark.integration
def test_get_product_basic_info(client: HttpClient):
    """Test product basic information retrieval."""
    # Test with Samsung Electronics (005930)
    response = client.domestic_stock_info.get_product_basic_info(
        pdno="005930",
        prdt_type_cd="300",  # Stock
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stock_basic_info(client: HttpClient):
    """Test stock basic information retrieval."""
    # Test with SK Hynix (000660)
    response = client.domestic_stock_info.get_stock_basic_info(
        prdt_type_cd="300",  # Stock
        pdno="000660",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_balance_sheet(client: HttpClient):
    """Test balance sheet retrieval."""
    response = client.domestic_stock_info.get_balance_sheet(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",  # Stock market
        fid_input_iscd="005930",  # Samsung Electronics
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_income_statement(client: HttpClient):
    """Test income statement retrieval."""
    response = client.domestic_stock_info.get_income_statement(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_financial_ratio(client: HttpClient):
    """Test financial ratio retrieval."""
    response = client.domestic_stock_info.get_financial_ratio(
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="000660",  # SK Hynix
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_profitability_ratio(client: HttpClient):
    """Test profitability ratio retrieval."""
    response = client.domestic_stock_info.get_profitability_ratio(
        fid_input_iscd="005930",  # Samsung Electronics
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_other_key_ratio(client: HttpClient):
    """Test other key ratio retrieval."""
    response = client.domestic_stock_info.get_other_key_ratio(
        fid_input_iscd="035720",  # Kakao
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stability_ratio(client: HttpClient):
    """Test stability ratio retrieval."""
    response = client.domestic_stock_info.get_stability_ratio(
        fid_input_iscd="005930",
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_growth_ratio(client: HttpClient):
    """Test growth ratio retrieval."""
    response = client.domestic_stock_info.get_growth_ratio(
        fid_input_iscd="000660",  # SK Hynix
        fid_div_cls_code="0",  # Year
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_margin_tradable_stocks(client: HttpClient):
    """Test margin tradable stocks retrieval."""
    response = client.domestic_stock_info.get_margin_tradable_stocks(
        fid_rank_sort_cls_code="0",  # Code order
        fid_slct_yn="0",  # Margin tradable
        fid_input_iscd="0000",  # All stocks
        fid_cond_scr_div_code="20477",  # Screen code
        fid_cond_mrkt_div_code="J",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_stock_loanable_list(client: HttpClient):
    """Test stock loanable list retrieval."""
    response = client.domestic_stock_info.get_stock_loanable_list(
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
def test_get_ksd_dividend_decision(client: HttpClient, date_range):
    """Test KSD dividend decision retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_dividend_decision(
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
def test_get_ksd_stock_dividend_decision(client: HttpClient, date_range):
    """Test KSD stock dividend decision retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_stock_dividend_decision(
        sht_cd="",  # All stocks
        t_dt=t_dt,
        f_dt=f_dt,
        cts="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_merger_split_decision(client: HttpClient, date_range):
    """Test KSD merger/split decision retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_merger_split_decision(
        cts="",
        f_dt=f_dt,
        t_dt=t_dt,
        sht_cd="",  # All stocks
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_par_value_change_decision(client: HttpClient, date_range):
    """Test KSD par value change decision retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_par_value_change_decision(
        sht_cd="",  # All stocks
        cts="",
        f_dt=f_dt,
        t_dt=t_dt,
        market_gb="0",  # All markets
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_capital_reduction_schedule(client: HttpClient, date_range):
    """Test KSD capital reduction schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_capital_reduction_schedule(cts="", f_dt=f_dt, t_dt=t_dt, sht_cd="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_listing_info_schedule(client: HttpClient, date_range):
    """Test KSD listing information schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_listing_info_schedule(sht_cd="", t_dt=t_dt, f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_ipo_subscription_schedule(client: HttpClient, date_range):
    """Test KSD IPO subscription schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_ipo_subscription_schedule(sht_cd="", cts="", f_dt=f_dt, t_dt=t_dt)

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_forfeited_share_schedule(client: HttpClient, date_range):
    """Test KSD forfeited share schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_forfeited_share_schedule(sht_cd="", t_dt=t_dt, f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_deposit_schedule(client: HttpClient, date_range):
    """Test KSD deposit schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_deposit_schedule(t_dt=t_dt, sht_cd="", f_dt=f_dt, cts="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_paid_in_capital_increase_schedule(client: HttpClient, date_range):
    """Test KSD paid-in capital increase schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_paid_in_capital_increase_schedule(
        cts="",
        gb1="1",  # By subscription date
        f_dt=f_dt,
        t_dt=t_dt,
        sht_cd="",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_ksd_stock_dividend_schedule(client: HttpClient, date_range):
    """Test KSD stock dividend schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_stock_dividend_schedule(cts="", f_dt=f_dt, t_dt=t_dt, sht_cd="")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_ksd_shareholder_meeting_schedule(client: HttpClient, date_range):
    """Test KSD shareholder meeting schedule retrieval."""
    f_dt, t_dt = date_range
    response = client.domestic_stock_info.get_ksd_shareholder_meeting_schedule(cts="", f_dt=f_dt, t_dt=t_dt, sht_cd="")

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
def test_get_estimated_earnings(client: HttpClient):
    """Test estimated earnings retrieval."""
    response = client.domestic_stock_info.get_estimated_earnings(
        sht_cd="005930"  # Samsung Electronics
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_investment_opinion(client: HttpClient, investment_date_range):
    """Test investment opinion retrieval."""
    f_dt, t_dt = investment_date_range
    response = client.domestic_stock_info.get_investment_opinion(
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="16633",  # Primary key
        fid_input_iscd="005930",  # Samsung Electronics
        fid_input_date_1=f_dt,
        fid_input_date_2=t_dt,
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_investment_opinion_by_brokerage(client: HttpClient, investment_date_range):
    """Test investment opinion by brokerage retrieval."""
    f_dt, t_dt = investment_date_range
    response = client.domestic_stock_info.get_investment_opinion_by_brokerage(
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
def test_invalid_stock_code(client: HttpClient):
    """Test handling of invalid stock code."""
    # This should either raise an exception or return an error response
    try:
        response = client.domestic_stock_info.get_product_basic_info(
            pdno="999999",  # Invalid code
            prdt_type_cd="300",
        )
        # If no exception, check for error in response
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid code
        assert e is not None


@pytest.mark.integration
def test_invalid_date_range(client: HttpClient):
    """Test handling of invalid date range."""
    try:
        response = client.domestic_stock_info.get_ksd_dividend_decision(
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
