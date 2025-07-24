import pytest
import requests_mock

from cluefin_openapi.krx._bond_types import (
    BondGeneralBondMarket,
    BondKoreaTreasuryBondMarket,
    BondSmallBondMarket,
)
from cluefin_openapi.krx._client import Client


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_korea_treasury_bond_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "MKT_NM": "국채전문유통시장",
                "ISU_CD": "KR103501GF30",
                "ISU_NM": "국고02625-2703(25-1)",
                "BND_EXP_TP_NM": "2",
                "GOVBND_ISU_TP_NM": "지표",
                "CLSPRC": "10128.5",
                "CMPPREVDD_PRC": "4.0",
                "CLSPRC_YD": "2.416",
                "OPNPRC": "10127.5",
                "OPNPRC_YD": "2.422",
                "HGPRC": "10128.5",
                "HGPRC_YD": "2.416",
                "LWPRC": "10126.0",
                "LWPRC_YD": "2.432",
                "ACC_TRDVOL": "180000000000",
                "ACC_TRDVAL": "182287150000",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "국채전문유통시장",
                "ISU_CD": "KR103501GF63",
                "ISU_NM": "국고02250-2806(25-4)",
                "BND_EXP_TP_NM": "3",
                "GOVBND_ISU_TP_NM": "지표",
                "CLSPRC": "9968.0",
                "CMPPREVDD_PRC": "5.5",
                "CLSPRC_YD": "2.457",
                "OPNPRC": "9964.5",
                "OPNPRC_YD": "2.470",
                "HGPRC": "9968.0",
                "HGPRC_YD": "2.457",
                "LWPRC": "9963.5",
                "LWPRC_YD": "2.474",
                "ACC_TRDVOL": "10459000000000",
                "ACC_TRDVAL": "10422928000000",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "국채전문유통시장",
                "ISU_CD": "KR103503GF38",
                "ISU_NM": "국고02625-3003(25-3)",
                "BND_EXP_TP_NM": "5",
                "GOVBND_ISU_TP_NM": "지표",
                "CLSPRC": "10093.5",
                "CMPPREVDD_PRC": "8.5",
                "CLSPRC_YD": "2.629",
                "OPNPRC": "10086.5",
                "OPNPRC_YD": "2.645",
                "HGPRC": "10094.0",
                "HGPRC_YD": "2.627",
                "LWPRC": "10086.5",
                "LWPRC_YD": "2.645",
                "ACC_TRDVOL": "2771000000000",
                "ACC_TRDVAL": "2795881250000",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/bon/kts_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.bond.get_korea_treasury_bond_market("20250721")
        assert isinstance(response.body, BondKoreaTreasuryBondMarket)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].market_name == "국채전문유통시장"
        assert response.body.data[0].issued_code == "KR103501GF30"


def test_get_general_bond_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "MKT_NM": "일반채권시장",
                "ISU_CD": "KR101501DAC3",
                "ISU_NM": "국민주택1종20-12",
                "CLSPRC": "10394.8",
                "CMPPREVDD_PRC": "2.0",
                "CLSPRC_YD": "2.481",
                "OPNPRC": "10394.8",
                "OPNPRC_YD": "2.481",
                "HGPRC": "10394.8",
                "HGPRC_YD": "2.481",
                "LWPRC": "10394.8",
                "LWPRC_YD": "2.481",
                "ACC_TRDVOL": "100000000",
                "ACC_TRDVAL": "103948000",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "일반채권시장",
                "ISU_CD": "KR101501DB56",
                "ISU_NM": "국민주택1종21-05",
                "CLSPRC": "10291.1",
                "CMPPREVDD_PRC": "",
                "CLSPRC_YD": "2.472",
                "OPNPRC": "10291.1",
                "OPNPRC_YD": "2.472",
                "HGPRC": "10291.1",
                "HGPRC_YD": "2.472",
                "LWPRC": "10291.1",
                "LWPRC_YD": "2.472",
                "ACC_TRDVOL": "98338000",
                "ACC_TRDVAL": "101200619",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "일반채권시장",
                "ISU_CD": "KR101501DB64",
                "ISU_NM": "국민주택1종21-06",
                "CLSPRC": "10273.3",
                "CMPPREVDD_PRC": "",
                "CLSPRC_YD": "2.444",
                "OPNPRC": "10273.3",
                "OPNPRC_YD": "2.444",
                "HGPRC": "10273.3",
                "HGPRC_YD": "2.444",
                "LWPRC": "10273.3",
                "LWPRC_YD": "2.444",
                "ACC_TRDVOL": "1004000",
                "ACC_TRDVAL": "1031439",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/bon/bnd_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.bond.get_general_bond_market("20250721")
        assert isinstance(response.body, BondGeneralBondMarket)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].market_name == "일반채권시장"
        assert response.body.data[0].issued_code == "KR101501DAC3"


def test_get_small_bond_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "MKT_NM": "소액채권시장",
                "ISU_CD": "KR101501DF60",
                "ISU_NM": "국민주택1종25-06",
                "CLSPRC": "9188.5",
                "CMPPREVDD_PRC": "10.5",
                "CLSPRC_YD": "2.755",
                "OPNPRC": "9180.0",
                "OPNPRC_YD": "2.774",
                "HGPRC": "9188.5",
                "HGPRC_YD": "2.755",
                "LWPRC": "9180.0",
                "LWPRC_YD": "2.774",
                "ACC_TRDVOL": "3312786000",
                "ACC_TRDVAL": "3042741862",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "소액채권시장",
                "ISU_CD": "KR101501DF78",
                "ISU_NM": "국민주택1종25-07",
                "CLSPRC": "9160.0",
                "CMPPREVDD_PRC": "14.0",
                "CLSPRC_YD": "2.772",
                "OPNPRC": "9160.5",
                "OPNPRC_YD": "2.771",
                "HGPRC": "9170.5",
                "HGPRC_YD": "2.748",
                "LWPRC": "9160.0",
                "LWPRC_YD": "2.772",
                "ACC_TRDVOL": "181561928000",
                "ACC_TRDVAL": "166389731889",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "소액채권시장",
                "ISU_CD": "KR2001024F69",
                "ISU_NM": "서울도시철도25-06",
                "CLSPRC": "9640.0",
                "CMPPREVDD_PRC": "25.0",
                "CLSPRC_YD": "2.972",
                "OPNPRC": "9614.0",
                "OPNPRC_YD": "3.012",
                "HGPRC": "9640.0",
                "HGPRC_YD": "2.972",
                "LWPRC": "9614.0",
                "LWPRC_YD": "3.012",
                "ACC_TRDVOL": "50010000",
                "ACC_TRDVAL": "48079640",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/bon/smb_bydd_trd.json?baseDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.bond.get_small_bond_market("20250721")
        assert isinstance(response.body, BondSmallBondMarket)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].market_name == "소액채권시장"
        assert response.body.data[0].issued_code == "KR101501DF60"
