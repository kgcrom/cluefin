from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd
from cluefin_openapi.kis._auth import Auth as KisAuth
from cluefin_openapi.kis._exceptions import KISAPIError
from cluefin_openapi.kis._http_client import HttpClient as KisClient
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient
from loguru import logger
from pydantic import SecretStr, ValidationError

from cluefin_desk.config.settings import settings


class DomesticDataFetcher:
    """Handles domestic stock data fetching from Kiwoom and KIS APIs.

    Kiwoom stays the primary source and authenticates eagerly at startup
    (existing behavior). KIS is optional enrichment: the client is built
    lazily on first use, so users without KIS keys keep every Kiwoom screen.
    """

    @staticmethod
    def _safe_float(value: str) -> float:
        if value == "-" or not value or value.strip() == "":
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def __init__(self):
        if not settings.kiwoom_app_key:
            raise ValueError("KIWOOM_APP_KEY environment variable is required")
        if not settings.kiwoom_secret_key:
            raise ValueError("KIWOOM_SECRET_KEY environment variable is required")

        auth = KiwoomAuth(
            app_key=settings.kiwoom_app_key,
            secret_key=SecretStr(settings.kiwoom_secret_key),
            env=settings.kiwoom_env,
        )
        token = auth.generate_token()
        self.kiwoom_client = KiwoomClient(
            token=token.get_token(),
            env=settings.kiwoom_env,
        )
        self._kis_client: Optional[KisClient] = None

    @property
    def kis_client(self) -> KisClient:
        """Build (once) the KIS client, generating a token on first use."""
        if self._kis_client is None:
            if not settings.kis_app_key:
                raise ValueError("KIS_APP_KEY environment variable is required")
            if not settings.kis_secret_key:
                raise ValueError("KIS_SECRET_KEY environment variable is required")

            auth = KisAuth(
                app_key=settings.kis_app_key,
                secret_key=SecretStr(settings.kis_secret_key),
                env=settings.kis_env,
            )
            token = auth.generate()
            self._kis_client = KisClient(
                token=token.get_token(),
                app_key=settings.kis_app_key,
                secret_key=SecretStr(settings.kis_secret_key),
                env=settings.kis_env,
            )
        return self._kis_client

    @property
    def has_kis(self) -> bool:
        """True when KIS credentials are configured (client may not be built yet)."""
        return bool(settings.kis_app_key and settings.kis_secret_key)

    # ──────────────────────────────────────
    # Basic stock data
    # ──────────────────────────────────────

    async def get_basic_data(self, stock_code: str) -> pd.DataFrame:
        """Fetch basic company data — KIS when configured, Kiwoom otherwise.

        Both paths return the same widget-facing keys (stock_name, market_cap,
        per/pbr/roe/eps/bps, sector_name, market_name); the KIS path adds price,
        52-week, supply/demand and financial columns on top.
        """
        if self.has_kis:
            return self._get_basic_data_kis(stock_code)
        return self._get_basic_data_kiwoom(stock_code)

    def _get_basic_data_kiwoom(self, stock_code: str) -> pd.DataFrame:
        stock_info = self.kiwoom_client.stock_info.get_stock_info(stock_code)
        stock_info_v1 = self.kiwoom_client.stock_info.get_stock_info_v1(stock_code)

        info = stock_info.body
        info_v1 = stock_info_v1.body

        merged_data = {
            "stock_code": info.stk_cd,
            "stock_name": info.stk_nm,
            "market_cap": info.mac,
            "per": info.per,
            "eps": info.eps,
            "roe": info.roe,
            "pbr": info.pbr,
            "bps": info.bps,
            "sector_name": info_v1.upName,
            "market_name": info_v1.marketName,
        }
        return pd.DataFrame([merged_data])

    def _get_basic_data_kis(self, stock_code: str) -> pd.DataFrame:
        # 주식현재가 시세 (FHKST01010100) carries the valuation/price block; 주식기본조회
        # (CTPF1002R) carries the identity block (name, listing date, 업종) that the
        # quote response leaves out.
        price = self.kis_client.domestic_basic_quote.get_stock_current_price(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd=stock_code,
        ).body.output
        product = self.kis_client.domestic_stock_info.get_stock_basic_info(
            prdt_type_cd="300",
            pdno=stock_code,
        ).body.output

        merged_data: Dict[str, Any] = {"stock_code": stock_code}

        if price is not None:
            merged_data.update(
                {
                    "market_name": price.rprs_mrkt_kor_name,
                    "industry_name": price.bstp_kor_isnm,
                    "settlement_month": price.stac_month,
                    "current_price": price.stck_prpr,
                    "price_change": price.prdy_vrss,
                    "price_change_rate": price.prdy_ctrt,
                    "market_cap": price.hts_avls,
                    "per": price.per,
                    "pbr": price.pbr,
                    "eps": price.eps,
                    "bps": price.bps,
                    "listed_shares": price.lstn_stcn,
                    "turnover_ratio": price.vol_tnrt,
                    "foreign_exhaustion_rate": price.hts_frgn_ehrt,
                    "credit_ratio": price.whol_loan_rmnd_rate,
                    "52_week_high": price.w52_hgpr,
                    "52_week_high_date": price.w52_hgpr_date,
                    "52_week_low": price.w52_lwpr,
                    "52_week_low_date": price.w52_lwpr_date,
                }
            )

        if product is not None:
            merged_data.update(
                {
                    "stock_name": product.prdt_abrv_name or product.prdt_name,
                    "registration_day": product.scts_mket_lstg_dt or product.kosdaq_mket_lstg_dt,
                    "sector_name": product.idx_bztp_mcls_cd_name,
                    "sector_detail_name": product.idx_bztp_scls_cd_name,
                    "state": self._describe_state(product.admn_item_yn, product.tr_stop_yn),
                }
            )

        merged_data.update(
            self._fetch_financial_metrics(stock_code, settlement_month=merged_data.get("settlement_month"))
        )

        return pd.DataFrame([merged_data])

    def _fetch_financial_metrics(self, stock_code: str, settlement_month: Optional[str] = None) -> Dict[str, Any]:
        """Fill in the profitability/scale figures the quote response omits.

        KIS 재무비율 (FHKST66430300) and 손익계산서 (FHKST66430200) cover ROE, 매출액,
        영업이익 and 당기순이익. Neither exists for ETF/ETN, so a failure here degrades
        to "no financial rows" rather than failing the whole lookup.

        `fid_div_cls_code="0"` is documented as 년(annual) but the live series leads with
        the *in-progress* fiscal year's cumulative figures. Reporting that row as annual
        inflates ROE and every growth rate, so the completed year is used for the
        headline numbers and the cumulative row is surfaced separately as YTD.
        """
        metrics: Dict[str, Any] = {}

        annual_ratio, ytd_ratio = self._split_annual_and_ytd(
            self.get_financial_ratio_series(stock_code), settlement_month
        )
        if annual_ratio is not None:
            metrics.update(
                {
                    "financial_period": annual_ratio.stac_yymm,
                    "roe": annual_ratio.roe_val,
                    "revenue_growth_rate": annual_ratio.grs,
                    "operating_profit_growth_rate": annual_ratio.bsop_prfi_inrt,
                    "net_profit_growth_rate": annual_ratio.ntin_inrt,
                    "debt_ratio": annual_ratio.lblt_rate,
                    "reserve_ratio": annual_ratio.rsrv_rate,
                }
            )
        if ytd_ratio is not None:
            metrics.update(
                {
                    "ytd_period": ytd_ratio.stac_yymm,
                    "ytd_roe": ytd_ratio.roe_val,
                    "ytd_debt_ratio": ytd_ratio.lblt_rate,
                }
            )

        annual_statement, ytd_statement = self._split_annual_and_ytd(
            self.get_income_statement_series(stock_code), settlement_month
        )
        if annual_statement is not None:
            metrics.update(
                {
                    "financial_period": annual_statement.stac_yymm,
                    "revenue": annual_statement.sale_account,
                    "operating_profit": annual_statement.bsop_prti,
                    "net_profit": annual_statement.thtr_ntin,
                }
            )
        if ytd_statement is not None:
            metrics.update(
                {
                    "ytd_period": ytd_statement.stac_yymm,
                    "ytd_revenue": ytd_statement.sale_account,
                    "ytd_operating_profit": ytd_statement.bsop_prti,
                    "ytd_net_profit": ytd_statement.thtr_ntin,
                }
            )

        return metrics

    def get_financial_ratio_series(self, stock_code: str) -> list:
        """KIS 재무비율 series (년 단위 + 진행연도 누적 행), newest first on live.

        Degrades to [] for ETF/ETN and other names with no financial rows.
        """
        try:
            return (
                self.kis_client.domestic_stock_info.get_financial_ratio(
                    fid_div_cls_code="0",
                    fid_cond_mrkt_div_code="J",
                    fid_input_iscd=stock_code,
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"financial ratio unavailable for {stock_code}: {exc}")
            return []

    def get_income_statement_series(self, stock_code: str) -> list:
        """KIS 손익계산서 series (년 단위 + 진행연도 누적 행), newest first on live.

        Degrades to [] for ETF/ETN and other names with no financial rows.
        """
        try:
            return (
                self.kis_client.domestic_stock_info.get_income_statement(
                    fid_div_cls_code="0",
                    fid_cond_mrkt_div_code="J",
                    fid_input_iscd=stock_code,
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"income statement unavailable for {stock_code}: {exc}")
            return []

    @staticmethod
    def _split_annual_and_ytd(items, settlement_month: Optional[str]):
        """Split the KIS "년" series into (completed fiscal year, in-progress cumulative).

        A row belongs to a completed year when its 결산 년월 ends on the company's
        settlement month. Without a usable settlement month there is nothing to compare
        against, so the newest row is treated as annual and no YTD row is reported.
        """
        if not items:
            return None, None

        ordered = sorted(items, key=lambda item: item.stac_yymm, reverse=True)
        if not settlement_month:
            return ordered[0], None

        month = str(settlement_month).zfill(2)
        annual = next((item for item in ordered if item.stac_yymm[4:] == month), None)
        if annual is None:
            return ordered[0], None

        ytd = ordered[0] if ordered[0].stac_yymm != annual.stac_yymm else None
        return annual, ytd

    @staticmethod
    def _describe_state(admin_issue_yn: str, trading_halt_yn: str) -> str:
        """Summarise the KIS admin/halt flags the way Kiwoom's `state` field read."""
        flags = []
        if admin_issue_yn == "Y":
            flags.append("관리종목")
        if trading_halt_yn == "Y":
            flags.append("거래정지")
        return " / ".join(flags) if flags else "정상"

    _CORPORATE_ACTION_LABELS = {
        "01": "권리락",
        "02": "배당락",
        "03": "분배락",
        "04": "권배락",
        "05": "중간배당락",
        "06": "권리중간배당락",
        "07": "권리분기배당락",
    }

    def get_corporate_actions(self, stock_code: str, days: int = 100) -> pd.DataFrame:
        """Fetch 권리락/배당락 events for the recent sessions.

        Kiwoom's 일봉차트 carries no 락 구분, so this comes from KIS 기간별시세
        (`FHKST03010100`), which tags each bar with 락구분코드 and 분할비율.
        KIS caps this response at the 100 most recent bars regardless of the
        requested range.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            bars = self.kis_client.domestic_basic_quote.get_stock_period_quote(
                fid_cond_mrkt_div_code="J",
                fid_input_iscd=stock_code,
                fid_input_date_1=start_date.strftime("%Y%m%d"),
                fid_input_date_2=end_date.strftime("%Y%m%d"),
                fid_period_div_code="D",
                fid_org_adj_prc="0",
            ).body.output2
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"period quote unavailable for {stock_code}: {exc}")
            return pd.DataFrame()

        rows = [
            {
                "date": pd.to_datetime(bar.stck_bsop_date),
                "event": self._CORPORATE_ACTION_LABELS.get(bar.flng_cls_code, bar.flng_cls_code),
                "split_ratio": self._safe_float(bar.prtt_rate),
            }
            for bar in bars
            if bar.flng_cls_code and bar.flng_cls_code != "00"
        ]
        if not rows:
            return pd.DataFrame()

        return pd.DataFrame(rows).set_index("date").sort_index()

    # KIS 종목별 투자자매매동향(일별) breaks 기관 down into 8 sub-categories that
    # Kiwoom's 기간 누적 endpoint lumps together.
    _INVESTOR_COLUMNS = (
        ("개인", "prsn_ntby_qty"),
        ("외국인", "frgn_ntby_qty"),
        ("기관계", "orgn_ntby_qty"),
        ("금융투자", "scrt_ntby_qty"),
        ("투신", "ivtr_ntby_qty"),
        ("사모펀드", "pe_fund_ntby_vol"),
        ("은행", "bank_ntby_qty"),
        ("보험", "insu_ntby_qty"),
        ("연기금", "fund_ntby_qty"),
        ("기타법인", "etc_corp_ntby_vol"),
    )

    def get_investor_trend_daily(self, stock_code: str, days: int = 20) -> pd.DataFrame:
        """Fetch the daily net-buy quantity per investor type (KIS).

        Returns a DataFrame indexed by date, one column per investor type;
        empty when KIS has no rows (or the lookup degrades).
        """
        base_date = datetime.now().strftime("%Y%m%d")

        try:
            items = self.kis_client.domestic_market_analysis.get_investor_trading_trend_by_stock_daily(
                fid_cond_mrkt_div_code="J",
                fid_input_iscd=stock_code,
                fid_input_date_1=base_date,
            ).body.output2
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"daily investor trend unavailable for {stock_code}: {exc}")
            return pd.DataFrame()

        rows = [
            {
                "date": pd.to_datetime(item.stck_bsop_date),
                **{label: self._safe_float(getattr(item, field)) for label, field in self._INVESTOR_COLUMNS},
            }
            for item in items
        ]
        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows).set_index("date").sort_index()
        return df.tail(days)

    # ──────────────────────────────────────
    # KIS: 투자의견 (stock detail)
    # ──────────────────────────────────────

    def get_investment_opinions(self, stock_code: str, months: int = 6) -> list:
        """증권사 리서치 투자의견 — Kiwoom/DART 에 대응 API 가 없는 KIS 고유 데이터.

        Items carry 의견(invt_opnn)·이전의견·증권사명(mbcr_name)·목표가(hts_goal_prc)·
        괴리율(dprt). Degrades to [] when the name has no coverage.
        """
        end = datetime.now()
        start = end - timedelta(days=months * 30)
        try:
            return (
                self.kis_client.domestic_stock_info.get_investment_opinion(
                    fid_cond_mrkt_div_code="J",
                    fid_cond_scr_div_code="16633",
                    fid_input_iscd=stock_code,
                    fid_input_date_1=start.strftime("%Y%m%d"),
                    fid_input_date_2=end.strftime("%Y%m%d"),
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"investment opinion unavailable for {stock_code}: {exc}")
            return []

    # ──────────────────────────────────────
    # KIS: 종목 수급 추이 (stock detail 수급 탭)
    # ──────────────────────────────────────

    def get_short_selling_trend(self, stock_code: str, days: int = 30) -> list:
        """공매도 일별 추이 (KIS). Items: stck_bsop_date, ssts_cntg_qty(공매도량),
        ssts_vol_rlim(비중), acml_ssts_cntg_qty(누적)."""
        end = datetime.now()
        start = end - timedelta(days=days)
        try:
            return (
                self.kis_client.domestic_market_analysis.get_short_selling_trend_daily(
                    fid_input_date_2=end.strftime("%Y%m%d"),
                    fid_cond_mrkt_div_code="J",
                    fid_input_iscd=stock_code,
                    fid_input_date_1=start.strftime("%Y%m%d"),
                ).body.output2
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"short selling trend unavailable for {stock_code}: {exc}")
            return []

    def get_credit_balance_trend(self, stock_code: str) -> list:
        """신용잔고 일별 추이 (KIS). Items: deal_date, whol_loan_rmnd_stcn(융자잔고),
        whol_loan_rmnd_rate(잔고비율)."""
        try:
            return (
                self.kis_client.domestic_market_analysis.get_credit_balance_trend_daily(
                    fid_cond_mrkt_div_code="J",
                    fid_cond_scr_div_code="20476",
                    fid_input_iscd=stock_code,
                    fid_input_date_1=datetime.now().strftime("%Y%m%d"),
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"credit balance trend unavailable for {stock_code}: {exc}")
            return []

    def get_program_trading_trend(self, stock_code: str) -> list:
        """종목별 프로그램매매 일별 추이 (KIS). Items: stck_bsop_date,
        whol_smtn_ntby_qty(순매수량), whol_smtn_ntby_tr_pbmn(순매수대금)."""
        try:
            return (
                self.kis_client.domestic_market_analysis.get_program_trading_trend_by_stock_daily(
                    fid_cond_mrkt_div_code="J",
                    fid_input_iscd=stock_code,
                    fid_input_date_1="",  # empty = 오늘 기준
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"program trading trend unavailable for {stock_code}: {exc}")
            return []

    # ──────────────────────────────────────
    # KIS: 시장 수급·자금 (market overview)
    # ──────────────────────────────────────

    def get_market_investor_trend_daily(self, market: str = "KSP", days: int = 30) -> list:
        """시장 전체 투자자별 일별 순매수 (KIS). market: KSP(코스피)/KSQ(코스닥).
        Items: stck_bsop_date, bstp_nmix_prpr(지수), prsn/frgn/orgn_ntby_qty."""
        end = datetime.now()
        start = end - timedelta(days=days)
        sector_code = "0001" if market == "KSP" else "1001"
        try:
            return (
                self.kis_client.domestic_market_analysis.get_investor_trading_trend_by_market_daily(
                    fid_cond_mrkt_div_code="U",
                    fid_input_iscd=sector_code,
                    fid_input_date_1=start.strftime("%Y%m%d"),
                    fid_input_iscd_1=market,
                    fid_input_date_2=end.strftime("%Y%m%d"),
                    fid_input_iscd_2=sector_code,
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"market investor trend unavailable for {market}: {exc}")
            return []

    def get_market_fund_summary(self) -> list:
        """시장 자금 동향 (KIS): 고객예탁금·신용융자잔고·펀드 자금 등 일별 시계열."""
        try:
            return (
                self.kis_client.domestic_market_analysis.get_market_fund_summary(
                    fid_input_date_1=datetime.now().strftime("%Y%m%d"),
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"market fund summary unavailable: {exc}")
            return []

    # ──────────────────────────────────────
    # KIS: 랭킹 (screening)
    # ──────────────────────────────────────

    def get_dividend_yield_top(self, market: str = "1") -> list:
        """배당수익률 상위 (KIS). market: 0 전체, 1 코스피, 2 코스피200, 3 코스닥.
        기준일은 최근 1년 결산·현금배당."""
        end = datetime.now()
        start = end - timedelta(days=365)
        try:
            return (
                self.kis_client.domestic_ranking_analysis.get_stock_dividend_yield_top(
                    cts_area="",
                    gb1=market,
                    upjong="0001",  # 종합
                    gb2="0",  # 전체
                    gb3="2",  # 현금배당
                    f_dt=start.strftime("%Y%m%d"),
                    t_dt=end.strftime("%Y%m%d"),
                    gb4="0",  # 전체(결산+중간)
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"dividend yield top unavailable: {exc}")
            return []

    def get_short_selling_top(self, market: str = "0001") -> list:
        """공매도 상위 (KIS, 당일). market: 0000 전체, 0001 코스피, 1001 코스닥."""
        try:
            return (
                self.kis_client.domestic_ranking_analysis.get_stock_short_selling_top(
                    fid_aply_rang_vol="",
                    fid_cond_mrkt_div_code="J",
                    fid_cond_scr_div_code="20482",
                    fid_input_iscd=market,
                    fid_period_div_code="D",
                    fid_input_cnt_1="0",  # 1일
                    fid_trgt_exls_cls_code="",
                    fid_trgt_cls_code="",
                    fid_aply_rang_prc_1="",
                    fid_aply_rang_prc_2="",
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"short selling top unavailable: {exc}")
            return []

    def get_credit_balance_top(self, market: str = "0001") -> list:
        """신용잔고 상위 (KIS, 잔고비율순). market: 0000 전체, 0001 거래소, 1001 코스닥."""
        try:
            return (
                self.kis_client.domestic_ranking_analysis.get_stock_credit_balance_top(
                    fid_cond_scr_div_code="11701",
                    fid_input_iscd=market,
                    fid_option="7",  # 증가율 기간(일)
                    fid_cond_mrkt_div_code="J",
                    fid_rank_sort_cls_code="0",  # 잔고비율상위
                ).body.output2
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"credit balance top unavailable: {exc}")
            return []

    def get_disparity_index_rank(self, market: str = "0001", hour: str = "20") -> list:
        """이격도 상위 (KIS). hour: 이동평균 기준(5/10/20/60/120)."""
        try:
            return (
                self.kis_client.domestic_ranking_analysis.get_stock_disparity_index_rank(
                    fid_input_price_2="",
                    fid_cond_mrkt_div_code="J",
                    fid_cond_scr_div_code="20178",
                    fid_div_cls_code="0",
                    fid_rank_sort_cls_code="0",  # 이격도상위순
                    fid_hour_cls_code=hour,
                    fid_input_iscd=market,
                    fid_trgt_cls_code="0",
                    fid_trgt_exls_cls_code="0",
                    fid_input_price_1="",
                    fid_vol_cnt="",
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"disparity index rank unavailable: {exc}")
            return []

    # ──────────────────────────────────────
    # KIS: ETF (etf analysis)
    # ──────────────────────────────────────

    def get_etf_nav_daily_trend(self, stk_cd: str, days: int = 30) -> list:
        """ETF NAV 대비 일별 추이 (KIS). Items: stck_bsop_date, stck_clpr, nav,
        dprt(괴리율)."""
        end = datetime.now()
        start = end - timedelta(days=days)
        try:
            return (
                self.kis_client.domestic_basic_quote.get_etf_nav_comparison_daily_trend(
                    fid_input_iscd=stk_cd,
                    fid_input_date_1=start.strftime("%Y%m%d"),
                    fid_input_date_2=end.strftime("%Y%m%d"),
                ).body.output
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"etf nav trend unavailable for {stk_cd}: {exc}")
            return []

    def get_etf_component_prices(self, stk_cd: str) -> list:
        """ETF 구성종목 시세 (KIS). Items: stck_shrn_iscd, hts_kor_isnm, stck_prpr,
        prdy_ctrt, etf_cnfg_issu_rlim(구성비중)."""
        try:
            return (
                self.kis_client.domestic_basic_quote.get_etf_component_stock_price(
                    fid_input_iscd=stk_cd,
                ).body.output2
                or []
            )
        except (KISAPIError, ValidationError) as exc:
            logger.debug(f"etf components unavailable for {stk_cd}: {exc}")
            return []

    async def get_stock_data(self, stock_code: str) -> pd.DataFrame:
        parsed_date = datetime.now().strftime("%Y%m%d")
        max_pages = 3
        cont_yn = "N"
        next_key = ""
        rows: List[Dict[str, Any]] = []

        for _ in range(max_pages):
            response = self.kiwoom_client.chart.get_stock_daily(
                stk_cd=stock_code,
                base_dt=parsed_date,
                upd_stkpc_tp="1",
                cont_yn=cont_yn,
                next_key=next_key,
            )

            items = response.body.stk_dt_pole_chart_qry
            if not items:
                break

            rows.extend(
                {
                    "date": pd.to_datetime(item.dt),
                    "open": self._safe_float(item.open_pric),
                    "high": self._safe_float(item.high_pric),
                    "low": self._safe_float(item.low_pric),
                    "close": self._safe_float(item.cur_prc),
                    "volume": self._safe_float(item.trde_qty),
                }
                for item in items
            )

            cont_yn = response.headers.cont_yn
            next_key = response.headers.next_key
            if cont_yn != "Y" or not next_key:
                break

        if rows:
            df = pd.DataFrame(rows)
            df.set_index("date", inplace=True)
            df.sort_index(inplace=True)
            df = df[~df.index.duplicated(keep="last")]
        else:
            df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])

        return df

    # ──────────────────────────────────────
    # Rankings (existing)
    # ──────────────────────────────────────

    def get_top_percentage_change(self, sort_tp: str = "1"):
        return self.kiwoom_client.rank_info.get_top_percentage_change_from_previous_day(
            mrkt_tp="000",
            sort_tp=sort_tp,
            trde_qty_cnd="0000",
            stk_cnd="4",
            crd_cnd="0",
            updown_incls="0",
            pric_cnd="8",
            trde_prica_cnd="10",
            stex_tp="1",
        )

    def get_top_trading_volume(self):
        return self.kiwoom_client.rank_info.get_top_current_day_trading_volume(
            mrkt_tp="000",
            sort_tp="1",
            mang_stk_incls="4",
            crd_tp="0",
            trde_qty_tp="0",
            pric_tp="2",
            trde_prica_tp="10",
            mrkt_open_tp="0",
            stex_tp="1",
        )

    def get_top_transaction_value(self):
        return self.kiwoom_client.rank_info.get_top_transaction_value(
            mrkt_tp="000",
            mang_stk_incls="0",
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Rankings (new)
    # ──────────────────────────────────────

    def get_top_foreigner_period_trading(self, trde_tp: str = "1"):
        return self.kiwoom_client.rank_info.get_top_foreigner_period_trading(
            mrkt_tp="000",
            trde_tp=trde_tp,
            dt="1",
            stex_tp="1",
        )

    def get_new_high_low_price(self, ntl_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_new_high_low_price(
            mrkt_tp="000",
            ntl_tp=ntl_tp,
            high_low_close_tp="1",
            stk_cnd="4",
            trde_qty_tp="0",
            crd_cnd="0",
            updown_incls="0",
            dt="1",
            stex_tp="1",
        )

    def get_price_volatility(self, flu_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_price_volatility(
            mrkt_tp="000",
            flu_tp=flu_tp,
            tm_tp="1",
            tm="60",
            trde_qty_tp="00000",
            stk_cnd="1",
            crd_cnd="0",
            pric_cnd="8",
            updown_incls="0",
            stex_tp="1",
        )

    def get_top_margin_ratio(self):
        return self.kiwoom_client.rank_info.get_top_margin_ratio(
            mrkt_tp="000",
            trde_qty_tp="0",
            stk_cnd="4",
            updown_incls="0",
            crd_cnd="0",
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Sector / Industry
    # ──────────────────────────────────────

    def get_all_industry_index(self, inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_all_industry_index(inds_cd=inds_cd)

    def get_industry_current_price(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_industry_current_price(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
        )

    def get_industry_price_by_sector(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_industry_price_by_sector(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
            stex_tp="1",
        )

    def get_daily_industry_current_price(self, mrkt_tp: str = "0001", inds_cd: str = "001"):
        return self.kiwoom_client.sector.get_daily_industry_current_price(
            mrkt_tp=mrkt_tp,
            inds_cd=inds_cd,
        )

    def get_industry_investor_net_buy(self, mrkt_tp: str = "0001", amt_qty_tp: str = "1"):
        return self.kiwoom_client.sector.get_industry_investor_net_buy(
            mrkt_tp=mrkt_tp,
            amt_qty_tp=amt_qty_tp,
            base_dt=datetime.now().strftime("%Y%m%d"),
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Theme
    # ──────────────────────────────────────

    def get_theme_group(self):
        return self.kiwoom_client.theme.get_theme_group(
            qry_tp="0",
            date_tp="1",
            thema_nm="",
            flu_pl_amt_tp="1",
            stex_tp="1",
        )

    def get_theme_group_stocks(self, thema_grp_cd: str):
        return self.kiwoom_client.theme.get_theme_group_stocks(
            thema_grp_cd=thema_grp_cd,
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # ETF
    # ──────────────────────────────────────

    def get_etf_full_price(self):
        return self.kiwoom_client.etf.get_etf_full_price(
            txon_type="0",
            navpre="0",
            mngmcomp="0",
            txon_yn="0",
            trace_idex="0",
            stex_tp="1",
        )

    def get_etf_return_rate(self, stk_cd: str, etfobjt_idex_cd: str = "0", dt: int = 0):
        return self.kiwoom_client.etf.get_etf_return_rate(
            stk_cd=stk_cd,
            etfobjt_idex_cd=etfobjt_idex_cd,
            dt=dt,
        )

    def get_etf_item_info(self, stk_cd: str):
        return self.kiwoom_client.etf.get_etf_item_info(stk_cd=stk_cd)

    def get_etf_daily_trend(self, stk_cd: str):
        return self.kiwoom_client.etf.get_etf_daily_trend(stk_cd=stk_cd)

    # ──────────────────────────────────────
    # Investor Flow
    # ──────────────────────────────────────

    def get_top_intraday_trading_by_investor(self, trde_tp: str = "1", orgn_tp: str = "1000"):
        return self.kiwoom_client.rank_info.get_top_intraday_trading_by_investor(
            trde_tp=trde_tp,
            mrkt_tp="000",
            orgn_tp=orgn_tp,
        )

    def get_top_50_program_net_buy(self, trde_upper_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_top_50_program_net_buy(
            trde_upper_tp=trde_upper_tp,
            amt_qty_tp="1",
            mrkt_tp="000",
            stex_tp="1",
        )

    def get_program_trading_status_by_stock(self):
        return self.kiwoom_client.stock_info.get_program_trading_status_by_stock(
            dt=datetime.now().strftime("%Y%m%d"),
            mrkt_tp="000",
            stex_tp="1",
        )

    # ──────────────────────────────────────
    # Stock Detail (extended)
    # ──────────────────────────────────────

    def get_institutional_investor_by_stock(self, stk_cd: str, amt_qty_tp: str = "1"):
        return self.kiwoom_client.stock_info.get_institutional_investor_by_stock(
            dt=datetime.now().strftime("%Y%m%d"),
            stk_cd=stk_cd,
            amt_qty_tp=amt_qty_tp,
            trde_tp="0",
            unit_tp="1",
        )

    def get_stock_trading_member(self, stk_cd: str):
        return self.kiwoom_client.stock_info.get_stock_trading_member(stk_cd=stk_cd)

    def get_stock_specific_securities_firm_ranking(self, stk_cd: str):
        today = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        return self.kiwoom_client.rank_info.get_stock_specific_securities_firm_ranking(
            stk_cd=stk_cd,
            strt_dt=start,
            end_dt=today,
            qry_tp="0",
        )

    def get_margin_trading_trend(self, stk_cd: str):
        return self.kiwoom_client.stock_info.get_margin_trading_trend(
            stk_cd=stk_cd,
            dt=datetime.now().strftime("%Y%m%d"),
            qry_tp="0",
        )

    def get_supply_demand_concentration(self):
        return self.kiwoom_client.stock_info.get_supply_demand_concentration(
            mrkt_tp="000",
            prps_cnctr_rt="5",
            cur_prc_entry="0",
            prpscnt="0",
            cycle_tp="0",
            stex_tp="1",
        )
