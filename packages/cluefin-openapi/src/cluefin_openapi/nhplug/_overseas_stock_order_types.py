from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugAssetHttpBody


class OverseasStockOrderOutput(BaseModel):
    """주문 접수 결과 (`Output_0`). 매수·매도·정정·취소 공통."""

    model_config = ConfigDict(extra="allow")

    amn_tab_cd: str | None = Field(default=None, description="관리팀점코드 / 길이 4")
    orr_no: int | None = Field(default=None, description="주문번호 / 길이 10")


class OverseasStockOrderBuy(NHPlugAssetHttpBody):
    """해외주식 주문매수 (`POST /gbstock/order/v1/buy`) 응답.

    블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class OverseasStockOrderSell(NHPlugAssetHttpBody):
    """해외주식 주문매도 (`POST /gbstock/order/v1/sell`) 응답."""

    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class OverseasStockOrderModify(NHPlugAssetHttpBody):
    """해외주식 정정취소주문정정 (`POST /gbstock/order/v1/modify`) 응답."""

    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class OverseasStockOrderCancel(NHPlugAssetHttpBody):
    """해외주식 정정취소주문취소 (`POST /gbstock/order/v1/cancel`) 응답."""

    output_0: OverseasStockOrderOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class OverseasStockOrderReservedSubmitOutput(BaseModel):
    """예약주문접수 결과 (`Output_0`)."""

    model_config = ConfigDict(extra="allow")

    bkg_rtn_orr_no: int | None = Field(default=None, description="예약접수주문번호 / 길이 10")


class OverseasStockOrderReservedSubmit(NHPlugAssetHttpBody):
    """해외주식 예약주문접수 (`POST /gbstock/order/v1/reservedSubmit`) 응답."""

    output_0: OverseasStockOrderReservedSubmitOutput | None = Field(
        default=None, alias="Output_0", description="예약주문접수 결과"
    )


class OverseasStockOrderReservedCancelOutput(BaseModel):
    """예약주문접수취소 결과 (`Output_0`)."""

    model_config = ConfigDict(extra="allow")

    wrk_rlt_cd: str | None = Field(default=None, description="작업결과코드 / 길이 5")


class OverseasStockOrderReservedCancel(NHPlugAssetHttpBody):
    """해외주식 예약주문접수취소 (`POST /gbstock/order/v1/reservedCancel`) 응답."""

    output_0: OverseasStockOrderReservedCancelOutput | None = Field(
        default=None, alias="Output_0", description="예약주문접수취소 결과"
    )
