import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const messageSchema = z
  .object({
    msg_code: z.string().nullish(),
    usr_msg: z.string().nullish(),
    msg_lv_code: z.string().nullish(),
    dvlp_msg_yn: z.string().nullish(),
    svc_nm: z.string().nullish(),
    func_nm: z.string().nullish(),
    line_no: z.string().nullish(),
    dvlp_msg: z.string().nullish(),
  })
  .passthrough();

/**
 * 자산군(krstock 등) 공통 응답 봉투.
 *
 * 스펙은 `Output_N` + `message` 구조로 명세하지만 실서버는 `rsp_cd`/`rsp_msg` 를
 * 반환하고 `message` 는 null 이다(모의 실측 2026-08-22). 셋 다 optional 로 둔다.
 */
const assetEnvelope = {
  /** 응답코드 (00000: 성공) */
  rsp_cd: z.string().nullish(),
  /** 응답메시지 */
  rsp_msg: z.string().nullish(),
  /** 스펙상 메시지 봉투 (실서버는 null) */
  message: messageSchema.nullish(),
};
/**
 * 파이썬 모델이 `int`/`float` 로 선언한 숫자 필드.
 *
 * 스펙이 int 라고 해도 실서버가 문자열로 내려주는 사례가 있어(예: 잔고조회
 * `orr_pbl_amt1`, 2026-08-22 모의 실측) 숫자로 강제 변환한다. 빈 문자열은
 * `z.coerce.number()` 가 0 으로 바꿔버리므로 null 로 따로 처리한다.
 */
const num = z.union([z.number(), z.literal('').transform(() => null), z.coerce.number()]);

/** 주식잔고조회 계좌 종합 정보 (Output_0). */
export const krStockInquiryBalanceAccountOutputSchema = z
  .object({
    /** 예수금 */
    dca: num.nullish(),
    /** 익일예수금 — D+1 예수금 */
    nxt_dd_dca: num.nullish(),
    /** 익익일예수금 — D+2 예수금 */
    nxt2_dd_dca: num.nullish(),
    /** 외화예수금 */
    fc_dca: z.union([z.string(), num]).nullish(),
    /** 외화담보금액 */
    fc_mgg_amt: z.union([z.string(), num]).nullish(),
    /** 외화주문가능금액 */
    fc_orr_pbl_amt: z.union([z.string(), num]).nullish(),
    /** 출금가능금액 */
    drn_pbl_amt: num.nullish(),
    /** 융자금액 */
    fnn_amt: z.union([z.string(), num]).nullish(),
    /** 담보비율 */
    mgg_rt: num.nullish(),
    /** 권리평가금액 */
    rit_eal_amt: z.union([z.string(), num]).nullish(),
    /** 주문가능금액 */
    orr_pbl_amt: z.union([z.string(), num]).nullish(),
    /** 순자산금액 */
    nas_amt: num.nullish(),
    /** 총자산금액 */
    tot_aet_amt: num.nullish(),
    /** 총매수금액 */
    tot_byn_amt: num.nullish(),
    /** 총평가금액 */
    tot_eal_amt: num.nullish(),
    /** 총평가손익 */
    tot_eal_pls: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 미수금 */
    rba: num.nullish(),
    /** 이자미납부금액 */
    int_ny_pmt_amt: num.nullish(),
    /** 미상환금액 */
    ny_rdp_amt: num.nullish(),
    /** 기타대여금 */
    ect_lga: num.nullish(),
    /** 대출금액 */
    lon_amt: num.nullish(),
    /** 대용금액 */
    sba_amt: num.nullish(),
    /** 주문가능금액1 — 20%주문가능금액 (스펙 string, 실측 int — 2026-08-22) */
    orr_pbl_amt1: z.union([z.string(), num]).nullish(),
    /** 주문가능금액2 — 30%주문가능금액 */
    orr_pbl_amt2: num.nullish(),
    /** 주문가능금액3 — 40%주문가능금액 */
    orr_pbl_amt3: num.nullish(),
    /** 주문가능금액4 — 100%주문가능금액 */
    orr_pbl_amt4: num.nullish(),
    /** 대주담보금액 */
    slo_mgg_amt: num.nullish(),
    /** 현금증거금 */
    csh_wtm: num.nullish(),
    /** 대용증거금 */
    sba_wtm: num.nullish(),
    /** 매도증거금액 */
    sll_edn_amt: num.nullish(),
    /** 신용상품유형명 */
    cfd_pdt_tp_nm: z.string().nullish(),
    /** 계좌활동유형세부코드 — 101: 활동 102: 휴면 401: 고객요청폐쇄 */
    act_atv_tp_dtl_cd: z.string().nullish(),
    /** 계좌번호 */
    act_no: z.string().nullish(),
  })
  .passthrough();

/** 주식잔고조회 보유 종목별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryBalanceHoldingOutputSchema = z
  .object({
    /** 상품유형명 */
    pdt_tp_nm: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 유형코드명 */
    tp_cd_nm: z.string().nullish(),
    /** 통합잔고수량 */
    itg_bnc_qty: num.nullish(),
    /** 미결제수량 */
    ny_stl_qty: num.nullish(),
    /** 잔량수량 */
    rsdl_qty: num.nullish(),
    /** 매입가격 */
    phs_pr: num.nullish(),
    /** 현재가격 */
    now_pr: num.nullish(),
    /** 매수금액 — 길이 18 (스펙 string, sibling 금액 필드처럼 실측 int 가능성) */
    byn_amt: z.union([z.string(), num]).nullish(),
    /** 평가금액 */
    eal_amt: num.nullish(),
    /** 평가손익금액 */
    eal_pls_amt: num.nullish(),
    /** 매도금액 */
    sll_amt: num.nullish(),
    /** 매도손익금액 */
    sll_pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 종합과세구분코드 */
    syn_ttn_dit_cd: z.string().nullish(),
    /** 종합과세구분코드명 */
    syn_ttn_dit_cd_nm: z.string().nullish(),
    /** CRM자산분류코드 */
    crm_aet_cfc_cd: z.string().nullish(),
    /** 약정이자율 */
    ctc_int_rt: z.string().nullish(),
    /** 대출매수일자 */
    lon_byn_dt: z.string().nullish(),
    /** 만기일자 */
    xrn_dt: z.string().nullish(),
    /** 증거금율 */
    wtm_rt: z.string().nullish(),
    /** 대출잔고금액 */
    lon_bnc_amt: num.nullish(),
    /** 종목중분류코드 */
    iem_mlf_cd: z.string().nullish(),
    /** 통합잔고유형코드 */
    itg_bnc_tp_cd: z.string().nullish(),
  })
  .passthrough();

