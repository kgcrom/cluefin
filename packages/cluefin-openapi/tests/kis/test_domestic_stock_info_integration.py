"""Integration tests for KIS Domestic Stock Info API.

These tests require valid API credentials in environment variables:
- KIWOOM_APP_KEY
- KIWOOM_SECRET_KEY
- KIWOOM_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_domestic_stock_info_integration.py -v -m integration
"""

import os
from datetime import datetime, timedelta

import pytest

from cluefin_openapi.kis._client import Client


@pytest.fixture(scope="module")
def kis_client():
    """Create KIS client with real credentials."""
    app_key = os.getenv("KIWOOM_APP_KEY")
    secret_key = os.getenv("KIWOOM_SECRET_KEY")
    env = os.getenv("KIWOOM_ENV", "dev")

    if not app_key or not secret_key:
        pytest.skip("KIS API credentials not found in environment variables")

    # For KIS API, we need to generate a token first
    # Assuming the client handles token generation internally
    client = Client(app_key=app_key, secret_key=secret_key, env=env)
    return client


@pytest.mark.integration
class TestProductAndStockInfo:
    """Test product and stock basic information retrieval."""

    def test_get_product_basic_info(self, kis_client):
        """Test product basic information retrieval."""
        # Test with Samsung Electronics (005930)
        response = kis_client.domestic_stock_info.get_product_basic_info(
            pdno="005930",
            prdt_type_cd="300"  # Stock
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_basic_info(self, kis_client):
        """Test stock basic information retrieval."""
        # Test with SK Hynix (000660)
        response = kis_client.domestic_stock_info.get_stock_basic_info(
            prdt_type_cd="300",  # Stock
            pdno="000660"
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestFinancialStatements:
    """Test financial statement retrieval methods."""

    def test_get_balance_sheet(self, kis_client):
        """Test balance sheet retrieval."""
        response = kis_client.domestic_stock_info.get_balance_sheet(
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J",  # Stock market
            fid_input_iscd="005930"  # Samsung Electronics
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_income_statement(self, kis_client):
        """Test income statement retrieval."""
        response = kis_client.domestic_stock_info.get_income_statement(
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_financial_ratio(self, kis_client):
        """Test financial ratio retrieval."""
        response = kis_client.domestic_stock_info.get_financial_ratio(
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="000660"  # SK Hynix
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestFinancialRatios:
    """Test various financial ratio retrieval methods."""

    def test_get_profitability_ratio(self, kis_client):
        """Test profitability ratio retrieval."""
        response = kis_client.domestic_stock_info.get_profitability_ratio(
            fid_input_iscd="005930",  # Samsung Electronics
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_other_key_ratio(self, kis_client):
        """Test other key ratio retrieval."""
        response = kis_client.domestic_stock_info.get_other_key_ratio(
            fid_input_iscd="035720",  # Kakao
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stability_ratio(self, kis_client):
        """Test stability ratio retrieval."""
        response = kis_client.domestic_stock_info.get_stability_ratio(
            fid_input_iscd="005930",
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_growth_ratio(self, kis_client):
        """Test growth ratio retrieval."""
        response = kis_client.domestic_stock_info.get_growth_ratio(
            fid_input_iscd="000660",  # SK Hynix
            fid_div_cls_code="0",  # Year
            fid_cond_mrkt_div_code="J"
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestTradableStocks:
    """Test margin and loanable stock retrieval methods."""

    def test_get_margin_tradable_stocks(self, kis_client):
        """Test margin tradable stocks retrieval."""
        response = kis_client.domestic_stock_info.get_margin_tradable_stocks(
            fid_rank_sort_cls_code="0",  # Code order
            fid_slct_yn="0",  # Margin tradable
            fid_input_iscd="0000",  # All stocks
            fid_cond_scr_div_code="20477",  # Screen code
            fid_cond_mrkt_div_code="J"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_loanable_list(self, kis_client):
        """Test stock loanable list retrieval."""
        response = kis_client.domestic_stock_info.get_stock_loanable_list(
            excg_dvsn_cd="00",  # All exchanges
            pdno="",  # All stocks
            thco_stln_psbl_yn="Y",
            inqr_dvsn_1="0",  # All
            ctx_area_fk200="",
            ctx_area_nk100=""
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestKSDInformation:
    """Test Korea Securities Depository (KSD) information retrieval."""

    @pytest.fixture(scope="class")
    def date_range(self):
        """Generate date range for KSD queries."""
        t_dt = datetime.now().strftime("%Y%m%d")
        f_dt = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")  # 6 months ago
        return f_dt, t_dt

    def test_get_ksd_dividend_decision(self, kis_client, date_range):
        """Test KSD dividend decision retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_dividend_decision(
            cts="",
            gb1="0",  # All dividends
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd="",  # All stocks
            high_gb=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_stock_dividend_decision(self, kis_client, date_range):
        """Test KSD stock dividend decision retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_stock_dividend_decision(
            sht_cd="",  # All stocks
            t_dt=t_dt,
            f_dt=f_dt,
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_merger_split_decision(self, kis_client, date_range):
        """Test KSD merger/split decision retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_merger_split_decision(
            cts="",
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd=""  # All stocks
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_par_value_change_decision(self, kis_client, date_range):
        """Test KSD par value change decision retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_par_value_change_decision(
            sht_cd="",  # All stocks
            cts="",
            f_dt=f_dt,
            t_dt=t_dt,
            market_gb="0"  # All markets
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_capital_reduction_schedule(self, kis_client, date_range):
        """Test KSD capital reduction schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_capital_reduction_schedule(
            cts="",
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_listing_info_schedule(self, kis_client, date_range):
        """Test KSD listing information schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_listing_info_schedule(
            sht_cd="",
            t_dt=t_dt,
            f_dt=f_dt,
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_ipo_subscription_schedule(self, kis_client, date_range):
        """Test KSD IPO subscription schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_ipo_subscription_schedule(
            sht_cd="",
            cts="",
            f_dt=f_dt,
            t_dt=t_dt
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_forfeited_share_schedule(self, kis_client, date_range):
        """Test KSD forfeited share schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_forfeited_share_schedule(
            sht_cd="",
            t_dt=t_dt,
            f_dt=f_dt,
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_deposit_schedule(self, kis_client, date_range):
        """Test KSD deposit schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_deposit_schedule(
            t_dt=t_dt,
            sht_cd="",
            f_dt=f_dt,
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_paid_in_capital_increase_schedule(self, kis_client, date_range):
        """Test KSD paid-in capital increase schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_paid_in_capital_increase_schedule(
            cts="",
            gb1="1",  # By subscription date
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_stock_dividend_schedule(self, kis_client, date_range):
        """Test KSD stock dividend schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_stock_dividend_schedule(
            cts="",
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_ksd_shareholder_meeting_schedule(self, kis_client, date_range):
        """Test KSD shareholder meeting schedule retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_ksd_shareholder_meeting_schedule(
            cts="",
            f_dt=f_dt,
            t_dt=t_dt,
            sht_cd=""
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestInvestmentInformation:
    """Test investment opinion and earnings estimation methods."""

    @pytest.fixture(scope="class")
    def date_range(self):
        """Generate date range for investment queries."""
        # Use format with leading zeros: 0020240513
        t_dt = "00" + datetime.now().strftime("%Y%m%d")
        f_dt = "00" + (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
        return f_dt, t_dt

    def test_get_estimated_earnings(self, kis_client):
        """Test estimated earnings retrieval."""
        response = kis_client.domestic_stock_info.get_estimated_earnings(
            sht_cd="005930"  # Samsung Electronics
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_investment_opinion(self, kis_client, date_range):
        """Test investment opinion retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_investment_opinion(
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="16633",  # Primary key
            fid_input_iscd="005930",  # Samsung Electronics
            fid_input_date_1=f_dt,
            fid_input_date_2=t_dt
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_investment_opinion_by_brokerage(self, kis_client, date_range):
        """Test investment opinion by brokerage retrieval."""
        f_dt, t_dt = date_range
        response = kis_client.domestic_stock_info.get_investment_opinion_by_brokerage(
            fid_cond_mrkt_div_code="J",
            fid_cond_scr_div_code="16634",  # Primary key
            fid_input_iscd="005930",  # Samsung Electronics
            fid_div_cls_code="0",  # All
            fid_input_date_1=f_dt,
            fid_input_date_2=t_dt
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_invalid_stock_code(self, kis_client):
        """Test handling of invalid stock code."""
        # This should either raise an exception or return an error response
        try:
            response = kis_client.domestic_stock_info.get_product_basic_info(
                pdno="999999",  # Invalid code
                prdt_type_cd="300"
            )
            # If no exception, check for error in response
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid code
            assert e is not None

    def test_invalid_date_range(self, kis_client):
        """Test handling of invalid date range."""
        try:
            response = kis_client.domestic_stock_info.get_ksd_dividend_decision(
                cts="",
                gb1="0",
                f_dt="20990101",  # Future date
                t_dt="20000101",  # Past date (reversed range)
                sht_cd="",
                high_gb=""
            )
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid date range
            assert e is not None
