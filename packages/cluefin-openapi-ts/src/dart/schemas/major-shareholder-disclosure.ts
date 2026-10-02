import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';
import { dartEnvelope, dartNumeric } from './common.js';

/** 자산양수도(기타), 풋백옵션 항목 */
export const treasuryStockAcquisitionDisposalPlanItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 보고 사유 */
  rp_rsn: z.string(),
  /** 자산양수ㆍ도 가액 */
  ast_inhtrf_prc: dartNumeric,
});

/** 부도발생 항목 */
export const realEstateDevelopmentItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 부도내용 */
  df_cn: z.string(),
  /** 부도금액 */
  df_amt: dartNumeric,
  /** 부도발생은행 */
  df_bnk: z.string(),
  /** 최종부도(당좌거래정지)일자 */
  dfd: z.string(),
  /** 부도사유 및 경위 */
  df_rs: z.string(),
});

/** 영업정지 항목 */
export const businessLetterItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 영업정지 분야 */
  bsnsp_rm: z.string(),
  /** 영업정지 내역(영업정지금액) */
  bsnsp_amt: dartNumeric,
  /** 영업정지 내역(최근매출총액) */
  rsl: dartNumeric,
  /** 영업정지 내역(매출액 대비) */
  sl_vs: z.string(),
  /** 영업정지 내역(대규모법인여부) */
  ls_atn: z.string(),
  /** 영업정지 내역(거래소 의무공시 해당 여부) */
  krx_stt_atn: z.string(),
  /** 영업정지 내용 */
  bsnsp_cn: z.string(),
  /** 영업정지사유 */
  bsnsp_rs: z.string(),
  /** 향후대책 */
  ft_ctp: z.string(),
  /** 영업정지영향 */
  bsnsp_af: z.string(),
  /** 영업정지일자 */
  bsnspd: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: dartNumeric,
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: dartNumeric,
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
});

/** 회생절차 개시신청 항목 */
export const corporateRehabilitationProceedingsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 신청인 (회사와의 관계) */
  apcnt: z.string(),
  /** 관할법원 */
  cpct: z.string(),
  /** 신청사유 */
  rq_rs: z.string(),
  /** 신청일자 */
  rqd: z.string(),
  /** 향후대책 및 일정 */
  ft_ctp_sc: z.string(),
});

/** 해산사유 발생 항목 */
export const dissolutionOccurrenceItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 해산사유 */
  ds_rs: z.string(),
  /** 해산사유발생일(결정일) */
  ds_rsd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: dartNumeric,
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: dartNumeric,
  /** 감사(감사위원)참석 여부 */
  adt_a_atn: z.string(),
});

/** 유상증자 결정 항목 */
export const securitiesGrantedDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 신주의 종류와 수(보통주식 (주)) */
  nstk_ostk_cnt: dartNumeric,
  /** 신주의 종류와 수(기타주식 (주)) */
  nstk_estk_cnt: dartNumeric,
  /** 1주당 액면가액 (원) */
  fv_ps: dartNumeric,
  /** 증자전 발행주식총수 (주)(보통주식 (주)) */
  bfic_tisstk_ostk: dartNumeric,
  /** 증자전 발행주식총수 (주)(기타주식 (주)) */
  bfic_tisstk_estk: dartNumeric,
  /** 자금조달의 목적(시설자금 (원)) */
  fdpp_fclt: dartNumeric,
  /** 자금조달의 목적(영업양수자금 (원)) ① 2019년 12월 9일부터 추가됨 */
  fdpp_bsninh: dartNumeric.nullish(),
  /** 자금조달의 목적(운영자금 (원)) */
  fdpp_op: dartNumeric,
  /** 자금조달의 목적(채무상환자금 (원)) ① 2019년 12월 9일부터 추가됨 */
  fdpp_dtrp: dartNumeric.nullish(),
  /** 자금조달의 목적(타법인 증권 취득자금 (원)) */
  fdpp_ocsa: dartNumeric,
  /** 자금조달의 목적(기타자금 (원)) */
  fdpp_etc: dartNumeric,
  /** 증자방식 */
  ic_mthn: z.string(),
  /** 공매도 해당여부 */
  ssl_at: z.string(),
  /** 공매도 시작일 */
  ssl_bgd: z.string().nullish(),
  /** 공매도 종료일 */
  ssl_edd: z.string().nullish(),
});

/** 무상증자 결정 항목 */
export const freeSecuritiesDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 신주의 종류와 수(보통주식 (주)) */
  nstk_ostk_cnt: dartNumeric,
  /** 신주의 종류와 수(기타주식 (주)) */
  nstk_estk_cnt: dartNumeric,
  /** 1주당 액면가액 (원) */
  fv_ps: dartNumeric,
  /** 증자전 발행주식총수 (주)(보통주식 (주)) */
  bfic_tisstk_ostk: dartNumeric,
  /** 증자전 발행주식총수 (주)(기타주식 (주)) */
  bfic_tisstk_estk: dartNumeric,
  /** 신주배정기준일 */
  nstk_asstd: z.string(),
  /** 1주당 신주배정 주식수(보통주식 (주)) */
  nstk_ascnt_ps_ostk: dartNumeric,
  /** 1주당 신주배정 주식수(기타주식 (주)) */
  nstk_ascnt_ps_estk: dartNumeric,
  /** 신주의 배당기산일 */
  nstk_dividrk: z.string(),
  /** 신주권교부예정일 */
  nstk_dlprd: z.string(),
  /** 신주의 상장 예정일 */
  nstk_lstprd: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: dartNumeric,
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: dartNumeric,
  /** 감사(감사위원)참석 여부 */
  adt_a_atn: z.string(),
});

/** 유무상증자 결정 항목 */
export const paidInCapitalReductionDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 유상증자(신주의 종류와 수(보통주식 (주))) */
  piic_nstk_ostk_cnt: dartNumeric,
  /** 유상증자(신주의 종류와 수(기타주식 (주))) */
  piic_nstk_estk_cnt: dartNumeric,
  /** 유상증자(1주당 액면가액 (원)) */
  piic_fv_ps: dartNumeric,
  /** 유상증자(증자전 발행주식총수 (주)(보통주식 (주))) */
  piic_bfic_tisstk_ostk: dartNumeric,
  /** 유상증자(증자전 발행주식총수 (주)(기타주식 (주))) */
  piic_bfic_tisstk_estk: dartNumeric,
  /** 유상증자(자금조달의 목적(시설자금 (원))) */
  piic_fdpp_fclt: dartNumeric,
  /** 유상증자(자금조달의 목적(영업양수자금 (원))) ① 2019년 12월 9일부터 추가됨 */
  piic_fdpp_bsninh: dartNumeric.nullish(),
  /** 유상증자(자금조달의 목적(운영자금 (원))) */
  piic_fdpp_op: dartNumeric,
  /** 유상증자(자금조달의 목적(채무상환자금 (원))) ① 2019년 12월 9일부터 추가됨 */
  piic_fdpp_dtrp: dartNumeric.nullish(),
  /** 유상증자(자금조달의 목적(타법인 증권 취득자금 (원))) */
  piic_fdpp_ocsa: dartNumeric,
  /** 유상증자(자금조달의 목적(기타자금 (원))) */
  piic_fdpp_etc: dartNumeric,
  /** 유상증자(증자방식) */
  piic_ic_mthn: z.string(),
  /** 무상증자(신주의 종류와 수(보통주식 (주))) */
  fric_nstk_ostk_cnt: dartNumeric,
  /** 무상증자(신주의 종류와 수(기타주식 (주))) */
  fric_nstk_estk_cnt: dartNumeric,
  /** 무상증자(1주당 액면가액 (원)) */
  fric_fv_ps: dartNumeric,
  /** 무상증자(증자전 발행주식총수(보통주식 (주))) */
  fric_bfic_tisstk_ostk: dartNumeric,
  /** 무상증자(증자전 발행주식총수(기타주식 (주))) */
  fric_bfic_tisstk_estk: dartNumeric,
  /** 무상증자(신주배정기준일) */
  fric_nstk_asstd: z.string(),
  /** 무상증자(1주당 신주배정 주식수(보통주식 (주))) */
  fric_nstk_ascnt_ps_ostk: dartNumeric,
  /** 무상증자(1주당 신주배정 주식수(기타주식 (주))) */
  fric_nstk_ascnt_ps_estk: dartNumeric,
  /** 무상증자(신주의 배당기산일) */
  fric_nstk_dividrk: z.string(),
  /** 무상증자(신주권교부예정일) */
  fric_nstk_dlprd: z.string(),
  /** 무상증자(신주의 상장 예정일) */
  fric_nstk_lstprd: z.string(),
  /** 무상증자(이사회결의일(결정일)) */
  fric_bddd: z.string(),
  /** 무상증자(사외이사 참석여부(참석(명))) */
  fric_od_a_at_t: dartNumeric,
  /** 무상증자(사외이사 참석여부(불참(명))) */
  fric_od_a_at_b: dartNumeric,
  /** 무상증자(감사(감사위원)참석 여부) */
  fric_adt_a_atn: z.string(),
  /** 공매도 해당여부 */
  ssl_at: z.string(),
  /** 공매도 시작일 */
  ssl_bgd: z.string().nullish(),
  /** 공매도 종료일 */
  ssl_edd: z.string().nullish(),
});

/** 감자 결정 항목 */
export const capitalReductionDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 감자주식의 종류와 수(보통주식 (주)) */
  crstk_ostk_cnt: dartNumeric,
  /** 감자주식의 종류와 수(기타주식 (주)) */
  crstk_estk_cnt: dartNumeric,
  /** 1주당 액면가액 (원) */
  fv_ps: dartNumeric,
  /** 감자전후 자본금(감자전 (원)) */
  bfcr_cpt: dartNumeric,
  /** 감자전후 자본금(감자후 (원)) */
  atcr_cpt: dartNumeric,
  /** 감자전후 발행주식수(보통주식 (주)(감자전 (원))) */
  bfcr_tisstk_ostk: dartNumeric,
  /** 감자전후 발행주식수(보통주식 (주)(감자후 (원))) */
  atcr_tisstk_ostk: dartNumeric,
  /** 감자전후 발행주식수(기타주식 (주)(감자전 (원))) */
  bfcr_tisstk_estk: dartNumeric,
  /** 감자전후 발행주식수(기타주식 (주)(감자후 (원))) */
  atcr_tisstk_estk: dartNumeric,
  /** 감자비율(보통주식 (%)) */
  cr_rt_ostk: z.string(),
  /** 감자비율(기타주식 (%)) */
  cr_rt_estk: z.string(),
  /** 감자기준일 */
  cr_std: z.string(),
  /** 감자방법 */
  cr_mth: z.string(),
  /** 감자사유 */
  cr_rs: z.string(),
  /** 감자일정(주주총회 예정일) */
  crsc_gmtsck_prd: z.string(),
  /** 감자일정(명의개서정지기간) */
  crsc_trnmsppd: z.string(),
  /** 감자일정(구주권 제출기간) ① 2019년 12월 8일까지 사용됨 */
  crsc_osprpd: z.string(),
  /** 감자일정(매매거래 정지예정기간) ① 2019년 12월 8일까지 사용됨 */
  crsc_trspprpd: z.string(),
  /** 감자일정(구주권 제출기간(시작일)) ② 2019년 12월 9일부터 추가됨 */
  crsc_osprpd_bgd: z.string().nullish(),
  /** 감자일정(구주권 제출기간(종료일)) ② 2019년 12월 9일부터 추가됨 */
  crsc_osprpd_edd: z.string().nullish(),
  /** 감자일정(매매거래 정지예정기간(시작일)) ② 2019년 12월 9일부터 추가됨 */
  crsc_trspprpd_bgd: z.string().nullish(),
  /** 감자일정(매매거래 정지예정기간(종료일)) ② 2019년 12월 9일부터 추가됨 */
  crsc_trspprpd_edd: z.string().nullish(),
  /** 감자일정(신주권교부예정일) */
  crsc_nstkdlprd: z.string(),
  /** 감자일정(신주상장예정일) */
  crsc_nstklstprd: z.string(),
  /** 채권자 이의제출기간(시작일) */
  cdobprpd_bgd: z.string(),
  /** 채권자 이의제출기간(종료일) */
  cdobprpd_edd: z.string(),
  /** 구주권제출 및 신주권교부장소 */
  ospr_nstkdl_pl: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: dartNumeric,
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: dartNumeric,
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
});

