import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._index import (
    IndexBond,
    IndexDerivatives,
    IndexKosdaq,
    IndexKospi,
    IndexKrx,
)


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_krx(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KRX",
                "IDX_NM": "KRX 300",
                "CLSPRC_IDX": "1137.98",
                "CMPPREVDD_IDX": "19.34",
                "FLUC_RT": "1.73",
                "OPNPRC_IDX": "1131.89",
                "HGPRC_IDX": "1142.77",
                "LWPRC_IDX": "1124.74",
                "ACC_TRDVOL": "337526678",
                "ACC_TRDVAL": "9398617470879",
                "MKTCAP": "1184884176524815",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KRX",
                "IDX_NM": "KRX 100",
                "CLSPRC_IDX": "3995.35",
                "CMPPREVDD_IDX": "65.86",
                "FLUC_RT": "1.68",
                "OPNPRC_IDX": "3976.80",
                "HGPRC_IDX": "4013.17",
                "LWPRC_IDX": "3950.53",
                "ACC_TRDVOL": "71367374",
                "ACC_TRDVAL": "3778785066889",
                "MKTCAP": "942869008383975",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KRX",
                "IDX_NM": "KRX 300 정보기술",
                "CLSPRC_IDX": "1636.75",
                "CMPPREVDD_IDX": "39.26",
                "FLUC_RT": "2.46",
                "OPNPRC_IDX": "1625.33",
                "HGPRC_IDX": "1644.74",
                "LWPRC_IDX": "1613.14",
                "ACC_TRDVOL": "39749726",
                "ACC_TRDVAL": "1722514279106",
                "MKTCAP": "419688423399820",
            },
        ]
    }
    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/idx/krx_dd_trd.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.index.get_krx(base_date=base_date)
        assert response is not None
        assert isinstance(response.body, IndexKrx)
        assert len(response.body.data) == 3


