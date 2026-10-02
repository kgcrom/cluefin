import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';
import { dartEnvelope } from './common.js';

/** 증자(감자) 현황 항목 */
export const capitalChangeStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 주식발행 감소일자 */
  isu_dcrs_de: z.string(),
  /** 발행 감소 형태 */
  isu_dcrs_stle: z.string(),
  /** 발행 감소 주식 종류 */
  isu_dcrs_stock_knd: z.string(),
  /** 발행 감소 수량 */
  isu_dcrs_qy: z.string(),
  /** 발행 감소 주당 액면 가액 */
  isu_dcrs_mstvdv_fval_amount: z.string(),
  /** 발행 감소 주당 가액 */
  isu_dcrs_mstvdv_amount: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 배당 관련 사항 항목 */
export const dividendInformationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 구분 */
  se: z.string(),
  /** 주식 종류 */
  stock_knd: z.string().nullish(),
  /** 당기 */
  thstrm: z.string(),
  /** 전기 */
  frmtrm: z.string(),
  /** 전전기 */
  lwfr: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 자기주식 취득 및 처분 현황 항목 */
export const treasuryStockActivityItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 취득방법 대분류 */
  acqs_mth1: z.string(),
  /** 취득방법 중분류 */
  acqs_mth2: z.string(),
  /** 취득방법 소분류 */
  acqs_mth3: z.string(),
  /** 주식 종류 */
  stock_knd: z.string(),
  /** 기초 수량 */
  bsis_qy: z.string(),
  /** 변동 수량 취득 */
  change_qy_acqs: z.string(),
  /** 변동 수량 처분 */
  change_qy_dsps: z.string(),
  /** 변동 수량 소각 */
  change_qy_incnr: z.string(),
  /** 기말 수량 */
  trmend_qy: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 최대주주 현황 항목 */
export const majorShareholderStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 성명 */
  nm: z.string(),
  /** 관계 */
  relate: z.string().nullish(),
  /** 주식 종류 */
  stock_knd: z.string(),
  /** 기초 소유 주식 수 */
  bsis_posesn_stock_co: z.string(),
  /** 기초 소유 주식 지분 율 */
  bsis_posesn_stock_qota_rt: z.string(),
  /** 기말 소유 주식 수 */
  trmend_posesn_stock_co: z.string(),
  /** 기말 소유 주식 지분 율 */
  trmend_posesn_stock_qota_rt: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 최대주주 변동현황 항목 */
export const majorShareholderChangesItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 변동 일 */
  change_on: z.string(),
  /** 최대 주주 명 */
  mxmm_shrholdr_nm: z.string(),
  /** 소유 주식 수 */
  posesn_stock_co: z.string(),
  /** 지분 율 */
  qota_rt: z.string(),
  /** 변동 원인 */
  change_cause: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 소액주주 현황 항목 */
export const minorityShareholderStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 구분 */
  se: z.string(),
  /** 주주수 */
  shrholdr_co: z.string(),
  /** 전체 주주수 */
  shrholdr_tot_co: z.string(),
  /** 주주 비율 */
  shrholdr_rate: z.string(),
  /** 보유 주식수 */
  hold_stock_co: z.string(),
  /** 총발행 주식수 */
  stock_tot_co: z.string(),
  /** 보유 주식 비율 */
  hold_stock_rate: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 임원 현황 항목 */
export const executiveStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 성명 */
  nm: z.string(),
  /** 성별 */
  sexdstn: z.string(),
  /** 출생 년월 */
  birth_ym: z.string(),
  /** 직위 */
  ofcps: z.string(),
  /** 등기 임원 여부 */
  rgist_exctv_at: z.string(),
  /** 상근 여부 */
  fte_at: z.string(),
  /** 담당 업무 */
  chrg_job: z.string(),
  /** 주요 경력 */
  main_career: z.string(),
  /** 최대 주주 관계 */
  mxmm_shrholdr_relate: z.string(),
  /** 재직 기간 */
  hffc_pd: z.string(),
  /** 임기 만료 일 */
  tenure_end_on: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 직원 현황 항목 */
