from pydantic import BaseModel

from cluefin_openapi.kis._model import KisHttpBody


class DomesticStockCurrentPriceItem(BaseModel):
    pass


class DomesticStockCurrentPrice(BaseModel, KisHttpBody):
    """국내주식 현재가 시세"""

    pass


class DomesticStockCurrentPriceItem2(BaseModel):
    pass


class DomesticStockCurrentPrice2(BaseModel, KisHttpBody):
    """국내주식 현재가 시세"""

    pass


class DomesticStockCurrentPriceDetailItem(BaseModel):
    pass


class DomesticStockCurrentPriceDetail(BaseModel, KisHttpBody):
    """국내주식 현재가 체결"""

    pass


class DomesticStockCurrentPriceDailyItem(BaseModel):
    pass


class DomesticStockCurrentPriceDaily(BaseModel, KisHttpBody):
    """국내주식 현재가 일자별"""

    pass


class DomesticStockCurrentPriceAskingExpectedConclusionItem(BaseModel):
    pass


class DomesticStockCurrentPriceAskingExpectedConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 호가/예상체결"""

    pass


class DomesticStockCurrentPriceInvestorItem(BaseModel):
    pass


class DomesticStockCurrentPriceInvestor(BaseModel, KisHttpBody):
    """국내주식 현재가 투자자"""

    pass


class DomesticStockCurrentPriceMemberItem(BaseModel):
    pass


class DomesticStockCurrentPriceMember(BaseModel, KisHttpBody):
    """국내주식 현재가 회원사"""

    pass


class DomesticStockPeriodQuoteItem(BaseModel):
    pass


class DomesticStockPeriodQuote(BaseModel, KisHttpBody):
    """국내주식 기간별시세"""

    pass


class DomesticStockTodayMinuteChartItem(BaseModel):
    pass


class DomesticStockTodayMinuteChart(BaseModel, KisHttpBody):
    """국내주식 당일분봉조회"""

    pass


class DomesticStockDailyMinuteChartItem(BaseModel):
    pass


class DomesticStockDailyMinuteChart(BaseModel, KisHttpBody):
    """국내주식 일별분봉조회"""

    pass


class DomesticStockCurrentPriceTimeItemConclusionItem(BaseModel):
    pass


class DomesticStockCurrentPriceTimeItemConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 당일시간대별체결"""

    pass


class DomesticStockCurrentPriceDailyOvertimePriceItem(BaseModel):
    pass


class DomesticStockCurrentPriceDailyOvertimePrice(BaseModel, KisHttpBody):
    """국내주식 현재가 시간외일자별주가"""

    pass


class DomesticStockCurrentPriceOvertimeConclusionItem(BaseModel):
    pass


class DomesticStockCurrentPriceOvertimeConclusion(BaseModel, KisHttpBody):
    """국내주식 현재가 시간외체결"""

    pass


class DomesticStockOvertimeCurrentPriceItem(BaseModel):
    pass


class DomesticStockOvertimeCurrentPrice(BaseModel, KisHttpBody):
    """국내주식 시간외현재가"""

    pass


class DomesticStockOvertimeAskingPriceItem(BaseModel):
    pass


class DomesticStockOvertimeAskingPrice(BaseModel, KisHttpBody):
    """국내주식 시간외호가"""

    pass


class DomesticStockClosingExpectedPriceItem(BaseModel):
    pass


class DomesticStockClosingExpectedPrice(BaseModel, KisHttpBody):
    """국내주식 장마감 예상체결가"""

    pass


class DomesticEtfEtnCurrentPriceItem(BaseModel):
    pass


class DomesticEtfEtnCurrentPrice(BaseModel, KisHttpBody):
    """국내ETF/ETN 현재가 시세"""

    pass


class DomesticEtfComponentStockPriceItem(BaseModel):
    pass


class DomesticEtfComponentStockPrice(BaseModel, KisHttpBody):
    """국내ETF 구성종목시세"""

    pass


class DomesticEtfNavComparisonTrendItem(BaseModel):
    pass


class DomesticEtfNavComparisonTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(종목)"""

    pass


class DomesticEtfNavComparisonDailyTrendItem(BaseModel):
    pass


class DomesticEtfNavComparisonDailyTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(일)"""

    pass


class DomesticEtfNavComparisonTimeTrendItem(BaseModel):
    pass


class DomesticEtfNavComparisonTimeTrend(BaseModel, KisHttpBody):
    """국내ETF NAV 비교추이(시간)"""

    pass
