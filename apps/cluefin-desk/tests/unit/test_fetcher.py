import asyncio
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from cluefin_openapi.kis._exceptions import KISAPIError

from cluefin_desk.data.fetcher import DomesticDataFetcher


def _make_fetcher(monkeypatch, **settings_overrides):
    """Build a fetcher with Kiwoom auth mocked out (no network)."""
    from cluefin_desk.config.settings import settings

    monkeypatch.setattr(settings, "kiwoom_app_key", "kiwoom-key")
    monkeypatch.setattr(settings, "kiwoom_secret_key", "kiwoom-secret")
    for name, value in settings_overrides.items():
        monkeypatch.setattr(settings, name, value)

    with (
        patch("cluefin_desk.data.fetcher.KiwoomAuth") as kiwoom_auth,
        patch("cluefin_desk.data.fetcher.KiwoomClient"),
    ):
        kiwoom_auth.return_value.generate_token.return_value.get_token.return_value = "kiwoom-token"
        return DomesticDataFetcher()


class TestKisClientLazy:
    def test_missing_kis_keys_raises_on_access_not_on_init(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key=None, kis_secret_key=None)
        assert fetcher.has_kis is False
        with pytest.raises(ValueError, match="KIS_APP_KEY"):
            _ = fetcher.kis_client

    def test_missing_kis_secret_raises(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key=None)
        assert fetcher.has_kis is False
        with pytest.raises(ValueError, match="KIS_SECRET_KEY"):
            _ = fetcher.kis_client

    def test_no_kis_auth_at_construction(self, monkeypatch):
        with patch("cluefin_desk.data.fetcher.KisAuth") as kis_auth:
            _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key="kis-secret")
            kis_auth.assert_not_called()

    def test_builds_once_and_caches(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="kis-key", kis_secret_key="kis-secret", kis_env="prod")
        assert fetcher.has_kis is True

        with (
            patch("cluefin_desk.data.fetcher.KisAuth") as kis_auth,
            patch("cluefin_desk.data.fetcher.KisClient") as kis_client_cls,
        ):
            kis_auth.return_value.generate.return_value.get_token.return_value = "kis-token"
            kis_client_cls.return_value = MagicMock()

            first = fetcher.kis_client
            second = fetcher.kis_client

        assert first is second
        kis_auth.assert_called_once()
        kis_auth.return_value.generate.assert_called_once()
        kis_client_cls.assert_called_once()
        assert kis_client_cls.call_args.kwargs["token"] == "kis-token"
        assert kis_client_cls.call_args.kwargs["env"] == "prod"


def _ratio_row(stac_yymm, **overrides):
    defaults = dict(roe_val="10.0", grs="5.0", bsop_prfi_inrt="3.0", ntin_inrt="2.0", lblt_rate="40.0", rsrv_rate="900")
    defaults.update(overrides)
    return SimpleNamespace(stac_yymm=stac_yymm, **defaults)


class TestSplitAnnualAndYtd:
    split = staticmethod(DomesticDataFetcher._split_annual_and_ytd)

    def test_empty(self):
        assert self.split([], "12") == (None, None)

    def test_no_settlement_month_returns_newest_as_annual(self):
        rows = [_ratio_row("202512"), _ratio_row("202606")]
        annual, ytd = self.split(rows, None)
        assert annual.stac_yymm == "202606"
        assert ytd is None

    def test_in_progress_cumulative_row_becomes_ytd(self):
        rows = [_ratio_row("202606"), _ratio_row("202512"), _ratio_row("202412")]
        annual, ytd = self.split(rows, "12")
        assert annual.stac_yymm == "202512"
        assert ytd.stac_yymm == "202606"

    def test_no_ytd_when_newest_is_the_completed_year(self):
        rows = [_ratio_row("202512"), _ratio_row("202412")]
        annual, ytd = self.split(rows, "12")
        assert annual.stac_yymm == "202512"
        assert ytd is None

    def test_unmatched_settlement_month_falls_back_to_newest(self):
        rows = [_ratio_row("202606"), _ratio_row("202603")]
        annual, ytd = self.split(rows, "12")
        assert annual.stac_yymm == "202606"
        assert ytd is None


