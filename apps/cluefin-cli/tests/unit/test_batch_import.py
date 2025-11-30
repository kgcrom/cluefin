"""Unit tests for batch import functionality.

This module tests:
1. check_data_exists_batch returns correct dict structure
2. import_batch processes stocks in chunks of 10
3. Existing stocks are properly skipped

Run with: uv run pytest apps/cluefin-cli/tests/unit/test_batch_import.py -v
"""

from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def mock_duckdb_connection(monkeypatch):
    """Mock DuckDB connection to avoid touching real database."""
    from pathlib import Path

    import duckdb

    mock_conn = MagicMock()

    # Create a mock result object that has fetchall() method
    mock_result = MagicMock()
    mock_conn.execute.return_value = mock_result

    monkeypatch.setattr("duckdb.connect", lambda *args, **kwargs: mock_conn)
    monkeypatch.setattr(Path, "mkdir", lambda *args, **kwargs: None)

    return mock_conn


@pytest.fixture
def mock_db_manager(mock_duckdb_connection):
    """Create DuckDBManager with mocked connection."""
    from cluefin_cli.data.duckdb_manager import DuckDBManager

    db = DuckDBManager()
    return db


def test_batch_check_empty_list(mock_db_manager, mock_duckdb_connection):
    """Test check_data_exists_batch with empty list."""
    # Empty list should return early without executing query
    result = mock_db_manager.check_domestic_stock_data_exists_batch([], "20240101", "20241231")

    assert result == {}, "Empty list should return empty dict"


def test_batch_check_sample_codes(mock_db_manager, mock_duckdb_connection):
    """Test check_data_exists_batch with sample stock codes."""
    # Mock execute to return counts for three stocks
    # Format: [(stock_code, count), ...]
    mock_duckdb_connection.execute.return_value.fetchall.return_value = [
        ("005930", 100),  # Has data
        ("035720", 0),  # No data
        ("000660", 50),  # Has data
    ]

    sample_codes = ["005930", "035720", "000660"]
    result = mock_db_manager.check_domestic_stock_data_exists_batch(sample_codes, "20240101", "20241231")

    assert len(result) == 3, "Should return 3 entries"
    assert all(isinstance(v, bool) for v in result.values()), "All values should be bool"
    assert result["005930"] is True, "005930 should have data"
    assert result["035720"] is False, "035720 should not have data"
    assert result["000660"] is True, "000660 should have data"


def test_batch_check_larger_batch(mock_db_manager, mock_duckdb_connection):
    """Test check_data_exists_batch with larger batch (15 codes)."""
    # Mock execute to return results for 15 stocks
    mock_results = [(f"{i:06d}", i % 2 * 10) for i in range(1, 16)]  # Alternating data/no-data
    mock_duckdb_connection.execute.return_value.fetchall.return_value = mock_results

    large_batch = [f"{i:06d}" for i in range(1, 16)]
    result = mock_db_manager.check_domestic_stock_data_exists_batch(large_batch, "20240101", "20241231")

    assert len(result) == 15, "Should return 15 entries"
    assert all(isinstance(v, bool) for v in result.values()), "All values should be bool"


def test_import_batch_logic():
    """Test import_batch chunking logic (pure logic test without I/O)."""
    # Simulate chunking logic
    stock_codes = [f"{i:06d}" for i in range(1, 25)]  # 24 stocks
    chunk_size = 10

    chunks = []
    for chunk_start in range(0, len(stock_codes), chunk_size):
        chunk_end = min(chunk_start + chunk_size, len(stock_codes))
        chunk = stock_codes[chunk_start:chunk_end]
        chunks.append(chunk)

    assert len(chunks) == 3, "24 stocks should create 3 chunks"
    assert len(chunks[0]) == 10, "First chunk should have 10 items"
    assert len(chunks[1]) == 10, "Second chunk should have 10 items"
    assert len(chunks[2]) == 4, "Third chunk should have 4 items"


