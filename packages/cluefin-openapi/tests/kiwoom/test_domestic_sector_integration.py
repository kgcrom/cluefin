from datetime import datetime

import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_sector_types import (
    DomesticSectorAllIndustryIndex,
    DomesticSectorDailyIndustryCurrentPrice,
    DomesticSectorIndustryCurrentPrice,
    DomesticSectorIndustryInvestorNetBuy,
    DomesticSectorIndustryPriceBySector,
    DomesticSectorIndustryProgram,
)


@pytest.mark.integration
def test_get_industry_program(client: Client):
    # Test parameters
    stk_code = "005930"  # Example sector code

    # Make the API call
    response = client.sector.get_industry_program(stk_code=stk_code)

    # Verify response structure
    assert response is not None
    assert response.headers is not None
    assert response.body is not None

    # Verify response body type
    assert isinstance(response.body, DomesticSectorIndustryProgram)


@pytest.mark.integration
def test_get_industry_investor_net_buy(client: Client):
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


@pytest.mark.integration
def test_get_industry_current_price_success(client: Client):
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


@pytest.mark.integration
def test_get_industry_price_by_sector_success(client: Client):
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


@pytest.mark.integration
def test_get_all_industry_index_success(client: Client):
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


@pytest.mark.integration
def test_get_daily_industry_current_price_success(client: Client):
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
