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


class OverseasStockUnexecutedItem(BaseModel):
    """해외주식 주문체결내역 조회 결과 항목 (`Output_0` 배열 원소)."""

    model_config = ConfigDict(extra="allow")

    rgs_tm: str | None = Field(default=None, description="등록시각 / 길이 8")
    oss_orr_knd_cd: str | None = Field(default=None, description="해외증권주문종류코드 / 길이 1")
    orr_knd_nm: str | None = Field(default=None, description="주문종류명 / 길이 10")
    orr_no: int | None = Field(default=None, description="주문번호 / 길이 10")
    org_orr_no: int | None = Field(default=None, description="원주문번호 / 길이 10")
    oss_sby_dit_cd: str | None = Field(default=None, description="해외증권매매구분코드 / 길이 1")
    sby_dit_nm: str | None = Field(default=None, description="매매구분명 / 길이 4")
    fc_sec_trd_nat_cd: str | None = Field(default=None, description="외화증권거래국가코드 / 길이 3")
    mkt_dit_cd_nm: str | None = Field(default=None, description="시장구분코드명 / 길이 50")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    orr_qty: int | None = Field(default=None, description="주문수량 / 길이 18")
    fc_orr_uit_pr: float | None = Field(default=None, description="외화주문단가 / 길이 15.6")
    cns_qty: int | None = Field(default=None, description="체결수량 / 길이 18")
    cns_pr: float | None = Field(default=None, description="체결가격 / 길이 15.6")
    ny_cns_orr_qty: int | None = Field(default=None, description="미체결주문수량 / 길이 18")
    cor_can_dit_cd: str | None = Field(default=None, description="정정취소구분코드 / 길이 1")
    cor_can_dit_nm: str | None = Field(default=None, description="정정취소구분명 / 길이 4")
    cor_qty: int | None = Field(default=None, description="정정수량 / 길이 18")
    can_qty: int | None = Field(default=None, description="취소수량 / 길이 18")
    oss_ato_orr_sts_cd: str | None = Field(default=None, description="해외증권자동주문상태코드 / 길이 1")
    orr_sts_nm: str | None = Field(default=None, description="주문상태명 / 길이 6")
    oms_cus_orr_no: str | None = Field(default=None, description="OMS고객주문번호 / 길이 40")
    rjt_rsn_cts: str | None = Field(default=None, description="거부사유내용 / 길이 500")
    ivs_nat_krx_dit_cd: str | None = Field(default=None, description="투자국가거래소구분코드 / 길이 4")
    fix_sgy_tgt_sgy_nm: str | None = Field(default=None, description="FIX전략타겟전략명 / 길이 10")
    fix_orr_pcs_mtd_cd: str | None = Field(default=None, description="FIX주문처리방법코드 / 길이 1")
    orr_pcs_mtd_cd_nm: str | None = Field(default=None, description="주문처리방법코드명 / 길이 40")
    rut_orr_krx_cd: str | None = Field(default=None, description="로이터주문거래소코드 / 길이 3")
    hts_usr_id: str | None = Field(default=None, description="HTS사용자ID / 길이 8")
    usr_ip_adr: str | None = Field(default=None, description="사용자IP주소 / 길이 32")
    cuc_mdi_cd: str | None = Field(default=None, description="통신매체코드 / 길이 2")
    cuc_mdi_cd_nm: str | None = Field(default=None, description="통신매체코드명 / 길이 50")
    ahi_nmn_pr_tp_cd: str | None = Field(default=None, description="현물호가유형코드 / 길이 2")
    ahi_nmn_pr_tp_cd_nm: str | None = Field(default=None, description="현물호가유형코드명 / 길이 20")
    fc_stop_orr_bse_pr: float | None = Field(default=None, description="외화STOP주문기준가격 / 길이 15.6")
    orr_pdt_dit_cd: str | None = Field(default=None, description="주문상품구분코드 / 길이 2")
    orr_dt: str | None = Field(default=None, description="주문일자 / 길이 8")
    csh_wtm_rt: float | None = Field(default=None, description="현금증거금율 / 길이 8.5")
    cfd_lon_cd: str | None = Field(default=None, description="신용대출코드 / 길이 2")
    cfd_lon_cd_nm: str | None = Field(default=None, description="신용대출코드명 / 길이 40")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")


