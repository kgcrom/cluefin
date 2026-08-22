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


class KrStockInquiryDailyOrderExecutionCustomerOutput(BaseModel):
    """주식일별주문체결조회 고객 정보 (Output_0).

    스펙은 Output_0 을 Object 로 선언하지만 스펙 자체의 x-schema-warning 이 예시
    응답은 Array 라고 명시한다 — `KrStockInquiryDailyOrderExecution.output_0` 에서
    object/array 둘 다 허용하는 Union 으로 받는다.
    """

    model_config = ConfigDict(extra="allow")

    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")


class KrStockInquiryDailyOrderExecutionOutput(BaseModel):
    """주식일별주문체결조회 주문·체결 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    itg_orr_no: int | None = Field(default=None, description="통합주문번호 / 길이 11")
    orr_mkt_cd_nm: str | None = Field(default=None, description="주문시장코드명 / 길이 50")
    mo_itg_orr_no: str | None = Field(default=None, description="모통합주문번호 / 길이 11")
    org_itg_orr_no: int | None = Field(default=None, description="원통합주문번호 / 길이 11")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 50")
    sby_dit_cd_nm: str | None = Field(default=None, description="매매구분코드명 / 길이 50")
    cor_can_dit_cd_nm: str | None = Field(default=None, description="정정취소구분코드명 / 길이 4")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")
    cfd_lon_cd: str | None = Field(
        default=None,
        description="신용대출코드 / 길이 20 / 00.일반거래 01.유통융자 02.자기융자 03.유통대주 04.자기대주 10.매입자금대출",
    )
    nmn_pr_tp_cd_nm: str | None = Field(default=None, description="호가유형코드명 / 길이 30")
    orr_cnd_dit_cd_nm: str | None = Field(default=None, description="주문조건구분코드명 / 길이 60")
    orr_qty: int | None = Field(default=None, description="주문수량 / 길이 19")
    orr_pr: float | None = Field(default=None, description="주문가격 / 길이 15.3")
    tot_cns_qty: int | None = Field(default=None, description="총체결수량 / 길이 23")
    cns_avg_uit_pr: float | None = Field(default=None, description="체결평균단가 / 길이 15.3")
    cns_amt: int | None = Field(default=None, description="체결금액 / 길이 16")
    cns_cnt: int | None = Field(default=None, description="체결건수 / 길이 19")
    ny_cns_qty: int | None = Field(default=None, description="미체결수량 / 길이 23")
    cor_qty: str | None = Field(default=None, description="정정수량 / 길이 19")
    can_qty: int | None = Field(default=None, description="취소수량 / 길이 19")
    orr_tm: str | None = Field(default=None, description="주문시각 / 길이 9")
    orr_mdi: str | None = Field(default=None, description="주문매체 / 길이 20")
    bnd_byn_dt: str | None = Field(default=None, description="채권매수일자 / 길이 8")
    syn_ttn_dit_cd_nm: str | None = Field(default=None, description="종합과세구분코드명 / 길이 50")
    orr_rjt_rsn_cd_nm: str | None = Field(default=None, description="주문거부사유코드명 / 길이 4")
    pcs_emp_no: str | None = Field(default=None, description="처리사원번호 / 길이 6")
    rmt_mkt_cd: str | None = Field(default=None, description="요청시장코드 / 길이 3 / SOR/KRX/NXT")
    sor_mkt_sli_yn: str | None = Field(default=None, description="SOR시장분할여부 / 길이 1 / Y.분할 N.미분할")
    krx_lnt_opi_sec_co_cd: str | None = Field(default=None, description="거래소대량상대증권회사코드 / 길이 5")
    krx_lnt_opi_act_no: str | None = Field(default=None, description="거래소대량상대계좌번호 / 길이 12")
    krx_lnt_cnf_cpl_hur: str | None = Field(default=None, description="거래소대량협의완료시간 / 길이 9")


class KrStockInquiryDailyOrderExecution(NHPlugAssetHttpBody):
    """주식일별주문체결조회 (`POST /krstock/inquiry/v1/dailyOrderExecution`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: (
        list[KrStockInquiryDailyOrderExecutionCustomerOutput] | KrStockInquiryDailyOrderExecutionCustomerOutput | None
    ) = Field(default=None, alias="Output_0", description="고객 정보 (스펙은 Object, 실제 예시는 Array — 둘 다 허용)")
    output_1: list[KrStockInquiryDailyOrderExecutionOutput] | None = Field(
        default=None, alias="Output_1", description="주문·체결 상세 목록"
    )
