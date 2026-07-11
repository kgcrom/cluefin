from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasAccountDailyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별계좌수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountMonthlyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별계좌수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountYearlyProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별계좌수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDailyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별종목수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountMonthlyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별종목수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountYearlyStockProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별종목수익률현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountLedgerUnfilledOrders(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 원장 미체결 응답")

    # TODO: 응답 필드 정의


class OverseasAccountLedgerBalance(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 원장잔고확인 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTransactionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래내역 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDeposit(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외주식 예수금 응답")

    # TODO: 응답 필드 정의


class OverseasAccountKrwWithdrawableAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="원화출금가능 금액 조회(원화대용 포함) 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDepositAndSecuritiesValuationByCurrency(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="통화별 예수금 및 증권 평가금현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountLedgerValuationAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외증권 원장 평가금액현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountValuationAmountByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="해외증권 특정일 평가금액 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDepositAndSecuritiesValuationByCurrencyByDate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="특정일 통화별 예수금 및 증권 평가금 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDailyOrderExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 주문체결내역 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDepositDetail(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 예수금 상세 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTodayRealizedProfitLossByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 종목별 실현손익 응답")

    # TODO: 응답 필드 정의


class OverseasAccountOrderHistoryByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 주문내역 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTodayOrderExecution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 주문체결 확인 응답")

    # TODO: 응답 필드 정의


class OverseasAccountRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 실현손익 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTodayTrading(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일매매 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTodayTradingSummary(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일매매정리 응답")

    # TODO: 응답 필드 정의


class OverseasAccountTodayRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 실현손익 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDailyRealizedProfitLossByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 종목별 실현손익 응답")

    # TODO: 응답 필드 정의


class OverseasAccountProfitRateByPeriod(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 수익률 현황 응답")

    # TODO: 응답 필드 정의


class OverseasAccountDailyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 실현손익 응답")

    # TODO: 응답 필드 정의


class OverseasAccountMonthlyRealizedProfitLoss(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월별 실현손익 응답")

    # TODO: 응답 필드 정의
