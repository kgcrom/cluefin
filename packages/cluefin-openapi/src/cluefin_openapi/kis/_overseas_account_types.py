from pydantic import BaseModel


class OrderStockItem(BaseModel):
    pass


class OrderStock(BaseModel):
    """해외주식 주문"""

    pass


class CorrectCancelOrderItem(BaseModel):
    pass


class CorrectCancelOrder(BaseModel):
    """해외주식 정정취소주문"""

    pass


class ReserveOrderItem(BaseModel):
    pass


class ReserveOrder(BaseModel):
    """해외주식 예약주문접수"""

    pass


class CancelReserveOrderItem(BaseModel):
    pass


class CancelReserveOrder(BaseModel):
    """해외주식 예약주문접수취소"""

    pass


class BuyTradableAmountItem(BaseModel):
    pass


class BuyTradableAmount(BaseModel):
    """해외주식 매수가능금액조회"""

    pass


class UnexecutedOrdersItem(BaseModel):
    pass


class UnexecutedOrders(BaseModel):
    """해외주식 미체결내역"""

    pass


class StockBalanceItem(BaseModel):
    pass


class StockBalance(BaseModel):
    """해외주식 잔고"""

    pass


class OrderExecutionHistoryItem(BaseModel):
    pass


class OrderExecutionHistory(BaseModel):
    """해외주식 주문체결내역"""

    pass


class CurrentBalanceByExecutionItem(BaseModel):
    pass


class CurrentBalanceByExecution(BaseModel):
    """해외주식 체결기준현재잔고"""

    pass


class ReserveOrdersItem(BaseModel):
    pass


class ReserveOrders(BaseModel):
    """해외주식 예약주문조회"""

    pass


class BalanceBySettlementItem(BaseModel):
    pass


class BalanceBySettlement(BaseModel):
    """해외주식 결제기준잔고"""

    pass


class DailyTransactionHistoryItem(BaseModel):
    pass


class DailyTransactionHistory(BaseModel):
    """해외주식 일별거래내역"""

    pass


class PeriodProfitLossItem(BaseModel):
    pass


class PeriodProfitLoss(BaseModel):
    """해외주식 기간손익"""

    pass


class MarginAggregateItem(BaseModel):
    pass


class MarginAggregate(BaseModel):
    """해외증거금 통합변조회"""

    pass


class OrderUsAfterHoursItem(BaseModel):
    pass


class OrderUsAfterHours(BaseModel):
    """해외주식 미국주간주문"""

    pass


class CorrectCancelUsAfterHoursItem(BaseModel):
    pass


class CorrectCancelUsAfterHours(BaseModel):
    """해외주식 미국주간정정취소"""

    pass


class LimitOrderNumberItem(BaseModel):
    pass


class LimitOrderNumber(BaseModel):
    """해외주식 지정가주문번호조회"""

    pass


class LimitOrderExecutionHistoryItem(BaseModel):
    pass


class LimitOrderExecutionHistory(BaseModel):
    """해외주식 지정가체결내역조회"""

    pass
