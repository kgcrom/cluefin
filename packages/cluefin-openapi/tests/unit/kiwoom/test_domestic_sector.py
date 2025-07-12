"""Tests for the Auth class."""

import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_sector import DomesticSector
from cluefin_openapi.kiwoom._domestic_sector_types import (
    DomesticSectorAllIndustryIndex,
    DomesticSectorDailyIndustryCurrentPrice,
    DomesticSectorIndustryCurrentPrice,
    DomesticSectorIndustryInvestorNetBuy,
    DomesticSectorIndustryPriceBySector,
    DomesticSectorIndustryProgram,
)


@pytest.fixture
def client():
    """Create a DomesticSector instance for testing."""
    return Client(
        token="test_token",
        env="dev",
    )


def test_get_industry_program_success(client):
    """Test successful industry program retrieval."""
    sector = DomesticSector(client)
    expected_data = {
        "dfrt_trst_sell_qty": "1000",
        "dfrt_trst_sell_amt": "5000000",
        "dfrt_trst_buy_qty": "1200",
        "dfrt_trst_buy_amt": "6000000",
        "dfrt_trst_netprps_qty": "-200",
        "dfrt_trst_netprps_amt": "-1000000",
        # Add other fields as necessary
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10010"},
        )

        response = sector.get_industry_program("005930", None, None)

        assert isinstance(response.body, DomesticSectorIndustryProgram)
        assert response.body.dfrt_trst_sell_qty == expected_data["dfrt_trst_sell_qty"]
        assert response.body.dfrt_trst_sell_amt == expected_data["dfrt_trst_sell_amt"]


