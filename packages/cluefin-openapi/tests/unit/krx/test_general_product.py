import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._general_product_types import (
    GeneralProductEmissionsMarket,
    GeneralProductGoldMarket,
    GeneralProductOilMarket,
)


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_oil_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "OIL_NM": "휘발유",
                "WT_AVG_PRC": "1533.33",
                "WT_DIS_AVG_PRC": "1535.42",
                "ACC_TRDVOL": "5825886",
                "ACC_TRDVAL": "8942051790",
            },
            {
                "BAS_DD": "20250721",
                "OIL_NM": "경유",
                "WT_AVG_PRC": "1425.00",
                "WT_DIS_AVG_PRC": "1428.00",
                "ACC_TRDVOL": "10314757",
                "ACC_TRDVAL": "14723155865",
            },
            {
                "BAS_DD": "20250721",
                "OIL_NM": "등유",
                "WT_AVG_PRC": "950.00",
                "WT_DIS_AVG_PRC": "947.90",
                "ACC_TRDVOL": "1605597",
                "ACC_TRDVAL": "1522277150",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        m.get("http://data-dbg.krx.co.kr/svc/apis/gen/oil_bydd_trd.json", status_code=200, json=expected_data)

        response = client.general_product.get_oil_market("20250721")

        assert isinstance(response.body, GeneralProductOilMarket)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].oil_name == "휘발유"
        assert response.body.data[0].weighted_avg_price_competitive == "1533.33"
        assert response.body.data[0].weighted_avg_price_agreed == "1535.42"


def test_get_gold_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "04020000",
                "ISU_NM": "금 99.99_1Kg",
                "TDD_CLSPRC": "150400",
                "CMPPREVDD_PRC": "900",
                "FLUC_RT": "0.60",
                "TDD_OPNPRC": "149520",
                "TDD_HGPRC": "150560",
                "TDD_LWPRC": "149520",
                "ACC_TRDVOL": "265716",
                "ACC_TRDVAL": "39907661290",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "04020100",
                "ISU_NM": "미니금 99.99_100g",
                "TDD_CLSPRC": "150390",
                "CMPPREVDD_PRC": "840",
                "FLUC_RT": "0.56",
                "TDD_OPNPRC": "149550",
                "TDD_HGPRC": "150440",
                "TDD_LWPRC": "149530",
                "ACC_TRDVOL": "7024",
                "ACC_TRDVAL": "1054393020",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        m.get("http://data-dbg.krx.co.kr/svc/apis/gen/gold_bydd_trd.json", status_code=200, json=expected_data)

        response = client.general_product.get_gold_market("20250721")

        assert isinstance(response.body, GeneralProductGoldMarket)
        assert len(response.body.data) == 2
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].issued_code == "04020000"
        assert response.body.data[0].issued_name == "금 99.99_1Kg"
        assert response.body.data[0].close_price == "150400"
        assert response.body.data[0].prev_close_price == "900"


def test_get_emissions_market(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "05003240",
                "ISU_NM": "KAU24",
                "TDD_CLSPRC": "8800",
                "CMPPREVDD_PRC": "140",
                "FLUC_RT": "1.62",
                "TDD_OPNPRC": "8650",
                "TDD_HGPRC": "8800",
                "TDD_LWPRC": "8650",
                "ACC_TRDVOL": "189564",
                "ACC_TRDVAL": "1652791740",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "05003250",
                "ISU_NM": "KAU25",
                "TDD_CLSPRC": "8650",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "TDD_OPNPRC": "8650",
                "TDD_HGPRC": "8650",
                "TDD_LWPRC": "8650",
                "ACC_TRDVOL": "20000",
                "ACC_TRDVAL": "173000000",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "05103240",
                "ISU_NM": "KCU24",
                "TDD_CLSPRC": "9000",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "TDD_OPNPRC": "0",
                "TDD_HGPRC": "0",
                "TDD_LWPRC": "0",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        m.get("http://data-dbg.krx.co.kr/svc/apis/gen/ets_bydd_trd.json", status_code=200, json=expected_data)

        response = client.general_product.get_emissions_market("20250721")

        assert isinstance(response.body, GeneralProductEmissionsMarket)
        assert len(response.body.data) == 3
        assert response.body.data[0].issued_code == "05003240"
        assert response.body.data[0].issued_name == "KAU24"
        assert response.body.data[0].close_price == "8800"
        assert response.body.data[0].prev_close_price == "140"
        assert response.body.data[0].fluctuation_rate == "1.62"
