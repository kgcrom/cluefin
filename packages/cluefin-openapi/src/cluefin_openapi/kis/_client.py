from typing import Literal, Union

import requests
from loguru import logger
from pydantic import SecretStr


class Client(object):
    def __init__(
        self,
        token: str,
        app_key: str,
        secret_key: Union[str, SecretStr],
        env: Literal["prod", "dev"] = "prod",
        debug: bool = False,
    ):
        self.token = token
        self.app_key = app_key
        self.secret_key = secret_key.get_secret_value() if isinstance(secret_key, SecretStr) else secret_key
        self.env = env
        self.debug = debug

        if self.env == "prod":
            self.base_url = "https://openapi.koreainvestment.com:9443"
        else:
            self.base_url = "https://openapivts.koreainvestment.com:29443"

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "cluefin-openapi/1.0",
            }
        )

        if self.debug:
            logger.enable("cluefin_openapi.kis")
        else:
            logger.disable("cluefin_openapi.kis")

    @property
    def domestic_account(self):
        """국내주식 주문/계좌"""
        from ._domestic_account import DomesticAccount

        return DomesticAccount(self)

    @property
    def domestic_basic_quote(self):
        """국내주식 기본시세"""
        from ._domestic_basic_quote import DomesticBasicQuote

        return DomesticBasicQuote(self)

    @property
    def domestic_issue_other(self):
        """국내주식 업종/기타"""
        from ._domestic_issue_other import DomesticIssueOther

        return DomesticIssueOther(self)

    @property
    def domestic_stock_info(self):
        """국내주식 종목정보"""
        from ._domestic_stock_info import DomesticStockInfo

        return DomesticStockInfo(self)

    @property
    def domestic_market_analysis(self):
        """국내주식 시세분석"""
        from ._domestic_market_analysis import DomesticMarketAnalysis

        return DomesticMarketAnalysis(self)

    @property
    def domestic_ranking_analysis(self):
        """국내주식 순위분석"""
        from ._domestic_ranking_analysis import DomesticRankingAnalysis

        return DomesticRankingAnalysis(self)

    @property
    def overseas_account(self):
        """해외주식 주문/계좌"""
        from ._overseas_account import OverseasAccount

        return OverseasAccount(self)

    @property
    def overseas_basic_quote(self):
        """해외주식 기본시세"""
        from ._overseas_basic_quote import OverseasBasicQuote

        return OverseasBasicQuote(self)

    @property
    def overseas_market_analysis(self):
        """해외주식 시세분석"""
        from ._overseas_market_analysis import OverseasMarketAnalysis

        return OverseasMarketAnalysis(self)

    # TODO 법인은 추후 필요해지면 구현
    def _get(self, path: str, headers: dict, params: dict) -> requests.Response:
        url = self.base_url + path
        if self.debug:
            logger.debug(f"GET {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Params: {params}")

        merged_headers = dict(self._session.headers)
        merged_headers["content-type"] = "application/json;charset=UTF-8"
        merged_headers["accept"] = "application/json"
        merged_headers["authorization"] = f"Bearer {self.token}"
        merged_headers["appkey"] = self.app_key
        merged_headers["appsecret"] = self.secret_key
        merged_headers["custtype"] = "P"  # P: 개인, C: 법인
        merged_headers.update(headers)  # Merge custom headers (e.g., tr_id)
        response = self._session.get(url, headers=merged_headers, params=params, timeout=30)
        if self.debug:
            logger.debug(f"Response Status: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug(f"Response Body: {response.text}")
        return response

    # TODO 법인은 추후 필요해지면 구현
    def _post(self, path: str, headers: dict, body: dict) -> requests.Response:
        url = self.base_url + path
        if self.debug:
            logger.debug(f"POST {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Body: {body}")

        merged_headers = dict(self._session.headers)
        merged_headers["content-type"] = "application/json;charset=UTF-8"
        merged_headers["accept"] = "application/json"
        merged_headers["authorization"] = f"Bearer {self.token}"
        merged_headers["appkey"] = self.app_key
        merged_headers["appsecret"] = self.secret_key
        merged_headers["custtype"] = "P"  # P: 개인, C: 법인
        merged_headers.update(headers)  # Merge custom headers (e.g., tr_id)
        response = self._session.post(url, headers=merged_headers, json=body, timeout=30)
        if self.debug:
            logger.debug(f"Response Status: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug(f"Response Body: {response.text}")
        return response
