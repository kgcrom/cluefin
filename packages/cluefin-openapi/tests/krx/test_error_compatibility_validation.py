"""Comprehensive error handling validation for KRX factory refactoring.

This module validates that factory-generated methods maintain identical error handling
behavior compared to original implementations. It tests various failure scenarios
including authentication errors, malformed dates, network timeouts, and server errors
to guarantee backward compatibility.

Requirements addressed: 4.2, 6.4
"""

import pytest
import requests_mock
from requests.exceptions import ConnectionError as RequestsConnectionError, ConnectTimeout, ReadTimeout

from cluefin_openapi.krx._bond_types import BondKoreaTreasuryBondMarket
from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._derivatives_types import DerivativesTradingOfFuturesExcludeStock
from cluefin_openapi.krx._exceptions import (
    KrxAPIError,
    KrxAuthenticationError,
    KrxAuthorizationError,
    KrxClientError,
    KrxServerError,
)
from cluefin_openapi.krx._factory import KrxApiMethodFactory
from cluefin_openapi.krx._index_types import IndexKrx
from cluefin_openapi.krx._stock_types import StockKospi


@pytest.fixture
def client():
    """Create test client instance."""
    return Client(auth_key="test_auth_key")


@pytest.fixture
def factory_stock_method(client):
    """Create factory-generated stock method for testing."""
    return KrxApiMethodFactory.create_single_param_method(
        client=client,
        path_template="/svc/apis/sto/{}",
        endpoint="stk_bydd_trd.json",
        response_model=StockKospi,
        docstring="Test stock method for error validation",
    )


@pytest.fixture
def factory_bond_method(client):
    """Create factory-generated bond method for testing."""
    return KrxApiMethodFactory.create_single_param_method(
        client=client,
        path_template="/svc/apis/bnd/{}",
        endpoint="kts_bydd_trd.json",
        response_model=BondKoreaTreasuryBondMarket,
        docstring="Test bond method for error validation",
    )


@pytest.fixture
def factory_index_method(client):
    """Create factory-generated index method for testing."""
    return KrxApiMethodFactory.create_single_param_method(
        client=client,
        path_template="/svc/apis/idx/{}",
        endpoint="idx_bydd_trd.json",
        response_model=IndexKrx,
        docstring="Test index method for error validation",
    )


@pytest.fixture
def factory_derivatives_method(client):
    """Create factory-generated derivatives method for testing."""
    return KrxApiMethodFactory.create_single_param_method(
        client=client,
        path_template="/svc/apis/drv/{}",
        endpoint="fut_bydd_trd.json",
        response_model=DerivativesTradingOfFuturesExcludeStock,
        docstring="Test derivatives method for error validation",
    )


class TestAuthenticationErrorCompatibility:
    """Test authentication error handling compatibility (401 errors)."""

    def test_401_authentication_error_stock(self, factory_stock_method):
        """Test that factory methods raise identical KrxAuthenticationError for 401 responses."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=401,
                json={"error": "invalid_token", "message": "Invalid or expired authentication token"},
            )

            with pytest.raises(KrxAuthenticationError) as exc_info:
                factory_stock_method("20241201")

            error = exc_info.value
            assert error.status_code == 401
            assert "Authentication failed" in str(error)
            assert error.response_data is not None
            assert error.response_data["error"] == "invalid_token"

    def test_401_authentication_error_bond(self, factory_bond_method):
        """Test authentication error handling for bond methods."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/bnd/kts_bydd_trd.json", status_code=401, text="Unauthorized access"
            )

            with pytest.raises(KrxAuthenticationError) as exc_info:
                factory_bond_method("20241201")

            error = exc_info.value
            assert error.status_code == 401
            assert isinstance(error, KrxAuthenticationError)


