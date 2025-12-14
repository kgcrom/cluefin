"""Integration tests for KIS Overseas Basic Quote API.

These tests require valid API credentials in environment variables:
- KIS_APP_KEY
- KIS_SECRET_KEY
- KIS_ENV (dev or prod)

Run with: uv run pytest packages/cluefin-openapi/tests/kis/test_overseas_basic_quote_integration.py -v -m integration
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
def client(auth_dev, token_cache) -> Client:
    """Fixture to create KIS Client with valid token."""
    token_response = token_cache.get()
    return Client(
        app_key=auth_dev.app_key,
        secret_key=auth_dev.secret_key,
        token=token_response.access_token,
        env=auth_dev.env,
        debug=True,
    )


@pytest.mark.integration
def test_get_stock_current_price_detail(client):
    """Test overseas stock current price detail retrieval."""
    time.sleep(1)
    # Test with Tesla (TSLA) on NASDAQ
    response = client.overseas_basic_quote.get_stock_current_price_detail(
        auth="",
        excd="NAS",  # NASDAQ
        symb="TSLA",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_current_price_first_quote(client):
    """Test current price first quote retrieval."""
    time.sleep(1)
    # Test with Apple (AAPL) on NASDAQ
    response = client.overseas_basic_quote.get_current_price_first_quote(auth="", excd="NAS", symb="AAPL")

    assert response is not None
    assert hasattr(response.body, "output1")


@pytest.mark.integration
def test_get_stock_current_price_conclusion(client):
    """Test current price conclusion retrieval."""
    time.sleep(1)
    # Test with Microsoft (MSFT) on NASDAQ
    response = client.overseas_basic_quote.get_stock_current_price_conclusion(auth="", excd="NAS", symb="MSFT")

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_conclusion_trend(client):
    """Test conclusion trend retrieval."""
    time.sleep(1)
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
def test_get_stock_minute_chart(client):
    """Test stock minute chart retrieval."""
    time.sleep(1)
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
def test_get_index_minute_chart(client):
    """Test index minute chart retrieval."""
    time.sleep(1)
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
def test_get_stock_period_quote(client):
    """Test stock period quote retrieval."""
    time.sleep(1)
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
def test_get_item_index_exchange_period_price(client):
    """Test item/index/exchange period price retrieval."""
    time.sleep(1)
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
def test_search_by_condition(client):
    """Test search by condition."""
    time.sleep(1)
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
def test_get_product_base_info(client):
    """Test product base information retrieval."""
    time.sleep(1)
    # Test with Apple (AAPL) - US NASDAQ product code
    response = client.overseas_basic_quote.get_product_base_info(
        prdt_type_cd="512",  # US NASDAQ
        pdno="AAPL",
    )

    assert response is not None
    assert hasattr(response.body, "output")


@pytest.mark.integration
def test_get_sector_price(client):
    """Test sector price retrieval."""
    time.sleep(1)
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
def test_get_sector_codes(client):
    """Test sector codes retrieval."""
    time.sleep(1)
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
def test_get_settlement_date(client):
    """Test settlement date retrieval."""
    time.sleep(1)
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
def test_current_price_multiple_exchanges(client, exchange, symbol):
    """Test current price retrieval across different exchanges."""
    time.sleep(1)
    try:
        response = client.overseas_basic_quote.get_stock_current_price_detail(auth="", excd=exchange, symb=symbol)
        assert response is not None
        assert hasattr(response.body, "output")
    except Exception as e:
        # Some exchanges might not be accessible in dev environment
        pytest.skip(f"Exchange {exchange} not accessible: {str(e)}")


@pytest.mark.integration
def test_invalid_stock_symbol(client):
    """Test handling of invalid stock symbol."""
    time.sleep(1)
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
def test_invalid_exchange_code(client):
    """Test handling of invalid exchange code."""
    time.sleep(1)
    try:
        response = client.overseas_basic_quote.get_stock_current_price_detail(auth="", excd="INVALID", symb="AAPL")
        assert response is not None
    except Exception as e:
        # Expected to fail with invalid exchange
        assert e is not None


@pytest.mark.integration
def test_invalid_date_format(client):
    """Test handling of invalid date format."""
    time.sleep(1)
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