/** 주식잔고조회 (`POST /krstock/inquiry/v1/balance`) 응답. */
export const krStockInquiryBalanceResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 종합 정보 */
    Output_0: krStockInquiryBalanceAccountOutputSchema.nullish(),
    /** 보유 종목별 상세 목록 */
    Output_1: z.array(krStockInquiryBalanceHoldingOutputSchema).nullish(),
  })
  .passthrough();

/** 주식일별주문체결조회 고객 정보 (Output_0). */
export const krStockInquiryDailyOrderExecutionCustomerOutputSchema = z
  .object({
    /** 고객성명 */
    cus_fnm: z.string().nullish(),
  })
  .passthrough();

/** 주식일별주문체결조회 주문·체결 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryDailyOrderExecutionOutputSchema = z
  .object({
    /** 통합주문번호 */
    itg_orr_no: num.nullish(),
    /** 주문시장코드명 */
    orr_mkt_cd_nm: z.string().nullish(),
    /** 모통합주문번호 */
    mo_itg_orr_no: z.string().nullish(),
    /** 원통합주문번호 */
    org_itg_orr_no: num.nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 매매구분코드명 */
    sby_dit_cd_nm: z.string().nullish(),
    /** 정정취소구분코드명 */
    cor_can_dit_cd_nm: z.string().nullish(),
    /** 대출일자 */
    lon_dt: z.string().nullish(),
    /** 신용대출코드 — 00.일반거래 01.유통융자 02.자기융자 03.유통대주 04.자기대주 10.매입자금대출 */
    cfd_lon_cd: z.string().nullish(),
    /** 호가유형코드명 */
    nmn_pr_tp_cd_nm: z.string().nullish(),
    /** 주문조건구분코드명 */
    orr_cnd_dit_cd_nm: z.string().nullish(),
    /** 주문수량 */
    orr_qty: num.nullish(),
    /** 주문가격 */
    orr_pr: num.nullish(),
    /** 총체결수량 */
    tot_cns_qty: num.nullish(),
    /** 체결평균단가 */
    cns_avg_uit_pr: num.nullish(),
    /** 체결금액 */
    cns_amt: num.nullish(),
    /** 체결건수 */
    cns_cnt: num.nullish(),
    /** 미체결수량 */
    ny_cns_qty: num.nullish(),
    /** 정정수량 */
    cor_qty: z.string().nullish(),
    /** 취소수량 */
    can_qty: num.nullish(),
    /** 주문시각 */
    orr_tm: z.string().nullish(),
    /** 주문매체 */
    orr_mdi: z.string().nullish(),
    /** 채권매수일자 */
    bnd_byn_dt: z.string().nullish(),
    /** 종합과세구분코드명 */
    syn_ttn_dit_cd_nm: z.string().nullish(),
    /** 주문거부사유코드명 */
    orr_rjt_rsn_cd_nm: z.string().nullish(),
    /** 처리사원번호 */
    pcs_emp_no: z.string().nullish(),
    /** 요청시장코드 — SOR/KRX/NXT */
    rmt_mkt_cd: z.string().nullish(),
    /** SOR시장분할여부 — Y.분할 N.미분할 */
    sor_mkt_sli_yn: z.string().nullish(),
    /** 거래소대량상대증권회사코드 */
    krx_lnt_opi_sec_co_cd: z.string().nullish(),
    /** 거래소대량상대계좌번호 */
    krx_lnt_opi_act_no: z.string().nullish(),
    /** 거래소대량협의완료시간 */
    krx_lnt_cnf_cpl_hur: z.string().nullish(),
  })
  .passthrough();

/** 주식일별주문체결조회 (`POST /krstock/inquiry/v1/dailyOrderExecution`) 응답. */
export const krStockInquiryDailyOrderExecutionResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 고객 정보 (스펙은 Object, 실제 예시는 Array — 둘 다 허용) */
    Output_0: z
      .union([
        z.array(krStockInquiryDailyOrderExecutionCustomerOutputSchema),
        krStockInquiryDailyOrderExecutionCustomerOutputSchema,
      ])
      .nullish(),
    /** 주문·체결 상세 목록 */
    Output_1: z.array(krStockInquiryDailyOrderExecutionOutputSchema).nullish(),
  })
  .passthrough();

