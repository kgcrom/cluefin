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

/** 신규 주문(현금·신용 매수/매도) 공통 접수 결과 — 스펙상 4개 API 의 Output_0 이 동일하다. */
export const krStockOrderPlacedOutputSchema = z
  .object({
    /** 주문채번팀점코드 */
    orr_gno_tab_cd: z.string().nullish(),
    /** 시장주문번호 — 정정·취소시 필요한 주문번호 */
    mkt_orr_no: num.nullish(),
    /** SOR파일ID — 요청시장코드 SOR 경우에만 세팅 */
    sor_fle_id: z.string().nullish(),
    /** SOR배분비율1 (KRX) — SOR 경우에만 세팅 */
    sor_ant_rt1: num.nullish(),
    /** SOR배분비율2 (NXT) — SOR 경우에만 세팅 */
    sor_ant_rt2: num.nullish(),
    /** 주문수량1 (KRX) */
    orr_qty1: num.nullish(),
    /** 주문수량2 (NXT) */
    orr_qty2: num.nullish(),
    /** 신규자시장주문번호1 (KRX) */
    anw_cld_mkt_orr_no1: num.nullish(),
    /** 신규자시장주문번호2 (NXT) */
    anw_cld_mkt_orr_no2: num.nullish(),
  })
  .passthrough();

/** 주식주문(현금) 매수 (`POST /krstock/order/v1/cashBuy`) 응답. */
export const krStockOrderCashBuyResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 주문 접수 결과 */
    Output_0: krStockOrderPlacedOutputSchema.nullish(),
  })
  .passthrough();

/** 주식주문(현금) 매도 (`POST /krstock/order/v1/cashSell`) 응답. */
export const krStockOrderCashSellResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 주문 접수 결과 */
    Output_0: krStockOrderPlacedOutputSchema.nullish(),
  })
  .passthrough();

/** 주식주문(신용) 매수 (`POST /krstock/order/v1/creditBuy`) 응답. */
export const krStockOrderCreditBuyResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 주문 접수 결과 */
    Output_0: krStockOrderPlacedOutputSchema.nullish(),
  })
  .passthrough();

/** 주식주문(신용) 매도 (`POST /krstock/order/v1/creditSell`) 응답. */
export const krStockOrderCreditSellResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 주문 접수 결과 */
    Output_0: krStockOrderPlacedOutputSchema.nullish(),
  })
  .passthrough();

/** 정정·취소(modify·cancel) 공통 접수 결과 — 스펙상 두 API 의 Output_0 이 동일하다. */
export const krStockOrderAmendedOutputSchema = z
  .object({
    /** 주문채번팀점코드 */
    orr_gno_tab_cd: z.string().nullish(),
    /** 시장주문번호 — 정정·취소시 필요한 주문번호 */
    mkt_orr_no: num.nullish(),
    /** SOR파일ID — 요청시장코드 SOR 경우에만 세팅 */
    sor_fle_id: z.string().nullish(),
    /** 취소SOR배분비율1 (KRX) — SOR 경우에만 세팅 */
    can_sor_ant_rt1: num.nullish(),
    /** 취소SOR배분비율2 (NXT) — SOR 경우에만 세팅 */
    can_sor_ant_rt2: num.nullish(),
    /** 취소주문수량1 (KRX) */
    can_orr_qty1: num.nullish(),
    /** 취소주문수량2 (NXT) */
    can_orr_qty2: num.nullish(),
    /** 취소자시장주문번호1 (KRX) */
    can_cld_mkt_orr_no1: num.nullish(),
    /** 취소자시장주문번호2 (NXT) */
    can_cld_mkt_orr_no2: num.nullish(),
  })
  .passthrough();

/** 주식주문(정정취소) 정정 (`POST /krstock/order/v1/modify`) 응답. */
export const krStockOrderModifyResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 정정 접수 결과 */
    Output_0: krStockOrderAmendedOutputSchema.nullish(),
  })
  .passthrough();

/** 주식주문(정정취소) 취소 (`POST /krstock/order/v1/cancel`) 응답. */
export const krStockOrderCancelResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 취소 접수 결과 */
    Output_0: krStockOrderAmendedOutputSchema.nullish(),
  })
  .passthrough();

/**
 * 주식예약주문 접수 결과 — 신규·정정취소 계열과 달리 전용 스키마(입력값 표시 위주)다.
 *
 * 주의: 아래 필드는 스펙(krstock/openapi.json)의 200 응답 스키마 선언을 옮긴 것이고
 * 실서버 응답으로 확인된 것이 아니다. 스펙에 이 API 의 예시 응답이 없고, 예약주문은
 * 실주문이라 모의투자에서도 접수가 안 돼 실측 경로가 없다. 실제로는 `bkg_orr_no` 만
 * 내려올 가능성이 크다. 전부 nullish 이므로 어느 쪽이든 파싱은 안전하다.
 */
