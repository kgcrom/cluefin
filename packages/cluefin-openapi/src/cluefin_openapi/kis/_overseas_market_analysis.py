from cluefin_openapi.kis._client import Client


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_price_rise_fall(self):
        """해외주식 가격금등락"""
        pass

    def get_stock_volume_surge(self):
        """해외주식 거래량금증"""
        pass

    def get_stock_buy_execution_strength_top(self):
        """해외주식 매수체결강도상위"""
        pass

    def get_stock_rise_decline_rate(self):
        """해외주식 상승률/하락율"""
        pass

    def get_stock_new_high_low_price(self):
        """해외주식 신고/신저가"""
        pass

    def get_stock_trading_volume_rank(self):
        """해외주식 거래량순위"""
        pass

    def get_stock_trading_amount_rank(self):
        """해외주식 거래대금순위"""
        pass

    def get_stock_trading_increase_rate_rank(self):
        """해외주식 거래증가율순위"""
        pass

    def get_stock_trading_turnover_rate_rank(self):
        """해외주식 거래회전율순위"""
        pass

    def get_stock_market_cap_rank(self):
        """해외주식 시가총액순위"""
        pass

    def get_stock_period_rights_inquiry(self):
        """해외주식 기간별권리조회"""
        pass

    def get_news_aggregate_title(self):
        """해외뉴스종합(제목)"""
        pass

    def get_stock_rights_aggregate(self):
        """해외주식 권리종합"""
        pass

    def get_stock_collateral_loan_eligible(self):
        """당사 해외주식담보대출 가능 종목"""
        pass

    def get_breaking_news_title(self):
        """해외속보(제목)"""
        pass
