from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasChartTick(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 틱 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartMinute(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 분 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartDaily(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartWeekly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartMonthly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartYearly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 년 차트 응답")

    # TODO: 응답 필드 정의


class OverseasChartQuarterly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 분기 차트 응답")

    # TODO: 응답 필드 정의
