"""Unit tests for KIS OnmarketBondRealtimeQuote module."""

from unittest.mock import AsyncMock, Mock

import pytest

from cluefin_openapi.kis._onmarket_bond_realtime_quote import OnmarketBondRealtimeQuote
from cluefin_openapi.kis._onmarket_bond_realtime_quote_types import (
    BOND_EXECUTION_FIELD_NAMES,
    BOND_INDEX_EXECUTION_FIELD_NAMES,
    BOND_ORDERBOOK_FIELD_NAMES,
    OnmarketBondIndexRealtimeExecutionItem,
    OnmarketBondRealtimeExecutionItem,
    OnmarketBondRealtimeOrderbookItem,
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
def realtime_quote(mock_socket_client) -> OnmarketBondRealtimeQuote:
    """Create OnmarketBondRealtimeQuote instance for testing."""
    return OnmarketBondRealtimeQuote(mock_socket_client)


@pytest.fixture
def sample_bond_execution_data() -> list[str]:
    """Generate sample bond execution data (19 fields)."""
    return [
        "KR103502GA34",  # stnd_iscd
        "국고채권03500-5306",  # bond_isnm
        "093000",  # stck_cntg_hour
        "2",  # prdy_vrss_sign
        "50",  # prdy_vrss
        "0.50",  # prdy_ctrt
        "10050",  # stck_prpr
        "1000",  # cntg_vol
        "10000",  # stck_oprc
        "10100",  # stck_hgpr
        "9950",  # stck_lwpr
        "10000",  # stck_prdy_clpr
        "3.500",  # bond_cntg_ert
        "3.550",  # oprc_ert
        "3.480",  # hgpr_ert
        "3.520",  # lwpr_ert
        "50000",  # acml_vol
        "45000",  # prdy_vol
        "1",  # cntg_type_cls_code
    ]


class TestOnmarketBondRealtimeQuoteInit:
    """Test OnmarketBondRealtimeQuote initialization."""

    def test_init_with_socket_client(self, mock_socket_client):
        """Test initialization with SocketClient."""
        quote = OnmarketBondRealtimeQuote(mock_socket_client)
        assert quote.socket_client is mock_socket_client

    def test_tr_id_constant(self):
        """Test TR_ID_EXECUTION constant value."""
        assert OnmarketBondRealtimeQuote.TR_ID_EXECUTION == "H0BJCNT0"

    def test_tr_id_index_execution_constant(self):
        """Test TR_ID_INDEX_EXECUTION constant value."""
        assert OnmarketBondRealtimeQuote.TR_ID_INDEX_EXECUTION == "H0BICNT0"


class TestSubscribeBondExecution:
    """Test subscribe_execution method."""

    @pytest.mark.asyncio
    async def test_subscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_execution calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_execution("KR103502GA34")

        mock_socket_client.subscribe.assert_called_once_with("H0BJCNT0", "KR103502GA34")

    @pytest.mark.asyncio
    async def test_subscribe_execution_different_bond_codes(self, realtime_quote, mock_socket_client):
        """Test subscription with different bond codes."""
        await realtime_quote.subscribe_execution("KR103502GA34")
        mock_socket_client.subscribe.assert_called_with("H0BJCNT0", "KR103502GA34")

        await realtime_quote.subscribe_execution("KR1035027B56")
        mock_socket_client.subscribe.assert_called_with("H0BJCNT0", "KR1035027B56")

    @pytest.mark.asyncio
    async def test_subscribe_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe_execution raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.subscribe_execution("KR103502GA34")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestUnsubscribeBondExecution:
    """Test unsubscribe_execution method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_execution calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_execution("KR103502GA34")

        mock_socket_client.unsubscribe.assert_called_once_with("H0BJCNT0", "KR103502GA34")

    @pytest.mark.asyncio
    async def test_unsubscribe_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe_execution raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.unsubscribe_execution("KR103502GA34")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestParseBondExecutionData:
    """Test parse_execution_data method."""

    def test_parse_execution_data_returns_model(self, sample_bond_execution_data):
        """Test that parse_execution_data returns list of OnmarketBondRealtimeExecutionItem."""
        result = OnmarketBondRealtimeQuote.parse_execution_data(sample_bond_execution_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OnmarketBondRealtimeExecutionItem)

    def test_parse_execution_data_field_values(self, sample_bond_execution_data):
        """Test that parsed data has correct field values."""
        result = OnmarketBondRealtimeQuote.parse_execution_data(sample_bond_execution_data)

        assert result[0].stnd_iscd == "KR103502GA34"
        assert result[0].bond_isnm == "국고채권03500-5306"
        assert result[0].stck_cntg_hour == "093000"
        assert result[0].prdy_vrss_sign == "2"
        assert result[0].prdy_vrss == "50"
        assert result[0].prdy_ctrt == "0.50"
        assert result[0].stck_prpr == "10050"
        assert result[0].cntg_vol == "1000"
        assert result[0].stck_oprc == "10000"
        assert result[0].stck_hgpr == "10100"
        assert result[0].stck_lwpr == "9950"
        assert result[0].stck_prdy_clpr == "10000"
        assert result[0].bond_cntg_ert == "3.500"
        assert result[0].oprc_ert == "3.550"
        assert result[0].hgpr_ert == "3.480"
        assert result[0].lwpr_ert == "3.520"
        assert result[0].acml_vol == "50000"
        assert result[0].prdy_vol == "45000"
        assert result[0].cntg_type_cls_code == "1"

    def test_parse_execution_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["KR103502GA34", "국고채권", "093000"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_execution_data(short_data)

        assert "Expected at least 19 fields, got 3" in str(exc_info.value)

    def test_parse_execution_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_execution_data([])

        assert "Expected at least 19 fields, got 0" in str(exc_info.value)

    def test_parse_execution_data_batched_5_records(self, sample_bond_execution_data):
        """Test parsing 5 batched records (5 × 19 = 95 fields)."""
        batched_data = []
        for i in range(5):
            record = sample_bond_execution_data.copy()
            # Vary price field to distinguish records
            record[6] = str(10050 + i * 10)
            batched_data.extend(record)

        result = OnmarketBondRealtimeQuote.parse_execution_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 5
        for i, item in enumerate(result):
            assert isinstance(item, OnmarketBondRealtimeExecutionItem)
            assert item.stck_prpr == str(10050 + i * 10)

    def test_parse_execution_data_single_record_with_extra_fields(self, sample_bond_execution_data):
        """Test single record with extra fields (19 + 3 = 22 fields) - forward compatibility."""
        data = sample_bond_execution_data + ["extra1", "extra2", "extra3"]

        result = OnmarketBondRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        # Extra fields should be ignored, first 19 used
        assert result[0].stnd_iscd == "KR103502GA34"
        assert result[0].cntg_type_cls_code == "1"

    def test_parse_execution_data_large_batch(self):
        """Test parsing large batch (20 × 19 = 380 fields)."""
        data = ["value"] * (20 * 19)

        result = OnmarketBondRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 20


class TestOnmarketBondRealtimeExecutionItem:
    """Test OnmarketBondRealtimeExecutionItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 19 fields."""
        assert len(BOND_EXECUTION_FIELD_NAMES) == 19
        assert len(OnmarketBondRealtimeExecutionItem.model_fields) == 19

    def test_model_validation_from_dict(self, sample_bond_execution_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(BOND_EXECUTION_FIELD_NAMES, sample_bond_execution_data, strict=False))
        item = OnmarketBondRealtimeExecutionItem.model_validate(field_dict)

        assert item.stnd_iscd == "KR103502GA34"
        assert item.stck_prpr == "10050"
        assert item.bond_cntg_ert == "3.500"

    def test_field_names_list_order(self, sample_bond_execution_data):
        """Test that BOND_EXECUTION_FIELD_NAMES order matches model fields."""
        field_dict = dict(zip(BOND_EXECUTION_FIELD_NAMES, sample_bond_execution_data, strict=False))
        item = OnmarketBondRealtimeExecutionItem.model_validate(field_dict)

        # First field
        assert BOND_EXECUTION_FIELD_NAMES[0] == "stnd_iscd"
        assert item.stnd_iscd == "KR103502GA34"

        # Last field
        assert BOND_EXECUTION_FIELD_NAMES[18] == "cntg_type_cls_code"
        assert item.cntg_type_cls_code == "1"


class TestBondExecutionFieldNames:
    """Test BOND_EXECUTION_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 19 entries."""
        assert len(BOND_EXECUTION_FIELD_NAMES) == 19

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in BOND_EXECUTION_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(BOND_EXECUTION_FIELD_NAMES) == len(set(BOND_EXECUTION_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(OnmarketBondRealtimeExecutionItem.model_fields.keys())
        field_names_set = set(BOND_EXECUTION_FIELD_NAMES)
        assert field_names_set == model_fields


# ============================================================
# Bond Orderbook Tests (H0BJASP0)
# ============================================================


@pytest.fixture
def sample_bond_orderbook_data() -> list[str]:
    """Generate sample bond orderbook data (34 fields)."""
    return [
        "KR103502GA34",  # stnd_iscd
        "093000",  # stck_cntg_hour
        "3.500",  # askp_ert1
        "3.510",  # bidp_ert1
        "10050",  # askp1
        "10040",  # bidp1
        "5000",  # askp_rsqn1
        "3000",  # bidp_rsqn1
        "3.490",  # askp_ert2
        "3.520",  # bidp_ert2
        "10060",  # askp2
        "10030",  # bidp2
        "4000",  # askp_rsqn2
        "2500",  # bidp_rsqn2
        "3.480",  # askp_ert3
        "3.530",  # bidp_ert3
        "10070",  # askp3
        "10020",  # bidp3
        "3500",  # askp_rsqn3
        "2000",  # bidp_rsqn3
        "3.470",  # askp_ert4
        "3.540",  # bidp_ert4
        "10080",  # askp4
        "10010",  # bidp4
        "3000",  # askp_rsqn4
        "1500",  # bidp_rsqn4
        "3.460",  # askp_ert5
        "3.550",  # bidp_ert5
        "10090",  # askp5
        "10000",  # bidp5
        "2500",  # askp_rsqn5
        "1000",  # bidp_rsqn5
        "18000",  # total_askp_rsqn
        "10000",  # total_bidp_rsqn
    ]


class TestTrIdOrderbookConstant:
    """Test TR_ID_ORDERBOOK constant."""

    def test_tr_id_orderbook_constant(self):
        """Test TR_ID_ORDERBOOK constant value."""
        assert OnmarketBondRealtimeQuote.TR_ID_ORDERBOOK == "H0BJASP0"


class TestSubscribeBondOrderbook:
    """Test subscribe_orderbook method."""

    @pytest.mark.asyncio
    async def test_subscribe_orderbook_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_orderbook calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_orderbook("KR103502GA34")

        mock_socket_client.subscribe.assert_called_once_with("H0BJASP0", "KR103502GA34")

    @pytest.mark.asyncio
    async def test_subscribe_orderbook_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe_orderbook raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.subscribe_orderbook("KR103502GA34")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestUnsubscribeBondOrderbook:
    """Test unsubscribe_orderbook method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_orderbook_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_orderbook calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_orderbook("KR103502GA34")

        mock_socket_client.unsubscribe.assert_called_once_with("H0BJASP0", "KR103502GA34")

    @pytest.mark.asyncio
    async def test_unsubscribe_orderbook_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe_orderbook raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.unsubscribe_orderbook("KR103502GA34")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestParseBondOrderbookData:
    """Test parse_orderbook_data method."""

    def test_parse_orderbook_data_returns_model(self, sample_bond_orderbook_data):
        """Test that parse_orderbook_data returns list of OnmarketBondRealtimeOrderbookItem."""
        result = OnmarketBondRealtimeQuote.parse_orderbook_data(sample_bond_orderbook_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OnmarketBondRealtimeOrderbookItem)

    def test_parse_orderbook_data_field_values(self, sample_bond_orderbook_data):
        """Test that parsed data has correct field values."""
        result = OnmarketBondRealtimeQuote.parse_orderbook_data(sample_bond_orderbook_data)

        assert result[0].stnd_iscd == "KR103502GA34"
        assert result[0].stck_cntg_hour == "093000"
        assert result[0].askp_ert1 == "3.500"
        assert result[0].bidp_ert1 == "3.510"
        assert result[0].askp1 == "10050"
        assert result[0].bidp1 == "10040"
        assert result[0].askp_rsqn1 == "5000"
        assert result[0].bidp_rsqn1 == "3000"
        assert result[0].askp5 == "10090"
        assert result[0].bidp5 == "10000"
        assert result[0].askp_rsqn5 == "2500"
        assert result[0].bidp_rsqn5 == "1000"
        assert result[0].total_askp_rsqn == "18000"
        assert result[0].total_bidp_rsqn == "10000"

    def test_parse_orderbook_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["KR103502GA34", "093000", "3.500"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_orderbook_data(short_data)

        assert "Expected at least 34 fields, got 3" in str(exc_info.value)

    def test_parse_orderbook_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_orderbook_data([])

        assert "Expected at least 34 fields, got 0" in str(exc_info.value)

    def test_parse_orderbook_data_batched_5_records(self, sample_bond_orderbook_data):
        """Test parsing 5 batched records (5 × 34 = 170 fields)."""
        batched_data = []
        for i in range(5):
            record = sample_bond_orderbook_data.copy()
            # Vary askp1 field to distinguish records
            record[4] = str(10050 + i * 10)
            batched_data.extend(record)

        result = OnmarketBondRealtimeQuote.parse_orderbook_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 5
        for i, item in enumerate(result):
            assert isinstance(item, OnmarketBondRealtimeOrderbookItem)
            assert item.askp1 == str(10050 + i * 10)

    def test_parse_orderbook_data_single_record_with_extra_fields(self, sample_bond_orderbook_data):
        """Test single record with extra fields (34 + 3 = 37 fields) - forward compatibility."""
        data = sample_bond_orderbook_data + ["extra1", "extra2", "extra3"]

        result = OnmarketBondRealtimeQuote.parse_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        # Extra fields should be ignored, first 34 used
        assert result[0].stnd_iscd == "KR103502GA34"
        assert result[0].total_bidp_rsqn == "10000"

    def test_parse_orderbook_data_large_batch(self):
        """Test parsing large batch (20 × 34 = 680 fields)."""
        data = ["value"] * (20 * 34)

        result = OnmarketBondRealtimeQuote.parse_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 20


class TestOnmarketBondRealtimeOrderbookItem:
    """Test OnmarketBondRealtimeOrderbookItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 34 fields."""
        assert len(BOND_ORDERBOOK_FIELD_NAMES) == 34
        assert len(OnmarketBondRealtimeOrderbookItem.model_fields) == 34

    def test_model_validation_from_dict(self, sample_bond_orderbook_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(BOND_ORDERBOOK_FIELD_NAMES, sample_bond_orderbook_data, strict=False))
        item = OnmarketBondRealtimeOrderbookItem.model_validate(field_dict)

        assert item.stnd_iscd == "KR103502GA34"
        assert item.askp1 == "10050"
        assert item.total_askp_rsqn == "18000"


class TestBondOrderbookFieldNames:
    """Test BOND_ORDERBOOK_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 34 entries."""
        assert len(BOND_ORDERBOOK_FIELD_NAMES) == 34

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(BOND_ORDERBOOK_FIELD_NAMES) == len(set(BOND_ORDERBOOK_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(OnmarketBondRealtimeOrderbookItem.model_fields.keys())
        field_names_set = set(BOND_ORDERBOOK_FIELD_NAMES)
        assert field_names_set == model_fields


# ============================================================
# Bond Index Execution Tests (H0BICNT0)
# ============================================================


@pytest.fixture
def sample_bond_index_execution_data() -> list[str]:
    """Generate sample bond index execution data (20 fields)."""
    return [
        "BOND_IDX_001",  # nmix_id
        "20240101",  # stnd_date1
        "093000",  # trnm_hour
        "1050.25",  # totl_ernn_nmix_oprc
        "1055.80",  # totl_ernn_nmix_hgpr
        "1048.10",  # totl_ernn_nmix_lwpr
        "1052.50",  # totl_ernn_nmix
        "1050.00",  # prdy_totl_ernn_nmix
        "2.50",  # totl_ernn_nmix_prdy_vrss
        "2",  # totl_ernn_nmix_prdy_vrss_sign
        "0.24",  # totl_ernn_nmix_prdy_ctrt
        "980.30",  # clen_prc_nmix
        "990.50",  # mrkt_prc_nmix
        "1010.20",  # bond_call_rnvs_nmix
        "1005.80",  # bond_zero_rnvs_nmix
        "105.25",  # bond_futs_thpr
        "5.230",  # bond_avrg_drtn_val
        "0.350",  # bond_avrg_cnvx_val
        "3.450",  # bond_avrg_ytm_val
        "3.520",  # bond_avrg_frdl_ytm_val
    ]


class TestSubscribeBondIndexExecution:
    """Test subscribe_index_execution method."""

    @pytest.mark.asyncio
    async def test_subscribe_index_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_index_execution calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_index_execution("BOND_IDX_001")

        mock_socket_client.subscribe.assert_called_once_with("H0BICNT0", "BOND_IDX_001")

    @pytest.mark.asyncio
    async def test_subscribe_index_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that subscribe_index_execution raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.subscribe_index_execution("BOND_IDX_001")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestUnsubscribeBondIndexExecution:
    """Test unsubscribe_index_execution method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_index_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_index_execution calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_index_execution("BOND_IDX_001")

        mock_socket_client.unsubscribe.assert_called_once_with("H0BICNT0", "BOND_IDX_001")

    @pytest.mark.asyncio
    async def test_unsubscribe_index_execution_raises_error_in_dev_env(self, mock_socket_client_dev):
        """Test that unsubscribe_index_execution raises ValueError in dev environment."""
        realtime_quote = OnmarketBondRealtimeQuote(mock_socket_client_dev)

        with pytest.raises(ValueError) as exc_info:
            await realtime_quote.unsubscribe_index_execution("BOND_IDX_001")

        assert "운영 서버(prod)에서만 사용 가능" in str(exc_info.value)
        assert "dev" in str(exc_info.value)


class TestParseBondIndexExecutionData:
    """Test parse_index_execution_data method."""

    def test_parse_index_execution_data_returns_model(self, sample_bond_index_execution_data):
        """Test that parse_index_execution_data returns list of OnmarketBondIndexRealtimeExecutionItem."""
        result = OnmarketBondRealtimeQuote.parse_index_execution_data(sample_bond_index_execution_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], OnmarketBondIndexRealtimeExecutionItem)

    def test_parse_index_execution_data_field_values(self, sample_bond_index_execution_data):
        """Test that parsed data has correct field values."""
        result = OnmarketBondRealtimeQuote.parse_index_execution_data(sample_bond_index_execution_data)

        assert result[0].nmix_id == "BOND_IDX_001"
        assert result[0].stnd_date1 == "20240101"
        assert result[0].trnm_hour == "093000"
        assert result[0].totl_ernn_nmix_oprc == "1050.25"
        assert result[0].totl_ernn_nmix_hgpr == "1055.80"
        assert result[0].totl_ernn_nmix_lwpr == "1048.10"
        assert result[0].totl_ernn_nmix == "1052.50"
        assert result[0].prdy_totl_ernn_nmix == "1050.00"
        assert result[0].totl_ernn_nmix_prdy_vrss == "2.50"
        assert result[0].totl_ernn_nmix_prdy_vrss_sign == "2"
        assert result[0].totl_ernn_nmix_prdy_ctrt == "0.24"
        assert result[0].clen_prc_nmix == "980.30"
        assert result[0].mrkt_prc_nmix == "990.50"
        assert result[0].bond_call_rnvs_nmix == "1010.20"
        assert result[0].bond_zero_rnvs_nmix == "1005.80"
        assert result[0].bond_futs_thpr == "105.25"
        assert result[0].bond_avrg_drtn_val == "5.230"
        assert result[0].bond_avrg_cnvx_val == "0.350"
        assert result[0].bond_avrg_ytm_val == "3.450"
        assert result[0].bond_avrg_frdl_ytm_val == "3.520"

    def test_parse_index_execution_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["BOND_IDX_001", "20240101", "093000"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_index_execution_data(short_data)

        assert "Expected at least 20 fields, got 3" in str(exc_info.value)

    def test_parse_index_execution_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            OnmarketBondRealtimeQuote.parse_index_execution_data([])

        assert "Expected at least 20 fields, got 0" in str(exc_info.value)

    def test_parse_index_execution_data_batched_5_records(self, sample_bond_index_execution_data):
        """Test parsing 5 batched records (5 × 20 = 100 fields)."""
        batched_data = []
        for i in range(5):
            record = sample_bond_index_execution_data.copy()
            # Vary totl_ernn_nmix field to distinguish records
            record[6] = str(1052.50 + i * 10)
            batched_data.extend(record)

        result = OnmarketBondRealtimeQuote.parse_index_execution_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 5
        for i, item in enumerate(result):
            assert isinstance(item, OnmarketBondIndexRealtimeExecutionItem)
            assert item.totl_ernn_nmix == str(1052.50 + i * 10)

    def test_parse_index_execution_data_single_record_with_extra_fields(self, sample_bond_index_execution_data):
        """Test single record with extra fields (20 + 3 = 23 fields) - forward compatibility."""
        data = sample_bond_index_execution_data + ["extra1", "extra2", "extra3"]

        result = OnmarketBondRealtimeQuote.parse_index_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        # Extra fields should be ignored, first 20 used
        assert result[0].nmix_id == "BOND_IDX_001"
        assert result[0].bond_avrg_frdl_ytm_val == "3.520"

    def test_parse_index_execution_data_large_batch(self):
        """Test parsing large batch (20 × 20 = 400 fields)."""
        data = ["value"] * (20 * 20)

        result = OnmarketBondRealtimeQuote.parse_index_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 20


class TestOnmarketBondIndexRealtimeExecutionItem:
    """Test OnmarketBondIndexRealtimeExecutionItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 20 fields."""
        assert len(BOND_INDEX_EXECUTION_FIELD_NAMES) == 20
        assert len(OnmarketBondIndexRealtimeExecutionItem.model_fields) == 20

    def test_model_validation_from_dict(self, sample_bond_index_execution_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(BOND_INDEX_EXECUTION_FIELD_NAMES, sample_bond_index_execution_data, strict=False))
        item = OnmarketBondIndexRealtimeExecutionItem.model_validate(field_dict)

        assert item.nmix_id == "BOND_IDX_001"
        assert item.totl_ernn_nmix == "1052.50"
        assert item.bond_avrg_ytm_val == "3.450"

    def test_field_names_list_order(self, sample_bond_index_execution_data):
        """Test that BOND_INDEX_EXECUTION_FIELD_NAMES order matches model fields."""
        field_dict = dict(zip(BOND_INDEX_EXECUTION_FIELD_NAMES, sample_bond_index_execution_data, strict=False))
        item = OnmarketBondIndexRealtimeExecutionItem.model_validate(field_dict)

        # First field
        assert BOND_INDEX_EXECUTION_FIELD_NAMES[0] == "nmix_id"
        assert item.nmix_id == "BOND_IDX_001"

        # Last field
        assert BOND_INDEX_EXECUTION_FIELD_NAMES[19] == "bond_avrg_frdl_ytm_val"
        assert item.bond_avrg_frdl_ytm_val == "3.520"


class TestBondIndexExecutionFieldNames:
    """Test BOND_INDEX_EXECUTION_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 20 entries."""
        assert len(BOND_INDEX_EXECUTION_FIELD_NAMES) == 20

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in BOND_INDEX_EXECUTION_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(BOND_INDEX_EXECUTION_FIELD_NAMES) == len(set(BOND_INDEX_EXECUTION_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(OnmarketBondIndexRealtimeExecutionItem.model_fields.keys())
        field_names_set = set(BOND_INDEX_EXECUTION_FIELD_NAMES)
        assert field_names_set == model_fields
