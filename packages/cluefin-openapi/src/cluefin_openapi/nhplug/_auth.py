from typing import Literal, Optional

import requests
from loguru import logger
from pydantic import SecretStr

from cluefin_openapi.nhplug._auth_types import TokenResponse, TokenRevokeResponse
from cluefin_openapi.nhplug._token_manager import TokenManager

# 접근토큰 발급/폐기는 운영 도메인 전용(모의투자 미제공). 발급받은 토큰은
# 운영·모의투자 호출 모두에 사용하므로 Auth 는 env 를 받지 않는다.
AUTH_BASE_URL = "https://api.nhplug.com:8443"


class Auth:
    def __init__(
        self,
        app_key: str,
        secret_key: SecretStr,
        cache_dir: Optional[str] = None,
        token_manager: Optional[TokenManager] = None,
    ) -> None:
        self.app_key = app_key
        self.secret_key = secret_key
        self.token_manager = token_manager or TokenManager(cache_dir=cache_dir, app_key=app_key)
        self._token_data: Optional[TokenResponse] = None

    def generate(self) -> TokenResponse:
        """Get cached token or generate a new one if expired.

        Returns:
            TokenResponse: Valid access token
        """
        token = self.token_manager.get_or_generate(self._generate_new_token)
        self._token_data = token
        return token

    def _generate_new_token(self) -> TokenResponse:
        """Generate a new token from the NH PLUG API.

        접근토큰발급은 초당 1회로 서버에서 제한되며, 불필요한 재발급은
        계좌 보안 알림을 유발한다 — 반드시 generate()의 캐시 경로를 쓸 것.

        Returns:
            TokenResponse: New access token
        """
        data = {
            "appkey": self.app_key,
            "appsecretkey": self.secret_key.get_secret_value(),
            "grant_type": "client_credentials",
            "scope": "oob",
        }

        response = requests.post(
            f"{AUTH_BASE_URL}/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to generate token: {e}, Response: {response.text}")
            raise

        token_data = TokenResponse(**response.json())
        self._token_data = token_data
        return self._token_data

    def revoke(
        self,
        token: Optional[str] = None,
        token_type_hint: Literal["access_token", "refresh_token"] = "access_token",
    ) -> TokenRevokeResponse:
        """Revoke an access token (`POST /oauth2/revoke`).

        Args:
            token: 폐기할 토큰. 생략하면 현재 보유한 토큰(캐시 포함)을 폐기한다.
            token_type_hint: 토큰 유형 hint.

        Returns:
            TokenRevokeResponse: 폐기 결과 (성공 시 code/message)
        """
        if token is None:
            cached = self._token_data or self.token_manager._token_cache
            if cached is None:
                raise ValueError("No token to revoke: pass `token` explicitly or call generate() first")
            token = cached.access_token

        data = {
            "token": token,
            "token_type_hint": token_type_hint,
            "appkey": self.app_key,
            "appsecretkey": self.secret_key.get_secret_value(),
        }

        response = requests.post(
            f"{AUTH_BASE_URL}/oauth2/revoke",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to revoke token: {e}, Response: {response.text}")
            raise

        result = TokenRevokeResponse(**response.json())

        # 폐기된 토큰이 캐시에 남아 재사용되지 않도록 정리
        if self._token_data is not None and self._token_data.access_token == token:
            self._token_data = None
        cached = self.token_manager._token_cache
        if cached is not None and cached.access_token == token:
            self.token_manager.clear_cache()

        return result
