from pydantic import BaseModel


class TradingVolumeRankItem(BaseModel):
    pass


class TradingVolumeRank(BaseModel):
    """거래량순위"""

    pass


class StockFluctuationRankItem(BaseModel):
    pass


class StockFluctuationRank(BaseModel):
    """국내주식 등락률 순위"""

    pass


class StockHogaQuantityRankItem(BaseModel):
    pass


class StockHogaQuantityRank(BaseModel):
    """국내주식 호가잔량 순위"""

    pass


class StockProfitabilityIndicatorRankItem(BaseModel):
    pass


class StockProfitabilityIndicatorRank(BaseModel):
    """국내주식 수익자산지표 순위"""

    pass


class StockMarketCapTopItem(BaseModel):
    pass


class StockMarketCapTop(BaseModel):
    """국내주식 시가총액 상위"""

    pass


class StockFinanceRatioRankItem(BaseModel):
    pass


class StockFinanceRatioRank(BaseModel):
    """국내주식 재무비율 순위"""

    pass


class StockTimeHogaRankItem(BaseModel):
    pass


class StockTimeHogaRank(BaseModel):
    """국내주식 시간외잔량 순위"""

    pass


class StockPreferredStockRatioTopItem(BaseModel):
    pass


class StockPreferredStockRatioTop(BaseModel):
    """국내주식 우선주/리리율 상위"""

    pass


class StockDisparityIndexRankItem(BaseModel):
    pass


class StockDisparityIndexRank(BaseModel):
    """국내주식 이격도 순위"""

    pass


class StockMarketPriceRankItem(BaseModel):
    pass


class StockMarketPriceRank(BaseModel):
    """국내주식 시장가치 순위"""

    pass


class StockExecutionStrengthTopItem(BaseModel):
    pass


class StockExecutionStrengthTop(BaseModel):
    """국내주식 체결강도 상위"""

    pass


class StockWatchlistRegistrationTopItem(BaseModel):
    pass


class StockWatchlistRegistrationTop(BaseModel):
    """국내주식 관심종목등록 상위"""

    pass


class StockExpectedExecutionRiseDeclineTopItem(BaseModel):
    pass


class StockExpectedExecutionRiseDeclineTop(BaseModel):
    """국내주식 예상체결 상승/하락상위"""

    pass


class StockProprietaryTradingTopItem(BaseModel):
    pass


class StockProprietaryTradingTop(BaseModel):
    """국내주식 당사매매종목 상위"""

    pass


class StockNewHighLowApproachingTopItem(BaseModel):
    pass


class StockNewHighLowApproachingTop(BaseModel):
    """국내주식 신고/신저근접종목 상위"""

    pass


class StockDividendYieldTopItem(BaseModel):
    pass


class StockDividendYieldTop(BaseModel):
    """국내주식 배당률 상위"""

    pass


class StockLargeExecutionCountTopItem(BaseModel):
    pass


class StockLargeExecutionCountTop(BaseModel):
    """국내주식 대량체결건수 상위"""

    pass


class StockCreditBalanceTopItem(BaseModel):
    pass


class StockCreditBalanceTop(BaseModel):
    """국내주식 신용잔고 상위"""

    pass


class StockShortSellingTopItem(BaseModel):
    pass


class StockShortSellingTop(BaseModel):
    """국내주식 공매도 상위종목"""

    pass


class StockAfterHoursFluctuationRankItem(BaseModel):
    pass


class StockAfterHoursFluctuationRank(BaseModel):
    """국내주식 시간외등락율순위"""

    pass


class StockAfterHoursVolumeRankItem(BaseModel):
    pass


class StockAfterHoursVolumeRank(BaseModel):
    """국내주식 시간외거래량순위"""

    pass


class HtsInquiryTop20Item(BaseModel):
    pass


class HtsInquiryTop20(BaseModel):
    """HTS조회상위20종목"""

    pass
