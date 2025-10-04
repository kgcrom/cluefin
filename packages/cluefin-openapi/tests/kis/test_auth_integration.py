"""Integration tests for KIS Auth module.

These tests require actual API credentials and network access.
They should be run against the sandbox environment for safety.
"""

import os
import time
from typing import Optional

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._auth_types import ApprovalResponse, TokenResponse


class _TokenProvider:
    """Cache tokens to avoid triggering the 1 minute rate limit."""

    def __init__(self, auth: Auth, min_interval: int = 65) -> None:
        self._auth = auth
        self._min_interval = min_interval
        self._token: Optional[TokenResponse] = None
        self._last_generated_at: float = 0.0

    def get(self, force_refresh: bool = False) -> TokenResponse:
        if force_refresh:
            self.clear()

        if self._token is not None:
            return self._token

        now = time.monotonic()
        if self._last_generated_at and now - self._last_generated_at < self._min_interval:
            time.sleep(self._min_interval - (now - self._last_generated_at))

        self._token = self._auth.generate()
        self._last_generated_at = time.monotonic()
        return self._token

    def clear(self) -> None:
        self._token = None



@pytest.fixture(scope="module")
def auth_dev():
    """Fixture to create Auth instance for dev environment."""
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("KIS_APP_KEY")
    secret_key = os.getenv("KIS_SECRET_KEY")
    
    if not app_key or not secret_key:
        pytest.skip("KIS API credentials not available in environment variables")
    

    return Auth(
        app_key=app_key,
        secret_key=SecretStr(secret_key),
        env="dev"
    )


@pytest.fixture(scope="module")
def token_provider(auth_dev):
    provider = _TokenProvider(auth_dev)
    yield provider
    provider.clear()

@pytest.mark.integration
def test_generate_token_dev_environment(auth_dev, token_provider):
    """Test token generation in dev environment."""
    try:
        token_response = token_provider.get()
        
        # Verify response structure
        assert isinstance(token_response, TokenResponse)
        assert hasattr(token_response, 'access_token')
        assert hasattr(token_response, 'token_type')
        assert hasattr(token_response, 'expires_in')
        assert hasattr(token_response, 'access_token_token_expired')
        
        # Verify token content
        assert token_response.access_token is not None
        assert len(token_response.access_token) > 0
        assert token_response.token_type == "Bearer"
        assert token_response.expires_in > 0
        
        # Verify token is stored in instance
        assert auth_dev._token_data == token_response

    except Exception as e:
        pytest.fail(f"Token generation failed: {e}")


@pytest.mark.integration
def test_token_expiration_information(auth_dev, token_provider):
    """Test that token expiration information is properly returned."""
    try:
        token_response = token_provider.get()

        # Verify expiration fields are present and valid
        assert token_response.expires_in > 0
        assert token_response.access_token_token_expired is not None
        assert len(token_response.access_token_token_expired) > 0

        # The expiration string should contain date/time information
        # Format is typically "YYYY-MM-DD HH:MM:SS"
        assert "-" in token_response.access_token_token_expired
        assert ":" in token_response.access_token_token_expired

    except Exception as e:
        pytest.fail(f"Token expiration test failed: {e}")


@pytest.mark.integration
def test_approval_request_dev_environment(auth_dev):
    """Test approval request in dev environment."""
    try:
        approval_response = auth_dev.approve()
        
        # Verify response structure
        assert isinstance(approval_response, ApprovalResponse)
        assert hasattr(approval_response, 'approval_key')
        assert approval_response.approval_key is not None
        assert len(approval_response.approval_key) > 0
    except Exception as e:
        pytest.fail(f"Approval request failed: {e}")

@pytest.mark.integration
def test_full_auth_workflow_dev_environment(auth_dev, token_provider):
    """Test complete authentication workflow in dev environment."""
    try:
        # Step 1: Generate or reuse a token while respecting the rate limit.
        token_response = token_provider.get()
        assert isinstance(token_response, TokenResponse)
        assert token_response.access_token is not None

        # Step 2: Get approval
        approval_response = auth_dev.approve()
        assert isinstance(approval_response, ApprovalResponse)
        assert approval_response.approval_key is not None

        # Step 3: Revoke token
        revoke_result = auth_dev.revoke()
        assert revoke_result is True
        token_provider.clear()

    except Exception as e:
        pytest.fail(f"Full auth workflow failed: {e}")

@pytest.mark.integration
def test_invalid_credentials_handling():
    """Test handling of invalid credentials."""
    invalid_auth = Auth(
        "invalid_app_key",
        SecretStr("invalid_secret_key"),
        env="dev"
    )
    
    # Should raise an HTTP error for unauthorized access
    with pytest.raises(Exception):  # Could be HTTPError or other API error
        invalid_auth.generate()
