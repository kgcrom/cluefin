import os
import time

import dotenv
import pytest

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_rank_info_types import (
    DomesticRankInfoAfterHoursSinglePriceChangeRateRanking,
    DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity,
    DomesticRankInfoRapidlyIncreasingTotalSellOrders,
    DomesticRankInfoRapidlyIncreasingTradingVolume,
    DomesticRankInfoSameNetBuySellRanking,
    DomesticRankInfoStockSpecificSecuritiesFirmRanking,
    DomesticRankInfoTopConsecutiveNetBuySellByForeigners,
    DomesticRankInfoTopCurrentDayDeviationSources,
    DomesticRankInfoTopCurrentDayMajorTraders,
    DomesticRankInfoTopCurrentDayTradingVolume,
    DomesticRankInfoTopExpectedConclusionPercentageChange,
    DomesticRankInfoTopForeignAccountGroupTrading,
    DomesticRankInfoTopForeignerLimitExhaustionRate,
    DomesticRankInfoTopForeignerPeriodTrading,
    DomesticRankInfoTopIntradayTradingByInvestor,
    DomesticRankInfoTopLimitExhaustionRateForeigner,
    DomesticRankInfoTopMarginRatio,
    DomesticRankInfoTopNetBuyTraderRanking,
    DomesticRankInfoTopPercentageChangeFromPreviousDay,
    DomesticRankInfoTopPreviousDayTradingVolume,
    DomesticRankInfoTopRemainingOrderQuantity,
    DomesticRankInfoTopSecuritiesFirmTrading,
    DomesticRankInfoTopTransactionValue,
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
    token = auth.generate_token()
    return Client(token=token.token, env="dev")


def test_get_top_remaining_order_quantity(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_remaining_order_quantity(
        mrkt_tp="001", sort_tp="1", trde_qty_tp="0000", stk_cnd="0", crd_cnd="0", stex_tp="1"
    )

    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopRemainingOrderQuantity)
    assert len(response.body.bid_req_upper) > 0


def test_get_rapidly_increasing_remaining_order_quantity(client: Client):
    time.sleep(1)

    response = client.rank_info.get_rapidly_increasing_remaining_order_quantity(
        mrkt_tp="001", trde_tp="1", sort_tp="1", tm_tp="30", trde_qty_tp="1", stk_cnd="0", stex_tp="1"
    )

    assert response is not None
    assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingRemainingOrderQuantity)
    assert len(response.body.bid_req_sdnin) > 0


def test_get_rapidly_increasing_total_sell_orders(client: Client):
    time.sleep(1)

    response = client.rank_info.get_rapidly_increasing_total_sell_orders(
        mrkt_tp="001", rt_tp="1", tm_tp="1", trde_qty_tp="5", stk_cnd="0", stex_tp="1"
    )

    assert response is not None
    assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingTotalSellOrders)
    assert len(response.body.req_rt_sdnin) > 0


def test_get_rapidly_increasing_trading_volume(client: Client):
    time.sleep(1)

    response = client.rank_info.get_rapidly_increasing_trading_volume(
        mrkt_tp="000", sort_tp="1", tm_tp="2", trde_qty_tp="5", stk_cnd="0", pric_tp="0", stex_tp="1"
    )

    assert response is not None
    assert isinstance(response.body, DomesticRankInfoRapidlyIncreasingTradingVolume)
    assert len(response.body.trde_qty_sdnin) > 0


