from pydantic import BaseModel


class StockCurrentPriceDetailItem(BaseModel):
    pass


class StockCurrentPriceDetail(BaseModel):
    """해외주식 현재가상세"""

    pass


class CurrentPriceFirstQuoteItem(BaseModel):
    pass


class CurrentPriceFirstQuote(BaseModel):
    """해외주식 현재가 1호가"""

    pass


class StockCurrentPriceConclusionItem(BaseModel):
    pass


class StockCurrentPriceConclusion(BaseModel):
    """해외주식 현재체결가"""

    pass


class ConclusionTrendItem(BaseModel):
    pass


class ConclusionTrend(BaseModel):
    """해외주식 체결추이"""

    pass


class StockMinuteChartItem(BaseModel):
    pass


class StockMinuteChart(BaseModel):
    """해외주식분봉조회"""

    pass


class IndexMinuteChartItem(BaseModel):
    pass


class IndexMinuteChart(BaseModel):
    """해외지수분봉조회"""

    pass


class StockPeriodQuoteItem(BaseModel):
    pass


class StockPeriodQuote(BaseModel):
    """해외주식 기간별시세"""

    pass


class ItemIndexExchangePeriodPriceItem(BaseModel):
    pass


class ItemIndexExchangePeriodPrice(BaseModel):
    """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""

    pass


class SearchByConditionItem(BaseModel):
    pass


class SearchByCondition(BaseModel):
    """해외주식조건검색"""

    pass


class SettlementDateItem(BaseModel):
    pass


class SettlementDate(BaseModel):
    """해외결제일자조회"""

    pass


class ProductBaseInfoItem(BaseModel):
    pass


class ProductBaseInfo(BaseModel):
    """해외주식 상품기본정보"""

    pass


class SectorPriceItem(BaseModel):
    pass


class SectorPrice(BaseModel):
    """해외주식 업종별시세"""

    pass


class SectorCodesItem(BaseModel):
    pass


class SectorCodes(BaseModel):
    """해외주식 업종별코드조회"""

    pass
