"""Integration tests for KIS Auth module.

These tests require actual API credentials and network access.
They should be run against the sandbox environment for safety.
"""

import pytest
import requests
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._auth_types import ApprovalResponse, TokenResponse


@pytest.mark.integration
def test_generate_token_dev_environment(auth_dev):
    """Test token generation in dev environment."""
    try:
        token_response = auth_dev.generate()

        # Verify response structure
        assert isinstance(token_response, TokenResponse)
        assert hasattr(token_response, "access_token")
        assert hasattr(token_response, "token_type")
        assert hasattr(token_response, "expires_in")
        assert hasattr(token_response, "access_token_token_expired")

        # Verify token content
        assert token_response.access_token is not None
        assert len(token_response.access_token) > 0
        assert token_response.token_type == "Bearer"
        assert token_response.expires_in > 0

    except Exception as e:
        pytest.fail(f"Token generation failed: {e}")


@pytest.mark.integration
def test_token_expiration_information(auth_dev):
    """Test that token expiration information is properly returned."""
    try:
        token_response = auth_dev.generate()

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
        assert hasattr(approval_response, "approval_key")
        assert approval_response.approval_key is not None
        assert len(approval_response.approval_key) > 0
    except Exception as e:
        pytest.fail(f"Approval request failed: {e}")


@pytest.mark.integration
def test_full_auth_workflow_dev_environment(auth_dev):
    """Test complete authentication workflow in dev environment."""
    try:
        # Step 1: Generate or reuse a token while respecting the rate limit.
        token_response = auth_dev.generate()
        assert isinstance(token_response, TokenResponse)
        assert token_response.access_token is not None

        # Step 2: Get approval
        approval_response = auth_dev.approve()
        assert isinstance(approval_response, ApprovalResponse)
        assert approval_response.approval_key is not None

        # Step 3: Revoke token
        revoke_result = auth_dev.revoke()
        assert revoke_result is True
        auth_dev.token_manager.clear_cache()

    except Exception as e:
        pytest.fail(f"Full auth workflow failed: {e}")


@pytest.mark.integration
def test_invalid_credentials_handling():
    """Test handling of invalid credentials."""
    from cluefin_openapi.kis._token_manager import TokenManager

    # Create a custom TokenManager that doesn't use cache to ensure we test the actual API call
    custom_token_manager = TokenManager()
    custom_token_manager._token_cache = None  # Clear any cached token
    invalid_auth = Auth(
        "invalid_app_key",
        SecretStr("invalid_secret_key"),
        env="dev",
        token_manager=custom_token_manager,
    )

    # Should raise an HTTP error for unauthorized access
    with pytest.raises(requests.HTTPError):
        invalid_auth.generate()