export const employeeStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 사업부문 */
  fo_bbm: z.string(),
  /** 성별 */
  sexdstn: z.string(),
  /** 개정 전 직원 수 정규직 */
  reform_bfe_emp_co_rgllbr: z.string(),
  /** 개정 전 직원 수 계약직 */
  reform_bfe_emp_co_cnttk: z.string(),
  /** 개정 전 직원 수 기타 */
  reform_bfe_emp_co_etc: z.string(),
  /** 정규직 수 */
  rgllbr_co: z.string(),
  /** 정규직 단시간 근로자 수 */
  rgllbr_abacpt_labrr_co: z.string(),
  /** 계약직 수 */
  cnttk_co: z.string(),
  /** 계약직 단시간 근로자 수 */
  cnttk_abacpt_labrr_co: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 평균 근속 연수 */
  avrg_cnwk_sdytrn: z.string(),
  /** 연간 급여 총액 */
  fyer_salary_totamt: z.string(),
  /** 1인평균 급여 액 */
  jan_salary_am: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 이사·감사 개별 보수현황(5억 이상) 항목 */
export const boardAndAuditCompensationAbove500mItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 이름 */
  nm: z.string(),
  /** 직위 */
  ofcps: z.string(),
  /** 보수 총액 */
  mendng_totamt: z.string(),
  /** 보수 총액 비 포함 보수 */
  mendng_totamt_ct_incls_mendng: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 이사·감사 전체 보수지급금액 항목 */
export const boardAndAuditTotalCompensationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 인원수 */
  nmpr: z.string(),
  /** 보수 총액 */
  mendng_totamt: z.string(),
  /** 1인 평균 보수 액 */
  jan_avrg_mendng_am: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 개인별 보수지급 금액(5억 이상 상위 5인) 항목 */
export const topFiveIndividualCompensationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 법인명 */
  corp_name: z.string(),
  /** 이름 */
  nm: z.string(),
  /** 직위 */
  ofcps: z.string(),
  /** 보수 총액 */
  mendng_totamt: z.string(),
  /** 보수 총액 비 포함 보수 */
  mendng_totamt_ct_incls_mendng: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 타법인 출자현황 항목 */
export const otherCorporationInvestmentsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 법인명 */
  inv_prm: z.string(),
  /** 최초 취득 일자 */
  frst_acqs_de: z.string(),
  /** 출자 목적 */
  invstmnt_purps: z.string(),
  /** 최초 취득 금액 */
  frst_acqs_amount: z.string(),
  /** 기초 잔액 수량 */
  bsis_blce_qy: z.string(),
  /** 기초 잔액 지분 율 */
  bsis_blce_qota_rt: z.string(),
  /** 기초 잔액 장부 가액 */
  bsis_blce_acntbk_amount: z.string(),
  /** 증가 감소 취득 처분 수량 */
  incrs_dcrs_acqs_dsps_qy: z.string(),
  /** 증가 감소 취득 처분 금액 */
  incrs_dcrs_acqs_dsps_amount: z.string(),
  /** 증가 감소 평가 손액 */
  incrs_dcrs_evl_lstmn: z.string(),
  /** 기말 잔액 수량 */
  trmend_blce_qy: z.string(),
  /** 기말 잔액 지분 율 */
  trmend_blce_qota_rt: z.string(),
  /** 기말 잔액 장부 가액 */
  trmend_blce_acntbk_amount: z.string(),
  /** 최근 사업 연도 재무 현황 총 자산 */
  recent_bsns_year_fnnr_sttus_tot_assets: z.string(),
  /** 최근 사업 연도 재무 현황 당기 순이익 */
  recent_bsns_year_fnnr_sttus_thstrm_ntpf: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 주식의 총수 현황 항목 */
export const totalNumberOfSharesItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분 */
  se: z.string(),
  /** 발행할 주식의 총수 */
  isu_stock_totqy: z.string(),
  /** 현재까지 발행한 주식의 총수 */
  now_to_isu_stock_totqy: z.string(),
  /** 현재까지 감소한 주식의 총수 */
  now_to_dcrs_stock_totqy: z.string(),
  /** 감자 */
  redc: z.string(),
  /** 이익소각 */
  profit_incnr: z.string(),
  /** 상환주식의 상환 */
  rdmstk_repy: z.string(),
  /** 기타 */
  etc: z.string(),
  /** 발행주식의 총수 */
  istc_totqy: z.string(),
  /** 자기주식수 */
  tesstk_co: z.string(),
  /** 유통주식수 */
  distb_stock_co: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 채무증권 발행실적 항목 */
export const debtSecuritiesIssuancePerformanceItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 발행회사 */
  isu_cmpny: z.string(),
  /** 증권종류 */
  scrits_knd_nm: z.string(),
  /** 발행방법 */
  isu_mth_nm: z.string(),
  /** 발행일자(YYYYMMDD) */
  isu_de: z.string(),
  /** 권면(전자등록)총액 */
  facvalu_totamt: z.string(),
  /** 이자율 */
  intrt: z.string(),
  /** 평가등급(평가기관) */
  evl_grad_instt: z.string(),
  /** 만기일(YYYYMMDD) */
  mtd: z.string(),
  /** 상환여부 */
  repy_at: z.string(),
  /** 주관회사 */
  mngt_cmpny: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 기업어음증권 미상환 잔액 항목 */
export const outstandingCommercialPaperBalanceItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 잔여만기 */
  remndr_exprtn1: z.string(),
  /** 잔여만기 */
  remndr_exprtn2: z.string(),
  /** 10일 이하 */
  de10_below: z.string(),
  /** 10일초과 30일이하 */
  de10_excess_de30_below: z.string(),
  /** 30일초과 90일이하 */
  de30_excess_de90_below: z.string(),
  /** 90일초과 180일이하 */
  de90_excess_de180_below: z.string(),
  /** 180일초과 1년이하 */
  de180_excess_yy1_below: z.string(),
  /** 1년초과 2년이하 */
  yy1_excess_yy2_below: z.string(),
  /** 2년초과 3년이하 */
  yy2_excess_yy3_below: z.string(),
  /** 3년 초과 */
  yy3_excess: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 단기사채 미상환 잔액 항목 */
export const outstandingShortTermBondsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 잔여만기 */
  remndr_exprtn1: z.string(),
  /** 잔여만기 */
  remndr_exprtn2: z.string(),
  /** 10일 이하 */
  de10_below: z.string(),
  /** 10일초과 30일이하 */
  de10_excess_de30_below: z.string(),
  /** 30일초과 90일이하 */
  de30_excess_de90_below: z.string(),
  /** 90일초과 180일이하 */
  de90_excess_de180_below: z.string(),
  /** 180일초과 1년이하 */
  de180_excess_yy1_below: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 발행 한도 */
  isu_lmt: z.string(),
  /** 잔여 한도 */
  remndr_lmt: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 회사채 미상환 잔액 항목 */
export const outstandingCorporateBondsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 잔여만기 */
  remndr_exprtn1: z.string(),
  /** 잔여만기 */
  remndr_exprtn2: z.string(),
  /** 1년 이하 */
  yy1_below: z.string(),
  /** 1년초과 2년이하 */
  yy1_excess_yy2_below: z.string(),
  /** 2년초과 3년이하 */
  yy2_excess_yy3_below: z.string(),
  /** 3년초과 4년이하 */
  yy3_excess_yy4_below: z.string(),
  /** 4년초과 5년이하 */
  yy4_excess_yy5_below: z.string(),
  /** 5년초과 10년이하 */
  yy5_excess_yy10_below: z.string(),
  /** 10년초과 */
  yy10_excess: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 신종자본증권 미상환 잔액 항목 */
export const outstandingHybridCapitalSecuritiesItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 잔여만기 */
  remndr_exprtn1: z.string(),
  /** 잔여만기 */
  remndr_exprtn2: z.string(),
  /** 1년 이하 */
  yy1_below: z.string(),
  /** 1년초과 5년이하 */
  yy1_excess_yy5_below: z.string(),
  /** 5년초과 10년이하 */
  yy5_excess_yy10_below: z.string(),
  /** 10년초과 15년이하 */
  yy10_excess_yy15_below: z.string(),
  /** 15년초과 20년이하 */
  yy15_excess_yy20_below: z.string(),
  /** 20년초과 30년이하 */
  yy20_excess_yy30_below: z.string(),
  /** 30년초과 */
  yy30_excess: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 조건부 자본증권 미상환 잔액 항목 */
export const outstandingContingentCapitalSecuritiesItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 잔여만기 */
  remndr_exprtn1: z.string(),
  /** 잔여만기 */
  remndr_exprtn2: z.string(),
  /** 1년 이하 */
  yy1_below: z.string(),
  /** 1년초과 2년이하 */
  yy1_excess_yy2_below: z.string(),
  /** 2년초과 3년이하 */
  yy2_excess_yy3_below: z.string(),
  /** 3년초과 4년이하 */
  yy3_excess_yy4_below: z.string(),
  /** 4년초과 5년이하 */
  yy4_excess_yy5_below: z.string(),
  /** 5년초과 10년이하 */
  yy5_excess_yy10_below: z.string(),
  /** 10년초과 20년이하 */
  yy10_excess_yy20_below: z.string(),
  /** 20년초과 30년이하 */
  yy20_excess_yy30_below: z.string(),
  /** 30년초과 */
  yy30_excess: z.string(),
  /** 합계 */
  sm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 회계감사인 명칭과 감사의견 항목 */
export const auditorNameAndOpinionItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사업연도 */
  bsns_year: z.string(),
  /** 감사인 */
  adtor: z.string(),
  /** 감사의견 */
  adt_opinion: z.string(),
  /** 감사보고서 특기사항 */
  adt_reprt_spcmnt_matter: z.string(),
  /** 강조사항 등 */
  emphs_matter: z.string(),
  /** 핵심감사사항 */
  core_adt_matter: z.string().nullish(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 감사용역 계약현황 항목 */
export const auditServiceContractsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 사업연도 */
  bsns_year: z.string(),
  /** 감사인 */
  adtor: z.string(),
  /** 내용 */
  cn: z.string(),
  /** 보수 */
  mendng: z.string(),
  /** 총소요시간 */
  tot_reqre_time: z.string(),
  /** 감사계약내역(보수) */
  adt_cntrct_dtls_mendng: z.string(),
  /** 감사계약내역(시간) */
  adt_cntrct_dtls_time: z.string(),
  /** 실제수행내역(보수) */
  real_exc_dtls_mendng: z.string(),
  /** 실제수행내역(시간) */
  real_exc_dtls_time: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 회계감사인과의 비감사용역 계약체결 현황 항목 */
export const nonAuditServiceContractsItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사명 */
  corp_name: z.string(),
  /** 사업연도 */
  bsns_year: z.string(),
  /** 계약체결일 */
  cntrct_cncls_de: z.string(),
  /** 용역내용 */
  servc_cn: z.string(),
  /** 용역수행기간 */
  servc_exc_pd: z.string(),
  /** 용역보수 */
  servc_mendng: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 사외이사 및 변동현황 항목 */
export const outsideDirectorStatusItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 이사의 수 */
  drctr_co: z.string(),
  /** 사외이사 수 */
  otcmp_drctr_co: z.string(),
  /** 사외이사 변동현황(선임) */
  apnt: z.string(),
  /** 사외이사 변동현황(해임) */
  rlsofc: z.string(),
  /** 사외이사 변동현황(중도퇴임) */
  mdstrm_resig: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 미등기임원 보수현황 항목 */
export const unregisteredExecutiveCompensationItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분(미등기임원) */
  se: z.string(),
  /** 9,999,999,999 */
  nmpr: z.string(),
  /** 연간급여 총액 */
  fyer_salary_totamt: z.string(),
  /** 1인평균 급여액 */
  jan_salary_am: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 이사·감사 전체 보수현황(주주총회 승인금액) 항목 */
export const boardAndAuditCompensationShareholderApprovedItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분 */
  se: z.string(),
  /** 인원수 */
  nmpr: z.string(),
  /** 주주총회 승인금액 */
  gmtsck_confm_amount: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 이사·감사 전체 보수현황(보수지급금액 유형별) 항목 */
export const boardAndAuditCompensationByTypeItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분 */
  se: z.string(),
  /** 인원수 */
  nmpr: z.string(),
  /** 보수총액 */
  pymnt_totamt: z.string(),
  /** 1인 평균 보수액 */
  psn1_avrg_pymntamt: z.string(),
  /** 비고 */
  rm: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 공모자금 사용내역 항목 */
export const publicOfferingFundUsageItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분 */
  se_nm: z.string(),
  /** 회차 */
  tm: z.string(),
  /** 납입일 */
  pay_de: z.string(),
  /** 납입금액 */
  pay_amount: z.string(),
  /** 신고서상 자금사용 계획 */
  on_dclrt_cptal_use_plan: z.string(),
  /** 실제 자금사용 현황 */
  real_cptal_use_sttus: z.string(),
  /** 증권신고서 등의 자금사용 계획(사용용도) */
  rs_cptal_use_plan_useprps: z.string(),
  /** 증권신고서 등의 자금사용 계획(조달금액) */
  rs_cptal_use_plan_prcure_amount: z.string(),
  /** 실제 자금사용 내역(내용) */
  real_cptal_use_dtls_cn: z.string(),
  /** 실제 자금사용 내역(금액) */
  real_cptal_use_dtls_amount: z.string(),
  /** 차이발생 사유 등 */
  dffrnc_occrrnc_resn: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 사모자금 사용내역 항목 */
export const privatePlacementFundUsageItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 법인구분 */
  corp_cls: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 구분 */
  se_nm: z.string(),
  /** 회차 */
  tm: z.string(),
  /** 납입일 */
  pay_de: z.string(),
  /** 납입금액 */
  pay_amount: z.string(),
  /** 자금사용 계획 */
  cptal_use_plan: z.string(),
  /** 실제 자금사용 현황 */
  real_cptal_use_sttus: z.string(),
  /** 주요사항보고서의 자금사용 계획(사용용도) */
  mtrpt_cptal_use_plan_useprps: z.string(),
  /** 주요사항보고서의 자금사용 계획(조달금액) */
  mtrpt_cptal_use_plan_prcure_amount: z.string(),
  /** 실제 자금사용 내역(내용) */
  real_cptal_use_dtls_cn: z.string(),
  /** 실제 자금사용 내역(금액) */
  real_cptal_use_dtls_amount: z.string(),
  /** 차이발생 사유 등 */
  dffrnc_occrrnc_resn: z.string(),
  /** 결산기준일 */
  stlm_dt: z.string(),
});