/** 재권은행 등의 관리절차 개시 항목 */
export const governmentBondManagerReplacementItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 관리절차개시 결정일자 */
  mngt_pcbg_dd: z.string(),
  /** 관리기관 */
  mngt_int: z.string(),
  /** 관리기간 */
  mngt_pd: z.string(),
  /** 관리사유 */
  mngt_rs: z.string(),
  /** 확인일자 */
  cfd: z.string(),
});

/** 소송 등의 제기 항목 */
export const profitRevocationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사건의 명칭 */
  icnm: z.string(),
  /** 원고ㆍ신청인 */
  ac_ap: z.string(),
  /** 청구내용 */
  rq_cn: z.string(),
  /** 관할법원 */
  cpct: z.string(),
  /** 향후대책 */
  ft_ctp: z.string(),
  /** 제기일자 */
  lgd: z.string(),
  /** 확인일자 */
  cfd: z.string(),
});

/** 해외 증권시장 주권등 상장 결정 항목 */
export const overseasSecuritiesTradingResolutionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 상장예정주식 종류ㆍ수(주)(보통주식) */
  lstprstk_ostk_cnt: z.string(),
  /** 상장예정주식 종류ㆍ수(주)(기타주식) */
  lstprstk_estk_cnt: z.string(),
  /** 발행주식 총수(주)(보통주식) */
  tisstk_ostk: z.string(),
  /** 발행주식 총수(주)(기타주식) */
  tisstk_estk: z.string(),
  /** 공모방법(신주발행 (주)) */
  psmth_nstk_sl: z.string(),
  /** 공모방법(구주매출 (주)) */
  psmth_ostk_sl: z.string(),
  /** 자금조달(신주발행) 목적 */
  fdpp: z.string(),
  /** 상장증권(원주상장 (주)) */
  lststk_orlst: z.string(),
  /** 상장증권(DR상장 (주)) */
  lststk_drlst: z.string(),
  /** 상장거래소(소재국가) */
  lstex_nt: z.string(),
  /** 해외상장목적 */
  lstpp: z.string(),
  /** 상장예정일자 */
  lstprd: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원)참석여부 */
  adt_a_atn: z.string(),
});

/** 해외 증권시장 주권등 상장폐지 결정 항목 */
export const overseasSecuritiesTradingDelistingResolutionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 상장폐지주식 종류ㆍ수(주)(보통주식) */
  dlststk_ostk_cnt: z.string(),
  /** 상장폐지주식 종류ㆍ수(주)(기타주식) */
  dlststk_estk_cnt: z.string(),
  /** 상장거래소(소재국가) */
  lstex_nt: z.string(),
  /** 폐지신청예정일자 */
  dlstrq_prd: z.string(),
  /** 폐지(예정)일자 */
  dlst_prd: z.string(),
  /** 폐지사유 */
  dlst_rs: z.string(),
  /** 이사회결의일(확인일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원)참석여부 */
  adt_a_atn: z.string(),
});

/** 해외 증권시장 주권등 상장 항목 */
export const overseasSecuritiesTradingStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 상장주식 종류 및 수(보통주식(주)) */
  lststk_ostk_cnt: z.string(),
  /** 상장주식 종류 및 수(기타주식(주)) */
  lststk_estk_cnt: z.string(),
  /** 상장거래소(소재국가) */
  lstex_nt: z.string(),
  /** 종목 명 (code) */
  stk_cd: z.string(),
  /** 상장일자 */
  lstd: z.string(),
  /** 확인일자 */
  cfd: z.string(),
});

/** 해외 증권시장 주권등 상장폐지 항목 */
export const overseasSecuritiesTradingStatusDelistingItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 상장거래소 및 소재국가 */
  lstex_nt: z.string(),
  /** 상장폐지주식의 종류(보통주식(주)) */
  dlststk_ostk_cnt: z.string(),
  /** 상장폐지주식의 종류(기타주식(주)) */
  dlststk_estk_cnt: z.string(),
  /** 매매거래종료일 */
  tredd: z.string(),
  /** 폐지사유 */
  dlst_rs: z.string(),
  /** 확인일자 */
  cfd: z.string(),
});

/** 전환사채권 발행결정 항목 */
export const convertibleBondIssuanceDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사채의 종류(회차) */
  bd_tm: z.string(),
  /** 사채의 종류(종류) */
  bd_knd: z.string(),
  /** 사채의 권면(전자등록)총액 (원) */
  bd_fta: z.string(),
  /** 정관상 잔여 발행한도 (원) */
  atcsc_rmislmt: z.string(),
  /** 해외발행(권면(전자등록)총액) */
  ovis_fta: z.string(),
  /** 해외발행(권면(전자등록)총액(통화단위)) */
  ovis_fta_crn: z.string(),
  /** 해외발행(기준환율등) */
  ovis_ster: z.string(),
  /** 해외발행(발행지역) */
  ovis_isar: z.string(),
  /** 해외발행(해외상장시 시장의 명칭) */
  ovis_mktnm: z.string(),
  /** 자금조달의 목적(시설자금 (원)) */
  fdpp_fclt: z.string(),
  /** 자금조달의 목적(영업양수자금 (원)) */
  fdpp_bsninh: z.string(),
  /** 자금조달의 목적(운영자금 (원)) */
  fdpp_op: z.string(),
  /** 자금조달의 목적(채무상환자금 (원)) */
  fdpp_dtrp: z.string(),
  /** 자금조달의 목적(타법인 증권 취득자금 (원)) */
  fdpp_ocsa: z.string(),
  /** 자금조달의 목적(기타자금 (원)) */
  fdpp_etc: z.string(),
  /** 사채의 이율(표면이자율 (%)) */
  bd_intr_ex: z.string(),
  /** 사채의 이율(만기이자율 (%)) */
  bd_intr_sf: z.string(),
  /** 사채만기일 */
  bd_mtd: z.string(),
  /** 사채발행방법 */
  bdis_mthn: z.string(),
  /** 전환에 관한 사항(전환비율 (%)) */
  cv_rt: z.string(),
  /** 전환에 관한 사항(전환가액 (원/주)) */
  cv_prc: z.string(),
  /** 전환에 관한 사항(전환에 따라 발행할 주식(종류)) */
  cvisstk_knd: z.string(),
  /** 전환에 관한 사항(전환에 따라 발행할 주식(주식수)) */
  cvisstk_cnt: z.string(),
  /** 전환에 관한 사항(전환에 따라 발행할 주식(주식총수 대비 비율(%))) */
  cvisstk_tisstk_vs: z.string(),
  /** 전환에 관한 사항(전환청구기간(시작일)) */
  cvrqpd_bgd: z.string(),
  /** 전환에 관한 사항(전환청구기간(종료일)) */
  cvrqpd_edd: z.string(),
  /** 전환에 관한 사항(시가하락에 따른 전환가액 조정(최저 조정가액 (원))) */
  act_mktprcfl_cvprc_lwtrsprc: z.string(),
  /** 전환에 관한 사항(시가하락에 따른 전환가액 조정(최저 조정가액 근거)) */
  act_mktprcfl_cvprc_lwtrsprc_bs: z.string(),
  /** 전환에 관한 사항(시가하락에 따른 전환가액 조정(발행당시 전환가액의 70% 미만으로 조정가능한 잔여 발행한도 (원))) */
  rmislmt_lt70p: z.string(),
  /** 합병 관련 사항 */
  abmg: z.string(),
  /** 청약일 */
  sbd: z.string(),
  /** 납입일 */
  pymd: z.string(),
  /** 대표주관회사 */
  rpmcmp: z.string(),
  /** 보증기관 */
  grint: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석 (명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참 (명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
  /** 당해 사채의 해외발행과 연계된 대차거래 내역 */
  ovis_ltdtl: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
});

