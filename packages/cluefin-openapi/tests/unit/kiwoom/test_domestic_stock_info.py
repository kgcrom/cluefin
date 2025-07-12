import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_stock_info_types import (
    DomesticStockInfoBasic,
    DomesticStockInfoBasicV1,
    DomesticStockInfoChangeRateFromOpen,
    DomesticStockInfoDailyPreviousDayConclusion,
    DomesticStockInfoDailyPreviousDayExecutionVolume,
    DomesticStockInfoDailyTradingDetails,
    DomesticStockInfoDailyTradingItemsByInvestor,
    DomesticStockInfoExecution,
    DomesticStockInfoHighLowPriceApproach,
    DomesticStockInfoHighPer,
    DomesticStockInfoIndustryCode,
    DomesticStockInfoInstitutionalInvestorByStock,
    DomesticStockInfoInterestStockInfo,
    DomesticStockInfoMarginTradingTrend,
    DomesticStockInfoMemberCompany,
    DomesticStockInfoNewHighLowPrice,
    DomesticStockInfoPriceVolatility,
    DomesticStockInfoProgramTradingStatusByStock,
    DomesticStockInfoSummary,
    DomesticStockInfoSupplyDemandConcentration,
    DomesticStockInfoTop50ProgramNetBuy,
    DomesticStockInfoTotalInstitutionalInvestorByStock,
    DomesticStockInfoTradingMember,
    DomesticStockInfoTradingMemberInstantVolume,
    DomesticStockInfoTradingMemberSupplyDemandAnalysis,
    DomesticStockInfoTradingVolumeRenewal,
    DomesticStockInfoUpperLowerLimitPrice,
    DomesticStockInfoVolatilityControlEvent,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_stock_info(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "setl_mm": "12",
        "fav": "5000",
        "cap": "1311",
        "flo_stk": "25527",
        "crd_rt": "+0.08",
        "oyr_hgst": "+181400",
        "oyr_lwst": "-91200",
        "mac": "24352",
        "mac_wght": "",
        "for_exh_rt": "0.00",
        "repl_pric": "66780",
        "per": "",
        "eps": "",
        "roe": "",
        "pbr": "",
        "ev": "",
        "bps": "-75300",
        "sale_amt": "0",
        "bus_pro": "0",
        "cup_nga": "0",
        "250hgst": "+124000",
        "250lwst": "-66800",
        "high_pric": "95400",
        "open_pric": "-0",
        "low_pric": "0",
        "upl_pric": "20241016",
        "lst_pric": "-47.41",
        "base_pric": "20231024",
        "exp_cntr_pric": "+26.69",
        "exp_cntr_qty": "95400",
        "250hgst_pric_dt": "3",
        "250hgst_pric_pre_rt": "0",
        "250lwst_pric_dt": "0.00",
        "250lwst_pric_pre_rt": "0",
        "cur_prc": "0.00",
        "pre_sig": "",
        "pred_pre": "",
        "flu_rt": "0",
        "trde_qty": "0",
        "trde_pre": "0",
        "fav_unit": "0",
        "dstr_stk": "0",
        "dstr_rt": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10001",
            },
        )
        response = client.stock_info.get_stock_info("005930")
        assert response is not None
        assert isinstance(response.body, DomesticStockInfoBasic)
        assert response.body.dstr_rt == "0"
        assert response.body.stk_cd == "005930"


def test_get_stock_trading_member(client: Client):
    expected_data = {
        "stk_cd": "005930",
        "stk_nm": "삼성전자",
        "cur_prc": "95400",
        "flu_smbol": "3",
        "base_pric": "95400",
        "pred_pre": "0",
        "flu_rt": "0.00",
        "sel_trde_ori_nm_1": "",
        "sel_trde_ori_1": "000",
        "sel_trde_qty_1": "0",
        "buy_trde_ori_nm_1": "",
        "buy_trde_ori_1": "000",
        "buy_trde_qty_1": "0",
        "sel_trde_ori_nm_2": "",
        "sel_trde_ori_2": "000",
        "sel_trde_qty_2": "0",
        "buy_trde_ori_nm_2": "",
        "buy_trde_ori_2": "000",
        "buy_trde_qty_2": "0",
        "sel_trde_ori_nm_3": "",
        "sel_trde_ori_3": "000",
        "sel_trde_qty_3": "0",
        "buy_trde_ori_nm_3": "",
        "buy_trde_ori_3": "000",
        "buy_trde_qty_3": "0",
        "sel_trde_ori_nm_4": "",
        "sel_trde_ori_4": "000",
        "sel_trde_qty_4": "0",
        "buy_trde_ori_nm_4": "",
        "buy_trde_ori_4": "000",
        "buy_trde_qty_4": "0",
        "sel_trde_ori_nm_5": "",
        "sel_trde_ori_5": "000",
        "sel_trde_qty_5": "0",
        "buy_trde_ori_nm_5": "",
        "buy_trde_ori_5": "000",
        "buy_trde_qty_5": "0",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10002",
            },
        )
        response = client.stock_info.get_stock_trading_member("005930")
        assert isinstance(response.body, DomesticStockInfoTradingMember)
        assert response.body.base_pric == "95400"