/** 증자(감자) 현황 응답 */
export const capitalChangeStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(capitalChangeStatusItemSchema).nullish(),
});

/** 배당 관련 사항 응답 */
export const dividendInformationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(dividendInformationItemSchema).nullish(),
});

/** 자기주식 취득 및 처분 현황 응답 */
export const treasuryStockActivityResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(treasuryStockActivityItemSchema).nullish(),
});

/** 최대주주 현황 응답 */
export const majorShareholderStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(majorShareholderStatusItemSchema).nullish(),
});

/** 최대주주 변동현황 응답 */
export const majorShareholderChangesResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(majorShareholderChangesItemSchema).nullish(),
});

/** 소액주주 현황 응답 */
export const minorityShareholderStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(minorityShareholderStatusItemSchema).nullish(),
});

/** 임원 현황 응답 */
export const executiveStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(executiveStatusItemSchema).nullish(),
});

/** 직원 현황 응답 */
export const employeeStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(employeeStatusItemSchema).nullish(),
});

/** 이사·감사 개별 보수현황(5억 이상) 응답 */
export const boardAndAuditCompensationAbove500mResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(boardAndAuditCompensationAbove500mItemSchema).nullish(),
});

/** 이사·감사 전체 보수지급금액 응답 */
export const boardAndAuditTotalCompensationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(boardAndAuditTotalCompensationItemSchema).nullish(),
});

/** 개인별 보수지급 금액(5억 이상 상위 5인) 응답 */
export const topFiveIndividualCompensationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(topFiveIndividualCompensationItemSchema).nullish(),
});

/** 타법인 출자현황 응답 */
export const otherCorporationInvestmentsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(otherCorporationInvestmentsItemSchema).nullish(),
});

/** 주식의 총수 현황 응답 */
export const totalNumberOfSharesResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(totalNumberOfSharesItemSchema).nullish(),
});

/** 채무증권 발행실적 응답 */
export const debtSecuritiesIssuancePerformanceResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(debtSecuritiesIssuancePerformanceItemSchema).nullish(),
});

/** 기업어음증권 미상환 잔액 응답 */
export const outstandingCommercialPaperBalanceResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outstandingCommercialPaperBalanceItemSchema).nullish(),
});

/** 단기사채 미상환 잔액 응답 */
export const outstandingShortTermBondsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outstandingShortTermBondsItemSchema).nullish(),
});

