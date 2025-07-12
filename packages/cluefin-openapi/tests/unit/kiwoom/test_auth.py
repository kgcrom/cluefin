"""Tests for the Auth class."""

from datetime import datetime

import pytest
import requests
import requests_mock

from cluefin_openapi.kiwoom._auth import Auth
from cluefin_openapi.kiwoom._auth_types import TokenResponse


@pytest.fixture
def auth():
    """Create an Auth instance for testing."""
    return Auth(app_key="test_app_key", secret_key="test_secret_key", env="dev")


def test_generate_token_success(auth):
    """Test successful token generation."""
    expected_token = "test_token"
    expected_token_type = "Bearer"
    expected_expires_dt = "20250614235959"

    response_data = {"token": expected_token, "token_type": expected_token_type, "expires_dt": expected_expires_dt}

    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/oauth2/token", json=response_data, status_code=200)

        token_response = auth.generate_token()

        assert isinstance(token_response, TokenResponse)
        assert token_response.token == expected_token
        assert token_response.token_type == expected_token_type
        assert token_response.expires_dt == datetime.strptime(expected_expires_dt, "%Y%m%d%H%M%S")


def test_generate_token_failure(auth):
    """Test token generation with API error."""
    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/oauth2/token", status_code=401, json={"error": "Invalid credentials"})

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            auth.generate_token()

        assert exc_info.value.response.status_code == 401


def test_revoke_token_success(auth):
    """Test successful token revocation."""
    test_token = "test_token"

    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/oauth2/revoke", status_code=200)

        result = auth.revoke_token(test_token)
        assert result is True


def test_revoke_token_failure(auth):
    """Test token revocation with API error."""
    test_token = "invalid_token"

    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/oauth2/revoke", status_code=400, json={"error": "Invalid token"})

        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            auth.revoke_token(test_token)

        assert exc_info.value.response.status_code == 400
