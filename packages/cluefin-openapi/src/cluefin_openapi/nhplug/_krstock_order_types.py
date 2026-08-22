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


class KrStockOrderCancel(NHPlugAssetHttpBody):
    """주식주문(정정취소) 취소 (`POST /krstock/order/v1/cancel`) 응답."""

    output_0: KrStockOrderAmendedOutput | None = Field(default=None, alias="Output_0", description="취소 접수 결과")


class KrStockOrderReservedOrderOutput(BaseModel):
    """주식예약주문 접수 결과 — 신규·정정취소 계열과 달리 전용 스키마(입력값 표시 위주)다."""

    model_config = ConfigDict(extra="allow")

    bkg_orr_no: int | None = Field(default=None, description="예약주문번호 / 길이 10 / 예약 접수된 번호")
    act_no: str | None = Field(default=None, description="계좌번호 / 길이 11 / 입력값 표시")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12 / 입력값 표시")
    sby_dit_cd: str | None = Field(default=None, description="매매구분코드 / 길이 1 / 입력값 표시 (1.매도 2.매수)")
    frs_sba_orr_yn: str | None = Field(default=None, description="선물대용주문여부 / 길이 1 / 입력값 표시")
    nmn_pr_tp_cd: str | None = Field(default=None, description="호가유형코드 / 길이 2 / 입력값 표시")
    cfd_lon_cd: str | None = Field(default=None, description="신용대출코드 / 길이 2 / 입력값 표시")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8 / 입력값 표시 (YYYYMMDD)")
    orr_qty: str | None = Field(default=None, description="주문수량 / 길이 18 / 입력값 표시")
    orr_uit_pr: str | None = Field(default=None, description="주문단가 / 길이 18 / 입력값 표시")
    aca_tel_no: str | None = Field(default=None, description="연락처전화번호 / 길이 20 / 입력값 표시 — 개인정보")
    bkg_orr_tp_cd: str | None = Field(default=None, description="예약주문유형코드 / 길이 1 / 입력값 표시")
    bkg_orr_sta_dt: str | None = Field(default=None, description="예약주문시작일자 / 길이 8 / 입력값 표시 (YYYYMMDD)")
    bkg_orr_end_dt: str | None = Field(default=None, description="예약주문종료일자 / 길이 8 / 입력값 표시 (YYYYMMDD)")
    bkg_orr_enf_tp_cd: str | None = Field(default=None, description="예약주문집행유형코드 / 길이 1 / 입력값 표시")
    end_pr_cmp_ftw_amt: str | None = Field(default=None, description="종가대비등락폭금액 / 길이 18 / 입력값 표시")
    orr_pr_rge_hlm_pr: str | None = Field(default=None, description="주문가격범위상한가 / 길이 18 / 입력값 표시")
    orr_pr_rge_llm_pr: str | None = Field(default=None, description="주문가격범위하한가 / 길이 18 / 입력값 표시")
    pwd: str | None = Field(
        default=None, description="비밀번호 / 길이 8 / 입력값 표시 — 민감정보(계좌 비밀번호), 로그·출력에 남기지 말 것"
    )


class KrStockOrderReservedOrder(NHPlugAssetHttpBody):
    """주식예약주문 (`POST /krstock/order/v1/reservedOrder`) 응답."""

    output_0: KrStockOrderReservedOrderOutput | None = Field(
        default=None, alias="Output_0", description="예약주문 접수 결과"
    )


class KrStockOrderReservedCancelOutput(BaseModel):
    """주식예약주문취소 접수 결과 — 신규·정정취소·예약주문 계열과 다른 전용 스키마(입력값 표시)다."""

    model_config = ConfigDict(extra="allow")

    act_no: str | None = Field(default=None, description="계좌번호 / 길이 11 / 입력값 표시")
    sby_dit_cd: str | None = Field(default=None, description="매매구분코드 / 길이 1 / 입력값 표시 (1.매도 2.매수)")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12 / 입력값 표시")
    bkg_orr_no: int | None = Field(default=None, description="예약주문번호 / 길이 10 / 입력값 표시")
    bkg_orr_tp_cd: str | None = Field(default=None, description="예약주문유형코드 / 길이 1 / 입력값 표시")
    bkg_rtn_dt: str | None = Field(default=None, description="예약접수일자 / 길이 8 / 입력값 표시 (YYYYMMDD)")


class KrStockOrderReservedCancel(NHPlugAssetHttpBody):
    """주식예약주문취소 (`POST /krstock/order/v1/reservedCancel`) 응답."""

    output_0: KrStockOrderReservedCancelOutput | None = Field(
        default=None, alias="Output_0", description="예약주문취소 접수 결과"
    )
