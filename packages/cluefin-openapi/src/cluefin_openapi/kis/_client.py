from typing import Literal

import requests
from loguru import logger


class Client(object):
    def __init__(self, token: str, env: Literal["prod", "dev"] = "prod", debug: bool = False):
        self.token = token
        self.env = env
        self.debug = debug
        if self.env == "prod":
            self.base_url = "https://openapi.koreainvestment.com:9443"
        else:
            self.base_url = "https://sandboxopenapi.koreainvestment.com:9443"
        
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "cluefin-openapi/1.0",
        })

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
