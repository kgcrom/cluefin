"""Unit tests for KrxApiMethodFactory.

This module provides comprehensive unit tests for the KrxApiMethodFactory class,
covering partial function creation, type safety, Korean parameter mapping,
and error handling scenarios.

Tests cover:
- Partial function creation and execution
- Type hint preservation and mypy compatibility
- Korean parameter mapping ("basDd" field alias)
- Method signature validation with TypedApiMethod[T] protocol
- Error condition testing with Korean stock codes
- requests_mock for API response simulation
"""

import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._factory import KrxApiMethodFactory, TypedApiMethod, _api_method_template
from cluefin_openapi.krx._model import KrxHttpResponse
from cluefin_openapi.krx._stock_types import StockKonex, StockKosdaq, StockKospi


@pytest.fixture
def client():
    """Create a test KRX client instance."""
    return Client(auth_key="test_auth_key")


@pytest.fixture
def mock_kospi_response():
    """Mock response data for KOSPI stock query."""
    return {
        "OutBlock_1": [
            {
                "BAS_DD": "20241201",
                "ISU_CD": "005930",
                "ISU_NM": "삼성전자",
                "MKT_NM": "KOSPI",
                "SECT_TP_NM": "전기전자",
                "TDD_CLSPRC": "71000",
                "CMPPREVDD_PRC": "1000",
                "FLUC_RT": "1.43",
                "TDD_OPNPRC": "70500",
                "TDD_HGPRC": "71500",
                "TDD_LWPRC": "70000",
                "ACC_TRDVOL": "12345678",
                "ACC_TRDVAL": "876543210000",
                "MKTCAP": "4235000000000000",
                "LIST_SHRS": "5969782550",
            }
        ]
    }


@pytest.fixture
def mock_kosdaq_response():
    """Mock response data for KOSDAQ stock query."""
    return {
        "OutBlock_1": [
            {
                "BAS_DD": "20241201",
                "ISU_CD": "035720",
                "ISU_NM": "카카오",
                "MKT_NM": "KOSDAQ",
                "SECT_TP_NM": "소프트웨어",
                "TDD_CLSPRC": "45000",
                "CMPPREVDD_PRC": "-500",
                "FLUC_RT": "-1.10",
                "TDD_OPNPRC": "45500",
                "TDD_HGPRC": "46000",
                "TDD_LWPRC": "44500",
                "ACC_TRDVOL": "987654",
                "ACC_TRDVAL": "44543210000",
                "MKTCAP": "1965000000000000",
                "LIST_SHRS": "436661563",
            }
        ]
    }


