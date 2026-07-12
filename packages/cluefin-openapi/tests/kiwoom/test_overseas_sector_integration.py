import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_sector_types import (
    OverseasSectorIndustryFluctuationRank,
    OverseasSectorIndustryPeriodProfitRate,
)


@pytest.mark.integration
def test_get_industry_period_profit_rate(client: Client):
    response = client.overseas_sector.get_industry_period_profit_rate(stex_tp="3", inds_cd="000")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasSectorIndustryPeriodProfitRate)


@pytest.mark.integration
def test_get_industry_fluctuation_rank(client: Client):
    response = client.overseas_sector.get_industry_fluctuation_rank(stex_tp="3", sort_tp="1", inds_cd="000")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasSectorIndustryFluctuationRank)
