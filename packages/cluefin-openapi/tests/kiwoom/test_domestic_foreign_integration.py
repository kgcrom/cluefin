import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_foreign_types import (
    DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner,
    DomesticForeignInvestorTradingTrendByStock,
    DomesticForeignStockInstitution,
)

from ._spec_conformance import assert_spec_conformance


@pytest.mark.integration
def test_get_foreign_investor_trading_trend_by_stock(client: Client):
    response = client.foreign.get_foreign_investor_trading_trend_by_stock("005930")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticForeignInvestorTradingTrendByStock)
    assert response.body.stk_frgnr is not None


@pytest.mark.integration
def test_get_stock_institution(client: Client):
    response = client.foreign.get_stock_institution("005930")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticForeignStockInstitution)
    assert response.body.pre is not None


@pytest.mark.integration
def test_get_consecutive_net_buy_sell_status_by_institution_foreigner(client: Client):
    response = client.foreign.get_consecutive_net_buy_sell_status_by_institution_foreigner("1", "001", "0", "0", "1")
    assert_spec_conformance(client, response)

    assert response is not None
    assert isinstance(response.body, DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner)
    assert len(response.body.orgn_frgnr_cont_trde_prst) > 0