/** 신주인수권부사채권 발행결정 항목 */
export const newStockWarrantBondIssuanceDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사채의 종류(회차) */
  bd_tm: z.string(),
  /** 사채의 종류(종류) */
  bd_knd: z.string(),
  /** 사채의 권면(전자등록)총액 (원) */
  bd_fta: z.string(),
  /** 정관상 잔여 발행한도 (원) */
  atcsc_rmislmt: z.string(),
  /** 해외발행(권면(전자등록)총액) */
  ovis_fta: z.string(),
  /** 해외발행(권면(전자등록)총액(통화단위)) */
  ovis_fta_crn: z.string(),
  /** 해외발행(기준환율등) */
  ovis_ster: z.string(),
  /** 해외발행(발행지역) */
  ovis_isar: z.string(),
  /** 해외발행(해외상장시 시장의 명칭) */
  ovis_mktnm: z.string(),
  /** 자금조달의 목적(시설자금 (원)) */
  fdpp_fclt: z.string(),
  /** 자금조달의 목적(영업양수자금 (원)) */
  fdpp_bsninh: z.string(),
  /** 자금조달의 목적(운영자금 (원)) */
  fdpp_op: z.string(),
  /** 자금조달의 목적(채무상환자금 (원)) */
  fdpp_dtrp: z.string(),
  /** 자금조달의 목적(타법인 증권 취득자금 (원)) */
  fdpp_ocsa: z.string(),
  /** 자금조달의 목적(기타자금 (원)) */
  fdpp_etc: z.string(),
  /** 사채의 이율(표면이자율 (%)) */
  bd_intr_ex: z.string(),
  /** 사채의 이율(만기이자율 (%)) */
  bd_intr_sf: z.string(),
  /** 사채만기일 */
  bd_mtd: z.string(),
  /** 사채발행방법 */
  bdis_mthn: z.string(),
  /** 신주인수권에 관한 사항(행사비율 (%)) */
  ex_rt: z.string(),
  /** 신주인수권에 관한 사항(행사가액 (원/주)) */
  ex_prc: z.string(),
  /** 신주인수권에 관한 사항(행사가액 결정방법) */
  ex_prc_dmth: z.string(),
  /** 신주인수권에 관한 사항(사채와 인수권의 분리여부) */
  bdwt_div_atn: z.string(),
  /** 신주인수권에 관한 사항(신주대금 납입방법) */
  nstk_pym_mth: z.string(),
  /** 신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(종류)) */
  nstk_isstk_knd: z.string(),
  /** 신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(주식수)) */
  nstk_isstk_cnt: z.string(),
  /** 신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(주식총수 대비 비율(%))) */
  nstk_isstk_tisstk_vs: z.string(),
  /** 신주인수권에 관한 사항(권리행사기간(시작일)) */
  expd_bgd: z.string(),
  /** 신주인수권에 관한 사항(권리행사기간(종료일)) */
  expd_edd: z.string(),
  /** 신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(최저 조정가액 (원))) */
  act_mktprcfl_cvprc_lwtrsprc: z.string(),
  /** 신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(최저 조정가액 근거)) */
  act_mktprcfl_cvprc_lwtrsprc_bs: z.string(),
  /** 신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(발행당시 행사가액의 70% 미만으로 조정가능한 잔여 발행한도 (원))) */
  rmislmt_lt70p: z.string(),
  /** 합병 관련 사항 */
  abmg: z.string(),
  /** 청약일 */
  sbd: z.string(),
  /** 납입일 */
  pymd: z.string(),
  /** 대표주관회사 */
  rpmcmp: z.string(),
  /** 보증기관 */
  grint: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석 (명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참 (명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
  /** 당해 사채의 해외발행과 연계된 대차거래 내역 */
  ovis_ltdtl: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
});

/** 교환사채권 발행결정 항목 */
export const corporateBondIssuanceDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사채의 종류(회차) */
  bd_tm: z.string(),
  /** 사채의 종류(종류) */
  bd_knd: z.string(),
  /** 사채의 권면(전자등록)총액 (원) */
  bd_fta: z.string(),
  /** 해외발행(권면(전자등록)총액) */
  ovis_fta: z.string(),
  /** 해외발행(권면(전자등록)총액(통화단위)) */
  ovis_fta_crn: z.string(),
  /** 해외발행(기준환율등) */
  ovis_ster: z.string(),
  /** 해외발행(발행지역) */
  ovis_isar: z.string(),
  /** 해외발행(해외상장시 시장의 명칭) */
  ovis_mktnm: z.string(),
  /** 자금조달의 목적(시설자금 (원)) */
  fdpp_fclt: z.string(),
  /** 자금조달의 목적(영업양수자금 (원)) */
  fdpp_bsninh: z.string(),
  /** 자금조달의 목적(운영자금 (원)) */
  fdpp_op: z.string(),
  /** 자금조달의 목적(채무상환자금 (원)) */
  fdpp_dtrp: z.string(),
  /** 자금조달의 목적(타법인 증권 취득자금 (원)) */
  fdpp_ocsa: z.string(),
  /** 자금조달의 목적(기타자금 (원)) */
  fdpp_etc: z.string(),
  /** 사채의 이율(표면이자율 (%)) */
  bd_intr_sf: z.string(),
  /** 사채의 이율(만기이자율 (%)) */
  bd_intr_ex: z.string(),
  /** 사채만기일 */
  bd_mtd: z.string(),
  /** 사채발행방법 */
  bdis_mthn: z.string(),
  /** 교환에 관한 사항(교환비율 (%)) */
  ex_rt: z.string(),
  /** 교환에 관한 사항(교환가액 (원/주)) */
  ex_prc: z.string(),
  /** 교환에 관한 사항(교환가액 결정방법) */
  ex_prc_dmth: z.string(),
  /** 교환에 관한 사항(교환대상(종류)) */
  extg: z.string(),
  /** 교환에 관한 사항(교환대상(주식수)) */
  extg_stkcnt: z.string(),
  /** 교환에 관한 사항(교환대상(주식총수 대비 비율(%))) */
  extg_tisstk_vs: z.string(),
  /** 교환에 관한 사항(교환청구기간(시작일)) */
  exrqpd_bgd: z.string(),
  /** 교환에 관한 사항(교환청구기간(종료일)) */
  exrqpd_edd: z.string(),
  /** 청약일 */
  sbd: z.string(),
  /** 납입일 */
  pymd: z.string(),
  /** 대표주관회사 */
  rpmcmp: z.string(),
  /** 보증기관 */
  grint: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석 (명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참 (명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
  /** 당해 사채의 해외발행과 연계된 대차거래 내역 */
  ovis_ltdtl: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
});

/** 채권은행 등의 관리절차 종단 항목 */
export const governmentBondManagerTransferTerminationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 관리절차중단 결정일자 */
  mngt_pcsp_dd: z.string(),
  /** 관리기관 */
  mngt_int: z.string(),
  /** 중단사유 */
  sp_rs: z.string(),
  /** 향후대책 */
  ft_ctp: z.string(),
  /** 확인일자 */
  cfd: z.string(),
});

/** 상각형 조건부자본증권 발행결정 항목 */
export const reorganizationPlanApprovedRulingItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사채의 종류(회차) */
  bd_tm: z.string(),
  /** 사채의 종류(종류) */
  bd_knd: z.string(),
  /** 사채의 권면(전자등록)총액 (원) */
  bd_fta: z.string(),
  /** 해외발행(권면(전자등록)총액) */
  ovis_fta: z.string(),
  /** 해외발행(권면(전자등록)총액(통화단위)) */
  ovis_fta_crn: z.string(),
  /** 해외발행(기준환율등) */
  ovis_ster: z.string(),
  /** 해외발행(발행지역) */
  ovis_isar: z.string(),
  /** 해외발행(해외상장시 시장의 명칭) */
  ovis_mktnm: z.string(),
  /** 자금조달의 목적(시설자금 (원)) */
  fdpp_fclt: z.string(),
  /** 자금조달의 목적(영업양수자금 (원)) */
  fdpp_bsninh: z.string(),
  /** 자금조달의 목적(운영자금 (원)) */
  fdpp_op: z.string(),
  /** 자금조달의 목적(채무상환자금 (원)) */
  fdpp_dtrp: z.string(),
  /** 자금조달의 목적(타법인 증권 취득자금 (원)) */
  fdpp_ocsa: z.string(),
  /** 자금조달의 목적(기타자금 (원)) */
  fdpp_etc: z.string(),
  /** 사채의 이율(표면이자율 (%)) */
  bd_intr_sf: z.string(),
  /** 사채의 이율(만기이자율 (%)) */
  bd_intr_ex: z.string(),
  /** 사채만기일 */
  bd_mtd: z.string(),
  /** 채무재조정에 관한 사항(채무재조정의 범위) */
  dbtrs_sc: z.string(),
  /** 청약일 */
  sbd: z.string(),
  /** 납입일 */
  pymd: z.string(),
  /** 대표주관회사 */
  rpmcmp: z.string(),
  /** 보증기관 */
  grint: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석 (명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참 (명)) */
  od_a_at_b: z.string(),
  /** 감사(감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
  /** 당해 사채의 해외발행과 연계된 대차거래 내역 */
  ovis_ltdtl: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
});

/** 자기주식 취득 결정 항목 */
export const treasuryStockAcquisitionDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 취득예정주식(주)(보통주식) */
  aqpln_stk_ostk: z.string(),
  /** 취득예정주식(주)(기타주식) */
  aqpln_stk_estk: z.string(),
  /** 취득예정금액(원)(보통주식) */
  aqpln_prc_ostk: z.string(),
  /** 취득예정금액(원)(기타주식) */
  aqpln_prc_estk: z.string(),
  /** 취득예상기간(시작일) */
  aqexpd_bgd: z.string(),
  /** 취득예상기간(종료일) */
  aqexpd_edd: z.string(),
  /** 보유예상기간(시작일) */
  hdexpd_bgd: z.string(),
  /** 보유예상기간(종료일) */
  hdexpd_edd: z.string(),
  /** 취득목적 */
  aq_pp: z.string(),
  /** 취득방법 */
  aq_mth: z.string(),
  /** 위탁투자중개업자 */
  cs_iv_bk: z.string(),
  /** 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(보통주식)) */
  aq_wtn_div_ostk: z.string(),
  /** 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%))) */
  aq_wtn_div_ostk_rt: z.string(),
  /** 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(기타주식)) */
  aq_wtn_div_estk: z.string(),
  /** 취득 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%))) */
  aq_wtn_div_estk_rt: z.string(),
  /** 취득 전 자기주식 보유현황(기타취득(주)(보통주식)) */
  eaq_ostk: z.string(),
  /** 취득 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_ostk_rt: z.string(),
  /** 취득 전 자기주식 보유현황(기타취득(주)(기타주식)) */
  eaq_estk: z.string(),
  /** 취득 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_estk_rt: z.string(),
  /** 취득결정일 */
  aq_dd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원)참석여부 */
  adt_a_atn: z.string(),
  /** 1일 매수 주문수량 한도(보통주식) */
  d1_prodlm_ostk: z.string(),
  /** 1일 매수 주문수량 한도(기타주식) */
  d1_prodlm_estk: z.string(),
});

/** 자기주식 처분 결정 항목 */
export const treasuryStockDisposalDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 처분예정주식(주)(보통주식) */
  dppln_stk_ostk: z.string(),
  /** 처분예정주식(주)(기타주식) */
  dppln_stk_estk: z.string(),
  /** 처분 대상 주식가격(원)(보통주식) */
  dpstk_prc_ostk: z.string(),
  /** 처분 대상 주식가격(원)(기타주식) */
  dpstk_prc_estk: z.string(),
  /** 처분예정금액(원)(보통주식) */
  dppln_prc_ostk: z.string(),
  /** 처분예정금액(원)(기타주식) */
  dppln_prc_estk: z.string(),
  /** 처분예정기간(시작일) */
  dpprpd_bgd: z.string(),
  /** 처분예정기간(종료일) */
  dpprpd_edd: z.string(),
  /** 처분목적 */
  dp_pp: z.string(),
  /** 처분방법(시장을 통한 매도(주)) */
  dp_m_mkt: z.string(),
  /** 처분방법(시간외대량매매(주)) */
  dp_m_ovtm: z.string(),
  /** 처분방법(장외처분(주)) */
  dp_m_otc: z.string(),
  /** 처분방법(기타(주)) */
  dp_m_etc: z.string(),
  /** 위탁투자중개업자 */
  cs_iv_bk: z.string(),
  /** 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(보통주식)) */
  aq_wtn_div_ostk: z.string(),
  /** 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%))) */
  aq_wtn_div_ostk_rt: z.string(),
  /** 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(기타주식)) */
  aq_wtn_div_estk: z.string(),
  /** 처분 전 자기주식 보유현황(배당가능이익 범위 내 취득(주)(비율(%))) */
  aq_wtn_div_estk_rt: z.string(),
  /** 처분 전 자기주식 보유현황(기타취득(주)(보통주식)) */
  eaq_ostk: z.string(),
  /** 처분 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_ostk_rt: z.string(),
  /** 처분 전 자기주식 보유현황(기타취득(주)(기타주식)) */
  eaq_estk: z.string(),
  /** 처분 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_estk_rt: z.string(),
  /** 처분결정일 */
  dp_dd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원)참석여부 */
  adt_a_atn: z.string(),
  /** 1일 매도 주문수량 한도(보통주식) */
  d1_slodlm_ostk: z.string(),
  /** 1일 매도 주문수량 한도(기타주식) */
  d1_slodlm_estk: z.string(),
});

