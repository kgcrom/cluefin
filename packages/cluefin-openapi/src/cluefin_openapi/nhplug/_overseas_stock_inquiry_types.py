from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugMessage


class OverseasStockBuyableAmountOutput(BaseModel):
    """해외주식 매수가능금액·수량 조회 결과 (`Output_0`)."""

    model_config = ConfigDict(extra="allow")

    fc_dca: float | None = Field(default=None, description="외화예수금 / 길이 15.3")
    mgg_fc_amt: float | None = Field(default=None, description="담보외화금액 / 길이 15.3")
    csh_wtm: float | None = Field(default=None, description="현금증거금 / 길이 15.3")
    re_use_obj_amt: float | None = Field(default=None, description="재사용대상금액 / 길이 15.3")
    re_use_rtr_use_amt: float | None = Field(default=None, description="재사용환원사용금액 / 길이 15.3")
    ect_use_amt: float | None = Field(default=None, description="기타사용금액 / 길이 15.3")
    orr_pbl_amt: float | None = Field(default=None, description="주문가능금액 / 길이 15.3")
    wtm_cur_cd: str | None = Field(default=None, description="증거금통화코드 / 길이 3")
    hld_qty: int | None = Field(default=None, description="보유수량 / 길이 18")
    orr_pbl_qty: int | None = Field(default=None, description="주문가능수량 / 길이 10")
    sll_pbl_qty: int | None = Field(default=None, description="매도가능수량 / 길이 18")
    sll_pbl_qty1: int | None = Field(default=None, description="매도가능수량1 / 길이 18")
    byn_cns_qty: int | None = Field(default=None, description="매수체결수량 / 길이 18")
    sll_cns_qty: int | None = Field(default=None, description="매도체결수량 / 길이 18")
    sll_orr_qty: int | None = Field(default=None, description="매도주문수량 / 길이 18")
    dps_rsc_qty: int | None = Field(default=None, description="처분제한수량 / 길이 18")
    byn_pbl_qty: int | None = Field(default=None, description="매수가능수량 / 길이 18")
    max_pbl_amt: float | None = Field(default=None, description="최대가능금액 / 길이 15.3")
    max_pbl_qty: int | None = Field(default=None, description="최대가능수량 / 길이 18")
    csh_wtm_rt: float | None = Field(default=None, description="현금증거금율 / 길이 8.5")


class OverseasStockBuyableAmount(BaseModel):
    """해외주식 매수가능금액·수량 조회 (`POST /gbstock/inquiry/v1/buyableAmount`) 응답.

    gbstock 스펙의 응답 봉투는 `Output_0` + `message` 이며 rsp_cd/rsp_msg 가
    명시돼 있지 않다. 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockBuyableAmountOutput | None = Field(
        default=None, alias="Output_0", description="매수가능금액·수량 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")
