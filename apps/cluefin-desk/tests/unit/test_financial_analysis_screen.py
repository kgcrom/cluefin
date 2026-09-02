"""재무분석 화면을 Textual Pilot 으로 띄워 탭이 실제로 채워지는지 본다.

이 화면의 실패는 예외가 아니라 "탭이 Loading... 에서 멈춘다" 형태로 나타난다
(주식변동 탭은 로더 자체가 없어 영구히 Loading 이었고, ETF 처럼 corp_code 가
없으면 다섯 탭이 조용히 Loading 에 머물렀다). 포매터 단위 테스트로는 잡히지
않으므로 화면을 조립해 패널 텍스트를 확인한다.

앱을 직접 쓰지 않고 하네스 앱을 쓰는 이유: `CluefinDeskApp.__init__` 은
`DomesticDataFetcher` 를 만들어 실계좌 인증을 때린다.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest
from textual.app import App
from textual.widgets import DataTable, Static

import cluefin_desk
from cluefin_desk.screens.financial_analysis import FinancialAnalysisScreen

STOCK_CODE = "005930"
CORP_CODE = "00126380"

PANEL_IDS = (
    "#kis-financial-content",
    "#financial-statement-content",
    "#dividend-content",
    "#major-shareholder-content",
    "#share-change-content",
    "#xbrl-content",
)


def _response(items):
    return SimpleNamespace(result=SimpleNamespace(list=items))


class FakeFetcher:
    """KIS 재무 탭만 쓰는 최소 fetcher — 실제 fetcher 는 생성만으로 인증한다."""

    def __init__(self, has_kis: bool = True):
        self.has_kis = has_kis

    def get_financial_ratio_series(self, stock_code):
        return [SimpleNamespace(stac_yymm="202512", roe_val="9.1", lblt_rate="40.0", rsrv_rate="3000", grs="5.2")]

    def get_income_statement_series(self, stock_code):
        return [SimpleNamespace(stac_yymm="202512", sale_account="3000", bsop_prti="350", thtr_ntin="300")]


class FakeKeyInformation:
    def get_dividend_information(self, corp_code, bsns_year, reprt_code):
        return _response(
            [SimpleNamespace(se="주당 현금배당금(원)", stock_knd="보통주", thstrm="361", frmtrm="361", lwfr="361")]
        )

    def get_major_shareholder_status(self, corp_code, bsns_year, reprt_code):
        return _response(
            [
                SimpleNamespace(
                    nm="이재용",
                    relate="최대주주 본인",
                    trmend_posesn_stock_co="97,414,196",
                    trmend_posesn_stock_qota_rt="1.63",
                )
            ]
        )

    def get_total_number_of_shares(self, corp_code, bsns_year, reprt_code):
        return _response(
            [SimpleNamespace(se="보통주", istc_totqy="5,969,782,550", tesstk_co="0", distb_stock_co="5,969,782,550")]
        )

    def get_capital_change_status(self, corp_code, bsns_year, reprt_code):
        return _response(
            [
                SimpleNamespace(
                    isu_dcrs_de="2025.03.20",
                    isu_dcrs_stle="유상증자(주주배정)",
                    isu_dcrs_stock_knd="보통주",
                    isu_dcrs_qy="1,000,000",
                    isu_dcrs_mstvdv_fval_amount="100",
                    isu_dcrs_mstvdv_amount="55,000",
                )
            ]
        )


class FakePublicDisclosure:
    def __init__(self, corp_code: str | None = CORP_CODE, raises: bool = False):
        self._corp_code = corp_code
        self._raises = raises

    def corp_code(self):
        if self._raises:
            raise RuntimeError("DART 등록되지 않은 키입니다")
        if self._corp_code is None:
            return _response([])
        return _response([SimpleNamespace(stock_code=STOCK_CODE, corp_code=self._corp_code)])

    def public_disclosure_search(self, corp_code, page_count=None):
        return _response(
            [
                SimpleNamespace(
                    rcept_dt="20260311",
                    corp_cls="Y",
                    report_nm="사업보고서 (2025.12)",
                    rcept_no="20260311000123",
                    corp_name="삼성전자",
                )
            ]
        )


class FakeDartClient:
    def __init__(self, corp_code: str | None = CORP_CODE, corp_code_raises: bool = False):
        self.public_disclosure = FakePublicDisclosure(corp_code, corp_code_raises)
        self.periodic_report_key_information = FakeKeyInformation()


class FakeStatementApi:
    """`PeriodicReportFinancialStatement(dart_client)` 자리에 끼워 넣는다."""

    def __init__(self, client):
        self.client = client

    def get_single_company_major_accounts(self, corp_code, bsns_year, reprt_code):
        return _response(
            [
                SimpleNamespace(account_nm="매출액", fs_div="CFS", thstrm_amount="3,000", frmtrm_amount="2,800"),
                SimpleNamespace(account_nm="매출액", fs_div="OFS", thstrm_amount="1,000", frmtrm_amount="900"),
            ]
        )

    def get_single_company_major_indicators(self, corp_code, bsns_year, reprt_code, idx_cl_code):
        return _response([SimpleNamespace(idx_nm="영업이익률", idx_val="0.12")])


class FakeXbrlFetcher:
    """XBRL 다운로드·파싱은 네트워크와 ZIP 을 타므로 결과 모양만 흉내낸다."""

    def __init__(self, dart_client):
        self.dart_client = dart_client

    def find_rcept_no(self, corp_code, year, reprt_code):
        return "20260311000123"

    def fetch(self, rcept_no, reprt_code):
        line_item = SimpleNamespace(
            depth=0, label_ko="매출액", concept_local_name="Revenue", is_abstract=False, value=3000
        )
        statement = SimpleNamespace(line_items=[line_item])
        note = SimpleNamespace(role_code="D100", title="일반사항", line_items=[line_item], is_consolidated=True)
        return SimpleNamespace(
            document=SimpleNamespace(reporting_period_end="2025-12-31", facts=[1, 2, 3]),
            statements=SimpleNamespace(statements={"IS": statement}, separate_statements={}),
            notes=SimpleNamespace(notes={"D100": note}),
        )


class HarnessApp(App):
    """FinancialAnalysisScreen 이 app 에 기대하는 것만 갖춘 껍데기 앱."""

    # 실제 스타일시트를 물려 테스트가 tcss 회귀까지 잡게 한다.
    CSS_PATH = Path(cluefin_desk.__file__).parent / "styles" / "app.tcss"

    def __init__(self, fetcher=None, dart_client=None):
        super().__init__()
        self.fetcher = fetcher if fetcher is not None else FakeFetcher()
        self._dart_client = dart_client
        self._current_screen_key = "1"

    @property
    def dart_client(self):
        return self._dart_client

    def on_mount(self) -> None:
        self.push_screen(FinancialAnalysisScreen(STOCK_CODE))


@pytest.fixture(autouse=True)
def _patch_external(monkeypatch):
    monkeypatch.setattr(
        "cluefin_openapi.dart._periodic_report_financial_statement.PeriodicReportFinancialStatement",
        FakeStatementApi,
    )
    monkeypatch.setattr("cluefin_desk.data.xbrl.XbrlStatementFetcher", FakeXbrlFetcher)


def _panel_text(screen, selector: str) -> str:
    return str(screen.query_one(selector, Static).content)


@pytest.mark.asyncio
class TestAllTabsPopulated:
    async def test_no_tab_is_left_loading(self):
        app = HarnessApp(dart_client=FakeDartClient())
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            for selector in PANEL_IDS:
                text = _panel_text(screen, selector)
                assert "Loading" not in text, f"{selector} 가 Loading 에서 멈췄다"

    async def test_each_tab_shows_its_own_data(self):
        app = HarnessApp(dart_client=FakeDartClient())
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            assert "재무비율 (KIS)" in _panel_text(screen, "#kis-financial-content")
            # 연결(CFS) 우선 — 개별 값 1,000 이 아니라 3,000 이 보여야 한다
            statements = _panel_text(screen, "#financial-statement-content")
            assert "3,000" in statements and "1,000" not in statements
            assert "주당 현금배당금(원) (보통주)" in _panel_text(screen, "#dividend-content")
            assert "이재용" in _panel_text(screen, "#major-shareholder-content")
            share_change = _panel_text(screen, "#share-change-content")
            assert "주식의 총수 현황" in share_change and "유상증자(주주배정)" in share_change
            assert "주석 목차" in _panel_text(screen, "#xbrl-content")

    async def test_disclosure_table_and_title(self):
        app = HarnessApp(dart_client=FakeDartClient())
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            table = screen.query_one("#disclosure-list-content", DataTable)
            assert table.row_count == 1
            assert "삼성전자" in _panel_text(screen, "#financial-title-bar")
            assert _panel_text(screen, "#disclosure-status") == ""


@pytest.mark.asyncio
class TestDegradedPaths:
    async def test_no_dart_key_tells_every_dart_tab(self):
        app = HarnessApp(dart_client=None)
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            for selector in PANEL_IDS[1:]:
                assert "DART_AUTH_KEY" in _panel_text(screen, selector)
            # KIS 탭은 DART 와 무관하게 계속 채워진다
            assert "재무비율 (KIS)" in _panel_text(screen, "#kis-financial-content")

    async def test_unlisted_code_says_not_a_dart_filer(self):
        """ETF/ETN 은 corp_code 가 없다 — 예전엔 다섯 탭이 Loading 에 머물렀다."""
        app = HarnessApp(dart_client=FakeDartClient(corp_code=None))
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            for selector in PANEL_IDS[1:]:
                text = _panel_text(screen, selector)
                assert "DART 공시대상 법인이 아닙니다" in text

    async def test_corp_code_lookup_failure_is_distinguished_from_unlisted(self):
        app = HarnessApp(dart_client=FakeDartClient(corp_code_raises=True))
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            text = _panel_text(screen, "#financial-statement-content")
            assert "corp_code 조회 실패" in text
            assert "등록되지 않은 키" in text

    async def test_missing_kis_keys_only_affects_the_kis_tab(self):
        app = HarnessApp(fetcher=FakeFetcher(has_kis=False), dart_client=FakeDartClient())
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            assert "KIS_APP_KEY" in _panel_text(screen, "#kis-financial-content")
            assert "이재용" in _panel_text(screen, "#major-shareholder-content")

    async def test_one_failing_tab_does_not_block_the_others(self, monkeypatch):
        def _boom(self, corp_code, bsns_year, reprt_code):
            raise RuntimeError("요청 제한을 초과하였습니다")

        monkeypatch.setattr(FakeKeyInformation, "get_dividend_information", _boom)

        app = HarnessApp(dart_client=FakeDartClient())
        async with app.run_test() as pilot:
            await pilot.pause()
            await app.workers.wait_for_complete()
            await pilot.pause()

            screen = app.screen
            dividend = _panel_text(screen, "#dividend-content")
            assert "배당 로딩 실패" in dividend
            assert "요청 제한" in dividend
            assert "이재용" in _panel_text(screen, "#major-shareholder-content")
            assert "주석 목차" in _panel_text(screen, "#xbrl-content")
