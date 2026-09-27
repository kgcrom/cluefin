import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_theme_types import (
    DomesticThemeGroup,
    DomesticThemeGroupStocks,
)

from ._spec_conformance import assert_spec_conformance


@pytest.mark.integration
def test_get_theme_group(client: Client):
    # 문서 요청 예시값. 문서에서 qry_tp "1"(테마검색)이 빠졌고 thema_nm 은 "삭제 예정" 이다 —
    # 전엔 qry_tp="1", thema_nm="test" 로 빈 결과를 받고 통과했다
    response = client.theme.get_theme_group(
        qry_tp="0",
        date_tp="10",
        thema_nm="",
        flu_pl_amt_tp="1",
        stex_tp="1",
    )
    assert_spec_conformance(client, response)
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticThemeGroup)


@pytest.mark.integration
def test_get_theme_group_stocks(client: Client):
    response = client.theme.get_theme_group_stocks(date_tp="2", thema_grp_cd="100", stex_tp="1")
    assert_spec_conformance(client, response)
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, DomesticThemeGroupStocks)
