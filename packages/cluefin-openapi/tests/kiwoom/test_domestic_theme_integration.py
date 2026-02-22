import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_theme_types import (
    DomesticThemeGroup,
    DomesticThemeGroupStocks,
)


@pytest.mark.integration
def test_get_theme_group(client: Client):
    response = client.theme.get_theme_group(
        qry_tp="1",
        date_tp="1",
        thema_nm="test",
        flu_pl_amt_tp="1",
        stex_tp="1",
    )
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticThemeGroup)


@pytest.mark.integration
def test_get_theme_group_stocks(client: Client):
    response = client.theme.get_theme_group_stocks(date_tp="2", thema_grp_cd="100", stex_tp="1")
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticThemeGroupStocks)
