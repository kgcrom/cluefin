from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.nhplug._model import NHPlugAssetHttpBody


class KrStockInquiryBalanceAccountOutput(BaseModel):
    """주식잔고조회 계좌 종합 정보 (Output_0).

    순자산금액·총자산금액·총매수금액·총평가금액·총평가손익은 보유한 잔고를 모두
    조회한 이후에만 제공된다(스펙 설명).
    """

    model_config = ConfigDict(extra="allow")

    dca: int | None = Field(default=None, description="예수금 / 길이 18")
    nxt_dd_dca: int | None = Field(default=None, description="익일예수금 / 길이 15 / D+1 예수금")
    nxt2_dd_dca: int | None = Field(default=None, description="익익일예수금 / 길이 18 / D+2 예수금")
    # 스펙은 아래 5개를 string 으로 명세하지만 실측(2026-08-22, 모의)에는 int 로 온다
    # (`orr_pbl_amt1` 에서 확인 — sibling 필드인 orr_pbl_amt2/3/4 는 스펙상으로도 int).
    # int|str Union 으로 두 표현을 모두 허용한다.
    fc_dca: int | str | None = Field(default=None, description="외화예수금 / 길이 18")
    fc_mgg_amt: int | str | None = Field(default=None, description="외화담보금액 / 길이 18")
    fc_orr_pbl_amt: int | str | None = Field(default=None, description="외화주문가능금액 / 길이 18")
    drn_pbl_amt: int | None = Field(default=None, description="출금가능금액 / 길이 18")
    fnn_amt: int | str | None = Field(default=None, description="융자금액 / 길이 18")
    mgg_rt: float | None = Field(default=None, description="담보비율 / 길이 11.8")
    rit_eal_amt: int | str | None = Field(default=None, description="권리평가금액 / 길이 18")
    orr_pbl_amt: int | str | None = Field(default=None, description="주문가능금액 / 길이 18")
    nas_amt: int | None = Field(default=None, description="순자산금액 / 길이 18")
    tot_aet_amt: int | None = Field(default=None, description="총자산금액 / 길이 18")
    tot_byn_amt: int | None = Field(default=None, description="총매수금액 / 길이 18")
    tot_eal_amt: int | None = Field(default=None, description="총평가금액 / 길이 18")
    tot_eal_pls: int | None = Field(default=None, description="총평가손익 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    rba: int | None = Field(default=None, description="미수금 / 길이 18")
    int_ny_pmt_amt: int | None = Field(default=None, description="이자미납부금액 / 길이 18")
    ny_rdp_amt: int | None = Field(default=None, description="미상환금액 / 길이 18")
    ect_lga: int | None = Field(default=None, description="기타대여금 / 길이 18")
    lon_amt: int | None = Field(default=None, description="대출금액 / 길이 18")
    sba_amt: int | None = Field(default=None, description="대용금액 / 길이 18")
    orr_pbl_amt1: int | str | None = Field(
        default=None, description="주문가능금액1 / 길이 18 / 20%주문가능금액 (스펙 string, 실측 int — 2026-08-22)"
    )
    orr_pbl_amt2: int | None = Field(default=None, description="주문가능금액2 / 길이 18 / 30%주문가능금액")
    orr_pbl_amt3: int | None = Field(default=None, description="주문가능금액3 / 길이 18 / 40%주문가능금액")
    orr_pbl_amt4: int | None = Field(default=None, description="주문가능금액4 / 길이 18 / 100%주문가능금액")
    slo_mgg_amt: int | None = Field(default=None, description="대주담보금액 / 길이 18")
    csh_wtm: int | None = Field(default=None, description="현금증거금 / 길이 18")
    sba_wtm: int | None = Field(default=None, description="대용증거금 / 길이 18")
    sll_edn_amt: int | None = Field(default=None, description="매도증거금액 / 길이 18")
    cfd_pdt_tp_nm: str | None = Field(default=None, description="신용상품유형명 / 길이 20")
    act_atv_tp_dtl_cd: str | None = Field(
        default=None, description="계좌활동유형세부코드 / 길이 3 / 101: 활동 102: 휴면 401: 고객요청폐쇄"
    )
    act_no: str | None = Field(default=None, description="계좌번호 / 길이 11")


class KrStockInquiryBalanceHoldingOutput(BaseModel):
    """주식잔고조회 보유 종목별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    pdt_tp_nm: str | None = Field(default=None, description="상품유형명 / 길이 50")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    tp_cd_nm: str | None = Field(default=None, description="유형코드명 / 길이 30")
    itg_bnc_qty: float | None = Field(default=None, description="통합잔고수량 / 길이 21.6")
    ny_stl_qty: float | None = Field(default=None, description="미결제수량 / 길이 21.6")
    rsdl_qty: float | None = Field(default=None, description="잔량수량 / 길이 21.6")
    phs_pr: int | None = Field(default=None, description="매입가격 / 길이 18")
    now_pr: int | None = Field(default=None, description="현재가격 / 길이 18")
    byn_amt: int | str | None = Field(
        default=None, description="매수금액 / 길이 18 (스펙 string, sibling 금액 필드처럼 실측 int 가능성)"
    )
    eal_amt: int | None = Field(default=None, description="평가금액 / 길이 18")
    eal_pls_amt: int | None = Field(default=None, description="평가손익금액 / 길이 18")
    sll_amt: int | None = Field(default=None, description="매도금액 / 길이 18")
    sll_pls_amt: int | None = Field(default=None, description="매도손익금액 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    syn_ttn_dit_cd: str | None = Field(default=None, description="종합과세구분코드 / 길이 1")
    syn_ttn_dit_cd_nm: str | None = Field(default=None, description="종합과세구분코드명 / 길이 20")
    crm_aet_cfc_cd: str | None = Field(default=None, description="CRM자산분류코드 / 길이 2")
    ctc_int_rt: str | None = Field(default=None, description="약정이자율 / 길이 11.8")
    lon_byn_dt: str | None = Field(default=None, description="대출매수일자 / 길이 8")
    xrn_dt: str | None = Field(default=None, description="만기일자 / 길이 8")
    wtm_rt: str | None = Field(default=None, description="증거금율 / 길이 10")
    lon_bnc_amt: int | None = Field(default=None, description="대출잔고금액 / 길이 18")
    iem_mlf_cd: str | None = Field(default=None, description="종목중분류코드 / 길이 5")
    itg_bnc_tp_cd: str | None = Field(default=None, description="통합잔고유형코드 / 길이 3")


class KrStockInquiryBalance(NHPlugAssetHttpBody):
    """주식잔고조회 (`POST /krstock/inquiry/v1/balance`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryBalanceAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 종합 정보"
    )
    output_1: list[KrStockInquiryBalanceHoldingOutput] | None = Field(
        default=None, alias="Output_1", description="보유 종목별 상세 목록"
    )
