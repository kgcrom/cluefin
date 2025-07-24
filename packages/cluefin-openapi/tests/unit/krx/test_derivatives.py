import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._derivatives_types import (
    DerivativesTradingOfFuturesExcludeStock,
    DerivativesTradingOfKosdaqFutures,
    DerivativesTradingOfKosdaqOption,
    DerivativesTradingOfKospiFutures,
    DerivativesTradingOfKospiOption,
    DerivativesTradingOfOptionExcludeStock,
)


@pytest.fixture
def client():
    return Client(
        token="test_token",
    )


def test_get_trading_of_futures_exclude_stock(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105W8000",
                "ISU_NM": "미니코스피 F 202508",
                "TDD_CLSPRC": "434.38",
                "CMPPREVDD_PRC": "3.02",
                "TDD_OPNPRC": "429.42",
                "TDD_HGPRC": "435.36",
                "TDD_LWPRC": "429.38",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.38",
                "ACC_TRDVOL": "73800",
                "ACC_TRDVAL": "1600863679000",
                "ACC_OPNINT_QTY": "35191",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105W9000",
                "ISU_NM": "미니코스피 F 202509",
                "TDD_CLSPRC": "434.62",
                "CMPPREVDD_PRC": "3.06",
                "TDD_OPNPRC": "429.70",
                "TDD_HGPRC": "435.52",
                "TDD_LWPRC": "429.68",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.65",
                "ACC_TRDVOL": "1128",
                "ACC_TRDVAL": "24486926000",
                "ACC_OPNINT_QTY": "4004",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105WA000",
                "ISU_NM": "미니코스피 F 202510",
                "TDD_CLSPRC": "434.60",
                "CMPPREVDD_PRC": "3.10",
                "TDD_OPNPRC": "430.98",
                "TDD_HGPRC": "435.00",
                "TDD_LWPRC": "430.98",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.60",
                "ACC_TRDVOL": "23",
                "ACC_TRDVAL": "499250000",
                "ACC_OPNINT_QTY": "145",
            },
        ]
    }
    with requests_mock.Mocker() as m:
        m.get("http://data-dbg.krx.co.kr/svc/apis/drv/fut_bydd_trd.json", status_code=200, json=expected_data)

        response = client.derivatives.get_trading_of_futures_exclude_stock("20250721")
        assert isinstance(response.body, DerivativesTradingOfFuturesExcludeStock)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].product_name == "미니코스피200 선물"


