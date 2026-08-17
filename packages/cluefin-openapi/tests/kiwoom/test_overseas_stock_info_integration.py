import pytest

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._overseas_stock_info_types import (
    OverseasStockInfoEtfCategoryList,
    OverseasStockInfoEtfEtnList,
    OverseasStockInfoExchangeList,
    OverseasStockInfoGapUpDownEtf,
    OverseasStockInfoGapUpDownStock,
    OverseasStockInfoHighLowApproachEtf,
    OverseasStockInfoHighLowApproachStock,
    OverseasStockInfoHighLowApproachWatchlist,
    OverseasStockInfoIndexList,
    OverseasStockInfoNewHighLowEtf,
    OverseasStockInfoNewHighLowStock,
    OverseasStockInfoPriceByRangeEtf,
    OverseasStockInfoPriceByRangeStock,
    OverseasStockInfoPriceSurgeEtf,
    OverseasStockInfoPriceSurgeStock,
    OverseasStockInfoPriceSurgeWatchlist,
    OverseasStockInfoRemainingRatioSurgeEtf,
    OverseasStockInfoRemainingRatioSurgeStock,
    OverseasStockInfoSectorList,
    OverseasStockInfoStock,
    OverseasStockInfoStockList,
    OverseasStockInfoStockMemo,
    OverseasStockInfoVolumeConcentrationEtf,
    OverseasStockInfoVolumeConcentrationStock,
    OverseasStockInfoVolumeRenewalEtf,
    OverseasStockInfoVolumeRenewalStock,
    OverseasStockInfoVolumeRenewalWatchlist,
    OverseasStockInfoVolumeSurgeEtf,
    OverseasStockInfoVolumeSurgeStock,
    OverseasStockInfoYearlyFluctuationRateByEtfCategory,
    OverseasStockInfoYearlyFluctuationRateBySector,
    OverseasStockInfoYearlyFluctuationRateEtf,
    OverseasStockInfoYearlyFluctuationRateSector,
    OverseasStockInfoYearlyFluctuationRateStock,
)


@pytest.mark.integration
def test_get_exchange_list(client: Client):
    response = client.overseas_stock_info.get_exchange_list(stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoExchangeList)


@pytest.mark.integration
def test_get_stock_list(client: Client):
    response = client.overseas_stock_info.get_stock_list(stex_tp="ND")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoStockList)


@pytest.mark.integration
def test_get_stock(client: Client):
    response = client.overseas_stock_info.get_stock(stk_cd="AAPL", stex_tp="ND")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoStock)


@pytest.mark.integration
def test_get_stock_memo(client: Client):
    response = client.overseas_stock_info.get_stock_memo(input_list=[{"stex_tp": "ND", "stk_cd": "AAPL"}])

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoStockMemo)


@pytest.mark.integration
def test_get_sector_list(client: Client):
    response = client.overseas_stock_info.get_sector_list(gubun="%")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoSectorList)


@pytest.mark.integration
def test_get_index_list(client: Client):
    response = client.overseas_stock_info.get_index_list(index_qry_tp="NQ")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoIndexList)


@pytest.mark.integration
def test_get_etf_etn_list(client: Client):
    response = client.overseas_stock_info.get_etf_etn_list(stex_tp="ND")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoEtfEtnList)


@pytest.mark.integration
def test_get_etf_category_list(client: Client):
    response = client.overseas_stock_info.get_etf_category_list(gubun="1")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoEtfCategoryList)


@pytest.mark.integration
def test_get_volume_surge_stock(client: Client):
    response = client.overseas_stock_info.get_volume_surge_stock(
        stex_tp="1",
        inds_cd="000",
        tm="5",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeSurgeStock)


@pytest.mark.integration
def test_get_volume_surge_etf(client: Client):
    response = client.overseas_stock_info.get_volume_surge_etf(
        stex_tp="1",
        tm="5",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeSurgeEtf)


