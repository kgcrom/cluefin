"""재무분석 화면의 순수 로직 — 사업연도 후퇴, 연결/개별 선택, 패널 포매팅.

화면 조립·워커 흐름은 test_financial_analysis_screen.py (Pilot 하네스) 가 본다.
"""

from datetime import datetime
from types import SimpleNamespace

from cluefin_desk.screens.financial_analysis import FinancialAnalysisScreen


def _response(items):
    """DART 응답 모양: 데이터가 없으면 status 013 + list=None 로 200 이 온다."""
    return SimpleNamespace(result=SimpleNamespace(list=items))


class TestDartYears:
    def test_newest_first_starting_from_previous_year(self):
        years = FinancialAnalysisScreen._dart_years()
        this_year = datetime.now().year
        assert years == [str(this_year - 1), str(this_year - 2)]


class TestFetchWithYearFallback:
    def test_uses_newest_year_when_it_has_data(self):
        calls = []

        def call(year):
            calls.append(year)
            return _response([SimpleNamespace(v=year)])

        items, year = FinancialAnalysisScreen._fetch_with_year_fallback(call)
        assert len(items) == 1
        assert year == calls[0] == FinancialAnalysisScreen._dart_years()[0]
        assert len(calls) == 1

    def test_falls_back_when_report_not_filed_yet(self):
        """연초에는 직전 사업연도 사업보고서가 아직 없다 — 한 해 더 물러나야 한다."""
        years = FinancialAnalysisScreen._dart_years()
        calls = []

        def call(year):
            calls.append(year)
            return _response(None if year == years[0] else [SimpleNamespace(v=year)])

        items, year = FinancialAnalysisScreen._fetch_with_year_fallback(call)
        assert year == years[1]
        assert len(items) == 1
        assert calls == years

    def test_all_years_empty_returns_empty_and_newest_year(self):
        items, year = FinancialAnalysisScreen._fetch_with_year_fallback(lambda _: _response(None))
        assert items == []
        assert year == FinancialAnalysisScreen._dart_years()[0]


def _account(name, fs_div, thstrm="100", frmtrm="90"):
    return SimpleNamespace(account_nm=name, fs_div=fs_div, thstrm_amount=thstrm, frmtrm_amount=frmtrm)


class TestSelectAccounts:
    def test_consolidated_wins_over_separate(self):
        """DART 는 같은 계정명을 연결(CFS)·개별(OFS) 로 함께 내려준다 — 섞으면
        어느 기준의 수치인지 알 수 없다."""
        selected = FinancialAnalysisScreen._select_accounts(
            [_account("자본총계", "OFS", "50"), _account("자본총계", "CFS", "100")]
        )
        assert [item.thstrm_amount for item in selected] == ["100"]

    def test_falls_back_to_separate_when_no_consolidated(self):
        selected = FinancialAnalysisScreen._select_accounts([_account("자본총계", "OFS", "50")])
        assert [item.thstrm_amount for item in selected] == ["50"]

    def test_duplicate_account_names_are_dropped(self):
        selected = FinancialAnalysisScreen._select_accounts(
            [_account("매출액", "CFS"), _account("매출액", "CFS"), _account("영업이익", "CFS")]
        )
        assert [item.account_nm for item in selected] == ["매출액", "영업이익"]

    def test_empty(self):
        assert FinancialAnalysisScreen._select_accounts(None) == []


class TestFormatStatementLines:
    def test_consolidated_basis_and_indicators(self):
        text = "\n".join(
            FinancialAnalysisScreen._format_statement_lines(
                [_account("매출액", "CFS", "1,000", "900")],
                [("수익성", "영업이익률", "0.12")],
                "2025",
            )
        )
        assert "2025 사업보고서 · 연결" in text
        assert "매출액" in text and "1,000" in text
        assert "[수익성] 영업이익률: 0.12" in text

    def test_separate_basis_label(self):
        text = "\n".join(FinancialAnalysisScreen._format_statement_lines([_account("매출액", "OFS")], [], "2025"))
        assert "· 개별" in text

    def test_no_accounts_says_so(self):
        text = "\n".join(FinancialAnalysisScreen._format_statement_lines([], [], "2025"))
        assert "재무계정 데이터 없음" in text


