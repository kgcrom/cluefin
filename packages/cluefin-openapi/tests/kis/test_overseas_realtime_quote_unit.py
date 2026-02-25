"""Unit tests for KIS OverseasRealtimeQuote module."""

from unittest.mock import AsyncMock, Mock

import pytest

from cluefin_openapi.kis._overseas_realtime_quote import OverseasRealtimeQuote
from cluefin_openapi.kis._overseas_realtime_quote_types import (
    OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
    OVERSEAS_EXECUTION_FIELD_NAMES,
    OVERSEAS_ORDERBOOK_FIELD_NAMES,
    OverseasRealtimeDelayedOrderbookItem,
    OverseasRealtimeExecutionItem,
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
    data = ["val_" + str(i) for i in range(71)]
    data[0] = "RNASAAPL"
    data[1] = "AAPL"
    return data


@pytest.fixture
def sample_execution_data() -> list[str]:
    """Generate sample overseas execution data (26 fields)."""
    return [
        "DNASAAPL",  # rsym
        "AAPL",  # symb
        "4",  # zdiv
        "20260225",  # tymd
        "20260225",  # xymd
        "103000",  # xhms
        "20260226",  # kymd
        "003000",  # khms
        "182.5000",  # open
        "185.0000",  # high
        "181.0000",  # low
        "184.2500",  # last
        "2",  # sign
        "1.7500",  # diff
        "0.96",  # rate
        "184.2000",  # pbid
        "184.3000",  # pask
        "500",  # vbid
        "300",  # vask
        "100",  # evol
        "5000000",  # tvol
        "920000000",  # tamt
        "60",  # bivl
        "40",  # asvl
        "98.50",  # strn
        "NAS",  # mtyp
    ]


@pytest.fixture
def sample_delayed_orderbook_data() -> list[str]:
    """Generate sample delayed orderbook data (17 fields)."""
    return [
        "DHKS00003",  # rsym
        "00003",  # symb
        "2",  # zdiv
        "20250224",  # xymd
        "143000",  # xhms
        "20250225",  # kymd
        "003000",  # khms
        "50000",  # bvol
        "30000",  # avol
        "1000",  # bdvl
        "-500",  # advl
        "12.50",  # pbid1
        "12.55",  # pask1
        "10000",  # vbid1
        "8000",  # vask1
        "200",  # dbid1
        "-100",  # dask1
    ]


class TestOverseasRealtimeQuoteInit:
    """Test OverseasRealtimeQuote initialization."""

    def test_init_with_socket_client(self, mock_socket_client):
        """Test initialization with SocketClient."""
        quote = OverseasRealtimeQuote(mock_socket_client)
        assert quote.socket_client is mock_socket_client

    def test_tr_id_constant(self):
        """Test TR_ID constant value."""
        assert OverseasRealtimeQuote.TR_ID == "HDFSASP0"

    def test_tr_id_execution_constant(self):
        """Test TR_ID_EXECUTION constant value."""
        assert OverseasRealtimeQuote.TR_ID_EXECUTION == "HDFSCNT0"

    def test_tr_id_delayed_orderbook_constant(self):
        """Test TR_ID_DELAYED_ORDERBOOK constant value."""
        assert OverseasRealtimeQuote.TR_ID_DELAYED_ORDERBOOK == "HDFSASP1"


class TestSubscribe:
    """Test subscribe method."""

    def test_generate_tr_key_regular(self, realtime_quote):
        """Test TR Key generation for Regular/Day market (R)."""
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
        assert result[0].dask10 == "val_70"

    def test_parse_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["val"] * 70

        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_data(short_data)

        assert "Expected at least 71 fields, got 70" in str(exc_info.value)

    def test_parse_data_batched_records(self, sample_orderbook_data):
        """Test parsing batched records (multiple of 71)."""
        batched_data = sample_orderbook_data * 2

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


class TestSubscribeExecution:
    """Test subscribe_execution method."""

    @pytest.mark.asyncio
    async def test_subscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_execution calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_execution("DNASAAPL")

        mock_socket_client.subscribe.assert_called_once_with("HDFSCNT0", "DNASAAPL")

    @pytest.mark.asyncio
    async def test_subscribe_execution_different_keys(self, realtime_quote, mock_socket_client):
        """Test subscription with different tr_keys."""
        await realtime_quote.subscribe_execution("DNASAAPL")
        mock_socket_client.subscribe.assert_called_with("HDFSCNT0", "DNASAAPL")

        await realtime_quote.subscribe_execution("DNYSAMZN")
        mock_socket_client.subscribe.assert_called_with("HDFSCNT0", "DNYSAMZN")

    @pytest.mark.asyncio
    async def test_subscribe_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe_execution raises ValueError in dev environment."""
        realtime_quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.subscribe_execution("DNASAAPL")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestUnsubscribeExecution:
    """Test unsubscribe_execution method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_execution calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_execution("DNASAAPL")

        mock_socket_client.unsubscribe.assert_called_once_with("HDFSCNT0", "DNASAAPL")

    @pytest.mark.asyncio
    async def test_unsubscribe_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe_execution raises ValueError in dev environment."""
        realtime_quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.unsubscribe_execution("DNASAAPL")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestParseExecutionData:
    """Test parse_execution_data method."""

    def test_parse_execution_data_returns_model(self, sample_execution_data):
        """Test that parse_execution_data returns list of OverseasRealtimeExecutionItem."""
        result = OverseasRealtimeQuote.parse_execution_data(sample_execution_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OverseasRealtimeExecutionItem)

    def test_parse_execution_data_field_values(self, sample_execution_data):
        """Test that parsed data has correct field values."""
        result = OverseasRealtimeQuote.parse_execution_data(sample_execution_data)

        assert result[0].rsym == "DNASAAPL"
        assert result[0].symb == "AAPL"
        assert result[0].zdiv == "4"
        assert result[0].tymd == "20260225"
        assert result[0].xymd == "20260225"
        assert result[0].xhms == "103000"
        assert result[0].kymd == "20260226"
        assert result[0].khms == "003000"
        assert result[0].open == "182.5000"
        assert result[0].high == "185.0000"
        assert result[0].low == "181.0000"
        assert result[0].last == "184.2500"
        assert result[0].sign == "2"
        assert result[0].diff == "1.7500"
        assert result[0].rate == "0.96"
        assert result[0].pbid == "184.2000"
        assert result[0].pask == "184.3000"
        assert result[0].vbid == "500"
        assert result[0].vask == "300"
        assert result[0].evol == "100"
        assert result[0].tvol == "5000000"
        assert result[0].tamt == "920000000"
        assert result[0].bivl == "60"
        assert result[0].asvl == "40"
        assert result[0].strn == "98.50"
        assert result[0].mtyp == "NAS"

    def test_parse_execution_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["DNASAAPL", "AAPL", "4"]

        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_execution_data(short_data)

        assert "Expected at least 26 fields, got 3" in str(exc_info.value)

    def test_parse_execution_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_execution_data([])

        assert "Expected at least 26 fields, got 0" in str(exc_info.value)

    def test_parse_execution_data_batched_5_records(self, sample_execution_data):
        """Test parsing 5 batched records (5 × 26 = 130 fields)."""
        batched_data = []
        for i in range(5):
            record = sample_execution_data.copy()
            record[11] = f"{184.25 + i * 0.5:.4f}"
            batched_data.extend(record)

        result = OverseasRealtimeQuote.parse_execution_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 5
        for i, item in enumerate(result):
            assert isinstance(item, OverseasRealtimeExecutionItem)
            assert item.last == f"{184.25 + i * 0.5:.4f}"

    def test_parse_execution_data_single_record_with_extra_fields(self, sample_execution_data):
        """Test single record with extra fields (26 + 3 = 29 fields) - forward compatibility."""
        data = sample_execution_data + ["extra1", "extra2", "extra3"]

        result = OverseasRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].rsym == "DNASAAPL"
        assert result[0].mtyp == "NAS"

    def test_parse_execution_data_large_batch(self):
        """Test parsing large batch (20 × 26 = 520 fields)."""
        data = ["value"] * (20 * 26)

        result = OverseasRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 20


class TestOverseasRealtimeExecutionItem:
    """Test OverseasRealtimeExecutionItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 26 fields."""
        assert len(OVERSEAS_EXECUTION_FIELD_NAMES) == 26
        assert len(OverseasRealtimeExecutionItem.model_fields) == 26

    def test_model_validation_from_dict(self, sample_execution_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(OVERSEAS_EXECUTION_FIELD_NAMES, sample_execution_data, strict=False))
        item = OverseasRealtimeExecutionItem.model_validate(field_dict)

        assert item.rsym == "DNASAAPL"
        assert item.last == "184.2500"
        assert item.mtyp == "NAS"


class TestOverseasExecutionFieldNames:
    """Test OVERSEAS_EXECUTION_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 26 entries."""
        assert len(OVERSEAS_EXECUTION_FIELD_NAMES) == 26

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in OVERSEAS_EXECUTION_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(OVERSEAS_EXECUTION_FIELD_NAMES) == len(set(OVERSEAS_EXECUTION_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(OverseasRealtimeExecutionItem.model_fields.keys())
        field_names_set = set(OVERSEAS_EXECUTION_FIELD_NAMES)
        assert field_names_set == model_fields


class TestSubscribeDelayedOrderbook:
    """Test subscribe_delayed_orderbook method."""

    @pytest.mark.asyncio
    async def test_subscribe_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_delayed_orderbook calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_delayed_orderbook("DHKS00003")

        mock_socket_client.subscribe.assert_called_once_with("HDFSASP1", "DHKS00003")

    @pytest.mark.asyncio
    async def test_subscribe_different_tr_keys(self, realtime_quote, mock_socket_client):
        """Test subscription with different tr_keys."""
        await realtime_quote.subscribe_delayed_orderbook("DHKS00003")
        mock_socket_client.subscribe.assert_called_with("HDFSASP1", "DHKS00003")

        await realtime_quote.subscribe_delayed_orderbook("DNAS00001")
        mock_socket_client.subscribe.assert_called_with("HDFSASP1", "DNAS00001")

    @pytest.mark.asyncio
    async def test_subscribe_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe_delayed_orderbook raises ValueError in dev environment."""
        realtime_quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.subscribe_delayed_orderbook("DHKS00003")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestUnsubscribeDelayedOrderbook:
    """Test unsubscribe_delayed_orderbook method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_delayed_orderbook calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_delayed_orderbook("DHKS00003")

        mock_socket_client.unsubscribe.assert_called_once_with("HDFSASP1", "DHKS00003")

    @pytest.mark.asyncio
    async def test_unsubscribe_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe_delayed_orderbook raises ValueError in dev environment."""
        realtime_quote = OverseasRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.unsubscribe_delayed_orderbook("DHKS00003")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestParseDelayedOrderbookData:
    """Test parse_delayed_orderbook_data method."""

    def test_parse_returns_model(self, sample_delayed_orderbook_data):
        """Test that parse_delayed_orderbook_data returns list of OverseasRealtimeDelayedOrderbookItem."""
        result = OverseasRealtimeQuote.parse_delayed_orderbook_data(sample_delayed_orderbook_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OverseasRealtimeDelayedOrderbookItem)

    def test_parse_field_values(self, sample_delayed_orderbook_data):
        """Test that parsed data has correct field values."""
        result = OverseasRealtimeQuote.parse_delayed_orderbook_data(sample_delayed_orderbook_data)

        assert result[0].rsym == "DHKS00003"
        assert result[0].symb == "00003"
        assert result[0].zdiv == "2"
        assert result[0].xymd == "20250224"
        assert result[0].xhms == "143000"
        assert result[0].kymd == "20250225"
        assert result[0].khms == "003000"
        assert result[0].bvol == "50000"
        assert result[0].avol == "30000"
        assert result[0].bdvl == "1000"
        assert result[0].advl == "-500"
        assert result[0].pbid1 == "12.50"
        assert result[0].pask1 == "12.55"
        assert result[0].vbid1 == "10000"
        assert result[0].vask1 == "8000"
        assert result[0].dbid1 == "200"
        assert result[0].dask1 == "-100"

    def test_parse_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["DHKS00003", "00003", "2"]

        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_delayed_orderbook_data(short_data)

        assert "Expected at least 17 fields, got 3" in str(exc_info.value)

    def test_parse_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OverseasRealtimeQuote.parse_delayed_orderbook_data([])

        assert "Expected at least 17 fields, got 0" in str(exc_info.value)

    def test_parse_batched_5_records(self, sample_delayed_orderbook_data):
        """Test parsing 5 batched records (5 × 17 = 85 fields)."""
        batched_data = []
        for i in range(5):
            record = sample_delayed_orderbook_data.copy()
            record[11] = str(12.50 + i * 0.10)
            batched_data.extend(record)

        result = OverseasRealtimeQuote.parse_delayed_orderbook_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 5
        for i, item in enumerate(result):
            assert isinstance(item, OverseasRealtimeDelayedOrderbookItem)
            assert item.pbid1 == str(12.50 + i * 0.10)

    def test_parse_single_record_with_extra_fields(self, sample_delayed_orderbook_data):
        """Test single record with extra fields (17 + 3 = 20 fields) - forward compatibility."""
        data = sample_delayed_orderbook_data + ["extra1", "extra2", "extra3"]

        result = OverseasRealtimeQuote.parse_delayed_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].rsym == "DHKS00003"
        assert result[0].dask1 == "-100"

    def test_parse_large_batch(self):
        """Test parsing large batch (20 × 17 = 340 fields)."""
        data = ["value"] * (20 * 17)

        result = OverseasRealtimeQuote.parse_delayed_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 20


