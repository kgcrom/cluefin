from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Iterable, Sequence

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.formatting import pad
from cluefin_desk.widgets.nav_footer import NavFooter


class FinancialAnalysisScreen(Screen):
    """Screen 7: Financial Analysis via DART API."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
    ]

    # 직전 사업연도 사업보고서 기준 (1분기 11013, 반기 11012, 3분기 11014, 사업 11011)
    DART_REPORT_CODE = "11011"

    # 사업보고서는 사업연도 종료 후 90일 안에 제출된다 — 연초에는 직전 사업연도
    # 보고서가 아직 없으므로 한 해 더 뒤로 물러나며 찾는다.
    DART_YEAR_LOOKBACK = 2

    # DART(corp_code)가 필요한 탭들 — 키가 없거나 비상장(ETF/ETN)이면 한꺼번에 안내한다.
    _DART_PANELS = (
        "#financial-statement-content",
        "#dividend-content",
        "#major-shareholder-content",
        "#share-change-content",
        "#xbrl-content",
        "#disclosure-status",
    )

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
                with VerticalScroll():
                    yield Static("Loading financial statements...", id="financial-statement-content")
            with TabPane("공시목록", id="tab-disclosure"):
                yield DataTable(id="disclosure-list-content")
                yield Static("", id="disclosure-status")
            with TabPane("배당", id="tab-dividend"):
                with VerticalScroll():
                    yield Static("Loading dividend data...", id="dividend-content")
            with TabPane("주요주주", id="tab-shareholder"):
                with VerticalScroll():
                    yield Static("Loading major shareholder data...", id="major-shareholder-content")
            with TabPane("주식변동", id="tab-share-change"):
                with VerticalScroll():
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

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="financial-load")
    def load_all_data(self) -> None:
        self._guarded("#kis-financial-content", "KIS 재무", self._load_kis_financials)

        dart_client = self.app.dart_client
        if dart_client is None:
            self._show_dart_unavailable(
                "DART API key not configured.\nSet DART_AUTH_KEY in .env to use financial analysis."
            )
            return

        try:
            corp_code = self._get_corp_code(dart_client)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to resolve corp_code for {self.stock_code}: {e}")
            self._show_dart_unavailable(f"DART corp_code 조회 실패: {e}")
            return

        if not corp_code:
            self._show_dart_unavailable(
                f"{self.stock_code} 는 DART 공시대상 법인이 아닙니다 (ETF/ETN 등은 조회할 수 없습니다)."
            )
            return

        self._guarded("#disclosure-status", "공시목록", self._load_disclosure_list, dart_client, corp_code)
        self._guarded("#financial-statement-content", "재무제표", self._load_dart_statements, dart_client, corp_code)
        self._guarded("#dividend-content", "배당", self._load_dividend_info, dart_client, corp_code)
        self._guarded("#major-shareholder-content", "주요주주", self._load_major_shareholders, dart_client, corp_code)
        self._guarded("#share-change-content", "주식변동", self._load_share_change, dart_client, corp_code)
        # XBRL download+parse is the slowest step — keep it last in the worker.
        self._guarded("#xbrl-content", "XBRL", self._load_xbrl, dart_client, corp_code)

    def _guarded(self, selector: str, label: str, fn: Callable[..., None], *args) -> None:
        """Run one tab loader; a failure must show up in that tab, not only in the log."""
        try:
            fn(*args)
        except Exception as e:
            from loguru import logger

            logger.error(f"Failed to load {label}: {e}")
            self._update_panel(selector, [f"{label} 로딩 실패: {e}"])

    def _update_panel(self, selector: str, lines: Sequence[str]) -> None:
        text = "\n".join(lines)

        def _apply():
            self.query_one(selector, Static).update(text)

        self.app.call_from_thread(_apply)

    def _show_dart_unavailable(self, message: str) -> None:
        def _apply():
            self.query_one("#disclosure-list-content", DataTable).clear()
            for selector in self._DART_PANELS:
                self.query_one(selector, Static).update(message)

        self.app.call_from_thread(_apply)

    def _get_corp_code(self, dart_client) -> str | None:
        """Memoised corp_code lookup — corp_code() downloads the full corp index,
        so resolve it once per screen, not once per tab."""
        if not self._corp_code_resolved:
            self._corp_code = self._find_corp_code(dart_client)
            self._corp_code_resolved = True
        return self._corp_code

    @classmethod
    def _dart_years(cls) -> list[str]:
        """조회 대상 사업연도, 최신 우선 — 직전 사업연도부터 뒤로."""
        this_year = datetime.now().year
        return [str(this_year - offset) for offset in range(1, cls.DART_YEAR_LOOKBACK + 1)]

    @classmethod
    def _fetch_with_year_fallback(cls, call: Callable[[str], Any]) -> tuple[list, str]:
        """`call(year)` 을 최신 연도부터 시도해 데이터가 있는 첫 응답을 쓴다.

        DART 는 데이터가 없을 때 status 013 + `list=None` 로 200 을 돌려주므로
        예외가 아니라 빈 목록으로 판별한다.
        """
        years = cls._dart_years()
        for year in years:
            items = call(year).result.list or []
            if items:
                return items, year
        return [], years[0]

    def _load_kis_financials(self) -> None:
        """KIS 재무비율·손익계산서 시계열. 진행연도 누적(YTD) 행이 연간 행과 섞여
        내려오므로 기간을 그대로 보여주고 라벨로만 구분한다."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:
            self._update_panel(
                "#kis-financial-content",
                ["KIS API keys not configured.", "Set KIS_APP_KEY / KIS_SECRET_KEY in .env to use KIS financials."],
            )
            return

        ratios = fetcher.get_financial_ratio_series(self.stock_code)
        statements = fetcher.get_income_statement_series(self.stock_code)
        self._update_panel("#kis-financial-content", self._format_kis_financial_lines(statements, ratios))

    @staticmethod
    def _format_kis_financial_lines(statements: Iterable, ratios: Iterable) -> list[str]:
        statements, ratios = list(statements or []), list(ratios or [])
        lines: list[str] = []
        if statements:
            lines += [
                "[bold]손익계산서 (KIS, 년 시리즈 — 최신 행은 진행연도 누적일 수 있음)[/bold]",
                "",
                f"{pad('결산', 8, 'right')} {pad('매출액', 14, 'right')} "
                f"{pad('영업이익', 14, 'right')} {pad('당기순이익', 14, 'right')}",
                "-" * 56,
            ]
            for item in statements[:8]:
                lines.append(
                    f"{pad(item.stac_yymm, 8, 'right')} {pad(item.sale_account, 14, 'right')} "
                    f"{pad(item.bsop_prti, 14, 'right')} {pad(item.thtr_ntin, 14, 'right')}"
                )
        if ratios:
            lines += [
                "",
                "[bold]재무비율 (KIS)[/bold]",
                "",
                f"{pad('결산', 8, 'right')} {pad('ROE', 8, 'right')} {pad('부채비율', 10, 'right')} "
                f"{pad('유보율', 12, 'right')} {pad('매출성장', 10, 'right')}",
                "-" * 56,
            ]
            for item in ratios[:8]:
                lines.append(
                    f"{pad(item.stac_yymm, 8, 'right')} {pad(item.roe_val, 8, 'right')} "
                    f"{pad(item.lblt_rate, 10, 'right')} {pad(item.rsrv_rate, 12, 'right')} "
                    f"{pad(item.grs, 10, 'right')}"
                )
        if not lines:
            lines = ["No KIS financial data available (ETF/ETN and some names have none)."]
        return lines

    def _load_disclosure_list(self, dart_client, corp_code: str) -> None:
        items = (
            dart_client.public_disclosure.public_disclosure_search(
                corp_code=corp_code,
                page_count=20,
            ).result.list
            or []
        )

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
            self.query_one("#disclosure-status", Static).update("" if items else "최근 공시가 없습니다.")
            if items:
                title = self.query_one("#financial-title-bar", Static)
                title.update(f"[bold]{items[0].corp_name}[/bold] ({self.stock_code}) — 재무 분석  [Esc·뒤로]")

        self.app.call_from_thread(_update_disclosure_table)

    _INDICATOR_CATEGORIES = {
        "M210000": "수익성",
        "M220000": "안정성",
        "M230000": "성장성",
        "M240000": "활동성",
    }

    def _load_dart_statements(self, dart_client, corp_code: str) -> None:
        """주요 재무계정·재무지표 (DART 정기보고서)."""
        from cluefin_openapi.dart._periodic_report_financial_statement import (
            PeriodicReportFinancialStatement,
        )

        statement_api = PeriodicReportFinancialStatement(dart_client)

        accounts, year = self._fetch_with_year_fallback(
            lambda y: statement_api.get_single_company_major_accounts(
                corp_code=corp_code,
                bsns_year=y,
                reprt_code=self.DART_REPORT_CODE,
            )
        )

        indicators: list[tuple[str, str, str]] = []
        for idx_cl_code, category in self._INDICATOR_CATEGORIES.items():
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

        self._update_panel("#financial-statement-content", self._format_statement_lines(accounts, indicators, year))

    @staticmethod
    def _select_accounts(accounts: Iterable) -> list:
        """연결(CFS)만 남긴다 — 연결·개별이 같은 계정명으로 함께 내려오므로
        섞어서 보여주면 어느 기준의 수치인지 알 수 없다. 연결이 없는 회사는 개별."""
        accounts = list(accounts or [])
        consolidated = [item for item in accounts if getattr(item, "fs_div", None) == "CFS"]
        selected = consolidated or accounts

        seen: set[str] = set()
        deduped = []
        for item in selected:
            if item.account_nm in seen:
                continue
            seen.add(item.account_nm)
            deduped.append(item)
        return deduped

    @classmethod
    def _format_statement_lines(
        cls, accounts: Iterable, indicators: Iterable[tuple[str, str, str]], year: str
    ) -> list[str]:
        selected = cls._select_accounts(accounts)
        basis = "연결" if any(getattr(item, "fs_div", None) == "CFS" for item in selected) else "개별"

        lines = [f"[bold]주요 재무계정 (DART, {year} 사업보고서 · {basis})[/bold]", ""]
        if selected:
            lines.append(f"{pad('계정', 14)} {pad('당기', 18, 'right')} {pad('전기', 18, 'right')}")
            lines.append("-" * 54)
            for item in selected:
                lines.append(
                    f"{pad(item.account_nm, 14)} {pad(item.thstrm_amount or '-', 18, 'right')} "
                    f"{pad(item.frmtrm_amount or '-', 18, 'right')}"
                )
        else:
            lines.append("재무계정 데이터 없음")

        indicators = list(indicators or [])
        if indicators:
            lines += ["", "[bold]주요 재무지표 (DART)[/bold]", ""]
            for category, name, value in indicators:
                lines.append(f"  [{category}] {name}: {value}")
        return lines

    def _load_dividend_info(self, dart_client, corp_code: str) -> None:
        """배당 관련 사항 (DART 정기보고서)."""
        items, year = self._fetch_with_year_fallback(
            lambda y: dart_client.periodic_report_key_information.get_dividend_information(
                corp_code=corp_code,
                bsns_year=y,
                reprt_code=self.DART_REPORT_CODE,
            )
        )
        self._update_panel("#dividend-content", self._format_dividend_lines(items, year))

    @staticmethod
    def _format_dividend_lines(items: Iterable, year: str) -> list[str]:
        items = list(items or [])
        if not items:
            return ["배당 데이터 없음"]

        lines = [
            f"[bold]배당에 관한 사항 (DART, {year} 사업보고서)[/bold]",
            "",
            f"{pad('구분', 28)} {pad('당기', 14, 'right')} {pad('전기', 14, 'right')} {pad('전전기', 14, 'right')}",
            "-" * 76,
        ]
        for item in items[:20]:
            label = (item.se or "-") + (f" ({item.stock_knd})" if item.stock_knd else "")
            lines.append(
                f"{pad(label, 28)} {pad(item.thstrm or '-', 14, 'right')} "
                f"{pad(item.frmtrm or '-', 14, 'right')} {pad(item.lwfr or '-', 14, 'right')}"
            )
        return lines

    def _load_major_shareholders(self, dart_client, corp_code: str) -> None:
        """최대주주 현황 (DART 정기보고서).

        이전 구현은 존재하지 않는 `dart_client.share_disclosure` 를 호출해 항상
        실패했다 — 정기보고서 주요정보의 최대주주 현황으로 교체.
        """
        items, year = self._fetch_with_year_fallback(
            lambda y: dart_client.periodic_report_key_information.get_major_shareholder_status(
                corp_code=corp_code,
                bsns_year=y,
                reprt_code=self.DART_REPORT_CODE,
            )
        )
        self._update_panel("#major-shareholder-content", self._format_shareholder_lines(items, year))

    @staticmethod
    def _format_shareholder_lines(items: Iterable, year: str) -> list[str]:
        items = list(items or [])
        if not items:
            return ["No major shareholder data available"]

        lines = [
            f"[bold]최대주주 현황 (DART, {year} 사업보고서)[/bold]",
            "",
            f"{pad('성명', 20)} {pad('관계', 12)} {pad('기말 보유주식수', 16, 'right')} {pad('지분율', 8, 'right')}",
            "-" * 62,
        ]
        for item in items[:20]:
            lines.append(
                f"{pad(item.nm, 20)} {pad(item.relate or '-', 12)} "
                f"{pad(item.trmend_posesn_stock_co or '-', 16, 'right')} "
                f"{pad((item.trmend_posesn_stock_qota_rt or '-') + '%', 8, 'right')}"
            )
        return lines

    def _load_share_change(self, dart_client, corp_code: str) -> None:
        """주식의 총수 현황 + 증자(감자) 현황 (DART 정기보고서).

        총수는 매년 있지만 증자·감자는 없는 해가 많아, 두 섹션의 사업연도가
        서로 다를 수 있다 — 그래서 각 섹션에 해당 연도를 함께 표시한다.
        """
        key_info = dart_client.periodic_report_key_information
        totals, totals_year = self._fetch_with_year_fallback(
            lambda y: key_info.get_total_number_of_shares(
                corp_code=corp_code,
                bsns_year=y,
                reprt_code=self.DART_REPORT_CODE,
            )
        )
        changes, changes_year = self._fetch_with_year_fallback(
            lambda y: key_info.get_capital_change_status(
                corp_code=corp_code,
                bsns_year=y,
                reprt_code=self.DART_REPORT_CODE,
            )
        )
        self._update_panel(
            "#share-change-content",
            self._format_share_change_lines(totals, totals_year, changes, changes_year),
        )

    @staticmethod
    def _format_share_change_lines(
        totals: Iterable, totals_year: str, changes: Iterable, changes_year: str
    ) -> list[str]:
        totals, changes = list(totals or []), list(changes or [])
        if not totals and not changes:
            return ["주식변동 데이터 없음"]

        lines: list[str] = []
        if totals:
            lines += [
                f"[bold]주식의 총수 현황 (DART, {totals_year} 사업보고서)[/bold]",
                "",
                f"{pad('구분', 14)} {pad('발행주식총수', 18, 'right')} "
                f"{pad('자기주식수', 16, 'right')} {pad('유통주식수', 18, 'right')}",
                "-" * 70,
            ]
            for item in totals[:10]:
                lines.append(
                    f"{pad(item.se, 14)} {pad(item.istc_totqy or '-', 18, 'right')} "
                    f"{pad(item.tesstk_co or '-', 16, 'right')} {pad(item.distb_stock_co or '-', 18, 'right')}"
                )

        if changes:
            if lines:
                lines.append("")
            lines += [
                f"[bold]증자(감자) 현황 (DART, {changes_year} 사업보고서)[/bold]",
                "",
                f"{pad('일자', 12)} {pad('형태', 16)} {pad('주식종류', 12)} "
                f"{pad('수량', 16, 'right')} {pad('발행가', 14, 'right')}",
                "-" * 74,
            ]
            for item in changes[:20]:
                lines.append(
                    f"{pad(item.isu_dcrs_de, 12)} {pad(item.isu_dcrs_stle, 16)} "
                    f"{pad(item.isu_dcrs_stock_knd, 12)} {pad(item.isu_dcrs_qy or '-', 16, 'right')} "
                    f"{pad(item.isu_dcrs_mstvdv_amount or '-', 14, 'right')}"
                )
        else:
            lines += ["", "증자(감자) 내역 없음"]

        return lines

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

    def _load_xbrl(self, dart_client, corp_code: str) -> None:
        """XBRL 본표·주석 (cluefin-xbrl). 사업보고서를 내려받아 본표 요약과 주석
        목차를 보여준다 — 주석 전문은 TUI 에 맞지 않아 목차만 표시한다."""
        from cluefin_desk.data.xbrl import XbrlStatementFetcher

        fetcher = XbrlStatementFetcher(dart_client)

        rcept_no: str | None = None
        year = self._dart_years()[0]
        for candidate in self._dart_years():
            rcept_no = fetcher.find_rcept_no(corp_code, candidate, self.DART_REPORT_CODE)
            if rcept_no is not None:
                year = candidate
                break

        if rcept_no is None:
            self._update_panel(
                "#xbrl-content", [f"{'·'.join(self._dart_years())} 사업보고서 XBRL 공시를 찾지 못했습니다."]
            )
            return

        bundle = fetcher.fetch(rcept_no, self.DART_REPORT_CODE)
        self._update_panel("#xbrl-content", self._format_xbrl_lines(bundle, year, rcept_no))

    @classmethod
    def _format_xbrl_lines(cls, bundle, year: str, rcept_no: str) -> list[str]:
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
            lines += ["", f"[bold cyan]{cls._XBRL_STATEMENT_LABELS.get(stmt_key, stmt_key)}[/bold cyan]"]
            for item in stmt.line_items[:25]:
                indent = "  " * item.depth
                label = item.label_ko or item.concept_local_name
                if item.is_abstract:
                    lines.append(f"{indent}[bold]{label}[/bold]")
                else:
                    lines.append(
                        f"{indent}{pad(label, max(4, 40 - len(indent)))} {pad(cls._format_xbrl_value(item.value), 18, 'right')}"
                    )

        notes = sorted(
            (n for n in bundle.notes.notes.values() if n.is_consolidated == (basis == "연결")),
            key=lambda n: n.role_code,
        )
        if notes:
            lines += ["", f"[bold cyan]주석 목차 ({len(notes)}건)[/bold cyan]"]
            for note in notes[:30]:
                lines.append(f"  {note.role_code}  {note.title or '-'}  ({len(note.line_items)} items)")
        return lines

    def _find_corp_code(self, dart_client) -> str | None:
        """Find DART corp_code from stock_code.

        Errors propagate on purpose: "코드를 못 찾았다"(비상장)와 "조회 자체가
        실패했다"(키·네트워크)를 화면에서 구분해야 한다.
        """
        corp_list = dart_client.public_disclosure.corp_code()
        for item in corp_list.result.list or []:
            if item.stock_code == self.stock_code:
                return item.corp_code
        return None

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_all_data()
