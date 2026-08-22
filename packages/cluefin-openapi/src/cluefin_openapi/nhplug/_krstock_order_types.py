from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugAssetHttpBody


class KrStockOrderPlacedOutput(BaseModel):
    """신규 주문(현금·신용 매수/매도) 공통 접수 결과 — 스펙상 4개 API 의 Output_0 이 동일하다."""

    model_config = ConfigDict(extra="allow")

    orr_gno_tab_cd: str | None = Field(default=None, description="주문채번팀점코드 / 길이 4")
    mkt_orr_no: int | None = Field(default=None, description="시장주문번호 / 정정·취소시 필요한 주문번호")
    sor_fle_id: str | None = Field(default=None, description="SOR파일ID / 요청시장코드 SOR 경우에만 세팅")
    sor_ant_rt1: float | None = Field(default=None, description="SOR배분비율1 (KRX) / SOR 경우에만 세팅")
    sor_ant_rt2: float | None = Field(default=None, description="SOR배분비율2 (NXT) / SOR 경우에만 세팅")
    orr_qty1: int | None = Field(default=None, description="주문수량1 (KRX)")
    orr_qty2: int | None = Field(default=None, description="주문수량2 (NXT)")
    anw_cld_mkt_orr_no1: int | None = Field(default=None, description="신규자시장주문번호1 (KRX)")
    anw_cld_mkt_orr_no2: int | None = Field(default=None, description="신규자시장주문번호2 (NXT)")


class KrStockOrderCashBuy(NHPlugAssetHttpBody):
    """주식주문(현금) 매수 (`POST /krstock/order/v1/cashBuy`) 응답."""

    output_0: KrStockOrderPlacedOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class KrStockOrderCashSell(NHPlugAssetHttpBody):
    """주식주문(현금) 매도 (`POST /krstock/order/v1/cashSell`) 응답."""

    output_0: KrStockOrderPlacedOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class KrStockOrderCreditBuy(NHPlugAssetHttpBody):
    """주식주문(신용) 매수 (`POST /krstock/order/v1/creditBuy`) 응답."""

    output_0: KrStockOrderPlacedOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class KrStockOrderCreditSell(NHPlugAssetHttpBody):
    """주식주문(신용) 매도 (`POST /krstock/order/v1/creditSell`) 응답."""

    output_0: KrStockOrderPlacedOutput | None = Field(default=None, alias="Output_0", description="주문 접수 결과")


class KrStockOrderAmendedOutput(BaseModel):
    """정정·취소(modify·cancel) 공통 접수 결과 — 스펙상 두 API 의 Output_0 이 동일하다."""

    model_config = ConfigDict(extra="allow")

    orr_gno_tab_cd: str | None = Field(default=None, description="주문채번팀점코드 / 길이 4")
    mkt_orr_no: int | None = Field(default=None, description="시장주문번호 / 정정·취소시 필요한 주문번호")
    sor_fle_id: str | None = Field(default=None, description="SOR파일ID / 요청시장코드 SOR 경우에만 세팅")
    can_sor_ant_rt1: float | None = Field(default=None, description="취소SOR배분비율1 (KRX) / SOR 경우에만 세팅")
    can_sor_ant_rt2: float | None = Field(default=None, description="취소SOR배분비율2 (NXT) / SOR 경우에만 세팅")
    can_orr_qty1: int | None = Field(default=None, description="취소주문수량1 (KRX)")
    can_orr_qty2: int | None = Field(default=None, description="취소주문수량2 (NXT)")
    can_cld_mkt_orr_no1: int | None = Field(default=None, description="취소자시장주문번호1 (KRX)")
    can_cld_mkt_orr_no2: int | None = Field(default=None, description="취소자시장주문번호2 (NXT)")


class KrStockOrderModify(NHPlugAssetHttpBody):
    """주식주문(정정취소) 정정 (`POST /krstock/order/v1/modify`) 응답."""

    output_0: KrStockOrderAmendedOutput | None = Field(default=None, alias="Output_0", description="정정 접수 결과")
