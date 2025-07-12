"""Integration tests for the DomesticSector class."""

import os
import time
from datetime import datetime

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_sector_types import (
    DomesticSectorAllIndustryIndex,
    DomesticSectorDailyIndustryCurrentPrice,
    DomesticSectorIndustryCurrentPrice,
    DomesticSectorIndustryInvestorNetBuy,
    DomesticSectorIndustryPriceBySector,
    DomesticSectorIndustryProgram,
)


@pytest.fixture
def auth() -> Auth:
    dotenv.load_dotenv(dotenv_path=".env.test")
    return Auth(
        app_key=os.getenv("APP_KEY"),
        secret_key=os.getenv("SECRET_KEY"),
        env="dev",
    )


@pytest.fixture
def client(auth: Auth) -> Client:
    """Create a Client instance for testing.

    Args:
        auth (Auth): The authenticated Auth instance.

    Returns:
        Client: A configured Client instance.
    """
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_industry_program(client: Client):
    """Test the get_industry_program method with actual API call.

    This test verifies that:
    1. The API request succeeds with status code 200
    2. The response data matches the expected DomesticSectorIndustryProgram model
    3. The response contains valid industry program data

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    stk_code = "005930"  # Example sector code
    cont_yn = None
    next_key = None

    # Make the API call
    response = client.sector.get_industry_program(stk_code=stk_code, cont_yn=cont_yn, next_key=next_key)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorIndustryProgram)


def test_get_industry_investor_net_buy(client: Client):
    """Test the get_industry_investor_net_buy method with actual API call.

    This test verifies that:
    1. The API request succeeds (the client method raises an exception on failure).
    2. The response data matches the expected DomesticSectorIndustryInvestorNetBuy model.
    3. The response contains valid industry investor net buy data.

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    mrkt_tp = "0"  # KOSPI
    amt_qty_tp = "0"  # Amount
    base_dt = datetime.now().strftime("%Y%m%d")  # Today's date
    stex_tp = "1"  # KRX

    # Make the API call
    response = client.sector.get_industry_investor_net_buy(
        mrkt_tp=mrkt_tp,
        amt_qty_tp=amt_qty_tp,
        base_dt=base_dt,
        stex_tp=stex_tp,
    )

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorIndustryInvestorNetBuy)


def test_get_industry_current_price_success(client: Client):
    """Test the get_industry_current_price method with actual API call.

    This test verifies that:
    1. The API request succeeds with status code 200
    2. The response data matches the expected DomesticSectorIndustryCurrentPrice model
    3. The response contains valid industry current price data

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    mrkt_tp = "0"  # KOSPI
    inds_cd = "001"  # Example industry code (KOSPI)

    # Make the API call
    response = client.sector.get_industry_current_price(mrkt_tp=mrkt_tp, inds_cd=inds_cd)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorIndustryCurrentPrice)


def test_get_industry_price_by_sector_success(client: Client):
    """Test the get_industry_price_by_sector method with actual API call.

    This test verifies that:
    1. The API request succeeds with status code 200
    2. The response data matches the expected DomesticSectorIndustryPriceBySector model
    3. The response contains valid industry price data

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    mrkt_tp = "0"  # KOSPI
    inds_cd = "001"  # Example industry code (KOSPI)
    stex_tp = "1"  # KRX

    # Make the API call
    response = client.sector.get_industry_price_by_sector(mrkt_tp=mrkt_tp, inds_cd=inds_cd, stex_tp=stex_tp)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorIndustryPriceBySector)


def test_get_all_industry_index_success(client: Client):
    """Test the get_all_industry_index method with actual API call.

    This test verifies that:
    1. The API request succeeds with status code 200
    2. The response data matches the expected DomesticSectorAllIndustryIndex model
    3. The response contains valid industry index data

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    inds_cd = "001"  # Example industry code (KOSPI)
    # Make the API call
    response = client.sector.get_all_industry_index(inds_cd=inds_cd)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorAllIndustryIndex)


def test_get_daily_industry_current_price_success(client: Client):
    """Test the get_daily_industry_current_price method with actual API call.

    This test verifies that:
    1. The API request succeeds with status code 200
    2. The response data matches the expected DomesticSectorIndustryCurrentPrice model
    3. The response contains valid industry current price data

    Args:
        client (Client): The Client instance.
    """
    time.sleep(1)
    # Test parameters
    mrkt_tp = "0"  # KOSPI
    inds_cd = "001"  # Example industry code (KOSPI)

    # Make the API call
    response = client.sector.get_daily_industry_current_price(mrkt_tp=mrkt_tp, inds_cd=inds_cd)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorDailyIndustryCurrentPrice)
