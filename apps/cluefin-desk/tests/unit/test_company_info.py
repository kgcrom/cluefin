import pandas as pd

from cluefin_desk.widgets.company_info import CompanyInfoWidget


def _kiwoom_row():
    return pd.Series(
        {
            "stock_code": "005930",
            "stock_name": "삼성전자",
            "market_name": "KOSPI",
            "sector_name": "전기전자",
            "market_cap": "4180000",
            "per": "12.5",
            "pbr": "1.4",
            "roe": "9.1",
            "eps": "5600",
            "bps": "50000",
        }
    )


def _kis_extras():
    return {
        "current_price": "70000",
        "price_change_rate": "0.72",
        "52_week_high": "88000",
        "52_week_low": "49000",
        "state": "정상",
        "financial_period": "202512",
        "revenue": "3000000",
        "operating_profit": "350000",
        "net_profit": "300000",
        "debt_ratio": "40.0",
        "foreign_exhaustion_rate": "52.1",
        "credit_ratio": "0.15",
    }


class TestFormatLines:
    def test_kiwoom_shape_has_no_kis_sections(self):
        text = "\n".join(CompanyInfoWidget.format_lines(_kiwoom_row()))
        assert "삼성전자" in text
        assert "PER: 12.5" in text
        assert "Price" not in text
        assert "Financials" not in text
        assert "Supply/Demand" not in text

    def test_kis_shape_adds_sections(self):
        row = pd.Series({**_kiwoom_row().to_dict(), **_kis_extras()})
        text = "\n".join(CompanyInfoWidget.format_lines(row))
        assert "현재가: 70000 (0.72%)" in text
        assert "52주: 49000 ~ 88000" in text
        assert "Financials (202512)" in text
        assert "매출액: 3000000" in text
        assert "외인소진율: 52.1%" in text

    def test_normal_state_is_hidden_but_halt_is_shown(self):
        row = pd.Series({**_kiwoom_row().to_dict(), "state": "정상"})
        assert "State" not in "\n".join(CompanyInfoWidget.format_lines(row))

        row["state"] = "거래정지"
        assert "State: 거래정지" in "\n".join(CompanyInfoWidget.format_lines(row))