class TestDescribeState:
    def test_normal(self):
        assert DomesticDataFetcher._describe_state("N", "N") == "정상"

    def test_flags_joined(self):
        assert DomesticDataFetcher._describe_state("Y", "Y") == "관리종목 / 거래정지"

    def test_halt_only(self):
        assert DomesticDataFetcher._describe_state("N", "Y") == "거래정지"


def _kis_price_output(**overrides):
    fields = dict(
        rprs_mrkt_kor_name="KOSPI",
        bstp_kor_isnm="전기·전자",
        stac_month="12",
        stck_prpr="70000",
        prdy_vrss="500",
        prdy_ctrt="0.72",
        hts_avls="4180000",
        per="12.5",
        pbr="1.4",
        eps="5600",
        bps="50000",
        lstn_stcn="5969782550",
        vol_tnrt="0.25",
        hts_frgn_ehrt="52.1",
        whol_loan_rmnd_rate="0.15",
        w52_hgpr="88000",
        w52_hgpr_date="20260115",
        w52_lwpr="49000",
        w52_lwpr_date="20250901",
    )
    fields.update(overrides)
    return SimpleNamespace(**fields)


def _kis_product_output(**overrides):
    fields = dict(
        prdt_abrv_name="삼성전자",
        prdt_name="삼성전자보통주",
        scts_mket_lstg_dt="19750611",
        kosdaq_mket_lstg_dt="",
        idx_bztp_mcls_cd_name="전기전자",
        idx_bztp_scls_cd_name="반도체",
        admn_item_yn="N",
        tr_stop_yn="N",
    )
    fields.update(overrides)
    return SimpleNamespace(**fields)


def _install_kis_mock(fetcher, price=None, product=None, ratios=None, statements=None):
    """Inject a fake KIS client so no property-triggered auth happens."""
    kis = MagicMock()
    kis.domestic_basic_quote.get_stock_current_price.return_value.body.output = price
    kis.domestic_stock_info.get_stock_basic_info.return_value.body.output = product
    kis.domestic_stock_info.get_financial_ratio.return_value.body.output = ratios or []
    kis.domestic_stock_info.get_income_statement.return_value.body.output = statements or []
    fetcher._kis_client = kis
    return kis


