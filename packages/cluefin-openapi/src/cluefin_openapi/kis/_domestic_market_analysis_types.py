from pydantic import BaseModel, Field


class ConditionSearchListItem(BaseModel):
    pass


class ConditionSearchList(BaseModel):
    """종목조건검색 목록조회"""

    pass


class ConditionSearchResultItem(BaseModel):
    pass


class ConditionSearchResult(BaseModel):
    """종목조건검색조회"""

    pass


class WatchlistGroupsItem(BaseModel):
    pass


class WatchlistGroups(BaseModel):
    """관심종목 그룹조회"""

    pass


class WatchlistMultiQuoteItem(BaseModel):
    pass


class WatchlistMultiQuote(BaseModel):
    """관심종목(멀티종목) 시세조회"""

    pass


class WatchlistStocksByGroupItem(BaseModel):
    pass


class WatchlistStocksByGroup(BaseModel):
    """관심종목 그룹별 종목조회"""

    pass


class InstitutionalForeignTradingAggregateItem(BaseModel):
    pass


class InstitutionalForeignTradingAggregate(BaseModel):
    """국내기관_외국인 매매종목가집계"""

    pass


class ForeignBrokerageTradingAggregateItem(BaseModel):
    pass


class ForeignBrokerageTradingAggregate(BaseModel):
    """외국계 매매종목 가집계"""

    pass


class InvestorTradingTrendByStockDailyItem(BaseModel):
    pass


class InvestorTradingTrendByStockDaily(BaseModel):
    """종목별 투자자매매동향(일별)"""

    pass


class InvestorTradingTrendByMarketIntradayItem(BaseModel):
    pass


class InvestorTradingTrendByMarketIntraday(BaseModel):
    """시장별 투자자매매동향(시세)"""

    pass


class InvestorTradingTrendByMarketDailyItem(BaseModel):
    pass


class InvestorTradingTrendByMarketDaily(BaseModel):
    """시장별 투자자매매동향(일별)"""

    pass


class ForeignNetBuyTrendByStockItem(BaseModel):
    pass


class ForeignNetBuyTrendByStock(BaseModel):
    """종목별 외국계 순매수추이"""

    pass


class MemberTradingTrendTickItem(BaseModel):
    pass


class MemberTradingTrendTick(BaseModel):
    """회원사 실시간 매매동향(틱)"""

    pass


class MemberTradingTrendByStockItem(BaseModel):
    pass


class MemberTradingTrendByStock(BaseModel):
    """주식현재가 회원사 종목매매동향"""

    pass


class ProgramTradingTrendByStockIntradayItem(BaseModel):
    pass


class ProgramTradingTrendByStockIntraday(BaseModel):
    """종목별 프로그램매매추이(체결)"""

    pass


class ProgramTradingTrendByStockDailyItem(BaseModel):
    pass


class ProgramTradingTrendByStockDaily(BaseModel):
    """종목별 프로그램매매추이(일별)"""

    pass


class ForeignInstitutionalEstimateByStockItem(BaseModel):
    pass


class ForeignInstitutionalEstimateByStock(BaseModel):
    """종목별 외인기관 추정기전계"""

    pass


class BuySellVolumeByStockDailyItem(BaseModel):
    pass


class BuySellVolumeByStockDaily(BaseModel):
    """종목별일별매수매도체결량"""

    pass


class ProgramTradingSummaryIntradayItem(BaseModel):
    pass


class ProgramTradingSummaryIntraday(BaseModel):
    """프로그램매매 종합현황(시간)"""

    pass


class ProgramTradingSummaryDailyItem(BaseModel):
    pass


class ProgramTradingSummaryDaily(BaseModel):
    """프로그램매매 종합현황(일별)"""

    pass


class ProgramTradingInvestorTrendTodayItem(BaseModel):
    pass


class ProgramTradingInvestorTrendToday(BaseModel):
    """프로그램매매 투자자매매동향(당일)"""

    pass


class CreditBalanceTrendDailyItem(BaseModel):
    pass


class CreditBalanceTrendDaily(BaseModel):
    """국내주식 신용잔고 일별추이"""

    pass


class ExpectedPriceTrendItem(BaseModel):
    pass


class ExpectedPriceTrend(BaseModel):
    """국내주식 예상체결가 추이"""

    pass


class ShortSellingTrendDailyItem(BaseModel):
    pass


class ShortSellingTrendDaily(BaseModel):
    """국내주식 공매도 일별추이"""

    pass


class AfterHoursExpectedFluctuationItem(BaseModel):
    pass


class AfterHoursExpectedFluctuation(BaseModel):
    """국내주식 시간외예상체결등락율"""

    pass


class TradingWeightByAmountItem(BaseModel):
    pass


class TradingWeightByAmount(BaseModel):
    """국내주식 체결금액별 매매비중"""

    pass


class MarketFundSummaryItem(BaseModel):
    pass


class MarketFundSummary(BaseModel):
    """국내 증시자금 종합"""

    pass


class StockLoanTrendDailyItem(BaseModel):
    pass


class StockLoanTrendDaily(BaseModel):
    """종목별 일별 대차거래추이"""

    pass


class LimitPriceStocksItem(BaseModel):
    pass


class LimitPriceStocks(BaseModel):
    """국내주식 상하한가 표착"""

    pass


class ResistanceLevelTradingWeightItem(BaseModel):
    pass


class ResistanceLevelTradingWeight(BaseModel):
    """국내주식 매물대/거래비중"""

    pass