def test_get_execution_info(client: Client):
    expected_data = {
        "cntr_infr": [
            {
                "tm": "130429",
                "cur_prc": "+53500",
                "pred_pre": "+500",
                "pre_rt": "+0.94",
                "pri_sel_bid_unit": "+68900",
                "pri_buy_bid_unit": "+53500",
                "cntr_trde_qty": "1010",
                "sign": "2",
                "acc_trde_qty": "8735",
                "acc_trde_prica": "524269500",
                "cntr_str": "12.99",
                "stex_tp": "KRX",
            },
            {
                "tm": "130153",
                "cur_prc": "+68900",
                "pred_pre": "+15900",
                "pre_rt": "+30.00",
                "pri_sel_bid_unit": "+68900",
                "pri_buy_bid_unit": "+55000",
                "cntr_trde_qty": "456",
                "sign": "1",
                "acc_trde_qty": "7725",
                "acc_trde_prica": "470234500",
                "cntr_str": "12.99",
                "stex_tp": "KRX",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10003",
            },
        )
        response = client.stock_info.get_execution("005930")
        assert isinstance(response.body, DomesticStockInfoExecution)
        assert response.body.cntr_infr[0].cur_prc == "+53500"


def test_get_margin_trading_trend(client: Client):
    expected_data = {
        "crd_trde_trend": [
            {
                "dt": "20241101",
                "cur_prc": "65100",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "trde_qty": "0",
                "new": "",
                "rpya": "",
                "remn": "",
                "amt": "",
                "pre": "",
                "shr_rt": "",
                "remn_rt": "",
            },
            {
                "dt": "20241031",
                "cur_prc": "65100",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "trde_qty": "0",
                "new": "",
                "rpya": "",
                "remn": "",
                "amt": "",
                "pre": "",
                "shr_rt": "",
                "remn_rt": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10013",
            },
        )

        response = client.stock_info.get_margin_trading_trend(stk_cd="005930", dt="20250701", qry_tp="1")
        assert isinstance(response.body, DomesticStockInfoMarginTradingTrend)
        assert response.body.crd_trde_trend[0].cur_prc == "65100"


def test_get_daily_trading_details(client: Client):
    expected_data = {
        "daly_trde_dtl": [
            {
                "dt": "20241105",
                "close_pric": "135300",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "trde_prica": "0",
                "bf_mkrt_trde_qty": "",
                "bf_mkrt_trde_wght": "",
                "opmr_trde_qty": "",
                "opmr_trde_wght": "",
                "af_mkrt_trde_qty": "",
                "af_mkrt_trde_wght": "",
                "tot_3": "0",
                "prid_trde_qty": "0",
                "cntr_str": "",
                "for_poss": "",
                "for_wght": "",
                "for_netprps": "",
                "orgn_netprps": "",
                "ind_netprps": "",
                "frgn": "",
                "crd_remn_rt": "",
                "prm": "",
                "bf_mkrt_trde_prica": "",
                "bf_mkrt_trde_prica_wght": "",
                "opmr_trde_prica": "",
                "opmr_trde_prica_wght": "",
                "af_mkrt_trde_prica": "",
                "af_mkrt_trde_prica_wght": "",
            },
            {
                "dt": "20241101",
                "close_pric": "65100",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "trde_prica": "0",
                "bf_mkrt_trde_qty": "",
                "bf_mkrt_trde_wght": "",
                "opmr_trde_qty": "",
                "opmr_trde_wght": "",
                "af_mkrt_trde_qty": "",
                "af_mkrt_trde_wght": "",
                "tot_3": "0",
                "prid_trde_qty": "0",
                "cntr_str": "",
                "for_poss": "",
                "for_wght": "",
                "for_netprps": "",
                "orgn_netprps": "",
                "ind_netprps": "",
                "frgn": "",
                "crd_remn_rt": "",
                "prm": "",
                "bf_mkrt_trde_prica": "",
                "bf_mkrt_trde_prica_wght": "",
                "opmr_trde_prica": "",
                "opmr_trde_prica_wght": "",
                "af_mkrt_trde_prica": "",
                "af_mkrt_trde_prica_wght": "",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10015",
            },
        )
        response = client.stock_info.get_daily_trading_details(stk_cd="005930", strt_dt="20250701")

        assert isinstance(response.body, DomesticStockInfoDailyTradingDetails)
        assert response.body.daly_trde_dtl[0].close_pric == "135300"


def test_get_new_high_low_price(client: Client):
    expected_data = {
        "ntl_pric": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "334",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "3",
                "pred_trde_qty_pre_rt": "-0.00",
                "sel_bid": "0",
                "buy_bid": "0",
                "high_pric": "334",
                "low_pric": "320",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-6230",
                "pred_pre_sig": "5",
                "pred_pre": "-60",
                "flu_rt": "-0.95",
                "trde_qty": "77",
                "pred_trde_qty_pre_rt": "-6.16",
                "sel_bid": "+6300",
                "buy_bid": "-6270",
                "high_pric": "6340",
                "low_pric": "6150",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10016",
            },
        )

        response = client.stock_info.get_new_high_low_price(
            mrkt_tp="001",  # KOSPI
            ntl_tp="1",  # 신고가
            high_low_close_tp="1",  # 고저기준
            stk_cnd="0",  # 전체조회
            trde_qty_tp="00000",  # 전체조회
            crd_cnd="0",  # 전체조회
            updown_incls="0",  # 미포함
            dt="5",  # 5일
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoNewHighLowPrice)
        assert response.body.ntl_pric[0].high_pric == "334"
        assert response.body.ntl_pric[0].low_pric == "320"


def test_get_upper_lower_limit_price(client: Client):
    expected_data = {
        "updown_pric": [
            {
                "stk_cd": "005930",
                "stk_infr": "",
                "stk_nm": "삼성전자",
                "cur_prc": "+235500",
                "pred_pre_sig": "1",
                "pred_pre": "+54200",
                "flu_rt": "+29.90",
                "trde_qty": "0",
                "pred_trde_qty": "96197",
                "sel_req": "0",
                "sel_bid": "0",
                "buy_bid": "+235500",
                "buy_req": "4",
                "cnt": "1",
            },
            {
                "stk_cd": "005930",
                "stk_infr": "",
                "stk_nm": "삼성전자",
                "cur_prc": "+13715",
                "pred_pre_sig": "1",
                "pred_pre": "+3165",
                "flu_rt": "+30.00",
                "trde_qty": "0",
                "pred_trde_qty": "929670",
                "sel_req": "0",
                "sel_bid": "0",
                "buy_bid": "+13715",
                "buy_req": "4",
                "cnt": "1",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10017",
            },
        )

        response = client.stock_info.get_upper_lower_limit_price(
            mrkt_tp="001",  # KOSPI
            updown_tp="1",  # 상한
            sort_tp="1",  # 종목코드순
            stk_cnd="0",  # 전체조회
            trde_qty_tp="00000",  # 전체조회
            crd_cnd="0",  # 전체조회
            trde_gold_tp="0",  # 전체조회
            stex_tp="1",  # KRX
        )
        assert isinstance(response.body, DomesticStockInfoUpperLowerLimitPrice)
        assert response.body.updown_pric[0].stk_cd == "005930"
        assert response.body.updown_pric[0].cur_prc == "+235500"


def test_get_high_low_price_approach(client: Client):
    expected_data = {
        "high_low_pric_alacc": [
            {
                "stk_cd": "004930",
                "stk_nm": "삼성전자",
                "cur_prc": "334",
                "pred_pre_sig": "0",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "3",
                "sel_bid": "0",
                "buy_bid": "0",
                "tdy_high_pric": "334",
                "tdy_low_pric": "334",
            },
            {
                "stk_cd": "004930",
                "stk_nm": "삼성전자",
                "cur_prc": "+7470",
                "pred_pre_sig": "2",
                "pred_pre": "+90",
                "flu_rt": "+1.22",
                "trde_qty": "2",
                "sel_bid": "0",
                "buy_bid": "-7320",
                "tdy_high_pric": "+7470",
                "tdy_low_pric": "+7470",
            },
            {
                "stk_cd": "004930",
                "stk_nm": "삼성전자",
                "cur_prc": "+214000",
                "pred_pre_sig": "60",
                "pred_pre": "+20900",
                "flu_rt": "+10.82",
                "trde_qty": "45",
                "sel_bid": "0",
                "buy_bid": "+214000",
                "tdy_high_pric": "+214000",
                "tdy_low_pric": "193100",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10018",
            },
        )

        response = client.stock_info.get_high_low_price_approach(
            high_low_tp="1",  # 고가
            alacc_rt="05",  # 0.5%
            mrkt_tp="001",  # KOSPI
            trde_qty_tp="00000",  # 전체조회
            stk_cnd="0",  # 전체조회
            crd_cnd="0",  # 전체조회
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoHighLowPriceApproach)
        assert response.body.high_low_pric_alacc[0].stk_cd == "004930"
        assert response.body.high_low_pric_alacc[0].buy_bid == "0"


def test_get_price_volatility(client: Client):
    expected_data = {
        "pric_jmpflu": [
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "2",
                "pred_pre": "+300",
                "flu_rt": "+0.57",
                "base_pric": "51600",
                "cur_prc": "+52700",
                "base_pre": "1100",
                "trde_qty": "2400",
                "jmp_rt": "+2.13",
            },
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "5",
                "pred_pre": "-24200",
                "flu_rt": "-26.68",
                "base_pric": "66000",
                "cur_prc": "-66500",
                "base_pre": "500",
                "trde_qty": "577",
                "jmp_rt": "+0.76",
            },
            {
                "stk_cd": "005930",
                "stk_cls": "",
                "stk_nm": "삼성전자",
                "pred_pre_sig": "2",
                "pred_pre": "+10",
                "flu_rt": "+0.06",
                "base_pric": "16370",
                "cur_prc": "+16380",
                "base_pre": "10",
                "trde_qty": "102",
                "jmp_rt": "+0.06",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10019",
            },
        )

        response = client.stock_info.get_price_volatility(
            mrkt_tp="000",
            flu_tp="1",  # 상위
            tm_tp="1",
            tm="60",
            trde_qty_tp="00000",  # 전체조회
            stk_cnd="0",  # 전체조회
            crd_cnd="0",  # 전체조회
            pric_cnd="0",  # 전체조회
            updown_incls="1",  # 포함
            stex_tp="1",  # KRX
        )
        assert isinstance(response.body, DomesticStockInfoPriceVolatility)
        assert response.body.pric_jmpflu[0].stk_cd == "005930"
        assert response.body.pric_jmpflu[0].cur_prc == "+52700"


def test_get_trading_volume_renewal(client: Client):
    expected_data = {
        "trde_qty_updt": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "prev_trde_qty": "243520",
                "now_trde_qty": "435771",
                "sel_bid": "0",
                "buy_bid": "+74800",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-42900",
                "pred_pre_sig": "5",
                "pred_pre": "-150",
                "flu_rt": "-0.35",
                "prev_trde_qty": "25377975",
                "now_trde_qty": "31399114",
                "sel_bid": "-42900",
                "buy_bid": "+45250",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10024",
            },
        )

        response = client.stock_info.get_trading_volume_renewal(
            mrkt_tp="001",  # KOSPI
            cycle_tp="5",  # 5일
            trde_qty_tp="5",  # 5천주이상
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoTradingVolumeRenewal)
        assert response.body.trde_qty_updt[0].stk_cd == "005930"


def test_get_supply_demand_concentration(client: Client):
    expected_data = {
        "prps_cnctr": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "30000",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "pric_strt": "31350",
                "pric_end": "31799",
                "prps_qty": "4",
                "prps_rt": "+50.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "30000",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "pric_strt": "32700",
                "pric_end": "33149",
                "prps_qty": "4",
                "prps_rt": "+50.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10025",
            },
        )

        response = client.stock_info.get_supply_demand_concentration(
            mrkt_tp="001",  # KOSPI
            prps_cnctr_rt="50",  # 매물집중비율 50%
            cur_prc_entry="0",  # 현재가 매물대 진입 포함안함
            prpscnt="10",  # 매물대수 10개
            cycle_tp="100",  # 100일
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoSupplyDemandConcentration)
        assert response.body.prps_cnctr[0].stk_cd == "005930"


def test_get_high_per(client: Client):
    expected_data = {
        "high_low_per": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.44",
                "cur_prc": "4930",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.54",
                "cur_prc": "5980",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "per": "0.71",
                "cur_prc": "3445",
                "pred_pre_sig": "3",
                "pred_pre": "0",
                "flu_rt": "0.00",
                "now_trde_qty": "0",
                "sel_bid": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10026",
            },
        )

        response = client.stock_info.get_high_per(
            pertp="4",  # 고PER
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoHighPer)
        assert response.body.high_low_per[0].stk_cd == "005930"
        assert response.body.high_low_per[0].stk_nm == "삼성전자"


