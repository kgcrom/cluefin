from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import (
    KiwoomHttpBody,
)


class DomesticOrderBuy(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식 매수주문 응답")

    ord_no: str = Field(default="", title="주문번호", max_length=7)
    dmst_stex_tp: str = Field(default="", title="국내거래소구분", max_length=3, description="KRX, NXT, SOR 중 하나")


class DomesticOrderSell(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식 매도주문 응답")

    ord_no: str = Field(default="", title="주문번호", max_length=7)
    dmst_stex_tp: str = Field(default="", title="국내거래소구분", max_length=3, description="KRX, NXT, SOR 중 하나")


class DomesticOrderModify(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식 정정주문 응답")

    ord_no: str = Field(default="", title="주문번호", max_length=7)
    base_orig_ord_no: str = Field(default="", title="모주문번호", max_length=7, description="정정할 원주문번호")
    stk_cd: str = Field(default="", title="종목코드", max_length=12)
    mdfy_qty: str = Field(default="", title="정정수량", max_length=12, description="정정할 수량")
    dmst_stex_tp: str = Field(default="", title="국내거래소구분", max_length=3, description="KRX, NXT, SOR 중 하나")


class DomesticOrderCancel(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식 취소주문 응답")

    ord_no: str = Field(default="", title="주문번호", max_length=7)
    base_orig_ord_no: str = Field(default="", title="모주문번호", max_length=7)
    cncl_qty: str = Field(default="", title="취소수량", max_length=12)
