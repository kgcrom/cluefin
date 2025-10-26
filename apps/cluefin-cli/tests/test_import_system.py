"""Unit tests for import system."""

import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest

from cluefin_cli.data.duckdb_manager import DuckDBManager
from cluefin_cli.data.importer import StockChartImporter
from cluefin_cli.data.stock_fetcher import StockListFetcher


@pytest.fixture
def temp_db():
    """Create temporary DuckDB for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".duckdb") as f:
        db_path = f.name

    yield db_path

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def db_manager(temp_db):
    """Create DuckDB manager instance."""
    manager = DuckDBManager(db_path=temp_db)
    yield manager
    manager.close()


@pytest.fixture
def mock_client():
    """Create mock Kiwoom client."""
    client = MagicMock()
    client.token = "test_token"
    return client


class TestDuckDBManager:
    """Test DuckDBManager class."""

    def test_create_tables(self, db_manager):
        """Test table creation."""
        # Verify tables exist by attempting to query
        result = db_manager.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [r[0] for r in result]

        assert "daily_chart" in table_names
        assert "weekly_chart" in table_names
        assert "monthly_chart" in table_names
        assert "stock_metadata" in table_names

    def test_insert_daily_chart(self, db_manager):
        """Test inserting daily chart data."""
        # Create sample data
        df = pd.DataFrame(
            {
                "dt": ["20231201", "20231202"],
                "cur_prc": ["50000", "51000"],
                "open_pric": ["49000", "50500"],
                "high_pric": ["51000", "51500"],
                "low_pric": ["48000", "50000"],
                "trde_qty": ["1000000", "1100000"],
            }
        )

        # Insert data
        count = db_manager.insert_daily_chart("005930", df)

        assert count == 2

        # Verify data exists
        result = db_manager.connection.execute(
            "SELECT COUNT(*) as count FROM daily_chart WHERE stock_code = '005930'"
        ).fetchall()
        assert result[0][0] == 2

    def test_insert_weekly_chart(self, db_manager):
        """Test inserting weekly chart data."""
        df = pd.DataFrame(
            {
                "dt": ["20231201", "20231208"],
                "cur_prc": ["50000", "51000"],
                "open_pric": ["49000", "50500"],
                "high_pric": ["51000", "51500"],
                "low_pric": ["48000", "50000"],
                "trde_qty": ["5000000", "5100000"],
                "trde_prica": ["250000000000", "260000000000"],
            }
        )

        count = db_manager.insert_weekly_chart("005930", df)
        assert count == 2

    def test_insert_monthly_chart(self, db_manager):
        """Test inserting monthly chart data."""
        df = pd.DataFrame(
            {
                "dt": ["20231101", "20231201"],
                "cur_prc": ["50000", "51000"],
                "open_pric": ["49000", "50500"],
                "high_pric": ["51000", "51500"],
                "low_pric": ["48000", "50000"],
                "trde_qty": ["20000000", "22000000"],
                "trde_prica": ["1000000000000", "1100000000000"],
            }
        )

        count = db_manager.insert_monthly_chart("005930", df)
        assert count == 2

    def test_update_stock_metadata(self, db_manager):
        """Test updating stock metadata."""
        db_manager.update_stock_metadata("005930", stock_name="Samsung", import_frequency="daily")

        result = db_manager.connection.execute(
            "SELECT stock_name, import_frequency FROM stock_metadata WHERE stock_code = '005930'"
        ).fetchall()

        assert len(result) == 1
        assert result[0][0] == "Samsung"
        assert result[0][1] == "daily"

    def test_get_database_stats(self, db_manager):
        """Test getting database statistics."""
        # Insert some data
        df = pd.DataFrame(
            {
                "dt": ["20231201"],
                "cur_prc": ["50000"],
                "open_pric": ["49000"],
                "high_pric": ["51000"],
                "low_pric": ["48000"],
                "trde_qty": ["1000000"],
            }
        )
        db_manager.insert_daily_chart("005930", df)

        stats = db_manager.get_database_stats()

        assert stats["daily_chart_count"] == 1
        assert stats["daily_chart_stocks"] == 1
        assert "database_size_mb" in stats

    def test_get_imported_stocks(self, db_manager):
        """Test getting list of imported stocks."""
        df = pd.DataFrame(
            {
                "dt": ["20231201"],
                "cur_prc": ["50000"],
                "open_pric": ["49000"],
                "high_pric": ["51000"],
                "low_pric": ["48000"],
                "trde_qty": ["1000000"],
            }
        )
        db_manager.insert_daily_chart("005930", df)
        db_manager.insert_daily_chart("035720", df)

        stocks = db_manager.get_imported_stocks()

        assert len(stocks) == 2
        assert "005930" in stocks
        assert "035720" in stocks

    def test_check_data_exists(self, db_manager):
        """Test checking if data exists."""
        # Insert data
        df = pd.DataFrame(
            {
                "dt": ["20231201", "20231202", "20231203"],
                "cur_prc": ["50000", "51000", "52000"],
                "open_pric": ["49000", "50500", "51500"],
                "high_pric": ["51000", "51500", "52500"],
                "low_pric": ["48000", "50000", "50500"],
                "trde_qty": ["1000000", "1100000", "1000500"],
            }
        )
        db_manager.insert_daily_chart("005930", df)

        # Check if data exists
        exists = db_manager.check_data_exists("005930", "daily_chart", "20231201", "20231203")
        assert exists is True

        # Check for range with no data
        exists = db_manager.check_data_exists("005930", "daily_chart", "20240101", "20240131")
        assert exists is False

    def test_empty_dataframe_insert(self, db_manager):
        """Test inserting empty DataFrame."""
        df = pd.DataFrame()
        count = db_manager.insert_daily_chart("005930", df)
        assert count == 0


class TestStockListFetcher:
    """Test StockListFetcher class."""

    def test_validate_stock_code_valid(self, mock_client):
        """Test validating valid stock code."""
        fetcher = StockListFetcher(mock_client)

        # Mock successful API call
        mock_client.stock_info.get_stock_info_v1 = MagicMock()

        result = fetcher.validate_stock_code("005930")
        assert result is True

    def test_validate_stock_code_invalid_format(self, mock_client):
        """Test validating invalid stock code format."""
        fetcher = StockListFetcher(mock_client)

        assert fetcher.validate_stock_code("ABC") is False
        assert fetcher.validate_stock_code("") is False
        assert fetcher.validate_stock_code("12345") is False  # Too short
        assert fetcher.validate_stock_code("1234567") is False  # Too long

    def test_parse_stocks_from_response(self, mock_client):
        """Test parsing stock codes from API response."""
        fetcher = StockListFetcher(mock_client)

        # Create mock response
        mock_item1 = MagicMock()
        mock_item1.stock_code = "005930"

        mock_item2 = MagicMock()
        mock_item2.stock_code = "035720"

        mock_body = MagicMock()
        mock_body.stocks = [mock_item1, mock_item2]

        mock_response = MagicMock()
        mock_response.body = mock_body

        stocks = fetcher._parse_stocks_from_response(mock_response)

        assert len(stocks) == 2
        assert "005930" in stocks
        assert "035720" in stocks


class TestStockChartImporter:
    """Test StockChartImporter class."""

    def test_import_stock_data_daily(self, mock_client, db_manager):
        """Test importing daily chart data."""
        importer = StockChartImporter(mock_client, db_manager)

        # Create mock response
        mock_item1 = MagicMock()
        mock_item1.dt = "20231201"
        mock_item1.cur_prc = "50000"
        mock_item1.open_pric = "49000"
        mock_item1.high_pric = "51000"
        mock_item1.low_pric = "48000"
        mock_item1.trde_qty = "1000000"

        mock_body = MagicMock()
        mock_body.stk_dt_pole_chart_qry = [mock_item1]

        mock_response = MagicMock()
        mock_response.body = mock_body

        mock_client.chart.get_stock_daily = MagicMock(return_value=mock_response)

        # Import data
        results = importer.import_stock_data(
            "005930", "20231101", "20231231", ["daily"], skip_existing=False
        )

        assert results["daily"] > 0

    def test_validate_date_format(self, mock_client, db_manager):
        """Test date format validation."""
        importer = StockChartImporter(mock_client, db_manager)

        assert importer._validate_date_format("20231201") is True
        assert importer._validate_date_format("2023-12-01") is False
        assert importer._validate_date_format("20231") is False
        assert importer._validate_date_format("") is False

    def test_get_default_date_range(self, mock_client, db_manager):
        """Test getting default date range."""
        start, end = StockChartImporter.get_default_date_range(days_back=365)

        # Verify format
        assert len(start) == 8
        assert len(end) == 8

        # Verify dates are valid
        start_date = datetime.strptime(start, "%Y%m%d")
        end_date = datetime.strptime(end, "%Y%m%d")

        # Verify end date is after start date
        assert end_date > start_date

        # Verify roughly 1 year difference
        delta = (end_date - start_date).days
        assert 360 <= delta <= 370

    def test_filter_date_range(self, mock_client, db_manager):
        """Test date range filtering."""
        importer = StockChartImporter(mock_client, db_manager)

        df = pd.DataFrame(
            {
                "dt": [
                    "20231101",
                    "20231115",
                    "20231201",
                    "20231215",
                    "20240101",
                ],
                "cur_prc": ["50000", "51000", "52000", "53000", "54000"],
            }
        )

        filtered = importer._filter_date_range(df, "20231115", "20231215")

        assert len(filtered) == 2
        assert filtered.iloc[0]["dt"] == "20231115"
        assert filtered.iloc[1]["dt"] == "20231215"

    def test_import_batch(self, mock_client, db_manager):
        """Test batch import."""
        importer = StockChartImporter(mock_client, db_manager)

        # Create mock response
        mock_body = MagicMock()
        mock_body.stk_dt_pole_chart_qry = []

        mock_response = MagicMock()
        mock_response.body = mock_body

        mock_client.chart.get_stock_daily = MagicMock(return_value=mock_response)

        # Import multiple stocks
        results = importer.import_batch(
            ["005930", "035720"],
            "20231101",
            "20231231",
            ["daily"],
            skip_existing=False,
        )

        assert len(results) == 2
        assert "005930" in results
        assert "035720" in results

    def test_item_to_dict_with_dict(self, mock_client, db_manager):
        """Test converting dict item to dictionary."""
        importer = StockChartImporter(mock_client, db_manager)

        item = {"cur_prc": "50000", "dt": "20231201"}
        result = importer._item_to_dict(item)

        assert result["cur_prc"] == "50000"
        assert result["dt"] == "20231201"

    def test_item_to_dict_with_object(self, mock_client, db_manager):
        """Test converting object item to dictionary."""
        importer = StockChartImporter(mock_client, db_manager)

        item = MagicMock()
        item.cur_prc = "50000"
        item.dt = "20231201"

        result = importer._item_to_dict(item)

        assert "cur_prc" in result or "dt" in result


class TestImportIntegration:
    """Integration tests for import system."""

    def test_full_import_workflow(self, mock_client, db_manager):
        """Test complete import workflow."""
        importer = StockChartImporter(mock_client, db_manager)

        # Create sample data
        df = pd.DataFrame(
            {
                "dt": ["20231201", "20231202"],
                "cur_prc": ["50000", "51000"],
                "open_pric": ["49000", "50500"],
                "high_pric": ["51000", "51500"],
                "low_pric": ["48000", "50000"],
                "trde_qty": ["1000000", "1100000"],
            }
        )

        # Mock API responses
        mock_daily_body = MagicMock()
        mock_daily_body.stk_dt_pole_chart_qry = []

        mock_daily_response = MagicMock()
        mock_daily_response.body = mock_daily_body

        mock_client.chart.get_stock_daily = MagicMock(return_value=mock_daily_response)

        # Test database stats before import
        stats_before = db_manager.get_database_stats()
        assert stats_before["daily_chart_count"] == 0

        # Manually insert test data
        db_manager.insert_daily_chart("005930", df)

        # Test database stats after import
        stats_after = db_manager.get_database_stats()
        assert stats_after["daily_chart_count"] == 2
        assert stats_after["daily_chart_stocks"] == 1

        # Test metadata update
        db_manager.update_stock_metadata("005930", stock_name="Samsung", import_frequency="daily")
        metadata = db_manager.connection.execute(
            "SELECT stock_name FROM stock_metadata WHERE stock_code = '005930'"
        ).fetchall()
        assert metadata[0][0] == "Samsung"