/** 매수가능수량조회 결과 (Output_0). */
export const krStockInquiryBuyableQuantityOutputSchema = z
  .object({
    /** 매도약정금액1 — 전일 매도 약정금액 */
    sll_ctc_amt1: z.string().nullish(),
    /** 매수약정금액1 — 전일 매수 약정금액 */
    byn_ctc_amt1: z.string().nullish(),
    /** 제비용1 — 전일 제비용 */
    sdr_xps1: z.string().nullish(),
    /** 예수금 — 당일 예수금 */
    dca: num.nullish(),
    /** 매도약정금액 — 당일 매도 약정금액 */
    sll_ctc_amt: z.string().nullish(),
    /** 매수약정금액 — 당일 매수 약정금액 */
    ost_byn_ctc_amt: z.string().nullish(),
    /** 제비용 — 당일 제비용 */
    sdr_xps: z.string().nullish(),
    /** 익일예수금 — D+1 예수금 */
    nxt_dd_dca: num.nullish(),
    /** 익익일예수금 — D+2 예수금 */
    nxt2_dd_dca: num.nullish(),
    /** 매수미체결주문금액 — D+2 매수미체결 주문금액 */
    byn_ny_cns_orr_amt: z.string().nullish(),
    /** 수수료 — D+2 수수료 */
    ost_fee: num.nullish(),
    /** 최대가능금액 — 조회구분 1. 현금 선택시 출력 최대(미수) 가능금액 */
    max_pbl_amt: num.nullish(),
    /** 최대가능수량 — 최대(미수) 가능수량 */
    max_pbl_qty: num.nullish(),
    /** 미수발생최대가능수수료 — 최대(미수) 수수료 */
    rvb_orn_max_pbl_fee: num.nullish(),
    /** 현금주문가능금액 — 미수 미발생 현금 가능금액 */
    csh_orr_pbl_amt: num.nullish(),
    /** 현금주문가능수량 — 미수 미발생 현금 가능수량 */
    csh_orr_pbl_qty: num.nullish(),
    /** 수수료1 — 미수 미발생 현금 수수료 */
    ost_fee1: num.nullish(),
    /** 신용미수주문가능금액 — 조회구분 2. 신용(융자대주) 선택시 출력 최대주문가능 매수주문 주문가능금액 */
    cfd_rvb_orr_pbl_amt: num.nullish(),
    /** 신용미수주문가능수량 — 최대주문가능 매수주문 주문가능수량 */
    cfd_rvb_orr_pbl_qty: num.nullish(),
    /** 신용최대가능수수료 — 최대주문가능 매수주문 수수료 */
    cfd_max_pbl_fee: num.nullish(),
    /** 신용주문가능금액 — 미수미발생 매수주문 주문가능금액 */
    cfd_orr_pbl_amt: num.nullish(),
    /** 신용주문가능수량 — 미수미발생 매수주문 주문가능수량 */
    cfd_orr_pbl_qty: num.nullish(),
    /** 수수료2 — 미수미발생 매수주문 수수료 */
    ost_fee2: num.nullish(),
    /** 한도금액 — 미수 미발생 현금 개인한도금액 */
    lmt_amt: num.nullish(),
    /** 사용한도금액 — 미수 미발생 현금 시용한도 */
    use_lmt_amt: num.nullish(),
    /** 잔여한도 — 미수 미발생 현금 잔여한도 */
    rmn_lmt: num.nullish(),
    /** 사용가능대용금액 — 미수 미발생 현금 사용가능대용(종가) */
    use_pbl_sba_amt: num.nullish(),
    /** 사용가능현금 — 미수 미발생 현금 사용가능현금 */
    use_pbl_csh: num.nullish(),
    /** 주문가능금액1 — 미수 미발생 현금 주문가능(한도적용전) */
    orr_pbl_amt1: num.nullish(),
    /** 대출한도금액 — 조회구분 3.매입자금대출 선택시 출력 대출한도 */
    lon_lmt_amt: num.nullish(),
    /** 한도사용금액 — 한도사용금액 */
    lmt_use_amt: num.nullish(),
    /** 잔여한도1 — 잔여한도 */
    rmn_lmt1: num.nullish(),
    /** 주문가능대용금액 — 주문가능대용 */
    orr_pbl_sba_amt: num.nullish(),
    /** 주문가능금액2 — 주문가능금액(한도적용전) */
    orr_pbl_amt2: num.nullish(),
    /** 주문가능금액3 — 주문가능금액(한도적용) */
    orr_pbl_amt3: num.nullish(),
    /** 주문가능수량 — 주문가능수량 */
    orr_pbl_qty: num.nullish(),
    /** 수수료3 — 수수료 */
    ost_fee3: num.nullish(),
    /** 이자율 — 이자율 */
    int_rt: num.nullish(),
    /** 주문가격 */
    orr_pr: z.string().nullish(),
    /** RP평가금액 — CMA 평가금 */
    rp_eal_amt: z.string().nullish(),
    /** 미결제수량 */
    ny_stl_qty: z.string().nullish(),
  })
  .passthrough();

/** 매수가능수량조회 (`POST /krstock/inquiry/v1/buyableQuantity`) 응답. */
export const krStockInquiryBuyableQuantityResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 매수가능수량 조회 결과 */
    Output_0: krStockInquiryBuyableQuantityOutputSchema.nullish(),
  })
  .passthrough();

/** 매도가능수량조회 결과 (Output_0). */
export const krStockInquirySellableQuantityOutputSchema = z
  .object({
    /** 고객성명 */
    cus_fnm: z.string().nullish(),
    /** 구분코드 — 1.현금 또는 신용 2.대출 */
    ost_dit_cd: z.string().nullish(),
    /** 구분명 */
    dit_nm: z.string().nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 대출일자 */
    lon_dt: z.string().nullish(),
    /** 신용대출코드 — 00.현금 01.유통융자 02.자기융자 03.유통대주 04.자기대주 10.매입자금대출 11.매도담보대출 12.주식담보대출 13.채권담보대출 14.ELS/DLS담보대출 15.수익증권대출 16.수익환매대출 17.청약자금대출 18.ELS/DLS환매담보대출 19.해외주식담보대출 20.해외주식매도담보대출 99.종합담보대출 _.해당사항없음 */
    cfd_lon_cd: z.string().nullish(),
    /** 신용대출코드명 */
    cfd_lon_cd_nm: z.string().nullish(),
    /** 과세유형코드 — 01.일반과세 02.비과세 03.세금우대 04.소액부징수 _.해당사항없음 */
    ttn_tp_cd: z.string().nullish(),
    /** 과세유형코드명 */
    ttn_tp_cd_nm: z.string().nullish(),
    /** 잔고수량 */
    bnc_qty: num.nullish(),
    /** 매도미결제수량 */
    sll_ny_stl_qty: z.string().nullish(),
    /** 매수미결제수량 */
    byn_ny_stl_qty: z.string().nullish(),
    /** 당일매도미체결수량 */
    tdt_sll_ny_cns_qty: num.nullish(),
    /** 매도가능수량 — 장중(08:00-15:00)까지는 수량단위미만 절사 */
    sll_pbl_qty: num.nullish(),
    /** 매입단가 */
    phs_uit_pr: z.string().nullish(),
  })
  .passthrough();

/** 매도가능수량조회 (`POST /krstock/inquiry/v1/sellableQuantity`) 응답. */
export const krStockInquirySellableQuantityResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 매도가능수량 조회 결과 */
    Output_0: krStockInquirySellableQuantityOutputSchema.nullish(),
  })
  .passthrough();

/** 주식예약주문조회 팀점 정보 (Output_0). */
export const krStockInquiryReservedInquiryHeaderOutputSchema = z
  .object({
    /** 팀점명 */
    tab_nm: z.string().nullish(),
    /** 예약주문접수일자 */
    bkg_orr_rtn_dt: z.string().nullish(),
  })
  .passthrough();

