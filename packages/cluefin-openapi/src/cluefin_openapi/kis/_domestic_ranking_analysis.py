from cluefin_openapi.kis._client import Client


class DomesticRankingAnalysis:
    """국내주식 순위분석"""

    def __init__(self, client: Client):
        self.client = client

    def get_trading_volume_rank(self):
        """거래량순위"""
        pass

    def get_domestic_stock_fluctuation_rank(self):
        """국내주식 등락률 순위"""
        pass

    def get_domestic_stock_hoga_quantity_rank(self):
        """국내주식 호가잔량 순위"""
        pass

    def get_domestic_stock_investor_transaction_rank(self):
        """국내주식 수익자산지표 순위"""
        pass

    def get_domestic_stock_market_cap_top(self):
        """국내주식 시가총액 상위"""
        pass

    def get_domestic_stock_finance_ratio_rank(self):
        """국내주식 재무비율 순위"""
        pass

    def get_domestic_stock_time_hoga_rank(self):
        """국내주식 시간외잔량 순위"""
        pass

    def get_domestic_stock_week_leader_ratio_top(self):
        """국내주식 우선주/리리율 상위"""
        pass

    def get_domestic_stock_volatility_rank(self):
        """국내주식 이격도 순위"""
        pass

    def get_domestic_stock_market_price_rank(self):
        """국내주식 시장가치 순위"""
        pass

    def get_domestic_stock_settlement_amount_top(self):
        """국내주식 체결강도 상위"""
        pass

    def get_domestic_stock_interest_stock_top(self):
        """국내주식 관심종목등록 상위"""
        pass

    def get_domestic_stock_expected_conclusion_top_decline_top(self):
        """국내주식 예상체결 상승/하락상위"""
        pass

    def get_domestic_stock_same_sale_buy_balance_top(self):
        """국내주식 당사매매종목 상위"""
        pass

    def get_domestic_stock_new_low_reserve_conclusion_top(self):
        """국내주식 신고/신저근접종목 상위"""
        pass

    def get_domestic_stock_sale_volume_top(self):
        """국내주식 배당률 상위"""
        pass

    def get_domestic_stock_settlement_conclusion_number_top(self):
        """국내주식 대량체결건수 상위"""
        pass

    def get_domestic_stock_new_credit_top(self):
        """국내주식 신용잔고 상위"""
        pass

    def get_domestic_stock_public_sale_top_item(self):
        """국내주식 공매도 상위종목"""
        pass

    def get_domestic_stock_time_fluctuation_up_rank(self):
        """국내주식 시간외등락율순위"""
        pass

    def get_domestic_stock_time_foreign_increase_rank(self):
        """국내주식 시간외거래량순위"""
        pass

    def get_hts_inquiry_top_20_item(self):
        """HTS조회상위20종목"""
        pass
