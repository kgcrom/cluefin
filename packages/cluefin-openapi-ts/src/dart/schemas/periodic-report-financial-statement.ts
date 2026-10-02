import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';
import { dartEnvelope, dartNumeric } from './common.js';

/** 단일회사 주요계정 현황 */
export const singleCompanyMajorAccountItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 사업 연도 (YYYY) */
  bsns_year: z.string(),
  /** 종목 코드 (상장회사의 종목코드 6자리) */
  stock_code: z.string(),
  /** 보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011) */
  reprt_code: z.string(),
  /** 계정명 (ex: 자본총계) */
  account_nm: z.string(),
  /** 개별/연결구분 (OFS:재무제표, CFS:연결재무제표) */
  fs_div: z.string(),
  /** 개별/연결명 (ex: 연결재무제표 또는 재무제표 출력) */
  fs_nm: z.string(),
  /** 재무제표구분 (BS:재무상태표, IS:손익계산서) */
  sj_div: z.string(),
  /** 재무제표명 (ex: 재무상태표 또는 손익계산서 출력) */
  sj_nm: z.string(),
  /** 당기명 (ex: 제 13 기 3분기말) */
  thstrm_nm: z.string(),
  /** 당기일자 (ex: 2018.09.30 현재) */
  thstrm_dt: z.string(),
  /** 당기금액 (ex: 9,999,999,999) */
  thstrm_amount: z.string(),
  /** 당기누적금액 (ex: 9,999,999,999) */
  thstrm_add_amount: z.string().nullish(),
  /** 전기명 (ex: 제 12 기말) */
  frmtrm_nm: z.string(),
  /** 전기일자 (ex: 2017.01.01 ~ 2017.12.31) */
  frmtrm_dt: z.string(),
  /** 전기금액 (ex: 9,999,999,999) */
  frmtrm_amount: z.string(),
  /** 전기누적금액 (ex: 9,999,999,999) */
  frmtrm_add_amount: z.string().nullish(),
  /** 전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_nm: z.string().nullish(),
  /** 전전기일자 (ex: 2016.12.31 현재(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_dt: z.string().nullish(),
  /** 전전기금액 (ex: 9,999,999,999(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_amount: z.string().nullish(),
  /** 계정과목 정렬순서 */
  ord: dartNumeric,
  /** 통화 단위 */
  currency: z.string(),
});

/** 다중회사 주요계정 현황 */
export const multiCompanyMajorAccountItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 사업 연도 (YYYY) */
  bsns_year: z.string(),
  /** 종목 코드 (상장회사의 종목코드 6자리) */
  stock_code: z.string(),
  /** 회사명 */
  corp_name: z.string().nullish(),
  /** 공시대상회사 고유번호 (8자리) */
  corp_code: z.string(),
  /** 보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011) */
  reprt_code: z.string(),
  /** 계정명 (ex: 자본총계) */
  account_nm: z.string(),
  /** 개별/연결구분 (OFS:재무제표, CFS:연결재무제표) */
  fs_div: z.string(),
  /** 개별/연결명 (ex: 연결재무제표 또는 재무제표 출력) */
  fs_nm: z.string(),
  /** 재무제표구분 (BS:재무상태표, IS:손익계산서) */
  sj_div: z.string(),
  /** 재무제표명 (ex: 재무상태표 또는 손익계산서 출력) */
  sj_nm: z.string(),
  /** 당기명 (ex: 제 13 기 3분기말) */
  thstrm_nm: z.string(),
  /** 당기일자 (ex: 2018.09.30 현재) */
  thstrm_dt: z.string(),
  /** 당기금액 (ex: 9,999,999,999) */
  thstrm_amount: z.string(),
  /** 당기누적금액 (ex: 9,999,999,999) */
  thstrm_add_amount: z.string().nullish(),
  /** 전기명 (ex: 제 12 기말) */
  frmtrm_nm: z.string(),
  /** 전기일자 (ex: 2017.01.01 ~ 2017.12.31) */
  frmtrm_dt: z.string(),
  /** 전기금액 (ex: 9,999,999,999) */
  frmtrm_amount: z.string(),
  /** 전기누적금액 (ex: 9,999,999,999) */
  frmtrm_add_amount: z.string().nullish(),
  /** 전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_nm: z.string().nullish(),
  /** 전전기일자 (ex: 2016.12.31 현재(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_dt: z.string().nullish(),
  /** 전전기금액 (ex: 9,999,999,999(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_amount: z.string().nullish(),
  /** 계정과목 정렬순서 */
  ord: z.string(),
  /** 통화 단위 */
  currency: z.string(),
});

