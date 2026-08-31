from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.widgets.nav_footer import NavFooter


class FinancialAnalysisScreen(Screen):
    """Screen 7: Financial Analysis via DART API."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]

    # 직전 사업연도 사업보고서 기준 (1분기 11013, 반기 11012, 3분기 11014, 사업 11011)
    DART_REPORT_CODE = "11011"

    def __init__(self, stock_code: str):
        super().__init__()
        self.stock_code = stock_code
        self._corp_code: str | None = None
        self._corp_code_resolved = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(f"{self.stock_code} — 재무 분석  [Esc·뒤로]", id="financial-title-bar")
        with TabbedContent(id="financial-tabs"):
            with TabPane("KIS 재무", id="tab-kis-financial"):
                yield Static("Loading KIS financials...", id="kis-financial-content")
            with TabPane("재무제표", id="tab-statement"):
                yield Static("Loading financial statements...", id="financial-statement-content")
            with TabPane("공시목록", id="tab-disclosure"):
                yield DataTable(id="disclosure-list-content")
            with TabPane("배당", id="tab-dividend"):
                yield Static("Loading dividend data...", id="dividend-content")
            with TabPane("주요주주", id="tab-shareholder"):
                yield Static("Loading major shareholder data...", id="major-shareholder-content")
            with TabPane("주식변동", id="tab-share-change"):
                yield Static("Loading share change data...", id="share-change-content")
            with TabPane("XBRL", id="tab-xbrl"):
                with VerticalScroll():
                    yield Static("Loading XBRL filing...", id="xbrl-content")
        yield NavFooter(id="nav-footer")

    def on_mount(self) -> None:
        self.query_one("#nav-footer", NavFooter).active_screen_key = self.app._current_screen_key
        self._setup_tables()
        self.load_all_data()

    def _setup_tables(self) -> None:
        tbl = self.query_one("#disclosure-list-content", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("접수일", 12),
            ("공시유형", 16),
            ("보고서명", 40),
        ]:
            tbl.add_column(label, key=label, width=width)

    @work(thread=True)
    def load_all_data(self) -> None:
        self._load_kis_financials()
        self._load_disclosure_list()
        self._load_dart_statements()
        self._load_dividend_info()
        self._load_major_shareholders()
        # XBRL download+parse is the slowest step — keep it last in the worker.
        self._load_xbrl()

    def _get_corp_code(self, dart_client) -> str | None:
        """Memoised corp_code lookup — corp_code() downloads the full corp index,
        so resolve it once per screen, not once per tab."""
        if not self._corp_code_resolved:
            self._corp_code = self._find_corp_code(dart_client)
            self._corp_code_resolved = True
        return self._corp_code

    @staticmethod
    def _dart_business_year() -> str:
        """직전 사업연도 — 사업보고서(11011)는 당해 연도 것이 아직 없다."""
        from datetime import datetime

        return str(datetime.now().year - 1)

    def _load_kis_financials(self) -> None:
        """KIS 재무비율·손익계산서 시계열. 진행연도 누적(YTD) 행이 연간 행과 섞여
        내려오므로 기간을 그대로 보여주고 라벨로만 구분한다."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:

            def _show_missing_kis_key():
                panel = self.query_one("#kis-financial-content", Static)
                panel.update(
                    "KIS API keys not configured.\nSet KIS_APP_KEY / KIS_SECRET_KEY in .env to use KIS financials."
                )

            self.app.call_from_thread(_show_missing_kis_key)
            return

        try:
            ratios = fetcher.get_financial_ratio_series(self.stock_code)
            statements = fetcher.get_income_statement_series(self.stock_code)

            def _update():
                lines = []
                if statements:
                    lines += [
                        "[bold]손익계산서 (KIS, 년 시리즈 — 최신 행은 진행연도 누적일 수 있음)[/bold]",
                        "",
                        f"{'결산':>8s} {'매출액':>14s} {'영업이익':>14s} {'당기순이익':>14s}",
                        "-" * 56,
                    ]
                    for item in statements[:8]:
                        lines.append(
                            f"{item.stac_yymm:>8s} {item.sale_account:>14s} {item.bsop_prti:>14s} {item.thtr_ntin:>14s}"
                        )
                if ratios:
                    lines += [
                        "",
                        "[bold]재무비율 (KIS)[/bold]",
                        "",
                        f"{'결산':>8s} {'ROE':>8s} {'부채비율':>10s} {'유보율':>12s} {'매출성장':>10s}",
                        "-" * 56,
                    ]
                    for item in ratios[:8]:
                        lines.append(
                            f"{item.stac_yymm:>8s} {item.roe_val:>8s} {item.lblt_rate:>10s} "
                            f"{item.rsrv_rate:>12s} {item.grs:>10s}"
                        )
                if not lines:
                    lines = ["No KIS financial data available (ETF/ETN and some names have none)."]

                panel = self.query_one("#kis-financial-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load KIS financials: {e}")

    def _load_disclosure_list(self) -> None:
        dart_client = self.app.dart_client
        if dart_client is None:

            def _clear_disclosure_table():
                tbl = self.query_one("#disclosure-list-content", DataTable)
                tbl.clear()

            self.app.call_from_thread(_clear_disclosure_table)

            def _show_missing_dart_key():
                panel = self.query_one("#financial-statement-content", Static)
                panel.update("DART API key not configured.\nSet DART_AUTH_KEY in .env to use financial analysis.")

            self.app.call_from_thread(_show_missing_dart_key)
            return

        try:
            # Look up corp_code from stock_code
            corp_code = self._get_corp_code(dart_client)
            if not corp_code:
                return

            response = dart_client.public_disclosure.public_disclosure_search(
                corp_code=corp_code,
                page_count=20,
            )
            items = response.result.list
            if not items:
                return

            def _update_disclosure_table():
                tbl = self.query_one("#disclosure-list-content", DataTable)
                tbl.clear()
                for item in items:
                    tbl.add_row(
                        item.rcept_dt,
                        item.corp_cls or "-",
                        item.report_nm,
                        key=item.rcept_no,
                    )

            self.app.call_from_thread(_update_disclosure_table)

            # Update title with company name
            if items:

                def _update_financial_title():
                    title = self.query_one("#financial-title-bar", Static)
                    title.update(f"[bold]{items[0].corp_name}[/bold] ({self.stock_code}) — 재무 분석  [Esc·뒤로]")

                self.app.call_from_thread(_update_financial_title)

        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load disclosures: {e}")

    def _load_dart_statements(self) -> None:
        """주요 재무계정·재무지표 (DART 정기보고서, 직전 사업연도)."""
        dart_client = self.app.dart_client
        if dart_client is None:
            return

        try:
            corp_code = self._get_corp_code(dart_client)
            if not corp_code:
                return

            from cluefin_openapi.dart._periodic_report_financial_statement import (
                PeriodicReportFinancialStatement,
            )

            statement_api = PeriodicReportFinancialStatement(dart_client)
            year = self._dart_business_year()

            accounts = (
                statement_api.get_single_company_major_accounts(
                    corp_code=corp_code,
                    bsns_year=year,
                    reprt_code=self.DART_REPORT_CODE,
                ).result.list
                or []
            )

            indicator_categories = {
                "M210000": "수익성",
                "M220000": "안정성",
                "M230000": "성장성",
                "M240000": "활동성",
            }
            indicators: list[tuple[str, str, str]] = []
            for idx_cl_code, category in indicator_categories.items():
                items = (
                    statement_api.get_single_company_major_indicators(
                        corp_code=corp_code,
                        bsns_year=year,
                        reprt_code=self.DART_REPORT_CODE,
                        idx_cl_code=idx_cl_code,
                    ).result.list
                    or []
                )
                indicators += [(category, item.idx_nm, item.idx_val or "-") for item in items[:4]]

            def _update():
                lines = [f"[bold]주요 재무계정 (DART, {year} 사업보고서)[/bold]", ""]
                if accounts:
                    seen = set()
                    lines.append(f"{'계정':<14s} {'당기':>18s} {'전기':>18s}")
                    lines.append("-" * 54)
                    for item in accounts:
                        if item.account_nm in seen:
                            continue
                        seen.add(item.account_nm)
                        lines.append(
                            f"{item.account_nm:<14s} {item.thstrm_amount or '-':>18s} {item.frmtrm_amount or '-':>18s}"
                        )
                else:
                    lines.append("재무계정 데이터 없음")

                if indicators:
                    lines += ["", "[bold]주요 재무지표 (DART)[/bold]", ""]
                    for category, name, value in indicators:
                        lines.append(f"  [{category}] {name}: {value}")

                panel = self.query_one("#financial-statement-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load DART statements: {e}")

    def _load_dividend_info(self) -> None:
        """배당 관련 사항 (DART 정기보고서, 직전 사업연도)."""
        dart_client = self.app.dart_client
        if dart_client is None:
            return

        try:
            corp_code = self._get_corp_code(dart_client)
            if not corp_code:
                return

            year = self._dart_business_year()
            items = (
                dart_client.periodic_report_key_information.get_dividend_information(
                    corp_code=corp_code,
                    bsns_year=year,
                    reprt_code=self.DART_REPORT_CODE,
                ).result.list
                or []
            )

            def _update():
                if not items:
                    lines = ["배당 데이터 없음"]
                else:
                    lines = [
                        f"[bold]배당에 관한 사항 (DART, {year} 사업보고서)[/bold]",
                        "",
                        f"{'구분':<28s} {'당기':>14s} {'전기':>14s} {'전전기':>14s}",
                        "-" * 76,
                    ]
                    for item in items[:20]:
                        label = item.se + (f" ({item.stock_knd})" if item.stock_knd else "")
                        lines.append(
                            f"{label:<28s} {item.thstrm or '-':>14s} {item.frmtrm or '-':>14s} {item.lwfr or '-':>14s}"
                        )

                panel = self.query_one("#dividend-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load dividend info: {e}")

    def _load_major_shareholders(self) -> None:
        """최대주주 현황 (DART 정기보고서).

        이전 구현은 존재하지 않는 `dart_client.share_disclosure` 를 호출해 항상
        실패했다 — 정기보고서 주요정보의 최대주주 현황으로 교체.
        """
        dart_client = self.app.dart_client
        if dart_client is None:
            return

        try:
            corp_code = self._get_corp_code(dart_client)
            if not corp_code:
                return

            year = self._dart_business_year()
            items = (
                dart_client.periodic_report_key_information.get_major_shareholder_status(
                    corp_code=corp_code,
                    bsns_year=year,
                    reprt_code=self.DART_REPORT_CODE,
                ).result.list
                or []
            )
            if not items:

                def _show_empty_major_shareholders():
                    panel = self.query_one("#major-shareholder-content", Static)
                    panel.update("No major shareholder data available")

                self.app.call_from_thread(_show_empty_major_shareholders)
                return

            def _update_major_shareholders():
                lines = [
                    f"[bold]최대주주 현황 (DART, {year} 사업보고서)[/bold]",
                    "",
                    f"{'성명':<20s} {'관계':<12s} {'기말 보유주식수':>16s} {'지분율':>8s}",
                    "-" * 62,
                ]
                for item in items[:20]:
                    lines.append(
                        f"{item.nm:<20s} {item.relate or '-':<12s} "
                        f"{item.trmend_posesn_stock_co or '-':>16s} {item.trmend_posesn_stock_qota_rt or '-':>7s}%"
                    )
                panel = self.query_one("#major-shareholder-content", Static)
                panel.update("\n".join(lines))

            self.app.call_from_thread(_update_major_shareholders)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load major shareholders: {e}")
            err_msg = str(e)

            def _update_err():
                panel = self.query_one("#major-shareholder-content", Static)
                panel.update(f"Failed to load: {err_msg}")

            self.app.call_from_thread(_update_err)

    _XBRL_STATEMENT_LABELS = {
        "BS": "재무상태표",
        "IS": "손익계산서",
        "CIS": "포괄손익계산서",
        "CF": "현금흐름표",
        "SCE": "자본변동표",
    }

    @staticmethod
    def _format_xbrl_value(value) -> str:
        if value is None:
            return "-"
        try:
            return f"{float(value):,.0f}"
        except (TypeError, ValueError):
            return str(value)

    def _load_xbrl(self) -> None:
        """XBRL 본표·주석 (cluefin-xbrl). 직전 사업연도 사업보고서를 내려받아
        연결 기준 본표 요약과 주석 목차를 보여준다 — 주석 전문은 TUI 에 맞지
        않아 목차(role·제목·항목수)만 표시한다."""
        dart_client = self.app.dart_client
        if dart_client is None:

            def _show_missing():
                self.query_one("#xbrl-content", Static).update(
                    "DART API key not configured.\nSet DART_AUTH_KEY in .env to use XBRL analysis."
                )

            self.app.call_from_thread(_show_missing)
            return

        try:
            corp_code = self._get_corp_code(dart_client)
            if not corp_code:
                return

            from cluefin_desk.data.xbrl import XbrlStatementFetcher

            fetcher = XbrlStatementFetcher(dart_client)
            year = self._dart_business_year()
            rcept_no = fetcher.find_rcept_no(corp_code, year, self.DART_REPORT_CODE)
            if rcept_no is None:

                def _show_not_found():
                    self.query_one("#xbrl-content", Static).update(f"{year} 사업보고서 XBRL 공시를 찾지 못했습니다.")

                self.app.call_from_thread(_show_not_found)
                return

            bundle = fetcher.fetch(rcept_no, self.DART_REPORT_CODE)

            def _update():
                doc = bundle.document
                statements = bundle.statements.statements or bundle.statements.separate_statements
                basis = "연결" if bundle.statements.statements else "별도"

                lines = [
                    f"[bold]XBRL — {year} 사업보고서 ({basis} 기준, rcept_no {rcept_no})[/bold]",
                    f"보고기간 종료일: {doc.reporting_period_end or '-'}  |  fact 수: {len(doc.facts):,}",
                    f"수록 본표: {', '.join(statements.keys()) or '-'}",
                ]

                for stmt_key in ("IS", "BS"):
                    stmt = statements.get(stmt_key)
                    if stmt is None:
                        continue
                    lines += ["", f"[bold cyan]{self._XBRL_STATEMENT_LABELS.get(stmt_key, stmt_key)}[/bold cyan]"]
                    for item in stmt.line_items[:25]:
                        indent = "  " * item.depth
                        label = item.label_ko or item.concept_local_name
                        if item.is_abstract:
                            lines.append(f"{indent}[bold]{label}[/bold]")
                        else:
                            lines.append(
                                f"{indent}{label:<{max(4, 40 - len(indent))}s} {self._format_xbrl_value(item.value):>18s}"
                            )

                notes = sorted(
                    (n for n in bundle.notes.notes.values() if n.is_consolidated == (basis == "연결")),
                    key=lambda n: n.role_code,
                )
                if notes:
                    lines += ["", f"[bold cyan]주석 목차 ({len(notes)}건)[/bold cyan]"]
                    for note in notes[:30]:
                        lines.append(f"  {note.role_code}  {note.title or '-'}  ({len(note.line_items)} items)")

                self.query_one("#xbrl-content", Static).update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load XBRL: {e}")
            err_msg = str(e)

            def _update_err():
                self.query_one("#xbrl-content", Static).update(f"XBRL 로딩 실패: {err_msg}")

            self.app.call_from_thread(_update_err)

    def _find_corp_code(self, dart_client) -> str | None:
        """Find DART corp_code from stock_code."""
        try:
            corp_list = dart_client.public_disclosure.corp_code()
            for item in corp_list.result.list or []:
                if item.stock_code == self.stock_code:
                    return item.corp_code
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to find corp_code for {self.stock_code}: {e}")
        return None

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_all_data()