export const krStockOrderReservedOrderOutputSchema = z
  .object({
    /** 예약주문번호 — 예약 접수된 번호 */
    bkg_orr_no: num.nullish(),
    /** 계좌번호 — 입력값 표시 */
    act_no: z.string().nullish(),
    /** 종목코드 — 입력값 표시 */
    iem_cd: z.string().nullish(),
    /** 매매구분코드 — 입력값 표시 (1.매도 2.매수) */
    sby_dit_cd: z.string().nullish(),
    /** 선물대용주문여부 — 입력값 표시 */
    frs_sba_orr_yn: z.string().nullish(),
    /** 호가유형코드 — 입력값 표시 */
    nmn_pr_tp_cd: z.string().nullish(),
    /** 신용대출코드 — 입력값 표시 */
    cfd_lon_cd: z.string().nullish(),
    /** 대출일자 — 입력값 표시 (YYYYMMDD) */
    lon_dt: z.string().nullish(),
    /** 주문수량 — 입력값 표시 */
    orr_qty: z.string().nullish(),
    /** 주문단가 — 입력값 표시 */
    orr_uit_pr: z.string().nullish(),
    /** 연락처전화번호 — 입력값 표시. 스펙 선언이며 실응답 미확인. 내려온다면 개인정보 */
    aca_tel_no: z.string().nullish(),
    /** 예약주문유형코드 — 입력값 표시 */
    bkg_orr_tp_cd: z.string().nullish(),
    /** 예약주문시작일자 — 입력값 표시 (YYYYMMDD) */
    bkg_orr_sta_dt: z.string().nullish(),
    /** 예약주문종료일자 — 입력값 표시 (YYYYMMDD) */
    bkg_orr_end_dt: z.string().nullish(),
    /** 예약주문집행유형코드 — 입력값 표시 */
    bkg_orr_enf_tp_cd: z.string().nullish(),
    /** 종가대비등락폭금액 — 입력값 표시 */
    end_pr_cmp_ftw_amt: z.string().nullish(),
    /** 주문가격범위상한가 — 입력값 표시 */
    orr_pr_rge_hlm_pr: z.string().nullish(),
    /** 주문가격범위하한가 — 입력값 표시 */
    orr_pr_rge_llm_pr: z.string().nullish(),
    /**
     * 비밀번호 — 입력값 표시. 스펙 선언이며 실응답 미확인(파이썬 모델 주석 참고).
     * 값이 실제로 내려온다면 계좌 비밀번호이므로 로그·출력에 남기지 말 것.
     */
    pwd: z.string().nullish(),
  })
  .passthrough();

/** 주식예약주문 (`POST /krstock/order/v1/reservedOrder`) 응답. */
export const krStockOrderReservedOrderResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 예약주문 접수 결과 */
    Output_0: krStockOrderReservedOrderOutputSchema.nullish(),
  })
  .passthrough();

/** 주식예약주문취소 접수 결과 — 신규·정정취소·예약주문 계열과 다른 전용 스키마(입력값 표시)다. */
export const krStockOrderReservedCancelOutputSchema = z
  .object({
    /** 계좌번호 — 입력값 표시 */
    act_no: z.string().nullish(),
    /** 매매구분코드 — 입력값 표시 (1.매도 2.매수) */
    sby_dit_cd: z.string().nullish(),
    /** 종목코드 — 입력값 표시 */
    iem_cd: z.string().nullish(),
    /** 예약주문번호 — 입력값 표시 */
    bkg_orr_no: num.nullish(),
    /** 예약주문유형코드 — 입력값 표시 */
    bkg_orr_tp_cd: z.string().nullish(),
    /** 예약접수일자 — 입력값 표시 (YYYYMMDD) */
    bkg_rtn_dt: z.string().nullish(),
  })
  .passthrough();

/** 주식예약주문취소 (`POST /krstock/order/v1/reservedCancel`) 응답. */
export const krStockOrderReservedCancelResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 예약주문취소 접수 결과 */
    Output_0: krStockOrderReservedCancelOutputSchema.nullish(),
  })
  .passthrough();

// ── Response Types ──

export type KrStockOrderCashBuyResponse = CamelizeKeys<z.infer<typeof krStockOrderCashBuyResponseSchema>>;
export type KrStockOrderCashSellResponse = CamelizeKeys<z.infer<typeof krStockOrderCashSellResponseSchema>>;
export type KrStockOrderCreditBuyResponse = CamelizeKeys<z.infer<typeof krStockOrderCreditBuyResponseSchema>>;
export type KrStockOrderCreditSellResponse = CamelizeKeys<z.infer<typeof krStockOrderCreditSellResponseSchema>>;
export type KrStockOrderModifyResponse = CamelizeKeys<z.infer<typeof krStockOrderModifyResponseSchema>>;
export type KrStockOrderCancelResponse = CamelizeKeys<z.infer<typeof krStockOrderCancelResponseSchema>>;
export type KrStockOrderReservedOrderResponse = CamelizeKeys<z.infer<typeof krStockOrderReservedOrderResponseSchema>>;
export type KrStockOrderReservedCancelResponse = CamelizeKeys<z.infer<typeof krStockOrderReservedCancelResponseSchema>>;

// ── Response Map ──

export interface KrstockOrderResponseMap {
  cashBuy: KrStockOrderCashBuyResponse;
  cashSell: KrStockOrderCashSellResponse;
  creditBuy: KrStockOrderCreditBuyResponse;
  creditSell: KrStockOrderCreditSellResponse;
  modify: KrStockOrderModifyResponse;
  cancel: KrStockOrderCancelResponse;
  reservedOrder: KrStockOrderReservedOrderResponse;
  reservedCancel: KrStockOrderReservedCancelResponse;
}
