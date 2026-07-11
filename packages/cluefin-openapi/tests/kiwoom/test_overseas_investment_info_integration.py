import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_investment_info_types import (
    OverseasInvestmentInfoResearch,
)


@pytest.mark.integration
def test_get_research(client: Client):
    response = client.overseas_investment_info.get_research(qry_tp="0")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasInvestmentInfoResearch)