/** 자기주식취득 신탁계약 체결 결정 항목 */
export const treasuryStockTrustContractDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 계약금액(원) */
  ctr_prc: z.string(),
  /** 계약기간(시작일) */
  ctr_pd_bgd: z.string(),
  /** 계약기간(종료일) */
  ctr_pd_edd: z.string(),
  /** 계약목적 */
  ctr_pp: z.string(),
  /** 계약체결기관 */
  ctr_cns_int: z.string(),
  /** 계약체결 예정일자 */
  ctr_cns_prd: z.string(),
  /** 계약 전 자기주식 보유현황(배당가능범위 내 취득(주)(보통주식)) */
  aq_wtn_div_ostk: z.string(),
  /** 계약 전 자기주식 보유현황(배당가능범위 내 취득(주)(비율(%))) */
  aq_wtn_div_ostk_rt: z.string(),
  /** 계약 전 자기주식 보유현황(배당가능범위 내 취득(주)(기타주식)) */
  aq_wtn_div_estk: z.string(),
  /** 계약 전 자기주식 보유현황(배당가능범위 내 취득(주)(비율(%))) */
  aq_wtn_div_estk_rt: z.string(),
  /** 계약 전 자기주식 보유현황(기타취득(주)(보통주식)) */
  eaq_ostk: z.string(),
  /** 계약 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_ostk_rt: z.string(),
  /** 계약 전 자기주식 보유현황(기타취득(주)(기타주식)) */
  eaq_estk: z.string(),
  /** 계약 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_estk_rt: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원)참석여부 */
  adt_a_atn: z.string(),
  /** 위탁투자중개업자 */
  cs_iv_bk: z.string(),
});

/** 자기주식취득 신탁계약 해지 결정 항목 */
export const treasuryStockTrustContractTerminationDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 계약금액(원)(해지 전) */
  ctr_prc_bfcc: z.string(),
  /** 계약금액(원)(해지 후) */
  ctr_prc_atcc: z.string(),
  /** 해지 전 계약기간(시작일) */
  ctr_pd_bfcc_bgd: z.string(),
  /** 해지 전 계약기간(종료일) */
  ctr_pd_bfcc_edd: z.string(),
  /** 해지목적 */
  cc_pp: z.string(),
  /** 해지기관 */
  cc_int: z.string(),
  /** 해지예정일자 */
  cc_prd: z.string(),
  /** 해지후 신탁재산의 반환방법 */
  tp_rm_atcc: z.string(),
  /** 해지 전 자기주식 보유현황(배당가능범위 내 취득(주)(보통주식)) */
  aq_wtn_div_ostk: z.string(),
  /** 해지 전 자기주식 보유현황(배당가능범위 내 취득(주)(비율(%))) */
  aq_wtn_div_ostk_rt: z.string(),
  /** 해지 전 자기주식 보유현황(배당가능범위 내 취득(주)(기타주식)) */
  aq_wtn_div_estk: z.string(),
  /** 해지 전 자기주식 보유현황(배당가능범위 내 취득(주)(비율(%))) */
  aq_wtn_div_estk_rt: z.string(),
  /** 해지 전 자기주식 보유현황(기타취득(주)(보통주식)) */
  eaq_ostk: z.string(),
  /** 해지 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_ostk_rt: z.string(),
  /** 해지 전 자기주식 보유현황(기타취득(주)(기타주식)) */
  eaq_estk: z.string(),
  /** 해지 전 자기주식 보유현황(기타취득(주)(비율(%))) */
  eaq_estk_rt: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원)참석여부 */
  adt_a_atn: z.string(),
});

/** 영업양수 결정 항목 */
export const businessPlanDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 양수영업 */
  inh_bsn: z.string(),
  /** 양수영업 주요내용 */
  inh_bsn_mc: z.string(),
  /** 양수가액(원) */
  inh_prc: z.string(),
  /** 영업전부의 양수 여부 */
  absn_inh_atn: z.string(),
  /** 재무내용(원)(자산액(양수대상 영업부문(A))) */
  ast_inh_bsn: z.string(),
  /** 재무내용(원)(자산액(당사전체(B))) */
  ast_cmp_all: z.string(),
  /** 재무내용(원)(자산액(비중(%)(A/B))) */
  ast_rt: z.string(),
  /** 재무내용(원)(매출액(양수대상 영업부문(A))) */
  sl_inh_bsn: z.string(),
  /** 재무내용(원)(매출액(당사전체(B))) */
  sl_cmp_all: z.string(),
  /** 재무내용(원)(매출액(비중(%)(A/B))) */
  sl_rt: z.string(),
  /** 재무내용(원)(부채액(양수대상 영업부문(A))) */
  dbt_inh_bsn: z.string(),
  /** 재무내용(원)(부채액(당사전체(B))) */
  dbt_cmp_all: z.string(),
  /** 재무내용(원)(부채액(비중(%)(A/B))) */
  dbt_rt: z.string(),
  /** 양수목적 */
  inh_pp: z.string(),
  /** 양수영향 */
  inh_af: z.string(),
  /** 양수예정일자(계약체결일) */
  inh_prd_ctr_cnsd: z.string(),
  /** 양수예정일자(양수기준일) */
  inh_prd_inh_std: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 양수대금지급 */
  inh_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 주주총회 특별결의 여부 */
  gmtsck_spd_atn: z.string(),
  /** 주주총회 예정일자 */
  gmtsck_prd: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 우회상장 해당 여부 */
  bdlst_atn: z.string(),
  /** 향후 6월이내 제3자배정 증자 등 계획 */
  n6m_tpai_plann: z.string(),
  /** 타법인의 우회상장 요건 충족여부 */
  otcpr_bdlst_sf_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 영업양도 결정 항목 */
export const businessTransferDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 양도영업 */
  trf_bsn: z.string(),
  /** 양도영업 주요내용 */
  trf_bsn_mc: z.string(),
  /** 양도가액(원) */
  trf_prc: z.string(),
  /** 재무내용(원)(자산액(양도대상 영업부문(A))) */
  ast_trf_bsn: z.string(),
  /** 재무내용(원)(자산액(당사전체(B))) */
  ast_cmp_all: z.string(),
  /** 재무내용(원)(자산액(비중(%)(A/B))) */
  ast_rt: z.string(),
  /** 재무내용(원)(매출액(양도대상 영업부문(A))) */
  sl_trf_bsn: z.string(),
  /** 재무내용(원)(매출액(당사전체(B))) */
  sl_cmp_all: z.string(),
  /** 재무내용(원)(매출액(비중(%)(A/B))) */
  sl_rt: z.string(),
  /** 양도목적 */
  trf_pp: z.string(),
  /** 양도영향 */
  trf_af: z.string(),
  /** 양도예정일자(계약체결일) */
  trf_prd_ctr_cnsd: z.string(),
  /** 양도예정일자(양도기준일) */
  trf_prd_trf_std: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 양도대금지급 */
  trf_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 주주총회 특별결의 여부 */
  gmtsck_spd_atn: z.string(),
  /** 주주총회 예정일자 */
  gmtsck_prd: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 유형자산 양수 결정 항목 */
export const tangibleAssetPlanDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 자산구분 */
  ast_sen: z.string(),
  /** 자산명 */
  ast_nm: z.string(),
  /** 양수내역(양수금액(원)) */
  inhdtl_inhprc: z.string(),
  /** 양수내역(자산총액(원)) */
  inhdtl_tast: z.string(),
  /** 양수내역(자산총액대비(%)) */
  inhdtl_tast_vs: z.string(),
  /** 양수목적 */
  inh_pp: z.string(),
  /** 양수영향 */
  inh_af: z.string(),
  /** 양수예정일자(계약체결일) */
  inh_prd_ctr_cnsd: z.string(),
  /** 양수예정일자(양수기준일) */
  inh_prd_inh_std: z.string(),
  /** 양수예정일자(등기예정일) */
  inh_prd_rgs_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 주주총회 특별결의 여부 */
  gmtsck_spd_atn: z.string(),
  /** 주주총회 예정일자 */
  gmtsck_prd: z.string(),
  /** 주식매수청구권에 관한 사항(행사요건) */
  aprskh_exrq: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(행사절차, 방법, 기간, 장소) */
  aprskh_ex_pc_mth_pd_pl: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 유형자산 양도 결정 항목 */
export const tangibleAssetTransferDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 자산구분 */
  ast_sen: z.string(),
  /** 자산명 */
  ast_nm: z.string(),
  /** 양도내역(양도금액(원)) */
  trfdtl_trfprc: z.string(),
  /** 양도내역(자산총액(원)) */
  trfdtl_tast: z.string(),
  /** 양도내역(자산총액대비(%)) */
  trfdtl_tast_vs: z.string(),
  /** 양도목적 */
  trf_pp: z.string(),
  /** 양도영향 */
  trf_af: z.string(),
  /** 양도예정일자(계약체결일) */
  trf_prd_ctr_cnsd: z.string(),
  /** 양도예정일자(양도기준일) */
  trf_prd_trf_std: z.string(),
  /** 양도예정일자(등기예정일) */
  trf_prd_rgs_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 주주총회 특별결의 여부 */
  gmtsck_spd_atn: z.string(),
  /** 주주총회 예정일자 */
  gmtsck_prd: z.string(),
  /** 주식매수청구권에 관한 사항(행사요건) */
  aprskh_exrq: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(행사절차, 방법, 기간, 장소) */
  aprskh_ex_pc_mth_pd_pl: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 타법인 주식 및 출자증권 양수결정 항목 */
export const retirementStockInvestmentPlanDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 발행회사(회사명) */
  iscmp_cmpnm: z.string(),
  /** 발행회사(국적) */
  iscmp_nt: z.string(),
  /** 발행회사(대표자) */
  iscmp_rp: z.string(),
  /** 발행회사(자본금(원)) */
  iscmp_cpt: z.string(),
  /** 발행회사(회사와 관계) */
  iscmp_rl_cmpn: z.string(),
  /** 발행회사(발행주식 총수(주)) */
  iscmp_tisstk: z.string(),
  /** 발행회사(주요사업) */
  iscmp_mbsn: z.string(),
  /** 최근 6월 이내 제3자 배정에 의한 신주취득 여부 */
  l6m_tpa_nstkaq_atn: z.string(),
  /** 양수내역(양수주식수(주)) */
  inhdtl_stkcnt: z.string(),
  /** 양수내역(양수금액(원)(A)) */
  inhdtl_inhprc: z.string(),
  /** 양수내역(총자산(원)(B)) */
  inhdtl_tast: z.string(),
  /** 양수내역(총자산대비(%)(A/B)) */
  inhdtl_tast_vs: z.string(),
  /** 양수내역(자기자본(원)(C)) */
  inhdtl_ecpt: z.string(),
  /** 양수내역(자기자본대비(%)(A/C)) */
  inhdtl_ecpt_vs: z.string(),
  /** 양수후 소유주식수 및 지분비율(소유주식수(주)) */
  atinh_owstkcnt: z.string(),
  /** 양수후 소유주식수 및 지분비율(지분비율(%)) */
  atinh_eqrt: z.string(),
  /** 양수목적 */
  inh_pp: z.string(),
  /** 양수예정일자 */
  inh_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 우회상장 해당 여부 */
  bdlst_atn: z.string(),
  /** 향후 6월이내 제3자배정 증자 등 계획 */
  n6m_tpai_plann: z.string(),
  /** 발행회사(타법인)의 우회상장 요건 충족여부 */
  iscmp_bdlst_sf_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 타법인 주식 및 출자증권 양도결정 항목 */
export const retirementStockInvestmentTransferDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 발행회사(회사명) */
  iscmp_cmpnm: z.string(),
  /** 발행회사(국적) */
  iscmp_nt: z.string(),
  /** 발행회사(대표자) */
  iscmp_rp: z.string(),
  /** 발행회사(자본금(원)) */
  iscmp_cpt: z.string(),
  /** 발행회사(회사와 관계) */
  iscmp_rl_cmpn: z.string(),
  /** 발행회사(발행주식 총수(주)) */
  iscmp_tisstk: z.string(),
  /** 발행회사(주요사업) */
  iscmp_mbsn: z.string(),
  /** 양도내역(양도주식수(주)) */
  trfdtl_stkcnt: z.string(),
  /** 양도내역(양도금액(원)(A)) */
  trfdtl_trfprc: z.string(),
  /** 양도내역(총자산(원)(B)) */
  trfdtl_tast: z.string(),
  /** 양도내역(총자산대비(%)(A/B)) */
  trfdtl_tast_vs: z.string(),
  /** 양도내역(자기자본(원)(C)) */
  trfdtl_ecpt: z.string(),
  /** 양도내역(자기자본대비(%)(A/C)) */
  trfdtl_ecpt_vs: z.string(),
  /** 양도후 소유주식수 및 지분비율(소유주식수(주)) */
  attrf_owstkcnt: z.string(),
  /** 양도후 소유주식수 및 지분비율(지분비율(%)) */
  attrf_eqrt: z.string(),
  /** 양도목적 */
  trf_pp: z.string(),
  /** 양도예정일자 */
  trf_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 주권 관련 사채권 양수 결정 항목 */
export const stockRelatedBondPlanDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 주권 관련 사채권의 종류 */
  stkrtbd_kndn: z.string(),
  /** 주권 관련 사채권의 종류(회차) */
  tm: z.string(),
  /** 주권 관련 사채권의 종류(종류) */
  knd: z.string(),
  /** 사채권 발행회사(회사명) */
  bdiscmp_cmpnm: z.string(),
  /** 사채권 발행회사(국적) */
  bdiscmp_nt: z.string(),
  /** 사채권 발행회사(대표자) */
  bdiscmp_rp: z.string(),
  /** 사채권 발행회사(자본금(원)) */
  bdiscmp_cpt: z.string(),
  /** 사채권 발행회사(회사와 관계) */
  bdiscmp_rl_cmpn: z.string(),
  /** 사채권 발행회사(발행주식 총수(주)) */
  bdiscmp_tisstk: z.string(),
  /** 사채권 발행회사(주요사업) */
  bdiscmp_mbsn: z.string(),
  /** 최근 6월 이내 제3자 배정에 의한 신주취득 여부 */
  l6m_tpa_nstkaq_atn: z.string(),
  /** 양수내역(사채의 권면(전자등록)총액(원)) */
  inhdtl_bd_fta: z.string(),
  /** 양수내역(양수금액(원)(A)) */
  inhdtl_inhprc: z.string(),
  /** 양수내역(총자산(원)(B)) */
  inhdtl_tast: z.string(),
  /** 양수내역(총자산대비(%)(A/B)) */
  inhdtl_tast_vs: z.string(),
  /** 양수내역(자기자본(원)(C)) */
  inhdtl_ecpt: z.string(),
  /** 양수내역(자기자본대비(%)(A/C)) */
  inhdtl_ecpt_vs: z.string(),
  /** 양수목적 */
  inh_pp: z.string(),
  /** 양수예정일자 */
  inh_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 주권 관련 사채권 양도 결정 항목 */
export const stockRelatedBondTransferDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 주권 관련 사채권의 종류 */
  stkrtbd_kndn: z.string(),
  /** 주권 관련 사채권의 종류(회차) */
  tm: z.string(),
  /** 주권 관련 사채권의 종류(종류) */
  knd: z.string(),
  /** 취득일자 */
  aqd: z.string(),
  /** 사채권 발행회사(회사명) */
  bdiscmp_cmpnm: z.string(),
  /** 사채권 발행회사(국적) */
  bdiscmp_nt: z.string(),
  /** 사채권 발행회사(대표자) */
  bdiscmp_rp: z.string(),
  /** 사채권 발행회사(자본금(원)) */
  bdiscmp_cpt: z.string(),
  /** 사채권 발행회사(회사와 관계) */
  bdiscmp_rl_cmpn: z.string(),
  /** 사채권 발행회사(발행주식 총수(주)) */
  bdiscmp_tisstk: z.string(),
  /** 사채권 발행회사(주요사업) */
  bdiscmp_mbsn: z.string(),
  /** 양도내역(사채의 권면(전자등록)총액(원)) */
  trfdtl_bd_fta: z.string(),
  /** 양도내역(양도금액(원)(A)) */
  trfdtl_trfprc: z.string(),
  /** 양도내역(총자산(원)(B)) */
  trfdtl_tast: z.string(),
  /** 양도내역(총자산대비(%)(A/B)) */
  trfdtl_tast_vs: z.string(),
  /** 양도내역(자기자본(원)(C)) */
  trfdtl_ecpt: z.string(),
  /** 양도내역(자기자본대비(%)(A/C)) */
  trfdtl_ecpt_vs: z.string(),
  /** 양도목적 */
  trf_pp: z.string(),
  /** 양도예정일자 */
  trf_prd: z.string(),
  /** 거래상대방(회사명(성명)) */
  dlptn_cmpnm: z.string(),
  /** 거래상대방(자본금(원)) */
  dlptn_cpt: z.string(),
  /** 거래상대방(주요사업) */
  dlptn_mbsn: z.string(),
  /** 거래상대방(본점소재지(주소)) */
  dlptn_hoadd: z.string(),
  /** 거래상대방(회사와의 관계) */
  dlptn_rl_cmpn: z.string(),
  /** 거래대금지급 */
  dl_pym: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사 참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사 참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 공정거래위원회 신고대상 여부 */
  ftc_stt_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
});

/** 회사합병 결정 항목 */
export const corporateLawDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 합병방법 */
  mg_mth: z.string(),
  /** 합병형태 */
  mg_stn: z.string(),
  /** 합병목적 */
  mg_pp: z.string(),
  /** 합병비율 */
  mg_rt: z.string(),
  /** 합병비율 산출근거 */
  mg_rt_bs: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string().nullish(),
  /** 합병신주의 종류와 수(주)(보통주식) */
  mgnstk_ostk_cnt: z.string(),
  /** 합병신주의 종류와 수(주)(종류주식) */
  mgnstk_cstk_cnt: z.string(),
  /** 합병상대회사(회사명) */
  mgptncmp_cmpnm: z.string(),
  /** 합병상대회사(주요사업) */
  mgptncmp_mbsn: z.string(),
  /** 합병상대회사(회사와의 관계) */
  mgptncmp_rl_cmpn: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(자산총계)) */
  rbsnfdtl_tast: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(부채총계)) */
  rbsnfdtl_tdbt: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(자본총계)) */
  rbsnfdtl_teqt: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(자본금)) */
  rbsnfdtl_cpt: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(매출액)) */
  rbsnfdtl_sl: z.string(),
  /** 합병상대회사(최근 사업연도 재무내용(원)(당기순이익)) */
  rbsnfdtl_nic: z.string(),
  /** 합병상대회사(외부감사 여부(기관명)) */
  eadtat_intn: z.string(),
  /** 합병상대회사(외부감사 여부(감사의견)) */
  eadtat_op: z.string(),
  /** 신설합병회사(회사명) */
  nmgcmp_cmpnm: z.string(),
  /** 신설합병회사(설립시 재무내용(원)(자산총계)) */
  ffdtl_tast: z.string(),
  /** 신설합병회사(설립시 재무내용(원)(부채총계)) */
  ffdtl_tdbt: z.string(),
  /** 신설합병회사(설립시 재무내용(원)(자본총계)) */
  ffdtl_teqt: z.string(),
  /** 신설합병회사(설립시 재무내용(원)(자본금)) */
  ffdtl_cpt: z.string(),
  /** 신설합병회사(설립시 재무내용(원)(현재기준)) */
  ffdtl_std: z.string(),
  /** 신설합병회사(신설사업부문 최근 사업연도 매출액(원)) */
  nmgcmp_nbsn_rsl: z.string(),
  /** 신설합병회사(주요사업) */
  nmgcmp_mbsn: z.string(),
  /** 신설합병회사(재상장신청 여부) */
  nmgcmp_rlst_atn: z.string(),
  /** 합병일정(합병계약일) */
  mgsc_mgctrd: z.string(),
  /** 합병일정(주주확정기준일) */
  mgsc_shddstd: z.string(),
  /** 합병일정(주주명부 폐쇄기간(시작일)) */
  mgsc_shclspd_bgd: z.string(),
  /** 합병일정(주주명부 폐쇄기간(종료일)) */
  mgsc_shclspd_edd: z.string(),
  /** 합병일정(합병반대의사통지 접수기간(시작일)) */
  mgsc_mgop_rcpd_bgd: z.string(),
  /** 합병일정(합병반대의사통지 접수기간(종료일)) */
  mgsc_mgop_rcpd_edd: z.string(),
  /** 합병일정(주주총회예정일자) */
  mgsc_gmtsck_prd: z.string(),
  /** 합병일정(주식매수청구권 행사기간(시작일)) */
  mgsc_aprskh_expd_bgd: z.string(),
  /** 합병일정(주식매수청구권 행사기간(종료일)) */
  mgsc_aprskh_expd_edd: z.string(),
  /** 합병일정(구주권 제출기간(시작일)) */
  mgsc_osprpd_bgd: z.string(),
  /** 합병일정(구주권 제출기간(종료일)) */
  mgsc_osprpd_edd: z.string(),
  /** 합병일정(매매거래 정지예정기간(시작일)) */
  mgsc_trspprpd_bgd: z.string(),
  /** 합병일정(매매거래 정지예정기간(종료일)) */
  mgsc_trspprpd_edd: z.string(),
  /** 합병일정(채권자이의 제출기간(시작일)) */
  mgsc_cdobprpd_bgd: z.string(),
  /** 합병일정(채권자이의 제출기간(종료일)) */
  mgsc_cdobprpd_edd: z.string(),
  /** 합병일정(합병기일) */
  mgsc_mgdt: z.string(),
  /** 합병일정(종료보고 총회일) */
  mgsc_ergmd: z.string(),
  /** 합병일정(합병등기예정일자) */
  mgsc_mgrgsprd: z.string(),
  /** 합병일정(신주권교부예정일) */
  mgsc_nstkdlprd: z.string(),
  /** 합병일정(신주의 상장예정일) */
  mgsc_nstklstprd: z.string(),
  /** 우회상장 해당 여부 */
  bdlst_atn: z.string(),
  /** 타법인의 우회상장 요건 충족여부 */
  otcpr_bdlst_sf_atn: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
});

