from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasExchangeEstimatedAmount(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환전 예상 금액 조회 응답")

    # TODO: 응답 필드 정의


class OverseasExchangeRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환율 조회 응답")

    # TODO: 응답 필드 정의


class OverseasExchangeRequest(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="환전 신청 응답")

    # TODO: 응답 필드 정의