/** 주식예약주문조회 예약주문 내역 (Output_1 배열의 각 항목). */
export const krStockInquiryReservedInquiryOutputSchema = z
  .object({
    /** 계좌번호 */
    act_no: z.string().nullish(),
    /** 고객성명 */
    cus_fnm: z.string().nullish(),
    /** 관리팀점명 */
    amn_tab_nm: z.string().nullish(),
    /** 계좌상품명 */
    act_pdt_nm: z.string().nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 매매구분코드명 */
    sby_dit_cd_nm: z.string().nullish(),
    /** 호가유형코드명 */
    nmn_pr_tp_cd_nm: z.string().nullish(),
    /** 신용대출코드명 */
    cfd_lon_cd_nm: z.string().nullish(),
    /** 대출일자 */
    lon_dt: z.string().nullish(),
    /** 주문수량 */
    orr_qty: num.nullish(),
    /** 주문가격 */
    orr_pr: num.nullish(),
    /** 누적체결수량 */
    acl_cns_qty: num.nullish(),
    /** 주문집행시작일자 */
    orr_enf_sta_dt: z.string().nullish(),
    /** 주문집행종료일자 */
    orr_enf_end_dt: z.string().nullish(),
    /** 최종주문집행일자 */
    lst_orr_enf_dt: z.string().nullish(),
    /** 예약주문유형코드명 */
    bkg_orr_tp_cd_nm: z.string().nullish(),
    /** 예약주문집행유형코드명 */
    bkg_orr_enf_tp_cd_nm: z.string().nullish(),
    /** 종가대비등락폭금액 */
    end_pr_cmp_ftw_amt: num.nullish(),
    /** 주문가격범위상한가 */
    orr_pr_rge_hlm_pr: num.nullish(),
    /** 주문가격범위하한가 */
    orr_pr_rge_llm_pr: num.nullish(),
    /** 예약주문취소구분코드명 */
    bkg_orr_can_dit_cd_nm: z.string().nullish(),
    /** 등록일자 */
    rgs_dt: z.string().nullish(),
    /** 등록시각 */
    rgs_tm: z.string().nullish(),
    /** 등록사원번호 */
    rgs_emp_no: z.string().nullish(),
    /** 취소일자 */
    can_dt: z.string().nullish(),
    /** 취소시각 */
    can_tm: z.string().nullish(),
    /** 취소사원번호 */
    can_emp_no: z.string().nullish(),
    /** 예약주문접수일자 */
    bkg_orr_rtn_dt: z.string().nullish(),
    /** 예약접수주문번호 */
    bkg_rtn_orr_no: num.nullish(),
    /** 매매구분코드 — 1.현금매도 2.현금매수 3.대용매도 4.신용매도 5.신용매수 6.대출매도 7.대출매수 (입력의 매매구분코드(0.전체/1.매도/2.매수)와는 다른 코드 집합) */
    sby_dit_cd: z.string().nullish(),
    /** 주식현재가격 */
    stk_now_pr: num.nullish(),
    /** 기간예약주문중단여부 */
    te_bkg_orr_ssp_yn: z.string().nullish(),
    /** 요청시장코드 */
    rmt_mkt_cd: z.string().nullish(),
  })
  .passthrough();

/** 주식잔고조회_실현손익 계좌 종합 정보 (Output_0). */
export const krStockInquiryRealizedPnlAccountOutputSchema = z
  .object({
    /** 고객성명 */
    cus_fnm: z.string().nullish(),
    /** 실명확인번호 */
    rnm_cfm_no: z.string().nullish(),
    /** 계좌활동유형세부코드 */
    act_atv_tp_dtl_cd: z.string().nullish(),
    /** 계좌관리팀점코드 */
    act_amn_tab_cd: z.string().nullish(),
    /** 계좌상품대분류코드 */
    act_pdt_llf_cd: z.string().nullish(),
    /** 금일예수금 — 예수금 */
    tdy_dca: num.nullish(),
    /** 익일예수금 — D+1 예수금 */
    nxt_dd_dca: num.nullish(),
    /** 익익일예수금 — D+2 예수금 */
    nxt2_dd_dca: num.nullish(),
    /** 주문가능금액1 — 100% 주문가능금액 */
    orr_pbl_amt1: num.nullish(),
    /** 주문가능금액2 — 20% 주문가능금액 */
    orr_pbl_amt2: num.nullish(),
    /** 주문가능금액3 — 30% 주문가능금액 */
    orr_pbl_amt3: num.nullish(),
    /** 주문가능금액4 — 40% 주문가능금액 */
    orr_pbl_amt4: num.nullish(),
    /** 현금증거금 */
    csh_wtm: num.nullish(),
    /** 대용증거금 */
    sba_wtm: num.nullish(),
    /** 당일매수금액 */
    tdt_byn_amt: num.nullish(),
    /** 당일매도금액 */
    tdt_sll_amt: num.nullish(),
    /** 제비용 — 당일매매제비용 */
    sdr_xps: num.nullish(),
    /** 매매손익금액 — 당일매매손익 */
    sby_pls_amt: num.nullish(),
    /** 평가금액합계 */
    eal_amt_sum: num.nullish(),
    /** 평가손익금액 */
    eal_pls_amt: num.nullish(),
    /** 매도증거금액 — (-)대용 */
    sll_edn_amt: num.nullish(),
    /** 자산금액 — D+2 자산금액 */
    aet_amt: num.nullish(),
    /** 자산감소금액 — 전체매도후자산 */
    aet_drs_amt: num.nullish(),
    /** 수익율1 — 총수익률 */
    pft_rt1: num.nullish(),
    /** 수익율2 — 당일실현수익률 */
    pft_rt2: num.nullish(),
    /** 전일평가금액2 — 전일잔고평가금액 */
    bf_dd_eal_amt2: num.nullish(),
    /** 평가손익2 — 전일대비손익 */
    eal_pls2: num.nullish(),
    /** 수익율3 — 전일대비수익률 */
    pft_rt3: num.nullish(),
    /** 원금합계금액 — 당일매도매입총원금 */
    pna_sum_amt: num.nullish(),
    /** 매입총액 — 잔고매입총액 */
    phs_tal: num.nullish(),
    /** 자산액면총액 — 실자산금액 */
    aet_par_tal: num.nullish(),
    /** 제비용2 — 매도제비용합 */
    sdr_xps2: num.nullish(),
    /** 매매증거금적용코드명 — 계좌증거금율 */
    sby_wtm_aly_cd_nm: z.string().nullish(),
    /** 수익율10 — 잔고평가수익률 */
    pft_rt10: num.nullish(),
  })
  .passthrough();