def test_get_top_percentage_change_from_previous_day(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_percentage_change_from_previous_day(
        mrkt_tp="000",
        sort_tp="1",
        trde_qty_cnd="0000",
        stk_cnd="0",
        crd_cnd="0",
        updown_incls="1",
        pric_cnd="0",
        trde_prica_cnd="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopPercentageChangeFromPreviousDay)
    assert len(response.body.pred_pre_flu_rt_upper) > 0


def test_get_top_expected_conclusion_percentage_change(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_expected_conclusion_percentage_change(
        mrkt_tp="000",
        sort_tp="1",
        trde_qty_cnd="0",
        stk_cnd="0",
        crd_cnd="0",
        pric_cnd="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopExpectedConclusionPercentageChange)
    assert len(response.body.exp_cntr_flu_rt_upper) > 0


def test_get_top_current_day_trading_volume(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_current_day_trading_volume(
        mrkt_tp="000",
        sort_tp="1",
        mang_stk_incls="0",
        crd_tp="0",
        trde_qty_tp="0",
        pric_tp="0",
        trde_prica_tp="0",
        mrkt_open_tp="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopCurrentDayTradingVolume)
    assert len(response.body.tdy_trde_qty_upper) > 0


def test_get_top_previous_day_trading_volume(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_previous_day_trading_volume(
        mrkt_tp="101", qry_tp="1", rank_strt="0", rank_end="10", stex_tp="1"
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopPreviousDayTradingVolume)
    assert len(response.body.pred_trde_qty_upper) > 0


def test_get_top_transaction_value(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_transaction_value(
        mrkt_tp="001",
        mang_stk_incls="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopTransactionValue)
    assert len(response.body.trde_prica_upper) > 0


def test_get_top_margin_ratio(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_margin_ratio(
        mrkt_tp="000",
        trde_qty_tp="0",
        stk_cnd="0",
        updown_incls="1",
        crd_cnd="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopMarginRatio)
    assert len(response.body.crd_rt_upper) > 0


def test_get_top_foreigner_period_trading(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_foreigner_period_trading(
        mrkt_tp="001",
        trde_tp="2",
        dt="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopForeignerPeriodTrading)
    assert len(response.body.for_dt_trde_upper) > 0


def test_get_top_consecutive_net_buy_sell_by_foreigners(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_consecutive_net_buy_sell_by_foreigners(
        mrkt_tp="000",
        trde_tp="2",
        base_dt_tp="1",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopConsecutiveNetBuySellByForeigners)
    assert len(response.body.for_cont_nettrde_upper) > 0


def test_get_top_limit_exhaustion_rate_foreigner(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_limit_exhaustion_rate_foreigner(
        mrkt_tp="000",
        dt="0",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopLimitExhaustionRateForeigner)
    assert len(response.body.for_limit_exh_rt_incrs_upper) > 0


def test_get_top_foreign_account_group_trading(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_foreign_account_group_trading(
        mrkt_tp="000", dt="0", trde_tp="1", sort_tp="2", stex_tp="1"
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopForeignAccountGroupTrading)
    assert len(response.body.frgn_wicket_trde_upper) > 0


def test_get_stock_specific_securities_firm_ranking(client: Client):
    time.sleep(1)

    response = client.rank_info.get_stock_specific_securities_firm_ranking(
        stk_cd="005930", strt_dt="20250601", end_dt="20250602", qry_tp="2", dt="1"
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoStockSpecificSecuritiesFirmRanking)
    assert response.body.rank_1 is not None
    assert len(response.body.stk_sec_rank) > 0


def test_get_top_securities_firm_trading(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_securities_firm_trading(
        mmcm_cd="001", trde_qty_tp="0", trde_tp="1", dt="1", stex_tp="1"
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopSecuritiesFirmTrading)
    assert len(response.body.sec_trde_upper) > 0


def test_get_top_current_day_major_traders(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_current_day_major_traders(stk_cd="005930")
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopCurrentDayMajorTraders)
    assert response.body.sel_trde_ori_1 is not None


def test_get_top_net_buy_trader_ranking(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_net_buy_trader_ranking(
        stk_cd="005930", strt_dt="20241031", end_dt="20241107", qry_dt_tp="0", pot_tp="0", dt="5", sort_base="1"
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopNetBuyTraderRanking)
    assert len(response.body.netprps_trde_ori_rank) > 0


def test_get_top_current_day_deviation_sources(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_current_day_deviation_sources(
        stk_cd="005930",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopCurrentDayDeviationSources)
    assert len(response.body.tdy_upper_scesn_ori) > 0


def test_get_same_net_buy_sell_ranking(client: Client):
    time.sleep(1)

    response = client.rank_info.get_same_net_buy_sell_ranking(
        strt_dt="20241106",
        end_dt="20241107",
        mrkt_tp="000",
        trde_tp="1",
        sort_cnd="1",
        unit_tp="1",
        stex_tp="1",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoSameNetBuySellRanking)
    assert len(response.body.eql_nettrde_rank) > 0


def test_get_top_intraday_trading_by_investor(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_intraday_trading_by_investor(
        trde_tp="1",
        mrkt_tp="000",
        orgn_tp="9000",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopIntradayTradingByInvestor)


def test_get_after_hours_single_price_change_rate_ranking(client: Client):
    time.sleep(1)

    response = client.rank_info.get_after_hours_single_price_change_rate_ranking(
        mrkt_tp="000",
        sort_base="5",
        stk_cnd="0",
        trde_qty_cnd="0",
        crd_cnd="0",
        trde_prica="0",
    )
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoAfterHoursSinglePriceChangeRateRanking)
    assert len(response.body.ovt_sigpric_flu_rt_rank) > 0


def test_get_top_foreigner_limit_exhaustion_rate(client: Client):
    time.sleep(1)

    response = client.rank_info.get_top_foreigner_limit_exhaustion_rate(mrkt_tp="001", dt="1", stex_tp="1")
    assert response is not None
    assert isinstance(response.body, DomesticRankInfoTopForeignerLimitExhaustionRate)
