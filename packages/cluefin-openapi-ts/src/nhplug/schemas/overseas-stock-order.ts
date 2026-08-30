import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

/**
 * NH PLUG 해외주식(주문) 응답 스키마.
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

// ── 주문 접수 결과 (`Output_0`). 매수·매도·정정·취소 공통. ──

export const overseasStockOrderOutputSchema = z
  .object({
    amn_tab_cd: str(), // 관리팀점코드
    orr_no: num(), // 주문번호
  })
  .passthrough();

/**
 * 해외주식 주문매수 (`POST /gbstock/order/v1/buy`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderBuyResponseSchema = z
  .object({
    ...envelope,
    /** 주문 접수 결과 */
    Output_0: overseasStockOrderOutputSchema.nullish(),
  })
  .passthrough();

/**
 * 해외주식 주문매도 (`POST /gbstock/order/v1/sell`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderSellResponseSchema = z
  .object({
    ...envelope,
    /** 주문 접수 결과 */
    Output_0: overseasStockOrderOutputSchema.nullish(),
  })
  .passthrough();

/**
 * 해외주식 정정취소주문정정 (`POST /gbstock/order/v1/modify`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderModifyResponseSchema = z
  .object({
    ...envelope,
    /** 주문 접수 결과 */
    Output_0: overseasStockOrderOutputSchema.nullish(),
  })
  .passthrough();

/**
 * 해외주식 정정취소주문취소 (`POST /gbstock/order/v1/cancel`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderCancelResponseSchema = z
  .object({
    ...envelope,
    /** 주문 접수 결과 */
    Output_0: overseasStockOrderOutputSchema.nullish(),
  })
  .passthrough();

// ── 예약주문접수 결과 (`Output_0`). ──

export const overseasStockOrderReservedSubmitOutputSchema = z
  .object({
    bkg_rtn_orr_no: num(), // 예약접수주문번호
  })
  .passthrough();

/**
 * 해외주식 예약주문접수 (`POST /gbstock/order/v1/reservedSubmit`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderReservedSubmitResponseSchema = z
  .object({
    ...envelope,
    /** 예약주문접수 결과 */
    Output_0: overseasStockOrderReservedSubmitOutputSchema.nullish(),
  })
  .passthrough();

// ── 예약주문접수취소 결과 (`Output_0`). ──

export const overseasStockOrderReservedCancelOutputSchema = z
  .object({
    wrk_rlt_cd: str(), // 작업결과코드
  })
  .passthrough();

/**
 * 해외주식 예약주문접수취소 (`POST /gbstock/order/v1/reservedCancel`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockOrderReservedCancelResponseSchema = z
  .object({
    ...envelope,
    /** 예약주문접수취소 결과 */
    Output_0: overseasStockOrderReservedCancelOutputSchema.nullish(),
  })
  .passthrough();

// ── Response Types ──

/** 해외주식 주문매수 (`POST /gbstock/order/v1/buy`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderBuyResponse = CamelizeKeys<z.infer<typeof overseasStockOrderBuyResponseSchema>>;
/** 해외주식 주문매도 (`POST /gbstock/order/v1/sell`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderSellResponse = CamelizeKeys<z.infer<typeof overseasStockOrderSellResponseSchema>>;
/** 해외주식 정정취소주문정정 (`POST /gbstock/order/v1/modify`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderModifyResponse = CamelizeKeys<z.infer<typeof overseasStockOrderModifyResponseSchema>>;
/** 해외주식 정정취소주문취소 (`POST /gbstock/order/v1/cancel`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderCancelResponse = CamelizeKeys<z.infer<typeof overseasStockOrderCancelResponseSchema>>;
/** 해외주식 예약주문접수 (`POST /gbstock/order/v1/reservedSubmit`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderReservedSubmitResponse = CamelizeKeys<
  z.infer<typeof overseasStockOrderReservedSubmitResponseSchema>
>;
/** 해외주식 예약주문접수취소 (`POST /gbstock/order/v1/reservedCancel`) 응답. — `Output_0`: 객체 */
export type OverseasStockOrderReservedCancelResponse = CamelizeKeys<
  z.infer<typeof overseasStockOrderReservedCancelResponseSchema>
>;

// ── Response Map ──

export interface OverseasStockOrderResponseMap {
  buy: OverseasStockOrderBuyResponse;
  sell: OverseasStockOrderSellResponse;
  modify: OverseasStockOrderModifyResponse;
  cancel: OverseasStockOrderCancelResponse;
  reservedSubmit: OverseasStockOrderReservedSubmitResponse;
  reservedCancel: OverseasStockOrderReservedCancelResponse;
}
