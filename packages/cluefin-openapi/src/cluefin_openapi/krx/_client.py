from typing import Dict, Optional

import requests

from ._exceptions import (
    KrxAPIError,
    KrxAuthenticationError,
    KrxAuthorizationError,
    KrxClientError,
    KrxServerError,
)


class Client(object):
    def __init__(self, auth_key: str, timeout: int = 30):
        self.auth_key = auth_key
        self.base_url = "http://data-dbg.krx.co.kr"
        self.timeout = timeout

    @property
    def index(self):
        from ._index import Index

        return Index(self)

    @property
    def stock(self):
        from ._stock import Stock

        return Stock(self)

    @property
    def exchange_traded_product(self):
        from ._exchange_traded_product import ExchangeTradedProduct

        return ExchangeTradedProduct(self)

    @property
    def bond(self):
        from ._bond import Bond

        return Bond(self)

    @property
    def derivatives(self):
        from ._derivatives import Derivatives

        return Derivatives(self)

    @property
    def general_product(self):
        from ._general_product import GeneralProduct

        return GeneralProduct(self)

    @property
    def esg(self):
        from ._esg import Esg

        return Esg(self)

    def _get(self, path: str, params: Optional[Dict] = None):
        url = self.base_url + path
        headers = {"AUTH_KEY": self.auth_key, "Accept": "application/json"}

        response = requests.get(url, params=params, headers=headers, timeout=self.timeout)

        # 응답 처리
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                # JSON 파싱 실패시 텍스트 반환
                return response.text
        elif response.status_code == 401:
            raise KrxAuthenticationError(
                "Authentication failed - invalid or expired token",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif response.status_code == 403:
            raise KrxAuthorizationError(
                "Access forbidden - insufficient permissions",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif 400 <= response.status_code < 500:
            raise KrxClientError(
                f"Client error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif 500 <= response.status_code < 600:
            raise KrxServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        else:
            raise KrxAPIError(
                f"Unexpected error: {response.status_code}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )

    def _safe_json(self, response):
        """안전하게 JSON을 파싱합니다."""
        try:
            return response.json()
        except ValueError:
            return None
