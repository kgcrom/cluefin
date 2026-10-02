import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';
import { dartEnvelope } from './common.js';

/** 공시검색 결과 항목 */
export const publicDisclosureSearchItemSchema = z.object({
  /** 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 공시대상회사의 종목명(상장사) 또는 법인명(기타법인) */
  corp_name: z.string(),
  /** 공시대상회사의 고유번호(8자리) */
  corp_code: z.string(),
  /** 상장회사의 종목코드(6자리) */
  stock_code: z.string(),
  /** 공시 보고서명. 기재정정, 첨부정정 등 수정 사유가 포함될 수 있습니다. */
  report_nm: z.string(),
  /** 접수번호(14자리). 전자공시시스템 공시뷰어 연결에 사용됩니다. */
  rcept_no: z.string(),
  /** 공시를 제출한 개인 또는 기관명 */
  flr_nm: z.string(),
  /** 공시 접수일자(YYYYMMDD) */
  rcept_dt: z.string(),
  rm: z.string(),
});

/** 공시검색 요청 응답 */
export const publicDisclosureSearchResponseSchema = z.object({
  ...dartEnvelope,
  list: z.array(publicDisclosureSearchItemSchema).nullish(),
});

/** 기업개황 응답 */
export const companyOverviewResponseSchema = z.object({
  /** 에러 및 정보 코드(※메시지 설명 참조) */
  status: z.string(),
  /** 에러 및 정보 메시지(※메시지 설명 참조) */
  message: z.string(),
  /** 정식명칭 */
  corp_name: z.string(),
  /** 영문정식회사명칭 */
  corp_name_eng: z.string(),
  /** 종목명(상장사) 또는 약식명칭(기타법인) */
  stock_name: z.string(),
  /** 상장회사의 종목코드(6자리) */
  stock_code: z.string(),
  /** 대표자명 */
  ceo_nm: z.string(),
  /** 법인구분: Y(유가), K(코스닥), N(코넥스), E(기타) */
  corp_cls: z.string(),
  /** 법인등록번호 */
  jurir_no: z.string(),
  /** 사업자등록번호 */
  bizr_no: z.string(),
  /** 주소 */
  adres: z.string(),
  /** 홈페이지 */
  hm_url: z.string(),
  /** IR홈페이지 */
  ir_url: z.string(),
  /** 전화번호 */
  phn_no: z.string(),
  /** 팩스번호 */
  fax_no: z.string(),
  /** 업종코드 */
  induty_code: z.string(),
  /** 설립일(YYYYMMDD) */
  est_dt: z.string(),
  /** 결산월(MM) */
  acc_mt: z.string(),
});

// ── Response Types ──

export type PublicDisclosureSearchResponse = CamelizeKeys<z.infer<typeof publicDisclosureSearchResponseSchema>>;
export type CompanyOverviewResponse = CamelizeKeys<z.infer<typeof companyOverviewResponseSchema>>;

// ── Response Map ──

export interface PublicDisclosureResponseMap {
  publicDisclosureSearch: PublicDisclosureSearchResponse;
  companyOverview: CompanyOverviewResponse;
}
