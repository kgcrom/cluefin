from pydantic import BaseModel


class ProductBasicInfoItem(BaseModel):
    pass


class ProductBasicInfo(BaseModel):
    """상품기본조회"""

    pass


class StockBasicInfoItem(BaseModel):
    pass


class StockBasicInfo(BaseModel):
    """주식기본조회"""

    pass


class BalanceSheetItem(BaseModel):
    pass


class BalanceSheet(BaseModel):
    """국내주식 대차대조표"""

    pass


class IncomeStatementItem(BaseModel):
    pass


class IncomeStatement(BaseModel):
    """국내주식 손익계산서"""

    pass


class FinancialRatioItem(BaseModel):
    pass


class FinancialRatio(BaseModel):
    """국내주식 재무비율"""

    pass


class ProfitabilityRatioItem(BaseModel):
    pass


class ProfitabilityRatio(BaseModel):
    """국내주식 수익성비율"""

    pass


class OtherKeyRatioItem(BaseModel):
    pass


class OtherKeyRatio(BaseModel):
    """국내주식 기타주요비율"""

    pass


class StabilityRatioItem(BaseModel):
    pass


class StabilityRatio(BaseModel):
    """국내주식 안정성비율"""

    pass


class GrowthRatioItem(BaseModel):
    pass


class GrowthRatio(BaseModel):
    """국내주식 성장성비율"""

    pass


class MarginTradableStocksItem(BaseModel):
    pass


class MarginTradableStocks(BaseModel):
    """국내주식 당사 신용가능종목"""

    pass


class KsdDividendDecisionItem(BaseModel):
    pass


class KsdDividendDecision(BaseModel):
    """예탁원정보(배당결정)"""

    pass


class KsdStockDividendDecisionItem(BaseModel):
    pass


class KsdStockDividendDecision(BaseModel):
    """예탁원정보(주식배수청구결정)"""

    pass


class KsdMergerSplitDecisionItem(BaseModel):
    pass


class KsdMergerSplitDecision(BaseModel):
    """예탁원정보(합병/분할결정)"""

    pass


class KsdParValueChangeDecisionItem(BaseModel):
    pass


class KsdParValueChangeDecision(BaseModel):
    """예탁원정보(액면교체결정)"""

    pass


class KsdCapitalReductionScheduleItem(BaseModel):
    pass


class KsdCapitalReductionSchedule(BaseModel):
    """예탁원정보(자본감소일정)"""

    pass


class KsdListingInfoScheduleItem(BaseModel):
    pass


class KsdListingInfoSchedule(BaseModel):
    """예탁원정보(상장정보일정)"""

    pass


class KsdIpoSubscriptionScheduleItem(BaseModel):
    pass


class KsdIpoSubscriptionSchedule(BaseModel):
    """예탁원정보(공모주청약일정)"""

    pass


class KsdForfeitedShareScheduleItem(BaseModel):
    pass


class KsdForfeitedShareSchedule(BaseModel):
    """예탁원정보(실권주일정)"""

    pass


class KsdDepositScheduleItem(BaseModel):
    pass


class KsdDepositSchedule(BaseModel):
    """예탁원정보(입무예치일정)"""

    pass


class KsdPaidInCapitalIncreaseScheduleItem(BaseModel):
    pass


class KsdPaidInCapitalIncreaseSchedule(BaseModel):
    """예탁원정보(유상증자일정)"""

    pass


class KsdStockDividendScheduleItem(BaseModel):
    pass


class KsdStockDividendSchedule(BaseModel):
    """예탁원정보(무상증자일정)"""

    pass


class KsdShareholderMeetingScheduleItem(BaseModel):
    pass


class KsdShareholderMeetingSchedule(BaseModel):
    """예탁원정보(주주총회일정)"""

    pass


class EstimatedEarningsItem(BaseModel):
    pass


class EstimatedEarnings(BaseModel):
    """국내주식 종목추정실적"""

    pass


class StockLoanableListItem(BaseModel):
    pass


class StockLoanableList(BaseModel):
    """당사 대주가능 종목"""

    pass


class InvestmentOpinionItem(BaseModel):
    pass


class InvestmentOpinion(BaseModel):
    """국내주식 종목투자의견"""

    pass


class InvestmentOpinionByBrokerageItem(BaseModel):
    pass


class InvestmentOpinionByBrokerage(BaseModel):
    """국내주식 증권사별 투자의견"""

    pass