class TestFormatDividendLines:
    def test_empty(self):
        assert FinancialAnalysisScreen._format_dividend_lines(None, "2025") == ["배당 데이터 없음"]

    def test_stock_kind_is_appended_to_label(self):
        item = SimpleNamespace(se="주당 현금배당금(원)", stock_knd="보통주", thstrm="361", frmtrm="361", lwfr="361")
        text = "\n".join(FinancialAnalysisScreen._format_dividend_lines([item], "2025"))
        assert "주당 현금배당금(원) (보통주)" in text
        assert "361" in text

    def test_missing_values_render_as_dash(self):
        item = SimpleNamespace(se="배당성향(%)", stock_knd=None, thstrm=None, frmtrm=None, lwfr=None)
        text = "\n".join(FinancialAnalysisScreen._format_dividend_lines([item], "2025"))
        assert "배당성향(%)" in text
        assert "(None)" not in text


class TestFormatShareholderLines:
    def test_empty(self):
        assert FinancialAnalysisScreen._format_shareholder_lines([], "2025") == ["No major shareholder data available"]

    def test_rows_include_ratio_percent(self):
        item = SimpleNamespace(
            nm="이재용",
            relate="최대주주 본인",
            trmend_posesn_stock_co="97,414,196",
            trmend_posesn_stock_qota_rt="1.63",
        )
        text = "\n".join(FinancialAnalysisScreen._format_shareholder_lines([item], "2025"))
        assert "이재용" in text
        assert "1.63%" in text

    def test_missing_relation_renders_as_dash(self):
        item = SimpleNamespace(nm="홍길동", relate=None, trmend_posesn_stock_co=None, trmend_posesn_stock_qota_rt=None)
        text = "\n".join(FinancialAnalysisScreen._format_shareholder_lines([item], "2025"))
        assert "None" not in text


def _total_shares(se="보통주"):
    return SimpleNamespace(se=se, istc_totqy="5,969,782,550", tesstk_co="0", distb_stock_co="5,969,782,550")


def _capital_change():
    return SimpleNamespace(
        isu_dcrs_de="2025.03.20",
        isu_dcrs_stle="유상증자(주주배정)",
        isu_dcrs_stock_knd="보통주",
        isu_dcrs_qy="1,000,000",
        isu_dcrs_mstvdv_fval_amount="100",
        isu_dcrs_mstvdv_amount="55,000",
    )


class TestFormatShareChangeLines:
    def test_both_sections(self):
        text = "\n".join(
            FinancialAnalysisScreen._format_share_change_lines([_total_shares()], "2025", [_capital_change()], "2025")
        )
        assert "주식의 총수 현황" in text
        assert "증자(감자) 현황" in text
        assert "유상증자(주주배정)" in text

    def test_totals_only_notes_absent_capital_change(self):
        text = "\n".join(FinancialAnalysisScreen._format_share_change_lines([_total_shares()], "2025", [], "2025"))
        assert "주식의 총수 현황" in text
        assert "증자(감자) 내역 없음" in text

    def test_sections_can_carry_different_years(self):
        text = "\n".join(
            FinancialAnalysisScreen._format_share_change_lines([_total_shares()], "2025", [_capital_change()], "2024")
        )
        assert "주식의 총수 현황 (DART, 2025" in text
        assert "증자(감자) 현황 (DART, 2024" in text

    def test_both_empty(self):
        assert FinancialAnalysisScreen._format_share_change_lines(None, "2025", None, "2025") == [
            "주식변동 데이터 없음"
        ]


def _kis_statement():
    return SimpleNamespace(stac_yymm="202512", sale_account="3000", bsop_prti="350", thtr_ntin="300")


def _kis_ratio():
    return SimpleNamespace(stac_yymm="202512", roe_val="9.1", lblt_rate="40.0", rsrv_rate="3000", grs="5.2")


class TestFormatKisFinancialLines:
    def test_both_series(self):
        text = "\n".join(FinancialAnalysisScreen._format_kis_financial_lines([_kis_statement()], [_kis_ratio()]))
        assert "손익계산서 (KIS" in text
        assert "재무비율 (KIS)" in text
        assert "202512" in text

    def test_ratios_only(self):
        text = "\n".join(FinancialAnalysisScreen._format_kis_financial_lines([], [_kis_ratio()]))
        assert "손익계산서" not in text
        assert "재무비율 (KIS)" in text

    def test_neither_degrades_with_a_message(self):
        text = "\n".join(FinancialAnalysisScreen._format_kis_financial_lines(None, None))
        assert "No KIS financial data available" in text


class TestFormatXbrlValue:
    def test_number_is_thousand_separated(self):
        assert FinancialAnalysisScreen._format_xbrl_value(1234567) == "1,234,567"

    def test_none(self):
        assert FinancialAnalysisScreen._format_xbrl_value(None) == "-"

    def test_non_numeric_passes_through(self):
        assert FinancialAnalysisScreen._format_xbrl_value("해당사항 없음") == "해당사항 없음"