/** 회사분할 결정 항목 */
export const corporateDivisionDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 분할방법 */
  dv_mth: z.string(),
  /** 분할의 중요영향 및 효과 */
  dv_impef: z.string(),
  /** 분할비율 */
  dv_rt: z.string(),
  /** 분할로 이전할 사업 및 재산의 내용 */
  dv_trfbsnprt_cn: z.string(),
  /** 분할 후 존속회사(회사명) */
  atdv_excmp_cmpnm: z.string(),
  /** 분할 후 존속회사(분할후 재무내용(원)(자산총계)) */
  atdvfdtl_tast: z.string(),
  /** 분할 후 존속회사(분할후 재무내용(원)(부채총계)) */
  atdvfdtl_tdbt: z.string(),
  /** 분할 후 존속회사(분할후 재무내용(원)(자본총계)) */
  atdvfdtl_teqt: z.string(),
  /** 분할 후 존속회사(분할후 재무내용(원)(자본금)) */
  atdvfdtl_cpt: z.string(),
  /** 분할 후 존속회사(분할후 재무내용(원)(현재기준)) */
  atdvfdtl_std: z.string(),
  /** 분할 후 존속회사(존속사업부문 최근 사업연도매출액(원)) */
  atdv_excmp_exbsn_rsl: z.string(),
  /** 분할 후 존속회사(주요사업) */
  atdv_excmp_mbsn: z.string(),
  /** 분할 후 존속회사(분할 후 상장유지 여부) */
  atdv_excmp_atdv_lstmn_atn: z.string(),
  /** 분할설립회사(회사명) */
  dvfcmp_cmpnm: z.string(),
  /** 분할설립회사(설립시 재무내용(원)(자산총계)) */
  ffdtl_tast: z.string(),
  /** 분할설립회사(설립시 재무내용(원)(부채총계)) */
  ffdtl_tdbt: z.string(),
  /** 분할설립회사(설립시 재무내용(원)(자본총계)) */
  ffdtl_teqt: z.string(),
  /** 분할설립회사(설립시 재무내용(원)(자본금)) */
  ffdtl_cpt: z.string(),
  /** 분할설립회사(설립시 재무내용(원)(현재기준)) */
  ffdtl_std: z.string(),
  /** 분할설립회사(신설사업부문 최근 사업연도 매출액(원)) */
  dvfcmp_nbsn_rsl: z.string(),
  /** 분할설립회사(주요사업) */
  dvfcmp_mbsn: z.string(),
  /** 분할설립회사(재상장신청 여부) */
  dvfcmp_rlst_atn: z.string(),
  /** 감자에 관한 사항(감자비율(%)) */
  abcr_crrt: z.string(),
  /** 감자에 관한 사항(구주권 제출기간(시작일)) */
  abcr_osprpd_bgd: z.string(),
  /** 감자에 관한 사항(구주권 제출기간(종료일)) */
  abcr_osprpd_edd: z.string(),
  /** 감자에 관한 사항(매매거래정지 예정기간(시작일)) */
  abcr_trspprpd_bgd: z.string(),
  /** 감자에 관한 사항(매매거래정지 예정기간(종료일)) */
  abcr_trspprpd_edd: z.string(),
  /** 감자에 관한 사항(신주배정조건) */
  abcr_nstkascnd: z.string(),
  /** 감자에 관한 사항(주주 주식수 비례여부 및 사유) */
  abcr_shstkcnt_rt_at_rs: z.string(),
  /** 감자에 관한 사항(신주배정기준일) */
  abcr_nstkasstd: z.string(),
  /** 감자에 관한 사항(신주권교부예정일) */
  abcr_nstkdlprd: z.string(),
  /** 감자에 관한 사항(신주의 상장예정일) */
  abcr_nstklstprd: z.string(),
  /** 주주총회 예정일 */
  gmtsck_prd: z.string(),
  /** 채권자 이의제출기간(시작일) */
  cdobprpd_bgd: z.string(),
  /** 채권자 이의제출기간(종료일) */
  cdobprpd_edd: z.string(),
  /** 분할기일 */
  dvdt: z.string(),
  /** 분할등기 예정일 */
  dvrgsprd: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
});

/** 회사분할합병 결정 항목 */
export const corporateLawMethodDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 분할합병 방법 */
  dvmg_mth: z.string(),
  /** 분할합병의 중요영향 및 효과 */
  dvmg_impef: z.string(),
  /** 분할에 관한 사항(분할로 이전할 사업 및 재산의 내용) */
  dv_trfbsnprt_cn: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(회사명)) */
  atdv_excmp_cmpnm: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자산총계))) */
  atdvfdtl_tast: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(부채총계))) */
  atdvfdtl_tdbt: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본총계))) */
  atdvfdtl_teqt: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(자본금))) */
  atdvfdtl_cpt: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할후 재무내용(원)(현재기준))) */
  atdvfdtl_std: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(존속사업부문 최근 사업연도매출액(원))) */
  atdv_excmp_exbsn_rsl: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(주요사업)) */
  atdv_excmp_mbsn: z.string(),
  /** 분할에 관한 사항(분할 후 존속회사(분할 후 상장유지 여부)) */
  atdv_excmp_atdv_lstmn_atn: z.string(),
  /** 분할에 관한 사항(분할설립 회사(회사명)) */
  dvfcmp_cmpnm: z.string(),
  /** 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자산총계))) */
  ffdtl_tast: z.string(),
  /** 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(부채총계))) */
  ffdtl_tdbt: z.string(),
  /** 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본총계))) */
  ffdtl_teqt: z.string(),
  /** 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(자본금))) */
  ffdtl_cpt: z.string(),
  /** 분할에 관한 사항(분할설립 회사(설립시 재무내용(원)(현재기준))) */
  ffdtl_std: z.string(),
  /** 분할에 관한 사항(분할설립 회사(신설사업부문 최근 사업연도 매출액(원))) */
  dvfcmp_nbsn_rsl: z.string(),
  /** 분할에 관한 사항(분할설립 회사(주요사업)) */
  dvfcmp_mbsn: z.string(),
  /** 분할에 관한 사항(분할설립 회사(분할후 상장유지여부)) */
  dvfcmp_atdv_lstmn_at: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(감자비율(%))) */
  abcr_crrt: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(구주권 제출기간(시작일))) */
  abcr_osprpd_bgd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(구주권 제출기간(종료일))) */
  abcr_osprpd_edd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(시작일))) */
  abcr_trspprpd_bgd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(매매거래정지 예정기간(종료일))) */
  abcr_trspprpd_edd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(신주배정조건)) */
  abcr_nstkascnd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(주주 주식수 비례여부 및 사유)) */
  abcr_shstkcnt_rt_at_rs: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(신주배정기준일)) */
  abcr_nstkasstd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(신주권교부예정일)) */
  abcr_nstkdlprd: z.string(),
  /** 분할에 관한 사항(감자에 관한 사항(신주의 상장예정일)) */
  abcr_nstklstprd: z.string(),
  /** 합병에 관한 사항(합병형태) */
  mg_stn: z.string(),
  /** 합병에 관한 사항(합병상대 회사(회사명)) */
  mgptncmp_cmpnm: z.string(),
  /** 합병에 관한 사항(합병상대 회사(주요사업)) */
  mgptncmp_mbsn: z.string(),
  /** 합병에 관한 사항(합병상대 회사(회사와의 관계)) */
  mgptncmp_rl_cmpn: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자산총계))) */
  rbsnfdtl_tast: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(부채총계))) */
  rbsnfdtl_tdbt: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본총계))) */
  rbsnfdtl_teqt: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(자본금))) */
  rbsnfdtl_cpt: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(매출액))) */
  rbsnfdtl_sl: z.string(),
  /** 합병에 관한 사항(합병상대 회사(최근 사업연도 재무내용(원)(당기순이익))) */
  rbsnfdtl_nic: z.string(),
  /** 합병에 관한 사항(합병상대 회사(외부감사 여부(기관명))) */
  eadtat_intn: z.string(),
  /** 합병에 관한 사항(합병상대 회사(외부감사 여부(감사의견))) */
  eadtat_op: z.string(),
  /** 합병에 관한 사항(분할합병신주의 종류와 수(주)(보통주식)) */
  dvmgnstk_ostk_cnt: z.string(),
  /** 합병에 관한 사항(분할합병신주의 종류와 수(주)(종류주식)) */
  dvmgnstk_cstk_cnt: z.string(),
  /** 합병에 관한 사항(합병신설 회사(회사명)) */
  nmgcmp_cmpnm: z.string(),
  /** 합병에 관한 사항(합병신설 회사(자본금(원))) */
  nmgcmp_cpt: z.string(),
  /** 합병에 관한 사항(합병신설 회사(주요사업)) */
  nmgcmp_mbsn: z.string(),
  /** 합병에 관한 사항(합병신설 회사(재상장신청 여부)) */
  nmgcmp_rlst_atn: z.string(),
  /** 분할합병비율 */
  dvmg_rt: z.string(),
  /** 분할합병비율 산출근거 */
  dvmg_rt_bs: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 분할합병일정(분할합병계약일) */
  dvmgsc_dvmgctrd: z.string(),
  /** 분할합병일정(주주확정기준일) */
  dvmgsc_shddstd: z.string(),
  /** 분할합병일정(주주명부 폐쇄기간(시작일)) */
  dvmgsc_shclspd_bgd: z.string(),
  /** 분할합병일정(주주명부 폐쇄기간(종료일)) */
  dvmgsc_shclspd_edd: z.string(),
  /** 분할합병일정(분할합병반대의사통지 접수기간(시작일)) */
  dvmgsc_dvmgop_rcpd_bgd: z.string(),
  /** 분할합병일정(분할합병반대의사통지 접수기간(종료일)) */
  dvmgsc_dvmgop_rcpd_edd: z.string(),
  /** 분할합병일정(주주총회예정일자) */
  dvmgsc_gmtsck_prd: z.string(),
  /** 분할합병일정(주식매수청구권 행사기간(시작일)) */
  dvmgsc_aprskh_expd_bgd: z.string(),
  /** 분할합병일정(주식매수청구권 행사기간(종료일)) */
  dvmgsc_aprskh_expd_edd: z.string(),
  /** 분할합병일정(채권자 이의 제출기간(시작일)) */
  dvmgsc_cdobprpd_bgd: z.string(),
  /** 분할합병일정(채권자 이의 제출기간(종료일)) */
  dvmgsc_cdobprpd_edd: z.string(),
  /** 분할합병일정(분할합병기일) */
  dvmgsc_dvmgdt: z.string(),
  /** 분할합병일정(종료보고 총회일) */
  dvmgsc_ergmd: z.string(),
  /** 분할합병일정(분할합병등기예정일) */
  dvmgsc_dvmgrgsprd: z.string(),
  /** 우회상장 해당 여부 */
  bdlst_atn: z.string(),
  /** 타법인의 우회상장 요건 충족여부 */
  otcpr_bdlst_sf_atn: z.string(),
  /** 주식매수청구권에 관한 사항(행사요건) */
  aprskh_exrq: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(행사절차, 방법, 기간, 장소) */
  aprskh_ex_pc_mth_pd_pl: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
});