/** 주식잔고조회_실현손익 종목별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryRealizedPnlOutputSchema = z
  .object({
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 통합잔고수량 */
    itg_bnc_qty: num.nullish(),
    /** 주문가능수량 */
    orr_pbl_qty: num.nullish(),
    /** 전일매수수량 */
    bf_dd_byn_qty: num.nullish(),
    /** 전일매도수량 */
    bf_dd_sll_qty: num.nullish(),
    /** 당일매수수량 */
    tdt_byn_qty: num.nullish(),
    /** 당일매도수량 */
    tdt_sll_qty: num.nullish(),
    /** 평균매입단가 */
    avg_phs_uit_pr: num.nullish(),
    /** 매도단가 */
    sll_uit_pr: num.nullish(),
    /** 매입금액 */
    phs_amt: num.nullish(),
    /** 실현손익금액 */
    rzt_pls_amt: num.nullish(),
    /** 제비용 — 당일매매제비용 */
    sdr_xps: num.nullish(),
    /** 실현수익매매손익금액 */
    rzt_pft_sby_pls_amt: num.nullish(),
    /** 매입금액원금 */
    ost_phs_amt_pna: num.nullish(),
    /** 평가손익 */
    eal_pls: num.nullish(),
    /** 현재가격 */
    now_pr: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 제비용1 — 매도제비용 */
    sdr_xps1: num.nullish(),
    /** 수익율7 — 당일실현수익률 */
    pft_rt7: num.nullish(),
    /** 수익율6 — 평가수익률 */
    pft_rt6: num.nullish(),
    /** 수익율2 — 당일실현수익률 */
    pft_rt2: num.nullish(),
    /** 잔고유형구분코드명 */
    bnc_tp_dit_cd_nm: z.string().nullish(),
    /** 대출일자 */
    lon_dt: z.string().nullish(),
    /** 전일종가 */
    bf_dd_end_pr: num.nullish(),
    /** 전일잔고금액 */
    bf_dd_bnc_amt: num.nullish(),
    /** 전일대비증감금액 */
    bf_dd_cmp_ind_amt: num.nullish(),
    /** 전일대비증감율 */
    bf_dd_cmp_ind_rt: num.nullish(),
    /** 결제잔고수량 */
    stl_bnc_qty: num.nullish(),
    /** 평균단가1 */
    avg_uit_pr1: num.nullish(),
    /** 만기일자 */
    xrn_dt: z.string().nullish(),
    /** 구분명1 */
    dit_nm1: z.string().nullish(),
    /** 전일매도금액 */
    bf_dd_sll_amt: num.nullish(),
    /** 금일매도금액 */
    tdy_sll_amt: num.nullish(),
    /** 전일매수금액 */
    bf_dd_byn_amt: num.nullish(),
    /** 금일매수금액 */
    tdy_byn_amt: num.nullish(),
    /** 매도원금 */
    sll_pna: num.nullish(),
    /** 잔고평가금액 */
    bnc_eal_amt: num.nullish(),
  })
  .passthrough();

/** 주식잔고조회_실현손익 (`POST /krstock/inquiry/v1/realizedPnl`) 응답. */
export const krStockInquiryRealizedPnlResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 종합 정보 */
    Output_0: krStockInquiryRealizedPnlAccountOutputSchema.nullish(),
    /** 종목별 실현손익 상세 목록 */
    Output_1: z.array(krStockInquiryRealizedPnlOutputSchema).nullish(),
  })
  .passthrough();

/** 투자계좌자산현황조회 계좌 종합 정보 (Output_0). */
export const krStockInquiryAssetStatusAccountOutputSchema = z
  .object({
    /** 고객성명 */
    cus_fnm: z.string().nullish(),
    /** 실명확인번호 */
    rnm_cfm_no: z.string().nullish(),
    /** 약정유형코드명 */
    ctc_tp_cd_nm: z.string().nullish(),
    /** 계좌관리팀점코드 */
    act_amn_tab_cd: z.string().nullish(),
    /** 계좌상품대분류코드 */
    act_pdt_llf_cd: z.string().nullish(),
    /** 관리사원성명 */
    amn_emp_fnm: z.string().nullish(),
    /** 예수금 — 예수금 */
    dca: num.nullish(),
    /** 익일예수금 — D+1 예수금 */
    nxt_dd_dca: num.nullish(),
    /** 익익일예수금 — D+2 예수금 */
    nxt2_dd_dca: num.nullish(),
    /** 원화환산외화예수금 */
    krw_tsl_fc_dca: num.nullish(),
    /** 원화환산외화담보금액 */
    krw_tsl_fc_mgg_amt: num.nullish(),
    /** 원화환산외화주문가능금액 */
    krw_tsl_fc_orr_pbl_amt: num.nullish(),
    /** 출금가능금액 */
    drn_pbl_amt: num.nullish(),
    /** 융자금액 */
    fnn_amt: num.nullish(),
    /** 담보비율 */
    mgg_rt: num.nullish(),
    /** 주식주문가능금액 */
    stk_orr_pbl_amt: num.nullish(),
    /** 총자산금액 */
    tot_aet_amt: num.nullish(),
    /** 순자산금액 */
    nas_amt: num.nullish(),
    /** 총매수금액 */
    tot_byn_amt: num.nullish(),
    /** 총평가금액 */
    tot_eal_amt: num.nullish(),
    /** 총평가손익금액 */
    tot_eal_pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 미수금 */
    rba: num.nullish(),
    /** 이자미납부금액 */
    int_ny_pmt_amt: num.nullish(),
    /** 기타대여금 */
    ect_lga: num.nullish(),
    /** 대출금액 */
    lon_amt: num.nullish(),
    /** 대용금액 */
    sba_amt: num.nullish(),
    /** 금융상품주문가능금액 */
    fnc_pdt_orr_pbl_amt: num.nullish(),
    /** 미상환금액 */
    ny_rdp_amt: num.nullish(),
    /** 신용상품유형명 */
    cfd_pdt_tp_nm: z.string().nullish(),
    /** 계좌활동유형코드명 */
    act_atv_tp_cd_nm: z.string().nullish(),
    /** 대주금액 */
    slo_amt: num.nullish(),
    /** 현금증거금 */
    csh_wtm: num.nullish(),
    /** 펀드매도결제예정금액 */
    fnd_sll_stl_xpn_amt: num.nullish(),
    /** 청약예수금 */
    sbi_dca: num.nullish(),
    /** IMA증거금 */
    ima_wtm: num.nullish(),
  })
  .passthrough();

