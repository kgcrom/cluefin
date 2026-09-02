import asyncio

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static, TabbedContent, TabPane

from cluefin_desk.formatting import pad
from cluefin_desk.screens._guard import screen_gone
from cluefin_desk.widgets.company_info import CompanyInfoWidget
from cluefin_desk.widgets.indicator_panel import IndicatorPanel
from cluefin_desk.widgets.nav_footer import NavFooter
from cluefin_desk.widgets.price_chart import PriceChartWidget


class StockDetailScreen(Screen):
    """Screen 6: Stock detail with 4 tabs (chart, investor, broker, supply-demand)."""

    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "refresh", "Refresh"),
        Binding("f", "financial", "Financial"),
        Binding("m", "run_ml", "ML예측"),
    ]

    def __init__(self, stock_code: str):
        super().__init__()
        self.stock_code = stock_code

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(f"Loading {self.stock_code}...", id="detail-title-bar")
        with TabbedContent(id="detail-tabs"):
            with TabPane("차트", id="tab-chart"):
                with Horizontal(id="detail-chart-content"):
                    with Vertical(id="detail-left"):
                        yield CompanyInfoWidget(id="company-info")
                    with Vertical(id="detail-right"):
                        yield PriceChartWidget(id="price-chart")
                        yield IndicatorPanel(id="indicator-panel")
            with TabPane("투자자", id="tab-investor"):
                yield DataTable(id="investor-detail-table")
            with TabPane("매매원", id="tab-broker"):
                yield Static("Loading broker data...", id="broker-detail-content")
            with TabPane("수급", id="tab-supply"):
                with VerticalScroll():
                    yield Static("Loading supply/demand data...", id="supply-detail-content")
                    yield Static("", id="kis-supply-content")
            with TabPane("투자의견", id="tab-opinion"):
                yield Static("Loading investment opinions...", id="opinion-detail-content")
            with TabPane("ML예측", id="tab-ml"):
                yield Static(
                    "M 키를 누르면 익일 등락 예측을 실행합니다.\n(LightGBM 인메모리 학습 — 수 초에서 수십 초 걸립니다)",
                    id="ml-detail-content",
                )
        yield NavFooter(id="nav-footer")

    def on_mount(self) -> None:
        self.query_one("#nav-footer", NavFooter).active_screen_key = self.app._current_screen_key
        self._setup_investor_table()
        self.load_detail_data()

    def _setup_investor_table(self) -> None:
        tbl = self.query_one("#investor-detail-table", DataTable)
        tbl.cursor_type = "row"
        tbl.zebra_stripes = True
        for label, width in [
            ("일자", 12),
            ("현재가", 10),
            ("등락률", 8),
            ("개인", 12),
            ("외국인", 12),
            ("기관", 12),
        ]:
            tbl.add_column(label, key=label, width=width)

    # `r` 연타로 워커가 겹치면 같은 패널에 두 응답이 번갈아 써진다 — 최신 것만 남긴다.
    @work(thread=True, exclusive=True, group="detail-load")
    def load_detail_data(self) -> None:
        self._guarded("#detail-title-bar", "종목 기본정보", self._load_basic_and_chart)
        self._guarded(None, "투자자", self._load_investor_data)
        self._guarded("#broker-detail-content", "매매원", self._load_broker_data)
        self._guarded("#supply-detail-content", "신용거래", self._load_supply_data)
        self._guarded("#kis-supply-content", "KIS 수급", self._load_kis_supply_data)
        self._guarded("#opinion-detail-content", "투자의견", self._load_kis_opinion_data)

    def _guarded(self, selector: str | None, label: str, fn) -> None:
        """탭 하나가 실패해도 나머지는 계속 로드하고, 실패는 그 탭에 남긴다.
        selector 가 None 인 탭(테이블만 있는 탭)은 로그만 남긴다."""
        try:
            fn()
        except Exception as e:
            if screen_gone(self, e):
                return
            from loguru import logger

            logger.error(f"Failed to load {label}: {e}")
            if selector is not None:
                self._update_panel(selector, [f"{label} 로딩 실패: {e}"])

    def _update_panel(self, selector: str, lines) -> None:
        text = "\n".join(lines)

        def _apply():
            self.query_one(selector, Static).update(text)

        self.app.call_from_thread(_apply)

    def _load_basic_and_chart(self) -> None:
        fetcher = self.app.fetcher
        loop = asyncio.new_event_loop()
        try:
            basic_df = loop.run_until_complete(fetcher.get_basic_data(self.stock_code))
            stock_df = loop.run_until_complete(fetcher.get_stock_data(self.stock_code))
        finally:
            loop.close()

        stock_name = ""
        if not basic_df.empty:
            stock_name = basic_df.iloc[0].get("stock_name", self.stock_code)

        def _update_title():
            title = self.query_one("#detail-title-bar", Static)
            if not basic_df.empty:
                row = basic_df.iloc[0]
                title.update(
                    f"[bold]{row.get('stock_name', 'N/A')}[/bold] ({self.stock_code})  "
                    f"{row.get('market_name', '')}  [F\u00b7재무] [Esc\u00b7뒤로]"
                )

        self.app.call_from_thread(_update_title)

        company_info = self.query_one("#company-info", CompanyInfoWidget)
        self.app.call_from_thread(company_info.update_info, basic_df)

        chart = self.query_one("#price-chart", PriceChartWidget)
        self.app.call_from_thread(chart.update_chart, stock_df, stock_name)

        indicator = self.query_one("#indicator-panel", IndicatorPanel)
        self.app.call_from_thread(indicator.update_indicators, stock_df)

    def _load_investor_data(self) -> None:
        fetcher = self.app.fetcher
        response = fetcher.get_institutional_investor_by_stock(self.stock_code)
        items = response.body.stk_invsr_orgn or []

        def _update():
            tbl = self.query_one("#investor-detail-table", DataTable)
            tbl.clear()
            for item in items[:30]:
                rate = float(item.flu_rt) if item.flu_rt and item.flu_rt != "-" else 0.0
                if rate > 0:
                    rate_str = f"[red]+{rate:.2f}%[/red]"
                elif rate < 0:
                    rate_str = f"[blue]{rate:.2f}%[/blue]"
                else:
                    rate_str = f"{rate:.2f}%"
                tbl.add_row(
                    item.dt,
                    item.cur_prc,
                    rate_str,
                    item.ind_invsr,
                    item.frgnr_invsr,
                    item.orgn,
                    key=item.dt,
                )

        self.app.call_from_thread(_update)

    def _load_broker_data(self) -> None:
        fetcher = self.app.fetcher
        body = fetcher.get_stock_trading_member(self.stock_code).body
        self._update_panel("#broker-detail-content", self._format_broker_lines(body))

    @staticmethod
    def _format_broker_lines(body) -> list[str]:
        lines = [
            f"[bold]매매원 현황 — {body.stk_nm} ({body.stk_cd})[/bold]",
            f"현재가: {body.cur_prc}  등락률: {body.flu_rt}%",
        ]
        for title, prefix in [("매수 상위", "buy"), ("매도 상위", "sel")]:
            lines += ["", f"[bold]{title}[/bold]"]
            for i in range(1, 6):
                nm = getattr(body, f"{prefix}_trde_ori_nm_{i}", "-")
                qty = getattr(body, f"{prefix}_trde_qty_{i}", "-")
                lines.append(f"  {i}. {pad(nm, 16)}  {pad(qty, 12, 'right')}")
        return lines

    def _load_supply_data(self) -> None:
        fetcher = self.app.fetcher
        items = fetcher.get_margin_trading_trend(self.stock_code).body.crd_trde_trend or []
        self._update_panel("#supply-detail-content", self._format_margin_lines(items))

    @staticmethod
    def _format_margin_lines(items) -> list[str]:
        if not items:
            return ["신용거래 추이 데이터 없음"]

        lines = [
            "[bold]신용거래 추이[/bold]",
            "",
            f"{pad('일자', 12)} {pad('현재가', 10, 'right')} {pad('신규', 8, 'right')} "
            f"{pad('상환', 8, 'right')} {pad('잔고', 10, 'right')} {pad('잔고율', 6, 'right')}",
            "-" * 60,
        ]
        for item in items[:15]:
            lines.append(
                f"{pad(item.dt, 12)} {pad(item.cur_prc, 10, 'right')} {pad(item.new, 8, 'right')} "
                f"{pad(item.rpya, 8, 'right')} {pad(item.remn, 10, 'right')} {pad(item.remn_rt, 6, 'right')}"
            )
        return lines

    def _load_kis_supply_data(self) -> None:
        """KIS enrichment for the 수급 tab: per-type daily net buy + 락 events.

        Skipped entirely (panel stays empty) when KIS keys are not configured;
        a lookup failure must not take down the Kiwoom half of the tab.
        """
        fetcher = self.app.fetcher
        if not fetcher.has_kis:
            return

        lines = self._format_kis_supply_lines(
            trend_df=fetcher.get_investor_trend_daily(self.stock_code, days=10),
            actions_df=fetcher.get_corporate_actions(self.stock_code),
            short_rows=fetcher.get_short_selling_trend(self.stock_code),
            credit_rows=fetcher.get_credit_balance_trend(self.stock_code),
            program_rows=fetcher.get_program_trading_trend(self.stock_code),
        )
        if lines:
            self._update_panel("#kis-supply-content", lines)

    @staticmethod
    def _format_kis_supply_lines(trend_df, actions_df, short_rows, credit_rows, program_rows) -> list[str]:
        lines: list[str] = []
        if not trend_df.empty:
            lines += [
                "",
                "[bold]투자자별 일별 순매수 (KIS, 주)[/bold]",
                "",
                f"{pad('일자', 11)} {pad('개인', 12, 'right')} {pad('외국인', 12, 'right')} "
                f"{pad('기관계', 12, 'right')} {pad('연기금', 12, 'right')}",
                "-" * 64,
            ]
            for date, row in trend_df.sort_index(ascending=False).iterrows():
                lines.append(
                    f"{pad(date.strftime('%Y-%m-%d'), 11)} {row['개인']:>12,.0f} "
                    f"{row['외국인']:>12,.0f} {row['기관계']:>12,.0f} {row['연기금']:>12,.0f}"
                )

        if short_rows:
            lines += [
                "",
                "[bold]공매도 추이 (KIS)[/bold]",
                "",
                f"{pad('일자', 10)} {pad('공매도량', 12, 'right')} {pad('비중', 8, 'right')} "
                f"{pad('누적', 14, 'right')}",
                "-" * 50,
            ]
            for item in short_rows[:5]:
                lines.append(
                    f"{pad(item.stck_bsop_date, 10)} {pad(item.ssts_cntg_qty, 12, 'right')} "
                    f"{pad(item.ssts_vol_rlim + '%', 8, 'right')} {pad(item.acml_ssts_cntg_qty, 14, 'right')}"
                )

        if credit_rows:
            lines += [
                "",
                "[bold]신용잔고 추이 (KIS)[/bold]",
                "",
                f"{pad('일자', 10)} {pad('융자잔고', 14, 'right')} {pad('잔고비율', 8, 'right')}",
                "-" * 38,
            ]
            for item in credit_rows[:5]:
                lines.append(
                    f"{pad(item.deal_date, 10)} {pad(item.whol_loan_rmnd_stcn, 14, 'right')} "
                    f"{pad(item.whol_loan_rmnd_rate + '%', 8, 'right')}"
                )

        if program_rows:
            lines += [
                "",
                "[bold]프로그램매매 추이 (KIS)[/bold]",
                "",
                f"{pad('일자', 10)} {pad('순매수량', 12, 'right')} {pad('순매수대금', 14, 'right')}",
                "-" * 40,
            ]
            for item in program_rows[:5]:
                lines.append(
                    f"{pad(item.stck_bsop_date, 10)} {pad(item.whol_smtn_ntby_qty, 12, 'right')} "
                    f"{pad(item.whol_smtn_ntby_tr_pbmn, 14, 'right')}"
                )

        if not actions_df.empty:
            lines += ["", "[bold]최근 권리락/배당락 (KIS)[/bold]", ""]
            for date, row in actions_df.sort_index(ascending=False).iterrows():
                lines.append(f"  {date.strftime('%Y-%m-%d')}  {row['event']}")

        return lines

    def _load_kis_opinion_data(self) -> None:
        """증권사 투자의견 탭 (KIS 전용 — Kiwoom/DART 에 대응 데이터가 없다)."""
        fetcher = self.app.fetcher
        if not fetcher.has_kis:
            self._update_panel(
                "#opinion-detail-content",
                ["KIS API keys not configured.", "Set KIS_APP_KEY / KIS_SECRET_KEY in .env to see 투자의견."],
            )
            return

        opinions = fetcher.get_investment_opinions(self.stock_code)
        self._update_panel("#opinion-detail-content", self._format_opinion_lines(opinions))

    @staticmethod
    def _format_opinion_lines(opinions) -> list[str]:
        opinions = list(opinions or [])
        if not opinions:
            return ["최근 6개월 내 증권사 투자의견이 없습니다."]

        lines = [
            "[bold]증권사 투자의견 (KIS, 최근 6개월)[/bold]",
            "",
            f"{pad('일자', 10)} {pad('증권사', 12)} {pad('의견', 8)} {pad('이전의견', 10)} "
            f"{pad('목표가', 10, 'right')} {pad('괴리율', 8, 'right')}",
            "-" * 62,
        ]
        for item in opinions[:20]:
            lines.append(
                f"{pad(item.stck_bsop_date, 10)} {pad(item.mbcr_name, 12)} {pad(item.invt_opnn, 8)} "
                f"{pad(item.rgbf_invt_opnn, 10)} {pad(item.hts_goal_prc, 10, 'right')} "
                f"{pad((item.dprt or '-') + '%', 8, 'right')}"
            )
        return lines

    def action_run_ml(self) -> None:
        panel = self.query_one("#ml-detail-content", Static)
        panel.update("모델 학습 중... (LightGBM, 인메모리 재학습)")
        self._run_ml_prediction()

    @work(thread=True, exclusive=True, group="ml-predict")
    def _run_ml_prediction(self) -> None:
        """cli --ml-predict 이식: 매 실행마다 인메모리로 학습→예측한다.

        rich Console 을 쓰는 predictor.display_* 는 TUI 를 깨뜨리므로 호출하지
        않고 결과 dict/metrics 만 받아 Static 으로 렌더링한다.
        """
        try:
            from cluefin_desk.ml import StockMLPredictor
            from cluefin_desk.ml.indicators import TechnicalAnalyzer

            fetcher = self.app.fetcher
            loop = asyncio.new_event_loop()
            try:
                stock_df = loop.run_until_complete(fetcher.get_stock_data(self.stock_code))
            finally:
                loop.close()

            if len(stock_df) < 30:

                def _too_short():
                    self.query_one("#ml-detail-content", Static).update(
                        f"예측 불가: 일봉 {len(stock_df)}개 — 최소 30개가 필요합니다."
                    )

                self.app.call_from_thread(_too_short)
                return

            indicators = TechnicalAnalyzer().calculate_all(stock_df)

            predictor = StockMLPredictor()
            prepared_df, _ = predictor.prepare_data(stock_df, indicators)
            metrics = predictor.train_model(prepared_df)
            result = predictor.predict(stock_df, indicators)
            importance = predictor.model.get_feature_importance(top_n=10)

            def _update():
                signal = result["signal"]
                signal_str = f"[red]▲ {signal}[/red]" if signal == "BUY" else f"[blue]▼ {signal}[/blue]"
                lines = [
                    f"[bold]익일 등락 예측 (LightGBM) — {self.stock_code}[/bold]",
                    "",
                    f"시그널: {signal_str}   신뢰도: {result['confidence']:.1%}",
                    f"상승 확률: {result['probability_up']:.1%}   하락 확률: {result['probability_down']:.1%}",
                    "",
                    "[bold]학습 성능 (검증셋)[/bold]",
                ]
                for key in ("accuracy", "precision", "recall", "f1", "roc_auc"):
                    if key in metrics:
                        lines.append(f"  {key}: {metrics[key]:.4f}")

                if importance is not None and len(importance) > 0:
                    lines += ["", "[bold]피처 중요도 상위 10[/bold]"]
                    max_imp = float(importance.iloc[0]) or 1.0
                    for name, value in importance.items():
                        bar = "█" * max(1, int(float(value) / max_imp * 20))
                        lines.append(f"  {name:<28s} {bar} {float(value):.0f}")

                lines += ["", "[dim]참고용 통계 모델입니다 — 투자 판단의 근거가 아닙니다.[/dim]"]
                self.query_one("#ml-detail-content", Static).update("\n".join(lines))

            self.app.call_from_thread(_update)
        except Exception as e:
            if screen_gone(self, e):
                return
            from loguru import logger

            logger.error(f"ML prediction failed: {e}")
            err_msg = str(e)

            def _update_err():
                self.query_one("#ml-detail-content", Static).update(f"ML 예측 실패: {err_msg}")

            self.app.call_from_thread(_update_err)

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_refresh(self) -> None:
        self.load_detail_data()

    def action_financial(self) -> None:
        from cluefin_desk.screens.financial_analysis import FinancialAnalysisScreen

        self.app.push_screen(FinancialAnalysisScreen(stock_code=self.stock_code))
