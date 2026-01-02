"""Unit tests for KIS DomesticRealtimeQuote module."""

from unittest.mock import AsyncMock, Mock

import pytest

from cluefin_openapi.kis._domestic_realtime_quote import DomesticRealtimeQuote
from cluefin_openapi.kis._domestic_realtime_quote_types import (
    EXECUTION_FIELD_NAMES,
    ORDERBOOK_FIELD_NAMES,
    DomesticRealtimeExecutionItem,
    DomesticRealtimeOrderbookItem,
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
        """Test that parse_execution_data returns list of DomesticRealtimeExecutionItem."""
        result = DomesticRealtimeQuote.parse_execution_data(sample_execution_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], DomesticRealtimeExecutionItem)

    def test_parse_execution_data_field_values(self, sample_execution_data):
        """Test that parsed data has correct field values."""
        result = DomesticRealtimeQuote.parse_execution_data(sample_execution_data)

        assert result[0].mksc_shrn_iscd == "005930"
        assert result[0].stck_cntg_hour == "093000"
        assert result[0].stck_prpr == "70000"
        assert result[0].prdy_vrss_sign == "2"
        assert result[0].prdy_vrss == "1000"
        assert result[0].prdy_ctrt == "1.45"
        assert result[0].acml_vol == "5000000"
        assert result[0].cttr == "118.00"
        assert result[0].bsop_date == "20251224"
        assert result[0].trht_yn == "N"
        assert result[0].vi_stnd_prc == "68000"

    def test_parse_execution_data_insufficient_fields_raises_error(self):
        """Test that insufficient fields raises ValueError."""
        short_data = ["005930", "093000", "70000"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_execution_data(short_data)

        assert "Expected at least 46 fields, got 3" in str(exc_info.value)

    def test_parse_execution_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_execution_data([])

        assert "Expected at least 46 fields, got 0" in str(exc_info.value)

    def test_parse_execution_data_batched_12_records(self, sample_execution_data):
        """Test parsing 12 batched records (12 × 46 = 552 fields)."""
        batched_data = []
        for i in range(12):
            record = sample_execution_data.copy()
            # Vary price field to distinguish records
            record[2] = str(70000 + i * 100)
            batched_data.extend(record)

        result = DomesticRealtimeQuote.parse_execution_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 12
        for i, item in enumerate(result):
            assert isinstance(item, DomesticRealtimeExecutionItem)
            assert item.stck_prpr == str(70000 + i * 100)

    def test_parse_execution_data_single_record_with_extra_fields(self, sample_execution_data):
        """Test single record with extra fields (46 + 3 = 49 fields) - forward compatibility."""
        data = sample_execution_data + ["extra1", "extra2", "extra3"]

        result = DomesticRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        # Extra fields should be ignored, first 46 used
        assert result[0].mksc_shrn_iscd == "005930"
        assert result[0].vi_stnd_prc == "68000"

    def test_parse_execution_data_large_batch(self):
        """Test parsing large batch (50 × 46 = 2300 fields)."""
        data = ["value"] * (50 * 46)

        result = DomesticRealtimeQuote.parse_execution_data(data)

        assert isinstance(result, list)
        assert len(result) == 50


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


# ===== Orderbook Tests =====


@pytest.fixture
def sample_orderbook_data() -> list[str]:
    """Generate sample orderbook data (59 fields)."""
    return [
        "005930",  # mksc_shrn_iscd
        "093000",  # bsop_hour
        "0",  # hour_cls_code
        "70100",  # askp1
        "70200",  # askp2
        "70300",  # askp3
        "70400",  # askp4
        "70500",  # askp5
        "70600",  # askp6
        "70700",  # askp7
        "70800",  # askp8
        "70900",  # askp9
        "71000",  # askp10
        "70000",  # bidp1
        "69900",  # bidp2
        "69800",  # bidp3
        "69700",  # bidp4
        "69600",  # bidp5
        "69500",  # bidp6
        "69400",  # bidp7
        "69300",  # bidp8
        "69200",  # bidp9
        "69100",  # bidp10
        "10000",  # askp_rsqn1
        "20000",  # askp_rsqn2
        "30000",  # askp_rsqn3
        "40000",  # askp_rsqn4
        "50000",  # askp_rsqn5
        "60000",  # askp_rsqn6
        "70000",  # askp_rsqn7
        "80000",  # askp_rsqn8
        "90000",  # askp_rsqn9
        "100000",  # askp_rsqn10
        "15000",  # bidp_rsqn1
        "25000",  # bidp_rsqn2
        "35000",  # bidp_rsqn3
        "45000",  # bidp_rsqn4
        "55000",  # bidp_rsqn5
        "65000",  # bidp_rsqn6
        "75000",  # bidp_rsqn7
        "85000",  # bidp_rsqn8
        "95000",  # bidp_rsqn9
        "105000",  # bidp_rsqn10
        "550000",  # total_askp_rsqn
        "600000",  # total_bidp_rsqn
        "1000",  # ovtm_total_askp_rsqn
        "2000",  # ovtm_total_bidp_rsqn
        "70050",  # antc_cnpr
        "5000",  # antc_cnqn
        "10000000",  # antc_vol
        "50",  # antc_cntg_vrss
        "2",  # antc_cntg_vrss_sign
        "0.07",  # antc_cntg_prdy_ctrt
        "5000000",  # acml_vol
        "10000",  # total_askp_rsqn_icdc
        "-5000",  # total_bidp_rsqn_icdc
        "100",  # ovtm_total_askp_icdc
        "-200",  # ovtm_total_bidp_icdc
        "00",  # stck_deal_cls_code
    ]


class TestSubscribeOrderbook:
    """Test subscribe_orderbook method."""

    @pytest.mark.asyncio
    async def test_subscribe_orderbook_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that subscribe_orderbook calls socket_client.subscribe with correct args."""
        await realtime_quote.subscribe_orderbook("005930")

        mock_socket_client.subscribe.assert_called_with("H0STASP0", "005930")

    @pytest.mark.asyncio
    async def test_subscribe_orderbook_different_stock_codes(self, realtime_quote, mock_socket_client):
        """Test subscription with different stock codes."""
        await realtime_quote.subscribe_orderbook("000660")
        mock_socket_client.subscribe.assert_called_with("H0STASP0", "000660")


class TestUnsubscribeOrderbook:
    """Test unsubscribe_orderbook method."""

    @pytest.mark.asyncio
    async def test_unsubscribe_orderbook_calls_socket_client(self, realtime_quote, mock_socket_client):
        """Test that unsubscribe_orderbook calls socket_client.unsubscribe with correct args."""
        await realtime_quote.unsubscribe_orderbook("005930")

        mock_socket_client.unsubscribe.assert_called_once_with("H0STASP0", "005930")


class TestParseOrderbookData:
    """Test parse_orderbook_data method."""

    def test_parse_orderbook_data_returns_model(self, sample_orderbook_data):
        """Test that parse_orderbook_data returns list of DomesticRealtimeOrderbookItem."""
        result = DomesticRealtimeQuote.parse_orderbook_data(sample_orderbook_data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], DomesticRealtimeOrderbookItem)

    def test_parse_orderbook_data_field_values(self, sample_orderbook_data):
        """Test that parsed data has correct field values."""
        result = DomesticRealtimeQuote.parse_orderbook_data(sample_orderbook_data)

        assert result[0].mksc_shrn_iscd == "005930"
        assert result[0].bsop_hour == "093000"
        assert result[0].hour_cls_code == "0"
        assert result[0].askp1 == "70100"
        assert result[0].bidp1 == "70000"
        assert result[0].total_askp_rsqn == "550000"
        assert result[0].total_bidp_rsqn == "600000"
        assert result[0].antc_cnpr == "70050"
        assert result[0].acml_vol == "5000000"

    def test_parse_orderbook_data_wrong_field_count_raises_error(self):
        """Test that wrong field count raises ValueError."""
        short_data = ["005930", "093000", "0"]  # Only 3 fields

        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_orderbook_data(short_data)

        assert "Expected at least 59 fields, got 3" in str(exc_info.value)

    def test_parse_orderbook_data_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            DomesticRealtimeQuote.parse_orderbook_data([])

        assert "Expected at least 59 fields, got 0" in str(exc_info.value)

    def test_parse_orderbook_data_batched_10_records(self, sample_orderbook_data):
        """Test parsing 10 batched orderbook records (10 × 59 = 590 fields)."""
        batched_data = []
        for i in range(10):
            record = sample_orderbook_data.copy()
            # Vary askp1 to distinguish records
            record[3] = str(70100 + i * 10)
            batched_data.extend(record)

        result = DomesticRealtimeQuote.parse_orderbook_data(batched_data)

        assert isinstance(result, list)
        assert len(result) == 10
        for i, item in enumerate(result):
            assert isinstance(item, DomesticRealtimeOrderbookItem)
            assert item.askp1 == str(70100 + i * 10)

    def test_parse_orderbook_data_single_record_with_extra_fields(self, sample_orderbook_data):
        """Test single record with 62 fields (59 + 3 extra) - forward compatibility."""
        # Simulate API returning 62 fields (actual case mentioned in docs)
        data = sample_orderbook_data + ["extra1", "extra2", "extra3"]

        result = DomesticRealtimeQuote.parse_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 1
        # Extra fields should be ignored, first 59 used
        assert result[0].mksc_shrn_iscd == "005930"
        assert result[0].stck_deal_cls_code == "00"

    def test_parse_orderbook_data_batched_with_extra_fields_per_record(self):
        """Test batched records where each has extra fields."""
        # 5 records × 62 fields per record (59 + 3 extras) = 310 total
        # Should parse floor(310 / 59) = 5 complete records
        data = ["value"] * (5 * 62)

        result = DomesticRealtimeQuote.parse_orderbook_data(data)

        assert isinstance(result, list)
        assert len(result) == 5
        assert all(isinstance(item, DomesticRealtimeOrderbookItem) for item in result)


class TestDomesticRealtimeOrderbookItem:
    """Test DomesticRealtimeOrderbookItem Pydantic model."""

    def test_model_field_count(self):
        """Test that model has exactly 59 fields."""
        assert len(ORDERBOOK_FIELD_NAMES) == 59
        assert len(DomesticRealtimeOrderbookItem.model_fields) == 59

    def test_model_validation_from_dict(self, sample_orderbook_data):
        """Test model can be created from dictionary."""
        field_dict = dict(zip(ORDERBOOK_FIELD_NAMES, sample_orderbook_data, strict=False))
        item = DomesticRealtimeOrderbookItem.model_validate(field_dict)

        assert item.mksc_shrn_iscd == "005930"
        assert item.askp1 == "70100"

    def test_field_names_list_order(self, sample_orderbook_data):
        """Test that ORDERBOOK_FIELD_NAMES order matches model fields."""
        field_dict = dict(zip(ORDERBOOK_FIELD_NAMES, sample_orderbook_data, strict=False))
        item = DomesticRealtimeOrderbookItem.model_validate(field_dict)

        # First field
        assert ORDERBOOK_FIELD_NAMES[0] == "mksc_shrn_iscd"
        assert item.mksc_shrn_iscd == "005930"

        # Last field
        assert ORDERBOOK_FIELD_NAMES[58] == "stck_deal_cls_code"
        assert item.stck_deal_cls_code == "00"


class TestOrderbookFieldNames:
    """Test ORDERBOOK_FIELD_NAMES constant."""

    def test_field_names_count(self):
        """Test that field names list has 59 entries."""
        assert len(ORDERBOOK_FIELD_NAMES) == 59

    def test_field_names_all_strings(self):
        """Test that all field names are strings."""
        assert all(isinstance(name, str) for name in ORDERBOOK_FIELD_NAMES)

    def test_field_names_no_duplicates(self):
        """Test that there are no duplicate field names."""
        assert len(ORDERBOOK_FIELD_NAMES) == len(set(ORDERBOOK_FIELD_NAMES))

    def test_field_names_match_model_fields(self):
        """Test that all field names exist in the model."""
        model_fields = set(DomesticRealtimeOrderbookItem.model_fields.keys())
        field_names_set = set(ORDERBOOK_FIELD_NAMES)
        assert field_names_set == model_fields


class TestTrIdConstants:
    """Test TR ID constants."""

    def test_tr_id_execution(self):
        """Test TR_ID_EXECUTION constant."""
        assert DomesticRealtimeQuote.TR_ID_EXECUTION == "H0UNCNT0"

    def test_tr_id_orderbook(self):
        """Test TR_ID_ORDERBOOK constant."""
        assert DomesticRealtimeQuote.TR_ID_ORDERBOOK == "H0STASP0"
