import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';

/**
 * NH PLUG 해외주식(시세) 응답 스키마.
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

// ── 해외주식 현재가상세 조회 결과 (`Output_0`). ──

export const overseasStockQuoteCurrentPriceOutputSchema = z
  .object({
    iem_cd: str(), // 종목코드
    kor_name: str(), // 종목명 / 스펙상 필드 (실서버는 iem_nm 로 내려준다)
    iem_nm: str(), // 종목명 / 실서버 실측 필드 (2026-08-22 운영 확인)
    industry_code: str(), // 업종코드
    industry_name: str(), // 업종명
    trdprc: num(), // 현재가
    netchng_cls: str(), // 전일대비구분 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)
    netchng: num(), // 전일대비
    pctchng: num(), // 전일대비율
    open_prc: num(), // 시가
    high: num(), // 고가
    low: num(), // 저가
    acvol: num(), // 거래량
    uplimit: num(), // 상한가
    uplimit_rate: num(), // 상한가비율
    lolimit: num(), // 하한가
    lolimit_rate: num(), // 하한가비율
    w52high_prc: num(), // 52주최고가
    w52highprc_netchng: num(), // 52주최고가대비
    w52high_date: str(), // 52주최고일자
    w52low_prc: num(), // 52주최저가
    w52lowprc_netchng: num(), // 52주최저가대비
    w52low_date: str(), // 52주최저일자
    quote_time: str(), // 호가시간
    best_ask1: num(), // 매도1호가
    best_bid1: num(), // 매수1호가
    best_asiz1: num(), // 매도1호가수량
    best_bsiz1: num(), // 매수1호가수량
    best_ask2: num(), // 매도2호가
    best_bid2: num(), // 매수2호가
    best_asiz2: num(), // 매도2호가수량
    best_bsiz2: num(), // 매수2호가수량
    best_ask3: num(), // 매도3호가
    best_bid3: num(), // 매수3호가
    best_asiz3: num(), // 매도3호가수량
    best_bsiz3: num(), // 매수3호가수량
    best_ask4: num(), // 매도4호가
    best_bid4: num(), // 매수4호가
    best_asiz4: num(), // 매도4호가수량
    best_bsiz4: num(), // 매수4호가수량
    best_ask5: num(), // 매도5호가
    best_bid5: num(), // 매수5호가
    best_asiz5: num(), // 매도5호가수량
    best_bsiz5: num(), // 매수5호가수량
    asksize: num(), // 총매도잔량
    bidsize: num(), // 총매수잔량
    cov_pric: num(), // 환산가
    currency_prc: num(), // 환율
    list_num: num(), // 발행주식수
    list_amt: num(), // 시가총액
    list_amt_2: num(), // 시가총액(원화)
    turnover: num(), // 거래대금
    currency_unit: str(), // 거래통화
    hst_trdprc: num(), // 전일종가
    capital_amt: num(), // 자본금
    base_prc: num(), // 기준가
    eps_date: str(), // EPS일자
    eps_prc: num(), // EPS
    per_prc: num(), // PER
    trading_unit: num(), // 매매단위
    hst_acvol: num(), // 전일거래량
    trade_date: str(), // 거래일자
    exch_id: str(), // 거래소ID
    exch_name: str(), // 거래소명
    com_kind: str(), // 자산구분코드
    com_kind_name: str(), // 자산구분명
    pf_jgubun: str(), // (PF)장구분
    pf_trdprc: num(), // (PF)현재가
    pf_netchng_cls: str(), // (PF)전일대비구분
    pf_netchng: num(), // (PF)전일대비
    pf_pctchng: num(), // (PF)전일대비율
    best_ask6: num(), // 매도6호가
    best_bid6: num(), // 매수6호가
    best_asiz6: num(), // 매도6호가수량
    best_bsiz6: num(), // 매수6호가수량
    best_ask7: num(), // 매도7호가
    best_bid7: num(), // 매수7호가
    best_asiz7: num(), // 매도7호가수량
    best_bsiz7: num(), // 매수7호가수량
    best_ask8: num(), // 매도8호가
    best_bid8: num(), // 매수8호가
    best_asiz8: num(), // 매도8호가수량
    best_bsiz8: num(), // 매수8호가수량
    best_ask9: num(), // 매도9호가
    best_bid9: num(), // 매수9호가
    best_asiz9: num(), // 매도9호가수량
    best_bsiz9: num(), // 매수9호가수량
    best_ask10: num(), // 매도10호가
    best_bid10: num(), // 매수10호가
    best_asiz10: num(), // 매도10호가수량
    best_bsiz10: num(), // 매수10호가수량
    marketperiod_cls: str(), // 현재시장구분
    normal_trdprc: num(), // 정규장종가
    normal_netchng_cls: str(), // 정규장대비구분 / 2.상승 3.보합 5.하락
    normal_netchng: num(), // 정규장전일대비
    normal_pctchng: num(), // 정규장전일대비율
    normal_acvol: num(), // 정규장누적거래량
    normal_open_prc: num(), // 정규장시가
    normal_high: num(), // 정규장고가
    normal_low: num(), // 정규장저가
  })
  .passthrough();

/**
 * 해외주식 현재가상세 (`POST /gbstock/quote/v1/current`) 응답.
 *
 * 응답 블록: `Output_0`: 객체
 */
