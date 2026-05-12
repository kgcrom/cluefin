import json
from datetime import date
from decimal import Decimal

from cluefin_etf import ProviderName, get_provider
from cluefin_etf.providers._kiwoom_holdings import parse_kiwoom_holdings_html, parse_kiwoom_holdings_json
from cluefin_etf.providers._kodex_holdings import parse_kodex_holdings_html, parse_kodex_holdings_json
from cluefin_etf.providers._rise_holdings import parse_rise_holdings_html
from cluefin_etf.providers._sol_holdings import parse_sol_holdings_html, parse_sol_holdings_json_items
from cluefin_etf.providers._tiger_holdings import parse_tiger_holdings_html


def test_kodex_holdings_parsers_map_api_and_rendered_rows():
    api_holdings = parse_kodex_holdings_json(
        json.dumps(
            {
                "pdf": {
                    "gijunYMD": "20260506",
                    "list": [
                        {
                            "rank": "2",
                            "itmNo": "010120",
                            "secNm": "LS ELECTRIC",
                            "applyQ": "4,840",
                            "evalA": "1,422,960,000",
                            "ratio": "-",
                        }
                    ],
                }
            },
            ensure_ascii=False,
        )
    )
    rendered_holdings = parse_kodex_holdings_html(
        """
        <input value="2026.05.06"/>
        <table>
          <thead><tr><th>종목명</th><th>종목코드</th><th>비중(%)</th><th>수량</th><th>평가금액(원)</th></tr></thead>
          <tbody><tr><td>원화예금</td><td>KRD010010001</td><td>-</td><td>5,457,620</td><td>5,457,620</td></tr></tbody>
        </table>
        """
    )

    assert api_holdings[0].rank == 2
    assert api_holdings[0].code == "010120"
    assert api_holdings[0].quantity == Decimal("4840")
    assert api_holdings[0].weight is None
    assert api_holdings[0].as_of_date == date(2026, 5, 6)
    assert rendered_holdings[0].name == "원화예금"
    assert rendered_holdings[0].valuation_amount == Decimal("5457620")


def test_tiger_holdings_parser_maps_rows_and_display_blanks():
    holdings = parse_tiger_holdings_html(
        """
        <tr data-tot-cnt="1">
          <td>005930</td><td>삼성전자</td><td>-</td><td>1,636,567,500</td><td>31.02</td><td>3.56 상승</td>
        </tr>
        """,
        as_of_date=date(2026, 5, 4),
    )

    assert holdings[0].rank == 1
    assert holdings[0].code == "005930"
    assert holdings[0].quantity is None
    assert holdings[0].valuation_amount == Decimal("1636567500")
    assert holdings[0].raw["return"] == "3.56 상승"


def test_rise_holdings_parser_maps_server_rendered_pdf_table():
    holdings = parse_rise_holdings_html(
        """
        <tbody data-class="tab3PdfList">
          <tr><th>1</th><td>선물2026년06월물</td><td>KR4A01660005</td><td>87.55</td><td>177.9</td><td>25,361,046,250</td></tr>
        </tbody>
        """,
        as_of_date=date(2026, 5, 8),
    )

    assert holdings[0].rank == 1
    assert holdings[0].code == "KR4A01660005"
    assert holdings[0].quantity == Decimal("87.55")
    assert holdings[0].weight == Decimal("177.9")
    assert holdings[0].as_of_date == date(2026, 5, 8)


def test_ace_holdings_parser_maps_json_payload():
    provider = get_provider(ProviderName.ACE)

    holdings = provider.parse_holdings_json(
        json.dumps(
            {
                "pdfList": [
                    {
                        "rank": "1",
                        "jm_KSC_CD": "",
                        "sec_NM": "삼성전자",
                        "cu_ITEM_CNT": "6,918",
                        "val_AM": "1,608,435,000",
                        "wg": "30.67",
                        "std_DT": "20260506",
                    }
                ]
            },
            ensure_ascii=False,
        )
    )

    assert holdings[0].rank == 1
    assert holdings[0].code is None
    assert holdings[0].name == "삼성전자"
    assert holdings[0].quantity == Decimal("6918")
    assert holdings[0].as_of_date == date(2026, 5, 6)


def test_sol_holdings_parsers_map_api_and_rendered_rows():
    api_holdings = parse_sol_holdings_json_items(
        [
            {
                "SEQ_NO": 7,
                "STOCK_CODE": "042700",
                "SEC_NM": "한미반도체",
                "QTY": "981",
                "PRICE": "370,818,000",
                "WT_DISP": "23.33%",
                "WORK_DT": "20260506",
            }
        ]
    )
    rendered_holdings = parse_sol_holdings_html(
        """
        <input id="f-pdf-calendar" value="2026-05-06"/>
        <table id="pdf-table"><tbody><tr><td>1</td><td>한미반도체</td><td>981</td><td>370,818,000</td><td>23.33%</td></tr></tbody></table>
        """
    )

    assert api_holdings[0].rank == 1
    assert api_holdings[0].code == "042700"
    assert api_holdings[0].as_of_date == date(2026, 5, 6)
    assert rendered_holdings[0].name == "한미반도체"
    assert rendered_holdings[0].weight == Decimal("23.33")


def test_kiwoom_holdings_parsers_map_api_and_rendered_rows():
    api_holdings = parse_kiwoom_holdings_json(
        json.dumps(
            {
                "pdfList": [
                    {
                        "businessDate": "2026.05.06",
                        "gcode": "KR7069660009",
                        "fundcode": "005930",
                        "itemCode": "005930",
                        "itemTitle": "삼성전자",
                        "volume": "7,039",
                        "assessment": "1,636,567,500",
                        "ratio": "31.02%",
                    }
                ]
            },
            ensure_ascii=False,
        )
    )
    rendered_holdings = parse_kiwoom_holdings_html(
        """
        <table>
          <thead><tr><th>NO.</th><th>종목명</th><th>종목코드</th><th>비중</th></tr></thead>
          <tbody><tr><td>1</td><td>KIWOOM 200</td><td>KR7069660009</td><td>17.20%</td></tr></tbody>
        </table>
        """,
        as_of_date=date(2026, 5, 6),
    )

    assert api_holdings[0].code == "005930"
    assert api_holdings[0].quantity == Decimal("7039")
    assert api_holdings[0].as_of_date == date(2026, 5, 6)
    assert rendered_holdings[0].name == "KIWOOM 200"
    assert rendered_holdings[0].weight == Decimal("17.20")
