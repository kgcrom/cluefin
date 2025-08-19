import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._esg_types import (
    EsgSociallyResponsibleInvestmentBond,
)


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_socially_responsible_investment_bond(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISUR_NM": "GS칼텍스",
                "ISU_CD": "KR60050829A5",
                "SRI_BND_TP_NM": "녹색채권",
                "ISU_NM": "GS칼텍스139-2(녹)",
                "LIST_DD": "20191029",
                "ISU_DD": "20191029",
                "REDMPT_DD": "20291029",
                "ISU_RT": "1.99000",
                "ISU_AMT": "70000000000",
                "LIST_AMT": "70000000000",
                "BND_TP_NM": "회사채",
            },
            {
                "BAS_DD": "20250721",
                "ISUR_NM": "한국전력공사",
                "ISU_CD": "KR350103G9A2",
                "SRI_BND_TP_NM": "지속가능채권",
                "ISU_NM": "한국전력공사채권999(지)",
                "LIST_DD": "20191107",
                "ISU_DD": "20191024",
                "REDMPT_DD": "20491024",
                "ISU_RT": "1.70900",
                "ISU_AMT": "60000000000",
                "LIST_AMT": "60000000000",
                "BND_TP_NM": "특수채",
            },
            {
                "BAS_DD": "20250721",
                "ISUR_NM": "한국남부발전",
                "ISU_CD": "KR6064311899",
                "SRI_BND_TP_NM": "녹색채권",
                "ISU_NM": "한국남부발전45(녹)",
                "LIST_DD": "20180928",
                "ISU_DD": "20180928",
                "REDMPT_DD": "20480928",
                "ISU_RT": "2.43400",
                "ISU_AMT": "100000000000",
                "LIST_AMT": "100000000000",
                "BND_TP_NM": "회사채",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"https://data-dbg.krx.co.kr/svc/apis/esg/sri_bond_info.json?basDd={base_date}",
            status_code=200,
            json=expected_data,
        )

        response = client.esg.get_socially_responsible_investment_bond(base_date)

        assert isinstance(response.body, EsgSociallyResponsibleInvestmentBond)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"
        assert response.body.data[0].issuer_name == "GS칼텍스"
        assert response.body.data[0].issued_code == "KR60050829A5"
        assert response.body.data[0].bond_type == "녹색채권"
        assert response.body.data[0].issued_name == "GS칼텍스139-2(녹)"