class OverseasStockUnexecuted(BaseModel):
    """해외주식 주문체결내역 조회 (`POST /gbstock/inquiry/v1/unexecuted`) 응답.

    URI 의 `unexecuted` 는 서버 경로일 뿐이며, 실제로는 체결·미체결 내역을
    모두 반환한다. 응답 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: list[OverseasStockUnexecutedItem] | None = Field(
        default=None, alias="Output_0", description="주문체결내역 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockBalanceOutput(BaseModel):
    """해외주식 잔고조회 결과 (`Output_0`)."""

    model_config = ConfigDict(extra="allow")

    abk_amt: int | None = Field(default=None, description="장부금액 / 길이 18")
    eal_amt_sum: int | None = Field(default=None, description="평가금액합계 / 길이 18")
    eal_pls_sum_amt: int | None = Field(default=None, description="평가손익합계금액 / 길이 18")
    krw_pft_rt: float | None = Field(default=None, description="원화수익율 / 길이 15.9")
    krw_dca: int | None = Field(default=None, description="원화예수금 / 길이 18")
    krw_ny_stl_xcl_amt: int | None = Field(default=None, description="원화미결제정산금액 / 길이 18")
    tot_aet_amt: int | None = Field(default=None, description="총자산금액 / 길이 18")
    fc_abk_amt: float | None = Field(default=None, description="외화장부금액 / 길이 15.3")
    fc_eal_amt: float | None = Field(default=None, description="외화평가금액 / 길이 15.3")
    fc_eal_pls_amt: float | None = Field(default=None, description="외화평가손익금액 / 길이 15.3")
    pft_rt: float | None = Field(default=None, description="수익율 / 길이 15.9")
    fc_dca: float | None = Field(default=None, description="외화예수금 / 길이 15.3")
    fc_ny_stl_xcl_amt: float | None = Field(default=None, description="외화미결제정산금액 / 길이 15.3")
    fc_aet_amt: float | None = Field(default=None, description="외화자산금액 / 길이 15.3")
    ptps_ttn_amt: float | None = Field(default=None, description="PTP과세금액 / 길이 15.3")
    ptps_ttn_amt1: float | None = Field(default=None, description="PTP과세금액1 / 길이 15.3")


class OverseasStockBalanceItem(BaseModel):
    """해외주식 잔고조회 결과 항목 (`Output_1` 배열 원소)."""

    model_config = ConfigDict(extra="allow")

    fc_sec_trd_nat_cd: str | None = Field(default=None, description="외화증권거래국가코드 / 길이 3")
    fc_sec_trd_nat_nm: str | None = Field(default=None, description="외화증권거래국가명 / 길이 50")
    iem_cd: str | None = Field(default=None, description="종목코드 / 길이 12")
    oss_iem_eng_nm: str | None = Field(default=None, description="해외증권종목영문명 / 길이 60")
    iem_nm: str | None = Field(default=None, description="외화증권한글명 / 길이 60")
    cns_bse_bnc_qty: int | None = Field(default=None, description="체결기준잔고수량 / 길이 18")
    sll_cns_qty: int | None = Field(default=None, description="매도체결수량 / 길이 18")
    byn_cns_qty: int | None = Field(default=None, description="매수체결수량 / 길이 18")
    sll_pbl_qty1: int | None = Field(default=None, description="매도가능수량1 / 길이 18")
    fc_abk_amt: float | None = Field(default=None, description="외화장부금액 / 길이 15.3")
    krw_abk_amt1: int | None = Field(default=None, description="원화장부금액1 / 길이 18")
    fc_phs_uit_pr: float | None = Field(default=None, description="외화매입단가 / 길이 15.6")
    phs_uit_pr: int | None = Field(default=None, description="매입단가 / 길이 15")
    fc_sec_end_pr: float | None = Field(default=None, description="외화증권종가 / 길이 15.6")
    end_pr: int | None = Field(default=None, description="종가 / 길이 15")
    fc_eal_amt: float | None = Field(default=None, description="외화평가금액 / 길이 15.3")
    krw_eal_amt: int | None = Field(default=None, description="원화평가금액 / 길이 18")
    fc_eal_pls_amt: float | None = Field(default=None, description="외화평가손익금액 / 길이 15.3")
    krw_eal_pls_amt: int | None = Field(default=None, description="원화평가손익금액 / 길이 18")
    eal_pft_rt: float | None = Field(default=None, description="평가수익율 / 길이 15.9")
    eal_pft_rt1: float | None = Field(default=None, description="평가수익율1 / 길이 15.9")
    cur_cd: str | None = Field(default=None, description="통화코드 / 길이 3")
    phs_xcg_rt: float | None = Field(default=None, description="매입환율 / 길이 13.6")
    tdt_sby_bse_xcg_rt: float | None = Field(default=None, description="당일매매기준환율 / 길이 12.6")
    fc_mkt_dit_cd: str | None = Field(default=None, description="외화시장구분코드 / 길이 3")
    fc_sll_pls_amt: float | None = Field(default=None, description="외화매도손익금액 / 길이 15.3")
    krw_sll_pls_amt: int | None = Field(default=None, description="원화매도손익금액 / 길이 18")
    fc_sll_pft_rt: float | None = Field(default=None, description="외화매도수익율 / 길이 15.9")
    krw_sll_pft_rt: float | None = Field(default=None, description="원화매도수익율 / 길이 15.9")
    fc_cns_bse_phs_xps: float | None = Field(default=None, description="외화체결기준매입비 / 길이 15.3")
    krw_cns_bse_phs_xps: int | None = Field(default=None, description="원화체결기준매입비 / 길이 18")
    fc_avg_phs_pr: float | None = Field(default=None, description="외화평균매입가격 / 길이 15.6")
    krw_avg_phs_pr: int | None = Field(default=None, description="원화평균매입가격 / 길이 18")
    fc_fee: float | None = Field(default=None, description="외화수수료 / 길이 15.3")
    krw_fee: int | None = Field(default=None, description="원화수수료 / 길이 18")
    fc_tax_amt: float | None = Field(default=None, description="외화세금금액 / 길이 15.3")
    krw_tax_amt: int | None = Field(default=None, description="원화세금금액 / 길이 18")
    fc_pls_qtr_phs_pr: float | None = Field(default=None, description="외화손익분기매입가격 / 길이 15.6")
    krw_pls_qtr_phs_pr: int | None = Field(default=None, description="원화손익분기매입가격 / 길이 18")
    sby_fee_rt: float | None = Field(default=None, description="매매수수료율 / 길이 15.9")
    fc_stk_lws_sby_fee: float | None = Field(default=None, description="외화주식최저매매수수료 / 길이 15.3")
    cfd_lon_cd_nm: str | None = Field(default=None, description="신용대출코드명 / 길이 8")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8")
    xrn_dt: str | None = Field(default=None, description="만기일자 / 길이 8")


class OverseasStockReservedInquiryItem(BaseModel):
    """해외주식 예약주문조회 결과 항목 (`Output_0` 배열 원소)."""

    model_config = ConfigDict(extra="allow")

    fc_mkt_dit_cd: str | None = Field(
        default=None, description="외화시장구분코드 / 길이 3 / 200.미국 070.일본 120.홍콩 160.상해 170.심천"
    )
    bkg_orr_dt: str | None = Field(default=None, description="예약주문일자 / 길이 8 / YYYYMMDD")
    act_no: str | None = Field(default=None, description="계좌번호 / 길이 11")
    cus_fnm: str | None = Field(default=None, description="고객성명 / 길이 40")
    iem_cd: str | None = Field(default=None, description="티커종목코드 / 길이 12")
    iem_nm: str | None = Field(default=None, description="종목명 / 길이 60")
    cur_cd: str | None = Field(default=None, description="통화코드 / 길이 3 / KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY")
    sby_dit_cd: str | None = Field(default=None, description="매매구분코드 / 길이 1 / 1.매도 2.매수")
    sby_dit_nm: str | None = Field(default=None, description="매매구분명 / 길이 4")
    orr_qty: int | None = Field(default=None, description="주문수량 / 길이 18")
    orr_pr: float | None = Field(default=None, description="주문가격 / 길이 15.6")
    cns_qty: int | None = Field(default=None, description="체결수량 / 길이 18")
    cns_pr: float | None = Field(default=None, description="체결가격 / 길이 15.6")
    bkg_orr_can_yn: str | None = Field(default=None, description="예약주문취소여부 / 길이 1")
    orr_can_dit_nm: str | None = Field(default=None, description="주문취소구분명 / 길이 50")
    bkg_orr_rtn_dt: str | None = Field(default=None, description="예약주문접수일자 / 길이 8 / YYYYMMDD")
    bkg_orr_rtn_tm: str | None = Field(default=None, description="예약주문접수시각 / 길이 8")
    rgs_tab_cd: str | None = Field(default=None, description="등록팀점코드 / 길이 4")
    rgs_emp_no: str | None = Field(default=None, description="등록사원번호 / 길이 6")
    rgs_emp_fnm: str | None = Field(default=None, description="등록사원성명 / 길이 40")
    cct_dt: str | None = Field(default=None, description="해지일자 / 길이 8 / YYYYMMDD")
    cct_tm: str | None = Field(default=None, description="해지시각 / 길이 8")
    cct_emp_no: str | None = Field(default=None, description="해지사원번호 / 길이 6")
    cct_emp_fnm: str | None = Field(default=None, description="해지사원성명 / 길이 40")
    bkg_rtn_orr_no: int | None = Field(default=None, description="예약접수주문번호 / 길이 10")
    orr_sno: int | None = Field(default=None, description="주문일련번호 / 길이 10")
    ost_orr_mdi: str | None = Field(default=None, description="주문매체 / 길이 2")
    orr_cpl_yn: str | None = Field(default=None, description="주문완료여부 / 길이 1")
    ost_pcs_cd: str | None = Field(default=None, description="처리코드 / 길이 5")
    pcs_msg_cts: str | None = Field(default=None, description="처리메시지내용 / 길이 300")
    aca_tel_no: str | None = Field(default=None, description="연락처전화번호 / 길이 20")
    ahi_nmn_pr_tp_cd: str | None = Field(default=None, description="현물호가유형코드 / 길이 2")
    ahi_nmn_pr_tp_cd_nm: str | None = Field(default=None, description="현물호가유형코드명 / 길이 20")
    oss_orr_knd_cd_nm: str | None = Field(default=None, description="해외증권주문종류코드명 / 길이 20")
    ivs_sgy_cd_nm: str | None = Field(default=None, description="투자전략코드명 / 길이 10")
    fc_csh_wtm: float | None = Field(default=None, description="외화현금증거금 / 길이 15.3")
    fc_csh_wtm_fee: float | None = Field(default=None, description="외화현금증거금수수료 / 길이 15.3")
    fc_csh_wtm_tax_amt: float | None = Field(default=None, description="외화현금증거금세금금액 / 길이 15.3")
    fc_csh_wtm_trd_tax: float | None = Field(default=None, description="외화현금증거금거래세 / 길이 15.3")
    fc_mkt_dit_cd_nm: str | None = Field(default=None, description="외화시장구분코드명 / 길이 50")
    bkg_orr_tp_cd: str | None = Field(
        default=None,
        description=(
            "예약주문유형코드 / 길이 1 / 1.\t일반예약주문 / 2.\t잔량기준기간예약주문 / "
            "3.\t수량기준기간예약주문 / 4.\t증거금징수 예약"
        ),
    )
    bkg_orr_tp_cd_nm: str | None = Field(default=None, description="예약주문유형코드명 / 길이 50")
    orr_enf_sta_dt: str | None = Field(default=None, description="주문집행시작일자 / 길이 8 / YYYYMMDD")
    orr_enf_end_dt: str | None = Field(default=None, description="주문집행종료일자 / 길이 8 / YYYYMMDD")
    acl_cns_qty: int | None = Field(default=None, description="누적체결수량 / 길이 18")
    lst_orr_enf_dt: str | None = Field(default=None, description="최종주문집행일자 / 길이 8 / YYYYMMDD")
    rmn_qty: int | None = Field(default=None, description="잔여수량 / 길이 18")
    wtm_cur_knd_cd: str | None = Field(
        default=None, description="증거금통화종류코드 / 길이 1 / 1.거래국가통화 2.원화 3.기타통화"
    )
    cd_nm: str | None = Field(default=None, description="코드명 / 길이 50")
    fc_stop_orr_bse_pr: float | None = Field(default=None, description="외화STOP주문기준가격 / 길이 15.6")
    orr_pdt_dit_cd: str | None = Field(default=None, description="주문상품구분코드 / 길이 2")
    cfd_lon_cd: str | None = Field(default=None, description="신용대출코드 / 길이 2")
    cfd_lon_cd_nm: str | None = Field(default=None, description="신용대출코드명 / 길이 40")
    lon_dt: str | None = Field(default=None, description="대출일자 / 길이 8 / YYYYMMDD")


class OverseasStockReservedInquiry(BaseModel):
    """해외주식 예약주문조회 (`POST /gbstock/inquiry/v1/reservedInquiry`) 응답.

    응답 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: list[OverseasStockReservedInquiryItem] | None = Field(
        default=None, alias="Output_0", description="예약주문내역 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")


class OverseasStockBalance(BaseModel):
    """해외주식 잔고조회 (`POST /gbstock/inquiry/v1/balance`) 응답.

    응답 블록은 데이터가 있을 때만 내려오므로 모두 Optional.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    output_0: OverseasStockBalanceOutput | None = Field(
        default=None, alias="Output_0", description="잔고 요약 조회 결과"
    )
    output_1: list[OverseasStockBalanceItem] | None = Field(
        default=None, alias="Output_1", description="잔고 종목별 조회 결과"
    )
    message: NHPlugMessage | None = Field(default=None, description="공통 응답 메시지 봉투")