/** 주식교환·이전 결정 항목 */
export const stockTradingOtherDecisionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 구분 */
  extr_sen: z.string(),
  /** 교환ㆍ이전 형태 */
  extr_stn: z.string(),
  /** 교환ㆍ이전 대상법인(회사명) */
  extr_tgcmp_cmpnm: z.string(),
  /** 교환ㆍ이전 대상법인(대표자) */
  extr_tgcmp_rp: z.string(),
  /** 교환ㆍ이전 대상법인(주요사업) */
  extr_tgcmp_mbsn: z.string(),
  /** 교환ㆍ이전 대상법인(회사와의 관계) */
  extr_tgcmp_rl_cmpn: z.string(),
  /** 교환ㆍ이전 대상법인(발행주식총수(주)(보통주식)) */
  extr_tgcmp_tisstk_ostk: z.string(),
  /** 교환ㆍ이전 대상법인(발행주식총수(주)(종류주식)) */
  extr_tgcmp_tisstk_cstk: z.string(),
  /** 교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자산총계)) */
  rbsnfdtl_tast: z.string(),
  /** 교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(부채총계)) */
  rbsnfdtl_tdbt: z.string(),
  /** 교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자본총계)) */
  rbsnfdtl_teqt: z.string(),
  /** 교환ㆍ이전 대상법인(최근 사업연도 요약재무내용(원)(자본금)) */
  rbsnfdtl_cpt: z.string(),
  /** 교환ㆍ이전 비율 */
  extr_rt: z.string(),
  /** 교환ㆍ이전 비율 산출근거 */
  extr_rt_bs: z.string(),
  /** 외부평가에 관한 사항(외부평가 여부) */
  exevl_atn: z.string(),
  /** 외부평가에 관한 사항(근거 및 사유) */
  exevl_bs_rs: z.string(),
  /** 외부평가에 관한 사항(외부평가기관의 명칭) */
  exevl_intn: z.string(),
  /** 외부평가에 관한 사항(외부평가 기간) */
  exevl_pd: z.string(),
  /** 외부평가에 관한 사항(외부평가 의견) */
  exevl_op: z.string(),
  /** 교환ㆍ이전 목적 */
  extr_pp: z.string(),
  /** 교환ㆍ이전일정(교환ㆍ이전계약일) */
  extrsc_extrctrd: z.string(),
  /** 교환ㆍ이전일정(주주확정기준일) */
  extrsc_shddstd: z.string(),
  /** 교환ㆍ이전일정(주주명부 폐쇄기간(시작일)) */
  extrsc_shclspd_bgd: z.string(),
  /** 교환ㆍ이전일정(주주명부 폐쇄기간(종료일)) */
  extrsc_shclspd_edd: z.string(),
  /** 교환ㆍ이전일정(주식교환ㆍ이전 반대의사 통지접수기간(시작일)) */
  extrsc_extrop_rcpd_bgd: z.string(),
  /** 교환ㆍ이전일정(주식교환ㆍ이전 반대의사 통지접수기간(종료일)) */
  extrsc_extrop_rcpd_edd: z.string(),
  /** 교환ㆍ이전일정(주주총회 예정일자) */
  extrsc_gmtsck_prd: z.string(),
  /** 교환ㆍ이전일정(주식매수청구권 행사기간(시작일)) */
  extrsc_aprskh_expd_bgd: z.string(),
  /** 교환           ㆍ이전일정(주식매수청구권 행사기간(종료일)) */
  extrsc_aprskh_expd_edd: z.string(),
  /** 교환ㆍ이전일정(구주권제출기간(시작일)) */
  extrsc_osprpd_bgd: z.string(),
  /** 교환ㆍ이전일정(구주권제출기간(종료일)) */
  extrsc_osprpd_edd: z.string(),
  /** 교환ㆍ이전일정(매매거래정지예정기간(시작일)) */
  extrsc_trspprpd_bgd: z.string(),
  /** 교환ㆍ이전일정(매매거래정지예정기간(종료일)) */
  extrsc_trspprpd_edd: z.string(),
  /** 교환ㆍ이전일정(교환ㆍ이전일자) */
  extrsc_extrdt: z.string(),
  /** 교환ㆍ이전일정(신주권교부예정일) */
  extrsc_nstkdlprd: z.string(),
  /** 교환ㆍ이전일정(신주의 상장예정일) */
  extrsc_nstklstprd: z.string(),
  /** 교환ㆍ이전 후 완전모회사명 */
  atextr_cpcmpnm: z.string(),
  /** 주식매수청구권에 관한 사항(매수예정가격) */
  aprskh_plnprc: z.string(),
  /** 주식매수청구권에 관한 사항(지급예정시기, 지급방법) */
  aprskh_pym_plpd_mth: z.string(),
  /** 주식매수청구권에 관한 사항(주식매수청구권 제한 관련 내용) */
  aprskh_lmt: z.string(),
  /** 주식매수청구권에 관한 사항(계약에 미치는 효력) */
  aprskh_ctref: z.string(),
  /** 우회상장 해당 여부 */
  bdlst_atn: z.string(),
  /** 타법인의 우회상장 요건 충족 여부 */
  otcpr_bdlst_sf_atn: z.string(),
  /** 이사회결의일(결정일) */
  bddd: z.string(),
  /** 사외이사참석여부(참석(명)) */
  od_a_at_t: z.string(),
  /** 사외이사참석여부(불참(명)) */
  od_a_at_b: z.string(),
  /** 감사(사외이사가 아닌 감사위원) 참석여부 */
  adt_a_atn: z.string(),
  /** 풋옵션 등 계약 체결여부 */
  popt_ctr_atn: z.string(),
  /** 계약내용 */
  popt_ctr_cn: z.string(),
  /** 증권신고서 제출대상 여부 */
  rs_sm_atn: z.string(),
  /** 제출을 면제받은 경우 그 사유 */
  ex_sm_r: z.string(),
});

/** 자산양수도(기타), 풋백옵션 응답 */
export const treasuryStockAcquisitionDisposalPlanResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockAcquisitionDisposalPlanItemSchema).nullish(),
});

/** 부도발생 응답 */
export const realEstateDevelopmentResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(realEstateDevelopmentItemSchema).nullish(),
});

/** 영업정지 응답 */
export const businessLetterResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(businessLetterItemSchema).nullish(),
});

/** 회생절차 개시신청 응답 */
export const corporateRehabilitationProceedingsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(corporateRehabilitationProceedingsItemSchema).nullish(),
});

/** 해산사유 발생 응답 */
export const dissolutionOccurrenceResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(dissolutionOccurrenceItemSchema).nullish(),
});

/** 유상증자 결정 응답 */
export const securitiesGrantedDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(securitiesGrantedDecisionItemSchema).nullish(),
});

/** 무상증자 결정 응답 */
export const freeSecuritiesDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(freeSecuritiesDecisionItemSchema).nullish(),
});

/** 유무상증자 결정 응답 */
export const paidInCapitalReductionDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(paidInCapitalReductionDecisionItemSchema).nullish(),
});

/** 감자 결정 응답 */
export const capitalReductionDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(capitalReductionDecisionItemSchema).nullish(),
});

/** 재권은행 등의 관리절차 개시 응답 */
export const governmentBondManagerReplacementResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(governmentBondManagerReplacementItemSchema).nullish(),
});

/** 소송 등의 제기 응답 */
export const profitRevocationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(profitRevocationItemSchema).nullish(),
});

/** 해외 증권시장 주권등 상장 결정 응답 */
export const overseasSecuritiesTradingResolutionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(overseasSecuritiesTradingResolutionItemSchema).nullish(),
});

/** 해외 증권시장 주권등 상장폐지 결정 응답 */
export const overseasSecuritiesTradingDelistingResolutionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(overseasSecuritiesTradingDelistingResolutionItemSchema).nullish(),
});

/** 해외 증권시장 주권등 상장 응답 */
export const overseasSecuritiesTradingStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(overseasSecuritiesTradingStatusItemSchema).nullish(),
});

/** 해외 증권시장 주권등 상장폐지 응답 */
export const overseasSecuritiesTradingStatusDelistingResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(overseasSecuritiesTradingStatusDelistingItemSchema).nullish(),
});

/** 전환사채권 발행결정 응답 */
export const convertibleBondIssuanceDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(convertibleBondIssuanceDecisionItemSchema).nullish(),
});

/** 신주인수권부사채권 발행결정 응답 */
export const newStockWarrantBondIssuanceDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(newStockWarrantBondIssuanceDecisionItemSchema).nullish(),
});

/** 교환사채권 발행결정 응답 */
export const corporateBondIssuanceDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(corporateBondIssuanceDecisionItemSchema).nullish(),
});

/** 채권은행 등의 관리절차 종단 응답 */
export const governmentBondManagerTransferTerminationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(governmentBondManagerTransferTerminationItemSchema).nullish(),
});

/** 상각형 조건부자본증권 발행결정 응답 */
export const reorganizationPlanApprovedRulingResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(reorganizationPlanApprovedRulingItemSchema).nullish(),
});

/** 자기주식 취득 결정 응답 */
export const treasuryStockAcquisitionDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockAcquisitionDecisionItemSchema).nullish(),
});

/** 자기주식 처분 결정 응답 */
export const treasuryStockDisposalDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockDisposalDecisionItemSchema).nullish(),
});

