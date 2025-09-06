"""Tests for display formatter functionality."""

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from cluefin_cli.commands.inquiry.config_models import APIConfig
from cluefin_cli.commands.inquiry.display_formatter import (
    DisplayFormatter,
    RankingDataFormatter,
    SectorDataFormatter,
    StockDataFormatter,
)


class TestDisplayFormatter:
    """Test cases for base DisplayFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = DisplayFormatter()

    def test_calculate_text_width_ascii(self):
        """Test text width calculation for ASCII characters."""
        text = "Hello World"
        width = self.formatter.calculate_text_width(text)
        assert width == 11

    def test_calculate_text_width_korean(self):
        """Test text width calculation for Korean characters."""
        text = "안녕하세요"  # 5 Korean characters
        width = self.formatter.calculate_text_width(text)
        assert width == 10  # Each Korean char is 2 units wide

    def test_calculate_text_width_mixed(self):
        """Test text width calculation for mixed ASCII and Korean."""
        text = "Hello 안녕"  # 5 ASCII + 1 space + 2 Korean
        width = self.formatter.calculate_text_width(text)
        assert width == 10  # 6 ASCII + 4 Korean

    def test_pad_korean_text_left(self):
        """Test left padding with Korean text."""
        text = "안녕"  # Width 4
        padded = self.formatter.pad_korean_text(text, 8, "left")
        assert padded == "안녕    "
        assert self.formatter.calculate_text_width(padded) == 8

    def test_pad_korean_text_right(self):
        """Test right padding with Korean text."""
        text = "안녕"  # Width 4
        padded = self.formatter.pad_korean_text(text, 8, "right")
        assert padded == "    안녕"
        assert self.formatter.calculate_text_width(padded) == 8

    def test_pad_korean_text_center(self):
        """Test center padding with Korean text."""
        text = "안녕"  # Width 4
        padded = self.formatter.pad_korean_text(text, 8, "center")
        assert padded == "  안녕  "
        assert self.formatter.calculate_text_width(padded) == 8

    def test_format_number_price(self):
        """Test price number formatting."""
        assert self.formatter.format_number(1234567, "price") == "1,234,567"
        assert self.formatter.format_number(1234.56, "price") == "1,234.56"
        assert self.formatter.format_number("1234567", "price") == "1,234,567"

    def test_format_number_volume(self):
        """Test volume number formatting with Korean units."""
        assert self.formatter.format_number(150000000, "volume") == "1.5억"
        assert self.formatter.format_number(50000, "volume") == "5.0만"
        assert self.formatter.format_number(5000, "volume") == "5,000"

    def test_format_number_percentage(self):
        """Test percentage formatting."""
        assert self.formatter.format_number(1.23, "percentage") == "+1.23%"
        assert self.formatter.format_number(-2.45, "percentage") == "-2.45%"
        assert self.formatter.format_number(0, "percentage") == "0.00%"

    def test_format_number_decimal(self):
        """Test formatting with Decimal type."""
        decimal_val = Decimal("1234.56")
        assert self.formatter.format_number(decimal_val, "price") == "1,234.56"

    def test_format_number_none_empty(self):
        """Test formatting None and empty values."""
        assert self.formatter.format_number(None) == "-"
        assert self.formatter.format_number("") == "-"

    def test_get_color_for_value_positive(self):
        """Test color selection for positive values."""
        assert self.formatter.get_color_for_value(1.23) == "bright_red"
        assert self.formatter.get_color_for_value("+1.23%") == "bright_red"

    def test_get_color_for_value_negative(self):
        """Test color selection for negative values."""
        assert self.formatter.get_color_for_value(-1.23) == "bright_blue"
        assert self.formatter.get_color_for_value("-1.23%") == "bright_blue"

    def test_get_color_for_value_neutral(self):
        """Test color selection for neutral values."""
        assert self.formatter.get_color_for_value(0) == "white"
        assert self.formatter.get_color_for_value("invalid") == "white"

    @patch("cluefin_cli.commands.inquiry.display_formatter.Console")
    def test_create_table(self, mock_console):
        """Test table creation."""
        headers = ["컬럼1", "컬럼2", "컬럼3"]
        rows = [["데이터1", "+1.23%", "1,000"], ["데이터2", "-2.45%", "2,000"]]

        table = self.formatter.create_table(headers, rows, "테스트 테이블")

        # Verify table was created (we can't easily test Rich Table internals)
        assert table is not None

    @patch("cluefin_cli.commands.inquiry.display_formatter.Console")
    def test_display_methods(self, mock_console):
        """Test display methods don't raise exceptions."""
        # These methods primarily interact with Rich console
        # We test they don't raise exceptions
        self.formatter.display_error("테스트 오류")
        self.formatter.display_success("테스트 성공")
        self.formatter.display_info("테스트 정보")
        self.formatter.display_loading("로딩 중...")
        self.formatter.clear_screen()
        self.formatter.print_separator()