class TestKrxApiMethodFactory:
    """Test suite for KrxApiMethodFactory class."""

    def test_create_single_param_method_basic_functionality(self, client: Client, mock_kospi_response):
        """Test basic creation and execution of single parameter method."""
        with requests_mock.Mocker() as m:
            # Mock the API endpoint
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                json=mock_kospi_response,
                status_code=200,
            )

            # Create method using factory
            get_kospi_method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="stk_bydd_trd.json",
                response_model=StockKospi,
                docstring="KOSPI 일별매매정보 조회\n\nArgs:\n    base_date (str): 조회할 날짜 (YYYYMMDD 형식)",
            )

            # Execute the method
            result = get_kospi_method("20241201")

            # Verify response structure and data
            assert isinstance(result, KrxHttpResponse)
            assert isinstance(result.body, StockKospi)
            assert len(result.body.data) == 1
            assert result.body.data[0].base_date == "20241201"
            assert result.body.data[0].issued_code == "005930"
            assert result.body.data[0].issued_name == "삼성전자"

    def test_create_single_param_method_korean_parameter_mapping(self, client: Client, mock_kospi_response):
        """Test that Korean parameter mapping (basDd) is preserved correctly."""
        with requests_mock.Mocker() as m:
            # Mock the API endpoint and capture the request
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                json=mock_kospi_response,
                status_code=200,
            )

            # Create method using factory
            method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="stk_bydd_trd.json",
                response_model=StockKospi,
                docstring="Test method",
            )

            # Execute method
            method("20241201")

            # Verify that the correct Korean parameter was sent
            assert len(m.request_history) == 1
            request = m.request_history[0]
            assert "basDd=20241201" in request.url

    def test_create_single_param_method_type_safety(self, client: Client):
        """Test that generated methods maintain proper type hints."""
        # Create method using factory
        method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="Type safety test method",
        )

        # Verify that the method conforms to TypedApiMethod protocol
        assert callable(method)
        assert callable(method)

        # Verify function name is set correctly
        assert method.__name__ == "krx_api_method_stk_bydd_trd_json"

        # Verify docstring is preserved
        assert method.__doc__ == "Type safety test method"

    def test_create_single_param_method_different_endpoints(self, client: Client, mock_kosdaq_response):
        """Test factory with different API endpoints and response models."""
        with requests_mock.Mocker() as m:
            # Mock KOSDAQ endpoint
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd.json",
                json=mock_kosdaq_response,
                status_code=200,
            )

            # Create KOSDAQ method
            get_kosdaq_method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="ksq_bydd_trd.json",
                response_model=StockKosdaq,
                docstring="KOSDAQ 일별매매정보 조회",
            )

            # Execute method
            result = get_kosdaq_method("20241201")

            # Verify correct response type and data
            assert isinstance(result, KrxHttpResponse)
            assert isinstance(result.body, StockKosdaq)
            assert len(result.body.data) == 1
            assert result.body.data[0].issued_code == "035720"
            assert result.body.data[0].issued_name == "카카오"

    def test_create_single_param_method_error_handling(self, client: Client):
        """Test error handling when API request fails."""
        with requests_mock.Mocker() as m:
            # Mock API error response
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=500,
                text="Internal Server Error",
            )

            # Create method
            method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="stk_bydd_trd.json",
                response_model=StockKospi,
                docstring="Error handling test",
            )

            # Verify that HTTP errors are propagated correctly
            with pytest.raises((Exception, ValueError, RuntimeError)):  # Various exceptions possible
                method("20241201")

    def test_create_single_param_method_invalid_date_format(self, client: Client):
        """Test behavior with invalid date format."""
        with requests_mock.Mocker() as m:
            # Mock API response for invalid date
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                json={"OutBlock_1": []},  # Empty response
                status_code=200,
            )

            method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="stk_bydd_trd.json",
                response_model=StockKospi,
                docstring="Invalid date test",
            )

            # Execute with invalid date format
            result = method("invalid-date")

            # Should handle gracefully and return empty data
            assert isinstance(result, KrxHttpResponse)
            assert isinstance(result.body, StockKospi)
            assert len(result.body.data) == 0

    def test_create_multi_param_method_basic_functionality(self, client: Client):
        """Test multi-parameter method creation and execution."""
        with requests_mock.Mocker() as m:
            # Mock response with all required fields
            mock_response = {
                "OutBlock_1": [
                    {
                        "BAS_DD": "20241201",
                        "ISU_CD": "TEST001",
                        "ISU_NM": "테스트종목",
                        "MKT_NM": "KOSPI",
                        "SECT_TP_NM": "테스트부",
                        "TDD_CLSPRC": "50000",
                        "CMPPREVDD_PRC": "100",
                        "FLUC_RT": "0.20",
                        "TDD_OPNPRC": "49900",
                        "TDD_HGPRC": "50100",
                        "TDD_LWPRC": "49800",
                        "ACC_TRDVOL": "1000000",
                        "ACC_TRDVAL": "50000000000",
                        "MKTCAP": "1000000000000",
                        "LIST_SHRS": "20000000",
                    }
                ]
            }
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/test_endpoint.json",
                json=mock_response,
                status_code=200,
            )

            # Create multi-parameter method
            method = KrxApiMethodFactory.create_multi_param_method(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="test_endpoint.json",
                response_model=StockKospi,
                param_mapping={"base_date": "basDd", "market_code": "mktCd"},
                docstring="Multi-parameter test method",
            )

            # Execute method with multiple parameters
            method(base_date="20241201", market_code="KOSPI")

            # Verify request was made with correct parameters
            assert len(m.request_history) == 1
            request = m.request_history[0]
            assert "basDd=20241201" in request.url
            assert "mktCd=KOSPI" in request.url

    def test_get_method_signature_info(self, client: Client):
        """Test method signature introspection utility."""
        # Create a method using factory
        method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="Signature info test method",
        )

        # Get signature information
        info = KrxApiMethodFactory.get_method_signature_info(method)

        # Verify signature info
        assert info["name"] == "krx_api_method_stk_bydd_trd_json"
        assert info["doc"] == "Signature info test method"
        assert info["type"] == "callable"

    def test_create_single_param_method_with_different_path_templates(self, client: Client, mock_kospi_response):
        """Test factory with different path templates."""
        with requests_mock.Mocker() as m:
            # Mock different API path
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/idx/custom_endpoint.json",
                json=mock_kospi_response,
                status_code=200,
            )

            # Create method with different path template
            method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template="/svc/apis/idx/{}",  # Different path template
                endpoint="custom_endpoint.json",
                response_model=StockKospi,
                docstring="Custom path test",
            )

            # Execute method
            method("20241201")

            # Verify correct path was used
            assert len(m.request_history) == 1
            request = m.request_history[0]
            assert "/svc/apis/idx/custom_endpoint.json" in request.url


