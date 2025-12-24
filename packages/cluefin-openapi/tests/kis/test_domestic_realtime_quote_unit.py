"""Unit tests for KIS DomesticRealtimeQuote module."""

from unittest.mock import AsyncMock, Mock

import pytest

from cluefin_openapi.kis._domestic_realtime_quote import DomesticRealtimeQuote
from cluefin_openapi.kis._domestic_realtime_quote_types import (
    EXECUTION_FIELD_NAMES,
    DomesticRealtimeExecutionItem,
)
from cluefin_openapi.kis._socket_client import SocketClient


@pytest.fixture
def mock_socket_client() -> Mock:
    """Create mock SocketClient for testing."""
    client = Mock(spec=SocketClient)
    client.subscribe = AsyncMock()
    client.unsubscribe = AsyncMock()
    return client


@pytest.fixture
def realtime_quote(mock_socket_client) -> DomesticRealtimeQuote:
    """Create DomesticRealtimeQuote instance for testing."""
    return DomesticRealtimeQuote(mock_socket_client)


@pytest.fixture
def sample_execution_data() -> list[str]:
    """Generate sample execution data (46 fields)."""
    return [
        "005930",  # mksc_shrn_iscd
        "093000",  # stck_cntg_hour
        "70000",  # stck_prpr
        "2",  # prdy_vrss_sign
        "1000",  # prdy_vrss
        "1.45",  # prdy_ctrt
        "69500",  # wghn_avrg_stck_prc
        "69000",  # stck_oprc
        "70500",  # stck_hgpr
        "68500",  # stck_lwpr
        "70100",  # askp1
        "70000",  # bidp1
        "100",  # cntg_vol
        "5000000",  # acml_vol
        "350000000000",  # acml_tr_pbmn
        "1234",  # seln_cntg_csnu
        "1456",  # shnu_cntg_csnu
        "222",  # ntby_cntg_csnu
        "118.00",  # cttr
        "2500000",  # seln_cntg_smtn
        "2950000",  # shnu_cntg_smtn
        "1",  # cntg_cls_code
        "54.12",  # shnu_rate
        "110.50",  # prdy_vol_vrss_acml_vol_rate
        "090000",  # oprc_hour
        "2",  # oprc_vrss_prpr_sign
        "1000",  # oprc_vrss_prpr
        "091530",  # hgpr_hour
        "2",  # hgpr_vrss_prpr_sign
        "-500",  # hgpr_vrss_prpr
        "093500",  # lwpr_hour
        "5",  # lwpr_vrss_prpr_sign
        "1500",  # lwpr_vrss_prpr
        "20251224",  # bsop_date
        "20",  # new_mkop_cls_code
        "N",  # trht_yn
        "50000",  # askp_rsqn1
        "45000",  # bidp_rsqn1
        "500000",  # total_askp_rsqn
        "450000",  # total_bidp_rsqn
        "0.83",  # vol_tnrt
        "4500000",  # prdy_smns_hour_acml_vol
        "111.11",  # prdy_smns_hour_acml_vol_rate
        "0",  # hour_cls_code
        "0",  # mrkt_trtm_cls_code
        "68000",  # vi_stnd_prc
    ]


class TestDomesticRealtimeQuoteInit:
    """Test DomesticRealtimeQuote initialization."""

    def test_init_with_socket_client(self, mock_socket_client):
        """Test initialization with SocketClient."""
        quote = DomesticRealtimeQuote(mock_socket_client)
        assert quote.socket_client is mock_socket_client

    def test_tr_id_constant(self):
        """Test TR_ID_EXECUTION constant value."""
        assert DomesticRealtimeQuote.TR_ID_EXECUTION == "H0UNCNT0"


