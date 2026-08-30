import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

/**
 * NH PLUG 해외주식(조회) 응답 스키마.
 *
 * 와이어 포맷은 snake_case 이며 (`Output_0`, `Output_1` … 블록 이름도 원문 그대로),
 * 공개 API 는 `camelizeKeys` 로 자동 camelCase 변환한다 — 스키마는 와이어를 그대로 기술한다.
 * 모든 블록·필드는 데이터가 있을 때만 내려오므로 전부 optional/nullable 이고,
 * 스펙에 없는 실서버 필드가 살아남도록 모든 객체에 `.passthrough()` 를 건다.
 */

/** 스펙상 문자열 필드. 실서버가 숫자로 내려주는 경우가 있어 문자열로 강제 변환한다. */
const str = () => z.coerce.string().nullish();

/**
 * 스펙상 숫자(`int`/`float`) 필드.
 *
 * 실서버는 숫자를 문자열로, 값 없는 숫자를 빈 문자열(`""`)로 내려주는 사례가 있어
 * (파이썬 `_overseas_stock_quote_types` 의 `_empty_str_to_none` 참고)
 * 빈 문자열은 null 로 접고 나머지는 숫자로 강제 변환한다.
 */
const num = () => z.preprocess((value) => (value === '' ? null : value), z.coerce.number().nullish()).nullish();

/** 스펙상 `message` 봉투. 실서버는 null 을 내려주고 `rsp_cd`/`rsp_msg` 를 대신 쓴다. */
const messageSchema = z
  .object({
    msg_code: str(),
    usr_msg: str(),
    msg_lv_code: str(),
    dvlp_msg_yn: str(),
  })
  .passthrough();

const envelope = {
  /** 응답코드 (00000·XA102: 성공) */
  rsp_cd: str(),
  /** 응답메시지 */
  rsp_msg: str(),
  /** 스펙상 메시지 봉투 (실서버는 null) */
  message: messageSchema.nullish(),
};

// ── 해외주식 매수가능금액·수량 조회 결과 (`Output_0`). ──

export const overseasStockInquiryBuyableAmountOutputSchema = z
  .object({
    fc_dca: num(), // 외화예수금
    mgg_fc_amt: num(), // 담보외화금액
    csh_wtm: num(), // 현금증거금
    re_use_obj_amt: num(), // 재사용대상금액
    re_use_rtr_use_amt: num(), // 재사용환원사용금액
    ect_use_amt: num(), // 기타사용금액
    orr_pbl_amt: num(), // 주문가능금액
    wtm_cur_cd: str(), // 증거금통화코드
    hld_qty: num(), // 보유수량
    orr_pbl_qty: num(), // 주문가능수량
    sll_pbl_qty: num(), // 매도가능수량
    sll_pbl_qty1: num(), // 매도가능수량1
    byn_cns_qty: num(), // 매수체결수량
    sll_cns_qty: num(), // 매도체결수량
    sll_orr_qty: num(), // 매도주문수량
    dps_rsc_qty: num(), // 처분제한수량
    byn_pbl_qty: num(), // 매수가능수량
    max_pbl_amt: num(), // 최대가능금액
    max_pbl_qty: num(), // 최대가능수량
    csh_wtm_rt: num(), // 현금증거금율
  })
  .passthrough();

/**
 * 해외주식 매수가능금액·수량 조회 (`POST /gbstock/inquiry/v1/buyableAmount`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockInquiryBuyableAmountResponseSchema = z
  .object({
    ...envelope,
    /** 매수가능금액·수량 조회 결과 */
    Output_0: overseasStockInquiryBuyableAmountOutputSchema.nullish(),
  })
  .passthrough();

// ── 해외주식 주문체결내역 조회 결과 항목 (`Output_0` 배열 원소). ──

