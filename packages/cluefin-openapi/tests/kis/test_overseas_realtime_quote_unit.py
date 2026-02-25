"""Unit tests for KIS OverseasRealtimeQuote module."""

from unittest.mock import AsyncMock, Mock

import pytest

from cluefin_openapi.kis._overseas_realtime_quote import OverseasRealtimeQuote
from cluefin_openapi.kis._overseas_realtime_quote_types import (
    OVERSEAS_ORDERBOOK_FIELD_NAMES,
    OverseasRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient


@pytest.fixture
def mock_socket_client() -> Mock:
    """Create mock SocketClient for testing (production environment)."""
    client = Mock(spec=SocketClient)
    client.subscribe = AsyncMock()
    client.unsubscribe = AsyncMock()
    client.env = "prod"
    return client


@pytest.fixture
def mock_socket_client_dev() -> Mock:
    """Create mock SocketClient for testing (development environment)."""
    client = Mock(spec=SocketClient)
    client.subscribe = AsyncMock()
    client.unsubscribe = AsyncMock()
    client.env = "dev"
    return client


@pytest.fixture
def realtime_quote(mock_socket_client) -> OverseasRealtimeQuote:
    """Create OverseasRealtimeQuote instance for testing."""
    return OverseasRealtimeQuote(mock_socket_client)


@pytest.fixture
def sample_orderbook_data() -> list[str]:
    """Generate sample overseas orderbook data (71 fields)."""
    # Create a list with 71 items
    # Using specific values to help identification
    data = ["val_" + str(i) for i in range(71)]

    # Set critical fields to match expected types if they had specific validation (currently all str)
    # rsym (0), symb (1)
    data[0] = "RNASAAPL"
    data[1] = "AAPL"

    return data


class TestOverseasRealtimeQuoteInit:
    """Test OverseasRealtimeQuote initialization."""

    def test_init_with_socket_client(self, mock_socket_client):
        """Test initialization with SocketClient."""
        quote = OverseasRealtimeQuote(mock_socket_client)
        assert quote.socket_client is mock_socket_client

    def test_tr_id_constant(self):
        """Test TR_ID constant value."""
        assert OverseasRealtimeQuote.TR_ID == "HDFSASP0"


class TestSubscribe:
    """Test subscribe method."""

    def test_generate_tr_key_regular(self, realtime_quote):
        """Test TR Key generation for Regular/Day market (R)."""
        # Default "R"
        key = realtime_quote._generate_tr_key("AAPL", "NAS", "R")
        assert key == "RNASAAPL"

    def test_generate_tr_key_night(self, realtime_quote):
        """Test TR Key generation for US Night market (D)."""
        key = realtime_quote._generate_tr_key("AAPL", "NAS", "D")
        assert key == "DNASAAPL"

    @pytest.mark.asyncio
    async def test_subscribe_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe("AAPL", "NAS")
        # Default service_type is "R" -> "RNASAAPL"
        mock_socket_client.subscribe.assert_called_once_with("HDFSASP0", "RNASAAPL")

    @pytest.mark.asyncio
    async def test_subscribe_with_service_type(self, realtime_quote, mock_socket_client):
        """Test subscribe with specific service type."""
        await realtime_quote.subscribe("AAPL", "NAS", service_type="D")
        mock_socket_client.subscribe.assert_called_once_with("HDFSASP0", "DNASAAPL")

    @pytest.mark.asyncio
    async def test_subscribe_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe raises ValueError in dev environment."""
        quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await quote.subscribe("AAPL", "NAS")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)


class TestUnsubscribe:
    """Test unsubscribe method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe("AAPL", "NAS")
        mock_socket_client.unsubscribe.assert_called_once_with("HDFSASP0", "RNASAAPL")

    @pytest.mark.asyncio
    async def test_unsubscribe_with_service_type(self, realtime_quote, mock_socket_client):
        """Test unsubscribe with specific service type."""
        await realtime_quote.unsubscribe("AAPL", "NAS", service_type="D")
        mock_socket_client.unsubscribe.assert_called_once_with("HDFSASP0", "DNASAAPL")

    @pytest.mark.asyncio
    async def test_unsubscribe_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe raises ValueError in dev environment."""
        quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await quote.unsubscribe("AAPL", "NAS")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)


class TestParseData:
    """Test parse_data method."""

    def test_parse_data_returns_model(self, sample_orderbook_data):
        """Test that parse_data returns list of OverseasRealtimeOrderbookItem."""
        result = OverseasRealtimeQuote.parse_data(sample_orderbook_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OverseasRealtimeOrderbookItem)

    def test_parse_data_field_values(self, sample_orderbook_data):
        """Test that parsed data has correct field values."""
        result = OverseasRealtimeQuote.parse_data(sample_orderbook_data)

        assert result[0].rsym == "RNASAAPL"
        assert result[0].symb == "AAPL"
        # Check last field (index 70)
        assert result[0].dask10 == "val_70"

    def test_parse_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["val"] * 70  # Only 70 fields

        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_data(short_data)

        assert "Expected at least 71 fields, got 70" in str(exc_info.value)

    def test_parse_data_batched_records(self, sample_orderbook_data):
        """Test parsing batched records (multiple of 71)."""
        batched_data = sample_orderbook_data * 2  # 142 fields

        result = OverseasRealtimeQuote.parse_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].rsym == "RNASAAPL"
        assert result[1].rsym == "RNASAAPL"


class TestOverseasRealtimeOrderbookItem:
    """Test OverseasRealtimeOrderbookItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 71 fields."""
        assert len(OVERSEAS_ORDERBOOK_FIELD_NAMES) == 71
        assert len(OverseasRealtimeOrderbookItem.model_fields) == 71
