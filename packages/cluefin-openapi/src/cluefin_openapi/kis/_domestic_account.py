from cluefin_openapi.kis._client import Client


class DomesticAccount:
    """국내주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

    def get_stock_quote_current(self):
        """주식주문(현금)"""
        pass

    def get_stock_quote_credit(self):
        """주식주문(신용)"""
        pass

    def get_stock_quote_correction(self):
        """주식주문(정정취소)"""
        pass

    def get_stock_correction_cancellable_qty(self):
        """주식정정취소가능주문조회"""
        pass

    def get_stock_daily_separate_conclusion(self):
        """주식일별주문체결조회"""
        pass

    def get_stock_balance(self):
        """주식잔고조회"""
        pass

    def get_buy_tradable_inquiry(self):
        """매수가능조회"""
        pass

    def get_sell_tradable_inquiry(self):
        """매도가능수량조회"""
        pass

    def get_new_subscription_tradable_inquiry(self):
        """신용매수가능조회"""
        pass

    def get_stock_reserve_quote(self):
        """주식예약주문"""
        pass

    def get_stock_reserve_quote_correction(self):
        """주식예약주문정정취소"""
        pass

    def get_stock_reserve_quote_inquiry(self):
        """주식예약주문조회"""
        pass

    def get_pension_fund_establishment_standard(self):
        """퇴직연금 체결기준잔고"""
        pass

    def get_pension_fund_unexecuted_history(self):
        """퇴직연금 미체결내역"""
        pass

    def get_pension_fund_buy_tradable_inquiry(self):
        """퇴직연금 매수가능조회"""
        pass

    def get_pension_fund_reserve_deposit_inquiry(self):
        """퇴직연금 예수금조회"""
        pass

    def get_pension_fund_balance(self):
        """퇴직연금 잔고조회"""
        pass

    def get_stock_balance_loss_profit(self):
        """주식잔고조회_실현손익"""
        pass

    def get_investment_account_current_status(self):
        """투자계좌자산현황조회"""
        pass

    def get_institution_separated_disclosure(self):
        """기관별순의별합산조회"""
        pass

    def get_institution_separated_sale_current_status(self):
        """기관별매매순의현황조회"""
        pass

    def get_stock_integrated_deposit_balance(self):
        """주식통합증거금 현황"""
        pass

    def get_institution_separated_accounting_current_status(self):
        """기관별계좌권리현황조회"""
        pass
