"""Unit tests for KIS Auth module."""

import pytest
import requests
import requests_mock
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._auth_types import TokenResponse, ApprovalResponse


@pytest.fixture
def dev_auth() -> Auth:
    return Auth("test_app_key", SecretStr("test_secret_key"), env="dev")


def test_generate_success(dev_auth, requests_mock):
    """Test successful token generation."""
    # Mock the API response
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/tokenP",
        json={
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 86400,
            "access_token_token_expired": "2025-10-05 10:00:00"
        }
    )

    result = dev_auth.generate()

    # Verify the response
    assert isinstance(result, TokenResponse)
    assert result.access_token == "test_access_token"
    assert result.token_type == "Bearer"
    assert result.expires_in == 86400
    assert result.access_token_token_expired == "2025-10-05 10:00:00"

    # Verify token is stored in instance
    assert dev_auth._token_data == result


def test_generate_http_error(dev_auth, requests_mock):
    """Test token generation with HTTP error."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/tokenP",
        status_code=401,
        json={"error": "Unauthorized"}
    )

    with pytest.raises(requests.HTTPError):
        dev_auth.generate()


def test_generate_invalid_response_format(dev_auth, requests_mock):
    """Test token generation with invalid response format."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/tokenP",
        json={"invalid": "data"}
    )

    with pytest.raises(Exception):  # Pydantic validation error
        dev_auth.generate()


def test_revoke_success(dev_auth, requests_mock):
    """Test successful token revocation."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/revokeP"
    )

    # Set up token data first
    dev_auth._token_data = TokenResponse(
        access_token="test_token",
        token_type="Bearer",
        expires_in=86400,
        access_token_token_expired="2025-10-05 10:00:00"
    )

    result = dev_auth.revoke()
    assert result is True


def test_revoke_http_error(dev_auth, requests_mock):
    """Test token revocation with HTTP error."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/revokeP",
        status_code=400,
        json={"error": "Bad Request"}
    )

    dev_auth._token_data = TokenResponse(
        access_token="test_token",
        token_type="Bearer",
        expires_in=86400,
        access_token_token_expired="2025-10-05 10:00:00"
    )

    with pytest.raises(requests.HTTPError):
        dev_auth.revoke()


def test_approve_success(dev_auth, requests_mock):
    """Test successful approval request."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/Approval",
        json={"approval_key": "test_approval_key_123456"}
    )

    result = dev_auth.approve()

    # Verify the response
    assert isinstance(result, ApprovalResponse)
    assert result.approval_key == "test_approval_key_123456"


def test_approve_http_error(dev_auth, requests_mock):
    """Test approval request with HTTP error."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/Approval",
        status_code=403,
        json={"error": "Forbidden"}
    )

    with pytest.raises(requests.HTTPError):
        dev_auth.approve()


def test_approve_invalid_response_format(dev_auth, requests_mock):
    """Test approval request with invalid response format."""
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/oauth2/Approval",
        json={"invalid": "data"}
    )

    with pytest.raises(Exception):  # Pydantic validation error
        dev_auth.approve()


def test_secret_key_security(dev_auth):
    """Test that secret key is properly protected."""
    secret_value = "test_secret_key"

    # Secret value should not be visible in string representation
    assert secret_value not in str(dev_auth.secret_key)
    assert secret_value not in repr(dev_auth.secret_key)

    # But should be accessible when needed
    assert dev_auth.secret_key.get_secret_value() == secret_value


def test_prod_vs_dev_url_configuration():
    """Test URL configuration for different environments."""
    dev_auth = Auth("test_app_key", SecretStr("test_secret_key"), env="dev")
    prod_auth = Auth("test_app_key", SecretStr("test_secret_key"), env="prod")

    assert dev_auth.url == "https://openapivts.koreainvestment.com:29443"
    assert prod_auth.url == "https://openapi.koreainvestment.com:9443"
    assert dev_auth.url != prod_auth.url