class TestSubscribeExecution:
    """Test subscribe_execution method."""

    @pytest.mark.asyncio
    async def test_subscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_execution calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_execution("005930")

        mock_socket_client.subscribe.assert_called_once_with("H0UNCNT0", "005930")

    @pytest.mark.asyncio
    async def test_subscribe_execution_different_stock_codes(self, realtime_quote, mock_socket_client):
        """Test subscription with different stock codes."""
        await realtime_quote.subscribe_execution("000660")  # SK Hynix
        mock_socket_client.subscribe.assert_called_with("H0UNCNT0", "000660")

        await realtime_quote.subscribe_execution("035720")  # Kakao
        mock_socket_client.subscribe.assert_called_with("H0UNCNT0", "035720")


class TestUnsubscribeExecution:
    """Test unsubscribe_execution method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_execution_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_execution calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_execution("005930")

        mock_socket_client.unsubscribe.assert_called_once_with("H0UNCNT0", "005930")


class TestParseExecutionData:
    """Test parse_execution_data method."""

    def test_parse_execution_data_returns_model(self, sample_execution_data):
        """Test that parse_execution_data returns DomesticRealtimeExecutionItem."""
        result = DomesticRealtimeQuote.parse_execution_data(sample_execution_data)
        assert isinstance(result, DomesticRealtimeExecutionItem)

    def test_parse_execution_data_field_values(self, sample_execution_data):
        """Test that parsed data has correct field values."""
        result = DomesticRealtimeQuote.parse_execution_data(sample_execution_data)

        assert result.mksc_shrn_iscd == "005930"
        assert result.stck_cntg_hour == "093000"
        assert result.stck_prpr == "70000"
        assert result.prdy_vrss_sign == "2"
        assert result.prdy_vrss == "1000"
        assert result.prdy_ctrt == "1.45"
        assert result.acml_vol == "5000000"
        assert result.cttr == "118.00"
        assert result.bsop_date == "20251224"
        assert result.trht_yn == "N"
        assert result.vi_stnd_prc == "68000"

    def test_parse_execution_data_wrong_field_count_raises_error(self):
        """Test that wrong field count raises ValueError."""
        short_data = ["005930", "093000", "70000"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_execution_data(short_data)

        assert "Expected 46 fields, got 3" in str(exc_info.value)

    def test_parse_execution_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_execution_data([])

        assert "Expected 46 fields, got 0" in str(exc_info.value)

    def test_parse_execution_data_too_many_fields_raises_error(self):
        """Test that too many fields raises ValueError."""
        long_data = ["value"] * 50  # 50 fields instead of 46

        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_execution_data(long_data)

        assert "Expected 46 fields, got 50" in str(exc_info.value)


class TestDomesticRealtimeExecutionItem:
    """Test DomesticRealtimeExecutionItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 46 fields."""
        assert len(EXECUTION_FIELD_NAMES) == 46
        assert len(DomesticRealtimeExecutionItem.model_fields) == 46

    def test_model_validation_from_dict(self, sample_execution_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(EXECUTION_FIELD_NAMES, sample_execution_data, strict=False))
        item = DomesticRealtimeExecutionItem.model_validate(field_dict)

        assert item.mksc_shrn_iscd == "005930"
        assert item.stck_prpr == "70000"

    def test_field_names_list_order(self, sample_execution_data):
        """Test that EXECUTION_FIELD_NAMES order matches model fields."""
        field_dict = dict(zip(EXECUTION_FIELD_NAMES, sample_execution_data, strict=False))
        item = DomesticRealtimeExecutionItem.model_validate(field_dict)

        # First field
        assert EXECUTION_FIELD_NAMES[0] == "mksc_shrn_iscd"
        assert item.mksc_shrn_iscd == "005930"

        # Last field
        assert EXECUTION_FIELD_NAMES[45] == "vi_stnd_prc"
        assert item.vi_stnd_prc == "68000"


class TestExecutionFieldNames:
    """Test EXECUTION_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 46 entries."""
        assert len(EXECUTION_FIELD_NAMES) == 46

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in EXECUTION_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(EXECUTION_FIELD_NAMES) == len(set(EXECUTION_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(DomesticRealtimeExecutionItem.model_fields.keys())
        field_names_set = set(EXECUTION_FIELD_NAMES)
        assert field_names_set == model_fields
