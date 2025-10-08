from cluefin_openapi.kis._client import Client


class DomesticStockInfo:
    """국내주식 종목정보"""

    def __init__(self, client: Client):
        self.client = client

    def get_product_basic_info(self):
        """상품기본조회"""
        pass

    def get_stock_basic_info(self):
        """주식기본조회"""
        pass

    def get_balance_sheet(self):
        """국내주식 대차대조표"""
        pass

    def get_income_statement(self):
        """국내주식 손익계산서"""
        pass

    def get_financial_ratio(self):
        """국내주식 재무비율"""
        pass

    def get_profitability_ratio(self):
        """국내주식 수익성비율"""
        pass

    def get_other_key_ratio(self):
        """국내주식 기타주요비율"""
        pass

    def get_stability_ratio(self):
        """국내주식 안정성비율"""
        pass

    def get_growth_ratio(self):
        """국내주식 성장성비율"""
        pass

    def get_margin_tradable_stocks(self):
        """국내주식 당사 신용가능종목"""
        pass

    def get_ksd_dividend_decision(self):
        """예탁원정보(배당결정)"""
        pass

    def get_ksd_stock_dividend_decision(self):
        """예탁원정보(주식배수청구결정)"""
        pass

    def get_ksd_merger_split_decision(self):
        """예탁원정보(합병/분할결정)"""
        pass

    def get_ksd_par_value_change_decision(self):
        """예탁원정보(액면교체결정)"""
        pass

    def get_ksd_capital_reduction_schedule(self):
        """예탁원정보(자본감소일정)"""
        pass

    def get_ksd_listing_info_schedule(self):
        """예탁원정보(상장정보일정)"""
        pass

    def get_ksd_ipo_subscription_schedule(self):
        """예탁원정보(공모주청약일정)"""
        pass

    def get_ksd_forfeited_share_schedule(self):
        """예탁원정보(실권주일정)"""
        pass

    def get_ksd_deposit_schedule(self):
        """예탁원정보(입무예치일정)"""
        pass

    def get_ksd_paid_in_capital_increase_schedule(self):
        """예탁원정보(유상증자일정)"""
        pass

    def get_ksd_stock_dividend_schedule(self):
        """예탁원정보(무상증자일정)"""
        pass

    def get_ksd_shareholder_meeting_schedule(self):
        """예탁원정보(주주총회일정)"""
        pass

    def get_estimated_earnings(self):
        """국내주식 종목추정실적"""
        pass

    def get_stock_loanable_list(self):
        """당사 대주가능 종목"""
        pass

    def get_investment_opinion(self):
        """국내주식 종목투자의견"""
        pass

    def get_investment_opinion_by_brokerage(self):
        """국내주식 증권사별 투자의견"""
        pass
