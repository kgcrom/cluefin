import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._stock import (
    StockKonex,
    StockKonexBaseInfo,
    StockKosdaq,
    StockKosdaqBaseInfo,
    StockKospi,
    StockKospiBaseInfo,
    StockSubscriptionWarrant,
    StockWarrant,
)


@pytest.fixture
def client():
    return Client(
        auth_key="test_auth_key",
    )


def test_get_kospi(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "338100",
                "ISU_NM": "NH프라임리츠",
                "MKT_NM": "KOSPI",
                "SECT_TP_NM": "-",
                "TDD_CLSPRC": "4715",
                "CMPPREVDD_PRC": "25",
                "FLUC_RT": "0.53",
                "TDD_OPNPRC": "4655",
                "TDD_HGPRC": "4720",
                "TDD_LWPRC": "4655",
                "ACC_TRDVOL": "21363",
                "ACC_TRDVAL": "100332885",
                "MKTCAP": "87981900000",
                "LIST_SHRS": "18660000",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "088980",
                "ISU_NM": "맥쿼리인프라",
                "MKT_NM": "KOSPI",
                "SECT_TP_NM": "-",
                "TDD_CLSPRC": "11200",
                "CMPPREVDD_PRC": "50",
                "FLUC_RT": "0.45",
                "TDD_OPNPRC": "11150",
                "TDD_HGPRC": "11200",
                "TDD_LWPRC": "11100",
                "ACC_TRDVOL": "610438",
                "ACC_TRDVAL": "6816285500",
                "MKTCAP": "3909296563200",
                "LIST_SHRS": "349044336",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "094800",
                "ISU_NM": "맵스리얼티1",
                "MKT_NM": "KOSPI",
                "SECT_TP_NM": "-",
                "TDD_CLSPRC": "4100",
                "CMPPREVDD_PRC": "5",
                "FLUC_RT": "0.12",
                "TDD_OPNPRC": "4135",
                "TDD_HGPRC": "4135",
                "TDD_LWPRC": "4065",
                "ACC_TRDVOL": "41770",
                "ACC_TRDVAL": "170832320",
                "MKTCAP": "380620757100",
                "LIST_SHRS": "92834331",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_kospi("20250721")
        assert isinstance(response.body, StockKospi)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"


def test_get_kosdaq(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "950170",
                "ISU_NM": "JTC",
                "MKT_NM": "KOSDAQ",
                "SECT_TP_NM": "외국기업(소속부없음)",
                "TDD_CLSPRC": "5100",
                "CMPPREVDD_PRC": "125",
                "FLUC_RT": "2.51",
                "TDD_OPNPRC": "4940",
                "TDD_HGPRC": "5150",
                "TDD_LWPRC": "4940",
                "ACC_TRDVOL": "112202",
                "ACC_TRDVAL": "570871860",
                "MKTCAP": "178528136700",
                "LIST_SHRS": "35005517",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "950110",
                "ISU_NM": "SBI핀테크솔루션즈",
                "MKT_NM": "KOSDAQ",
                "SECT_TP_NM": "외국기업(소속부없음)",
                "TDD_CLSPRC": "7900",
                "CMPPREVDD_PRC": "350",
                "FLUC_RT": "4.64",
                "TDD_OPNPRC": "7650",
                "TDD_HGPRC": "7910",
                "TDD_LWPRC": "7550",
                "ACC_TRDVOL": "41691",
                "ACC_TRDVAL": "326525080",
                "MKTCAP": "194786666000",
                "LIST_SHRS": "24656540",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_kosdaq(base_date)
        assert isinstance(response.body, StockKosdaq)
        assert len(response.body.data) == 2
        assert response.body.data[0].base_date == "20250721"


def test_get_konex(client: Client):
    excepted_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "ISU_CD": "456700",
                "ISU_NM": "길교이앤씨",
                "MKT_NM": "KONEX",
                "SECT_TP_NM": "일반기업부",
                "TDD_CLSPRC": "6630",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "TDD_OPNPRC": "0",
                "TDD_HGPRC": "0",
                "TDD_LWPRC": "0",
                "ACC_TRDVOL": "0",
                "ACC_TRDVAL": "0",
                "MKTCAP": "5967000000",
                "LIST_SHRS": "900000",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "223220",
                "ISU_NM": "로지스몬",
                "MKT_NM": "KONEX",
                "SECT_TP_NM": "일반기업부",
                "TDD_CLSPRC": "148",
                "CMPPREVDD_PRC": "19",
                "FLUC_RT": "14.73",
                "TDD_OPNPRC": "129",
                "TDD_HGPRC": "148",
                "TDD_LWPRC": "110",
                "ACC_TRDVOL": "2122",
                "ACC_TRDVAL": "313648",
                "MKTCAP": "6815574048",
                "LIST_SHRS": "46051176",
            },
            {
                "BAS_DD": "20250721",
                "ISU_CD": "390110",
                "ISU_NM": "애니메디솔루션",
                "MKT_NM": "KONEX",
                "SECT_TP_NM": "일반기업부",
                "TDD_CLSPRC": "1343",
                "CMPPREVDD_PRC": "45",
                "FLUC_RT": "3.47",
                "TDD_OPNPRC": "1343",
                "TDD_HGPRC": "1343",
                "TDD_LWPRC": "1343",
                "ACC_TRDVOL": "1",
                "ACC_TRDVAL": "1343",
                "MKTCAP": "12204239871",
                "LIST_SHRS": "9087297",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/knx_bydd_trd.json?basDd={base_date}",
            json=excepted_data,
            status_code=200,
        )

        response = client.stock.get_konex(base_date)
        assert isinstance(response.body, StockKonex)
        assert len(response.body.data) == 3
        assert response.body.data[0].sector_type_name == "일반기업부"


def test_get_warrant(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSDAQ",
                "ISU_CD": "1099621D",
                "ISU_NM": "AP헬스케어 6WR",
                "TDD_CLSPRC": "52",
                "CMPPREVDD_PRC": "0",
                "FLUC_RT": "0.00",
                "TDD_OPNPRC": "52",
                "TDD_HGPRC": "52",
                "TDD_LWPRC": "49",
                "ACC_TRDVOL": "288585",
                "ACC_TRDVAL": "14654238",
                "MKTCAP": "885106196",
                "LIST_SHRS": "17021273",
                "EXER_PRC": "809",
                "EXST_STRT_DD": "20230825",
                "EXST_END_DD": "20260625",
                "TARSTK_ISU_SRT_CD": "109960",
                "TARSTK_ISU_NM": "AP헬스케어",
                "TARSTK_ISU_PRSNT_PRC": "352",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSDAQ",
                "ISU_CD": "2901221D",
                "ISU_NM": "DH오토리드 9WR",
                "TDD_CLSPRC": "429",
                "CMPPREVDD_PRC": "17",
                "FLUC_RT": "4.13",
                "TDD_OPNPRC": "429",
                "TDD_HGPRC": "429",
                "TDD_LWPRC": "429",
                "ACC_TRDVOL": "1",
                "ACC_TRDVAL": "429",
                "MKTCAP": "1328051868",
                "LIST_SHRS": "3095692",
                "EXER_PRC": "3491",
                "EXST_STRT_DD": "20230705",
                "EXST_END_DD": "20260506",
                "TARSTK_ISU_SRT_CD": "290120",
                "TARSTK_ISU_NM": "DH오토리드",
                "TARSTK_ISU_PRSNT_PRC": "2770",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSPI",
                "ISU_CD": "0036221D",
                "ISU_NM": "KG모빌리티 122WR",
                "TDD_CLSPRC": "840",
                "CMPPREVDD_PRC": "-18",
                "FLUC_RT": "-2.10",
                "TDD_OPNPRC": "850",
                "TDD_HGPRC": "859",
                "TDD_LWPRC": "815",
                "ACC_TRDVOL": "8977",
                "ACC_TRDVAL": "7392717",
                "MKTCAP": "15029941080",
                "LIST_SHRS": "17892787",
                "EXER_PRC": "6729",
                "EXST_STRT_DD": "20240105",
                "EXST_END_DD": "20281105",
                "TARSTK_ISU_SRT_CD": "003620",
                "TARSTK_ISU_NM": "KG모빌리티",
                "TARSTK_ISU_PRSNT_PRC": "3695",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/sw_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_warrant(base_date)
        assert isinstance(response.body, StockWarrant)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"


def test_get_warrant_subscription(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSDAQ",
                "ISU_CD": "0603701F",
                "ISU_NM": "LS마린솔루션 9R",
                "TDD_CLSPRC": "4940",
                "CMPPREVDD_PRC": "2",
                "FLUC_RT": "-1.79",
                "TDD_OPNPRC": "5030",
                "TDD_HGPRC": "5030",
                "TDD_LWPRC": "4500",
                "ACC_TRDVOL": "496129",
                "ACC_TRDVAL": "2357686890",
                "MKTCAP": "96594566640",
                "LIST_SHRS": "19553556",
                "ISU_PRC": "21900",
                "DELIST_DD": "20250725",
                "TARSTK_ISU_SRT_CD": "060370",
                "TARSTK_ISU_NM": "LS마린솔루션",
                "TARSTK_ISU_PRSNT_PRC": "28000",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSDAQ",
                "ISU_CD": "0237901F",
                "ISU_NM": "동일스틸럭스 14R",
                "TDD_CLSPRC": "48",
                "CMPPREVDD_PRC": "1",
                "FLUC_RT": "4.35",
                "TDD_OPNPRC": "46",
                "TDD_HGPRC": "80",
                "TDD_LWPRC": "42",
                "ACC_TRDVOL": "1084064",
                "ACC_TRDVAL": "55089285",
                "MKTCAP": "239891712",
                "LIST_SHRS": "4997744",
                "ISU_PRC": "623",
                "DELIST_DD": "20250725",
                "TARSTK_ISU_SRT_CD": "023790",
                "TARSTK_ISU_NM": "동일스틸럭스",
                "TARSTK_ISU_PRSNT_PRC": "773",
            },
            {
                "BAS_DD": "20250721",
                "MKT_NM": "KOSDAQ",
                "ISU_CD": "1893301F",
                "ISU_NM": "씨이랩 18R",
                "TDD_CLSPRC": "379",
                "CMPPREVDD_PRC": "1",
                "FLUC_RT": "0.00",
                "TDD_OPNPRC": "610",
                "TDD_HGPRC": "650",
                "TDD_LWPRC": "374",
                "ACC_TRDVOL": "793219",
                "ACC_TRDVAL": "381031705",
                "MKTCAP": "1245423183",
                "LIST_SHRS": "3286077",
                "ISU_PRC": "6180",
                "DELIST_DD": "20250728",
                "TARSTK_ISU_SRT_CD": "189330",
                "TARSTK_ISU_NM": "씨이랩",
                "TARSTK_ISU_PRSNT_PRC": "6880",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/sr_bydd_trd.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_subscription_warrant(base_date)
        assert isinstance(response.body, StockSubscriptionWarrant)
        assert len(response.body.data) == 3
        assert response.body.data[0].base_date == "20250721"


def test_get_kospi_base_info(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "ISU_CD": "KR7365550003",
                "ISU_SRT_CD": "365550",
                "ISU_NM": "ESR켄달스퀘어리츠보통주",
                "ISU_ABBRV": "ESR켄달스퀘어리츠",
                "ISU_ENG_NM": "ESR KENDALL SQUARE REIT",
                "LIST_DD": "20201223",
                "MKT_TP_NM": "KOSPI",
                "SECUGRP_NM": "부동산투자회사",
                "SECT_TP_NM": "-",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "1000",
                "LIST_SHRS": "213089000",
            },
            {
                "ISU_CD": "KR7432320000",
                "ISU_SRT_CD": "432320",
                "ISU_NM": "KB스타리츠보통주",
                "ISU_ABBRV": "KB스타리츠",
                "ISU_ENG_NM": "KB STAR REIT",
                "LIST_DD": "20221006",
                "MKT_TP_NM": "KOSPI",
                "SECUGRP_NM": "부동산투자회사",
                "SECT_TP_NM": "-",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "500",
                "LIST_SHRS": "101414285",
            },
            {
                "ISU_CD": "KR7088980008",
                "ISU_SRT_CD": "088980",
                "ISU_NM": "맥쿼리한국인프라투융자회사 보통주",
                "ISU_ABBRV": "맥쿼리인프라",
                "ISU_ENG_NM": "Macquarie Korea Infrastructure Fund",
                "LIST_DD": "20060315",
                "MKT_TP_NM": "KOSPI",
                "SECUGRP_NM": "사회간접자본투융자회사",
                "SECT_TP_NM": "-",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "무액면",
                "LIST_SHRS": "478921993",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_kospi_base_info(base_date)
        assert isinstance(response.body, StockKospiBaseInfo)
        assert len(response.body.data) == 3
        assert response.body.data[0].issued_name == "ESR켄달스퀘어리츠보통주"
        assert response.body.data[0].issued_abbreviation == "ESR켄달스퀘어리츠"


def test_get_kosdaq_base_info(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "ISU_CD": "KR8392070007",
                "ISU_SRT_CD": "950110",
                "ISU_NM": "SBI핀테크솔루션즈",
                "ISU_ABBRV": "SBI핀테크솔루션즈",
                "ISU_ENG_NM": "SBI FinTech Solutions Co., Ltd.",
                "LIST_DD": "20121217",
                "MKT_TP_NM": "KOSDAQ",
                "SECUGRP_NM": "주식예탁증권",
                "SECT_TP_NM": "외국기업(소속부없음)",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "무액면",
                "LIST_SHRS": "24052540",
            },
            {
                "ISU_CD": "KR8344390008",
                "ISU_SRT_CD": "950190",
                "ISU_NM": "고스트스튜디오",
                "ISU_ABBRV": "고스트스튜디오",
                "ISU_ENG_NM": "GHOST STUDIO",
                "LIST_DD": "20200818",
                "MKT_TP_NM": "KOSDAQ",
                "SECUGRP_NM": "주식예탁증권",
                "SECT_TP_NM": "외국기업(소속부없음)",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "무액면",
                "LIST_SHRS": "13017059",
            },
            {
                "ISU_CD": "KYG3931T1076",
                "ISU_SRT_CD": "900070",
                "ISU_NM": "글로벌에스엠테크리미티드",
                "ISU_ABBRV": "글로벌에스엠",
                "ISU_ENG_NM": "Global SM Tech Limited",
                "LIST_DD": "20091223",
                "MKT_TP_NM": "KOSDAQ",
                "SECUGRP_NM": "외국주권",
                "SECT_TP_NM": "외국기업(소속부없음)",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": ".5",
                "LIST_SHRS": "53743968",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/ksq_isu_base_info.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_kosdaq_base_info(base_date)
        assert isinstance(response.body, StockKosdaqBaseInfo)
        assert len(response.body.data) == 3
        assert response.body.data[0].issued_name == "SBI핀테크솔루션즈"


def test_get_konex_base_info(client: Client):
    expected_data = {
        "OutBlock_1": [
            {
                "ISU_CD": "KR7456700004",
                "ISU_SRT_CD": "456700",
                "ISU_NM": "길교이앤씨",
                "ISU_ABBRV": "길교이앤씨",
                "ISU_ENG_NM": "GILGYO E&C",
                "LIST_DD": "20230726",
                "MKT_TP_NM": "KONEX",
                "SECUGRP_NM": "주권",
                "SECT_TP_NM": "일반기업부",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "500",
                "LIST_SHRS": "900000",
            },
            {
                "ISU_CD": "KR7223220005",
                "ISU_SRT_CD": "223220",
                "ISU_NM": "로지스몬",
                "ISU_ABBRV": "로지스몬",
                "ISU_ENG_NM": "Logis Mon",
                "LIST_DD": "20150709",
                "MKT_TP_NM": "KONEX",
                "SECUGRP_NM": "주권",
                "SECT_TP_NM": "일반기업부",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "100",
                "LIST_SHRS": "46051176",
            },
            {
                "ISU_CD": "KR7390110005",
                "ISU_SRT_CD": "390110",
                "ISU_NM": "애니메디솔루션",
                "ISU_ABBRV": "애니메디솔루션",
                "ISU_ENG_NM": "Anymedi",
                "LIST_DD": "20221221",
                "MKT_TP_NM": "KONEX",
                "SECUGRP_NM": "주권",
                "SECT_TP_NM": "일반기업부",
                "KIND_STKCERT_TP_NM": "보통주",
                "PARVAL": "500",
                "LIST_SHRS": "9087297",
            },
        ]
    }

    with requests_mock.Mocker() as m:
        base_date = "20250721"
        m.get(
            f"http://data-dbg.krx.co.kr/svc/apis/sto/knx_isu_base_info.json?basDd={base_date}",
            json=expected_data,
            status_code=200,
        )

        response = client.stock.get_konex_base_info(base_date)
        assert isinstance(response.body, StockKonexBaseInfo)
        assert len(response.body.data) == 3
        assert response.body.data[0].issued_name == "길교이앤씨"
