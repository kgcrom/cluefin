from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasStockInfoExchangeList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래소구분 조회 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoStockList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 종목리스트 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 종목 조회 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoSectorList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종리스트 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoIndexList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국지수 리스트 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoEtfEtnList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국 ETF,ETN 리스트 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoEtfCategoryList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국 ETF 카테고리 리스트 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량급등락(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량급등락(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoPriceByRangeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격대별주가(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoPriceByRangeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격대별주가(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoPriceSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoPriceSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoPriceSurgeWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoHighLowApproachStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoHighLowApproachEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoHighLowApproachWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeRenewalStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeRenewalEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeRenewalWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(관심종목) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoNewHighLowStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 신고가/신저가(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoNewHighLowEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 신고가/신저가(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoGapUpDownStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 갭상승/갭하락(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoGapUpDownEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 갭상승/갭하락(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoRemainingRatioSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 잔량률급증(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoRemainingRatioSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 잔량률급증(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeConcentrationStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매물대집중(주식/업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoVolumeConcentrationEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매물대집중(ETF) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoYearlyFluctuationRateStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(종목) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoYearlyFluctuationRateBySector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 업종별 종목등락률 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoYearlyFluctuationRateByEtfCategory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 ETF 카테고리별 종목등락률 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoYearlyFluctuationRateSector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(업종) 응답")

    # TODO: 응답 필드 정의


class OverseasStockInfoYearlyFluctuationRateEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(ETF) 응답")

    # TODO: 응답 필드 정의