class TestBasicDataDispatch:
    def test_without_kis_uses_kiwoom(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key=None, kis_secret_key=None)
        info = MagicMock()
        info.body = SimpleNamespace(
            stk_cd="005930", stk_nm="삼성전자", mac="4180000", per="12.5", eps="5600", roe="9.1", pbr="1.4", bps="50000"
        )
        info_v1 = MagicMock()
        info_v1.body = SimpleNamespace(upName="전기전자", marketName="KOSPI")
        fetcher.kiwoom_client = MagicMock()
        fetcher.kiwoom_client.stock_info.get_stock_info.return_value = info
        fetcher.kiwoom_client.stock_info.get_stock_info_v1.return_value = info_v1

        df = asyncio.run(fetcher.get_basic_data("005930"))

        row = df.iloc[0]
        assert row["stock_name"] == "삼성전자"
        assert row["market_name"] == "KOSPI"
        assert "current_price" not in df.columns

    def test_with_kis_uses_kis_and_keeps_widget_keys(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        fetcher.kiwoom_client = MagicMock()
        statement = SimpleNamespace(
            stac_yymm="202512", sale_account="3000000", sale_totl_prfi="", bsop_prti="350000", thtr_ntin="300000"
        )
        _install_kis_mock(
            fetcher,
            price=_kis_price_output(),
            product=_kis_product_output(),
            ratios=[_ratio_row("202512"), _ratio_row("202606", roe_val="4.0")],
            statements=[statement],
        )

        df = asyncio.run(fetcher.get_basic_data("005930"))

        row = df.iloc[0]
        # widget-facing keys shared with the Kiwoom shape
        for key in ("stock_name", "market_name", "sector_name", "market_cap", "per", "pbr", "roe", "eps", "bps"):
            assert key in df.columns, key
        assert row["stock_name"] == "삼성전자"
        # annual (202512), not the in-progress cumulative row (202606)
        assert row["roe"] == "10.0"
        assert row["financial_period"] == "202512"
        assert row["ytd_period"] == "202606"
        assert row["revenue"] == "3000000"
        assert row["state"] == "정상"
        fetcher.kiwoom_client.stock_info.get_stock_info.assert_not_called()

    def test_kis_financial_failure_degrades_to_no_financial_columns(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        kis = _install_kis_mock(fetcher, price=_kis_price_output(), product=_kis_product_output())
        kis.domestic_stock_info.get_financial_ratio.side_effect = KISAPIError("no data")
        kis.domestic_stock_info.get_income_statement.side_effect = KISAPIError("no data")

        df = asyncio.run(fetcher.get_basic_data("069500"))

        assert df.iloc[0]["stock_name"] == "삼성전자"
        assert "roe" not in df.columns
        assert "revenue" not in df.columns


class TestInvestorTrendDaily:
    def _item(self, date, qty):
        fields = {field: str(qty) for _, field in DomesticDataFetcher._INVESTOR_COLUMNS}
        return SimpleNamespace(stck_bsop_date=date, **fields)

    def test_rows_sorted_and_tailed(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        kis = _install_kis_mock(fetcher)
        kis.domestic_market_analysis.get_investor_trading_trend_by_stock_daily.return_value.body.output2 = [
            self._item("20260828", 300),
            self._item("20260826", 100),
            self._item("20260827", 200),
        ]

        df = fetcher.get_investor_trend_daily("005930", days=2)

        assert len(df) == 2
        assert list(df.index) == [pd.Timestamp("2026-08-27"), pd.Timestamp("2026-08-28")]
        assert df.iloc[-1]["개인"] == 300.0
        assert "연기금" in df.columns

    def test_degrades_to_empty(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        kis = _install_kis_mock(fetcher)
        kis.domestic_market_analysis.get_investor_trading_trend_by_stock_daily.side_effect = KISAPIError("boom")

        assert fetcher.get_investor_trend_daily("005930").empty


class TestKisPhase2Wrappers:
    """Param mapping + degrade behavior for the Phase-2 KIS wrappers."""

    def _fetcher(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        return fetcher, _install_kis_mock(fetcher)

    def test_investment_opinions_params_and_degrade(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_stock_info.get_investment_opinion.return_value.body.output = [SimpleNamespace(invt_opnn="매수")]

        rows = fetcher.get_investment_opinions("005930")

        assert rows[0].invt_opnn == "매수"
        kwargs = kis.domestic_stock_info.get_investment_opinion.call_args.kwargs
        assert kwargs["fid_input_iscd"] == "005930"
        assert kwargs["fid_cond_scr_div_code"] == "16633"
        assert kwargs["fid_input_date_1"] < kwargs["fid_input_date_2"]

        kis.domestic_stock_info.get_investment_opinion.side_effect = KISAPIError("none")
        assert fetcher.get_investment_opinions("005930") == []

    def test_stock_news_filters_by_code_and_degrades(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        api = kis.domestic_issue_other.get_market_announcement_schedule
        api.return_value.body.output = [SimpleNamespace(hts_pbnt_titl_cntt="삼성전자, 신규 공장")]

        rows = fetcher.get_stock_news("005930")

        assert rows[0].hts_pbnt_titl_cntt == "삼성전자, 신규 공장"
        kwargs = api.call_args.kwargs
        assert kwargs["fid_input_iscd"] == "005930"
        # 문서상 "공백 필수" 인 파라미터들 — 값을 넣으면 빈 응답이 온다
        for key in ("fid_news_ofer_entp_code", "fid_cond_mrkt_cls_code", "fid_titl_cntt", "fid_rank_sort_cls_code"):
            assert kwargs[key] == ""

        api.side_effect = KISAPIError("none")
        assert fetcher.get_stock_news("005930") == []

    def test_stock_supply_trends_degrade_to_empty(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_market_analysis.get_short_selling_trend_daily.side_effect = KISAPIError("x")
        kis.domestic_market_analysis.get_credit_balance_trend_daily.side_effect = KISAPIError("x")
        kis.domestic_market_analysis.get_program_trading_trend_by_stock_daily.side_effect = KISAPIError("x")

        assert fetcher.get_short_selling_trend("005930") == []
        assert fetcher.get_credit_balance_trend("005930") == []
        assert fetcher.get_program_trading_trend("005930") == []

    def test_market_investor_trend_maps_market_to_sector_code(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_market_analysis.get_investor_trading_trend_by_market_daily.return_value.body.output = []

        fetcher.get_market_investor_trend_daily(market="KSQ")
        kwargs = kis.domestic_market_analysis.get_investor_trading_trend_by_market_daily.call_args.kwargs
        assert kwargs["fid_input_iscd"] == "1001"
        assert kwargs["fid_input_iscd_1"] == "KSQ"

        fetcher.get_market_investor_trend_daily(market="KSP")
        kwargs = kis.domestic_market_analysis.get_investor_trading_trend_by_market_daily.call_args.kwargs
        assert kwargs["fid_input_iscd"] == "0001"

    def test_dividend_yield_top_uses_one_year_window(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_ranking_analysis.get_stock_dividend_yield_top.return_value.body.output = []

        fetcher.get_dividend_yield_top()
        kwargs = kis.domestic_ranking_analysis.get_stock_dividend_yield_top.call_args.kwargs
        assert kwargs["gb3"] == "2"  # 현금배당
        assert kwargs["f_dt"] < kwargs["t_dt"]

    def test_credit_balance_top_reads_output2(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_ranking_analysis.get_stock_credit_balance_top.return_value.body.output2 = [
            SimpleNamespace(hts_kor_isnm="삼성전자")
        ]
        assert fetcher.get_credit_balance_top()[0].hts_kor_isnm == "삼성전자"

    def test_etf_nav_trend_and_components(self, monkeypatch):
        fetcher, kis = self._fetcher(monkeypatch)
        kis.domestic_basic_quote.get_etf_nav_comparison_daily_trend.return_value.body.output = [
            SimpleNamespace(dprt="0.05")
        ]
        kis.domestic_basic_quote.get_etf_component_stock_price.return_value.body.output2 = [
            SimpleNamespace(hts_kor_isnm="삼성전자")
        ]

        assert fetcher.get_etf_nav_daily_trend("069500")[0].dprt == "0.05"
        assert fetcher.get_etf_component_prices("069500")[0].hts_kor_isnm == "삼성전자"

        kis.domestic_basic_quote.get_etf_nav_comparison_daily_trend.side_effect = KISAPIError("x")
        assert fetcher.get_etf_nav_daily_trend("069500") == []


class TestCorporateActions:
    def _bar(self, date, code, ratio="0.00"):
        return SimpleNamespace(stck_bsop_date=date, flng_cls_code=code, prtt_rate=ratio)

    def test_filters_non_events_and_maps_labels(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        kis = _install_kis_mock(fetcher)
        kis.domestic_basic_quote.get_stock_period_quote.return_value.body.output2 = [
            self._bar("20260827", "00"),
            self._bar("20260626", "02"),
            self._bar("20260625", ""),
        ]

        df = fetcher.get_corporate_actions("005930")

        assert len(df) == 1
        assert df.iloc[0]["event"] == "배당락"

    def test_no_events_returns_empty(self, monkeypatch):
        fetcher = _make_fetcher(monkeypatch, kis_app_key="k", kis_secret_key="s")
        kis = _install_kis_mock(fetcher)
        kis.domestic_basic_quote.get_stock_period_quote.return_value.body.output2 = [self._bar("20260827", "00")]

        assert fetcher.get_corporate_actions("005930").empty