def test_get_kospi(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSPI",
                "IDX_NM": "코스피",
                "CLSPRC_IDX": "1857.08",
                "CMPPREVDD_IDX": "31.32",
                "FLUC_RT": "1.72",
                "OPNPRC_IDX": "1846.41",
                "HGPRC_IDX": "1864.46",
                "LWPRC_IDX": "1837.17",
                "ACC_TRDVOL": "886483849",
                "ACC_TRDVAL": "9994489217634",
                "MKTCAP": "1248689568256916",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSPI",
                "IDX_NM": "코스피 200",
                "CLSPRC_IDX": "247.45",
                "CMPPREVDD_IDX": "4.05",
                "FLUC_RT": "1.66",
                "OPNPRC_IDX": "246.20",
                "HGPRC_IDX": "248.55",
                "LWPRC_IDX": "244.58",
                "ACC_TRDVOL": "193118126",
                "ACC_TRDVAL": "6324478963869",
                "MKTCAP": "1073726558045430",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSPI",
                "IDX_NM": "코스피 100",
                "CLSPRC_IDX": "1901.46",
                "CMPPREVDD_IDX": "30.20",
                "FLUC_RT": "1.61",
                "OPNPRC_IDX": "1893.22",
                "HGPRC_IDX": "1909.54",
                "LWPRC_IDX": "1880.47",
                "ACC_TRDVOL": "96496189",
                "ACC_TRDVAL": "4172518137834",
                "MKTCAP": "995035040295400",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/idx/kospi_dd_trd.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.index.get_kospi(base_date=base_date)
        assert response is not None
        assert isinstance(response.body, IndexKospi)
        assert len(response.body.data) == 3


def test_get_kosdaq(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSDAQ",
                "IDX_NM": "코스닥 (외국주포함)",
                "CLSPRC_IDX": "-",
                "CMPPREVDD_IDX": "-",
                "FLUC_RT": "-",
                "OPNPRC_IDX": "-",
                "HGPRC_IDX": "-",
                "LWPRC_IDX": "-",
                "ACC_TRDVOL": "1600520940",
                "ACC_TRDVAL": "8357337654927",
                "MKTCAP": "223912578480156",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSDAQ",
                "IDX_NM": "코스닥",
                "CLSPRC_IDX": "610.29",
                "CMPPREVDD_IDX": "13.58",
                "FLUC_RT": "2.28",
                "OPNPRC_IDX": "605.14",
                "HGPRC_IDX": "611.36",
                "LWPRC_IDX": "602.05",
                "ACC_TRDVOL": "1585402718",
                "ACC_TRDVAL": "8335407901227",
                "MKTCAP": "221665428846109",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "KOSDAQ",
                "IDX_NM": "코스닥 150",
                "CLSPRC_IDX": "952.71",
                "CMPPREVDD_IDX": "24.69",
                "FLUC_RT": "2.66",
                "OPNPRC_IDX": "942.13",
                "HGPRC_IDX": "956.14",
                "LWPRC_IDX": "935.40",
                "ACC_TRDVOL": "185817975",
                "ACC_TRDVAL": "3297642344033",
                "MKTCAP": "105899515520235",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/idx/kosdaq_dd_trd.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.index.get_kosdaq(base_date=base_date)
        assert response is not None
        assert isinstance(response.body, IndexKosdaq)
        assert len(response.body.data) == 3


def test_get_bond(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20200414",
                "BND_IDX_GRP_NM": "KRX 채권지수",
                "TOT_EARNG_IDX": "189.02",
                "TOT_EARNG_IDX_CMPPREVDD": "0.03",
                "NETPRC_IDX": "110.03",
                "NETPRC_IDX_CMPPREVDD": "0.01",
                "ZERO_REINVST_IDX": "183.02",
                "ZERO_REINVST_IDX_CMPPREVDD": "0.03",
                "CALL_REINVST_IDX": "186.33",
                "CALL_REINVST_IDX_CMPPREVDD": "0.03",
                "MKT_PRC_IDX": "111.86",
                "MKT_PRC_IDX_CMPPREVDD": "0.02",
                "AVG_DURATION": "5.670",
                "AVG_CONVEXITY_PRC": "87.205",
                "BND_IDX_AVG_YD": "1.338",
            },
            {
                "BAS_DD": "20200414",
                "BND_IDX_GRP_NM": "KTB 지수",
                "TOT_EARNG_IDX": "14602.28",
                "TOT_EARNG_IDX_CMPPREVDD": "1.25",
                "NETPRC_IDX": "10865.53",
                "NETPRC_IDX_CMPPREVDD": "0.10",
                "ZERO_REINVST_IDX": "-",
                "ZERO_REINVST_IDX_CMPPREVDD": "-",
                "CALL_REINVST_IDX": "-",
                "CALL_REINVST_IDX_CMPPREVDD": "-",
                "MKT_PRC_IDX": "10799.43",
                "MKT_PRC_IDX_CMPPREVDD": "0.92",
                "AVG_DURATION": "2.979",
                "AVG_CONVEXITY_PRC": "11.308",
                "BND_IDX_AVG_YD": "1.063",
            },
            {
                "BAS_DD": "20200414",
                "BND_IDX_GRP_NM": "국고채프라임지수",
                "TOT_EARNG_IDX": "186.26",
                "TOT_EARNG_IDX_CMPPREVDD": "0.01",
                "NETPRC_IDX": "115.51",
                "NETPRC_IDX_CMPPREVDD": "-0.00",
                "ZERO_REINVST_IDX": "-",
                "ZERO_REINVST_IDX_CMPPREVDD": "-",
                "CALL_REINVST_IDX": "-",
                "CALL_REINVST_IDX_CMPPREVDD": "-",
                "MKT_PRC_IDX": "-",
                "MKT_PRC_IDX_CMPPREVDD": "-",
                "AVG_DURATION": "4.433",
                "AVG_CONVEXITY_PRC": "29.125",
                "BND_IDX_AVG_YD": "1.187",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/idx/bon_dd_trd.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.index.get_bond(base_date=base_date)
        assert response is not None
        assert isinstance(response.body, IndexBond)
        assert len(response.body.data) == 3


def test_get_derivatives(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "선물지수",
                "IDX_NM": "코스피 200 선물지수",
                "CLSPRC_IDX": "1212.67",
                "CMPPREVDD_IDX": "23.59",
                "FLUC_RT": "1.98",
                "OPNPRC_IDX": "1202.10",
                "HGPRC_IDX": "1219.55",
                "LWPRC_IDX": "1195.96",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "옵션지수",
                "IDX_NM": "코스피 200 변동성지수",
                "CLSPRC_IDX": "36.04",
                "CMPPREVDD_IDX": "-3.65",
                "FLUC_RT": "-9.20",
                "OPNPRC_IDX": "38.29",
                "HGPRC_IDX": "38.36",
                "LWPRC_IDX": "35.96",
            },
            {
                "BAS_DD": "20200414",
                "IDX_CLSS": "전략지수",
                "IDX_NM": "코스피 200 선물 인버스지수",
                "CLSPRC_IDX": "866.00",
                "CMPPREVDD_IDX": "-17.50",
                "FLUC_RT": "-1.98",
                "OPNPRC_IDX": "873.85",
                "HGPRC_IDX": "878.42",
                "LWPRC_IDX": "860.89",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/idx/drvprod_dd_trd.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.index.get_derivatives(base_date=base_date)
        assert response is not None
        assert isinstance(response.body, IndexDerivatives)
        assert len(response.body.data) == 3