class TestRankingDataFormatter:
    """Test cases for RankingDataFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = RankingDataFormatter()

    def test_format_ranking_data_no_data(self):
        """Test handling of empty data."""
        with patch.object(self.formatter, "display_error") as mock_error:
            self.formatter.format_ranking_data(None, "테스트 API")
            mock_error.assert_called_once()

    def test_format_ranking_data_empty_output(self):
        """Test handling of empty output."""
        mock_data = Mock()
        mock_data.output = []

        mock_api_config = APIConfig(
            name="test_api", korean_name="테스트 API", api_method="test_method", description="mocking api"
        )

        with patch.object(self.formatter, "display_error") as mock_error:
            self.formatter.format_ranking_data(mock_data, mock_api_config)
            mock_error.assert_called_once()

    def test_format_volume_ranking_data(self):
        """Test volume ranking data formatting."""
        # Create mock data
        mock_item = Mock()
        mock_item.hts_kor_isnm = "삼성전자"
        mock_item.mksc_shrn_iscd = "005930"
        mock_item.stck_prpr = "75000"
        mock_item.prdy_ctrt = "1.23"
        mock_item.acml_vol = "1000000"
        mock_item.acml_tr_pbmn = "75000000000"

        mock_data = Mock()
        mock_data.tdy_trde_qty_upper = [mock_item]

        mock_api_config = APIConfig(
            name="current_day_trading_volume_top",
            korean_name="거래량 상위 요청",
            api_method="test_method",
            description="test api",
        )

        with patch.object(self.formatter, "display_table") as mock_display:
            self.formatter.format_ranking_data(mock_data, mock_api_config)
            mock_display.assert_called_once()

            # Check that the call was made with proper headers
            args, kwargs = mock_display.call_args
            headers, rows, title = args
            assert "순위" in headers
            assert "종목명" in headers
            assert "거래량" in headers


class TestSectorDataFormatter:
    """Test cases for SectorDataFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = SectorDataFormatter()

    def test_format_sector_data_no_data(self):
        """Test handling of empty sector data."""
        with patch.object(self.formatter, "display_error") as mock_error:
            self.formatter.format_sector_data(None, "테스트 API")
            mock_error.assert_called_once()

    def test_format_investor_sector_data(self):
        """Test investor sector data formatting."""
        mock_item = Mock()
        mock_item.inds_nm = "반도체"
        mock_item.cur_prc = "1000"
        mock_item.flu_rt = "2.15"
        mock_item.trde_qty = "5000000"
        mock_item.ind_netprps = "1000000000"
        mock_item.frgnr_netprps = "-500000000"
        mock_item.orgn_netprps = "200000000"

        # Create proper mock data structure
        mock_body = Mock()
        mock_body.inds_netprps = [mock_item]
        mock_data = Mock()
        mock_data.body = mock_body

        mock_api_config = APIConfig(
            name="industry_investor_net_buy",
            korean_name="업종별 투자자 순매수 요청",
            api_method="test_method",
        )

        with patch.object(self.formatter, "display_table") as mock_display:
            self.formatter.format_sector_data(mock_data, mock_api_config)
            mock_display.assert_called_once()

            args, kwargs = mock_display.call_args
            headers, rows, title = args
            assert "업종명" in headers
            assert "개인순매수" in headers
            assert "외국인순매수" in headers

    def test_format_index_data(self):
        """Test sector index data formatting."""
        mock_item = Mock()
        mock_item.stk_cd = "001"
        mock_item.stk_nm = "IT"
        mock_item.cur_prc = "1500.25"
        mock_item.pre_sig = "+"
        mock_item.pred_pre = "15.30"
        mock_item.flu_rt = "1.03"
        mock_item.trde_qty = "50000000"
        mock_item.wght = "10.5"
        mock_item.trde_prica = "2000000000"

        # Create proper mock data structure
        mock_body = Mock()
        mock_body.all_inds_index = [mock_item]
        mock_data = Mock()
        mock_data.body = mock_body

        mock_api_config = APIConfig(
            name="all_industry_index",
            korean_name="전업종 지수요청",
            api_method="test_method",
        )

        with patch.object(self.formatter, "display_table") as mock_display:
            self.formatter.format_sector_data(mock_data, mock_api_config)
            mock_display.assert_called_once()


