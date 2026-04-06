"""Authentication module for Kiwoom API.

This module provides functionality for generating and revoking API tokens
using client credentials authentication flow.
"""

from __future__ import annotations

from typing import Literal, Optional

import requests
from pydantic import SecretStr

from ._auth_types import TokenResponse
from ._token_manager import TokenManager


class Auth:
    """Initialize the Auth client.

    Args:
        app_key: The application key provided by Kiwoom.
        secret_key: The secret key provided by Kiwoom.
        env: The environment to use. Either "dev" or "prod".
            Defaults to "dev".

    Raises:
        ValueError: If an invalid environment is provided.
    """

    def __init__(
        self,
        app_key: str,
        secret_key: SecretStr,
        env: Literal["dev", "prod"] = "dev",
        cache_dir: Optional[str] = None,
        token_manager: Optional[TokenManager] = None,
    ) -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.token_manager = token_manager or TokenManager(cache_dir=cache_dir)

        if env == "dev":
            self.url = "https://mockapi.kiwoom.com"
        elif env == "prod":
            self.url = "https://api.kiwoom.com"
        else:
            raise ValueError("Invalid environment. Must be either 'dev' or 'prod'.")

    def generate_token(self) -> TokenResponse:
        """Generate a new access token.

        Calls the Kiwoom OAuth2 token endpoint to generate a new access token
        using the client credentials flow.

        Returns:
            TokenResponse: The generated token data including access token
                and expiration.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        if self.token_manager is not None:
            token = self.token_manager.get_or_generate(self._generate_new_token)
            self._token_data = token
            return token

        return self._generate_new_token()

    def _generate_new_token(self) -> TokenResponse:
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.secret_key.get_secret_value(),
        }

        response = requests.post(f"{self.url}/oauth2/token", headers=headers, json=data)
        response.raise_for_status()

        token_data = TokenResponse(**response.json())
        self._token_data = token_data

        return self._token_data

    def revoke_token(self, token: str) -> bool:
        """Revoke an access token.

        Args:
            token: The token to revoke.
        Returns:
            bool: True if the token was successfully revoked.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }

        data = {"appkey": self.app_key, "secretkey": self.secret_key.get_secret_value(), "token": token}

        response = requests.post(f"{self.url}/oauth2/revoke", headers=headers, json=data)
        response.raise_for_status()

        return True