def test_get_change_rate_from_open(client: Client):
    expected_data = {
        "open_pric_pre_flu_rt": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "open_pric": "+65000",
                "high_pric": "+74800",
                "low_pric": "-57000",
                "open_pric_pre": "+15.08",
                "now_trde_qty": "448203",
                "cntr_str": "346.54",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-200000",
                "pred_pre_sig": "5",
                "pred_pre": "-15000",
                "flu_rt": "-6.98",
                "open_pric": "-180000",
                "high_pric": "215000",
                "low_pric": "-180000",
                "open_pric_pre": "+11.11",
                "now_trde_qty": "619",
                "cntr_str": "385.07",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10028",
            },
        )

        response = client.stock_info.get_change_rate_from_open(
            sort_tp="1",  # 시가
            trde_qty_cnd="0000",  # 전체조회
            mrkt_tp="001",  # KOSPI
            updown_incls="0",  # 불 포함
            stk_cnd="0",  # 전체조회
            crd_cnd="0",  # 전체조회
            trde_prica_cnd="0",  # 전체조회
            flu_cnd="1",  # 상위
            stex_tp="1",  # KRX
        )
        assert isinstance(response.body, DomesticStockInfoChangeRateFromOpen)
        assert response.body.open_pric_pre_flu_rt[0].stk_cd == "005930"
        assert response.body.open_pric_pre_flu_rt[0].cur_prc == "+74800"