/** 투자계좌자산현황조회 보유 종목별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryAssetStatusOutputSchema = z
  .object({
    /** 종목중분류명 */
    iem_mlf_nm: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 잔고유형구분코드명 */
    bnc_tp_dit_cd_nm: z.string().nullish(),
    /** 통합잔고수량 */
    itg_bnc_qty: num.nullish(),
    /** 매입가격 */
    phs_pr: num.nullish(),
    /** 현재가격 */
    now_pr: num.nullish(),
    /** 매수금액 */
    byn_amt: num.nullish(),
    /** 평가금액 */
    eal_amt: num.nullish(),
    /** 평가손익금액 */
    eal_pls_amt: num.nullish(),
    /** 매도손익금액 */
    sll_pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 이자율 */
    int_rt: num.nullish(),
    /** 매수일자 */
    byn_dt: z.string().nullish(),
    /** 만기일자 */
    xrn_dt: z.string().nullish(),
    /** 대출만기일자 */
    lon_xrn_dt: z.string().nullish(),
    /** 종합과세구분코드 */
    syn_ttn_dit_cd: z.string().nullish(),
    /** 종합과세구분코드명 */
    syn_ttn_dit_cd_nm: z.string().nullish(),
    /** CRM자산분류코드 */
    crm_aet_cfc_cd: z.string().nullish(),
    /** 종목중분류코드 */
    iem_mlf_cd: z.string().nullish(),
    /** 매수청구수량 */
    byn_cim_qty: num.nullish(),
    /** 실물수량 */
    rth_qty: num.nullish(),
    /** 약정이자율 */
    ctc_int_rt: num.nullish(),
    /** 대출잔고금액 */
    lon_bnc_amt: num.nullish(),
    /** 통화코드 */
    cur_cd: z.string().nullish(),
    /** 외화증권거래국가코드 */
    fc_sec_trd_nat_cd: z.string().nullish(),
    /** 국가코드명 */
    nat_cd_nm: z.string().nullish(),
    /** 통합잔고유형코드 */
    itg_bnc_tp_cd: z.string().nullish(),
    /** 티커종목코드 */
    tck_iem_cd: z.string().nullish(),
  })
  .passthrough();

/** 투자계좌자산현황조회 (`POST /krstock/inquiry/v1/assetStatus`) 응답. */
export const krStockInquiryAssetStatusResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 종합 정보 */
    Output_0: krStockInquiryAssetStatusAccountOutputSchema.nullish(),
    /** 보유 종목별 상세 목록 */
    Output_1: z.array(krStockInquiryAssetStatusOutputSchema).nullish(),
  })
  .passthrough();

/** 실현손익일별합산조회 계좌 종합 정보 (Output_0). */
export const krStockInquiryDailyPnlAccountOutputSchema = z
  .object({
    /** 계좌성명 */
    act_fnm: z.string().nullish(),
    /** 매수대금합계1 */
    byn_cst_sum: z.union([z.string(), num]).nullish(),
    /** 매도대금합계1 */
    sll_cst_sum: z.union([z.string(), num]).nullish(),
    /** 손익금액합계 */
    pls_amt_sum: num.nullish(),
    /** 누적제비용 */
    acl_sdr_xps: num.nullish(),
  })
  .passthrough();

/** 실현손익일별합산조회 일별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryDailyPnlOutputSchema = z
  .object({
    /** 매매일자 */
    sby_dt: z.string().nullish(),
    /** 매수수량 */
    byn_qty: num.nullish(),
    /** 매수금액 */
    byn_amt: num.nullish(),
    /** 매수수수료 */
    byn_fee: num.nullish(),
    /** 매수금액합계 */
    byn_amt_sum: num.nullish(),
    /** 매도수량 */
    sll_qty: num.nullish(),
    /** 매도금액 */
    sll_amt: num.nullish(),
    /** 매도세금합계 */
    sll_tax_sum: num.nullish(),
    /** 매도금액합계 */
    sll_amt_sum: num.nullish(),
    /** 손익금액 */
    pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 종목중분류코드 — 01001.주식 01002.DR 01003.투자회사 01004.신주인수권증권 01005.상장REITS 01006.신주인수권증서 01007.ETF 01008.상장수익증권 */
    iem_mlf_cd: z.string().nullish(),
  })
  .passthrough();

/** 실현손익일별합산조회 (`POST /krstock/inquiry/v1/dailyPnl`) 응답. */
export const krStockInquiryDailyPnlResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 종합 정보 */
    Output_0: krStockInquiryDailyPnlAccountOutputSchema.nullish(),
    /** 일별 실현손익 상세 목록 */
    Output_1: z.array(krStockInquiryDailyPnlOutputSchema).nullish(),
  })
  .passthrough();

/** 종목별실현손익현황조회 계좌 합계 정보 (Output_0). */
export const krStockInquiryTradingPnlAccountOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 매수수량 */
    byn_qty: num.nullish(),
    /** 매수단가 */
    byn_uit_pr: num.nullish(),
    /** 매수수수료 */
    byn_fee: num.nullish(),
    /** 매수건수 */
    byn_cnt: num.nullish(),
    /** 매수금액 */
    byn_amt: num.nullish(),
    /** 매도수량 */
    sll_qty: num.nullish(),
    /** 매도단가 */
    sll_uit_pr: num.nullish(),
    /** 매도세금합계 */
    sll_tax_sum: num.nullish(),
    /** 매도건수 */
    sll_cnt: num.nullish(),
    /** 매도금액 */
    sll_amt: num.nullish(),
    /** 매도장부금액 */
    sll_abk_amt: num.nullish(),
    /** 손익금액 */
    pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 수수료합계 */
    fee_sum: z.union([z.string(), num]).nullish(),
    /** 세금합계 */
    tax_sum: z.union([z.string(), num]).nullish(),
  })
  .passthrough();