export const overseasStockQuoteCurrentPriceResponseSchema = z
  .object({
    ...envelope,
    /** 해외주식 현재가상세 조회 결과 */
    Output_0: overseasStockQuoteCurrentPriceOutputSchema.nullish(),
  })
  .passthrough();

// ── 해외주식 체결추이 조회 결과 (`Output_0`) 항목. ──

export const overseasStockQuoteExecutionTrendOutputSchema = z
  .object({
    iem_cd: str(), // 종목코드
    trade_date: str(), // 체결일자 / YYYYMMDD
    trade_time: str(), // 체결시간 / HHMMSS
    trdprc: num(), // 체결가
    netchng_cls: str(), // 전일대비구분 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)
    netchng: num(), // 전일대비가
    pctchng: num(), // 전일대비율
    turnover: num(), // 거래대금
    fill_size: num(), // 변동량
    acvol: num(), // 체결량
    open_prc: num(), // 시가
    high: num(), // 고가
    low: num(), // 저가
    best_ask1: num(), // 매도1호가
    best_bid1: num(), // 매수1호가
    cont_rate: num(), // 당일체결강도
    nextbutton: str(), // NEXTBUTTON
    ctsz18: str(), // CTSz18
  })
  .passthrough();

/**
 * 해외주식 체결추이 (`POST /gbstock/quote/v1/executionTrend`) 응답.
 *
 * 응답 블록: `Output_0`: 배열
 */
