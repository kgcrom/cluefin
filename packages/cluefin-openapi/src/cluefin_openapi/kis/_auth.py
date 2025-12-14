from typing import Literal, Optional

import requests
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi.kis._auth_types import (
    ApprovalResponse,
    TokenResponse,
)
from cluefin_openapi.kis._token_manager import TokenManager


class Auth:
    def __init__(
        self,
        app_key: str,
        secret_key: SecretStr,
        env: Literal["dev", "prod"] = "dev",
        token_manager: Optional[TokenManager] = None,
    ) -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.env = env
        self.token_manager = token_manager or TokenManager()
        self._token_data: Optional[TokenResponse] = None

        if env == "prod":
            self.url = "https://openapi.koreainvestment.com:9443"
        else:
            self.url = "https://openapivts.koreainvestment.com:29443"

    def generate(self) -> TokenResponse:
        """Get cached token or generate a new one if expired.

        Returns:
            TokenResponse: Valid access token
        """
        token = self.token_manager.get_or_generate(self._generate_new_token)
        self._token_data = token
        return token

    def _generate_new_token(self) -> TokenResponse:
        """Generate a new token from KIS API.

        Returns:
            TokenResponse: New access token
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.secret_key.get_secret_value(),
        }

        response = requests.post(f"{self.url}/oauth2/tokenP", headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to generate token: {e}, Response: {response.text}")
            raise

        token_data = TokenResponse(**response.json())
        self._token_data = token_data
        return self._token_data

    def revoke(self) -> bool:
        """Revoke the current access token.

        Returns:
            True if revocation successful

        Raises:
            RuntimeError: If no token has been generated yet
        """
        if self._token_data is None:
            raise RuntimeError("Cannot revoke token: no token has been generated yet")

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }

        data = {
            "appkey": self.app_key,
            "appsecret": self.secret_key.get_secret_value(),
            "token": self._token_data.access_token,
        }

        response = requests.post(f"{self.url}/oauth2/revokeP", headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to revoke token: {e}, Response: {response.text}")
            raise

        return True

    def approve(self) -> ApprovalResponse:
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }

        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.secret_key.get_secret_value(),
        }

        response = requests.post(f"{self.url}/oauth2/Approval", headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to get approval key: {e}, Response: {response.text}")
            raise

        approval_data = ApprovalResponse(**response.json())
        return approval_data