def test_get_industry_investor_net_buy_success(client):
    """Test successful industry investor net buy retrieval."""
    sector = DomesticSector(client)
    expected_data = {
        "inds_netprps": [
            {
                "inds_cd": "001_AL",
                "inds_nm": "종합(KOSPI)",
                "cur_prc": "+265381",
                "pre_smbol": "2",
                "pred_pre": "+9030",
                "flu_rt": "352",
                "trde_qty": "1164",
                "sc_netprps": "+255",
                "insrnc_netprps": "+0",
                "invtrt_netprps": "+0",
                "bank_netprps": "+0",
                "jnsinkm_netprps": "+0",
                "endw_netprps": "+0",
                "etc_corp_netprps": "+0",
                "ind_netprps": "-0",
                "frgnr_netprps": "-622",
                "native_trmt_frgnr_netprps": "+4",
                "natn_netprps": "+0",
                "samo_fund_netprps": "+1",
                "orgn_netprps": "+601",
            },
            {
                "inds_cd": "002_AL",
                "inds_nm": "대형주",
                "cur_prc": "+265964",
                "pre_smbol": "2",
                "pred_pre": "+10690",
                "flu_rt": "419",
                "trde_qty": "1145",
                "sc_netprps": "+255",
                "insrnc_netprps": "+0",
                "invtrt_netprps": "+0",
                "bank_netprps": "+0",
                "jnsinkm_netprps": "+0",
                "endw_netprps": "+0",
                "etc_corp_netprps": "+0",
                "ind_netprps": "+16",
                "frgnr_netprps": "-622",
                "native_trmt_frgnr_netprps": "+4",
                "natn_netprps": "+0",
                "samo_fund_netprps": "+1",
                "orgn_netprps": "+602",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka10051"},
        )

        response = sector.get_industry_investor_net_buy(mrkt_tp="0", amt_qty_tp="0", base_dt="20230101", stex_tp="1")

        assert isinstance(response.body, DomesticSectorIndustryInvestorNetBuy)
        assert response.body.return_code == expected_data["return_code"]
        # The API response uses "return_msg" but the model uses "return_msg"
        # For the purpose of this test, we'll align with the model's expected field name if different,
        # or ensure the test data uses the exact key the model expects if they must match.
        # The model uses "return_msg", so the test data and assertion should align.
        assert response.body.return_msg == expected_data["return_msg"]
        assert len(response.body.inds_netprps) == 2

        # Assertions for the first item in inds_netprps
        item1 = response.body.inds_netprps[0]
        expected_item1 = expected_data["inds_netprps"][0]
        assert item1.inds_cd == expected_item1["inds_cd"]
        assert item1.inds_nm == expected_item1["inds_nm"]
        assert item1.cur_prc == expected_item1["cur_prc"]
        assert item1.orgn_netprps == expected_item1["orgn_netprps"]

        # Assertions for the second item in inds_netprps
        item2 = response.body.inds_netprps[1]
        expected_item2 = expected_data["inds_netprps"][1]
        assert item2.inds_cd == expected_item2["inds_cd"]
        assert item2.inds_nm == expected_item2["inds_nm"]
        assert item2.cur_prc == expected_item2["cur_prc"]
        assert item2.orgn_netprps == expected_item2["orgn_netprps"]


def test_get_industry_current_price_success(client):
    """Test successful industry current price retrieval."""
    sector = DomesticSector(client)
    # This expected_data should match the structure of DomesticSectorIndustryCurrentPrice
    # and its nested DomesticSectorIndustryCurrentPriceItem for the time series.
    expected_data = {
        "cur_prc": "-2394.49",
        "pred_pre_sig": "5",
        "pred_pre": "-278.47",
        "flu_rt": "-10.42",
        "trde_qty": "890",
        "trde_prica": "41867",
        "trde_frmatn_stk_num": "330",
        "trde_frmatn_rt": "+34.38",
        "open_pric": "-2669.53",
        "high_pric": "-2669.53",
        "low_pric": "-2375.21",
        "upl": "0",
        "rising": "17",
        "stdns": "183",
        "fall": "130",
        "lst": "3",
        "52wk_hgst_pric": "+3001.91",
        "52wk_hgst_pric_dt": "20241004",
        "52wk_hgst_pric_pre_rt": "-20.23",
        "52wk_lwst_pric": "-1608.07",
        "52wk_lwst_pric_dt": "20241031",
        "52wk_lwst_pric_pre_rt": "+48.90",
        "inds_cur_prc_tm": [
            {
                "tm_n": "143000",
                "cur_prc_n": "-2394.49",
                "pred_pre_sig_n": "5",
                "pred_pre_n": "-278.47",
                "flu_rt_n": "-10.42",
                "trde_qty_n": "14",
                "acc_trde_qty_n": "890",
                "stex_tp": "",
            },
            {
                "tm_n": "142950",
                "cur_prc_n": "-2394.49",
                "pred_pre_sig_n": "5",
                "pred_pre_n": "-278.47",
                "flu_rt_n": "-10.42",
                "trde_qty_n": "14",
                "acc_trde_qty_n": "876",
                "stex_tp": "",
            }
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20001"},  # Corrected API ID
        )

        # Assuming inds_cd "001" (KOSPI) is what this data represents
        response = sector.get_industry_current_price(mrkt_tp="0", inds_cd="001")

        assert isinstance(response.body, DomesticSectorIndustryCurrentPrice)
        assert response.body.return_code == expected_data["return_code"]
        assert response.body.return_msg == expected_data["return_msg"]

        # Assert top-level fields
        assert response.body.cur_prc == expected_data["cur_prc"]
        assert response.body.trde_qty == expected_data["trde_qty"]
        assert response.body.open_pric == expected_data["open_pric"]
        assert response.body.week52_hgst_pric == expected_data["52wk_hgst_pric"]

        # Assert list length and items for inds_cur_prc_tm
        assert len(response.body.inds_cur_prc_tm) == 2

        item1_response = response.body.inds_cur_prc_tm[0]
        item1_expected = expected_data["inds_cur_prc_tm"][0]
        assert item1_response.tm_n == item1_expected["tm_n"]
        assert item1_response.cur_prc_n == item1_expected["cur_prc_n"]
        assert item1_response.trde_qty_n == item1_expected["trde_qty_n"]

        item2_response = response.body.inds_cur_prc_tm[1]
        item2_expected = expected_data["inds_cur_prc_tm"][1]
        assert item2_response.tm_n == item2_expected["tm_n"]
        assert item2_response.cur_prc_n == item2_expected["cur_prc_n"]
        assert item2_response.trde_qty_n == item2_expected["trde_qty_n"]


def test_get_industry_price_by_sector_success(client):
    """Test successful industry price by sector retrieval."""
    sector = DomesticSector(client)
    expected_data = {
        "inds_stkpc": [
            {
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "75000",
                "pred_pre_sig": "2",
                "pred_pre": "1000",
                "flu_rt": "1.35",
                "now_trde_qty": "100000",
                "sel_bid": "75100",
                "buy_bid": "75000",
                "open_pric": "74500",
                "high_pric": "75500",
                "low_pric": "74300",
            },
            {
                "stk_cd": "000660",
                "stk_nm": "SK하이닉스",
                "cur_prc": "130000",
                "pred_pre_sig": "5",
                "pred_pre": "-2000",
                "flu_rt": "-1.52",
                "now_trde_qty": "50000",
                "sel_bid": "130100",
                "buy_bid": "130000",
                "open_pric": "132000",
                "high_pric": "132500",
                "low_pric": "129500",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20002"},
        )

        response = sector.get_industry_price_by_sector(mrkt_tp="0", inds_cd="001", stex_tp="1")

        assert isinstance(response.body, DomesticSectorIndustryPriceBySector)
        assert response.body.return_code == expected_data["return_code"]
        assert response.body.return_msg == expected_data["return_msg"]
        assert len(response.body.inds_stkpc) == 2

        # Assertions for the first item in inds_stkpc
        item1_response = response.body.inds_stkpc[0]
        item1_expected = expected_data["inds_stkpc"][0]
        assert item1_response.stk_cd == item1_expected["stk_cd"]
        assert item1_response.stk_nm == item1_expected["stk_nm"]
        assert item1_response.cur_prc == item1_expected["cur_prc"]
        assert item1_response.now_trde_qty == item1_expected["now_trde_qty"]

        # Assertions for the second item in inds_stkpc
        item2_response = response.body.inds_stkpc[1]
        item2_expected = expected_data["inds_stkpc"][1]
        assert item2_response.stk_cd == item2_expected["stk_cd"]
        assert item2_response.stk_nm == item2_expected["stk_nm"]
        assert item2_response.cur_prc == item2_expected["cur_prc"]
        assert item2_response.now_trde_qty == item2_expected["now_trde_qty"]


def test_get_all_industry_index_success(client):
    """Test successful all industry index retrieval."""
    sector = DomesticSector(client)
    expected_data = {
        "all_inds_index": [
            {
                "stk_cd": "001",
                "stk_nm": "종합(KOSPI)",
                "cur_prc": "-2393.33",
                "pre_sig": "5",
                "pred_pre": "-279.63",
                "flu_rt": "-10.46",
                "trde_qty": "993",
                "wght": "",
                "trde_prica": "46494",
                "upl": "0",
                "rising": "17",
                "stdns": "184",
                "fall": "129",
                "lst": "4",
                "flo_stk_num": "960",
            },
            {
                "stk_cd": "002",
                "stk_nm": "대형주",
                "cur_prc": "-2379.14",
                "pre_sig": "5",
                "pred_pre": "-326.94",
                "flu_rt": "-12.08",
                "trde_qty": "957",
                "wght": "",
                "trde_prica": "44563",
                "upl": "0",
                "rising": "6",
                "stdns": "32",
                "fall": "56",
                "lst": "2",
                "flo_stk_num": "100",
            },
            {
                "stk_cd": "003",
                "stk_nm": "중형주",
                "cur_prc": "-2691.27",
                "pre_sig": "5",
                "pred_pre": "-58.55",
                "flu_rt": "-2.13",
                "trde_qty": "26",
                "wght": "",
                "trde_prica": "1823",
                "upl": "0",
                "rising": "5",
                "stdns": "75",
                "fall": "49",
                "lst": "2",
                "flo_stk_num": "200",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20003"},
        )

        # Parameter inds_cd for get_all_industry_index can be specific like "001" or a broader category.
        # For this test, let's assume "001" is passed, but the API returns multiple indices.
        # The actual API behavior might differ based on the inds_cd sent.
        response = sector.get_all_industry_index(inds_cd="001")  # Example: KOSPI

        assert isinstance(response.body, DomesticSectorAllIndustryIndex)
        assert response.body.return_code == expected_data["return_code"]
        assert response.body.return_msg == expected_data["return_msg"]
        assert len(response.body.all_inds_index) == 3

        # Assertions for the first item
        item1_response = response.body.all_inds_index[0]
        item1_expected = expected_data["all_inds_index"][0]
        assert item1_response.stk_cd == item1_expected["stk_cd"]
        assert item1_response.stk_nm == item1_expected["stk_nm"]
        assert item1_response.cur_prc == item1_expected["cur_prc"]
        assert item1_response.trde_qty == item1_expected["trde_qty"]

        # Assertions for the second item
        item2_response = response.body.all_inds_index[1]
        item2_expected = expected_data["all_inds_index"][1]
        assert item2_response.stk_cd == item2_expected["stk_cd"]
        assert item2_response.stk_nm == item2_expected["stk_nm"]
        assert item2_response.cur_prc == item2_expected["cur_prc"]
        assert item2_response.trde_qty == item2_expected["trde_qty"]


def test_get_daily_industry_current_price_success(client):
    """Test successful daily industry current price retrieval."""
    sector = DomesticSector(client)
    expected_data = {
        "cur_prc": "-2384.71",
        "pred_pre_sig": "5",
        "pred_pre": "-288.25",
        "flu_rt": "-10.78",
        "trde_qty": "1103",
        "trde_prica": "48151",
        "trde_frmatn_stk_num": "333",
        "trde_frmatn_rt": "+34.69",
        "open_pric": "-2669.53",
        "high_pric": "-2669.53",
        "low_pric": "-2375.21",
        "upl": "0",
        "rising": "18",
        "stdns": "183",
        "fall": "132",
        "lst": "4",
        "52wk_hgst_pric": "+3001.91",
        "52wk_hgst_pric_dt": "20241004",
        "52wk_hgst_pric_pre_rt": "-20.56",
        "52wk_lwst_pric": "-1608.07",
        "52wk_lwst_pric_dt": "20241031",
        "52wk_lwst_pric_pre_rt": "+48.30",
        "inds_cur_prc_daly_rept": [
            {
                "dt_n": "20241122",
                "cur_prc_n": "-2384.71",
                "pred_pre_sig_n": "5",
                "pred_pre_n": "-288.25",
                "flu_rt_n": "-10.78",
                "acc_trde_qty_n": "1103",
            },
            {
                "dt_n": "20241121",
                "cur_prc_n": "+2672.96",
                "pred_pre_sig_n": "2",
                "pred_pre_n": "+25.56",
                "flu_rt_n": "+0.97",
                "acc_trde_qty_n": "444",
            },
            {
                "dt_n": "20241120",
                "cur_prc_n": "+2647.40",
                "pred_pre_sig_n": "2",
                "pred_pre_n": "+83.56",
                "flu_rt_n": "+3.26",
                "acc_trde_qty_n": "195",
            },
        ],
        "return_code": 0,
        "return_msg": "정상적으로 처리되었습니다.",
    }

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/api/dostk/sect",
            json=expected_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "ka20009"},
        )

        response = sector.get_daily_industry_current_price(mrkt_tp="0", inds_cd="001")  # Example: KOSPI Composite

        assert isinstance(response.body, DomesticSectorDailyIndustryCurrentPrice)
        assert response.body.return_code == expected_data["return_code"]
        assert response.body.return_msg == expected_data["return_msg"]

        # Assert top-level fields
        assert response.body.cur_prc == expected_data["cur_prc"]
        assert response.body.trde_qty == expected_data["trde_qty"]
        assert response.body.open_pric == expected_data["open_pric"]
        assert response.body.week52_hgst_pric == expected_data["52wk_hgst_pric"]  # Using model field name

        # Assert list length and items for inds_cur_prc_daly_rept
        assert len(response.body.inds_cur_prc_daly_rept) == 3

        item1_response = response.body.inds_cur_prc_daly_rept[0]
        item1_expected = expected_data["inds_cur_prc_daly_rept"][0]
        assert item1_response.dt_n == item1_expected["dt_n"]
        assert item1_response.cur_prc_n == item1_expected["cur_prc_n"]
        assert item1_response.acc_trde_qty_n == item1_expected["acc_trde_qty_n"]

        item2_response = response.body.inds_cur_prc_daly_rept[1]
        item2_expected = expected_data["inds_cur_prc_daly_rept"][1]
        assert item2_response.dt_n == item2_expected["dt_n"]
        assert item2_response.cur_prc_n == item2_expected["cur_prc_n"]
        assert item2_response.acc_trde_qty_n == item2_expected["acc_trde_qty_n"]
