from typing import Dict, Optional

import requests

from ._exceptions import (
    DartAPIError,
    DartAuthenticationError,
    DartAuthorizationError,
    DartClientError,
    DartServerError,
)


class Client(object):
    def __init__(self, auth_key: str, timeout: int = 30):
        self.auth_key = auth_key
        self.base_url = "https://opendart.fss.or.kr"
        self.timeout = timeout

    @property
    def major_shareholder_disclosure(self):
        from ._major_shareholder_disclosure import MajorShareholderDisclosure

        return MajorShareholderDisclosure(self)

    @property
    def public_disclosure(self):
        from ._public_disclosure import PublicDisclosure

        return PublicDisclosure(self)

    @property
    def periodic_report_key_information(self):
        from ._periodic_report_key_information import PeriodicReportKeyInformation

        return PeriodicReportKeyInformation(self)

    def _get_bytes(self, path: str, *, params: Optional[Dict] = None):
        url = self.base_url + path
        if params is None:
            params = {}
        params["crtfc_key"] = self.auth_key

        response = requests.get(url, params=params, timeout=self.timeout)
        self._raise_for_status(response)
        return response.content

    def _get(self, path: str, *, params: Optional[Dict] = None):
        url = self.base_url + path
        if params is None:
            params = {}
        params["crtfc_key"] = self.auth_key

        response = requests.get(url, params=params, timeout=self.timeout)
        self._raise_for_status(response)
        try:
            return response.json()
        except ValueError:
            return response.text

    def _raise_for_status(self, response):
        if response.status_code == 200:
            return
        elif response.status_code == 401:
            raise DartAuthenticationError(
                "Authentication failed - invalid or expired token",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif response.status_code == 403:
            raise DartAuthorizationError(
                "Access forbidden - insufficient permissions",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif 400 <= response.status_code < 500:
            raise DartClientError(
                f"Client error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        elif 500 <= response.status_code < 600:
            raise DartServerError(
                f"Server error: {response.text}",
                status_code=response.status_code,
                response_data=self._safe_json(response),
            )
        else:
            raise DartAPIError(
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
