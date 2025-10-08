from typing import Literal

import requests
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi.kis._auth_types import (
    ApprovalResponse,
    TokenResponse,
)


class Auth:
    def __init__(self, app_key: str, secret_key: SecretStr, env: Literal["dev", "prod"] = "dev") -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.env = env

        if env == "prod":
            self.url = "https://openapi.koreainvestment.com:9443"
        else:
            self.url = "https://openapivts.koreainvestment.com:29443"

    def generate(self) -> TokenResponse:
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