class TestOverseasRealtimeDelayedOrderbookItem:
    """Test OverseasRealtimeDelayedOrderbookItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 17 fields."""
        assert len(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES) == 17
        assert len(OverseasRealtimeDelayedOrderbookItem.model_fields) == 17

    def test_model_validation_from_dict(self, sample_delayed_orderbook_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES, sample_delayed_orderbook_data, strict=False))
        item = OverseasRealtimeDelayedOrderbookItem.model_validate(field_dict)

        assert item.rsym == "DHKS00003"
        assert item.pbid1 == "12.50"
        assert item.pask1 == "12.55"

    def test_field_names_list_order(self, sample_delayed_orderbook_data):
        """Test that OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES order matches model fields."""
        field_dict = dict(zip(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES, sample_delayed_orderbook_data, strict=False))
        item = OverseasRealtimeDelayedOrderbookItem.model_validate(field_dict)

        assert OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES[0] == "rsym"
        assert item.rsym == "DHKS00003"

        assert OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES[16] == "dask1"
        assert item.dask1 == "-100"


class TestOverseasDelayedOrderbookFieldNames:
    """Test OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 17 entries."""
        assert len(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES) == 17

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES) == len(set(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(OverseasRealtimeDelayedOrderbookItem.model_fields.keys())
        field_names_set = set(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES)
        assert field_names_set == model_fields
