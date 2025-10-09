from pydantic import BaseModel


class StockPriceRiseFallItem(BaseModel):
    pass


class StockPriceRiseFall(BaseModel):
    """해외주식 가격급등락"""

    pass


class StockVolumeSurgeItem(BaseModel):
    pass


class StockVolumeSurge(BaseModel):
    """해외주식 거래량급증"""

    pass


class StockBuyExecutionStrengthTopItem(BaseModel):
    pass


class StockBuyExecutionStrengthTop(BaseModel):
    """해외주식 매수체결강도상위"""

    pass


class StockRiseDeclineRateItem(BaseModel):
    pass


class StockRiseDeclineRate(BaseModel):
    """해외주식 상승률/하락율"""

    pass


class StockNewHighLowPriceItem(BaseModel):
    pass


class StockNewHighLowPrice(BaseModel):
    """해외주식 신고/신저가"""

    pass


class StockTradingVolumeRankItem(BaseModel):
    pass


class StockTradingVolumeRank(BaseModel):
    """해외주식 거래량순위"""

    pass


class StockTradingAmountRankItem(BaseModel):
    pass


class StockTradingAmountRank(BaseModel):
    """해외주식 거래대금순위"""

    pass


class StockTradingIncreaseRateRankItem(BaseModel):
    pass


class StockTradingIncreaseRateRank(BaseModel):
    """해외주식 거래증가율순위"""

    pass


class StockTradingTurnoverRateRankItem(BaseModel):
    pass


class StockTradingTurnoverRateRank(BaseModel):
    """해외주식 거래회전율순위"""

    pass


class StockMarketCapRankItem(BaseModel):
    pass


class StockMarketCapRank(BaseModel):
    """해외주식 시가총액순위"""

    pass


class StockPeriodRightsInquiryItem(BaseModel):
    pass


class StockPeriodRightsInquiry(BaseModel):
    """해외주식 기간별권리조회"""

    pass


class NewsAggregateTitleItem(BaseModel):
    pass


class NewsAggregateTitle(BaseModel):
    """해외뉴스종합(제목)"""

    pass


class StockRightsAggregateItem(BaseModel):
    pass


class StockRightsAggregate(BaseModel):
    """해외주식 권리종합"""

    pass


class StockCollateralLoanEligibleItem(BaseModel):
    pass


class StockCollateralLoanEligible(BaseModel):
    """당사 해외주식담보대출 가능 종목"""

    pass


class BreakingNewsTitleItem(BaseModel):
    pass


class BreakingNewsTitle(BaseModel):
    """해외속보(제목)"""

    pass