/** 종목별실현손익현황조회 종목별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryTradingPnlOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 매수수량 */
    byn_qty: num.nullish(),
    /** 매수단가 */
    byn_uit_pr: num.nullish(),
    /** 매수수수료 */
    byn_fee: num.nullish(),
    /** 매수건수 */
    byn_cnt: num.nullish(),
    /** 매수금액 */
    byn_amt: num.nullish(),
    /** 매도수량 */
    sll_qty: num.nullish(),
    /** 매도단가 */
    sll_uit_pr: num.nullish(),
    /** 매도세금합계 */
    sll_tax_sum: num.nullish(),
    /** 매도건수 */
    sll_cnt: num.nullish(),
    /** 매도금액 */
    sll_amt: num.nullish(),
    /** 매도장부금액 */
    sll_abk_amt: num.nullish(),
    /** 손익금액 */
    pls_amt: num.nullish(),
    /** 수익율 */
    pft_rt: num.nullish(),
    /** 수수료합계 */
    fee_sum: z.union([z.string(), num]).nullish(),
    /** 세금합계 */
    tax_sum: z.union([z.string(), num]).nullish(),
    /** 종목중분류코드 — 01001.주식 01002.DR 01003.투자회사 01004.신주인수권증권 01005.상장REITS 01006.신주인수권증서 01007.ETF 01008.상장수익증권 */
    iem_mlf_cd: z.string().nullish(),
  })
  .passthrough();

/** 종목별실현손익현황조회 (`POST /krstock/inquiry/v1/tradingPnl`) 응답. */
export const krStockInquiryTradingPnlResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 합계 정보 */
    Output_0: krStockInquiryTradingPnlAccountOutputSchema.nullish(),
    /** 종목별 실현손익 상세 목록 */
    Output_1: z.array(krStockInquiryTradingPnlOutputSchema).nullish(),
  })
  .passthrough();

/** 주식통합증거금 현황 계좌 한도 정보 (Output_0). */
export const krStockInquiryIntegratedMarginAccountOutputSchema = z
  .object({
    /** 외화주문가능금액3 — 주문가능금액 */
    fc_orr_pbl_amt3: num.nullish(),
    /** 교차매매결제금액 — 결제금(원) */
    cro_sby_stl_amt: num.nullish(),
    /** 교차매매계좌여부 — 약정여부 */
    cro_sby_act_yn: z.string().nullish(),
    /** 한도금액 — 한도금액(원) */
    lmt_amt: num.nullish(),
    /** 한도사용금액 — 한도사용금액(원) */
    lmt_use_amt: num.nullish(),
    /** 잔여한도금액 — 한도잔여금액(원) */
    rmn_lmt_amt: num.nullish(),
  })
  .passthrough();

/** 주식통합증거금 현황 통화별 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryIntegratedMarginOutputSchema = z
  .object({
    /** 통화코드 */
    cur_cd: z.string().nullish(),
    /** 외화예수금 */
    fc_dca: num.nullish(),
    /** 외화담보금액 */
    fc_mgg_amt: num.nullish(),
    /** 해외거래세 */
    ose_trd_tax: num.nullish(),
    /** 외화자동재매매대상금액 — 매도금액 */
    fc_ato_re_sby_obj_amt: num.nullish(),
    /** 외화주문가능금액 — 자국통화 주문가능금액 */
    fc_orr_pbl_amt: num.nullish(),
    /** 적용환율 */
    aly_xcg_rt: num.nullish(),
    /** 주문가능금액현금 */
    orr_pbl_amt_csh: num.nullish(),
    /** 전환비율 — 통합증거금 통화간 전환비율 */
    cnv_rt: num.nullish(),
    /** 원화환산교차가능금액 — 타국통화 통합증거금 가능금액(원) */
    krw_tsl_cro_pbl_amt: num.nullish(),
    /** 거래통화교차가능금액 — 타국통화 주문가능금액 */
    trd_cur_cro_pbl_amt: num.nullish(),
    /** 외화주문가능금액1 — 주문가능금액 */
    fc_orr_pbl_amt1: num.nullish(),
    /** 외화주문가능금액2 — 가능금액 */
    fc_orr_pbl_amt2: num.nullish(),
    /** 거래통화교차사용금액 — 사용금액 */
    trd_cur_cro_use_amt: num.nullish(),
  })
  .passthrough();

/** 주식통합증거금 현황 (`POST /krstock/inquiry/v1/integratedMargin`) 응답. */
export const krStockInquiryIntegratedMarginResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 계좌 한도 정보 */
    Output_0: krStockInquiryIntegratedMarginAccountOutputSchema.nullish(),
    /** 통화별 상세 목록 */
    Output_1: z.array(krStockInquiryIntegratedMarginOutputSchema).nullish(),
  })
  .passthrough();

/** 기간별계좌권리현황조회보유 조회 조건 정보 (Output_0). */
export const krStockInquiryRightsHeldHeaderOutputSchema = z
  .object({
    /** 시작일자 — YYYYMMDD */
    sta_dt: z.string().nullish(),
  })
  .passthrough();

/** 기간별계좌권리현황조회보유 보유 권리 상세 (Output_1 배열의 각 항목). */
export const krStockInquiryRightsHeldOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 기준일자 — YYYYMMDD */
    bse_dt: z.string().nullish(),
    /** 권리유형코드 — _.해당사항없음 01.배당 02.유상 03.무상 04.매수청구 05.신주인수권증서 06.뮤추얼 07.ETF분배금 08.선박펀드 09.투융자펀드 10.해외자원개발펀드 11.Ritz(부동산신탁) 12.ELS상환 13.DLS상환 14.ELW만기결제 15.기타청산 16.전환/상환 17.ETN분배금 21.흡수합병 22.회사분할 23.주식교환 24.자본감소 25.액면분할 26.액면병합 27.종목변경 등 (전체 코드 목록은 스펙 참고, 문자·숫자 혼용 코드 다수) */
    rit_tp_cd: z.string().nullish(),
    /** 보유수량 */
    hld_qty: num.nullish(),
    /** 배정기준가격 */
    aloc_bse_pr: num.nullish(),
    /** 신청금액 */
    req_amt: num.nullish(),
    /** 배정금액지급일자 — YYYYMMDD */
    aloc_amt_pym_dt: z.string().nullish(),
    /** 상장일자 — YYYYMMDD */
    ltg_dt: z.string().nullish(),
    /** 신청여부 */
    req_yn: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 대여차입구분코드 — 01.차입 02.대여(주식) 03.대여풀 04.대여(채권) 05.대여(해외주식) 06.대여(해외채권) */
    ldg_brw_dit_cd: z.string().nullish(),
    /** 유통구분코드 — 01.일반 02.유통금융 03.유통대주 */
    cln_dit_cd: z.string().nullish(),
    /** 배정수량 */
    aloc_qty: num.nullish(),
    /** 신청종료일자 — YYYYMMDD */
    req_end_dt: z.string().nullish(),
    /** 신청수량 */
    req_qty: num.nullish(),
    /** 권리배정금액 */
    rit_aloc_amt: num.nullish(),
    /** 상장종목코드 */
    ltg_iem_cd: z.string().nullish(),
    /** 처리여부 */
    pcs_yn: z.string().nullish(),
    /** 고배당여부 */
    hdd_yn: z.string().nullish(),
    /** 예약시작일자 — YYYYMMDD */
    bkg_sta_dt: z.string().nullish(),
    /** 예약종료일자 — YYYYMMDD */
    bkg_end_dt: z.string().nullish(),
    /** 반대의사접수종료일자 — YYYYMMDD */
    rrs_itn_rtn_end_dt: z.string().nullish(),
    /** 매수청구접수종료일자 — YYYYMMDD */
    byn_cim_rtn_end_dt: z.string().nullish(),
  })
  .passthrough();

