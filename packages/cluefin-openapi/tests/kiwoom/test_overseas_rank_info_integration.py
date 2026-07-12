import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_rank_info_types import (
    OverseasRankInfoConsecutiveRiseFallRankEtf,
    OverseasRankInfoConsecutiveRiseFallRankStock,
    OverseasRankInfoConsecutiveRiseFallRankWatchlist,
    OverseasRankInfoCumulativeFluctuationTopEtf,
    OverseasRankInfoCumulativeFluctuationTopStock,
    OverseasRankInfoDaytimeTradingDisparityTopEtf,
    OverseasRankInfoDaytimeTradingDisparityTopStock,
    OverseasRankInfoHighLowPriceRiseFallEtf,
    OverseasRankInfoHighLowPriceRiseFallStock,
    OverseasRankInfoKiwoomTradingTopEtf,
    OverseasRankInfoKiwoomTradingTopStock,
    OverseasRankInfoMarketCapTopEtf,
    OverseasRankInfoMarketCapTopStock,
    OverseasRankInfoOpenPriceFluctuationRankEtf,
    OverseasRankInfoOpenPriceFluctuationRankStock,
    OverseasRankInfoOpenPriceFluctuationRankWatchlist,
    OverseasRankInfoPeriodFluctuationRankEtf,
    OverseasRankInfoPeriodFluctuationRankStock,
    OverseasRankInfoPeriodFluctuationRankWatchlist,
    OverseasRankInfoPreviousDayFluctuationRankEtf,
    OverseasRankInfoPreviousDayFluctuationRankStock,
    OverseasRankInfoPreviousDayTradingTopEtf,
    OverseasRankInfoPreviousDayTradingTopStock,
    OverseasRankInfoQuoteRemainingVolumeTopEtf,
    OverseasRankInfoQuoteRemainingVolumeTopStock,
    OverseasRankInfoRealtimeSymbolQueryRank,
    OverseasRankInfoSpecificDateRiseFallEtf,
    OverseasRankInfoSpecificDateRiseFallStock,
    OverseasRankInfoTodayTradingValueTopEtf,
    OverseasRankInfoTodayTradingValueTopStock,
    OverseasRankInfoTodayTradingVolumeTopEtf,
    OverseasRankInfoTodayTradingVolumeTopStock,
    OverseasRankInfoTurnoverRateTopEtf,
    OverseasRankInfoTurnoverRateTopStock,
    OverseasRankInfoWatchlistRegistrationTop,
)


@pytest.mark.integration
def test_get_realtime_symbol_query_rank(client: Client):
    response = client.overseas_rank_info.get_realtime_symbol_query_rank(svc_type="B286")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoRealtimeSymbolQueryRank)


@pytest.mark.integration
def test_get_watchlist_registration_top(client: Client):
    response = client.overseas_rank_info.get_watchlist_registration_top(dt_unit_tp="D", stk_tp="A")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoWatchlistRegistrationTop)


@pytest.mark.integration
def test_get_period_fluctuation_rank_stock(client: Client):
    response = client.overseas_rank_info.get_period_fluctuation_rank_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        stk_cnd="0",
        tm="1",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPeriodFluctuationRankStock)


@pytest.mark.integration
def test_get_period_fluctuation_rank_etf(client: Client):
    response = client.overseas_rank_info.get_period_fluctuation_rank_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        tm="1",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPeriodFluctuationRankEtf)


@pytest.mark.integration
def test_get_period_fluctuation_rank_watchlist(client: Client):
    response = client.overseas_rank_info.get_period_fluctuation_rank_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        tm="1",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPeriodFluctuationRankWatchlist)


@pytest.mark.integration
def test_get_today_trading_volume_top_stock(client: Client):
    response = client.overseas_rank_info.get_today_trading_volume_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        trde_qty_tp="0",
        qry_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTodayTradingVolumeTopStock)


@pytest.mark.integration
def test_get_today_trading_volume_top_etf(client: Client):
    response = client.overseas_rank_info.get_today_trading_volume_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        qry_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTodayTradingVolumeTopEtf)


@pytest.mark.integration
def test_get_today_trading_value_top_stock(client: Client):
    response = client.overseas_rank_info.get_today_trading_value_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTodayTradingValueTopStock)


@pytest.mark.integration
def test_get_today_trading_value_top_etf(client: Client):
    response = client.overseas_rank_info.get_today_trading_value_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTodayTradingValueTopEtf)


@pytest.mark.integration
def test_get_market_cap_top_stock(client: Client):
    response = client.overseas_rank_info.get_market_cap_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoMarketCapTopStock)


@pytest.mark.integration
def test_get_market_cap_top_etf(client: Client):
    response = client.overseas_rank_info.get_market_cap_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoMarketCapTopEtf)