def test_get_trading_member_supply_demand_analysis(client: Client):
    expected_data = {
        "trde_ori_prps_anly": [
            {
                "dt": "20241105",
                "close_pric": "135300",
                "pre_sig": "2",
                "pred_pre": "+1700",
                "sel_qty": "43",
                "buy_qty": "1090",
                "netprps_qty": "1047",
                "trde_qty_sum": "1133",
                "trde_wght": "+1317.44",
            },
            {
                "dt": "20241107",
                "close_pric": "133600",
                "pre_sig": "3",
                "pred_pre": "0",
                "sel_qty": "0",
                "buy_qty": "0",
                "netprps_qty": "0",
                "trde_qty_sum": "0",
                "trde_wght": "0.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10043",
            },
        )

        response = client.stock_info.get_trading_member_supply_demand_analysis(
            stk_cd="005930",  # 종목코드
            strt_dt="20250701",  # 시작일자
            end_dt="20250731",  # 종료일자
            qry_dt_tp="0",  # 기간으로 조회
            pot_tp="0",  # 당일
            dt="10",  # 10일
            sort_base="1",  # 종가순
            mmcm_cd="001",  # 회원사코드 (예시)
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoTradingMemberSupplyDemandAnalysis)
        assert response.body.trde_ori_prps_anly[0].dt == "20241105"
        assert response.body.trde_ori_prps_anly[0].close_pric == "135300"


def test_get_trading_member_instant_volume(client: Client):
    expected_data = {
        "trde_ori_mont_trde_qty": [
            {
                "tm": "161437",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "trde_ori_nm": "다이와",
                "tp": "-매도",
                "mont_trde_qty": "-399928",
                "acc_netprps": "-1073004",
                "cur_prc": "+57700",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "+0.70",
            },
            {
                "tm": "161423",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "trde_ori_nm": "다이와",
                "tp": "-매도",
                "mont_trde_qty": "-100000",
                "acc_netprps": "-673076",
                "cur_prc": "+57700",
                "pred_pre_sig": "2",
                "pred_pre": "400",
                "flu_rt": "+0.70",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10052",
            },
        )

        response = client.stock_info.get_trading_member_instant_volume(
            mmcm_cd="001",  # 회원사코드 (예시)
            stk_cd="005930",  # 종목코드
            mrkt_tp="0",  # 전체
            qty_tp="0",  # 전체
            pric_tp="0",  # 전체
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoTradingMemberInstantVolume)
        assert response.body.trde_ori_mont_trde_qty[0].tm == "161437"
        assert response.body.trde_ori_mont_trde_qty[0].stk_cd == "005930"


def test_get_volatility_control_event(client: Client):
    expected_data = {
        "motn_stk": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "acc_trde_qty": "1105968",
                "motn_pric": "67000",
                "dynm_dispty_rt": "+9.30",
                "trde_cntr_proc_time": "172311",
                "virelis_time": "172511",
                "viaplc_tp": "동적",
                "dynm_stdpc": "61300",
                "static_stdpc": "0",
                "static_dispty_rt": "0.00",
                "open_pric_pre_flu_rt": "+16.93",
                "vimotn_cnt": "23",
                "stex_tp": "NXT",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "acc_trde_qty": "1105968",
                "motn_pric": "65000",
                "dynm_dispty_rt": "-3.13",
                "trde_cntr_proc_time": "170120",
                "virelis_time": "170320",
                "viaplc_tp": "동적",
                "dynm_stdpc": "67100",
                "static_stdpc": "0",
                "static_dispty_rt": "0.00",
                "open_pric_pre_flu_rt": "+13.44",
                "vimotn_cnt": "22",
                "stex_tp": "NXT",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10054",
            },
        )

        response = client.stock_info.get_volatility_control_event(
            mrkt_tp="001",  # KOSPI
            bf_mkrt_tp="0",  # 전체
            motn_tp="0",  # 전체
            skip_stk="000000000",  # 전종목포함 조회
            trde_qty_tp="0",  # 사용안함
            min_trde_qty="",  # 공백허용
            max_trde_qty="",  # 공백허용
            trde_prica_tp="0",  # 사용안함
            min_trde_prica="",  # 공백허용
            max_trde_prica="",  # 공백허용
            motn_drc="0",  # 전체
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoVolatilityControlEvent)
        assert response.body.motn_stk[0].stk_cd == "005930"
        assert response.body.motn_stk[0].trde_cntr_proc_time == "172311"


def test_get_daily_previous_day_execution_volume(client: Client):
    expected_data = {
        "tdy_pred_cntr_qty": [
            {
                "cntr_tm": "171945",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1793",
                "acc_trde_qty": "446203",
                "acc_trde_prica": "33225",
            },
            {
                "cntr_tm": "154626",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1",
                "acc_trde_qty": "444401",
                "acc_trde_prica": "33090",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10055",
            },
        )
        response = client.stock_info.get_daily_previous_day_execution_volume(
            stk_cd="005930",  # 종목코드
            tdy_pred="1",  # 당일
        )

        assert isinstance(response.body, DomesticStockInfoDailyPreviousDayExecutionVolume)
        assert response.body.tdy_pred_cntr_qty[0].cntr_tm == "171945"
        assert response.body.tdy_pred_cntr_qty[0].cntr_pric == "+74800"


def test_get_daily_trading_items_by_investor(client: Client):
    expected_data = {
        "invsr_daly_trde_stk": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "netslmt_qty": "+4464",
                "netslmt_amt": "+25467",
                "prsm_avg_pric": "57056",
                "cur_prc": "+61300",
                "pre_sig": "2",
                "pred_pre": "+4000",
                "avg_pric_pre": "+4244",
                "pre_rt": "+7.43",
                "dt_trde_qty": "1554171",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "netslmt_qty": "+12",
                "netslmt_amt": "+106",
                "prsm_avg_pric": "86658",
                "cur_prc": "+100200",
                "pre_sig": "2",
                "pred_pre": "+5200",
                "avg_pric_pre": "+13542",
                "pre_rt": "+15.62",
                "dt_trde_qty": "12868",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10058",
            },
        )
        response = client.stock_info.get_daily_trading_items_by_investor(
            strt_dt="20250701",  # 시작일자
            end_dt="20250731",  # 종료일자
            trde_tp="2",  # 순매수
            mrkt_tp="001",  # KOSPI
            invsr_tp="8000",  # 개인
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoDailyTradingItemsByInvestor)
        assert response.body.invsr_daly_trde_stk[0].stk_cd == "005930"
        assert response.body.invsr_daly_trde_stk[0].netslmt_qty == "+4464"


def test_get_institutional_investor_by_stock(client: Client):
    expected_data = {
        "stk_invsr_orgn": [
            {
                "dt": "20241107",
                "cur_prc": "+61300",
                "pre_sig": "2",
                "pred_pre": "+4000",
                "flu_rt": "+698",
                "acc_trde_qty": "1105968",
                "acc_trde_prica": "64215",
                "ind_invsr": "1584",
                "frgnr_invsr": "-61779",
                "orgn": "60195",
                "fnnc_invt": "25514",
                "insrnc": "0",
                "invtrt": "0",
                "etc_fnnc": "34619",
                "bank": "4",
                "penfnd_etc": "-1",
                "samo_fund": "58",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "1",
            },
            {
                "dt": "20241106",
                "cur_prc": "+74800",
                "pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+2986",
                "acc_trde_qty": "448203",
                "acc_trde_prica": "33340",
                "ind_invsr": "-639",
                "frgnr_invsr": "-7",
                "orgn": "646",
                "fnnc_invt": "-47",
                "insrnc": "15",
                "invtrt": "-2",
                "etc_fnnc": "730",
                "bank": "-51",
                "penfnd_etc": "1",
                "samo_fund": "0",
                "natn": "0",
                "etc_corp": "0",
                "natfor": "0",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10059",
            },
        )

        response = client.stock_info.get_institutional_investor_by_stock(
            dt="20250701",  # 일자
            stk_cd="005930",  # 종목코드
            amt_qty_tp="1",  # 금액
            trde_tp="0",  # 순매수
            unit_tp="1000",  # 천주
        )

        assert isinstance(response.body, DomesticStockInfoInstitutionalInvestorByStock)
        assert response.body.stk_invsr_orgn[0].dt == "20241107"
        assert response.body.stk_invsr_orgn[0].cur_prc == "+61300"


def test_get_total_institutional_investor_by_stock(client: Client):
    expected_data = {
        "stk_invsr_orgn_tot": [
            {
                "ind_invsr": "--28837",
                "frgnr_invsr": "--40142",
                "orgn": "+64891",
                "fnnc_invt": "+72584",
                "insrnc": "--9071",
                "invtrt": "--7790",
                "etc_fnnc": "+35307",
                "bank": "+526",
                "penfnd_etc": "--22783",
                "samo_fund": "--3881",
                "natn": "0",
                "etc_corp": "+1974",
                "natfor": "+2114",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10061",
            },
        )
        response = client.stock_info.get_total_institutional_investor_by_stock(
            stk_cd="005930",  # 종목코드
            strt_dt="20250701",  # 시작일자
            end_dt="20250731",  # 종료일자
            amt_qty_tp="1",  # 금액
            trde_tp="0",  # 순매수
            unit_tp="1000",  # 천주
        )

        assert isinstance(response.body, DomesticStockInfoTotalInstitutionalInvestorByStock)
        assert response.body.stk_invsr_orgn_tot[0].ind_invsr == "--28837"
        assert response.body.stk_invsr_orgn_tot[0].frgnr_invsr == "--40142"


def test_get_daily_previous_day_conclusion(client: Client):
    expected_data = {
        "tdy_pred_cntr_qty": [
            {
                "cntr_tm": "171945",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1793",
                "acc_trde_qty": "446203",
                "acc_trde_prica": "33225",
            },
            {
                "cntr_tm": "154626",
                "cntr_pric": "+74800",
                "pred_pre_sig": "1",
                "pred_pre": "+17200",
                "flu_rt": "+29.86",
                "cntr_qty": "-1",
                "acc_trde_qty": "444401",
                "acc_trde_prica": "33090",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10084",
            },
        )
        response = client.stock_info.get_daily_previous_day_conclusion(
            stk_cd="005930",  # 종목코드
            tdy_pred="1",  # 당일
        )

        assert isinstance(response.body, DomesticStockInfoDailyPreviousDayConclusion)
        assert response.body.tdy_pred_cntr_qty[0].cntr_tm == "171945"
        assert response.body.tdy_pred_cntr_qty[0].pred_pre == "+17200"


def test_get_interest_stock_info(client: Client):
    expected_data = {
        "atn_stk_infr": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+156600",
                "base_pric": "121700",
                "pred_pre": "+34900",
                "pred_pre_sig": "2",
                "flu_rt": "+28.68",
                "trde_qty": "118636",
                "trde_prica": "14889",
                "cntr_qty": "-1",
                "cntr_str": "172.01",
                "pred_trde_qty_pre": "+1995.22",
                "sel_bid": "+156700",
                "buy_bid": "+156600",
                "sel_1th_bid": "+156700",
                "sel_2th_bid": "+156800",
                "sel_3th_bid": "+156900",
                "sel_4th_bid": "+158000",
                "sel_5th_bid": "+158100",
                "buy_1th_bid": "+156600",
                "buy_2th_bid": "+156500",
                "buy_3th_bid": "+156400",
                "buy_4th_bid": "+130000",
                "buy_5th_bid": "121700",
                "upl_pric": "+158200",
                "lst_pric": "-85200",
                "open_pric": "121700",
                "high_pric": "+158200",
                "low_pric": "-85200",
                "close_pric": "+156600",
                "cntr_tm": "163713",
                "exp_cntr_pric": "+156600",
                "exp_cntr_qty": "823",
                "cap": "7780",
                "fav": "100",
                "mac": "9348679",
                "stkcnt": "5969783",
                "bid_tm": "164000",
                "dt": "20241128",
                "pri_sel_req": "8003",
                "pri_buy_req": "7705",
                "pri_sel_cnt": "",
                "pri_buy_cnt": "",
                "tot_sel_req": "24028",
                "tot_buy_req": "26579",
                "tot_sel_cnt": "-11",
                "tot_buy_cnt": "",
                "prty": "0.00",
                "gear": "0.00",
                "pl_qutr": "0.00",
                "cap_support": "0.00",
                "elwexec_pric": "0",
                "cnvt_rt": "0.0000",
                "elwexpr_dt": "00000000",
                "cntr_engg": "",
                "cntr_pred_pre": "",
                "theory_pric": "",
                "innr_vltl": "",
                "delta": "",
                "gam": "",
                "theta": "",
                "vega": "",
                "law": "",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10095",
            },
        )

        response = client.stock_info.get_interest_stock_info(
            stk_cd="005930",  # 여러 종목코드 입력시 | 로 구분
        )

        assert isinstance(response.body, DomesticStockInfoInterestStockInfo)
        assert response.body.atn_stk_infr[0].stk_cd == "005930"


def test_get_stock_info_summary(client: Client):
    expected_data = {
        "return_msg": "정상적으로 처리되었습니다",
        "return_code": 0,
        "list": [
            {
                "code": "005930",
                "name": "삼성전자",
                "listCount": "0000000123759593",
                "auditInfo": "투자주의환기종목",
                "regDay": "20091204",
                "lastPrice": "00000197",
                "state": "관리종목",
                "marketCode": "10",
                "marketName": "코스닥",
                "upName": "",
                "upSizeName": "",
                "companyClassName": "",
                "orderWarning": "0",
                "nxtEnable": "Y",
            },
            {
                "code": "005930",
                "name": "삼성전자",
                "listCount": "0000000136637536",
                "auditInfo": "정상",
                "regDay": "20100423",
                "lastPrice": "00000213",
                "state": "증거금100%",
                "marketCode": "10",
                "marketName": "코스닥",
                "upName": "",
                "upSizeName": "",
                "companyClassName": "외국기업",
                "orderWarning": "0",
                "nxtEnable": "Y",
            },
        ],
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10099",
            },
        )
        response = client.stock_info.get_stock_info_summary(
            mrkt_tp="0",  # KOSPI
        )

        assert isinstance(response.body, DomesticStockInfoSummary)
        assert response.body.list[0].code == "005930"
        assert response.body.list[0].marketName == "코스닥"


def test_get_stock_info_v1(client: Client):
    expected_data = {
        "code": "005930",
        "name": "삼성전자",
        "listCount": "0000000026034239",
        "auditInfo": "정상",
        "regDay": "20090803",
        "lastPrice": "00136000",
        "state": "증거금20%|담보대출|신용가능",
        "marketCode": "0",
        "marketName": "거래소",
        "upName": "금융업",
        "upSizeName": "대형주",
        "companyClassName": "",
        "orderWarning": "0",
        "nxtEnable": "Y",
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10100",
            },
        )

        response = client.stock_info.get_stock_info_v1(
            stk_cd="005930",  # 종목코드
        )

        assert isinstance(response.body, DomesticStockInfoBasicV1)
        assert response.body.nxtEnable == "Y"
        assert response.body.code == "005930"


def test_get_industry_code(client: Client):
    expected_data = {
        "return_msg": "정상적으로 처리되었습니다",
        "list": [
            {"marketCode": "0", "code": "001", "name": "종합(KOSPI)", "group": "1"},
            {"marketCode": "0", "code": "002", "name": "대형주", "group": "2"},
            {"marketCode": "0", "code": "003", "name": "중형주", "group": "3"},
            {"marketCode": "0", "code": "004", "name": "소형주", "group": "4"},
            {"marketCode": "0", "code": "005", "name": "음식료업", "group": "5"},
        ],
        "return_code": 0,
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10101",
            },
        )

        response = client.stock_info.get_industry_code(
            mrkt_tp="0",  # KOSPI
        )

        assert isinstance(response.body, DomesticStockInfoIndustryCode)
        assert response.body.list[0].code == "001"