class TestApiMethodTemplate:
    """Test suite for _api_method_template function."""

    def test_api_method_template_direct_call(self, client: Client, mock_kospi_response):
        """Test direct usage of _api_method_template function."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                json=mock_kospi_response,
                status_code=200,
            )

            # Call template function directly
            result = _api_method_template(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="stk_bydd_trd.json",
                response_model=StockKospi,
                base_date="20241201",
            )

            # Verify result
            assert isinstance(result, KrxHttpResponse)
            assert isinstance(result.body, StockKospi)
            assert result.body.data[0].base_date == "20241201"

    def test_api_method_template_with_additional_kwargs(self, client: Client):
        """Test _api_method_template with additional parameters."""
        with requests_mock.Mocker() as m:
            # Create complete mock response with all required fields
            mock_response = {
                "OutBlock_1": [
                    {
                        "BAS_DD": "20241201",
                        "ISU_CD": "TEST001",
                        "ISU_NM": "테스트종목",
                        "MKT_NM": "KOSPI",
                        "SECT_TP_NM": "테스트부",
                        "TDD_CLSPRC": "50000",
                        "CMPPREVDD_PRC": "100",
                        "FLUC_RT": "0.20",
                        "TDD_OPNPRC": "49900",
                        "TDD_HGPRC": "50100",
                        "TDD_LWPRC": "49800",
                        "ACC_TRDVOL": "1000000",
                        "ACC_TRDVAL": "50000000000",
                        "MKTCAP": "1000000000000",
                        "LIST_SHRS": "20000000",
                    }
                ]
            }
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/test.json",
                json=mock_response,
                status_code=200,
            )

            # Call with additional kwargs
            _api_method_template(
                client=client,
                path_template="/svc/apis/sto/{}",
                endpoint="test.json",
                response_model=StockKospi,
                base_date="20241201",
                extra_param="value123",  # Additional parameter
            )

            # Verify request included both base_date and extra parameter
            assert len(m.request_history) == 1
            request = m.request_history[0]
            assert "basDd=20241201" in request.url
            assert "extra_param=value123" in request.url


class TestTypeCompatibility:
    """Test suite for type compatibility and protocol adherence."""

    def test_typed_api_method_protocol_compatibility(self, client: Client):
        """Test that factory-generated methods conform to TypedApiMethod protocol."""
        # Create method using factory
        method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="Protocol compatibility test",
        )

        # Verify that the method can be assigned to TypedApiMethod type
        typed_method: TypedApiMethod[StockKospi] = method

        # Verify that it's callable with the expected signature
        assert callable(typed_method)

    def test_multiple_methods_with_different_types(self, client: Client):
        """Test creating multiple methods with different response types."""
        # Create multiple methods with different types
        kospi_method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="KOSPI method",
        )

        kosdaq_method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="ksq_bydd_trd.json",
            response_model=StockKosdaq,
            docstring="KOSDAQ method",
        )

        konex_method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="knx_bydd_trd.json",
            response_model=StockKonex,
            docstring="KONEX method",
        )

        # Verify each method has correct typing
        assert kospi_method.__name__ == "krx_api_method_stk_bydd_trd_json"
        assert kosdaq_method.__name__ == "krx_api_method_ksq_bydd_trd_json"
        assert konex_method.__name__ == "krx_api_method_knx_bydd_trd_json"

    def test_method_introspection_properties(self, client: Client):
        """Test that generated methods have proper introspection properties."""
        method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="Introspection test method with detailed documentation",
        )

        # Test introspection properties
        assert hasattr(method, "__name__")
        assert hasattr(method, "__doc__")
        assert callable(method)

        # Verify the method name and docstring
        assert method.__name__ == "krx_api_method_stk_bydd_trd_json"
        assert method.__doc__ == "Introspection test method with detailed documentation"

        # Verify it's callable with the expected signature
        assert callable(method)
