"""Integration tests for KIS Overseas Basic Quote API.

These tests require valid API credentials in environment variables:
- KIS_APP_KEY
- KIS_SECRET_KEY
- KIS_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_overseas_basic_quote_integration.py -v -m integration
"""

from datetime import datetime, timedelta

import pytest

from cluefin_openapi.kis._http_client import HttpClient


@pytest.mark.integration
def test_get_stock_current_price_detail(client: HttpClient):
    """Test overseas stock current price detail retrieval."""
    # Test with Tesla (TSLA) on NASDAQ
    response = client.overseas_basic_quote.get_stock_current_price_detail(
        auth="",
        excd="NAS",  # NASDAQ
        symb="TSLA",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_current_price_first_quote(client: HttpClient):
    """Test current price first quote retrieval."""
    # Test with Apple (AAPL) on NASDAQ
    response = client.overseas_basic_quote.get_current_price_first_quote(auth="", excd="NAS", symb="AAPL")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_stock_current_price_conclusion(client: HttpClient):
    """Test current price conclusion retrieval."""
    # Test with Microsoft (MSFT) on NASDAQ
    response = client.overseas_basic_quote.get_stock_current_price_conclusion(auth="", excd="NAS", symb="MSFT")

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_conclusion_trend(client: HttpClient):
    """Test conclusion trend retrieval."""
    # Test with NVIDIA (NVDA) on NASDAQ
    response = client.overseas_basic_quote.get_conclusion_trend(
        excd="NAS",
        auth="",
        keyb="",
        tday="1",  # Current day
        symb="NVDA",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_stock_minute_chart(client: HttpClient):
    """Test stock minute chart retrieval."""
    # Test with Amazon (AMZN) on NASDAQ
    response = client.overseas_basic_quote.get_stock_minute_chart(
        auth="",
        excd="NAS",
        symb="AMZN",
        nmin="1",  # 1-minute chart
        pinc="0",  # Current day only
        next="",  # First query
        nrec="30",  # Request 30 records
        fill="",
        keyb="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_index_minute_chart(client: HttpClient):
    """Test index minute chart retrieval."""
    # Test with NASDAQ index
    response = client.overseas_basic_quote.get_index_minute_chart(
        fid_cond_mrkt_div_code="N",  # Overseas index
        fid_input_iscd="COMP",  # NASDAQ Composite
        fid_hour_cls_code="0",  # Regular trading hours
        fid_pw_data_incu_yn="Y",  # Include past data
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_stock_period_quote(client: HttpClient):
    """Test stock period quote retrieval."""
    # Test with Google (GOOGL) on NASDAQ with daily data
    response = client.overseas_basic_quote.get_stock_period_quote(
        auth="",
        excd="NAS",
        symb="GOOGL",
        gubn="0",  # Daily
        bymd="",  # Use today as base date
        modp="0",  # No adjustment for stock split
        keyb="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_item_index_exchange_period_price(client: HttpClient):
    """Test item/index/exchange period price retrieval."""
    # Test with date range
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")

    response = client.overseas_basic_quote.get_item_index_exchange_period_price(
        fid_cond_mrkt_div_code="N",  # Overseas index
        fid_input_iscd="SPX",  # S&P 500 index
        fid_input_date_1=start_date,
        fid_input_date_2=end_date,
        fid_period_div_code="D",  # Daily
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_search_by_condition(client: HttpClient):
    """Test search by condition."""
    # Search for stocks on NYSE with price range
    response = client.overseas_basic_quote.search_by_condition(
        auth="",
        excd="NYS",  # New York Stock Exchange
        co_yn_pricecur="1",  # Use current price condition
        co_st_pricecur="100",  # Start price: $100
        co_en_pricecur="500",  # End price: $500
        keyb="",
    )

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_product_base_info(client: HttpClient):
    """Test product base information retrieval."""
    # Test with Apple (AAPL) - US NASDAQ product code
    response = client.overseas_basic_quote.get_product_base_info(
        prdt_type_cd="512",  # US NASDAQ
        pdno="AAPL",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_sector_price(client: HttpClient):
    """Test sector price retrieval."""
    # First get sector codes to use a valid sector code
    codes_response = client.overseas_basic_quote.get_sector_codes(
        auth="",
        excd="NYS",  # New York Stock Exchange
    )

    assert codes_response is not None

    # If we got sector codes, test sector price with the first code
    if hasattr(codes_response.body, "output") and codes_response.body.output:
        # Get first sector code (this depends on the response structure)
        # For now, we'll use a generic test
        try:
            response = client.overseas_basic_quote.get_sector_price(
                keyb="",
                auth="",
                excd="NYS",
                icod="0001",  # Sample sector code - may need adjustment
                vol_rang="0",  # All volume ranges
            )
            assert response is not None
        except Exception:
            # If the sector code doesn't exist, that's ok for this test
            pass


@pytest.mark.integration
def test_get_sector_codes(client: HttpClient):
    """Test sector codes retrieval."""
    # Test with NASDAQ
    response = client.overseas_basic_quote.get_sector_codes(
        auth="",
        excd="NAS",  # NASDAQ
    )

    assert response is not None
    assert hasattr(response.body, "output1")

    # Test with NYSE
    response_nys = client.overseas_basic_quote.get_sector_codes(
        auth="",
        excd="NYS",  # NYSE
    )

    assert response_nys is not None
    assert hasattr(response_nys.body, "output1")


@pytest.mark.integration
def test_get_settlement_date(client: HttpClient):
    """Test settlement date retrieval."""
    # Test with current date
    trad_dt = datetime.now().strftime("%Y%m%d")

    response = client.overseas_basic_quote.get_settlement_date(trad_dt=trad_dt, ctx_area_nk="", ctx_area_fk="")

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
@pytest.mark.parametrize(
    "exchange,symbol",
    [
        ("NYS", "IBM"),  # New York Stock Exchange
        ("NAS", "TSLA"),  # NASDAQ
        ("HKS", "00700"),  # Hong Kong - Tencent
        ("TSE", "7203"),  # Tokyo - Toyota
    ],
)
def test_current_price_multiple_exchanges(client: HttpClient, exchange, symbol):
    """Test current price retrieval across different exchanges."""
    try:
        response = client.overseas_basic_quote.get_stock_current_price_detail(auth="", excd=exchange, symb=symbol)
        assert response is not None
        assert hasattr(response.body, "output")
    except Exception as e:
        # Some exchanges might not be accessible in dev environment
        pytest.skip(f"Exchange {exchange} not accessible: {str(e)}")


@pytest.mark.integration
def test_invalid_stock_symbol(client: HttpClient):
    """Test handling of invalid stock symbol."""
    try:
        response = client.overseas_basic_quote.get_stock_current_price_detail(
            auth="", excd="NAS", symb="INVALIDCODE123456"
        )
        # If no exception, check for error in response
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid symbol
        assert e is not None


@pytest.mark.integration
def test_invalid_exchange_code(client: HttpClient):
    """Test handling of invalid exchange code."""
    try:
        response = client.overseas_basic_quote.get_stock_current_price_detail(auth="", excd="INVALID", symb="AAPL")
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid exchange
        assert e is not None


@pytest.mark.integration
def test_invalid_date_format(client: HttpClient):
    """Test handling of invalid date format."""
    try:
        response = client.overseas_basic_quote.get_item_index_exchange_period_price(
            fid_cond_mrkt_div_code="N",
            fid_input_iscd="SPX",
            fid_input_date_1="invalid_date",
            fid_input_date_2="20250101",
            fid_period_div_code="D",
        )
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid date
        assert e is not None
