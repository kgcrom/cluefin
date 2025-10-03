from cluefin_openapi.kis._domestic_account import DomesticAccount
from cluefin_openapi.kis._domestic_basic_quote import DomesticBasicQuote
from cluefin_openapi.kis._domestic_issue_other import DomesticIssueOther
from cluefin_openapi.kis._domestic_stock_info import DomesticStockInfo
from cluefin_openapi.kis._domestic_market_analysis import DomesticMarketAnalysis
from cluefin_openapi.kis._domestic_ranking_analysis import DomesticRankingAnalysis
from cluefin_openapi.kis._overseas_account import OverseasAccount
from cluefin_openapi.kis._overseas_basic_quote import OverseasBasicQuote
from cluefin_openapi.kis._overseas_market_analysis import OverseasMarketAnalysis
from cluefin_openapi.kis._overseas_realtime_quote import OverseasRealtimeQuote


class Client:
    def __init__(self, token: str, env: str = "prod"):
        """
        Initialize KIS API Client

        Args:
            token (str): Access token for authentication
            env (str): Environment ("dev" or "prod")
        """
        self.token = token
        self.env = env


    @property
    def domestic_account(self) -> DomesticAccount:
        """국내주식 주문/계좌"""
        if self._domestic_account is None:
            self._domestic_account = DomesticAccount(self)
        return self._domestic_account

    @property
    def domestic_basic_quote(self) -> DomesticBasicQuote:
        """국내주식 기본시세"""
        if self._domestic_basic_quote is None:
            self._domestic_basic_quote = DomesticBasicQuote(self)
        return self._domestic_basic_quote

    @property
    def domestic_issue_other(self) -> DomesticIssueOther:
        """국내주식 업종/기타"""
        if self._domestic_issue_other is None:
            self._domestic_issue_other = DomesticIssueOther(self)
        return self._domestic_issue_other

    @property
    def domestic_stock_info(self) -> DomesticStockInfo:
        """국내주식 종목정보"""
        if self._domestic_stock_info is None:
            self._domestic_stock_info = DomesticStockInfo(self)
        return self._domestic_stock_info

    @property
    def domestic_market_analysis(self) -> DomesticMarketAnalysis:
        """국내주식 시세분석"""
        if self._domestic_market_analysis is None:
            self._domestic_market_analysis = DomesticMarketAnalysis(self)
        return self._domestic_market_analysis

    @property
    def domestic_ranking_analysis(self) -> DomesticRankingAnalysis:
        """국내주식 순위분석"""
        if self._domestic_ranking_analysis is None:
            self._domestic_ranking_analysis = DomesticRankingAnalysis(self)
        return self._domestic_ranking_analysis

    @property
    def overseas_account(self) -> OverseasAccount:
        """해외주식 주문/계좌"""
        if self._overseas_account is None:
            self._overseas_account = OverseasAccount(self)
        return self._overseas_account

    @property
    def overseas_basic_quote(self) -> OverseasBasicQuote:
        """해외주식 기본시세"""
        if self._overseas_basic_quote is None:
            self._overseas_basic_quote = OverseasBasicQuote(self)
        return self._overseas_basic_quote

    @property
    def overseas_market_analysis(self) -> OverseasMarketAnalysis:
        """해외주식 시세분석"""
        if self._overseas_market_analysis is None:
            self._overseas_market_analysis = OverseasMarketAnalysis(self)
        return self._overseas_market_analysis

    @property
    def overseas_realtime_quote(self) -> OverseasRealtimeQuote:
        """해외주식 실시간시세"""
        if self._overseas_realtime_quote is None:
            self._overseas_realtime_quote = OverseasRealtimeQuote(self)
        return self._overseas_realtime_quote