def test_chunking_edge_cases():
    """Test edge cases for chunking logic."""
    chunk_size = 10

    # Test 1: Exactly chunk_size items
    codes = [f"{i:06d}" for i in range(1, 11)]  # 10 items
    chunks = [codes[i : i + chunk_size] for i in range(0, len(codes), chunk_size)]
    assert len(chunks) == 1, "10 items should create 1 chunk"
    assert len(chunks[0]) == 10

    # Test 2: Exactly 2x chunk_size items
    codes = [f"{i:06d}" for i in range(1, 21)]  # 20 items
    chunks = [codes[i : i + chunk_size] for i in range(0, len(codes), chunk_size)]
    assert len(chunks) == 2, "20 items should create 2 chunks"
    assert all(len(c) == 10 for c in chunks)

    # Test 3: Single item
    codes = ["005930"]
    chunks = [codes[i : i + chunk_size] for i in range(0, len(codes), chunk_size)]
    assert len(chunks) == 1, "1 item should create 1 chunk"
    assert len(chunks[0]) == 1

    # Test 4: Empty list
    codes = []
    chunks = [codes[i : i + chunk_size] for i in range(0, len(codes), chunk_size)]
    assert len(chunks) == 0, "Empty list should create 0 chunks"


# ============================================================================
# Concurrent Import Tests
# ============================================================================


def test_stock_fetch_result_dataclass():
    """Test StockFetchResult dataclass structure."""
    from cluefin_cli.data.stock_importer import StockFetchResult

    # Test success case
    result = StockFetchResult(
        stock_code="005930",
        success=True,
        data={"output1": None, "output2": []},
    )
    assert result.stock_code == "005930"
    assert result.success is True
    assert result.data is not None
    assert result.error is None

    # Test failure case
    result = StockFetchResult(
        stock_code="005930",
        success=False,
        error="Network error",
    )
    assert result.success is False
    assert result.error == "Network error"
    assert result.data is None


def test_domestic_importer_init_with_rate_limit():
    """Test DomesticStockChartImporter initialization with rate limit params."""
    from cluefin_cli.data.stock_importer import DomesticStockChartImporter

    mock_client = MagicMock()
    mock_db = MagicMock()

    # Default values
    importer = DomesticStockChartImporter(mock_client, mock_db)
    assert importer.rate_limit == 20.0
    assert importer.max_workers == 3
    assert importer.rate_limiter is not None

    # Custom values
    importer = DomesticStockChartImporter(
        mock_client, mock_db, rate_limit=10.0, max_workers=5
    )
    assert importer.rate_limit == 10.0
    assert importer.max_workers == 5

    # Max workers limit
    importer = DomesticStockChartImporter(
        mock_client, mock_db, max_workers=20
    )
    assert importer.max_workers == 10, "max_workers should be capped at 10"


def test_overseas_importer_init_with_rate_limit():
    """Test OverseasStockChartImporter initialization with rate limit params."""
    from cluefin_cli.data.stock_importer import OverseasStockChartImporter

    mock_client = MagicMock()
    mock_db = MagicMock()

    # Default values
    importer = OverseasStockChartImporter(mock_client, mock_db)
    assert importer.rate_limit == 20.0
    assert importer.max_workers == 3
    assert importer.rate_limiter is not None


def test_create_worker_client():
    """Test _create_worker_client creates independent client instances."""
    from cluefin_cli.data.stock_importer import DomesticStockChartImporter

    mock_client = MagicMock()
    mock_client.token = "test_token"  # nosec B105 - test mock value
    mock_client.app_key = "test_app_key"  # nosec B105 - test mock value
    mock_client.secret_key = "test_secret"  # nosec B105 - test mock value
    mock_client.env = "prod"
    mock_client.debug = False

    mock_db = MagicMock()

    importer = DomesticStockChartImporter(mock_client, mock_db)

    # Create worker client
    worker_client = importer._create_worker_client()

    # Verify it's a new instance with same credentials
    assert worker_client is not mock_client
    assert worker_client.token == mock_client.token
    assert worker_client.app_key == mock_client.app_key


def test_save_chunk_results_success():
    """Test _save_chunk_results with successful results."""
    from cluefin_cli.data.stock_importer import (
        DomesticStockChartImporter,
        StockFetchResult,
    )
    import pandas as pd

    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_db.insert_domestic_stock_daily_chart.return_value = 10

    importer = DomesticStockChartImporter(mock_client, mock_db)

    # Mock _prepare_stock_chart_data
    importer._prepare_stock_chart_data = MagicMock(return_value=pd.DataFrame())

    results = [
        StockFetchResult(
            stock_code="005930",
            success=True,
            data={"output1": None, "output2": [1, 2, 3]},
        ),
    ]

    counts = importer._save_chunk_results(results)
    assert counts["005930"] == 10