export const overseasStockInquiryUnexecutedOutputSchema = z
  .object({
    rgs_tm: str(), // 등록시각
    oss_orr_knd_cd: str(), // 해외증권주문종류코드
    orr_knd_nm: str(), // 주문종류명
    orr_no: num(), // 주문번호
    org_orr_no: num(), // 원주문번호
    oss_sby_dit_cd: str(), // 해외증권매매구분코드
    sby_dit_nm: str(), // 매매구분명
    fc_sec_trd_nat_cd: str(), // 외화증권거래국가코드
    mkt_dit_cd_nm: str(), // 시장구분코드명
    iem_cd: str(), // 종목코드
    iem_nm: str(), // 종목명
    orr_qty: num(), // 주문수량
    fc_orr_uit_pr: num(), // 외화주문단가
    cns_qty: num(), // 체결수량
    cns_pr: num(), // 체결가격
    ny_cns_orr_qty: num(), // 미체결주문수량
    cor_can_dit_cd: str(), // 정정취소구분코드
    cor_can_dit_nm: str(), // 정정취소구분명
    cor_qty: num(), // 정정수량
    can_qty: num(), // 취소수량
    oss_ato_orr_sts_cd: str(), // 해외증권자동주문상태코드
    orr_sts_nm: str(), // 주문상태명
    oms_cus_orr_no: str(), // OMS고객주문번호
    rjt_rsn_cts: str(), // 거부사유내용
    ivs_nat_krx_dit_cd: str(), // 투자국가거래소구분코드
    fix_sgy_tgt_sgy_nm: str(), // FIX전략타겟전략명
    fix_orr_pcs_mtd_cd: str(), // FIX주문처리방법코드
    orr_pcs_mtd_cd_nm: str(), // 주문처리방법코드명
    rut_orr_krx_cd: str(), // 로이터주문거래소코드
    hts_usr_id: str(), // HTS사용자ID
    usr_ip_adr: str(), // 사용자IP주소
    cuc_mdi_cd: str(), // 통신매체코드
    cuc_mdi_cd_nm: str(), // 통신매체코드명
    ahi_nmn_pr_tp_cd: str(), // 현물호가유형코드
    ahi_nmn_pr_tp_cd_nm: str(), // 현물호가유형코드명
    fc_stop_orr_bse_pr: num(), // 외화STOP주문기준가격
    orr_pdt_dit_cd: str(), // 주문상품구분코드
    orr_dt: str(), // 주문일자
    csh_wtm_rt: num(), // 현금증거금율
    cfd_lon_cd: str(), // 신용대출코드
    cfd_lon_cd_nm: str(), // 신용대출코드명
    lon_dt: str(), // 대출일자
  })
  .passthrough();

/**
 * 해외주식 주문체결내역 조회 (`POST /gbstock/inquiry/v1/unexecuted`) 응답.
 *
 * 응답 블록: `Output_0`: 배열
 */
