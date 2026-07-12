import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_chart_types import (
    OverseasChartDaily,
    OverseasChartMinute,
    OverseasChartMonthly,
    OverseasChartQuarterly,
    OverseasChartTick,
    OverseasChartWeekly,
    OverseasChartYearly,
)


@pytest.mark.integration
def test_get_tick_chart(client: Client):
    response = client.overseas_chart.get_tick_chart(
        stex_tp="ND", stk_cd="AAPL", tic_scope="1", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartTick)


@pytest.mark.integration
def test_get_minute_chart(client: Client):
    response = client.overseas_chart.get_minute_chart(
        stex_tp="ND",
        stk_cd="AAPL",
        strt_dt="20240102",
        tic_scope="1",
        upd_stkpc_tp="0",
        exrt_appl_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartMinute)


@pytest.mark.integration
def test_get_daily_chart(client: Client):
    response = client.overseas_chart.get_daily_chart(
        stex_tp="ND", stk_cd="AAPL", strt_dt="20240102", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartDaily)


@pytest.mark.integration
def test_get_weekly_chart(client: Client):
    response = client.overseas_chart.get_weekly_chart(
        stex_tp="ND", stk_cd="AAPL", strt_dt="20240102", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartWeekly)


@pytest.mark.integration
def test_get_monthly_chart(client: Client):
    response = client.overseas_chart.get_monthly_chart(
        stex_tp="ND", stk_cd="AAPL", strt_dt="20240102", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartMonthly)


@pytest.mark.integration
def test_get_yearly_chart(client: Client):
    response = client.overseas_chart.get_yearly_chart(
        stex_tp="ND", stk_cd="AAPL", strt_dt="20240102", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartYearly)


@pytest.mark.integration
def test_get_quarterly_chart(client: Client):
    response = client.overseas_chart.get_quarterly_chart(
        stex_tp="ND", stk_cd="AAPL", strt_dt="20240102", upd_stkpc_tp="0", exrt_appl_tp="0"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasChartQuarterly)