/** 단일회사 전체 재무제표 현황 */
export const singleCompanyFullStatementItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011) */
  reprt_code: z.string(),
  /** 사업 연도 (YYYY) */
  bsns_year: z.string(),
  /** 고유번호 (공시대상회사의 고유번호(8자리)) */
  corp_code: z.string(),
  /** 재무제표구분 (BS : 재무상태표 IS : 손익계산서 CIS : 포괄손익계산서 CF : 현금흐름표 SCE : 자본변동표) */
  sj_div: z.string(),
  /** 재무제표명 (ex: 재무상태표 또는 손익계산서 출력) */
  sj_nm: z.string(),
  account_id: z.string(),
  /** 계정명 (계정명칭 ex) 자본총계) */
  account_nm: z.string(),
  /** 계정상세 (※ 자본변동표에만 출력) */
  account_detail: z.string(),
  /** 당기명 (ex: 제 13 기) */
  thstrm_nm: z.string(),
  /** 당기금액 (9,999,999,999 ※ 분/반기 보고서이면서 (포괄)손익계산서 일 경우 [3개월] 금액) */
  thstrm_amount: z.string(),
  /** 당기누적금액 (9,999,999,999) */
  thstrm_add_amount: z.string().nullish(),
  /** 전기명 (ex: 제 12 기말) */
  frmtrm_nm: z.string().nullish(),
  /** 전기금액 (9,999,999,999) */
  frmtrm_amount: z.string().nullish(),
  /** 전기명(분/반기) (ex: 제 18 기 반기) */
  frmtrm_q_nm: z.string().nullish(),
  /** 전기금액(분/반기) (9,999,999,999 ※ 분/반기 보고서이면서 (포괄)손익계산서 일 경우 [3개월] 금액) */
  frmtrm_q_amount: z.string().nullish(),
  /** 전기누적금액 (9,999,999,999) */
  frmtrm_add_amount: z.string().nullish(),
  /** 전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_nm: z.string().nullish(),
  /** 전전기금액 (9,999,999,999(※ 사업보고서의 경우에만 출력)) */
  bfefrmtrm_amount: z.string().nullish(),
  /** 계정과목 정렬순서 (계정과목 정렬순서) */
  ord: z.string(),
  /** 통화 단위 (통화 단위) */
  currency: z.string(),
});

/** 단일회사 주요 재무지표 현황 */
export const singleCompanyMajorIndicatorItemSchema = z.object({
  /** 보고서 코드 (1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011) */
  reprt_code: z.string(),
  /** 사업 연도 (YYYY) */
  bsns_year: z.string(),
  /** 고유번호 (공시대상회사의 고유번호(8자리)) */
  corp_code: z.string(),
  /** 종목 코드 (상장회사의 종목코드(6자리)) */
  stock_code: z.string(),
  /** 결산기준일 (YYYY-MM-DD) */
  stlm_dt: z.string(),
  /** 지표분류코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000) */
  idx_cl_code: z.string(),
  /** 지표분류명 (수익성지표,안정성지표,성장성지표,활동성지표) */
  idx_cl_nm: z.string(),
  /** 지표코드 (ex) M211000 */
  idx_code: z.string(),
  /** 지표명 (ex) 영업이익률 */
  idx_nm: z.string(),
  /** 지표값 (ex) 0.256 — 일부 항목은 값이 제공되지 않습니다. */
  idx_val: z.string().nullish(),
});

/** 다중회사 주요 재무지표 현황 */
export const multiCompanyMajorIndicatorItemSchema = z.object({
  /** 보고서 코드 (1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011) */
  reprt_code: z.string(),
  /** 사업 연도 (YYYY) */
  bsns_year: z.string(),
  /** 고유번호 (공시대상회사의 고유번호(8자리)) */
  corp_code: z.string(),
  /** 종목 코드 (상장회사의 종목코드(6자리)) */
  stock_code: z.string(),
  /** 결산기준일 (YYYY-MM-DD) */
  stlm_dt: z.string(),
  /** 지표분류코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000) */
  idx_cl_code: z.string(),
  /** 지표분류명 (수익성지표,안정성지표,성장성지표,활동성지표) */
  idx_cl_nm: z.string(),
  /** 지표코드 (ex) M211000 */
  idx_code: z.string(),
  /** 지표명 (ex) 영업이익률 */
  idx_nm: z.string(),
  /** 지표값 (ex) 0.256 — 일부 항목은 값이 제공되지 않습니다. */
  idx_val: z.string().nullish(),
});