def test_get_member_company(client: Client):
    expected_data = {
        "return_msg": "정상적으로 처리되었습니다",
        "list": [
            {"code": "001", "name": "교  보", "gb": "0"},
            {"code": "002", "name": "신한금융투자", "gb": "0"},
            {"code": "003", "name": "한국투자증권", "gb": "0"},
            {"code": "004", "name": "대  신", "gb": "0"},
            {"code": "005", "name": "미래대우", "gb": "0"},
        ],
        "return_code": 0,
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka10102",
            },
        )

        response = client.stock_info.get_member_company()
        assert isinstance(response.body, DomesticStockInfoMemberCompany)
        assert response.body.list[0].code == "001"
        assert response.body.list[0].name == "교  보"


def test_get_top_50_program_net_buy(client: Client):
    expected_data = {
        "prm_netprps_upper_50": [
            {
                "rank": "1",
                "stk_cd": "000660",
                "stk_nm": "SK하이닉스",
                "cur_prc": "-270500",
                "flu_sig": "5",
                "pred_pre": "-8000",
                "flu_rt": "-2.87",
                "acc_trde_qty": "3654933",
                "prm_sell_amt": "242315",
                "prm_buy_amt": "387427",
                "prm_netprps_amt": "+145112",
            },
            {
                "rank": "2",
                "stk_cd": "402340",
                "stk_nm": "SK스퀘어",
                "cur_prc": "-163200",
                "flu_sig": "5",
                "pred_pre": "-8600",
                "flu_rt": "-5.01",
                "acc_trde_qty": "852852",
                "prm_sell_amt": "40843",
                "prm_buy_amt": "102350",
                "prm_netprps_amt": "+61507",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka90003",
            },
        )

        response = client.stock_info.get_top_50_program_net_buy(
            trde_upper_tp="2",  # 순매수상위
            amt_qty_tp="1",  # 금액
            mrkt_tp="P00101",  # KOSPI
            stex_tp="1",  # KRX
        )

        assert isinstance(response.body, DomesticStockInfoTop50ProgramNetBuy)
        assert response.body.prm_netprps_upper_50[0].rank == "1"
        assert response.body.prm_netprps_upper_50[0].cur_prc == "-270500"


def test_get_program_trading_status_by_stock(client: Client):
    expected_data = {
        "tot_1": "0",
        "tot_2": "2",
        "tot_3": "0",
        "tot_4": "2",
        "tot_5": "0",
        "tot_6": "",
        "stk_prm_trde_prst": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-75000",
                "flu_sig": "5",
                "pred_pre": "-2800",
                "buy_cntr_qty": "0",
                "buy_cntr_amt": "0",
                "sel_cntr_qty": "0",
                "sel_cntr_amt": "0",
                "netprps_prica": "0",
                "all_trde_rt": "+0.00",
            },
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+130000",
                "flu_sig": "2",
                "pred_pre": "+6800",
                "buy_cntr_qty": "0",
                "buy_cntr_amt": "0",
                "sel_cntr_qty": "0",
                "sel_cntr_amt": "0",
                "netprps_prica": "0",
                "all_trde_rt": "+0.00",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json=expected_data,
            status_code=200,
            headers={
                "cont-yn": "N",
                "next-key": "",
                "api-id": "ka90004",
            },
        )
        response = client.stock_info.get_program_trading_status_by_stock(
            dt="20250701",  # 일자
            mrkt_tp="P00101",  # KOSPI
            stex_tp="1",  # KRX
        )
        assert isinstance(response.body, DomesticStockInfoProgramTradingStatusByStock)
        assert response.body.stk_prm_trde_prst[0].stk_cd == "005930"
        assert response.body.stk_prm_trde_prst[0].cur_prc == "-75000"