class TestAuthorizationErrorCompatibility:
    """Test authorization error handling compatibility (403 errors)."""

    def test_403_authorization_error_index(self, factory_index_method):
        """Test that factory methods raise identical KrxAuthorizationError for 403 responses."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/idx/idx_bydd_trd.json",
                status_code=403,
                json={"error": "access_denied", "message": "Insufficient permissions for this resource"},
            )

            with pytest.raises(KrxAuthorizationError) as exc_info:
                factory_index_method("20241201")

            error = exc_info.value
            assert error.status_code == 403
            assert "Access forbidden" in str(error)
            assert error.response_data is not None
            assert error.response_data["error"] == "access_denied"

    def test_403_authorization_error_derivatives(self, factory_derivatives_method):
        """Test authorization error handling for derivatives methods."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/drv/fut_bydd_trd.json",
                status_code=403,
                text="Forbidden: API access denied",
            )

            with pytest.raises(KrxAuthorizationError) as exc_info:
                factory_derivatives_method("20241201")

            error = exc_info.value
            assert error.status_code == 403
            assert isinstance(error, KrxAuthorizationError)


class TestClientErrorCompatibility:
    """Test client error handling compatibility (4xx errors)."""

    def test_400_bad_request_malformed_date(self, factory_stock_method):
        """Test that factory methods raise identical KrxClientError for malformed dates."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=400,
                json={"error": "invalid_date_format", "message": "Date must be in YYYYMMDD format"},
            )

            with pytest.raises(KrxClientError) as exc_info:
                # Test with invalid date format (not YYYYMMDD)
                factory_stock_method("2024-12-01")  # Wrong format - should be "20241201"

            error = exc_info.value
            assert error.status_code == 400
            assert "Client error" in str(error)
            assert error.response_data is not None
            assert error.response_data["error"] == "invalid_date_format"

    def test_404_not_found_invalid_endpoint(self, factory_bond_method):
        """Test 404 errors for invalid endpoints."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/bnd/kts_bydd_trd.json", status_code=404, text="Endpoint not found"
            )

            with pytest.raises(KrxClientError) as exc_info:
                factory_bond_method("20241201")

            error = exc_info.value
            assert error.status_code == 404
            assert isinstance(error, KrxClientError)

    def test_422_unprocessable_entity_invalid_stock_code(self, factory_stock_method):
        """Test validation errors for invalid Korean stock codes."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=422,
                json={"error": "validation_error", "message": "Invalid Korean stock code format"},
            )

            with pytest.raises(KrxClientError) as exc_info:
                factory_stock_method("20241201")

            error = exc_info.value
            assert error.status_code == 422
            assert "Client error" in str(error)


class TestServerErrorCompatibility:
    """Test server error handling compatibility (5xx errors)."""

    def test_500_internal_server_error(self, factory_index_method):
        """Test that factory methods raise identical KrxServerError for 500 responses."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/idx/idx_bydd_trd.json",
                status_code=500,
                json={"error": "internal_error", "message": "Database connection failed"},
            )

            with pytest.raises(KrxServerError) as exc_info:
                factory_index_method("20241201")

            error = exc_info.value
            assert error.status_code == 500
            assert "Server error" in str(error)
            assert error.response_data is not None
            assert error.response_data["error"] == "internal_error"

    def test_503_service_unavailable(self, factory_derivatives_method):
        """Test service unavailable errors during maintenance."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/drv/fut_bydd_trd.json",
                status_code=503,
                text="Service temporarily unavailable - maintenance in progress",
            )

            with pytest.raises(KrxServerError) as exc_info:
                factory_derivatives_method("20241201")

            error = exc_info.value
            assert error.status_code == 503
            assert isinstance(error, KrxServerError)

    def test_502_bad_gateway(self, factory_stock_method):
        """Test bad gateway errors from upstream services."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=502,
                json={"error": "upstream_error", "message": "Upstream KRX service unavailable"},
            )

            with pytest.raises(KrxServerError) as exc_info:
                factory_stock_method("20241201")

            error = exc_info.value
            assert error.status_code == 502
            assert error.response_data is not None
            assert error.response_data["error"] == "upstream_error"