@pytest.mark.integration
def test_get_price_by_range_stock(client: Client):
    response = client.overseas_stock_info.get_price_by_range_stock(
        stex_tp="1",
        stk_tp="0",
        stk_cnd="0",
        inds_cd="000",
        trde_qty_tp="0",
        pric_cnd1="",
        pric_cnd2="",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoPriceByRangeStock)


@pytest.mark.integration
def test_get_price_by_range_etf(client: Client):
    response = client.overseas_stock_info.get_price_by_range_etf(
        stex_tp="1",
        stk_cnd="0",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        pric_cnd1="",
        pric_cnd2="",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoPriceByRangeEtf)


@pytest.mark.integration
def test_get_price_surge_stock(client: Client):
    response = client.overseas_stock_info.get_price_surge_stock(
        stex_tp="1",
        stk_tp="0",
        inds_cd="000",
        stk_cnd="0",
        flu_tp="1",
        tm_tp="1",
        tm="5",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoPriceSurgeStock)


@pytest.mark.integration
def test_get_price_surge_etf(client: Client):
    response = client.overseas_stock_info.get_price_surge_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        flu_tp="1",
        tm_tp="1",
        tm="5",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoPriceSurgeEtf)


@pytest.mark.integration
def test_get_price_surge_watchlist(client: Client):
    response = client.overseas_stock_info.get_price_surge_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        flu_tp="1",
        tm_tp="1",
        tm="5",
        stk_cnd="0",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoPriceSurgeWatchlist)


@pytest.mark.integration
def test_get_high_low_approach_stock(client: Client):
    response = client.overseas_stock_info.get_high_low_approach_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        high_low_tp="1",
        alacc_rt="0.5",
        stk_cnd="0",
        pric_cnd_st="0",
        pric_cnd_ed="0",
        trde_pric_cnd_st="0",
        trde_qty_cnd_fr="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoHighLowApproachStock)


@pytest.mark.integration
def test_get_high_low_approach_etf(client: Client):
    response = client.overseas_stock_info.get_high_low_approach_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        high_low_tp="1",
        alacc_rt="0.5",
        stk_cnd="0",
        pric_cnd_st="0",
        pric_cnd_ed="0",
        trde_pric_cnd_st="0",
        trde_qty_cnd_fr="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoHighLowApproachEtf)


@pytest.mark.integration
def test_get_high_low_approach_watchlist(client: Client):
    response = client.overseas_stock_info.get_high_low_approach_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        high_low_tp="1",
        alacc_rt="0.5",
        stk_cnd="0",
        pric_cnd_st="0",
        pric_cnd_ed="0",
        trde_pric_cnd_st="0",
        trde_qty_cnd_fr="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoHighLowApproachWatchlist)


@pytest.mark.integration
def test_get_volume_renewal_stock(client: Client):
    response = client.overseas_stock_info.get_volume_renewal_stock(
        stex_tp="1",
        stk_cd="000",
        trde_qty_tp="0",
        stk_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        dt_tp="5",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeRenewalStock)


@pytest.mark.integration
def test_get_volume_renewal_etf(client: Client):
    response = client.overseas_stock_info.get_volume_renewal_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        dt_tp="5",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeRenewalEtf)


@pytest.mark.integration
def test_get_volume_renewal_watchlist(client: Client):
    response = client.overseas_stock_info.get_volume_renewal_watchlist(
        stex_tp="1",
        stk_cd=[{"stex_tp": "ND", "stk_cd": "AAPL"}],
        trde_qty_tp="0",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        dt_tp="5",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeRenewalWatchlist)


@pytest.mark.integration
def test_get_new_high_low_stock(client: Client):
    response = client.overseas_stock_info.get_new_high_low_stock(
        stex_tp="1",
        stk_tp="0",
        inds_cd="000",
        stk_cnd="0",
        ntl_tp="1",
        high_low_tp="1",
        dt="20",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoNewHighLowStock)