/** 자기주식취득 신탁계약 체결 결정 응답 */
export const treasuryStockTrustContractDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockTrustContractDecisionItemSchema).nullish(),
});

/** 자기주식취득 신탁계약 해지 결정 응답 */
export const treasuryStockTrustContractTerminationDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockTrustContractTerminationDecisionItemSchema).nullish(),
});

/** 영업양수 결정 응답 */
export const businessPlanDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(businessPlanDecisionItemSchema).nullish(),
});

/** 영업양도 결정 응답 */
export const businessTransferDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(businessTransferDecisionItemSchema).nullish(),
});

/** 유형자산 양수 결정 응답 */
export const tangibleAssetPlanDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(tangibleAssetPlanDecisionItemSchema).nullish(),
});

/** 유형자산 양도 결정 응답 */
export const tangibleAssetTransferDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(tangibleAssetTransferDecisionItemSchema).nullish(),
});

/** 타법인 주식 및 출자증권 양수결정 응답 */
export const retirementStockInvestmentPlanDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(retirementStockInvestmentPlanDecisionItemSchema).nullish(),
});

/** 타법인 주식 및 출자증권 양도결정 응답 */
export const retirementStockInvestmentTransferDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(retirementStockInvestmentTransferDecisionItemSchema).nullish(),
});

/** 주권 관련 사채권 양수 결정 응답 */
export const stockRelatedBondPlanDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(stockRelatedBondPlanDecisionItemSchema).nullish(),
});

/** 주권 관련 사채권 양도 결정 응답 */
export const stockRelatedBondTransferDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(stockRelatedBondTransferDecisionItemSchema).nullish(),
});

/** 회사합병 결정 응답 */
export const corporateLawDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(corporateLawDecisionItemSchema).nullish(),
});

/** 회사분할 결정 응답 */
export const corporateDivisionDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(corporateDivisionDecisionItemSchema).nullish(),
});

/** 회사분할합병 결정 응답 */
export const corporateLawMethodDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(corporateLawMethodDecisionItemSchema).nullish(),
});

/** 주식교환·이전 결정 응답 */
export const stockTradingOtherDecisionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(stockTradingOtherDecisionItemSchema).nullish(),
});

// ── Response Types ──

export type TreasuryStockAcquisitionDisposalPlanResponse = CamelizeKeys<
  z.infer<typeof treasuryStockAcquisitionDisposalPlanResponseSchema>
>;
export type RealEstateDevelopmentResponse = CamelizeKeys<z.infer<typeof realEstateDevelopmentResponseSchema>>;
export type BusinessLetterResponse = CamelizeKeys<z.infer<typeof businessLetterResponseSchema>>;
export type CorporateRehabilitationProceedingsResponse = CamelizeKeys<
  z.infer<typeof corporateRehabilitationProceedingsResponseSchema>
>;
export type DissolutionOccurrenceResponse = CamelizeKeys<z.infer<typeof dissolutionOccurrenceResponseSchema>>;
export type SecuritiesGrantedDecisionResponse = CamelizeKeys<z.infer<typeof securitiesGrantedDecisionResponseSchema>>;
export type FreeSecuritiesDecisionResponse = CamelizeKeys<z.infer<typeof freeSecuritiesDecisionResponseSchema>>;
export type PaidInCapitalReductionDecisionResponse = CamelizeKeys<
  z.infer<typeof paidInCapitalReductionDecisionResponseSchema>
>;
export type CapitalReductionDecisionResponse = CamelizeKeys<z.infer<typeof capitalReductionDecisionResponseSchema>>;
export type GovernmentBondManagerReplacementResponse = CamelizeKeys<
  z.infer<typeof governmentBondManagerReplacementResponseSchema>
>;
export type ProfitRevocationResponse = CamelizeKeys<z.infer<typeof profitRevocationResponseSchema>>;
export type OverseasSecuritiesTradingResolutionResponse = CamelizeKeys<
  z.infer<typeof overseasSecuritiesTradingResolutionResponseSchema>
>;
export type OverseasSecuritiesTradingDelistingResolutionResponse = CamelizeKeys<
  z.infer<typeof overseasSecuritiesTradingDelistingResolutionResponseSchema>
>;
export type OverseasSecuritiesTradingStatusResponse = CamelizeKeys<
  z.infer<typeof overseasSecuritiesTradingStatusResponseSchema>
>;
export type OverseasSecuritiesTradingStatusDelistingResponse = CamelizeKeys<
  z.infer<typeof overseasSecuritiesTradingStatusDelistingResponseSchema>
>;
export type ConvertibleBondIssuanceDecisionResponse = CamelizeKeys<
  z.infer<typeof convertibleBondIssuanceDecisionResponseSchema>
>;
export type NewStockWarrantBondIssuanceDecisionResponse = CamelizeKeys<
  z.infer<typeof newStockWarrantBondIssuanceDecisionResponseSchema>
>;
export type CorporateBondIssuanceDecisionResponse = CamelizeKeys<
  z.infer<typeof corporateBondIssuanceDecisionResponseSchema>
>;
export type GovernmentBondManagerTransferTerminationResponse = CamelizeKeys<
  z.infer<typeof governmentBondManagerTransferTerminationResponseSchema>
>;
export type ReorganizationPlanApprovedRulingResponse = CamelizeKeys<
  z.infer<typeof reorganizationPlanApprovedRulingResponseSchema>
>;
export type TreasuryStockAcquisitionDecisionResponse = CamelizeKeys<
  z.infer<typeof treasuryStockAcquisitionDecisionResponseSchema>
>;
export type TreasuryStockDisposalDecisionResponse = CamelizeKeys<
  z.infer<typeof treasuryStockDisposalDecisionResponseSchema>
>;
export type TreasuryStockTrustContractDecisionResponse = CamelizeKeys<
  z.infer<typeof treasuryStockTrustContractDecisionResponseSchema>
>;
export type TreasuryStockTrustContractTerminationDecisionResponse = CamelizeKeys<
  z.infer<typeof treasuryStockTrustContractTerminationDecisionResponseSchema>
>;
export type BusinessPlanDecisionResponse = CamelizeKeys<z.infer<typeof businessPlanDecisionResponseSchema>>;
export type BusinessTransferDecisionResponse = CamelizeKeys<z.infer<typeof businessTransferDecisionResponseSchema>>;
export type TangibleAssetPlanDecisionResponse = CamelizeKeys<z.infer<typeof tangibleAssetPlanDecisionResponseSchema>>;
export type TangibleAssetTransferDecisionResponse = CamelizeKeys<
  z.infer<typeof tangibleAssetTransferDecisionResponseSchema>
>;
export type RetirementStockInvestmentPlanDecisionResponse = CamelizeKeys<
  z.infer<typeof retirementStockInvestmentPlanDecisionResponseSchema>
>;
export type RetirementStockInvestmentTransferDecisionResponse = CamelizeKeys<
  z.infer<typeof retirementStockInvestmentTransferDecisionResponseSchema>
>;
export type StockRelatedBondPlanDecisionResponse = CamelizeKeys<
  z.infer<typeof stockRelatedBondPlanDecisionResponseSchema>
>;
export type StockRelatedBondTransferDecisionResponse = CamelizeKeys<
  z.infer<typeof stockRelatedBondTransferDecisionResponseSchema>
>;
export type CorporateLawDecisionResponse = CamelizeKeys<z.infer<typeof corporateLawDecisionResponseSchema>>;
export type CorporateDivisionDecisionResponse = CamelizeKeys<z.infer<typeof corporateDivisionDecisionResponseSchema>>;
export type CorporateLawMethodDecisionResponse = CamelizeKeys<z.infer<typeof corporateLawMethodDecisionResponseSchema>>;
export type StockTradingOtherDecisionResponse = CamelizeKeys<z.infer<typeof stockTradingOtherDecisionResponseSchema>>;

// ── Response Map ──

export interface MajorShareholderDisclosureResponseMap {
  treasuryStockAcquisitionDisposalPlan: TreasuryStockAcquisitionDisposalPlanResponse;
  realEstateDevelopment: RealEstateDevelopmentResponse;
  businessLetter: BusinessLetterResponse;
  corporateRehabilitationProceedings: CorporateRehabilitationProceedingsResponse;
  dissolutionOccurrence: DissolutionOccurrenceResponse;
  securitiesGrantedDecision: SecuritiesGrantedDecisionResponse;
  freeSecuritiesDecision: FreeSecuritiesDecisionResponse;
  paidInCapitalReductionDecision: PaidInCapitalReductionDecisionResponse;
  capitalReductionDecision: CapitalReductionDecisionResponse;
  governmentBondManagerReplacement: GovernmentBondManagerReplacementResponse;
  profitRevocation: ProfitRevocationResponse;
  overseasSecuritiesTradingResolution: OverseasSecuritiesTradingResolutionResponse;
  overseasSecuritiesTradingDelistingResolution: OverseasSecuritiesTradingDelistingResolutionResponse;
  overseasSecuritiesTradingStatus: OverseasSecuritiesTradingStatusResponse;
  overseasSecuritiesTradingStatusDelisting: OverseasSecuritiesTradingStatusDelistingResponse;
  convertibleBondIssuanceDecision: ConvertibleBondIssuanceDecisionResponse;
  newStockWarrantBondIssuanceDecision: NewStockWarrantBondIssuanceDecisionResponse;
  corporateBondIssuanceDecision: CorporateBondIssuanceDecisionResponse;
  governmentBondManagerTransferTermination: GovernmentBondManagerTransferTerminationResponse;
  reorganizationPlanApprovedRuling: ReorganizationPlanApprovedRulingResponse;
  treasuryStockAcquisitionDecision: TreasuryStockAcquisitionDecisionResponse;
  treasuryStockDisposalDecision: TreasuryStockDisposalDecisionResponse;
  treasuryStockTrustContractDecision: TreasuryStockTrustContractDecisionResponse;
  treasuryStockTrustContractTerminationDecision: TreasuryStockTrustContractTerminationDecisionResponse;
  businessPlanDecision: BusinessPlanDecisionResponse;
  businessTransferDecision: BusinessTransferDecisionResponse;
  tangibleAssetPlanDecision: TangibleAssetPlanDecisionResponse;
  tangibleAssetTransferDecision: TangibleAssetTransferDecisionResponse;
  retirementStockInvestmentPlanDecision: RetirementStockInvestmentPlanDecisionResponse;
  retirementStockInvestmentTransferDecision: RetirementStockInvestmentTransferDecisionResponse;
  stockRelatedBondPlanDecision: StockRelatedBondPlanDecisionResponse;
  stockRelatedBondTransferDecision: StockRelatedBondTransferDecisionResponse;
  corporateLawDecision: CorporateLawDecisionResponse;
  corporateDivisionDecision: CorporateDivisionDecisionResponse;
  corporateLawMethodDecision: CorporateLawMethodDecisionResponse;
  stockTradingOtherDecision: StockTradingOtherDecisionResponse;
}
