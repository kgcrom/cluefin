"""Unit tests for stock_fetcher.py concurrent processing functionality.

This module tests:
1. MetadataFetchResult dataclass structure
2. StockListFetcher initialization with rate limit params
3. Worker client creation methods
4. Chunk result saving methods

Run with: uv run pytest apps/cluefin-cli/tests/unit/test_stock_fetcher.py -v
"""

from unittest.mock import MagicMock

# ============================================================================
# MetadataFetchResult Dataclass Tests
# ============================================================================


def test_metadata_fetch_result_dataclass_success():
    """Test MetadataFetchResult dataclass with successful fetch."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult

    result = MetadataFetchResult(
        stock_code="005930",
        success=True,
        data={"stock_code": "005930", "stock_name": "Samsung"},
    )
    assert result.stock_code == "005930"
    assert result.success is True
    assert result.data is not None
    assert result.error is None
    assert result.skipped is False


def test_metadata_fetch_result_dataclass_failure():
    """Test MetadataFetchResult dataclass with failed fetch."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult

    result = MetadataFetchResult(
        stock_code="005930",
        success=False,
        error="Network error",
    )
    assert result.stock_code == "005930"
    assert result.success is False
    assert result.error == "Network error"
    assert result.data is None
    assert result.skipped is False


def test_metadata_fetch_result_dataclass_skipped():
    """Test MetadataFetchResult dataclass with skipped (ETF) case."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult

    result = MetadataFetchResult(
        stock_code="SPY",
        success=True,
        skipped=True,
    )
    assert result.stock_code == "SPY"
    assert result.success is True
    assert result.skipped is True
    assert result.data is None


# ============================================================================
# StockListFetcher Initialization Tests
# ============================================================================


def test_stock_list_fetcher_init_with_default_rate_limit():
    """Test StockListFetcher initialization with default rate limit params."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    assert fetcher.rate_limit == 20.0
    assert fetcher.max_workers == 3
    assert fetcher.rate_limiter is not None


def test_stock_list_fetcher_init_with_custom_rate_limit():
    """Test StockListFetcher initialization with custom rate limit params."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client, rate_limit=10.0, max_workers=5)

    assert fetcher.rate_limit == 10.0
    assert fetcher.max_workers == 5


def test_stock_list_fetcher_init_max_workers_capped():
    """Test StockListFetcher max_workers is capped at 10."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client, max_workers=20)

    assert fetcher.max_workers == 10, "max_workers should be capped at 10"


def test_stock_list_fetcher_init_with_kis_client():
    """Test StockListFetcher initialization with KIS client."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, kis_client=mock_kis_client)

    assert fetcher.kis_client is mock_kis_client


# ============================================================================
# Worker Client Creation Tests
# ============================================================================


def test_create_kiwoom_worker_client():
    """Test _create_kiwoom_worker_client creates new client instance."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kiwoom_client.url = "https://api.kiwoom.com"  # prod URL
    mock_kiwoom_client.token = "test_token"  # nosec B105 - test mock value
    mock_kiwoom_client.timeout = 30
    mock_kiwoom_client.max_retries = 3
    mock_kiwoom_client.debug = False

    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    # Create worker client
    worker_client = fetcher._create_kiwoom_worker_client()

    # Verify it's a new instance with same credentials
    assert worker_client is not mock_kiwoom_client
    assert worker_client.token == mock_kiwoom_client.token


def test_create_kiwoom_worker_client_dev_env():
    """Test _create_kiwoom_worker_client with dev environment."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kiwoom_client.url = "https://mockapi.kiwoom.com"  # dev URL
    mock_kiwoom_client.token = "test_token"  # nosec B105 - test mock value
    mock_kiwoom_client.timeout = 30
    mock_kiwoom_client.max_retries = 3
    mock_kiwoom_client.debug = False

    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)
    worker_client = fetcher._create_kiwoom_worker_client()

    # Dev environment should use mockapi URL
    assert "mockapi" in worker_client.url


def test_create_kis_worker_client():
    """Test _create_kis_worker_client creates new client instance."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_kis_client.token = "kis_token"  # nosec B105 - test mock value
    mock_kis_client.app_key = "app_key"
    mock_kis_client.secret_key = "secret_key"  # nosec B105 - test mock value
    mock_kis_client.env = "prod"
    mock_kis_client.debug = False

    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, kis_client=mock_kis_client)

    # Create worker client
    worker_client = fetcher._create_kis_worker_client()

    # Verify it's a new instance with same credentials
    assert worker_client is not mock_kis_client
    assert worker_client.token == mock_kis_client.token
    assert worker_client.app_key == mock_kis_client.app_key


def test_create_kis_worker_client_none():
    """Test _create_kis_worker_client returns None when no KIS client."""
    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, kis_client=None)

    worker_client = fetcher._create_kis_worker_client()
    assert worker_client is None


# ============================================================================
# Chunk Result Saving Tests
# ============================================================================


