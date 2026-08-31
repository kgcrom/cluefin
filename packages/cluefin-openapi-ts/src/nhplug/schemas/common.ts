import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';

/** 공통 응답 봉투 (`rsp_cd`/`rsp_msg`). */
const commonEnvelope = {
  /** 응답코드 (00000: 성공) */
  rsp_cd: z.string(),
  /** 응답메시지 */
  rsp_msg: z.string(),
};

export const accountItemSchema = z
  .object({
    /** 계좌번호 (이후 API 의 입력 `act_no` 에 사용) */
    acct_no: z.string(),
    /** 계좌구분 (01: 자계좌, 02: 주문대리인계좌, 03: 모의투자계좌) */
    acct_type: z.enum(['01', '02', '03']),
  })
  .passthrough();

/** 계좌 목록 조회 (`POST /n2/acctinfo`) 응답. */
export const accountListResponseSchema = z
  .object({
    /** 응답코드 */
    rsp_cd: z.string().nullish(),
    /** 응답메시지 */
    rsp_msg: z.string().nullish(),
    /** 고객번호 */
    cust_no: z.string().nullish(),
    /** 보유 계좌 목록 */
    Output_0: z.array(accountItemSchema).nullish(),
  })
  .passthrough();

/** 실시간(Websocket) 세션해제 (`POST /websocket/close/session`) 응답. */
export const websocketCloseResponseSchema = z
  .object({
    ...commonEnvelope,
  })
  .passthrough();

// ── Response Types ──

export type AccountListResponse = CamelizeKeys<z.infer<typeof accountListResponseSchema>>;
export type WebsocketCloseResponse = CamelizeKeys<z.infer<typeof websocketCloseResponseSchema>>;

// ── Response Map ──

export interface CommonResponseMap {
  getAccountList: AccountListResponse;
  closeWebsocketSession: WebsocketCloseResponse;
}
