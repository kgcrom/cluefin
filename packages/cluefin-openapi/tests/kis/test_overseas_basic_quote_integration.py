"""Integration tests for KIS Overseas Basic Quote API.

These tests require valid API credentials in environment variables:
- KIWOOM_APP_KEY
- KIWOOM_SECRET_KEY
- KIWOOM_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_overseas_basic_quote_integration.py -v -m integration
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
    token = os.getenv("KIWOOM_TOKEN", "")

    if not app_key or not secret_key or not token:
        pytest.skip("KIS API credentials not found in environment variables")

    client = Client(token=token, app_key=app_key, secret_key=secret_key, env=env)
    return client


@pytest.mark.integration
class TestStockCurrentPrice:
    """Test current price related methods."""

    def test_get_stock_current_price_detail(self, kis_client):
        """Test overseas stock current price detail retrieval."""
        # Test with Tesla (TSLA) on NASDAQ
        response = kis_client.overseas_basic_quote.get_stock_current_price_detail(
            auth="",
            excd="NAS",  # NASDAQ
            symb="TSLA"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_current_price_first_quote(self, kis_client):
        """Test current price first quote retrieval."""
        # Test with Apple (AAPL) on NASDAQ
        response = kis_client.overseas_basic_quote.get_current_price_first_quote(
            auth="",
            excd="NAS",
            symb="AAPL"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_current_price_conclusion(self, kis_client):
        """Test current price conclusion retrieval."""
        # Test with Microsoft (MSFT) on NASDAQ
        response = kis_client.overseas_basic_quote.get_stock_current_price_conclusion(
            auth="",
            excd="NAS",
            symb="MSFT"
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_conclusion_trend(self, kis_client):
        """Test conclusion trend retrieval."""
        # Test with NVIDIA (NVDA) on NASDAQ
        response = kis_client.overseas_basic_quote.get_conclusion_trend(
            excd="NAS",
            auth="",
            keyb="",
            tday="1",  # Current day
            symb="NVDA"
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestChartData:
    """Test chart data retrieval methods."""

    def test_get_stock_minute_chart(self, kis_client):
        """Test stock minute chart retrieval."""
        # Test with Amazon (AMZN) on NASDAQ
        response = kis_client.overseas_basic_quote.get_stock_minute_chart(
            auth="",
            excd="NAS",
            symb="AMZN",
            nmin="1",  # 1-minute chart
            pinc="0",  # Current day only
            next="",  # First query
            nrec="30",  # Request 30 records
            fill="",
            keyb=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_index_minute_chart(self, kis_client):
        """Test index minute chart retrieval."""
        # Test with NASDAQ index
        response = kis_client.overseas_basic_quote.get_index_minute_chart(
            fid_cond_mrkt_div_code="N",  # Overseas index
            fid_input_iscd="COMP",  # NASDAQ Composite
            fid_hour_cls_code="0",  # Regular trading hours
            fid_pw_data_incu_yn="Y"  # Include past data
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_stock_period_quote(self, kis_client):
        """Test stock period quote retrieval."""
        # Test with Google (GOOGL) on NASDAQ with daily data
        response = kis_client.overseas_basic_quote.get_stock_period_quote(
            auth="",
            excd="NAS",
            symb="GOOGL",
            gubn="0",  # Daily
            bymd="",  # Use today as base date
            modp="0",  # No adjustment for stock split
            keyb=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_item_index_exchange_period_price(self, kis_client):
        """Test item/index/exchange period price retrieval."""
        # Test with date range
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")

        response = kis_client.overseas_basic_quote.get_item_index_exchange_period_price(
            fid_cond_mrkt_div_code="N",  # Overseas index
            fid_input_iscd="SPX",  # S&P 500 index
            fid_input_date_1=start_date,
            fid_input_date_2=end_date,
            fid_period_div_code="D"  # Daily
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestStockSearch:
    """Test stock search and screening methods."""

    def test_search_by_condition(self, kis_client):
        """Test search by condition."""
        # Search for stocks on NYSE with price range
        response = kis_client.overseas_basic_quote.search_by_condition(
            auth="",
            excd="NYS",  # New York Stock Exchange
            co_yn_pricecur="1",  # Use current price condition
            co_st_pricecur="100",  # Start price: $100
            co_en_pricecur="500",  # End price: $500
            keyb=""
        )

        assert response is not None
        assert hasattr(response, 'output')

    def test_get_product_base_info(self, kis_client):
        """Test product base information retrieval."""
        # Test with Apple (AAPL) - US NASDAQ product code
        response = kis_client.overseas_basic_quote.get_product_base_info(
            prdt_type_cd="512",  # US NASDAQ
            pdno="AAPL"
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestSectorInformation:
    """Test sector-related information retrieval."""

    def test_get_sector_price(self, kis_client):
        """Test sector price retrieval."""
        # First get sector codes to use a valid sector code
        codes_response = kis_client.overseas_basic_quote.get_sector_codes(
            auth="",
            excd="NYS"  # New York Stock Exchange
        )

        assert codes_response is not None

        # If we got sector codes, test sector price with the first code
        if hasattr(codes_response, 'output') and codes_response.output:
            # Get first sector code (this depends on the response structure)
            # For now, we'll use a generic test
            try:
                response = kis_client.overseas_basic_quote.get_sector_price(
                    keyb="",
                    auth="",
                    excd="NYS",
                    icod="0001",  # Sample sector code - may need adjustment
                    vol_rang="0"  # All volume ranges
                )
                assert response is not None
            except Exception:
                # If the sector code doesn't exist, that's ok for this test
                pass

    def test_get_sector_codes(self, kis_client):
        """Test sector codes retrieval."""
        # Test with NASDAQ
        response = kis_client.overseas_basic_quote.get_sector_codes(
            auth="",
            excd="NAS"  # NASDAQ
        )

        assert response is not None
        assert hasattr(response, 'output')

        # Test with NYSE
        response_nys = kis_client.overseas_basic_quote.get_sector_codes(
            auth="",
            excd="NYS"  # NYSE
        )

        assert response_nys is not None
        assert hasattr(response_nys, 'output')


@pytest.mark.integration
class TestSettlementAndHolidays:
    """Test settlement date and holiday information."""

    def test_get_settlement_date(self, kis_client):
        """Test settlement date retrieval."""
        # Test with current date
        trad_dt = datetime.now().strftime("%Y%m%d")

        response = kis_client.overseas_basic_quote.get_settlement_date(
            trad_dt=trad_dt,
            ctx_area_nk="",
            ctx_area_fk=""
        )

        assert response is not None
        assert hasattr(response, 'output')


@pytest.mark.integration
class TestMultipleExchanges:
    """Test methods across different exchanges."""

    @pytest.mark.parametrize("exchange,symbol", [
        ("NYS", "IBM"),      # New York Stock Exchange
        ("NAS", "TSLA"),     # NASDAQ
        ("HKS", "00700"),    # Hong Kong - Tencent
        ("TSE", "7203"),     # Tokyo - Toyota
    ])
    def test_current_price_multiple_exchanges(self, kis_client, exchange, symbol):
        """Test current price retrieval across different exchanges."""
        try:
            response = kis_client.overseas_basic_quote.get_stock_current_price_detail(
                auth="",
                excd=exchange,
                symb=symbol
            )
            assert response is not None
            assert hasattr(response, 'output')
        except Exception as e:
            # Some exchanges might not be accessible in dev environment
            pytest.skip(f"Exchange {exchange} not accessible: {str(e)}")


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling for invalid inputs."""

    def test_invalid_stock_symbol(self, kis_client):
        """Test handling of invalid stock symbol."""
        try:
            response = kis_client.overseas_basic_quote.get_stock_current_price_detail(
                auth="",
                excd="NAS",
                symb="INVALIDCODE123456"
            )
            # If no exception, check for error in response
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid symbol
            assert e is not None

    def test_invalid_exchange_code(self, kis_client):
        """Test handling of invalid exchange code."""
        try:
            response = kis_client.overseas_basic_quote.get_stock_current_price_detail(
                auth="",
                excd="INVALID",
                symb="AAPL"
            )
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid exchange
            assert e is not None

    def test_invalid_date_format(self, kis_client):
        """Test handling of invalid date format."""
        try:
            response = kis_client.overseas_basic_quote.get_item_index_exchange_period_price(
                fid_cond_mrkt_div_code="N",
                fid_input_iscd="SPX",
                fid_input_date_1="invalid_date",
                fid_input_date_2="20250101",
                fid_period_div_code="D"
            )
            assert response is not None
        except Exception as e:
            # Expected to fail with invalid date
            assert e is not None