def test_save_domestic_chunk_results_success():
    """Test _save_domestic_chunk_results with successful results."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()
    mock_db.upsert_domestic_stock_metadata_extended.return_value = 3

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="005930",
            success=True,
            data={"stock_code": "005930", "stock_name": "Samsung"},
        ),
        MetadataFetchResult(
            stock_code="035720",
            success=True,
            data={"stock_code": "035720", "stock_name": "Kakao"},
        ),
        MetadataFetchResult(
            stock_code="000660",
            success=True,
            data={"stock_code": "000660", "stock_name": "SK Hynix"},
        ),
    ]

    success_count, failed_count = fetcher._save_domestic_chunk_results(results)

    assert success_count == 3
    assert failed_count == 0
    mock_db.upsert_domestic_stock_metadata_extended.assert_called_once()


def test_save_domestic_chunk_results_with_errors():
    """Test _save_domestic_chunk_results handles errors correctly."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()
    mock_db.upsert_domestic_stock_metadata_extended.return_value = 1

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="005930",
            success=False,
            error="Network error",
        ),
        MetadataFetchResult(
            stock_code="035720",
            success=True,
            data={"stock_code": "035720", "stock_name": "Kakao"},
        ),
        MetadataFetchResult(
            stock_code="000660",
            success=False,
            error="Timeout",
        ),
    ]

    success_count, failed_count = fetcher._save_domestic_chunk_results(results)

    assert success_count == 1
    assert failed_count == 2


def test_save_domestic_chunk_results_empty():
    """Test _save_domestic_chunk_results with all failed results."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="005930",
            success=False,
            error="Network error",
        ),
    ]

    success_count, failed_count = fetcher._save_domestic_chunk_results(results)

    assert success_count == 0
    assert failed_count == 1
    mock_db.upsert_domestic_stock_metadata_extended.assert_not_called()


def test_save_overseas_chunk_results_success():
    """Test _save_overseas_chunk_results with successful results."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()
    mock_db.upsert_overseas_stock_metadata.return_value = 2

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="AAPL",
            success=True,
            data={"stock_code": "AAPL", "stock_name_en": "Apple"},
        ),
        MetadataFetchResult(
            stock_code="GOOGL",
            success=True,
            data={"stock_code": "GOOGL", "stock_name_en": "Google"},
        ),
    ]

    success_count, failed_count, skipped_count = fetcher._save_overseas_chunk_results(results)

    assert success_count == 2
    assert failed_count == 0
    assert skipped_count == 0
    mock_db.upsert_overseas_stock_metadata.assert_called_once()


def test_save_overseas_chunk_results_with_skipped():
    """Test _save_overseas_chunk_results handles ETF skipped cases."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()
    mock_db.upsert_overseas_stock_metadata.return_value = 1

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="AAPL",
            success=True,
            data={"stock_code": "AAPL", "stock_name_en": "Apple"},
        ),
        MetadataFetchResult(
            stock_code="SPY",
            success=True,
            skipped=True,  # ETF skipped
        ),
        MetadataFetchResult(
            stock_code="QQQ",
            success=True,
            skipped=True,  # ETF skipped
        ),
        MetadataFetchResult(
            stock_code="MSFT",
            success=False,
            error="API error",
        ),
    ]

    success_count, failed_count, skipped_count = fetcher._save_overseas_chunk_results(results)

    assert success_count == 1
    assert failed_count == 1
    assert skipped_count == 2


def test_save_overseas_chunk_results_all_skipped():
    """Test _save_overseas_chunk_results when all results are skipped."""
    from cluefin_cli.data.stock_fetcher import MetadataFetchResult, StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client)

    results = [
        MetadataFetchResult(
            stock_code="SPY",
            success=True,
            skipped=True,
        ),
        MetadataFetchResult(
            stock_code="QQQ",
            success=True,
            skipped=True,
        ),
    ]

    success_count, failed_count, skipped_count = fetcher._save_overseas_chunk_results(results)

    assert success_count == 0
    assert failed_count == 0
    assert skipped_count == 2
    mock_db.upsert_overseas_stock_metadata.assert_not_called()


# ============================================================================
# TokenBucket Integration Tests
# ============================================================================


def test_token_bucket_integration():
    """Test TokenBucket is properly integrated in StockListFetcher."""
    from cluefin_openapi import TokenBucket

    from cluefin_cli.data.stock_fetcher import StockListFetcher

    mock_kiwoom_client = MagicMock()
    mock_kis_client = MagicMock()
    mock_db = MagicMock()

    fetcher = StockListFetcher(mock_kiwoom_client, mock_db, mock_kis_client, rate_limit=10.0)

    # Verify TokenBucket is created with correct parameters
    assert isinstance(fetcher.rate_limiter, TokenBucket)
    assert fetcher.rate_limiter.capacity == 10
    assert fetcher.rate_limiter.refill_rate == 10.0
