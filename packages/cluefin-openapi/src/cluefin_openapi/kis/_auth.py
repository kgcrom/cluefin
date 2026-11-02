import logging
from typing import Literal

import requests
from pydantic import SecretStr

from cluefin_openapi.kis._auth_types import (
    ApprovalResponse,
    TokenResponse,
)
from cluefin_openapi.kis._exceptions import KISAPIError, KISAuthenticationError, KISRateLimitError
from cluefin_openapi.kis._token_manager import TokenManager

logger = logging.getLogger(__name__)

# 토큰 발급은 서버가 1분에 1회로 막는다. 같은 403 이지만 키 문제가 아니다.
_TOKEN_RATE_LIMIT_CODE = "EGW00133"


def _token_error(response: requests.Response) -> KISAPIError | None:
    """토큰 발급 401·403 을 키 오류(EGW00103 AppKey, EGW00105 AppSecret 등)나 발급 제한으로 바꾼다. 그 밖은 None."""
    if response.status_code not in (401, 403):
        return None
    try:
        body = response.json()
    except ValueError:
        body = None
    body = body if isinstance(body, dict) else {}
    code = body.get("error_code")
    description = body.get("error_description") or response.reason
    response_data = {key: body[key] for key in ("error_code", "error_description") if key in body}
    message = f"Token generation failed: {code} {description}" if code else f"Token generation failed: {description}"
    if code == _TOKEN_RATE_LIMIT_CODE:
        return KISRateLimitError(message, response.status_code, response_data, retry_after=60)
    return KISAuthenticationError(message, response.status_code, response_data)


class Auth:
    def __init__(
        self,
        app_key: str,
        secret_key: SecretStr,
        env: Literal["dev", "prod"] = "dev",
        cache_dir: str | None = None,
        token_manager: TokenManager | None = None,
    ) -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.env = env
        self.token_manager = token_manager or TokenManager(cache_dir=cache_dir, env=env, app_key=app_key)
        self._token_data: TokenResponse | None = None

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
            token_error = _token_error(response)
            if token_error is None:
                raise
            raise token_error from e

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