class TestStockDataFormatter:
    """Test cases for StockDataFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = StockDataFormatter()

    def test_format_stock_data_no_data(self):
        """Test handling of empty stock data."""
        with patch.object(self.formatter, "display_error") as mock_error:
            self.formatter.format_stock_data(None, "테스트 API")
            mock_error.assert_called_once()

    def test_format_volume_renewal_data(self):
        """Test volume renewal data formatting."""
        mock_item = Mock()
        mock_item.stck_cntg_hour = "14:30:00"
        mock_item.stck_prpr = "75000"
        mock_item.prdy_vrss = "1000"
        mock_item.prdy_ctrt = "1.35"
        mock_item.cntg_vol = "10000"
        mock_item.acml_vol = "500000"

        # Create proper mock data structure
        mock_body = Mock()
        mock_body.trde_qty_updt = [mock_item]
        mock_data = Mock()
        mock_data.body = mock_body

        mock_api_config = APIConfig(
            name="trading_volume_renewal",
            korean_name="거래량갱신요청",
            api_method="test_method",
            description="test api",
        )

        with patch.object(self.formatter, "display_table") as mock_display:
            self.formatter.format_stock_data(mock_data, mock_api_config)
            mock_display.assert_called_once()

            args, kwargs = mock_display.call_args
            headers, rows, title = args
            assert "종목코드" in headers
            assert "현재가" in headers
            assert "현재거래량" in headers

    def test_format_broker_analysis_data(self):
        """Test broker analysis data formatting."""
        mock_item = Mock()
        mock_item.dt = "20231201"
        mock_item.close_pric = "75000"
        mock_item.pred_pre = "1000"
        mock_item.sel_qty = "10000"
        mock_item.buy_qty = "15000"
        mock_item.netprps_qty = "5000"
        mock_item.trde_qty_sum = "25000"
        mock_item.trde_wght = "5.2"

        # Create proper mock data structure
        mock_body = Mock()
        mock_body.trde_ori_prps_anly = [mock_item]
        mock_data = Mock()
        mock_data.body = mock_body

        mock_api_config = APIConfig(
            name="trading_member_supply_demand_analysis", 
            korean_name="거래원매물대분석요청", 
            api_method="test_method"
        )

        with patch.object(self.formatter, "display_table") as mock_display:
            self.formatter.format_stock_data(mock_data, mock_api_config)
            mock_display.assert_called_once()

            args, kwargs = mock_display.call_args
            headers, rows, title = args
            assert "일자" in headers
            assert "매도량" in headers
            assert "매수량" in headers


if __name__ == "__main__":
    pytest.main([__file__])
