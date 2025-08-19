import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._exchange_traded_product_types import (
    ExchangeTradedELW,
    ExchangeTradedETF,
    ExchangeTradedETN,
)


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_etf(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "483340",
                "ISU_NM": "ACE 구글밸류체인액티브",
                "TDD_CLSPRC": "11620",
                "CMPPREVDD_PRC": "25",
                "FLUC_RT": "0.22",
                "NAV": "11540.98",
                "TDD_OPNPRC": "11660",
                "TDD_HGPRC": "11660",
                "TDD_LWPRC": "11580",
                "ACC_TRDVOL": "72613",
                "ACC_TRDVAL": "843137444",
                "MKTCAP": "24402000000",
                "INVSTASST_NETASST_TOTAMT": "20773762782",
                "LIST_SHRS": "2100000",
                "IDX_IND_NM": "KEDI 글로벌 AI 클라우드 지수",
                "OBJ_STKPRC_IDX": "5235.73",
                "CMPPREVDD_IDX": "38.68",
                "FLUC_RT_IDX": "0.74",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "464240",
                "ISU_NM": "KIWOOM 26-09회사채(AA-이상)액티브",
                "TDD_CLSPRC": "52780",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "NAV": "52776.90",
                "TDD_OPNPRC": "52755",
                "TDD_HGPRC": "52780",
                "TDD_LWPRC": "52755",
                "ACC_TRDVOL": "988",
                "ACC_TRDVAL": "52128880",
                "MKTCAP": "143561600000",
                "INVSTASST_NETASST_TOTAMT": "132997799760",
                "LIST_SHRS": "2720000",
                "IDX_IND_NM": "KIS 2609 만기형 크레딧 종합채권 지수(AA-이상)(총수익지수)",
                "OBJ_STKPRC_IDX": "115.06",
                "CMPPREVDD_IDX": "0.02",
                "FLUC_RT_IDX": "0.02",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "130730",
                "ISU_NM": "KIWOOM 단기자금",
                "TDD_CLSPRC": "103305",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "NAV": "103298.26",
                "TDD_OPNPRC": "103305",
                "TDD_HGPRC": "103315",
                "TDD_LWPRC": "103300",
                "ACC_TRDVOL": "3840",
                "ACC_TRDVAL": "396702540",
                "MKTCAP": "134089890000",
                "INVSTASST_NETASST_TOTAMT": "136147100827",
                "LIST_SHRS": "1298000",
                "IDX_IND_NM": "MK 머니마켓 지수(총수익)",
                "OBJ_STKPRC_IDX": "14337.68",
                "CMPPREVDD_IDX": "0.96",
                "FLUC_RT_IDX": "0.01",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"https://data-dbg.krx.co.kr/svc/apis/etp/etf_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.exchange_traded_product.get_etf(base_date=base_date)
        assert isinstance(response.body, ExchangeTradedETF)
        assert response.body.data[0].issued_name == "ACE 구글밸류체인액티브"


def test_get_etn(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "500067",
                "ISU_NM": "신한 레버리지 10년 국채선물 ETN",
                "TDD_CLSPRC": "11310",
                "CMPPREVDD_PRC": "45",
                "FLUC_RT": "0.40",
                "PER1SECU_INDIC_VAL": "11371.18",
                "TDD_OPNPRC": "11320",
                "TDD_HGPRC": "11320",
                "TDD_LWPRC": "11310",
                "ACC_TRDVOL": "2",
                "ACC_TRDVAL": "22630",
                "MKTCAP": "7917000000",
                "INDIC_VAL_AMT": "7959826000",
                "LIST_SHRS": "700000",
                "IDX_IND_NM": "10년국채선물 레버리지지수",
                "OBJ_STKPRC_IDX": "2020.10",
                "CMPPREVDD_IDX": "9.29",
                "FLUC_RT_IDX": "0.46",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "500056",
                "ISU_NM": "신한 레버리지 Russell 2000 ETN",
                "TDD_CLSPRC": "12580",
                "CMPPREVDD_PRC": "-225",
                "FLUC_RT": "-1.76",
                "PER1SECU_INDIC_VAL": "12502.05",
                "TDD_OPNPRC": "12595",
                "TDD_HGPRC": "12595",
                "TDD_LWPRC": "12560",
                "ACC_TRDVOL": "738",
                "ACC_TRDVAL": "9287310",
                "MKTCAP": "12580000000",
                "INDIC_VAL_AMT": "12502050000",
                "LIST_SHRS": "1000000",
                "IDX_IND_NM": "Russell 2000 2X Daily Leveraged Index",
                "OBJ_STKPRC_IDX": "49754.23",
                "CMPPREVDD_IDX": "-418.08",
                "FLUC_RT_IDX": "-0.83",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "500071",
                "ISU_NM": "신한 레버리지 코스닥 150 선물 ETN",
                "TDD_CLSPRC": "31290",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "PER1SECU_INDIC_VAL": "31276.49",
                "TDD_OPNPRC": "31290",
                "TDD_HGPRC": "31290",
                "TDD_LWPRC": "31290",
                "ACC_TRDVOL": "1",
                "ACC_TRDVAL": "31290",
                "MKTCAP": "78225000000",
                "INDIC_VAL_AMT": "78191225000",
                "LIST_SHRS": "2500000",
                "IDX_IND_NM": "코스닥 150 선물 TWAP 레버리지 지수",
                "OBJ_STKPRC_IDX": "1231.42",
                "CMPPREVDD_IDX": "2.16",
                "FLUC_RT_IDX": "0.18",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"https://data-dbg.krx.co.kr/svc/apis/etp/etn_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.exchange_traded_product.get_etn(base_date=base_date)
        assert isinstance(response.body, ExchangeTradedETN)
        assert response.body.data[0].issued_name == "신한 레버리지 10년 국채선물 ETN"


def test_get_elw(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "52L223",
                "ISU_NM": "미래L223삼성전자콜",
                "TDD_CLSPRC": "95",
                "CMPPREVDD_PRC": "10",
                "TDD_OPNPRC": "95",
                "TDD_HGPRC": "95",
                "TDD_LWPRC": "95",
                "ACC_TRDVOL": "400",
                "ACC_TRDVAL": "38000",
                "MKTCAP": "3961500000",
                "LIST_SHRS": "41700000",
                "ULY_NM": "삼성전자",
                "ULY_PRC": "67,800",
                "CMPPREVDD_PRC_ULY": "700",
                "FLUC_RT_ULY": "1.04",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "52L224",
                "ISU_NM": "미래L224삼성전자콜",
                "TDD_CLSPRC": "65",
                "CMPPREVDD_PRC": "0",
                "TDD_OPNPRC": "0",
                "TDD_HGPRC": "0",
                "TDD_LWPRC": "0",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "MKTCAP": "1976000000",
                "LIST_SHRS": "30400000",
                "ULY_NM": "삼성전자",
                "ULY_PRC": "67,800",
                "CMPPREVDD_PRC_ULY": "700",
                "FLUC_RT_ULY": "1.04",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "52L225",
                "ISU_NM": "미래L225삼성전자콜",
                "TDD_CLSPRC": "110",
                "CMPPREVDD_PRC": "15",
                "TDD_OPNPRC": "100",
                "TDD_HGPRC": "110",
                "TDD_LWPRC": "100",
                "ACC_TRDVOL": "12520",
                "ACC_TRDVAL": "1367000",
                "MKTCAP": "3443000000",
                "LIST_SHRS": "31300000",
                "ULY_NM": "삼성전자",
                "ULY_PRC": "67,800",
                "CMPPREVDD_PRC_ULY": "700",
                "FLUC_RT_ULY": "1.04",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"https://data-dbg.krx.co.kr/svc/apis/etp/elw_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.exchange_traded_product.get_elw(base_date=base_date)
        assert isinstance(response.body, ExchangeTradedELW)
        assert response.body.data[0].issued_name == "미래L223삼성전자콜"
