from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasOrderBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매수 주문 응답")

    # TODO: 응답 필드 정의


class OverseasOrderSell(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매도 주문 응답")

    # TODO: 응답 필드 정의


class OverseasOrderModify(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 정정 주문 응답")

    # TODO: 응답 필드 정의


class OverseasOrderCancel(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 취소 주문 응답")

    # TODO: 응답 필드 정의


class OverseasOrderOrderableQuantity(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주문가능수량(종목/증거금률별) 응답")

    # TODO: 응답 필드 정의
