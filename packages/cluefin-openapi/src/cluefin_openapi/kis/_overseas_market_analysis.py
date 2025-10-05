from cluefin_openapi.kis._client import Client


class OverseasMarketAnalysis:
    """해외주식 시세분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_overseas_stock_price_volume_trend(self):
        """해외주식 가격금등락"""
        pass

    def get_overseas_stock_trading_volume_trend(self):
        """해외주식 거래량금증"""
        pass

    def get_overseas_stock_buy_settlement_amount_top(self):
        """해외주식 매수체결강도상위"""
        pass

    def get_overseas_stock_top_decline_rate(self):
        """해외주식 상승률/하락율"""
        pass

    def get_overseas_stock_new_high_low_price(self):
        """해외주식 신고/신저가"""
        pass

    def get_overseas_stock_trading_volume_rank(self):
        """해외주식 거래량순위"""
        pass

    def get_overseas_stock_trading_amount_rank(self):
        """해외주식 거래대금순위"""
        pass

    def get_overseas_stock_trading_increase_rank(self):
        """해외주식 거래증가율순위"""
        pass

    def get_overseas_stock_trading_member_rate_rank(self):
        """해외주식 거래회전율순위"""
        pass

    def get_overseas_stock_market_cap_rank(self):
        """해외주식 시가총액순위"""
        pass

    def get_overseas_stock_period_separate_interest_inquiry(self):
        """해외주식 기간별권리조회"""
        pass

    def get_overseas_news_aggregate_title(self):
        """해외뉴스종합(제목)"""
        pass

    def get_overseas_stock_interest_aggregate(self):
        """해외주식 권리종합"""
        pass

    def get_same_overseas_stock_same_sale_tradable_item(self):
        """당사 해외주식담보대출 가능 종목"""
        pass

    def get_overseas_report_title(self):
        """해외속보(제목)"""
        pass