/** 회사채 미상환 잔액 응답 */
export const outstandingCorporateBondsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outstandingCorporateBondsItemSchema).nullish(),
});

/** 신종자본증권 미상환 잔액 응답 */
export const outstandingHybridCapitalSecuritiesResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outstandingHybridCapitalSecuritiesItemSchema).nullish(),
});

/** 조건부 자본증권 미상환 잔액 응답 */
export const outstandingContingentCapitalSecuritiesResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outstandingContingentCapitalSecuritiesItemSchema).nullish(),
});

/** 회계감사인 명칭과 감사의견 응답 */
export const auditorNameAndOpinionResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(auditorNameAndOpinionItemSchema).nullish(),
});

/** 감사용역 계약현황 응답 */
export const auditServiceContractsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(auditServiceContractsItemSchema).nullish(),
});

/** 회계감사인과의 비감사용역 계약체결 현황 응답 */
export const nonAuditServiceContractsResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(nonAuditServiceContractsItemSchema).nullish(),
});

/** 사외이사 및 변동현황 응답 */
export const outsideDirectorStatusResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(outsideDirectorStatusItemSchema).nullish(),
});

/** 미등기임원 보수현황 응답 */
export const unregisteredExecutiveCompensationResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(unregisteredExecutiveCompensationItemSchema).nullish(),
});

/** 이사·감사 전체 보수현황(주주총회 승인금액) 응답 */
export const boardAndAuditCompensationShareholderApprovedResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(boardAndAuditCompensationShareholderApprovedItemSchema).nullish(),
});

/** 이사·감사 전체 보수현황(보수지급금액 유형별) 응답 */
export const boardAndAuditCompensationByTypeResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(boardAndAuditCompensationByTypeItemSchema).nullish(),
});

/** 공모자금 사용내역 응답 */
export const publicOfferingFundUsageResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(publicOfferingFundUsageItemSchema).nullish(),
});

/** 사모자금 사용내역 응답 */
export const privatePlacementFundUsageResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(privatePlacementFundUsageItemSchema).nullish(),
});

// ── Response Types ──

export type CapitalChangeStatusResponse = CamelizeKeys<z.infer<typeof capitalChangeStatusResponseSchema>>;
export type DividendInformationResponse = CamelizeKeys<z.infer<typeof dividendInformationResponseSchema>>;
export type TreasuryStockActivityResponse = CamelizeKeys<z.infer<typeof treasuryStockActivityResponseSchema>>;
export type MajorShareholderStatusResponse = CamelizeKeys<z.infer<typeof majorShareholderStatusResponseSchema>>;
export type MajorShareholderChangesResponse = CamelizeKeys<z.infer<typeof majorShareholderChangesResponseSchema>>;
export type MinorityShareholderStatusResponse = CamelizeKeys<z.infer<typeof minorityShareholderStatusResponseSchema>>;
export type ExecutiveStatusResponse = CamelizeKeys<z.infer<typeof executiveStatusResponseSchema>>;
export type EmployeeStatusResponse = CamelizeKeys<z.infer<typeof employeeStatusResponseSchema>>;
export type BoardAndAuditCompensationAbove500mResponse = CamelizeKeys<
  z.infer<typeof boardAndAuditCompensationAbove500mResponseSchema>
>;
export type BoardAndAuditTotalCompensationResponse = CamelizeKeys<
  z.infer<typeof boardAndAuditTotalCompensationResponseSchema>
>;
export type TopFiveIndividualCompensationResponse = CamelizeKeys<
  z.infer<typeof topFiveIndividualCompensationResponseSchema>
>;
export type OtherCorporationInvestmentsResponse = CamelizeKeys<
  z.infer<typeof otherCorporationInvestmentsResponseSchema>
>;
export type TotalNumberOfSharesResponse = CamelizeKeys<z.infer<typeof totalNumberOfSharesResponseSchema>>;
export type DebtSecuritiesIssuancePerformanceResponse = CamelizeKeys<
  z.infer<typeof debtSecuritiesIssuancePerformanceResponseSchema>
>;
export type OutstandingCommercialPaperBalanceResponse = CamelizeKeys<
  z.infer<typeof outstandingCommercialPaperBalanceResponseSchema>
