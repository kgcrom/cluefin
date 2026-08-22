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


class KrStockInquiryBuyableQuantityOutput(BaseModel):
    """매수가능수량조회 결과 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    sll_ctc_amt1: str | None = Field(default=None, description="매도약정금액1 / 길이 18 / 전일 매도 약정금액")
    byn_ctc_amt1: str | None = Field(default=None, description="매수약정금액1 / 길이 18 / 전일 매수 약정금액")
    sdr_xps1: str | None = Field(default=None, description="제비용1 / 길이 18 / 전일 제비용")
    dca: int | None = Field(default=None, description="예수금 / 길이 18 / 당일 예수금")
    sll_ctc_amt: str | None = Field(default=None, description="매도약정금액 / 길이 18 / 당일 매도 약정금액")
    ost_byn_ctc_amt: str | None = Field(default=None, description="매수약정금액 / 길이 18 / 당일 매수 약정금액")
    sdr_xps: str | None = Field(default=None, description="제비용 / 길이 18 / 당일 제비용")
    nxt_dd_dca: int | None = Field(default=None, description="익일예수금 / 길이 18 / D+1 예수금")
    nxt2_dd_dca: int | None = Field(default=None, description="익익일예수금 / 길이 18 / D+2 예수금")
    byn_ny_cns_orr_amt: str | None = Field(
        default=None, description="매수미체결주문금액 / 길이 18 / D+2 매수미체결 주문금액"
    )
    ost_fee: int | None = Field(default=None, description="수수료 / 길이 18 / D+2 수수료")
    max_pbl_amt: int | None = Field(
        default=None, description="최대가능금액 / 길이 18 / 조회구분 1. 현금 선택시 출력 최대(미수) 가능금액"
    )
    max_pbl_qty: int | None = Field(default=None, description="최대가능수량 / 길이 18 / 최대(미수) 가능수량")
    rvb_orn_max_pbl_fee: int | None = Field(
        default=None, description="미수발생최대가능수수료 / 길이 18 / 최대(미수) 수수료"
    )
    csh_orr_pbl_amt: int | None = Field(
        default=None, description="현금주문가능금액 / 길이 18 / 미수 미발생 현금 가능금액"
    )
    csh_orr_pbl_qty: int | None = Field(
        default=None, description="현금주문가능수량 / 길이 18 / 미수 미발생 현금 가능수량"
    )
    ost_fee1: int | None = Field(default=None, description="수수료1 / 길이 18 / 미수 미발생 현금 수수료")
    cfd_rvb_orr_pbl_amt: int | None = Field(
        default=None,
        description="신용미수주문가능금액 / 길이 18 / 조회구분 2. 신용(융자대주) 선택시 출력 최대주문가능 매수주문 주문가능금액",
    )
    cfd_rvb_orr_pbl_qty: int | None = Field(
        default=None, description="신용미수주문가능수량 / 길이 18 / 최대주문가능 매수주문 주문가능수량"
    )
    cfd_max_pbl_fee: int | None = Field(
        default=None, description="신용최대가능수수료 / 길이 18 / 최대주문가능 매수주문 수수료"
    )
    cfd_orr_pbl_amt: int | None = Field(
        default=None, description="신용주문가능금액 / 길이 18 / 미수미발생 매수주문 주문가능금액"
    )
    cfd_orr_pbl_qty: int | None = Field(
        default=None, description="신용주문가능수량 / 길이 18 / 미수미발생 매수주문 주문가능수량"
    )
    ost_fee2: int | None = Field(default=None, description="수수료2 / 길이 18 / 미수미발생 매수주문 수수료")
    lmt_amt: int | None = Field(default=None, description="한도금액 / 길이 18 / 미수 미발생 현금 개인한도금액")
    use_lmt_amt: int | None = Field(default=None, description="사용한도금액 / 길이 18 / 미수 미발생 현금 시용한도")
    rmn_lmt: int | None = Field(default=None, description="잔여한도 / 길이 18 / 미수 미발생 현금 잔여한도")
    use_pbl_sba_amt: int | None = Field(
        default=None, description="사용가능대용금액 / 길이 18 / 미수 미발생 현금 사용가능대용(종가)"
    )
    use_pbl_csh: int | None = Field(default=None, description="사용가능현금 / 길이 18 / 미수 미발생 현금 사용가능현금")
    orr_pbl_amt1: int | None = Field(
        default=None, description="주문가능금액1 / 길이 18 / 미수 미발생 현금 주문가능(한도적용전)"
    )
    lon_lmt_amt: int | None = Field(
        default=None, description="대출한도금액 / 길이 18 / 조회구분 3.매입자금대출 선택시 출력 대출한도"
    )
    lmt_use_amt: int | None = Field(default=None, description="한도사용금액 / 길이 18 / 한도사용금액")
    rmn_lmt1: int | None = Field(default=None, description="잔여한도1 / 길이 18 / 잔여한도")
    orr_pbl_sba_amt: int | None = Field(default=None, description="주문가능대용금액 / 길이 18 / 주문가능대용")
    orr_pbl_amt2: int | None = Field(default=None, description="주문가능금액2 / 길이 18 / 주문가능금액(한도적용전)")
    orr_pbl_amt3: int | None = Field(default=None, description="주문가능금액3 / 길이 18 / 주문가능금액(한도적용)")
    orr_pbl_qty: int | None = Field(default=None, description="주문가능수량 / 길이 18 / 주문가능수량")
    ost_fee3: int | None = Field(default=None, description="수수료3 / 길이 18 / 수수료")
    int_rt: float | None = Field(default=None, description="이자율 / 길이 11.8 / 이자율")
    orr_pr: str | None = Field(default=None, description="주문가격 / 길이 18")
    rp_eal_amt: str | None = Field(default=None, description="RP평가금액 / 길이 18 / CMA 평가금")
    ny_stl_qty: str | None = Field(default=None, description="미결제수량 / 길이 21.6")


class KrStockInquiryBuyableQuantity(NHPlugAssetHttpBody):
    """매수가능수량조회 (`POST /krstock/inquiry/v1/buyableQuantity`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryBuyableQuantityOutput | None = Field(
        default=None, alias="Output_0", description="매수가능수량 조회 결과"
    )


class KrStockInquirySellableQuantityOutput(BaseModel):
    """매도가능수량조회 결과 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")
    ost_dit_cd: str | None = Field(default=None, description="구분코드 / 길이 1 / 1.현금 또는 신용 2.대출")
    dit_nm: str | None = Field(default=None, description="구분명 / 길이 20")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")
    cfd_lon_cd: str | None = Field(
        default=None,
        description=(
            "신용대출코드 / 길이 2 / 00.현금 01.유통융자 02.자기융자 03.유통대주 04.자기대주 "
            "10.매입자금대출 11.매도담보대출 12.주식담보대출 13.채권담보대출 14.ELS/DLS담보대출 "
            "15.수익증권대출 16.수익환매대출 17.청약자금대출 18.ELS/DLS환매담보대출 19.해외주식담보대출 "
            "20.해외주식매도담보대출 99.종합담보대출 _.해당사항없음"
        ),
    )
    cfd_lon_cd_nm: str | None = Field(default=None, description="신용대출코드명 / 길이 40")
    ttn_tp_cd: str | None = Field(
        default=None,
        description="과세유형코드 / 길이 2 / 01.일반과세 02.비과세 03.세금우대 04.소액부징수 _.해당사항없음",
    )
    ttn_tp_cd_nm: str | None = Field(default=None, description="과세유형코드명 / 길이 40")
    bnc_qty: int | None = Field(default=None, description="잔고수량 / 길이 18")
    sll_ny_stl_qty: str | None = Field(default=None, description="매도미결제수량 / 길이 18.0")
    byn_ny_stl_qty: str | None = Field(default=None, description="매수미결제수량 / 길이 18.0")
    tdt_sll_ny_cns_qty: float | None = Field(default=None, description="당일매도미체결수량 / 길이 18.0")
    sll_pbl_qty: float | None = Field(
        default=None, description="매도가능수량 / 길이 18.0 / 장중(08:00-15:00)까지는 수량단위미만 절사"
    )
    phs_uit_pr: str | None = Field(default=None, description="매입단가 / 길이 18.0")


class KrStockInquirySellableQuantity(NHPlugAssetHttpBody):
    """매도가능수량조회 (`POST /krstock/inquiry/v1/sellableQuantity`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquirySellableQuantityOutput | None = Field(
        default=None, alias="Output_0", description="매도가능수량 조회 결과"
    )


class KrStockInquiryReservedInquiryHeaderOutput(BaseModel):
    """주식예약주문조회 팀점 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    tab_nm: str | None = Field(default=None, description="팀점명 / 길이 50")
    bkg_orr_rtn_dt: str | None = Field(default=None, description="예약주문접수일자 / 길이 8")


class KrStockInquiryReservedInquiryOutput(BaseModel):
    """주식예약주문조회 예약주문 내역 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    act_no: str | None = Field(default=None, description="계좌번호 / 길이 11")
    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")
    amn_tab_nm: str | None = Field(default=None, description="관리팀점명 / 길이 50")
    act_pdt_nm: str | None = Field(default=None, description="계좌상품명 / 길이 60")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    sby_dit_cd_nm: str | None = Field(default=None, description="매매구분코드명 / 길이 50")
    nmn_pr_tp_cd_nm: str | None = Field(default=None, description="호가유형코드명 / 길이 30")
    cfd_lon_cd_nm: str | None = Field(default=None, description="신용대출코드명 / 길이 40")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")
    orr_qty: int | None = Field(default=None, description="주문수량 / 길이 18")
    orr_pr: int | None = Field(default=None, description="주문가격 / 길이 18")
    acl_cns_qty: int | None = Field(default=None, description="누적체결수량 / 길이 18")
    orr_enf_sta_dt: str | None = Field(default=None, description="주문집행시작일자 / 길이 8")
    orr_enf_end_dt: str | None = Field(default=None, description="주문집행종료일자 / 길이 8")
    lst_orr_enf_dt: str | None = Field(default=None, description="최종주문집행일자 / 길이 8")
    bkg_orr_tp_cd_nm: str | None = Field(default=None, description="예약주문유형코드명 / 길이 50")
    bkg_orr_enf_tp_cd_nm: str | None = Field(default=None, description="예약주문집행유형코드명 / 길이 60")
    end_pr_cmp_ftw_amt: int | None = Field(default=None, description="종가대비등락폭금액 / 길이 18")
    orr_pr_rge_hlm_pr: int | None = Field(default=None, description="주문가격범위상한가 / 길이 18")
    orr_pr_rge_llm_pr: int | None = Field(default=None, description="주문가격범위하한가 / 길이 18")
    bkg_orr_can_dit_cd_nm: str | None = Field(default=None, description="예약주문취소구분코드명 / 길이 50")
    rgs_dt: str | None = Field(default=None, description="등록일자 / 길이 8")
    rgs_tm: str | None = Field(default=None, description="등록시각 / 길이 8")
    rgs_emp_no: str | None = Field(default=None, description="등록사원번호 / 길이 6")
    can_dt: str | None = Field(default=None, description="취소일자 / 길이 8")
    can_tm: str | None = Field(default=None, description="취소시각 / 길이 8")
    can_emp_no: str | None = Field(default=None, description="취소사원번호 / 길이 6")
    bkg_orr_rtn_dt: str | None = Field(default=None, description="예약주문접수일자 / 길이 8")
    bkg_rtn_orr_no: int | None = Field(default=None, description="예약접수주문번호 / 길이 10")
    sby_dit_cd: str | None = Field(
        default=None,
        description=(
            "매매구분코드 / 길이 1 / 1.현금매도 2.현금매수 3.대용매도 4.신용매도 5.신용매수 6.대출매도 "
            "7.대출매수 (입력의 매매구분코드(0.전체/1.매도/2.매수)와는 다른 코드 집합)"
        ),
    )
    stk_now_pr: int | None = Field(default=None, description="주식현재가격 / 길이 18")
    te_bkg_orr_ssp_yn: str | None = Field(default=None, description="기간예약주문중단여부 / 길이 1")
    rmt_mkt_cd: str | None = Field(default=None, description="요청시장코드 / 길이 3")


class KrStockInquiryRealizedPnlAccountOutput(BaseModel):
    """주식잔고조회_실현손익 계좌 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")
    rnm_cfm_no: str | None = Field(default=None, description="실명확인번호 / 길이 13")
    act_atv_tp_dtl_cd: str | None = Field(default=None, description="계좌활동유형세부코드 / 길이 3")
    act_amn_tab_cd: str | None = Field(default=None, description="계좌관리팀점코드 / 길이 4")
    act_pdt_llf_cd: str | None = Field(default=None, description="계좌상품대분류코드 / 길이 2")
    tdy_dca: int | None = Field(default=None, description="금일예수금 / 길이 18 / 예수금")
    nxt_dd_dca: int | None = Field(default=None, description="익일예수금 / 길이 18 / D+1 예수금")
    nxt2_dd_dca: int | None = Field(default=None, description="익익일예수금 / 길이 18 / D+2 예수금")
    orr_pbl_amt1: int | None = Field(default=None, description="주문가능금액1 / 길이 18 / 100% 주문가능금액")
    orr_pbl_amt2: int | None = Field(default=None, description="주문가능금액2 / 길이 18 / 20% 주문가능금액")
    orr_pbl_amt3: int | None = Field(default=None, description="주문가능금액3 / 길이 18 / 30% 주문가능금액")
    orr_pbl_amt4: int | None = Field(default=None, description="주문가능금액4 / 길이 18 / 40% 주문가능금액")
    csh_wtm: int | None = Field(default=None, description="현금증거금 / 길이 18")
    sba_wtm: int | None = Field(default=None, description="대용증거금 / 길이 18")
    tdt_byn_amt: int | None = Field(default=None, description="당일매수금액 / 길이 18")
    tdt_sll_amt: int | None = Field(default=None, description="당일매도금액 / 길이 18")
    sdr_xps: int | None = Field(default=None, description="제비용 / 길이 18 / 당일매매제비용")
    sby_pls_amt: int | None = Field(default=None, description="매매손익금액 / 길이 18 / 당일매매손익")
    eal_amt_sum: int | None = Field(default=None, description="평가금액합계 / 길이 18")
    eal_pls_amt: int | None = Field(default=None, description="평가손익금액 / 길이 18")
    sll_edn_amt: int | None = Field(default=None, description="매도증거금액 / 길이 18 / (-)대용")
    aet_amt: int | None = Field(default=None, description="자산금액 / 길이 18 / D+2 자산금액")
    aet_drs_amt: int | None = Field(default=None, description="자산감소금액 / 길이 18 / 전체매도후자산")
    pft_rt1: float | None = Field(default=None, description="수익율1 / 길이 15.9 / 총수익률")
    pft_rt2: float | None = Field(default=None, description="수익율2 / 길이 15.9 / 당일실현수익률")
    bf_dd_eal_amt2: int | None = Field(default=None, description="전일평가금액2 / 길이 18 / 전일잔고평가금액")
    eal_pls2: int | None = Field(default=None, description="평가손익2 / 길이 18 / 전일대비손익")
    pft_rt3: float | None = Field(default=None, description="수익율3 / 길이 15.9 / 전일대비수익률")
    pna_sum_amt: int | None = Field(default=None, description="원금합계금액 / 길이 18 / 당일매도매입총원금")
    phs_tal: int | None = Field(default=None, description="매입총액 / 길이 18 / 잔고매입총액")
    aet_par_tal: int | None = Field(default=None, description="자산액면총액 / 길이 18 / 실자산금액")
    sdr_xps2: int | None = Field(default=None, description="제비용2 / 길이 18 / 매도제비용합")
    sby_wtm_aly_cd_nm: str | None = Field(default=None, description="매매증거금적용코드명 / 길이 50 / 계좌증거금율")
    pft_rt10: float | None = Field(default=None, description="수익율10 / 길이 15.9 / 잔고평가수익률")


class KrStockInquiryRealizedPnlOutput(BaseModel):
    """주식잔고조회_실현손익 종목별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    itg_bnc_qty: float | None = Field(default=None, description="통합잔고수량 / 길이 18.3")
    orr_pbl_qty: int | None = Field(default=None, description="주문가능수량 / 길이 18")
    bf_dd_byn_qty: int | None = Field(default=None, description="전일매수수량 / 길이 18")
    bf_dd_sll_qty: int | None = Field(default=None, description="전일매도수량 / 길이 18")
    tdt_byn_qty: int | None = Field(default=None, description="당일매수수량 / 길이 18")
    tdt_sll_qty: int | None = Field(default=None, description="당일매도수량 / 길이 18")
    avg_phs_uit_pr: int | None = Field(default=None, description="평균매입단가 / 길이 18")
    sll_uit_pr: int | None = Field(default=None, description="매도단가 / 길이 18")
    phs_amt: int | None = Field(default=None, description="매입금액 / 길이 18")
    rzt_pls_amt: int | None = Field(default=None, description="실현손익금액 / 길이 18")
    sdr_xps: int | None = Field(default=None, description="제비용 / 길이 18 / 당일매매제비용")
    rzt_pft_sby_pls_amt: int | None = Field(default=None, description="실현수익매매손익금액 / 길이 18")
    ost_phs_amt_pna: int | None = Field(default=None, description="매입금액원금 / 길이 18")
    eal_pls: int | None = Field(default=None, description="평가손익 / 길이 18")
    now_pr: int | None = Field(default=None, description="현재가격 / 길이 15")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    sdr_xps1: int | None = Field(default=None, description="제비용1 / 길이 15 / 매도제비용")
    pft_rt7: float | None = Field(default=None, description="수익율7 / 길이 15.9 / 당일실현수익률")
    pft_rt6: float | None = Field(default=None, description="수익율6 / 길이 15.9 / 평가수익률")
    pft_rt2: float | None = Field(default=None, description="수익율2 / 길이 15.9 / 당일실현수익률")
    bnc_tp_dit_cd_nm: str | None = Field(default=None, description="잔고유형구분코드명 / 길이 50")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")
    bf_dd_end_pr: int | None = Field(default=None, description="전일종가 / 길이 18")
    bf_dd_bnc_amt: int | None = Field(default=None, description="전일잔고금액 / 길이 18")
    bf_dd_cmp_ind_amt: int | None = Field(default=None, description="전일대비증감금액 / 길이 18")
    bf_dd_cmp_ind_rt: float | None = Field(default=None, description="전일대비증감율 / 길이 8.3")
    stl_bnc_qty: int | None = Field(default=None, description="결제잔고수량 / 길이 18")
    avg_uit_pr1: int | None = Field(default=None, description="평균단가1 / 길이 15")
    xrn_dt: str | None = Field(default=None, description="만기일자 / 길이 8")
    dit_nm1: str | None = Field(default=None, description="구분명1 / 길이 10")
    bf_dd_sll_amt: int | None = Field(default=None, description="전일매도금액 / 길이 18")
    tdy_sll_amt: int | None = Field(default=None, description="금일매도금액 / 길이 18")
    bf_dd_byn_amt: int | None = Field(default=None, description="전일매수금액 / 길이 18")
    tdy_byn_amt: int | None = Field(default=None, description="금일매수금액 / 길이 18")
    sll_pna: int | None = Field(default=None, description="매도원금 / 길이 18")
    bnc_eal_amt: int | None = Field(default=None, description="잔고평가금액 / 길이 18")


class KrStockInquiryRealizedPnl(NHPlugAssetHttpBody):
    """주식잔고조회_실현손익 (`POST /krstock/inquiry/v1/realizedPnl`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryRealizedPnlAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 종합 정보"
    )
    output_1: list[KrStockInquiryRealizedPnlOutput] | None = Field(
        default=None, alias="Output_1", description="종목별 실현손익 상세 목록"
    )


class KrStockInquiryAssetStatusAccountOutput(BaseModel):
    """투자계좌자산현황조회 계좌 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")
    rnm_cfm_no: str | None = Field(default=None, description="실명확인번호 / 길이 13")
    ctc_tp_cd_nm: str | None = Field(default=None, description="약정유형코드명 / 길이 20")
    act_amn_tab_cd: str | None = Field(default=None, description="계좌관리팀점코드 / 길이 4")
    act_pdt_llf_cd: str | None = Field(default=None, description="계좌상품대분류코드 / 길이 2")
    amn_emp_fnm: str | None = Field(default=None, description="관리사원성명 / 길이 40")
    dca: int | None = Field(default=None, description="예수금 / 길이 18 / 예수금")
    nxt_dd_dca: int | None = Field(default=None, description="익일예수금 / 길이 15 / D+1 예수금")
    nxt2_dd_dca: int | None = Field(default=None, description="익익일예수금 / 길이 18 / D+2 예수금")
    krw_tsl_fc_dca: int | None = Field(default=None, description="원화환산외화예수금 / 길이 18")
    krw_tsl_fc_mgg_amt: int | None = Field(default=None, description="원화환산외화담보금액 / 길이 18")
    krw_tsl_fc_orr_pbl_amt: int | None = Field(default=None, description="원화환산외화주문가능금액 / 길이 18")
    drn_pbl_amt: int | None = Field(default=None, description="출금가능금액 / 길이 18")
    fnn_amt: int | None = Field(default=None, description="융자금액 / 길이 18")
    mgg_rt: float | None = Field(default=None, description="담보비율 / 길이 15.3")
    stk_orr_pbl_amt: int | None = Field(default=None, description="주식주문가능금액 / 길이 18")
    tot_aet_amt: int | None = Field(default=None, description="총자산금액 / 길이 18")
    nas_amt: int | None = Field(default=None, description="순자산금액 / 길이 18")
    tot_byn_amt: int | None = Field(default=None, description="총매수금액 / 길이 18")
    tot_eal_amt: int | None = Field(default=None, description="총평가금액 / 길이 18")
    tot_eal_pls_amt: int | None = Field(default=None, description="총평가손익금액 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    rba: int | None = Field(default=None, description="미수금 / 길이 18")
    int_ny_pmt_amt: int | None = Field(default=None, description="이자미납부금액 / 길이 18")
    ect_lga: int | None = Field(default=None, description="기타대여금 / 길이 18")
    lon_amt: int | None = Field(default=None, description="대출금액 / 길이 18")
    sba_amt: int | None = Field(default=None, description="대용금액 / 길이 18")
    fnc_pdt_orr_pbl_amt: int | None = Field(default=None, description="금융상품주문가능금액 / 길이 18")
    ny_rdp_amt: int | None = Field(default=None, description="미상환금액 / 길이 18")
    cfd_pdt_tp_nm: str | None = Field(default=None, description="신용상품유형명 / 길이 20")
    act_atv_tp_cd_nm: str | None = Field(default=None, description="계좌활동유형코드명 / 길이 50")
    slo_amt: int | None = Field(default=None, description="대주금액 / 길이 18")
    csh_wtm: int | None = Field(default=None, description="현금증거금 / 길이 18")
    fnd_sll_stl_xpn_amt: float | None = Field(default=None, description="펀드매도결제예정금액 / 길이 18.3")
    sbi_dca: int | None = Field(default=None, description="청약예수금 / 길이 18")
    ima_wtm: int | None = Field(default=None, description="IMA증거금 / 길이 18")


class KrStockInquiryAssetStatusOutput(BaseModel):
    """투자계좌자산현황조회 보유 종목별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_mlf_nm: str | None = Field(default=None, description="종목중분류명 / 길이 50")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    bnc_tp_dit_cd_nm: str | None = Field(default=None, description="잔고유형구분코드명 / 길이 50")
    itg_bnc_qty: float | None = Field(default=None, description="통합잔고수량 / 길이 21.6")
    phs_pr: float | None = Field(default=None, description="매입가격 / 길이 15.2")
    now_pr: float | None = Field(default=None, description="현재가격 / 길이 15.2")
    byn_amt: int | None = Field(default=None, description="매수금액 / 길이 18")
    eal_amt: int | None = Field(default=None, description="평가금액 / 길이 18")
    eal_pls_amt: int | None = Field(default=None, description="평가손익금액 / 길이 18")
    sll_pls_amt: float | None = Field(default=None, description="매도손익금액 / 길이 15.3")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    int_rt: float | None = Field(default=None, description="이자율 / 길이 11.8")
    byn_dt: str | None = Field(default=None, description="매수일자 / 길이 8")
    xrn_dt: str | None = Field(default=None, description="만기일자 / 길이 8")
    lon_xrn_dt: str | None = Field(default=None, description="대출만기일자 / 길이 8")
    syn_ttn_dit_cd: str | None = Field(default=None, description="종합과세구분코드 / 길이 1")
    syn_ttn_dit_cd_nm: str | None = Field(default=None, description="종합과세구분코드명 / 길이 50")
    crm_aet_cfc_cd: str | None = Field(default=None, description="CRM자산분류코드 / 길이 2")
    iem_mlf_cd: str | None = Field(default=None, description="종목중분류코드 / 길이 5")
    byn_cim_qty: int | None = Field(default=None, description="매수청구수량 / 길이 18")
    rth_qty: int | None = Field(default=None, description="실물수량 / 길이 18")
    ctc_int_rt: float | None = Field(default=None, description="약정이자율 / 길이 11.8")
    lon_bnc_amt: int | None = Field(default=None, description="대출잔고금액 / 길이 18")
    cur_cd: str | None = Field(default=None, description="통화코드 / 길이 3")
    fc_sec_trd_nat_cd: str | None = Field(default=None, description="외화증권거래국가코드 / 길이 3")
    nat_cd_nm: str | None = Field(default=None, description="국가코드명 / 길이 40")
    itg_bnc_tp_cd: str | None = Field(default=None, description="통합잔고유형코드 / 길이 3")
    tck_iem_cd: str | None = Field(default=None, description="티커종목코드 / 길이 12")


class KrStockInquiryAssetStatus(NHPlugAssetHttpBody):
    """투자계좌자산현황조회 (`POST /krstock/inquiry/v1/assetStatus`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryAssetStatusAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 종합 정보"
    )
    output_1: list[KrStockInquiryAssetStatusOutput] | None = Field(
        default=None, alias="Output_1", description="보유 종목별 상세 목록"
    )


class KrStockInquiryDailyPnlAccountOutput(BaseModel):
    """실현손익일별합산조회 계좌 종합 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    act_fnm: str | None = Field(default=None, description="계좌성명 / 길이 40")
    # 스펙은 string 으로 명세하지만 실측(2026-08-22, 모의)에는 int 로 온다 — balance 의
    # orr_pbl_amt1 과 같은 divergence. int|str Union 으로 두 표현을 모두 허용한다.
    byn_cst_sum: int | str | None = Field(default=None, description="매수대금합계1 / 길이 18")
    sll_cst_sum: int | str | None = Field(default=None, description="매도대금합계1 / 길이 18")
    pls_amt_sum: int | None = Field(default=None, description="손익금액합계 / 길이 15")
    acl_sdr_xps: int | None = Field(default=None, description="누적제비용 / 길이 18")


class KrStockInquiryDailyPnlOutput(BaseModel):
    """실현손익일별합산조회 일별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    sby_dt: str | None = Field(default=None, description="매매일자 / 길이 8")
    byn_qty: float | None = Field(default=None, description="매수수량 / 길이 18.6")
    byn_amt: int | None = Field(default=None, description="매수금액 / 길이 18")
    byn_fee: int | None = Field(default=None, description="매수수수료 / 길이 18")
    byn_amt_sum: int | None = Field(default=None, description="매수금액합계 / 길이 18")
    sll_qty: float | None = Field(default=None, description="매도수량 / 길이 18.6")
    sll_amt: int | None = Field(default=None, description="매도금액 / 길이 18")
    sll_tax_sum: int | None = Field(default=None, description="매도세금합계 / 길이 18")
    sll_amt_sum: int | None = Field(default=None, description="매도금액합계 / 길이 18")
    pls_amt: int | None = Field(default=None, description="손익금액 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    iem_mlf_cd: str | None = Field(
        default=None,
        description=(
            "종목중분류코드 / 길이 5 / 01001.주식 01002.DR 01003.투자회사 01004.신주인수권증권 "
            "01005.상장REITS 01006.신주인수권증서 01007.ETF 01008.상장수익증권"
        ),
    )


class KrStockInquiryDailyPnl(NHPlugAssetHttpBody):
    """실현손익일별합산조회 (`POST /krstock/inquiry/v1/dailyPnl`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryDailyPnlAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 종합 정보"
    )
    output_1: list[KrStockInquiryDailyPnlOutput] | None = Field(
        default=None, alias="Output_1", description="일별 실현손익 상세 목록"
    )


class KrStockInquiryTradingPnlAccountOutput(BaseModel):
    """종목별실현손익현황조회 계좌 합계 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    byn_qty: float | None = Field(default=None, description="매수수량 / 길이 18.6")
    byn_uit_pr: float | None = Field(default=None, description="매수단가 / 길이 15.3")
    byn_fee: int | None = Field(default=None, description="매수수수료 / 길이 18")
    byn_cnt: int | None = Field(default=None, description="매수건수 / 길이 18")
    byn_amt: int | None = Field(default=None, description="매수금액 / 길이 18")
    sll_qty: float | None = Field(default=None, description="매도수량 / 길이 18.6")
    sll_uit_pr: float | None = Field(default=None, description="매도단가 / 길이 15.3")
    sll_tax_sum: int | None = Field(default=None, description="매도세금합계 / 길이 18")
    sll_cnt: int | None = Field(default=None, description="매도건수 / 길이 18")
    sll_amt: int | None = Field(default=None, description="매도금액 / 길이 18")
    sll_abk_amt: int | None = Field(default=None, description="매도장부금액 / 길이 18")
    pls_amt: int | None = Field(default=None, description="손익금액 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    # 스펙은 string 으로 명세하지만 dailyPnl 의 byn_cst_sum/sll_cst_sum 과 같은
    # "합계" 계열 필드에서 실측 int divergence 가 반복 확인됐다 — int|str Union 으로
    # 선제 완화한다(2026-08-22).
    fee_sum: int | str | None = Field(default=None, description="수수료합계 / 길이 18")
    tax_sum: int | str | None = Field(default=None, description="세금합계 / 길이 18")


class KrStockInquiryTradingPnlOutput(BaseModel):
    """종목별실현손익현황조회 종목별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    byn_qty: float | None = Field(default=None, description="매수수량 / 길이 18.6")
    byn_uit_pr: float | None = Field(default=None, description="매수단가 / 길이 15.3")
    byn_fee: int | None = Field(default=None, description="매수수수료 / 길이 18")
    byn_cnt: int | None = Field(default=None, description="매수건수 / 길이 18")
    byn_amt: int | None = Field(default=None, description="매수금액 / 길이 18")
    sll_qty: float | None = Field(default=None, description="매도수량 / 길이 18.6")
    sll_uit_pr: float | None = Field(default=None, description="매도단가 / 길이 15.3")
    sll_tax_sum: int | None = Field(default=None, description="매도세금합계 / 길이 18")
    sll_cnt: int | None = Field(default=None, description="매도건수 / 길이 18")
    sll_amt: int | None = Field(default=None, description="매도금액 / 길이 18")
    sll_abk_amt: int | None = Field(default=None, description="매도장부금액 / 길이 18")
    pls_amt: int | None = Field(default=None, description="손익금액 / 길이 18")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    fee_sum: int | str | None = Field(default=None, description="수수료합계 / 길이 18")
    tax_sum: int | str | None = Field(default=None, description="세금합계 / 길이 18")
    iem_mlf_cd: str | None = Field(
        default=None,
        description=(
            "종목중분류코드 / 길이 5 / 01001.주식 01002.DR 01003.투자회사 01004.신주인수권증권 "
            "01005.상장REITS 01006.신주인수권증서 01007.ETF 01008.상장수익증권"
        ),
    )


class KrStockInquiryTradingPnl(NHPlugAssetHttpBody):
    """종목별실현손익현황조회 (`POST /krstock/inquiry/v1/tradingPnl`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryTradingPnlAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 합계 정보"
    )
    output_1: list[KrStockInquiryTradingPnlOutput] | None = Field(
        default=None, alias="Output_1", description="종목별 실현손익 상세 목록"
    )


class KrStockInquiryIntegratedMarginAccountOutput(BaseModel):
    """주식통합증거금 현황 계좌 한도 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    fc_orr_pbl_amt3: float | None = Field(default=None, description="외화주문가능금액3 / 길이 15.3 / 주문가능금액")
    cro_sby_stl_amt: int | None = Field(default=None, description="교차매매결제금액 / 길이 18 / 결제금(원)")
    cro_sby_act_yn: str | None = Field(default=None, description="교차매매계좌여부 / 길이 1 / 약정여부")
    lmt_amt: int | None = Field(default=None, description="한도금액 / 길이 18 / 한도금액(원)")
    lmt_use_amt: int | None = Field(default=None, description="한도사용금액 / 길이 18 / 한도사용금액(원)")
    rmn_lmt_amt: int | None = Field(default=None, description="잔여한도금액 / 길이 18 / 한도잔여금액(원)")


class KrStockInquiryIntegratedMarginOutput(BaseModel):
    """주식통합증거금 현황 통화별 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    cur_cd: str | None = Field(default=None, description="통화코드 / 길이 3")
    fc_dca: float | None = Field(default=None, description="외화예수금 / 길이 15.3")
    fc_mgg_amt: float | None = Field(default=None, description="외화담보금액 / 길이 15.3")
    ose_trd_tax: float | None = Field(default=None, description="해외거래세 / 길이 15.3")
    fc_ato_re_sby_obj_amt: float | None = Field(
        default=None, description="외화자동재매매대상금액 / 길이 15.3 / 매도금액"
    )
    fc_orr_pbl_amt: float | None = Field(
        default=None, description="외화주문가능금액 / 길이 15.3 / 자국통화 주문가능금액"
    )
    aly_xcg_rt: float | None = Field(default=None, description="적용환율 / 길이 12.6")
    orr_pbl_amt_csh: int | None = Field(default=None, description="주문가능금액현금 / 길이 18")
    cnv_rt: float | None = Field(default=None, description="전환비율 / 길이 11.8 / 통합증거금 통화간 전환비율")
    krw_tsl_cro_pbl_amt: int | None = Field(
        default=None, description="원화환산교차가능금액 / 길이 18 / 타국통화 통합증거금 가능금액(원)"
    )
    trd_cur_cro_pbl_amt: float | None = Field(
        default=None, description="거래통화교차가능금액 / 길이 15.3 / 타국통화 주문가능금액"
    )
    fc_orr_pbl_amt1: float | None = Field(default=None, description="외화주문가능금액1 / 길이 15.3 / 주문가능금액")
    fc_orr_pbl_amt2: float | None = Field(default=None, description="외화주문가능금액2 / 길이 15.3 / 가능금액")
    trd_cur_cro_use_amt: float | None = Field(default=None, description="거래통화교차사용금액 / 길이 15.3 / 사용금액")


class KrStockInquiryIntegratedMargin(NHPlugAssetHttpBody):
    """주식통합증거금 현황 (`POST /krstock/inquiry/v1/integratedMargin`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다. 스펙상 금액류 필드는 모두 number/integer 로 선언돼 있어
    (balance/dailyPnl/tradingPnl 의 "합계" 필드처럼 string 으로 명세된 필드가 없음)
    int|str 완화가 필요하지 않았다.
    """

    output_0: KrStockInquiryIntegratedMarginAccountOutput | None = Field(
        default=None, alias="Output_0", description="계좌 한도 정보"
    )
    output_1: list[KrStockInquiryIntegratedMarginOutput] | None = Field(
        default=None, alias="Output_1", description="통화별 상세 목록"
    )


class KrStockInquiryRightsHeldHeaderOutput(BaseModel):
    """기간별계좌권리현황조회보유 조회 조건 정보 (Output_0)."""

    model_config = ConfigDict(extra="allow")

    sta_dt: str | None = Field(default=None, description="시작일자 / 길이 8 / YYYYMMDD")


class KrStockInquiryRightsHeldOutput(BaseModel):
    """기간별계좌권리현황조회보유 보유 권리 상세 (Output_1 배열의 각 항목)."""

    model_config = ConfigDict(extra="allow")

    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    bse_dt: str | None = Field(default=None, description="기준일자 / 길이 8 / YYYYMMDD")
    rit_tp_cd: str | None = Field(
        default=None,
        description=(
            "권리유형코드 / 길이 2 / _.해당사항없음 01.배당 02.유상 03.무상 04.매수청구 "
            "05.신주인수권증서 06.뮤추얼 07.ETF분배금 08.선박펀드 09.투융자펀드 10.해외자원개발펀드 "
            "11.Ritz(부동산신탁) 12.ELS상환 13.DLS상환 14.ELW만기결제 15.기타청산 16.전환/상환 "
            "17.ETN분배금 21.흡수합병 22.회사분할 23.주식교환 24.자본감소 25.액면분할 26.액면병합 "
            "27.종목변경 등 (전체 코드 목록은 스펙 참고, 문자·숫자 혼용 코드 다수)"
        ),
    )
    hld_qty: int | None = Field(default=None, description="보유수량 / 길이 18")
    aloc_bse_pr: int | None = Field(default=None, description="배정기준가격 / 길이 18")
    req_amt: int | None = Field(default=None, description="신청금액 / 길이 18")
    aloc_amt_pym_dt: str | None = Field(default=None, description="배정금액지급일자 / 길이 8 / YYYYMMDD")
    ltg_dt: str | None = Field(default=None, description="상장일자 / 길이 8 / YYYYMMDD")
    req_yn: str | None = Field(default=None, description="신청여부 / 길이 1")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 50")
    ldg_brw_dit_cd: str | None = Field(
        default=None,
        description="대여차입구분코드 / 길이 2 / 01.차입 02.대여(주식) 03.대여풀 04.대여(채권) 05.대여(해외주식) 06.대여(해외채권)",
    )
    cln_dit_cd: str | None = Field(default=None, description="유통구분코드 / 길이 2 / 01.일반 02.유통금융 03.유통대주")
    aloc_qty: int | None = Field(default=None, description="배정수량 / 길이 18")
    req_end_dt: str | None = Field(default=None, description="신청종료일자 / 길이 8 / YYYYMMDD")
    req_qty: int | None = Field(default=None, description="신청수량 / 길이 18")
    rit_aloc_amt: int | None = Field(default=None, description="권리배정금액 / 길이 18")
    ltg_iem_cd: str | None = Field(default=None, description="상장종목코드 / 길이 12")
    pcs_yn: str | None = Field(default=None, description="처리여부 / 길이 1")
    hdd_yn: str | None = Field(default=None, description="고배당여부 / 길이 1")
    bkg_sta_dt: str | None = Field(default=None, description="예약시작일자 / 길이 8 / YYYYMMDD")
    bkg_end_dt: str | None = Field(default=None, description="예약종료일자 / 길이 8 / YYYYMMDD")
    rrs_itn_rtn_end_dt: str | None = Field(default=None, description="반대의사접수종료일자 / 길이 8 / YYYYMMDD")
    byn_cim_rtn_end_dt: str | None = Field(default=None, description="매수청구접수종료일자 / 길이 8 / YYYYMMDD")


class KrStockInquiryRightsHeld(NHPlugAssetHttpBody):
    """기간별계좌권리현황조회보유 (`POST /krstock/inquiry/v1/rightsHeld`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryRightsHeldHeaderOutput | None = Field(
        default=None, alias="Output_0", description="조회 조건 정보"
    )
    output_1: list[KrStockInquiryRightsHeldOutput] | None = Field(
        default=None, alias="Output_1", description="보유 권리 상세 목록"
    )


class KrStockInquiryReservedInquiry(NHPlugAssetHttpBody):
    """주식예약주문조회 (`POST /krstock/inquiry/v1/reservedInquiry`) 응답.

    연속조회를 지원한다 — 응답 헤더 `cts_flag` 가 "Y" 면 그 `cts` 값을 다음 호출에
    전달해 이어받는다.
    """

    output_0: KrStockInquiryReservedInquiryHeaderOutput | None = Field(
        default=None, alias="Output_0", description="팀점 정보"
    )
    output_1: list[KrStockInquiryReservedInquiryOutput] | None = Field(
        default=None, alias="Output_1", description="예약주문 내역 목록"
    )
