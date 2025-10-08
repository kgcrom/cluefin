from cluefin_openapi.kis._client import Client


class OverseasAccount:
    """해외주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

    def order_stock(self):
        """해외주식 주문"""
        pass

    def correct_cancel_order(self):
        """해외주식 정정취소주문"""
        pass

    def reserve_order(self):
        """해외주식 예약주문접수"""
        pass

    def cancel_reserve_order(self):
        """해외주식 예약주문접수취소"""
        pass

    def get_buy_tradable_amount(self):
        """해외주식 매수가능금액조회"""
        pass

    def get_unexecuted_orders(self):
        """해외주식 미체결내역"""
        pass

    def get_stock_balance(self):
        """해외주식 잔고"""
        pass

    def get_order_execution_history(self):
        """해외주식 주문체결내역"""
        pass

    def get_current_balance_by_execution(self):
        """해외주식 체결기준현재잔고"""
        pass

    def get_reserve_orders(self):
        """해외주식 예약주문조회"""
        pass

    def get_balance_by_settlement(self):
        """해외주식 결제기준잔고"""
        pass

    def get_daily_transaction_history(self):
        """해외주식 일별거래내역"""
        pass

    def get_period_profit_loss(self):
        """해외주식 기간손익"""
        pass

    def get_margin_aggregate(self):
        """해외증거금 통합변조회"""
        pass

    def order_us_after_hours(self):
        """해외주식 미국주간주문"""
        pass

    def correct_cancel_us_after_hours(self):
        """해외주식 미국주간정정취소"""
        pass

    def get_limit_order_number(self):
        """해외주식 지정가주문번호조회"""
        pass

    def get_limit_order_execution_history(self):
        """해외주식 지정가체결내역조회"""
        pass
