import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';
import { dartEnvelope } from './common.js';

/** 주식등의 대량보유 상황보고 항목 */
export const largeHoldingReportItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 공시 접수일자(YYYYMMDD) */
  rcept_dt: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 공시대상회사의 종목명(상장사) 또는 법인명(기타법인) */
  corp_name: z.string(),
  /** 보고구분 */
  report_tp: z.string(),
  /** 대표보고자명 */
  repror: z.string(),
  /** 보유주식등의 수 */
  stkqy: z.string(),
  /** 보유주식등의 증감 */
  stkqy_irds: z.string(),
  /** 보유비율 */
  stkrt: z.string(),
  /** 보유비율 증감 */
  stkrt_irds: z.string(),
  /** 주요체결 주식등의 수 */
  ctr_stkqy: z.string(),
  /** 주요체결 보유비율 */
  ctr_stkrt: z.string(),
  /** 보고사유 */
  report_resn: z.string(),
});

/** 임원·주요주주 소유보고 항목 */
export const executiveMajorShareholderOwnershipReportItemSchema = z.object({
  /** 접수번호(14자리) */
  rcept_no: z.string(),
  /** 공시 접수일자(YYYYMMDD) */
  rcept_dt: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 회사명 */
  corp_name: z.string(),
  /** 보고자명 */
  repror: z.string(),
  /** 발행 회사 관계 임원(등기임원, 비등기임원 등) */
  isu_exctv_rgist_at: z.string(),
  /** 발행 회사 관계 임원 직위(대표이사, 이사, 전무 등) */
  isu_exctv_ofcps: z.string(),
  /** 발행 회사 관계 주요 주주(10%이상주주 등) */
  isu_main_shrhldr: z.string().nullish(),
  /** 특정 증권 등 소유 수 */
  sp_stock_lmp_cnt: z.string(),
  /** 특정 증권 등 소유 증감 수 */
  sp_stock_lmp_irds_cnt: z.string(),
  /** 특정 증권 등 소유 비율 */
  sp_stock_lmp_rate: z.string(),
  /** 특정 증권 등 소유 증감 비율 */
  sp_stock_lmp_irds_rate: z.string(),
});

/** 주식등의 대량보유 상황보고 응답 */
export const largeHoldingReportResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(largeHoldingReportItemSchema).nullish(),
});

/** 임원·주요주주 소유보고 응답 */
export const executiveMajorShareholderOwnershipReportResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(executiveMajorShareholderOwnershipReportItemSchema).nullish(),
});

// ── Response Types ──

export type LargeHoldingReportResponse = CamelizeKeys<z.infer<typeof largeHoldingReportResponseSchema>>;
export type ExecutiveMajorShareholderOwnershipReportResponse = CamelizeKeys<
  z.infer<typeof executiveMajorShareholderOwnershipReportResponseSchema>
>;

// ── Response Map ──

export interface ShareDisclosureComprehensiveResponseMap {
  largeHoldingReport: LargeHoldingReportResponse;
  executiveMajorShareholderOwnershipReport: ExecutiveMajorShareholderOwnershipReportResponse;
}