export const overseasStockQuoteExecutionTrendResponseSchema = z
  .object({
    ...envelope,
    /** 해외주식 체결추이 조회 결과 */
    Output_0: z.array(overseasStockQuoteExecutionTrendOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 기간별시세(개별종목) 조회 결과 (`Output_0`) 항목. ──

export const overseasStockQuotePeriodPriceOutputSchema = z
  .object({
    date: str(), // 조회날짜 / YYYYMMDD
    time: str(), // 조회시간 / HHMMSS
    iem_cd: str(), // 종목코드
    kor_name: str(), // 종목명 / 스펙상 필드 (실서버는 iem_nm 로 내려준다)
    iem_nm: str(), // 종목명 / 실서버 실측 필드 (2026-08-22 운영 확인)
    trdprc: num(), // 현재가
    netchng_cls: str(), // 등락부호 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)
    netchng: num(), // 대비
    pctchng: num(), // 대비율
    acvol: num(), // 거래량
    turnover: num(), // 거래대금
    open_prc: num(), // 시가
    high: num(), // 고가
    low: num(), // 저가
    per: num(), // PER
    pbr: num(), // PBR
    eps: num(), // EPS
    list_num: num(), // 상장주수
    list_amt: num(), // 시가총액
    hst_open_prc: num(), // 전일시가
    hst_high: num(), // 전일고가
    hst_low: num(), // 전일저가
    hst_trdprc: num(), // 전일종가
    hst_acvol: num(), // 전일거래량
    hst_acvol_rate: num(), // 전일거래량대비
    best_ask: num(), // 매도호가
    best_bid: num(), // 매수호가
    week_open_prc: num(), // 이번주시가
    week_high: num(), // 이번주고가
    week_low: num(), // 이번주저가
    mon_open_prc: num(), // 이번달시가
    mon_high: num(), // 이번달고가
    mon_low: num(), // 이번달저가
    market_start_time: str(), // 장시작시간 / HHMMSS
    market_end_time: str(), // 장마감시간 / HHMMSS
    bsop_date: str(), // 영업일 / YYYYMMDD
    fx_rate: num(), // 환율
    trading_cls: str(), // 실시간구분
    decimal: str(), // 소수점
    base_prc: num(), // 기준가
    ctsz16: str(), // 검색키
    tick_cnt: str(), // 마지막틱봉갯수
    count: str(), // 조회건수
    marketperiod_cls: str(), // 현재시장구분
    r_base_prc: num(), // 직전정규장기준가
  })
  .passthrough();

// ── 해외주식 기간별시세(개별종목) 조회 결과 (`Output_1`) 항목. ──

export const overseasStockQuotePeriodPriceVolumeOutputSchema = z
  .object({
    trade_date: str(), // 체결일자 / YYYYMMDD
    trade_time: str(), // 체결시간 / HHmmSS
    open_prc: num(), // 시가
    high: num(), // 고가
    low: num(), // 저가
    close_prc: num(), // 종가
    movolume: num(), // 변동거래량
    movalue: num(), // 변동거래대금
    netchng_cls: str(), // 등락부호 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)
    bsop_date: str(), // 영업일 / YYYYMMDD
  })
  .passthrough();

/**
 * 해외주식 기간별시세(개별종목) (`POST /gbstock/quote/v1/period`) 응답.
 *
 * 응답 블록: `Output_0`: 배열, `Output_1`: 배열
 */
export const overseasStockQuotePeriodPriceResponseSchema = z
  .object({
    ...envelope,
    /** 해외주식 기간별시세(개별종목) 조회 결과 */
    Output_0: z.array(overseasStockQuotePeriodPriceOutputSchema).nullish(),
    /** 해외주식 기간별시세(개별종목) 변동거래량 조회 결과 */
    Output_1: z.array(overseasStockQuotePeriodPriceVolumeOutputSchema).nullish(),
  })
  .passthrough();

// ── 해외주식 기간별시세(지수·환율) 조회 결과 (`Output_0`). ──

export const overseasStockQuoteSymbolIndexFxPeriodOutputSchema = z
  .object({
    qry_date: str(), // 조회날짜 / YYYYMMDD
    qry_time: str(), // 조회시간 / HHMMSS
    data_code: str(), // 해외종목타입
    iem_cd: str(), // SYMBOL
    hts_kor_isnm: str(), // 종목명 / 스펙상 필드 (실서버는 iem_nm 로 내려준다)
    iem_nm: str(), // 종목명 / 실서버 실측 필드 (2026-08-22 운영 확인)
    ovrs_prpr: num(), // 현재가
    prdy_vrss_sign: str(), // 등락부호 / 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세)
    prdy_vrss: num(), // 대비
    prdy_ctrt: num(), // 대비율
    acml_vol: num(), // 거래량
    acml_tr_pbmn: num(), // 거래대금
    prdy_clpr: num(), // 전일종가
    ovrs_oprc: num(), // 시가
    ovrs_hgpr: num(), // 고가
    ovrs_lwpr: num(), // 저가
    prdy_oprc: num(), // 전일시가
    prdy_hgpr: num(), // 전일고가
    prdy_lwpr: num(), // 전일저가
    prdy_prpr: num(), // 전일종가
    tdw_ovrs_oprc: num(), // 이번주시가
    tdw_ovrs_hgpr: num(), // 이번주고가
    tdw_ovrs_lwpr: num(), // 이번주저가
    tdm_ovrs_oprc: num(), // 이번달시가
    tdm_ovrs_hgpr: num(), // 이번달고가
    tdm_ovrs_lwpr: num(), // 이번달저가
    localtime: str(), // 현지시간
    bsop_date: str(), // 영업일
    base_ptr: str(), // 소수점자리수
    ctsz30: str(), // 이전키
    lasttickcount: str(), // 마지막N틱봉의틱묶음갯수
    send_cnt: str(), // 전송레코드건수
  })
  .passthrough();

// ── 해외주식 기간별시세(지수·환율) 조회 결과 (`Output_1`) 항목. ──

export const overseasStockQuoteSymbolIndexFxPeriodBarOutputSchema = z
  .object({
    bsop_date: str(), // 영업일
    bsop_time: str(), // 시간 / HHmmSS
    ovrs_oprc: num(), // 시가
    ovrs_hgpr: num(), // 고가
    ovrs_lwpr: num(), // 저가
    ovrs_prpr: num(), // 현재가
    vol: num(), // 거래량
  })
  .passthrough();

/**
 * 해외주식 기간별시세(지수·환율) (`POST /gbstock/quote/v1/symbolIndexFxPeriod`) 응답.
 *
 * 응답 블록: `Output_0`: 객체, `Output_1`: 배열
 */
export const overseasStockQuoteSymbolIndexFxPeriodResponseSchema = z
  .object({
    ...envelope,
    /** 해외주식 기간별시세(지수·환율) 조회 결과 */
    Output_0: overseasStockQuoteSymbolIndexFxPeriodOutputSchema.nullish(),
    /** 해외주식 기간별시세(지수·환율) 시세 목록 */
    Output_1: z.array(overseasStockQuoteSymbolIndexFxPeriodBarOutputSchema).nullish(),
  })
  .passthrough();

// ── Response Types ──

/** 해외주식 현재가상세 (`POST /gbstock/quote/v1/current`) 응답. — `Output_0`: 객체 */
export type OverseasStockQuoteCurrentPriceResponse = CamelizeKeys<
  z.infer<typeof overseasStockQuoteCurrentPriceResponseSchema>
>;
/** 해외주식 체결추이 (`POST /gbstock/quote/v1/executionTrend`) 응답. — `Output_0`: 배열 */
export type OverseasStockQuoteExecutionTrendResponse = CamelizeKeys<
  z.infer<typeof overseasStockQuoteExecutionTrendResponseSchema>
>;
/** 해외주식 기간별시세(개별종목) (`POST /gbstock/quote/v1/period`) 응답. — `Output_0`: 배열, `Output_1`: 배열 */
export type OverseasStockQuotePeriodPriceResponse = CamelizeKeys<
  z.infer<typeof overseasStockQuotePeriodPriceResponseSchema>
>;
/** 해외주식 기간별시세(지수·환율) (`POST /gbstock/quote/v1/symbolIndexFxPeriod`) 응답. — `Output_0`: 객체, `Output_1`: 배열 */
export type OverseasStockQuoteSymbolIndexFxPeriodResponse = CamelizeKeys<
  z.infer<typeof overseasStockQuoteSymbolIndexFxPeriodResponseSchema>
>;

// ── Response Map ──

export interface OverseasStockQuoteResponseMap {
  current: OverseasStockQuoteCurrentPriceResponse;
  executionTrend: OverseasStockQuoteExecutionTrendResponse;
  period: OverseasStockQuotePeriodPriceResponse;
  symbolIndexFxPeriod: OverseasStockQuoteSymbolIndexFxPeriodResponse;
}
