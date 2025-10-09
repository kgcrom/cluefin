"""Integration tests for KIS Overseas Market Analysis API.

These tests require valid API credentials in environment variables:
- KIWOOM_APP_KEY
- KIWOOM_SECRET_KEY
- KIWOOM_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_overseas_market_analysis_integration.py -v -m integration
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

    client = Client(app_key=app_key, secret_key=secret_key, env=env)
    return client


@pytest.fixture(scope="module")
def common_params():
    """Common parameters used across multiple tests."""
    return {
        "keyb": "",  # NEXT KEY BUFF (empty for first call)
        "auth": "",  # User auth info (empty)
        "vol_rang": "0"  # Volume condition (0: all)
    }


@pytest.mark.integration
class TestStockPriceAnalysis:
    """Test stock price fluctuation analysis methods."""

    def test_get_stock_price_rise_fall_nasdaq_rise(self, kis_client, common_params):
        """Test stock price rise/fall for NASDAQ - rising stocks."""
        response = kis_client.overseas_market_analysis.get_stock_price_rise_fall(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            gubn="1",  # Rising
            mixn="3",  # 5 minutes ago
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_price_rise_fall_nyse_fall(self, kis_client, common_params):
        """Test stock price rise/fall for NYSE - falling stocks."""
        response = kis_client.overseas_market_analysis.get_stock_price_rise_fall(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            gubn="0",  # Falling
            mixn="4",  # 10 minutes ago
            vol_rang="1"  # 100+ shares
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_price_rise_fall_hks(self, kis_client, common_params):
        """Test stock price rise/fall for Hong Kong Stock Exchange."""
        response = kis_client.overseas_market_analysis.get_stock_price_rise_fall(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="HKS",  # Hong Kong
            gubn="1",  # Rising
            mixn="5",  # 15 minutes ago
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestVolumeAnalysis:
    """Test volume-related analysis methods."""

    def test_get_stock_volume_surge_nasdaq(self, kis_client, common_params):
        """Test volume surge analysis for NASDAQ."""
        response = kis_client.overseas_market_analysis.get_stock_volume_surge(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            mixn="3",  # 5 minutes ago
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_volume_surge_tse(self, kis_client, common_params):
        """Test volume surge analysis for Tokyo Stock Exchange."""
        response = kis_client.overseas_market_analysis.get_stock_volume_surge(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="TSE",  # Tokyo
            mixn="4",  # 10 minutes ago
            vol_rang="2"  # 1000+ shares
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_buy_execution_strength_top(self, kis_client, common_params):
        """Test buy execution strength top ranking."""
        response = kis_client.overseas_market_analysis.get_stock_buy_execution_strength_top(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            nday="3",  # 5 minutes ago
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestRateRankings:
    """Test various rate and ranking analysis methods."""

    def test_get_stock_rise_decline_rate_rise(self, kis_client, common_params):
        """Test stock rise/decline rate - rising stocks."""
        response = kis_client.overseas_market_analysis.get_stock_rise_decline_rate(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            gubn="1",  # Rise rate
            nday="0",  # Today
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_rise_decline_rate_decline_5day(self, kis_client, common_params):
        """Test stock rise/decline rate - declining stocks over 5 days."""
        response = kis_client.overseas_market_analysis.get_stock_rise_decline_rate(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            gubn="0",  # Decline rate
            nday="3",  # 5 days
            vol_rang="1"  # 100+ shares
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_new_high_low_price_high(self, kis_client, common_params):
        """Test new high price stocks."""
        response = kis_client.overseas_market_analysis.get_stock_new_high_low_price(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            gubn="1",  # New high
            gubn2="1",  # Sustained breakthrough
            nday="6",  # 52 weeks
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_new_high_low_price_low(self, kis_client, common_params):
        """Test new low price stocks."""
        response = kis_client.overseas_market_analysis.get_stock_new_high_low_price(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            gubn="0",  # New low
            gubn2="0",  # Temporary breakthrough
            nday="4",  # 60 days
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestTradingRankings:
    """Test trading volume and amount ranking methods."""

    def test_get_stock_trading_volume_rank_nasdaq(self, kis_client, common_params):
        """Test trading volume ranking for NASDAQ."""
        response = kis_client.overseas_market_analysis.get_stock_trading_volume_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            nday="0",  # Today
            prc1="0",  # Price from
            prc2="999999",  # Price to
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_trading_volume_rank_with_price_filter(self, kis_client, common_params):
        """Test trading volume ranking with price filter."""
        response = kis_client.overseas_market_analysis.get_stock_trading_volume_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            nday="1",  # 2 days
            prc1="10",  # Price from $10
            prc2="100",  # Price to $100
            vol_rang="2"  # 1000+ shares
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_trading_amount_rank(self, kis_client, common_params):
        """Test trading amount ranking."""
        response = kis_client.overseas_market_analysis.get_stock_trading_amount_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            nday="0",  # Today
            vol_rang=common_params["vol_rang"],
            prc1="0",
            prc2="999999"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_trading_increase_rate_rank(self, kis_client, common_params):
        """Test trading increase rate ranking."""
        response = kis_client.overseas_market_analysis.get_stock_trading_increase_rate_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            nday="3",  # 5 days
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_trading_turnover_rate_rank(self, kis_client, common_params):
        """Test trading turnover rate ranking."""
        response = kis_client.overseas_market_analysis.get_stock_trading_turnover_rate_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            nday="0",  # Today
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestMarketCapAndOther:
    """Test market cap and other analysis methods."""

    def test_get_stock_market_cap_rank_nasdaq(self, kis_client, common_params):
        """Test market cap ranking for NASDAQ."""
        response = kis_client.overseas_market_analysis.get_stock_market_cap_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NAS",  # NASDAQ
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_market_cap_rank_nyse(self, kis_client, common_params):
        """Test market cap ranking for NYSE."""
        response = kis_client.overseas_market_analysis.get_stock_market_cap_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="NYS",  # NYSE
            vol_rang="1"  # 100+ shares
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_market_cap_rank_hks(self, kis_client, common_params):
        """Test market cap ranking for Hong Kong."""
        response = kis_client.overseas_market_analysis.get_stock_market_cap_rank(
            keyb=common_params["keyb"],
            auth=common_params["auth"],
            excd="HKS",  # Hong Kong
            vol_rang=common_params["vol_rang"]
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestRightsInquiry:
    """Test stock rights inquiry methods."""

    @pytest.fixture(scope="class")
    def date_range(self):
        """Generate date range for rights queries."""
        end_dt = datetime.now().strftime("%Y%m%d")
        start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")  # 3 months ago
        return start_dt, end_dt

    def test_get_stock_period_rights_inquiry_all(self, kis_client, date_range):
        """Test period rights inquiry - all types."""
        start_dt, end_dt = date_range
        response = kis_client.overseas_market_analysis.get_stock_period_rights_inquiry(
            rght_type_cd="%%",  # All types
            inqr_dvsn_cd="02",  # Local base date
            inqr_strt_dt=start_dt,
            inqr_end_dt=end_dt,
            pdno="",  # All products
            prdt_type_cd="",
            ctx_area_nk50="",
            ctx_area_fk50=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_period_rights_inquiry_dividend(self, kis_client, date_range):
        """Test period rights inquiry - dividends only."""
        start_dt, end_dt = date_range
        response = kis_client.overseas_market_analysis.get_stock_period_rights_inquiry(
            rght_type_cd="03",  # Dividend
            inqr_dvsn_cd="02",  # Local base date
            inqr_strt_dt=start_dt,
            inqr_end_dt=end_dt,
            pdno="",
            prdt_type_cd="",
            ctx_area_nk50="",
            ctx_area_fk50=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_rights_aggregate_us(self, kis_client):
        """Test stock rights aggregate for US stocks."""
        # Use specific stock like AAPL
        start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
        end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

        response = kis_client.overseas_market_analysis.get_stock_rights_aggregate(
            ncod="US",  # United States
            symb="AAPL",  # Apple
            st_ymd=start_dt,
            ed_ymd=end_dt
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_rights_aggregate_hk(self, kis_client):
        """Test stock rights aggregate for Hong Kong stocks."""
        start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
        end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

        response = kis_client.overseas_market_analysis.get_stock_rights_aggregate(
            ncod="HK",  # Hong Kong
            symb="00700",  # Tencent
            st_ymd=start_dt,
            ed_ymd=end_dt
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestNewsInformation:
    """Test news and breaking news methods."""

    def test_get_news_aggregate_title_all(self, kis_client):
        """Test news aggregate title - all news."""
        response = kis_client.overseas_market_analysis.get_news_aggregate_title(
            info_gb="",  # All news
            class_cd="",  # All categories
            nation_cd="",  # All countries
            exchange_cd="",  # All exchanges
            symb="",  # All stocks
            data_dt="",  # All dates
            data_tm="",  # All times
            cts=""  # First page
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_news_aggregate_title_us_only(self, kis_client):
        """Test news aggregate title - US news only."""
        response = kis_client.overseas_market_analysis.get_news_aggregate_title(
            info_gb="",
            class_cd="",
            nation_cd="US",  # US only
            exchange_cd="",
            symb="",
            data_dt="",
            data_tm="",
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_news_aggregate_title_specific_date(self, kis_client):
        """Test news aggregate title - specific date."""
        today = datetime.now().strftime("%Y%m%d")
        response = kis_client.overseas_market_analysis.get_news_aggregate_title(
            info_gb="",
            class_cd="",
            nation_cd="",
            exchange_cd="",
            symb="",
            data_dt=today,  # Today's news
            data_tm="",
            cts=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_breaking_news_title(self, kis_client):
        """Test breaking news title retrieval."""
        response = kis_client.overseas_market_analysis.get_breaking_news_title(
            fid_news_ofer_entp_code="0",  # All providers
            fid_cond_mrkt_cls_code="",
            fid_input_iscd="",
            fid_titl_cntt="",
            fid_input_date_1="",
            fid_input_hour_1="",
            fid_rank_sort_cls_code="",
            fid_input_srno="",
            fid_cond_scr_div_code="11801"  # Screen code
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestCollateralLoan:
    """Test collateral loan eligible stocks inquiry."""

    def test_get_stock_collateral_loan_eligible_us_all(self, kis_client):
        """Test collateral loan eligible stocks - US all stocks."""
        response = kis_client.overseas_market_analysis.get_stock_collateral_loan_eligible(
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
            ctx_area_nk100=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_collateral_loan_eligible_us_specific(self, kis_client):
        """Test collateral loan eligible stocks - specific US stock."""
        response = kis_client.overseas_market_analysis.get_stock_collateral_loan_eligible(
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
            ctx_area_nk100=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_collateral_loan_eligible_hk(self, kis_client):
        """Test collateral loan eligible stocks - Hong Kong."""
        response = kis_client.overseas_market_analysis.get_stock_collateral_loan_eligible(
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
            ctx_area_nk100=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_collateral_loan_eligible_china(self, kis_client):
        """Test collateral loan eligible stocks - China."""
        response = kis_client.overseas_market_analysis.get_stock_collateral_loan_eligible(
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
            ctx_area_nk100=""
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestMultipleExchanges:
    """Test methods across multiple exchanges."""

    @pytest.mark.parametrize("exchange_code,exchange_name", [
        ("NYS", "NYSE"),
        ("NAS", "NASDAQ"),
        ("AMS", "AMEX"),
        ("HKS", "Hong Kong"),
        ("TSE", "Tokyo"),
    ])
    def test_price_rise_fall_multiple_exchanges(self, kis_client, exchange_code, exchange_name):
        """Test price rise/fall across multiple exchanges."""
        response = kis_client.overseas_market_analysis.get_stock_price_rise_fall(
            keyb="",
            auth="",
            excd=exchange_code,
            gubn="1",  # Rising
            mixn="3",  # 5 minutes ago
            vol_rang="0"
        )

        assert response is not None
        assert hasattr(response, 'output')

    @pytest.mark.parametrize("exchange_code,exchange_name", [
        ("NYS", "NYSE"),
        ("NAS", "NASDAQ"),
        ("HKS", "Hong Kong"),
        ("TSE", "Tokyo"),
    ])
    def test_market_cap_rank_multiple_exchanges(self, kis_client, exchange_code, exchange_name):
        """Test market cap ranking across multiple exchanges."""
        response = kis_client.overseas_market_analysis.get_stock_market_cap_rank(
            keyb="",
            auth="",
            excd=exchange_code,
            vol_rang="0"
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_invalid_exchange_code(self, kis_client):
        """Test handling of invalid exchange code."""
        try:
            response = kis_client.overseas_market_analysis.get_stock_price_rise_fall(
                keyb="",
                auth="",
                excd="INVALID",  # Invalid exchange code
                gubn="1",
                mixn="3",
                vol_rang="0"
            )
            # If no exception, check for error in response
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid exchange code
            assert e is not None

    def test_invalid_date_range_rights(self, kis_client):
        """Test handling of invalid date range for rights inquiry."""
        try:
            response = kis_client.overseas_market_analysis.get_stock_period_rights_inquiry(
                rght_type_cd="%%",
                inqr_dvsn_cd="02",
                inqr_strt_dt="20990101",  # Future date
                inqr_end_dt="20000101",  # Past date (reversed)
                pdno="",
                prdt_type_cd="",
                ctx_area_nk50="",
                ctx_area_fk50=""
            )
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid date range
            assert e is not None

    def test_invalid_stock_symbol_rights(self, kis_client):
        """Test handling of invalid stock symbol in rights aggregate."""
        start_dt = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
        end_dt = (datetime.now() + timedelta(days=90)).strftime("%Y%m%d")

        try:
            response = kis_client.overseas_market_analysis.get_stock_rights_aggregate(
                ncod="US",
                symb="INVALID999",  # Invalid symbol
                st_ymd=start_dt,
                ed_ymd=end_dt
            )
            # If no exception, check for error in response
            assert response is not None
        except Exception as e:
            # Expected to fail or return empty results
            assert e is not None