/** XBRL 택사노미 재무제표 양식 현황 */
export const xbrlTaxonomyItemSchema = z.object({
  /** 재무제표구분 (BS1:재무상태표, BS2:재무상태표(요약), BS3:재무상태표(비교), BS4:재무상태표(요약,비교), IS1:손익계산서, IS2:손익계산서(요약), IS3:손익계산서(비교), IS4:손익계산서(요약,비교), CIS1:포괄손익계산서, CIS2:포괄손익계산서(요약), CIS3:포괄손익계산서(비교), CIS4:포괄손익계산서(요약,비교), DCIS1:별도손익계산서, DCIS2:별도손익계산서(요약), DCIS3:별도손익계산서(비교), DCIS4:별도손익계산서(요약,비교), DCIS5:별도포괄손익계산서, DCIS6:별도포괄손익계산서(요약), DCIS7:별도포괄손익계산서(비교), DCIS8:별도포괄손익계산서(요약,비교), CF1:현금흐름표, CF2:현금흐름표(요약), CF3:현금흐름표(비교), CF4:현금흐름표(요약,비교), SCE1:자본변동표, SCE2:자본변동표(요약)) */
  sj_div: z.string(),
  account_id: z.string(),
  /** 계정명 (계정명칭 ex) 자본총계) */
  account_nm: z.string(),
  /** 기준일 (ex: 20221231) */
  bsns_de: z.string(),
  /** 한글 출력명 (ex: 자본총계) */
  label_kor: z.string(),
  /** 영문 출력명 (ex: Total Equity) */
  label_eng: z.string(),
  /** 데이터 유형 (※ 데이타 유형설명 - text block : 제목 - Text : Text - yyyy-mm-dd : Date - X : Monetary Value - (X): Monetary Value(Negative) - X.XX : Decimalized Value - Shares : Number of shares (주식 수) - For each : 공시된 항목이 전후로 반복적으로 공시될 경우 사용 - 공란 : 입력 필요 없음) */
  data_tp: z.string().nullish(),
  /** IFRS Reference (ex: K-IFRS 1001 문단 54 (9),K-IFRS 1007 문단 45) */
  ifrs_ref: z.string(),
});

/** 단일회사 주요계정 응답 */
export const singleCompanyMajorAccountResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(singleCompanyMajorAccountItemSchema).nullish(),
});

/** 다중회사 주요계정 응답 */
export const multiCompanyMajorAccountResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(multiCompanyMajorAccountItemSchema).nullish(),
});

/** 단일회사 전체 재무제표 응답 */
export const singleCompanyFullStatementResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(singleCompanyFullStatementItemSchema).nullish(),
});

/** 단일회사 주요 재무지표 응답 */
export const singleCompanyMajorIndicatorResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(singleCompanyMajorIndicatorItemSchema).nullish(),
});

/** 다중회사 주요 재무지표 응답 */
export const multiCompanyMajorIndicatorResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(multiCompanyMajorIndicatorItemSchema).nullish(),
});

/** XBRL 택사노미 재무제표 양식 응답 */
export const xbrlTaxonomyResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(xbrlTaxonomyItemSchema).nullish(),
});

// ── Response Types ──

export type SingleCompanyMajorAccountResponse = CamelizeKeys<z.infer<typeof singleCompanyMajorAccountResponseSchema>>;
export type MultiCompanyMajorAccountResponse = CamelizeKeys<z.infer<typeof multiCompanyMajorAccountResponseSchema>>;
export type SingleCompanyFullStatementResponse = CamelizeKeys<z.infer<typeof singleCompanyFullStatementResponseSchema>>;
export type SingleCompanyMajorIndicatorResponse = CamelizeKeys<
  z.infer<typeof singleCompanyMajorIndicatorResponseSchema>
>;
export type MultiCompanyMajorIndicatorResponse = CamelizeKeys<z.infer<typeof multiCompanyMajorIndicatorResponseSchema>>;
export type XbrlTaxonomyResponse = CamelizeKeys<z.infer<typeof xbrlTaxonomyResponseSchema>>;

// ── Response Map ──

export interface PeriodicReportFinancialStatementResponseMap {
  getSingleCompanyMajorAccounts: SingleCompanyMajorAccountResponse;
  getMultiCompanyMajorAccounts: MultiCompanyMajorAccountResponse;
  getSingleCompanyFullStatements: SingleCompanyFullStatementResponse;
  getSingleCompanyMajorIndicators: SingleCompanyMajorIndicatorResponse;
  getMultiCompanyMajorIndicators: MultiCompanyMajorIndicatorResponse;
  getXbrlTaxonomy: XbrlTaxonomyResponse;
}