def teset_get_trading_of_kospi_futures(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105W8000",
                "ISU_NM": "미니코스피 F 202508",
                "TDD_CLSPRC": "434.38",
                "CMPPREVDD_PRC": "3.02",
                "TDD_OPNPRC": "429.42",
                "TDD_HGPRC": "435.36",
                "TDD_LWPRC": "429.38",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.38",
                "ACC_TRDVOL": "73800",
                "ACC_TRDVAL": "1600863679000",
                "ACC_OPNINT_QTY": "35191",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105W9000",
                "ISU_NM": "미니코스피 F 202509",
                "TDD_CLSPRC": "434.62",
                "CMPPREVDD_PRC": "3.06",
                "TDD_OPNPRC": "429.70",
                "TDD_HGPRC": "435.52",
                "TDD_LWPRC": "429.68",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.65",
                "ACC_TRDVOL": "1128",
                "ACC_TRDVAL": "24486926000",
                "ACC_OPNINT_QTY": "4004",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "미니코스피200 선물",
                "MKT_NM": "정규",
                "ISU_CD": "105WA000",
                "ISU_NM": "미니코스피 F 202510",
                "TDD_CLSPRC": "434.60",
                "CMPPREVDD_PRC": "3.10",
                "TDD_OPNPRC": "430.98",
                "TDD_HGPRC": "435.00",
                "TDD_LWPRC": "430.98",
                "SPOT_PRC": "434.56",
                "SETL_PRC": "434.60",
                "ACC_TRDVOL": "23",
                "ACC_TRDVAL": "499250000",
                "ACC_OPNINT_QTY": "145",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/drv/stk_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.derivatives.get_trading_of_kospi_futures(base_date)
        assert isinstance(response.body, DerivativesTradingOfKospiFutures)
        assert len(response.body.data) == 3
        assert response.body.data[0].bas_dd == "20250721"
        assert response.body.data[0].prod_nm == "미니코스피200 선물"
        assert response.body.data[0].isu_cd == "105W8000"


def test_get_trading_of_kosdaq_futures(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "HPSP 선물",
                "MKT_NM": "정규",
                "ISU_CD": "11BW8000",
                "ISU_NM": "HPSP       F 202508 ",
                "TDD_CLSPRC": "25700.00",
                "CMPPREVDD_PRC": "-200.00",
                "TDD_OPNPRC": "25800.00",
                "TDD_HGPRC": "25850.00",
                "TDD_LWPRC": "25550.00",
                "SPOT_PRC": "25750.00",
                "SETL_PRC": "25700.00",
                "ACC_TRDVOL": "199",
                "ACC_TRDVAL": "51147500",
                "ACC_OPNINT_QTY": "11841",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "HPSP 선물",
                "MKT_NM": "정규",
                "ISU_CD": "11BW9000",
                "ISU_NM": "HPSP       F 202509 ",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "SPOT_PRC": "25750.00",
                "SETL_PRC": "25750.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "HPSP 선물",
                "MKT_NM": "정규",
                "ISU_CD": "11BWA000",
                "ISU_NM": "HPSP       F 202510 ",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "SPOT_PRC": "25750.00",
                "SETL_PRC": "25800.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/drv/eqkfu_ksq_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.derivatives.get_trading_of_kosdaq_futures(base_date)
        assert isinstance(response.body, DerivativesTradingOfKosdaqFutures)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].product_name == "HPSP 선물"
        assert response.body.data[0].issued_code == "11BW8000"


def test_get_trading_of_option_exclude_stock(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "코스피200 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "201W8185",
                "ISU_NM": "코스피200 C 202508 185.0",
                "TDD_CLSPRC": "248.80",
                "CMPPREVDD_PRC": "1.30",
                "TDD_OPNPRC": "248.10",
                "TDD_HGPRC": "248.80",
                "TDD_LWPRC": "248.10",
                "IMP_VOLT": "64.00",
                "NXTDD_BAS_PRC": "248.80",
                "ACC_TRDVOL": "20",
                "ACC_TRDVAL": "1241875000",
                "ACC_OPNINT_QTY": "204",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "코스피200 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "201W8187",
                "ISU_NM": "코스피200 C 202508 187.5",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "63.41",
                "NXTDD_BAS_PRC": "247.30",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "코스피200 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "201W8190",
                "ISU_NM": "코스피200 C 202508 190.0",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "62.82",
                "NXTDD_BAS_PRC": "244.80",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/drv/opt_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.derivatives.get_trading_of_option_exclude_stock(base_date)
        assert isinstance(response.body, DerivativesTradingOfOptionExcludeStock)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].product_name == "코스피200 옵션"
        assert response.body.data[0].issued_code == "201W8185"


def test_get_trading_of_kospi_option(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "삼성전자 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "211W8032",
                "ISU_NM": "삼성전자   C 202508    48,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "32.40",
                "NXTDD_BAS_PRC": "19800.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "삼성전자 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "211W8037",
                "ISU_NM": "삼성전자   C 202508    49,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "32.40",
                "NXTDD_BAS_PRC": "18800.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "삼성전자 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "211W8034",
                "ISU_NM": "삼성전자   C 202508    50,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "32.40",
                "NXTDD_BAS_PRC": "17800.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/drv/eqsop_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.derivatives.get_trading_of_kospi_option(base_date)
        assert isinstance(response.body, DerivativesTradingOfKospiOption)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].product_name == "삼성전자 옵션"
        assert response.body.data[0].issued_code == "211W8032"


def test_get_trading_of_kosdaq_option(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "PROD_NM": "에코프로비엠 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "2EYW8034",
                "ISU_NM": "에코프로비 C 202508    92,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "67.80",
                "NXTDD_BAS_PRC": "22600.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "0",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "에코프로비엠 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "2EYW8032",
                "ISU_NM": "에코프로비 C 202508    96,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "67.80",
                "NXTDD_BAS_PRC": "19200.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "1",
            },
            {
                "BAS_DD": "20250721",
                "PROD_NM": "에코프로비엠 옵션",
                "RGHT_TP_NM": "CALL",
                "ISU_CD": "2EYW8033",
                "ISU_NM": "에코프로비 C 202508    98,000(  10)",
                "TDD_CLSPRC": "-",
                "CMPPREVDD_PRC": "-",
                "TDD_OPNPRC": "-",
                "TDD_HGPRC": "-",
                "TDD_LWPRC": "-",
                "IMP_VOLT": "67.80",
                "NXTDD_BAS_PRC": "17600.00",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "ACC_OPNINT_QTY": "47",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/drv/eqkop_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.derivatives.get_trading_of_kosdaq_option(base_date)
        assert isinstance(response.body, DerivativesTradingOfKosdaqOption)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].product_name == "에코프로비엠 옵션"
        assert response.body.data[0].issued_code == "2EYW8034"
