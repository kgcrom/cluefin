from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasRankInfoRealtimeSymbolQueryRank(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 실시간 종목 조회 순위 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoWatchlistRegistrationTop(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 등록 상위 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPeriodFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPeriodFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPeriodFluctuationRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTodayTradingVolumeTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래량 상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTodayTradingVolumeTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래량 상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTodayTradingValueTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래대금 상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTodayTradingValueTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래대금 상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoMarketCapTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가총액상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoMarketCapTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가총액상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoKiwoomTradingTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="키움 거래 상위 종목(미국주식) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoKiwoomTradingTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="키움 거래 상위 종목(미국 ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPreviousDayFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일대비 등락률상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPreviousDayFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일대비 등락률상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoOpenPriceFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoOpenPriceFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoOpenPriceFluctuationRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoCumulativeFluctuationTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 누적 등락률 상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoCumulativeFluctuationTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 누적 등락률 상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPreviousDayTradingTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일 거래상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoPreviousDayTradingTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일 거래상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoHighLowPriceRiseFallStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 최고최저가대비 상승하락(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoHighLowPriceRiseFallEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 최고최저가대비 상승하락(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoSpecificDateRiseFallStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 특정일자 상승/하락(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoSpecificDateRiseFallEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 특정일자 상승/하락(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTurnoverRateTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 회전율 상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoTurnoverRateTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 회전율 상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoConsecutiveRiseFallRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoConsecutiveRiseFallRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoConsecutiveRiseFallRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoQuoteRemainingVolumeTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 호가잔량상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoQuoteRemainingVolumeTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 호가잔량상위(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoDaytimeTradingDisparityTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주간거래 괴리율 상위(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasRankInfoDaytimeTradingDisparityTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주간거래 괴리율 상위(ETF) 응답")

    # TODO: 응답 필드 정의