/** 기간별계좌권리현황조회보유 (`POST /krstock/inquiry/v1/rightsHeld`) 응답. */
export const krStockInquiryRightsHeldResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 조회 조건 정보 */
    Output_0: krStockInquiryRightsHeldHeaderOutputSchema.nullish(),
    /** 보유 권리 상세 목록 */
    Output_1: z.array(krStockInquiryRightsHeldOutputSchema).nullish(),
  })
  .passthrough();

/** 기간별계좌권리현황조회예정 예정 권리 상세 (Output_0 배열의 각 항목). */
export const krStockInquiryRightsScheduledOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 권리유형코드 — _.전체 01.배당 02.유상 03.무상 04.매수청구 05.신주인수권증서 06.뮤추얼 07.ETF분배금 08.선박펀드 09.투융자펀드 10.해외자원개발펀드 11.Ritz(부동산신탁) 12.ELS상환 13.DLS상환 14.ELW만기결제 15.기타청산 16.전환/상환 17.ETN분배금 21.흡수합병 22.회사분할 등 (전체 코드 목록은 스펙 참고, 문자·숫자 혼용 코드 다수) */
    rit_tp_cd: z.string().nullish(),
    /** 권리유형명 */
    rit_tp_nm: z.string().nullish(),
    /** 배정수량 */
    aloc_qty: num.nullish(),
    /** 배정비율 */
    aloc_rt: num.nullish(),
    /** 권리락일자 */
    xgt_dt: z.string().nullish(),
    /** 기준일자 */
    bse_dt: z.string().nullish(),
    /** 권리행사종료일자 */
    rit_erc_end_dt: z.string().nullish(),
    /** 상장일자 */
    ltg_dt: z.string().nullish(),
    /** 권리행사가격 */
    rit_erc_pr: num.nullish(),
  })
  .passthrough();

/** 기간별계좌권리현황조회예정 (`POST /krstock/inquiry/v1/rightsScheduled`) 응답. */
export const krStockInquiryRightsScheduledResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 예정 권리 상세 목록 */
    Output_0: z.array(krStockInquiryRightsScheduledOutputSchema).nullish(),
  })
  .passthrough();

/** 주식예약주문조회 (`POST /krstock/inquiry/v1/reservedInquiry`) 응답. */
export const krStockInquiryReservedInquiryResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 팀점 정보 */
    Output_0: krStockInquiryReservedInquiryHeaderOutputSchema.nullish(),
    /** 예약주문 내역 목록 */
    Output_1: z.array(krStockInquiryReservedInquiryOutputSchema).nullish(),
  })
  .passthrough();

// ── Response Types ──

export type KrStockInquiryBalanceResponse = CamelizeKeys<z.infer<typeof krStockInquiryBalanceResponseSchema>>;
export type KrStockInquiryDailyOrderExecutionResponse = CamelizeKeys<
  z.infer<typeof krStockInquiryDailyOrderExecutionResponseSchema>
>;
export type KrStockInquiryBuyableQuantityResponse = CamelizeKeys<
  z.infer<typeof krStockInquiryBuyableQuantityResponseSchema>
>;
export type KrStockInquirySellableQuantityResponse = CamelizeKeys<
  z.infer<typeof krStockInquirySellableQuantityResponseSchema>
>;
export type KrStockInquiryRealizedPnlResponse = CamelizeKeys<z.infer<typeof krStockInquiryRealizedPnlResponseSchema>>;
export type KrStockInquiryAssetStatusResponse = CamelizeKeys<z.infer<typeof krStockInquiryAssetStatusResponseSchema>>;
export type KrStockInquiryDailyPnlResponse = CamelizeKeys<z.infer<typeof krStockInquiryDailyPnlResponseSchema>>;
export type KrStockInquiryTradingPnlResponse = CamelizeKeys<z.infer<typeof krStockInquiryTradingPnlResponseSchema>>;
export type KrStockInquiryIntegratedMarginResponse = CamelizeKeys<
  z.infer<typeof krStockInquiryIntegratedMarginResponseSchema>
>;
export type KrStockInquiryRightsHeldResponse = CamelizeKeys<z.infer<typeof krStockInquiryRightsHeldResponseSchema>>;
export type KrStockInquiryRightsScheduledResponse = CamelizeKeys<
  z.infer<typeof krStockInquiryRightsScheduledResponseSchema>
>;
export type KrStockInquiryReservedInquiryResponse = CamelizeKeys<
  z.infer<typeof krStockInquiryReservedInquiryResponseSchema>
>;

// ── Response Map ──

export interface KrstockInquiryResponseMap {
  balance: KrStockInquiryBalanceResponse;
  dailyOrderExecution: KrStockInquiryDailyOrderExecutionResponse;
  buyableQuantity: KrStockInquiryBuyableQuantityResponse;
  sellableQuantity: KrStockInquirySellableQuantityResponse;
  reservedInquiry: KrStockInquiryReservedInquiryResponse;
  realizedPnl: KrStockInquiryRealizedPnlResponse;
  assetStatus: KrStockInquiryAssetStatusResponse;
  dailyPnl: KrStockInquiryDailyPnlResponse;
  tradingPnl: KrStockInquiryTradingPnlResponse;
  integratedMargin: KrStockInquiryIntegratedMarginResponse;
  rightsHeld: KrStockInquiryRightsHeldResponse;
  rightsScheduled: KrStockInquiryRightsScheduledResponse;
}
