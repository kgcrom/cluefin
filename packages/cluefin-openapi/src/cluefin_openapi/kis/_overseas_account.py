from cluefin_openapi.kis._client import Client


class OverseasAccount:
    """해외주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

    def get_overseas_stock_order(self):
        """해외주식 주문"""
        pass

    def get_overseas_stock_correction_cancel_order(self):
        """해외주식 정정취소주문"""
        pass

    def get_overseas_stock_reserve_quote_count(self):
        """해외주식 예약주문접수"""
        pass

    def get_overseas_stock_reserve_quote_cancel(self):
        """해외주식 예약주문접수취소"""
        pass

    def get_overseas_stock_buy_tradable_amount_inquiry(self):
        """해외주식 매수가능금액조회"""
        pass

    def get_overseas_stock_unexecuted_history(self):
        """해외주식 미체결내역"""
        pass

    def get_overseas_stock_balance(self):
        """해외주식 잔고"""
        pass

    def get_overseas_stock_order_settlement_history(self):
        """해외주식 주문체결내역"""
        pass

    def get_overseas_stock_settlement_standard_current_balance(self):
        """해외주식 체결기준현재잔고"""
        pass

    def get_overseas_stock_reserve_quote_inquiry(self):
        """해외주식 예약주문조회"""
        pass

    def get_overseas_stock_settlement_standard_balance(self):
        """해외주식 결제기준잔고"""
        pass

    def get_overseas_stock_daily_separate_history(self):
        """해외주식 일별거래내역"""
        pass

    def get_overseas_stock_period_loss_profit(self):
        """해외주식 기간손익"""
        pass

    def get_overseas_medium_capital_aggregate_inquiry(self):
        """해외증거금 통합변조회"""
        pass

    def get_overseas_stock_us_stock_order(self):
        """해외주식 미국주간주문"""
        pass

    def get_overseas_stock_us_stock_correction_cancel(self):
        """해외주식 미국주간정정취소"""
        pass

    def get_overseas_stock_designated_quote_number_inquiry(self):
        """해외주식 지정가주문번호조회"""
        pass

    def get_overseas_stock_designated_settlement_history_inquiry(self):
        """해외주식 지정가체결내역조회"""
        pass
