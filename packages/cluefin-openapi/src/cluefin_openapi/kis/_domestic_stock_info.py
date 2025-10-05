from cluefin_openapi.kis._client import Client


class DomesticStockInfo:
    """국내주식 종목정보"""

    def __init__(self, client: Client):
        self.client = client

    def get_product_base_info(self):
        """상품기본조회"""
        pass

    def get_stock_base_info(self):
        """주식기본조회"""
        pass

    def get_domestic_stock_master_price(self):
        """국내주식 대차대조표"""
        pass

    def get_domestic_stock_loss_revenue_statement(self):
        """국내주식 손익계산서"""
        pass

    def get_domestic_stock_finance_ratio(self):
        """국내주식 재무비율"""
        pass

    def get_domestic_stock_profit_ratio(self):
        """국내주식 수익성비율"""
        pass

    def get_domestic_stock_period_summary_ratio(self):
        """국내주식 기타주요비율"""
        pass

    def get_domestic_stock_stability_ratio(self):
        """국내주식 안정성비율"""
        pass

    def get_domestic_stock_growth_ratio(self):
        """국내주식 성장성비율"""
        pass

    def get_domestic_stock_same_new_trading_info(self):
        """국내주식 당사 신용가능종목"""
        pass

    def get_forecast_info_sale_result(self):
        """예탁원정보(배당결정)"""
        pass

    def get_forecast_info_week_trading_summary_result(self):
        """예탁원정보(주식배수청구결정)"""
        pass

    def get_forecast_info_merger_split_result(self):
        """예탁원정보(합병/분할결정)"""
        pass

    def get_forecast_info_capital_reduction_result(self):
        """예탁원정보(액면교체결정)"""
        pass

    def get_forecast_info_capital_increase_result(self):
        """예탁원정보(자본감소일정)"""
        pass

    def get_forecast_info_business_info_result(self):
        """예탁원정보(상장정보일정)"""
        pass

    def get_forecast_info_public_tender_result(self):
        """예탁원정보(공모주청약일정)"""
        pass

    def get_forecast_info_practice_schedule_result(self):
        """예탁원정보(실권주일정)"""
        pass

    def get_forecast_info_deposit_receive_result(self):
        """예탁원정보(입무예치일정)"""
        pass

    def get_forecast_info_paid_shareholder_result(self):
        """예탁원정보(유상증자일정)"""
        pass

    def get_forecast_info_unpaid_shareholder_result(self):
        """예탁원정보(무상증자일정)"""
        pass

    def get_forecast_info_shareholder_general_meeting_result(self):
        """예탁원정보(주주총회일정)"""
        pass

    def get_domestic_stock_item_target_actual(self):
        """국내주식 종목추정실적"""
        pass

    def get_same_major_tradable_item(self):
        """당사 대주가능 종목"""
        pass

    def get_domestic_stock_item_investor_exception(self):
        """국내주식 종목투자의견"""
        pass

    def get_domestic_stock_item_separate_investment_opinion(self):
        """국내주식 증권사별 투자의견"""
        pass
