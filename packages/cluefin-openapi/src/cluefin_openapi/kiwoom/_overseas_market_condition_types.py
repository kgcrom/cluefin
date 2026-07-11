from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasMarketConditionCurrentPriceStockInfo(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 현재가 종목정보 응답")

    # TODO: 응답 필드 정의


class OverseasMarketConditionCurrentPriceTenQuotes(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 현재가 10호가 응답")

    # TODO: 응답 필드 정의


class OverseasMarketConditionDetailedExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 상세 체결내역 응답")

    # TODO: 응답 필드 정의


class OverseasMarketConditionDailyExecutionHistory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별 체결내역 응답")

    # TODO: 응답 필드 정의


class OverseasMarketConditionDailyStockPrice(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일별주가 응답")

    # TODO: 응답 필드 정의
