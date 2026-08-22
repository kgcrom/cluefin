from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugMessage


class OverseasStockOrderOutput(BaseModel):
    """주문 접수 결과 (`Output_0`). 매수·매도·정정·취소 공통."""

    model_config = ConfigDict(extra="allow")

    amn_tab_cd: str | None = Field(default=None, description="관리팀점코드 / 길이 4")
    orr_no: int | None = Field(default=None, description="주문번호 / 길이 10")


class OverseasStockOrderBuy(BaseModel):
    """해외주식 주문매수 (`POST /gbstock/order/v1/buy`) 응답.

    gbstock 스펙의 응답 봉투는 `Output_0` + `message` 이며 rsp_cd/rsp_msg 가
    명시돼 있지 않다. 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockOrderSell(BaseModel):
    """해외주식 주문매도 (`POST /gbstock/order/v1/sell`) 응답."""

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockOrderModify(BaseModel):
    """해외주식 정정취소주문정정 (`POST /gbstock/order/v1/modify`) 응답."""

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockOrderCancel(BaseModel):
    """해외주식 정정취소주문취소 (`POST /gbstock/order/v1/cancel`) 응답."""

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")