export const overseasStockInquiryUnexecutedResponseSchema = z
  .object({
    ...envelope,
    /** 주문체결내역 조회 결과 */
    Output_0: z.array(overseasStockInquiryUnexecutedOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 잔고조회 결과 (`Output_0`). ──

export const overseasStockInquiryBalanceAccountOutputSchema = z
  .object({
    abk_amt: num(), // 장부금액
    eal_amt_sum: num(), // 평가금액합계
    eal_pls_sum_amt: num(), // 평가손익합계금액
    krw_pft_rt: num(), // 원화수익율
    krw_dca: num(), // 원화예수금
    krw_ny_stl_xcl_amt: num(), // 원화미결제정산금액
    tot_aet_amt: num(), // 총자산금액
    fc_abk_amt: num(), // 외화장부금액
    fc_eal_amt: num(), // 외화평가금액
    fc_eal_pls_amt: num(), // 외화평가손익금액
    pft_rt: num(), // 수익율
    fc_dca: num(), // 외화예수금
    fc_ny_stl_xcl_amt: num(), // 외화미결제정산금액
    fc_aet_amt: num(), // 외화자산금액
    ptps_ttn_amt: num(), // PTP과세금액
    ptps_ttn_amt1: num(), // PTP과세금액1
  })
  .passthrough();

// ── 해외주식 잔고조회 결과 항목 (`Output_1` 배열 원소). ──

export const overseasStockInquiryBalanceHoldingOutputSchema = z
  .object({
    fc_sec_trd_nat_cd: str(), // 외화증권거래국가코드
    fc_sec_trd_nat_nm: str(), // 외화증권거래국가명
    iem_cd: str(), // 종목코드
    oss_iem_eng_nm: str(), // 해외증권종목영문명
    iem_nm: str(), // 외화증권한글명
    cns_bse_bnc_qty: num(), // 체결기준잔고수량
    sll_cns_qty: num(), // 매도체결수량
    byn_cns_qty: num(), // 매수체결수량
    sll_pbl_qty1: num(), // 매도가능수량1
    fc_abk_amt: num(), // 외화장부금액
    krw_abk_amt1: num(), // 원화장부금액1
    fc_phs_uit_pr: num(), // 외화매입단가
    phs_uit_pr: num(), // 매입단가
    fc_sec_end_pr: num(), // 외화증권종가
    end_pr: num(), // 종가
    fc_eal_amt: num(), // 외화평가금액
    krw_eal_amt: num(), // 원화평가금액
    fc_eal_pls_amt: num(), // 외화평가손익금액
    krw_eal_pls_amt: num(), // 원화평가손익금액
    eal_pft_rt: num(), // 평가수익율
    eal_pft_rt1: num(), // 평가수익율1
    cur_cd: str(), // 통화코드
    phs_xcg_rt: num(), // 매입환율
    tdt_sby_bse_xcg_rt: num(), // 당일매매기준환율
    fc_mkt_dit_cd: str(), // 외화시장구분코드
    fc_sll_pls_amt: num(), // 외화매도손익금액
    krw_sll_pls_amt: num(), // 원화매도손익금액
    fc_sll_pft_rt: num(), // 외화매도수익율
    krw_sll_pft_rt: num(), // 원화매도수익율
    fc_cns_bse_phs_xps: num(), // 외화체결기준매입비
    krw_cns_bse_phs_xps: num(), // 원화체결기준매입비
    fc_avg_phs_pr: num(), // 외화평균매입가격
    krw_avg_phs_pr: num(), // 원화평균매입가격
    fc_fee: num(), // 외화수수료
    krw_fee: num(), // 원화수수료
    fc_tax_amt: num(), // 외화세금금액
    krw_tax_amt: num(), // 원화세금금액
    fc_pls_qtr_phs_pr: num(), // 외화손익분기매입가격
    krw_pls_qtr_phs_pr: num(), // 원화손익분기매입가격
    sby_fee_rt: num(), // 매매수수료율
    fc_stk_lws_sby_fee: num(), // 외화주식최저매매수수료
    cfd_lon_cd_nm: str(), // 신용대출코드명
    lon_dt: str(), // 대출일자
    xrn_dt: str(), // 만기일자
  })
  .passthrough();

/**
 * 해외주식 잔고조회 (`POST /gbstock/inquiry/v1/balance`) 응답.
 *
 * 응답 블록: `Output_0`: 객체, `Output_1`: 배열
 */
export const overseasStockInquiryBalanceResponseSchema = z
  .object({
    ...envelope,
    /** 잔고 요약 조회 결과 */
    Output_0: overseasStockInquiryBalanceAccountOutputSchema.nullish(),
    /** 잔고 종목별 조회 결과 */
    Output_1: z.array(overseasStockInquiryBalanceHoldingOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 예약주문조회 결과 항목 (`Output_0` 배열 원소). ──

export const overseasStockInquiryReservedInquiryOutputSchema = z
  .object({
    fc_mkt_dit_cd: str(), // 외화시장구분코드 / 200.미국 070.일본 120.홍콩 160.상해 170.심천
    bkg_orr_dt: str(), // 예약주문일자 / YYYYMMDD
    act_no: str(), // 계좌번호
    cus_fnm: str(), // 고객성명
    iem_cd: str(), // 티커종목코드
    iem_nm: str(), // 종목명
    cur_cd: str(), // 통화코드 / KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY
    sby_dit_cd: str(), // 매매구분코드 / 1.매도 2.매수
    sby_dit_nm: str(), // 매매구분명
    orr_qty: num(), // 주문수량
    orr_pr: num(), // 주문가격
    cns_qty: num(), // 체결수량
    cns_pr: num(), // 체결가격
    bkg_orr_can_yn: str(), // 예약주문취소여부
    orr_can_dit_nm: str(), // 주문취소구분명
    bkg_orr_rtn_dt: str(), // 예약주문접수일자 / YYYYMMDD
    bkg_orr_rtn_tm: str(), // 예약주문접수시각
    rgs_tab_cd: str(), // 등록팀점코드
    rgs_emp_no: str(), // 등록사원번호
    rgs_emp_fnm: str(), // 등록사원성명
    cct_dt: str(), // 해지일자 / YYYYMMDD
    cct_tm: str(), // 해지시각
    cct_emp_no: str(), // 해지사원번호
    cct_emp_fnm: str(), // 해지사원성명
    bkg_rtn_orr_no: num(), // 예약접수주문번호
    orr_sno: num(), // 주문일련번호
    ost_orr_mdi: str(), // 주문매체
    orr_cpl_yn: str(), // 주문완료여부
    ost_pcs_cd: str(), // 처리코드
    pcs_msg_cts: str(), // 처리메시지내용
    aca_tel_no: str(), // 연락처전화번호
    ahi_nmn_pr_tp_cd: str(), // 현물호가유형코드
    ahi_nmn_pr_tp_cd_nm: str(), // 현물호가유형코드명
    oss_orr_knd_cd_nm: str(), // 해외증권주문종류코드명
    ivs_sgy_cd_nm: str(), // 투자전략코드명
    fc_csh_wtm: num(), // 외화현금증거금
    fc_csh_wtm_fee: num(), // 외화현금증거금수수료
    fc_csh_wtm_tax_amt: num(), // 외화현금증거금세금금액
    fc_csh_wtm_trd_tax: num(), // 외화현금증거금거래세
    fc_mkt_dit_cd_nm: str(), // 외화시장구분코드명
    bkg_orr_tp_cd: str(), // 예약주문유형코드 / 1. 일반예약주문 / 2. 잔량기준기간예약주문 / 3. 수량기준기간예약주문 / 4. 증거금징수 예약
    bkg_orr_tp_cd_nm: str(), // 예약주문유형코드명
    orr_enf_sta_dt: str(), // 주문집행시작일자 / YYYYMMDD
    orr_enf_end_dt: str(), // 주문집행종료일자 / YYYYMMDD
    acl_cns_qty: num(), // 누적체결수량
    lst_orr_enf_dt: str(), // 최종주문집행일자 / YYYYMMDD
    rmn_qty: num(), // 잔여수량
    wtm_cur_knd_cd: str(), // 증거금통화종류코드 / 1.거래국가통화 2.원화 3.기타통화
    cd_nm: str(), // 코드명
    fc_stop_orr_bse_pr: num(), // 외화STOP주문기준가격
    orr_pdt_dit_cd: str(), // 주문상품구분코드
    cfd_lon_cd: str(), // 신용대출코드
    cfd_lon_cd_nm: str(), // 신용대출코드명
    lon_dt: str(), // 대출일자 / YYYYMMDD
  })
  .passthrough();

/**
 * 해외주식 예약주문조회 (`POST /gbstock/inquiry/v1/reservedInquiry`) 응답.
 *
 * 응답 블록: `Output_0`: 배열
 */
export const overseasStockInquiryReservedInquiryResponseSchema = z
  .object({
    ...envelope,
    /** 예약주문내역 조회 결과 */
    Output_0: z.array(overseasStockInquiryReservedInquiryOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 일별거래내역 조회 결과 항목 (`Output_0` 배열 원소). ──

export const overseasStockInquiryDailyTransactionOutputSchema = z
  .object({
    trd_dt: str(), // 거래일자
    trd_sno: num(), // 거래일련번호
    act_trd_tp_nm: str(), // 계좌거래유형명
    sps_cd_nm: str(), // 적요코드명
    iem_krl_nm: str(), // 종목한글명
    iem_cd: str(), // 종목코드
    trd_qty: num(), // 거래수량
    trd_uit_pr: num(), // 거래단가
    cur_cd_nm: str(), // 통화코드명
    aly_xcg_rt: num(), // 적용환율
    trd_bf_bnc_qty: num(), // 거래전잔고수량
    trd_af_bnc_qty: num(), // 거래후잔고수량
    fc_trd_amt: num(), // 외화거래금액
    krw_trd_amt: num(), // 원화거래금액
    trd_af_fc_dca: num(), // 거래후외화예수금
    trd_af_dca: num(), // 거래후예수금
    trd_af_fc_mgg_amt: num(), // 거래후외화담보금액
    trd_af_krw_mgg_amt: num(), // 거래후원화담보금액
    abd_sdr_xps_fc_amt: num(), // 국외제비용외화금액
    tsl_mgg_amt: num(), // 환산담보금액
    ose_fee: num(), // 해외수수료
    dmt_fee: num(), // 국내수수료
    icm_tax: num(), // 소득세
    rsd_tax: num(), // 주민세
    rgs_cuc_mdi_cd_nm: str(), // 등록통신매체코드명
    rgs_tm: str(), // 등록시각
    rgs_tab_cd: str(), // 등록팀점코드
    rgs_emp_no: str(), // 등록사원번호
    oss_iem_cd: str(), // 해외증권종목코드
    oss_iem_nm: str(), // 해외증권종목명
    trd_bf_fc_dca: num(), // 거래전외화예수금
    trd_bf_dca: num(), // 거래전예수금
    oss_stm_tax: num(), // 해외증권인지세
    fc_tsl_txa: num(), // 외화환산세액
    fc_amt: num(), // 외화금액
    krw_amt: num(), // 원화금액
    fc_tax_sum: num(), // 외화세금합계
    tax_sum: num(), // 세금합계
    fc_icm_tax: num(), // 외화소득세
    fc_rsd_tax: num(), // 외화주민세
    fc_sas_amt: num(), // 외화과세표준금액
    krw_sas_amt: num(), // 원화과세표준금액
    tsl_cmu_txa: num(), // 환산산출세액
    fc_trd_dit_cd: str(), // 외화거래구분코드
    ral_trd_dt: str(), // 실거래일자
  })
  .passthrough();

// ── 해외주식 일별거래내역 조회 결과 요약 (`Output_1`). ──

export const overseasStockInquiryDailyTransactionSummaryOutputSchema = z
  .object({
    cus_fnm: str(), // 고객성명
    rnm_cfm_no: str(), // 실명확인번호
    rpm_tal: num(), // 입금총액
    drn_tal: num(), // 출금총액
    amt_sum: num(), // 금액합계
    tax_sum_amt: num(), // 세금합계금액
    fee_sum_amt: num(), // 수수료합계금액
  })
  .passthrough();

/**
 * 해외주식 일별거래내역 조회 (`POST /gbstock/inquiry/v1/dailyTransaction`) 응답.
 *
 * 응답 블록: `Output_0`: 배열, `Output_1`: 객체
 */
export const overseasStockInquiryDailyTransactionResponseSchema = z
  .object({
    ...envelope,
    /** 일별거래내역 조회 결과 */
    Output_0: z.array(overseasStockInquiryDailyTransactionOutputSchema).nullish(),
    /** 일별거래내역 조회 결과 요약 */
    Output_1: overseasStockInquiryDailyTransactionSummaryOutputSchema.nullish(),
  })
  .passthrough();

// ── 해외주식 기간손익 조회 결과 요약 (`Output_0`). ──

export const overseasStockInquiryPeriodPnlSummaryOutputSchema = z
  .object({
    act_fnm: str(), // 계좌성명
    byn_qty_sum: num(), // 매수수량합계
    fc_byn_amt_sum: num(), // 외화매수금액합계
    sll_qty_sum: num(), // 매도수량합계
    fc_sll_amt_sum: num(), // 외화매도금액합계
    fc_sby_pls_sum: num(), // 외화매매손익합계
    fc_sby_pft_rt: num(), // 외화매매수익율
    fc_sdr_xps_sum: num(), // 외화제비용합계
    fc_rzt_pls_sum: num(), // 외화실현손익합계
    fc_rzt_pft_rt: num(), // 외화실현수익율
  })
  .passthrough();

// ── 해외주식 기간손익 조회 결과 항목 (`Output_1` 배열 원소). ──

export const overseasStockInquiryPeriodPnlDailyOutputSchema = z
  .object({
    orr_dt: str(), // 주문일자 / YYYYMMDD
    fc_sec_trd_nat_cd: str(), // 외화증권거래국가코드 / 200.미국 070.일본 120.홍콩 160.상해 170.심천
    fc_sec_trd_nat_nm: str(), // 외화증권거래국가명
    trd_cur_cd: str(), // 거래통화코드 / KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY
    byn_qty: num(), // 매수수량
    byn_uit_pr: num(), // 매수단가
    fc_byn_amt1: num(), // 외화매수금액1
    sll_qty: num(), // 매도수량
    sll_uit_pr: num(), // 매도단가
    fc_sll_amt: num(), // 외화매도금액
    fc_sby_pls: num(), // 외화매매손익
    fc_sby_pft_rt: num(), // 외화매매수익율
    fc_sdr_xps: num(), // 외화제비용
    fc_rzt_pls: num(), // 외화실현손익
    fc_rzt_pft_rt: num(), // 외화실현수익율
  })
  .passthrough();

/**
 * 해외주식 기간손익 조회 (`POST /gbstock/inquiry/v1/periodPnl`) 응답.
 *
 * 응답 블록: `Output_0`: 객체, `Output_1`: 배열
 */
export const overseasStockInquiryPeriodPnlResponseSchema = z
  .object({
    ...envelope,
    /** 기간손익 조회 결과 요약 */
    Output_0: overseasStockInquiryPeriodPnlSummaryOutputSchema.nullish(),
    /** 기간손익 조회 결과 목록 */
    Output_1: z.array(overseasStockInquiryPeriodPnlDailyOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 기간손익 상세 조회 결과 항목 (`Output_0` 배열 원소). ──

export const overseasStockInquiryPeriodPnlDetailOutputSchema = z
  .object({
    iem_cd: str(), // 종목코드
    iem_nm: str(), // 종목명
    byn_qty: num(), // 매수수량
    byn_uit_pr: num(), // 매수단가
    fc_byn_amt1: num(), // 외화매수금액1
    sll_qty: num(), // 매도수량
    sll_uit_pr: num(), // 매도단가
    fc_sll_amt: num(), // 외화매도금액
    fc_sby_pls: num(), // 외화매매손익
    fc_sby_pft_rt: num(), // 외화매매수익율
    fc_sdr_xps: num(), // 외화제비용
    fc_rzt_pls: num(), // 외화실현손익
    fc_rzt_pft_rt: num(), // 외화실현수익율
  })
  .passthrough();

/**
 * 해외주식 기간손익 상세 조회 (`POST /gbstock/inquiry/v1/periodPnlDetail`) 응답.
 *
 * 응답 블록: `Output_0`: 배열
 */
export const overseasStockInquiryPeriodPnlDetailResponseSchema = z
  .object({
    ...envelope,
    /** 기간손익 상세 조회 결과 목록 */
    Output_0: z.array(overseasStockInquiryPeriodPnlDetailOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외증거금 통화별조회 결과 항목 (`Output_0` 배열 원소). ──

export const overseasStockInquiryMarginOutputSchema = z
  .object({
    cur_cd: str(), // 통화코드 / KRW.KRW USD.USD CNY.CNY HKD.HKD JPY.JPY
    dca: num(), // 예수금
    orr_wtm: num(), // 주문증거금
    ect_mgg_amt: num(), // 기타담보금액
    drn_pbl_amt: num(), // 출금가능금액
    fc_dca: num(), // 외화예수금
    fc_mgg_amt: num(), // 외화담보금액
    ect_mgg_fc_amt: num(), // 기타담보외화금액
    fc_drn_pbl_amt: num(), // 외화출금가능금액
    sby_bse_xcg_rt: num(), // 매매기준환율
    fc_rba: num(), // 외화미수금
    rba: num(), // 미수금
    fc_rvb_odu_fee: num(), // 외화미수연체료
    rvb_odu_fee: num(), // 미수연체료
    stl_af_dca: num(), // 결제후예수금
    stl_af_drn_pbl_amt: num(), // 결제후출금가능금액
    stl_af_fc_dca: num(), // 결제후외화예수금
    stl_af_fc_drn_pbl_amt: num(), // 결제후외화출금가능금액
  })
  .passthrough();

/**
 * 해외증거금 통화별조회 (`POST /gbstock/inquiry/v1/margin`) 응답.
 *
 * 응답 블록: `Output_0`: 배열
 */
export const overseasStockInquiryMarginResponseSchema = z
  .object({
    ...envelope,
    /** 해외증거금 통화별조회 결과 목록 */
    Output_0: z.array(overseasStockInquiryMarginOutputSchema).nullish(),
  })
  .passthrough();

// ── Response Types ──

/** 해외주식 매수가능금액·수량 조회 (`POST /gbstock/inquiry/v1/buyableAmount`) 응답. — `Output_0`: 객체 */
export type OverseasStockInquiryBuyableAmountResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryBuyableAmountResponseSchema>
>;
/** 해외주식 주문체결내역 조회 (`POST /gbstock/inquiry/v1/unexecuted`) 응답. — `Output_0`: 배열 */
export type OverseasStockInquiryUnexecutedResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryUnexecutedResponseSchema>
>;
/** 해외주식 잔고조회 (`POST /gbstock/inquiry/v1/balance`) 응답. — `Output_0`: 객체, `Output_1`: 배열 */
export type OverseasStockInquiryBalanceResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryBalanceResponseSchema>
>;
/** 해외주식 예약주문조회 (`POST /gbstock/inquiry/v1/reservedInquiry`) 응답. — `Output_0`: 배열 */
export type OverseasStockInquiryReservedInquiryResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryReservedInquiryResponseSchema>
>;
/** 해외주식 일별거래내역 조회 (`POST /gbstock/inquiry/v1/dailyTransaction`) 응답. — `Output_0`: 배열, `Output_1`: 객체 */
export type OverseasStockInquiryDailyTransactionResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryDailyTransactionResponseSchema>
>;
/** 해외주식 기간손익 조회 (`POST /gbstock/inquiry/v1/periodPnl`) 응답. — `Output_0`: 객체, `Output_1`: 배열 */
export type OverseasStockInquiryPeriodPnlResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryPeriodPnlResponseSchema>
>;
/** 해외주식 기간손익 상세 조회 (`POST /gbstock/inquiry/v1/periodPnlDetail`) 응답. — `Output_0`: 배열 */
export type OverseasStockInquiryPeriodPnlDetailResponse = CamelizeKeys<
  z.infer<typeof overseasStockInquiryPeriodPnlDetailResponseSchema>
>;
/** 해외증거금 통화별조회 (`POST /gbstock/inquiry/v1/margin`) 응답. — `Output_0`: 배열 */
export type OverseasStockInquiryMarginResponse = CamelizeKeys<z.infer<typeof overseasStockInquiryMarginResponseSchema>>;

// ── Response Map ──

export interface OverseasStockInquiryResponseMap {
  buyableAmount: OverseasStockInquiryBuyableAmountResponse;
  unexecuted: OverseasStockInquiryUnexecutedResponse;
  balance: OverseasStockInquiryBalanceResponse;
  reservedInquiry: OverseasStockInquiryReservedInquiryResponse;
  dailyTransaction: OverseasStockInquiryDailyTransactionResponse;
  periodPnl: OverseasStockInquiryPeriodPnlResponse;
  periodPnlDetail: OverseasStockInquiryPeriodPnlDetailResponse;
  margin: OverseasStockInquiryMarginResponse;
}