class TestNetworkErrorCompatibility:
    """Test network-level error handling compatibility."""

    def test_connection_timeout_error(self, factory_bond_method):
        """Test that factory methods handle connection timeouts identically."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/bnd/kts_bydd_trd.json", exc=ConnectTimeout("Connection timed out")
            )

            with pytest.raises(ConnectTimeout):
                factory_bond_method("20241201")

    def test_read_timeout_error(self, factory_index_method):
        """Test read timeout error handling."""
        with requests_mock.Mocker() as m:
            m.get("https://data-dbg.krx.co.kr/svc/apis/idx/idx_bydd_trd.json", exc=ReadTimeout("Read timed out"))

            with pytest.raises(ReadTimeout):
                factory_index_method("20241201")

    def test_connection_error(self, factory_derivatives_method):
        """Test network connection errors."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/drv/fut_bydd_trd.json",
                exc=RequestsConnectionError("Failed to establish connection"),
            )

            with pytest.raises(RequestsConnectionError):
                factory_derivatives_method("20241201")


class TestUnexpectedErrorCompatibility:
    """Test handling of unexpected HTTP status codes."""

    def test_418_teapot_error(self, factory_stock_method):
        """Test that 418 status code (4xx range) raises KrxClientError."""
        with requests_mock.Mocker() as m:
            m.get("https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json", status_code=418, text="I'm a teapot")

            with pytest.raises(KrxClientError) as exc_info:
                factory_stock_method("20241201")

            error = exc_info.value
            assert error.status_code == 418
            assert "Client error" in str(error)
            # Should be a subclass of KrxAPIError but not other specific error types
            assert isinstance(error, KrxAPIError)
            assert not isinstance(error, KrxAuthenticationError)
            assert not isinstance(error, KrxServerError)

    def test_600_unusual_status_code(self, factory_bond_method):
        """Test truly unexpected status codes (outside standard ranges)."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/bnd/kts_bydd_trd.json",
                status_code=600,  # Outside standard HTTP ranges
                text="Unusual status code",
            )

            with pytest.raises(KrxAPIError) as exc_info:
                factory_bond_method("20241201")

            error = exc_info.value
            assert error.status_code == 600
            assert "Unexpected error" in str(error)
            # Should not be a subclass of specific error types
            assert not isinstance(error, KrxAuthenticationError)
            assert not isinstance(error, KrxClientError)
            assert not isinstance(error, KrxServerError)


class TestKoreanParameterErrorCompatibility:
    """Test Korean-specific parameter error handling."""

    def test_korean_date_format_validation_error(self, factory_stock_method):
        """Test Korean date format validation errors."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                status_code=400,
                json={
                    "error": "invalid_bas_dd",
                    "message": "basDd parameter must be in YYYYMMDD format (Korean date standard)",
                    "korean_message": "기준일자는 YYYYMMDD 형식이어야 합니다",
                },
            )

            with pytest.raises(KrxClientError) as exc_info:
                # Test with various invalid Korean date formats
                factory_stock_method("24-12-01")  # Wrong format

            error = exc_info.value
            assert error.status_code == 400
            assert error.response_data is not None
            assert "basDd" in str(error.response_data.get("message", ""))

    def test_korean_market_closed_error(self, factory_index_method):
        """Test Korean market closed error handling."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/svc/apis/idx/idx_bydd_trd.json",
                status_code=422,
                json={
                    "error": "market_closed",
                    "message": "Korean market was closed on the requested date",
                    "korean_message": "요청한 날짜에 한국 시장이 휴장이었습니다",
                },
            )

            with pytest.raises(KrxClientError) as exc_info:
                # Test with a Korean holiday date
                factory_index_method("20241225")  # Christmas Day

            error = exc_info.value
            assert error.status_code == 422
            assert error.response_data is not None
            assert "market_closed" in str(error.response_data.get("error", ""))


class TestErrorMessageConsistency:
    """Test that error messages maintain consistency across modules."""

    def test_error_message_format_consistency(self, client):
        """Test that all factory methods produce consistent error message formats."""
        methods = [
            (StockKospi, "/svc/apis/sto/{}", "stk_bydd_trd.json"),
            (BondKoreaTreasuryBondMarket, "/svc/apis/bnd/{}", "kts_bydd_trd.json"),
            (IndexKrx, "/svc/apis/idx/{}", "idx_bydd_trd.json"),
            (DerivativesTradingOfFuturesExcludeStock, "/svc/apis/drv/{}", "fut_bydd_trd.json"),
        ]

        for response_model, path_template, endpoint in methods:
            method = KrxApiMethodFactory.create_single_param_method(
                client=client,
                path_template=path_template,
                endpoint=endpoint,
                response_model=response_model,
                docstring="Test method",
            )

            with requests_mock.Mocker() as m:
                # All should produce identical error behavior for 401
                m.get(
                    f"https://data-dbg.krx.co.kr{path_template.format(endpoint)}",
                    status_code=401,
                    json={"error": "unauthorized"},
                )

                with pytest.raises(KrxAuthenticationError) as exc_info:
                    method("20241201")

                error = exc_info.value
                assert error.status_code == 401
                assert "Authentication failed" in str(error)
                assert error.response_data is not None
                assert error.response_data["error"] == "unauthorized"

    def test_exception_inheritance_consistency(self, factory_stock_method):
        """Test that exception inheritance hierarchy is preserved."""
        with requests_mock.Mocker() as m:
            m.get("https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json", status_code=401, json={"error": "test"})

            with pytest.raises(Exception) as exc_info:
                factory_stock_method("20241201")

            error = exc_info.value
            # Verify complete inheritance chain
            assert isinstance(error, KrxAuthenticationError)
            assert isinstance(error, KrxAPIError)
            assert isinstance(error, Exception)

    def test_error_attribute_preservation(self, factory_bond_method):
        """Test that all error attributes are preserved identically."""
        test_response_data = {
            "error_code": "AUTH_001",
            "error_message": "Invalid authentication token",
            "korean_message": "인증 토큰이 유효하지 않습니다",
            "timestamp": "2024-12-01T09:00:00Z",
        }

        with requests_mock.Mocker() as m:
            m.get("https://data-dbg.krx.co.kr/svc/apis/bnd/kts_bydd_trd.json", status_code=401, json=test_response_data)

            with pytest.raises(KrxAuthenticationError) as exc_info:
                factory_bond_method("20241201")

            error = exc_info.value
            assert error.status_code == 401
            assert error.response_data == test_response_data
            assert hasattr(error, "message")
            assert hasattr(error, "status_code")
            assert hasattr(error, "response_data")


class TestErrorCompatibilityWithOriginalMethods:
    """Test direct comparison between original and factory methods."""

    def test_side_by_side_error_comparison(self, client):
        """Compare error behavior side-by-side between original and factory methods."""
        # Create factory method
        factory_method = KrxApiMethodFactory.create_single_param_method(
            client=client,
            path_template="/svc/apis/sto/{}",
            endpoint="stk_bydd_trd.json",
            response_model=StockKospi,
            docstring="Test method",
        )

        test_cases = [
            (401, KrxAuthenticationError, {"error": "auth_failed"}),
            (403, KrxAuthorizationError, {"error": "forbidden"}),
            (400, KrxClientError, {"error": "bad_request"}),
            (500, KrxServerError, {"error": "server_error"}),
            (418, KrxAPIError, {"error": "teapot"}),
        ]

        for status_code, expected_exception, response_data in test_cases:
            with requests_mock.Mocker() as m:
                m.get(
                    "https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd.json",
                    status_code=status_code,
                    json=response_data,
                )

                # Test factory method
                with pytest.raises(expected_exception) as factory_exc_info:
                    factory_method("20241201")

                # Test original method (through client.stock.get_kospi)
                with pytest.raises(expected_exception) as original_exc_info:
                    client.stock.get_kospi("20241201")

                # Compare error properties
                factory_error = factory_exc_info.value
                original_error = original_exc_info.value

                assert type(factory_error) is type(original_error)
                assert factory_error.status_code == original_error.status_code
                assert factory_error.response_data == original_error.response_data
                assert str(factory_error) == str(original_error)
