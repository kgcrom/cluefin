from typing import Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class SectorCurrentIndexItem(BaseModel):
    pass

class SectorCurrentIndex(BaseModel, KisHttpBody):
    """국내업종 현재지수 응답"""
    pass

class SectorDailyIndexItem(BaseModel):
    pass

class SectorDailyIndex(BaseModel, KisHttpBody):
    """국내업종 일자별지수 응답"""
    pass

class SectorTimeIndexSecondItem(BaseModel):
    pass

class SectorTimeIndexSecond(BaseModel, KisHttpBody):
    """국내업종 시간별지수(초) 응답"""
    pass

class SectorTimeIndexMinuteItem(BaseModel):
    pass

class SectorTimeIndexMinute(BaseModel, KisHttpBody):
    """국내업종 시간별지수(분) 응답"""
    pass

class SectorMinuteInquiryItem(BaseModel):
    pass

class SectorMinuteInquiry(BaseModel, KisHttpBody):
    """업종 분봉조회 응답"""
    pass

class SectorPeriodQuoteItem(BaseModel):
    pass

class SectorPeriodQuote(BaseModel, KisHttpBody):
    """국내주식업종기간별시세(일/주/월/년) 응답"""
    pass

class SectorAllQuoteByCategoryItem(BaseModel):
    pass

class SectorAllQuoteByCategory(BaseModel, KisHttpBody):
    """국내업종 구분별전체시세 응답"""
    pass

class ExpectedIndexTrendItem(BaseModel):
    pass

class ExpectedIndexTrend(BaseModel, KisHttpBody):
    """국내주식 예상체결지수 추이 응답"""
    pass

class ExpectedIndexAllItem(BaseModel):
    pass

class ExpectedIndexAll(BaseModel, KisHttpBody):
    """국내주식 예상체결 전체지수 응답"""
    pass

class VolatilityInterruptionStatusItem(BaseModel):
    pass

class VolatilityInterruptionStatus(BaseModel, KisHttpBody):
    """변동성완화장치(VI) 현황 응답"""
    pass

class InterestRateSummaryItem(BaseModel):
    pass

class InterestRateSummary(BaseModel, KisHttpBody):
    """금리 종합(국내채권/금리) 응답"""
    pass

class MarketAnnouncementScheduleItem(BaseModel):
    pass

class MarketAnnouncementSchedule(BaseModel, KisHttpBody):
    """종합 시황/공시(제목) 응답"""
    pass

class HolidayInquiryItem(BaseModel):
    pass

class HolidayInquiry(BaseModel, KisHttpBody):
    """국내휴장일조회 응답"""
    pass

class FuturesBusinessDayInquiryItem(BaseModel):
    pass

class FuturesBusinessDayInquiry(BaseModel, KisHttpBody):
    """국내선물 영업일조회 응답"""
    pass
