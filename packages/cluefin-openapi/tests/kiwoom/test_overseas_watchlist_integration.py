import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_watchlist_types import (
    OverseasWatchlistGroupDetail,
    OverseasWatchlistGroupList,
)

from ._spec_conformance import assert_spec_conformance


@pytest.mark.integration
def test_get_watchlist_group_list(client: Client):
    response = client.overseas_watchlist.get_watchlist_group_list()
    assert_spec_conformance(client, response)

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasWatchlistGroupList)


@pytest.mark.integration
def test_get_watchlist_group_detail(client: Client):
    response = client.overseas_watchlist.get_watchlist_group_detail(arn_grp_id="10")
    assert_spec_conformance(client, response)

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasWatchlistGroupDetail)