@pytest.mark.integration
def test_get_new_high_low_etf(client: Client):
    response = client.overseas_stock_info.get_new_high_low_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        stk_cnd="0",
        ntl_tp="1",
        high_low_tp="1",
        dt="20",
        pric_cnd="0",
        trde_qty_tp="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoNewHighLowEtf)


@pytest.mark.integration
def test_get_gap_up_down_stock(client: Client):
    response = client.overseas_stock_info.get_gap_up_down_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        sort_tp="1",
        updown_tp="1",
        alacc_rt="3",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoGapUpDownStock)


@pytest.mark.integration
def test_get_gap_up_down_etf(client: Client):
    response = client.overseas_stock_info.get_gap_up_down_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        sort_tp="1",
        updown_tp="1",
        alacc_rt="3",
        stk_cnd="0",
        pric_cnd="0",
        trde_prica_cnd="0",
        trde_qty_tp="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoGapUpDownEtf)


@pytest.mark.integration
def test_get_remaining_ratio_surge_stock(client: Client):
    response = client.overseas_stock_info.get_remaining_ratio_surge_stock(
        stex_tp="1",
        inds_cd="000",
        rt_tp="0",
        stk_tp="0",
        tm="5",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoRemainingRatioSurgeStock)


@pytest.mark.integration
def test_get_remaining_ratio_surge_etf(client: Client):
    response = client.overseas_stock_info.get_remaining_ratio_surge_etf(
        stex_tp="1",
        rt_tp="0",
        etf_cat1="",
        etf_cat2="",
        tm="5",
        stk_cnd="0",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoRemainingRatioSurgeEtf)


@pytest.mark.integration
def test_get_volume_concentration_stock(client: Client):
    response = client.overseas_stock_info.get_volume_concentration_stock(
        stex_tp="1",
        inds_cd="000",
        stk_tp="0",
        dt="20",
        prps_cnctr_rt="50",
        cond="0",
        prpscnt="10",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeConcentrationStock)


@pytest.mark.integration
def test_get_volume_concentration_etf(client: Client):
    response = client.overseas_stock_info.get_volume_concentration_etf(
        stex_tp="1",
        etf_cat1="",
        etf_cat2="",
        dt="20",
        prps_cnctr_rt="50",
        cond="0",
        prpscnt="10",
        trde_qty_tp="0",
        pric_cnd="0",
        trde_prica_cnd="0",
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoVolumeConcentrationEtf)


@pytest.mark.integration
def test_get_yearly_fluctuation_rate_stock(client: Client):
    response = client.overseas_stock_info.get_yearly_fluctuation_rate_stock(stex_tp="ND", stk_cd="AAPL")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoYearlyFluctuationRateStock)


@pytest.mark.integration
def test_get_yearly_fluctuation_rate_by_sector(client: Client):
    response = client.overseas_stock_info.get_yearly_fluctuation_rate_by_sector(inds_cd="000", srch_yr="2024")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoYearlyFluctuationRateBySector)


@pytest.mark.integration
def test_get_yearly_fluctuation_rate_by_etf_category(client: Client):
    response = client.overseas_stock_info.get_yearly_fluctuation_rate_by_etf_category(
        etf_cat1="", etf_cat2="", srch_yr="2024"
    )

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoYearlyFluctuationRateByEtfCategory)


@pytest.mark.integration
def test_get_yearly_fluctuation_rate_sector(client: Client):
    response = client.overseas_stock_info.get_yearly_fluctuation_rate_sector(inds_cd="000")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoYearlyFluctuationRateSector)


@pytest.mark.integration
def test_get_yearly_fluctuation_rate_etf(client: Client):
    response = client.overseas_stock_info.get_yearly_fluctuation_rate_etf(etf_cat1="", etf_cat2="")

    assert response is not None
    assert response.headers is not None
    assert response.body is not None
    assert isinstance(response.body, OverseasStockInfoYearlyFluctuationRateEtf)