>;
export type OutstandingShortTermBondsResponse = CamelizeKeys<z.infer<typeof outstandingShortTermBondsResponseSchema>>;
export type OutstandingCorporateBondsResponse = CamelizeKeys<z.infer<typeof outstandingCorporateBondsResponseSchema>>;
export type OutstandingHybridCapitalSecuritiesResponse = CamelizeKeys<
  z.infer<typeof outstandingHybridCapitalSecuritiesResponseSchema>
>;
export type OutstandingContingentCapitalSecuritiesResponse = CamelizeKeys<
  z.infer<typeof outstandingContingentCapitalSecuritiesResponseSchema>
>;
export type AuditorNameAndOpinionResponse = CamelizeKeys<z.infer<typeof auditorNameAndOpinionResponseSchema>>;
export type AuditServiceContractsResponse = CamelizeKeys<z.infer<typeof auditServiceContractsResponseSchema>>;
export type NonAuditServiceContractsResponse = CamelizeKeys<z.infer<typeof nonAuditServiceContractsResponseSchema>>;
export type OutsideDirectorStatusResponse = CamelizeKeys<z.infer<typeof outsideDirectorStatusResponseSchema>>;
export type UnregisteredExecutiveCompensationResponse = CamelizeKeys<
  z.infer<typeof unregisteredExecutiveCompensationResponseSchema>
>;
export type BoardAndAuditCompensationShareholderApprovedResponse = CamelizeKeys<
  z.infer<typeof boardAndAuditCompensationShareholderApprovedResponseSchema>
>;
export type BoardAndAuditCompensationByTypeResponse = CamelizeKeys<
  z.infer<typeof boardAndAuditCompensationByTypeResponseSchema>
>;
export type PublicOfferingFundUsageResponse = CamelizeKeys<z.infer<typeof publicOfferingFundUsageResponseSchema>>;
export type PrivatePlacementFundUsageResponse = CamelizeKeys<z.infer<typeof privatePlacementFundUsageResponseSchema>>;

// ── Response Map ──

export interface PeriodicReportKeyInformationResponseMap {
  getCapitalChangeStatus: CapitalChangeStatusResponse;
  getDividendInformation: DividendInformationResponse;
  getTreasuryStockActivity: TreasuryStockActivityResponse;
  getMajorShareholderStatus: MajorShareholderStatusResponse;
  getMajorShareholderChanges: MajorShareholderChangesResponse;
  getMinorityShareholderStatus: MinorityShareholderStatusResponse;
  getExecutiveStatus: ExecutiveStatusResponse;
  getEmployeeStatus: EmployeeStatusResponse;
  getBoardAndAuditCompensationAbove500m: BoardAndAuditCompensationAbove500mResponse;
  getBoardAndAuditTotalCompensation: BoardAndAuditTotalCompensationResponse;
  getTopFiveIndividualCompensation: TopFiveIndividualCompensationResponse;
  getOtherCorporationInvestments: OtherCorporationInvestmentsResponse;
  getTotalNumberOfShares: TotalNumberOfSharesResponse;
  getDebtSecuritiesIssuancePerformance: DebtSecuritiesIssuancePerformanceResponse;
  getOutstandingCommercialPaperBalance: OutstandingCommercialPaperBalanceResponse;
  getOutstandingShortTermBonds: OutstandingShortTermBondsResponse;
  getOutstandingCorporateBonds: OutstandingCorporateBondsResponse;
  getOutstandingHybridCapitalSecurities: OutstandingHybridCapitalSecuritiesResponse;
  getOutstandingContingentCapitalSecurities: OutstandingContingentCapitalSecuritiesResponse;
  getAuditorNameAndOpinion: AuditorNameAndOpinionResponse;
  getAuditServiceContracts: AuditServiceContractsResponse;
  getNonAuditServiceContracts: NonAuditServiceContractsResponse;
  getOutsideDirectorStatus: OutsideDirectorStatusResponse;
  getUnregisteredExecutiveCompensation: UnregisteredExecutiveCompensationResponse;
  getBoardAndAuditCompensationShareholderApproved: BoardAndAuditCompensationShareholderApprovedResponse;
  getBoardAndAuditCompensationByType: BoardAndAuditCompensationByTypeResponse;
  getPublicOfferingFundUsage: PublicOfferingFundUsageResponse;
  getPrivatePlacementFundUsage: PrivatePlacementFundUsageResponse;
}