@pytest.mark.integration
def test_get_kiwoom_trading_top_stock(client: Client):
    response = client.overseas_rank_info.get_kiwoom_trading_top_stock(qry_tp="1", dt_unit_tp="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoKiwoomTradingTopStock)


@pytest.mark.integration
def test_get_kiwoom_trading_top_etf(client: Client):
    response = client.overseas_rank_info.get_kiwoom_trading_top_etf(qry_tp="1", dt_unit_tp="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoKiwoomTradingTopEtf)


@pytest.mark.integration
def test_get_previous_day_fluctuation_rank_stock(client: Client):
    response = client.overseas_rank_info.get_previous_day_fluctuation_rank_stock(
        stex_tp="1",
        inds_cd="000",
        inds_cls_tp="0",
        sort_tp="1",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPreviousDayFluctuationRankStock)


@pytest.mark.integration
def test_get_previous_day_fluctuation_rank_etf(client: Client):
    response = client.overseas_rank_info.get_previous_day_fluctuation_rank_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        sort_tp="1",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPreviousDayFluctuationRankEtf)


@pytest.mark.integration
def test_get_open_price_fluctuation_rank_stock(client: Client):
    response = client.overseas_rank_info.get_open_price_fluctuation_rank_stock(
        stex_tp="1",
        inds_cd="000",
        trde_qty_tp="0",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        sort_tp="1",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoOpenPriceFluctuationRankStock)


@pytest.mark.integration
def test_get_open_price_fluctuation_rank_etf(client: Client):
    response = client.overseas_rank_info.get_open_price_fluctuation_rank_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        sort_tp="1",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoOpenPriceFluctuationRankEtf)


@pytest.mark.integration
def test_get_open_price_fluctuation_rank_watchlist(client: Client):
    response = client.overseas_rank_info.get_open_price_fluctuation_rank_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        sort_tp="1",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoOpenPriceFluctuationRankWatchlist)


@pytest.mark.integration
def test_get_cumulative_fluctuation_top_stock(client: Client):
    response = client.overseas_rank_info.get_cumulative_fluctuation_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        sort_tp="0",
        pric_cnd1="",
        pric_cnd2="",
        base_dt="20240102",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoCumulativeFluctuationTopStock)


@pytest.mark.integration
def test_get_cumulative_fluctuation_top_etf(client: Client):
    response = client.overseas_rank_info.get_cumulative_fluctuation_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        sort_tp="0",
        pric_cnd1="",
        pric_cnd2="",
        base_dt="20240102",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoCumulativeFluctuationTopEtf)


@pytest.mark.integration
def test_get_previous_day_trading_top_stock(client: Client):
    response = client.overseas_rank_info.get_previous_day_trading_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        qry_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPreviousDayTradingTopStock)


@pytest.mark.integration
def test_get_previous_day_trading_top_etf(client: Client):
    response = client.overseas_rank_info.get_previous_day_trading_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        qry_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoPreviousDayTradingTopEtf)


@pytest.mark.integration
def test_get_high_low_price_rise_fall_stock(client: Client):
    response = client.overseas_rank_info.get_high_low_price_rise_fall_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        sort_tp="0",
        dt_tp="0",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoHighLowPriceRiseFallStock)


@pytest.mark.integration
def test_get_high_low_price_rise_fall_etf(client: Client):
    response = client.overseas_rank_info.get_high_low_price_rise_fall_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        sort_tp="0",
        dt_tp="0",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoHighLowPriceRiseFallEtf)


@pytest.mark.integration
def test_get_specific_date_rise_fall_stock(client: Client):
    response = client.overseas_rank_info.get_specific_date_rise_fall_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
        base_dt="20240102",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoSpecificDateRiseFallStock)


@pytest.mark.integration
def test_get_specific_date_rise_fall_etf(client: Client):
    response = client.overseas_rank_info.get_specific_date_rise_fall_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
        base_dt="20240102",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoSpecificDateRiseFallEtf)


@pytest.mark.integration
def test_get_turnover_rate_top_stock(client: Client):
    response = client.overseas_rank_info.get_turnover_rate_top_stock(
        stex_tp="1",
        inds_cd="000",
        trde_qty_tp="0",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTurnoverRateTopStock)


@pytest.mark.integration
def test_get_turnover_rate_top_etf(client: Client):
    response = client.overseas_rank_info.get_turnover_rate_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoTurnoverRateTopEtf)


@pytest.mark.integration
def test_get_consecutive_rise_fall_rank_stock(client: Client):
    response = client.overseas_rank_info.get_consecutive_rise_fall_rank_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoConsecutiveRiseFallRankStock)


@pytest.mark.integration
def test_get_consecutive_rise_fall_rank_etf(client: Client):
    response = client.overseas_rank_info.get_consecutive_rise_fall_rank_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoConsecutiveRiseFallRankEtf)


@pytest.mark.integration
def test_get_consecutive_rise_fall_rank_watchlist(client: Client):
    response = client.overseas_rank_info.get_consecutive_rise_fall_rank_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoConsecutiveRiseFallRankWatchlist)


@pytest.mark.integration
def test_get_quote_remaining_volume_top_stock(client: Client):
    response = client.overseas_rank_info.get_quote_remaining_volume_top_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        sort_tp="1",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoQuoteRemainingVolumeTopStock)


@pytest.mark.integration
def test_get_quote_remaining_volume_top_etf(client: Client):
    response = client.overseas_rank_info.get_quote_remaining_volume_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        sort_tp="1",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoQuoteRemainingVolumeTopEtf)


@pytest.mark.integration
def test_get_daytime_trading_disparity_top_stock(client: Client):
    response = client.overseas_rank_info.get_daytime_trading_disparity_top_stock(
        stex_tp="1",
        inds_cd="000",
        inds_cls_tp="0",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoDaytimeTradingDisparityTopStock)


@pytest.mark.integration
def test_get_daytime_trading_disparity_top_etf(client: Client):
    response = client.overseas_rank_info.get_daytime_trading_disparity_top_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
        sort_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasRankInfoDaytimeTradingDisparityTopEtf)