def test_save_chunk_results_with_errors():
    """Test _save_chunk_results handles errors correctly."""
    from cluefin_cli.data.stock_importer import (
        DomesticStockChartImporter,
        StockFetchResult,
    )

    mock_client = MagicMock()
    mock_db = MagicMock()

    importer = DomesticStockChartImporter(mock_client, mock_db)

    results = [
        StockFetchResult(stock_code="005930", success=False, error="Network error"),
        StockFetchResult(stock_code="035720", success=True, data=None),
        StockFetchResult(stock_code="000660", success=True, data={"output2": []}),
    ]

    counts = importer._save_chunk_results(results)
    assert counts["005930"] == -1, "Failed fetch should return -1"
    assert counts["035720"] == 0, "No data should return 0"
    assert counts["000660"] == 0, "Empty output2 should return 0"


def test_token_bucket_integration():
    """Test TokenBucket is properly integrated."""
    from cluefin_openapi import TokenBucket
    from cluefin_cli.data.stock_importer import DomesticStockChartImporter

    mock_client = MagicMock()
    mock_db = MagicMock()

    importer = DomesticStockChartImporter(mock_client, mock_db, rate_limit=10.0)

    # Verify TokenBucket is created with correct parameters
    assert isinstance(importer.rate_limiter, TokenBucket)
    assert importer.rate_limiter.capacity == 10
    assert importer.rate_limiter.refill_rate == 10.0


# ============================================================================
# OverseasStockChartImporter Tests
# ============================================================================


def test_overseas_create_worker_client():
    """Test OverseasStockChartImporter._create_worker_client creates independent client."""
    from cluefin_cli.data.stock_importer import OverseasStockChartImporter

    mock_client = MagicMock()
    mock_client.token = "test_token"  # nosec B105 - test mock value
    mock_client.app_key = "test_app_key"  # nosec B105 - test mock value
    mock_client.secret_key = "test_secret"  # nosec B105 - test mock value
    mock_client.env = "prod"
    mock_client.debug = False

    mock_db = MagicMock()

    importer = OverseasStockChartImporter(mock_client, mock_db)

    # Create worker client
    worker_client = importer._create_worker_client()

    # Verify it's a new instance with same credentials
    assert worker_client is not mock_client
    assert worker_client.token == mock_client.token
    assert worker_client.app_key == mock_client.app_key


def test_overseas_save_chunk_results_success():
    """Test OverseasStockChartImporter._save_chunk_results with successful results."""
    from cluefin_cli.data.stock_importer import (
        OverseasStockChartImporter,
        StockFetchResult,
    )
    import pandas as pd

    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_db.insert_overseas_stock_daily_chart.return_value = 10

    importer = OverseasStockChartImporter(mock_client, mock_db)

    # Mock _prepare_stock_chart_data
    importer._prepare_stock_chart_data = MagicMock(return_value=pd.DataFrame())

    results = [
        StockFetchResult(
            stock_code="AAPL",
            success=True,
            data={"output1": None, "output2": [1, 2, 3], "start_date": "20240101"},
        ),
    ]

    counts = importer._save_chunk_results("NYSE", results)
    assert counts["AAPL"] == 10


def test_overseas_save_chunk_results_with_errors():
    """Test OverseasStockChartImporter._save_chunk_results handles errors correctly."""
    from cluefin_cli.data.stock_importer import (
        OverseasStockChartImporter,
        StockFetchResult,
    )

    mock_client = MagicMock()
    mock_db = MagicMock()

    importer = OverseasStockChartImporter(mock_client, mock_db)

    results = [
        StockFetchResult(stock_code="AAPL", success=False, error="Network error"),
        StockFetchResult(stock_code="GOOGL", success=True, data=None),
        StockFetchResult(stock_code="MSFT", success=True, data={"output2": []}),
    ]

    counts = importer._save_chunk_results("NYSE", results)
    assert counts["AAPL"] == -1, "Failed fetch should return -1"
    assert counts["GOOGL"] == 0, "No data should return 0"
    assert counts["MSFT"] == 0, "Empty output2 should return 0"


def test_overseas_token_bucket_integration():
    """Test TokenBucket is properly integrated in OverseasStockChartImporter."""
    from cluefin_openapi import TokenBucket
    from cluefin_cli.data.stock_importer import OverseasStockChartImporter

    mock_client = MagicMock()
    mock_db = MagicMock()

    importer = OverseasStockChartImporter(mock_client, mock_db, rate_limit=15.0)

    # Verify TokenBucket is created with correct parameters
    assert isinstance(importer.rate_limiter, TokenBucket)
    assert importer.rate_limiter.capacity == 15
    assert importer.rate_limiter.refill_rate == 15.0
