import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';

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

/** 주식현재가 시세 종합 정보 (Output_0). */
export const krStockQuoteCurrentPriceOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
    /** 거래비율 */
    vol_rate: num.nullish(),
    /** 유동주회전율 */
    move_rate: num.nullish(),
    /** 거래대금 */
    acml_tr_pbmn: num.nullish(),
    /** 상한가 */
    stck_mxpr: num.nullish(),
    /** 고가 */
    stck_hgpr: num.nullish(),
    /** 시가 */
    stck_oprc: num.nullish(),
    /** 시가대비부호 */
    stck_oprc_sign: z.string().nullish(),
    /** 시가대비등락폭 */
    stck_oprc_vrss: num.nullish(),
    /** 저가 */
    stck_lwpr: num.nullish(),
    /** 하한가 */
    stck_llam: num.nullish(),
    /** 호가시간 */
    hoga_bsop_hour: z.string().nullish(),
    /** 매도호가1 */
    askp1: num.nullish(),
    /** 매도호가2 */
    askp2: num.nullish(),
    /** 매도호가3 */
    askp3: num.nullish(),
    /** 매도호가4 */
    askp4: num.nullish(),
    /** 매도호가5 */
    askp5: num.nullish(),
    /** 매도호가6 */
    askp6: num.nullish(),
    /** 매도호가7 */
    askp7: num.nullish(),
    /** 매도호가8 */
    askp8: num.nullish(),
    /** 매도호가9 */
    askp9: num.nullish(),
    /** 매도호가10 */
    askp10: num.nullish(),
    /** 매수호가1 */
    bidp1: num.nullish(),
    /** 매수호가2 */
    bidp2: num.nullish(),
    /** 매수호가3 */
    bidp3: num.nullish(),
    /** 매수호가4 */
    bidp4: num.nullish(),
    /** 매수호가5 */
    bidp5: num.nullish(),
    /** 매수호가6 */
    bidp6: num.nullish(),
    /** 매수호가7 */
    bidp7: num.nullish(),
    /** 매수호가8 */
    bidp8: num.nullish(),
    /** 매수호가9 */
    bidp9: num.nullish(),
    /** 매수호가10 */
    bidp10: num.nullish(),
    /** 매도호가잔량1 */
    askp_rsqn1: num.nullish(),
    /** 매도호가잔량2 */
    askp_rsqn2: num.nullish(),
    /** 매도호가잔량3 */
    askp_rsqn3: num.nullish(),
    /** 매도호가잔량4 */
    askp_rsqn4: num.nullish(),
    /** 매도호가잔량5 */
    askp_rsqn5: num.nullish(),
    /** 매도호가잔량6 */
    askp_rsqn6: num.nullish(),
    /** 매도호가잔량7 */
    askp_rsqn7: num.nullish(),
    /** 매도호가잔량8 */
    askp_rsqn8: num.nullish(),
    /** 매도호가잔량9 */
    askp_rsqn9: num.nullish(),
    /** 매도호가잔량10 */
    askp_rsqn10: num.nullish(),
    /** 매수호가잔량1 */
    bidp_rsqn1: num.nullish(),
    /** 매수호가잔량2 */
    bidp_rsqn2: num.nullish(),
    /** 매수호가잔량3 */
    bidp_rsqn3: num.nullish(),
    /** 매수호가잔량4 */
    bidp_rsqn4: num.nullish(),
    /** 매수호가잔량5 */
    bidp_rsqn5: num.nullish(),
    /** 매수호가잔량6 */
    bidp_rsqn6: num.nullish(),
    /** 매수호가잔량7 */
    bidp_rsqn7: num.nullish(),
    /** 매수호가잔량8 */
    bidp_rsqn8: num.nullish(),
    /** 매수호가잔량9 */
    bidp_rsqn9: num.nullish(),
    /** 매수호가잔량10 */
    bidp_rsqn10: num.nullish(),
    /** 총매도잔량 */
    total_askp_rsqn: num.nullish(),
    /** 총매수잔량 */
    total_bidp_rsqn: num.nullish(),
    /** 시간외매도잔량 */
    ovtm_askp_rsqn: num.nullish(),
    /** 시간외매수잔량 */
    ovtm_bidp_rsqn: num.nullish(),
    /** 피봇2차저항 */
    pvt_scnd_dmrs: num.nullish(),
    /** 피봇1차저항 */
    pvt_frst_dmrs: num.nullish(),
    /** 피봇가 */
    pvt_pont_val: num.nullish(),
    /** 피봇1차지지 */
    pvt_frst_dmsp: num.nullish(),
    /** 피봇2차지지 */
    pvt_scnd_dmsp: num.nullish(),
    /** 코스피코스닥구분 */
    mrkt_div_isnm: z.string().nullish(),
    /** 업종명 */
    bstp_kor_isnm: z.string().nullish(),
    /** 업종코드 */
    bstp_cls_code: z.string().nullish(),
    /** 자본금규모 */
    avls_scal_isnm: z.string().nullish(),
    /** 결산월 */
    stac_month: z.string().nullish(),
    /** 시장조치1 */
    market1: z.string().nullish(),
    /** 시장조치2 */
    market2: z.string().nullish(),
    /** 시장조치3 */
    market3: z.string().nullish(),
    /** 시장조치4 */
    market4: z.string().nullish(),
    /** 시장조치5 */
    market5: z.string().nullish(),
    /** 시장조치6 */
    market6: z.string().nullish(),
    /** CB구분 */
    cb_text: z.string().nullish(),
    /** 액면가 */
    stck_fcam: num.nullish(),
    /** 전일종가타이틀 */
    prdy_clpr_title: z.string().nullish(),
    /** 전일종가 */
    stck_prdy_clpr: num.nullish(),
    /** 대용가 */
    stck_sspr: num.nullish(),
    /** 공모가 */
    gongprice: num.nullish(),
    /** 5일고가 */
    d5_hgpr: num.nullish(),
    /** 5일저가 */
    d5_lwpr: num.nullish(),
    /** 20일고가 */
    d20_hgpr: num.nullish(),
    /** 20일저가 */
    d20_lwpr: num.nullish(),
    /** 52주최고가 */
    w52_hgpr: num.nullish(),
    /** 52주최고가일 */
    w52_hgpr_date: z.string().nullish(),
    /** 52주최저가 */
    w52_lwpr: num.nullish(),
    /** 52주최저가일 */
    w52_lwpr_date: z.string().nullish(),
    /** 유동주식수 */
    move_stcn: num.nullish(),
    /** 상장주식수 */
    lstn_stcn_unit3: num.nullish(),
    /** 시가총액 */
    hts_avls: num.nullish(),
    /** 시간 */
    memb_bsop_hour: z.string().nullish(),
    /** 매도거래원1 */
    seln_mbcr_name1: z.string().nullish(),
    /** 매수거래원1 */
    shnu_mbcr_name1: z.string().nullish(),
    /** 매도거래량1 */
    seln_qty1: num.nullish(),
    /** 매수거래량1 */
    shnu_qty1: num.nullish(),
    /** 매도거래원2 */
    seln_mbcr_name2: z.string().nullish(),
    /** 매수거래원2 */
    shnu_mbcr_name2: z.string().nullish(),
    /** 매도거래량2 */
    seln_qty2: num.nullish(),
    /** 매수거래량2 */
    shnu_qty2: num.nullish(),
    /** 매도거래원3 */
    seln_mbcr_name3: z.string().nullish(),
    /** 매수거래원3 */
    shnu_mbcr_name3: z.string().nullish(),
    /** 매도거래량3 */
    seln_qty3: num.nullish(),
    /** 매수거래량3 */
    shnu_qty3: num.nullish(),
    /** 매도거래원4 */
    seln_mbcr_name4: z.string().nullish(),
    /** 매수거래원4 */
    shnu_mbcr_name4: z.string().nullish(),
    /** 매도거래량4 */
    seln_qty4: num.nullish(),
    /** 매수거래량4 */
    shnu_qty4: num.nullish(),
    /** 매도거래원5 */
    seln_mbcr_name5: z.string().nullish(),
    /** 매수거래원5 */
    shnu_mbcr_name5: z.string().nullish(),
    /** 매도거래량5 */
    seln_qty5: num.nullish(),
    /** 매수거래량5 */
    shnu_qty5: num.nullish(),
    /** 매도외국인거래량 */
    glob_seln_qty: num.nullish(),
    /** 매수외국인거래량 */
    glob_shnu_qty: num.nullish(),
    /** 외국인시간 */
    for_hour: z.string().nullish(),
    /** 외국인지분율 */
    for_rate: num.nullish(),
    /** 결제일 */
    crdt_stlm_date: z.string().nullish(),
    /** 잔고비율(%) */
    crdt_rmnd_rate: num.nullish(),
    /** 유상기준일 */
    yu_date: z.string().nullish(),
    /** 무상기준일 */
    mu_date: z.string().nullish(),
    /** 유상배정비율 */
    yu_rate: num.nullish(),
    /** 무상배정비율 */
    mu_rate: num.nullish(),
    /** 외국인변동주수 */
    frgn_ntby_vol: num.nullish(),
    /** 자사주 */
    jasa: z.string().nullish(),
    /** 상장일 */
    stck_lstn_date: z.string().nullish(),
    /** 대주주지분율 */
    dae_rate: num.nullish(),
    /** 대주주지분일자 */
    dae_date: z.string().nullish(),
    /** FILLER */
    filler: z.string().nullish(),
    /** 증거금율 */
    deposit_gb: z.string().nullish(),
    /** 자본금 */
    cpfn: num.nullish(),
    /** 전체거래원매도합 */
    total_seln_qty: num.nullish(),
    /** 전체거래원매수합 */
    total_shnu_qty: num.nullish(),
    /** 우회상장여부 */
    detour_gb: z.string().nullish(),
    /** 증권구분 */
    scrt_grp_isnm: z.string().nullish(),
    /** 공여율기준일 */
    crdt_deal_date: z.string().nullish(),
    /** 공여율(%) */
    crdt_loan_gvrt: num.nullish(),
    /** PER */
    per: num.nullish(),
    /** 종목별신용한도 */
    hando_gb: z.string().nullish(),
    /** 가중가 */
    wghn_avrg_prc: num.nullish(),
    /** 상장주식수_주 */
    lstn_stcn_unit0: num.nullish(),
    /** 추가상장주수 */
    add_lstn_stcn: num.nullish(),
    /** 종목comment */
    gicomment: z.string().nullish(),
    /** 전일거래량 */
    prdy_vol: num.nullish(),
    /** 전일대비등락부호 */
    pre_prdy_sign: z.string().nullish(),
    /** 전일대비등락폭 */
    pre_prdy_vrss: num.nullish(),
    /** 연종최고가 */
    stck_dryy_hgpr: num.nullish(),
    /** 연중최고가일 */
    dryy_hgpr_date: z.string().nullish(),
    /** 연중최저가 */
    stck_dryy_lwpr: num.nullish(),
    /** 연중최저가일 */
    dryy_lwpr_date: z.string().nullish(),
    /** 외국인보유주식수 */
    frgn_hldn_qty: num.nullish(),
    /** 외국인한도율(%) */
    issu_limt_rate: num.nullish(),
    /** 매매수량단위 */
    frml_mrkt_unit: num.nullish(),
    /** 경쟁대량방향구분 */
    comp_cls_code: z.string().nullish(),
    /** 대량매매구분 */
    largem_gb: z.string().nullish(),
    /** PBR */
    pbr: num.nullish(),
    /** 디저항값 */
    dmrs_val: num.nullish(),
    /** 디지지값 */
    dmsp_val: num.nullish(),
    /** 전일거래대금 */
    prdy_tr_pbmn: num.nullish(),
    /** VI기준가 */
    vi_antc_sdpr: num.nullish(),
    /** VI상승발동가 */
    vi_antc_mxpr: num.nullish(),
    /** VI하락발동가 */
    vi_antc_llam: num.nullish(),
    /** 투자유의종목여부 */
    invt_epmd_yn: z.string().nullish(),
    /** 상한수량 */
    uplm_qty: num.nullish(),
    /** 단기과열구분코드 — 1.단기과열예고 2.단기과열지정 3.단기과열연장 */
    short_over_code: z.string().nullish(),
    /** 투자주의경고구분코드 — 1.투자주의 2.투자경고 3.투자주의>투자위험예고 4.투자경고투자위험예고 5.투자위험 */
    mrkt_alrm_code: z.string().nullish(),
    /** 정리매매여부 — Y.정리매매종목 */
    sltr_yn: z.string().nullish(),
    /** 담보유지비율(%) */
    crd_rt_grd_nm: z.string().nullish(),
    /** 중간가 */
    mid_prc: num.nullish(),
    /** 매도중간가잔량합계수량 */
    midp_total_askp_rsqn: num.nullish(),
    /** 매수중간가잔량합계수량 */
    midp_total_bidp_rsqn: num.nullish(),
    /** nxt중간가 */
    nxt_mid_prc: num.nullish(),
    /** nxt매도중간가잔량합계수량 */
    nxt_midp_total_askp_rsqn: num.nullish(),
    /** nxt매수중간가잔량합계수량 */
    nxt_midp_total_bidp_rsqn: num.nullish(),
    /** 증거금등급구분코드 */
    marg_grad_cls_code: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시세 시간대별 체결 (Output_1 배열의 각 항목). */
export const krStockQuoteCurrentPriceTickOutputSchema = z
  .object({
    /** 시간 */
    bsop_hour: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 변동거래량 */
    cntg_vol: z.union([z.string(), num]).nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
  })
  .passthrough();

/** 주식현재가 시세 예상체결/ECN 정보 (Output_2). */
export const krStockQuoteCurrentPriceExpectedOutputSchema = z
  .object({
    /** 동시호가구분 — 1.동시호가 이외 정규시장 */
    cncc_aspr_code: z.string().nullish(),
    /** 예상체결가 */
    antc_cnpr: z.union([z.string(), num, num]).nullish(),
    /** 예상체결부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    antc_cntg_sign: z.string().nullish(),
    /** 예상체결등락폭 */
    antc_cntg_vrss: z.union([z.string(), num, num]).nullish(),
    /** 예상체결등락률 */
    antc_prdy_ctrt: z.union([z.string(), num, num]).nullish(),
    /** 예상체결수량 */
    antc_vol: z.union([z.string(), num, num]).nullish(),
    /** ECN정보유무구분 */
    chkdata: z.string().nullish(),
    /** ECN전일종가 */
    ovtm_untp_prpr: z.union([z.string(), num, num]).nullish(),
    /** ECN부호 */
    ovtm_untp_sign: z.string().nullish(),
    /** ECN등락폭 */
    ovtm_untp_vrss: z.union([z.string(), num, num]).nullish(),
    /** ECN등락률 */
    ovtm_untp_ctrt: z.union([z.string(), num, num]).nullish(),
    /** ECN체결수량 */
    ovtm_untp_vol: z.union([z.string(), num, num]).nullish(),
    /** ECN대비예상체결부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    ovtm_antc_sign: z.string().nullish(),
    /** ECN대비예상체결등락폭 */
    ovtm_antc_vrss: z.union([z.string(), num, num]).nullish(),
    /** ECN대비예상체결등락률 */
    ovtm_antc_ctrt: z.union([z.string(), num, num]).nullish(),
    /** 종합스코어링 */
    scoring: z.union([z.string(), num, num]).nullish(),
    /** VI거래중지여부 — 1.VI발동 N.그외 */
    vi_type_code: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시세 (`POST /krstock/quote/v1/currentPrice`) 응답. */
export const krStockQuoteCurrentPriceResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 현재가 종합 정보 */
    Output_0: krStockQuoteCurrentPriceOutputSchema.nullish(),
    /** 시간대별 체결 목록 */
    Output_1: z.array(krStockQuoteCurrentPriceTickOutputSchema).nullish(),
    /** 예상체결/ECN 정보 (스펙은 Array, 실제 예시는 Object — 둘 다 허용) */
    Output_2: z
      .union([z.array(krStockQuoteCurrentPriceExpectedOutputSchema), krStockQuoteCurrentPriceExpectedOutputSchema])
      .nullish(),
  })
  .passthrough();

/** 주식현재가 체결 시간대별 체결 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteCurrentExecutionTickOutputSchema = z
  .object({
    /** 시간 */
    bsop_hour: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 변동거래량 */
    cntg_vol: num.nullish(),
    /** 누적매수체결량 */
    shnu_cntg_smtn: num.nullish(),
    /** 당일매수비중 */
    bidrate: num.nullish(),
    /** 누적매도체결량 */
    seln_cntg_smtn: num.nullish(),
    /** 당일매도비중 */
    askrate: num.nullish(),
    /** 누적보합체결량 */
    stnr_cntg_smtn: num.nullish(),
    /** 당일보합비중 */
    uncrate: num.nullish(),
    /** 체결강도 */
    cttr: num.nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 전체거래량 */
    acml_vol: num.nullish(),
    /** filler */
    filler: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 체결 종목 종합 정보 (Output_1). */
export const krStockQuoteCurrentExecutionSummaryOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** KOR_종목명 */
    iem_nm: z.string().nullish(),
    /** 누적매도가체결량 */
    toffervol: z.union([z.string(), num]).nullish(),
    /** 누적매수가체결량 */
    tbidvol: z.union([z.string(), num]).nullish(),
    /** 누적보합가체결량 */
    tbovol: z.union([z.string(), num]).nullish(),
    /** 누적매도가체결건수 */
    toffersu: z.union([z.string(), num]).nullish(),
    /** 누적매수가체결건수 */
    tbidsu: z.union([z.string(), num]).nullish(),
    /** 누적보합가체결건수 */
    tbosu: z.union([z.string(), num]).nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 전체거래량 */
    acml_vol: num.nullish(),
    /** 시가 */
    stck_oprc: z.union([z.string(), num]).nullish(),
    /** 고가 */
    stck_hgpr: z.union([z.string(), num]).nullish(),
    /** 저가 */
    stck_lwpr: z.union([z.string(), num]).nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 체결강도 */
    cttr: num.nullish(),
    /** 신규거래량 */
    new_volume: z.union([z.string(), num]).nullish(),
    /** 전일종가 — 기준가 혹은 전일종가 기준가 우선 셋팅 */
    stck_prdy_clpr: z.union([z.string(), num]).nullish(),
    /** filler */
    filler: z.string().nullish(),
    /** CTSz20 */
    ctsz20: z.string().nullish(),
    /** NEXTBUTTON */
    nextbutton: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 체결 (`POST /krstock/quote/v1/currentExecution`) 응답. */
export const krStockQuoteCurrentExecutionResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 시간대별 체결 상세 목록 */
    Output_0: z.array(krStockQuoteCurrentExecutionTickOutputSchema).nullish(),
    /** 종목 종합 정보 */
    Output_1: krStockQuoteCurrentExecutionSummaryOutputSchema.nullish(),
  })
  .passthrough();

/** 주식현재가 일자별 일별 시세 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteCurrentDailyOutputSchema = z
  .object({
    /** 일자 — YY/MM/DD */
    bsop_date: z.string().nullish(),
    /** 시가 */
    stck_oprc: z.union([z.string(), num]).nullish(),
    /** 고가 */
    stck_hgpr: z.union([z.string(), num]).nullish(),
    /** 저가 */
    stck_lwpr: z.union([z.string(), num]).nullish(),
    /** 종가 */
    stck_clpr: z.union([z.string(), num]).nullish(),
    /** FILLER */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: z.union([z.string(), num]).nullish(),
    /** 등락률 */
    prdy_ctrt: z.union([z.string(), num]).nullish(),
    /** 거래량 */
    acml_vol: z.union([z.string(), num]).nullish(),
    /** 거래대금 */
    acml_tr_pbmn: z.union([z.string(), num]).nullish(),
    /** 고가일 */
    high_date: z.string().nullish(),
    /** 저가일 */
    low_date: z.string().nullish(),
    /** 거래량전일비 */
    vol_prdy_rt: z.union([z.string(), num]).nullish(),
    /** 체결강도 */
    cttr: z.union([z.string(), num]).nullish(),
    /** FILLER */
    filler: z.string().nullish(),
    /** NEXT_KEY */
    next_key: z.string().nullish(),
    /** NEXTBUTTON */
    nextbutton: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 일자별 (`POST /krstock/quote/v1/currentDaily`) 응답. */
export const krStockQuoteCurrentDailyResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 일별 시세 상세 목록 */
    Output_0: z.array(krStockQuoteCurrentDailyOutputSchema).nullish(),
  })
  .passthrough();

/** 주식현재가 투자자 투자자별 거래현황 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteCurrentInvestorOutputSchema = z
  .object({
    /** 거래일자 — YYYYMMDD */
    bsop_date1: z.string().nullish(),
    /** 거래일자 — YYMMDD00 */
    bsop_date2: z.string().nullish(),
    /** 종가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
    /** 외국인지분율 */
    for_rate: num.nullish(),
    /** 외국인순매수량 */
    frgn_ntby_qty: num.nullish(),
    /** 개인투자자순매수량 */
    person: num.nullish(),
    /** 기관계투자자순매수량 */
    gigwan: num.nullish(),
    /** 외국인투자자순매수량 */
    invest: num.nullish(),
    /** 거래원순매수량 */
    account: num.nullish(),
    /** 프로그램 */
    program: num.nullish(),
    /** 자사주 */
    jasaz10: z.string().nullish(),
    /** FILLER */
    filler: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 투자자 (`POST /krstock/quote/v1/currentInvestor`) 응답. */
export const krStockQuoteCurrentInvestorResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 투자자별 거래현황 상세 목록 */
    Output_0: z.array(krStockQuoteCurrentInvestorOutputSchema).nullish(),
  })
  .passthrough();

/** 국내주식기간별시세(일/주/월/년) 종합 정보 (Output_0). */
export const krStockQuotePeriodOutputSchema = z
  .object({
    /** 조회날짜 — YYYYMMDD */
    qry_date: z.string().nullish(),
    /** 조회시간 — HHmmSS */
    qry_time: z.string().nullish(),
    /** 단축종목코드 */
    iem_cd: z.string().nullish(),
    /** 한글종목명 */
    iem_nm: z.string().nullish(),
    /** 현재가 */
    stck_prpr: z.string().nullish(),
    /** 전일대비부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 전일대비 */
    prdy_vrss: z.string().nullish(),
    /** 전일대비율 — float 5.2 */
    prdy_ctrt: z.string().nullish(),
    /** 누적거래량 */
    acml_vol: z.string().nullish(),
    /** 누적거래대금 */
    acml_tr_pbmn: z.string().nullish(),
    /** 전일거래량 */
    prdy_vol: z.string().nullish(),
    /** 거래량전일비 — float 15.2 */
    prdy_vol_rate: z.string().nullish(),
    /** 거래량회전율 — float 10.5 */
    vol_rate: z.string().nullish(),
    /** 체결강도 — float 6.2 */
    cttr: z.string().nullish(),
    /** 전일체결강도 — float 6.2 */
    prdy_cttr: z.string().nullish(),
    /** 매도호가 */
    askp: z.string().nullish(),
    /** 매수호가 */
    bidp: z.string().nullish(),
    /** 매도1호가잔량 */
    askp_rsqn1: z.string().nullish(),
    /** 매수1호가잔량 */
    bidp_rsqn1: z.string().nullish(),
    /** 상한가 */
    stck_mxpr: z.string().nullish(),
    /** 하한가 */
    stck_llam: z.string().nullish(),
    /** 시가 */
    stck_oprc: z.string().nullish(),
    /** 고가 */
    stck_hgpr: z.string().nullish(),
    /** 저가 */
    stck_lwpr: z.string().nullish(),
    /** 상장주수 */
    lstn_stcn: z.string().nullish(),
    /** 시가총액 — 억단위 */
    hts_avls: z.string().nullish(),
    /** 대주주지분율 — float 5.2 */
    dae_rate: z.string().nullish(),
    /** PER — float 5.2 */
    per: z.string().nullish(),
    /** PBR — float 5.2 */
    pbr: z.string().nullish(),
    /** EPS */
    eps: z.string().nullish(),
    /** BPS */
    bps: z.string().nullish(),
    /** 전일시가 */
    prdy_oprc: z.string().nullish(),
    /** 전일고가 */
    prdy_high: z.string().nullish(),
    /** 전일저가 */
    prdy_low: z.string().nullish(),
    /** 전일종가 */
    prdy_clpr: z.string().nullish(),
    /** 이번주시가 */
    tdw_oprc: z.string().nullish(),
    /** 이번주고가 */
    tdw_high: z.string().nullish(),
    /** 이번주저가 */
    tdw_low: z.string().nullish(),
    /** 이번달시가 */
    tdm_oprc: z.string().nullish(),
    /** 이번달고가 */
    tdm_high: z.string().nullish(),
    /** 이번달저가 */
    tdm_low: z.string().nullish(),
    /** VI정적발동상승 */
    vi_sttc_mxpr: z.string().nullish(),
    /** VI정적발동하락 */
    vi_sttc_llam: z.string().nullish(),
    /** 장시작시간 — HHmmSS */
    start_time: z.string().nullish(),
    /** 장마감시간 — HHmmSS */
    end_time: z.string().nullish(),
    /** 영업일 */
    bsop_date: z.string().nullish(),
    /** 주식기준가 */
    stck_sdpr: z.string().nullish(),
    /** 주식액면가 */
    stck_fcam: z.string().nullish(),
    /** 업종한글명 */
    bstp_kor_isnm: z.string().nullish(),
    /** 업종코드 */
    bstp_cls_code: z.string().nullish(),
    /** 달러환율 */
    exchange_prpr: z.string().nullish(),
    /** 연속조회키 */
    ctsz30: z.string().nullish(),
    /** 마지막N틱봉의틱묶음갯수 — 최근봉마지막틱갯수 */
    lasttickcount: z.string().nullish(),
    /** 전송레코드건수 */
    send_cnt: z.string().nullish(),
    /** 프리마켓시작시간 — NXT/UNT프리마켓시작시간 */
    pre_tr_sta_hour: z.string().nullish(),
    /** 프리마켓종료시간 — NXT/UNT프리마켓종료시간 */
    pre_tr_fin_hour: z.string().nullish(),
    /** 메인마겟시작시간 — NXT/UNT메인마켓시작시간 */
    main_tr_sta_hour: z.string().nullish(),
    /** 메인마겟종료시간 — NXT/UNT메인마켓종료시간 */
    main_tr_fin_hour: z.string().nullish(),
    /** 에프터마겟시작시간 — NXT/UNT에프터마켓시작시간 */
    aft_tr_sta_hour: z.string().nullish(),
    /** 에프터마겟종료시간 — NXT/UNT에프터마켓종료시간 */
    aft_tr_fin_hour: z.string().nullish(),
    /** 정규장마감전동시호가 — KRX/UNT종료전동시호가시작시간 */
    cncc_aspr_sta_hour: z.string().nullish(),
  })
  .passthrough();

/** 국내주식기간별시세(일/주/월/년) 주기별 봉 상세 (Output_1 배열의 각 항목). */
export const krStockQuotePeriodBarOutputSchema = z
  .object({
    /** 영업일 */
    bsop_date: z.string().nullish(),
    /** 시간 — HHmmSS */
    bsop_time: z.string().nullish(),
    /** 주식기준가 */
    stck_sdpr: z.string().nullish(),
    /** 시가 */
    stck_oprc: z.string().nullish(),
    /** 고가 */
    stck_hgpr: z.string().nullish(),
    /** 저가 */
    stck_lwpr: z.string().nullish(),
    /** 현재가 */
    stck_prpr: z.string().nullish(),
    /** 거래량 */
    vol: z.string().nullish(),
    /** 거래대금 */
    tr_pbmn: z.string().nullish(),
    /** 락구분코드 — 01.권리락 02.배당락 03.분배락 04.권배락 05.중간배당락 06.권리중간배당락 07.권리분기배당락 99.기타 */
    flng_cls_code: z.string().nullish(),
    /** 락비율 — float 8.2 */
    prtt_rate: z.string().nullish(),
    /** 뉴스건수 — 일간일때만처리 */
    news_cnt: z.string().nullish(),
    /** 상하한가표시 — 0.기본 1.상한 4.하한 */
    updownmark: z.string().nullish(),
    /** 액면가변경구분코드 — 00.해당없음 01.액면분할 02.액면병합 03.주식분할 04.주식병합 99.기타 */
    fcam_mod_cls_code: z.string().nullish(),
    /** 거래량수정비율 */
    vol_prtt_rate: z.string().nullish(),
  })
  .passthrough();

/** 국내주식기간별시세(일/주/월/년) (`POST /krstock/quote/v1/period`) 응답. */
export const krStockQuotePeriodResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 종합 정보 (스펙은 Array, 실제 예시는 Object — 둘 다 허용) */
    Output_0: z.union([z.array(krStockQuotePeriodOutputSchema), krStockQuotePeriodOutputSchema]).nullish(),
    /** 주기별 봉 상세 목록 */
    Output_1: z.array(krStockQuotePeriodBarOutputSchema).nullish(),
  })
  .passthrough();

/** 국내주식 시간외현재가 시간외 단일가 종합 정보 (Output_0). */
export const krStockQuoteAfterHoursCurrentOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 시장구분 */
    mrkt_cls_code: z.string().nullish(),
    /** 거래구분 */
    trht_yn: z.string().nullish(),
    /** 장구분 */
    mkop_cls_code: z.string().nullish(),
    /** 정규장종가 */
    stck_prpr: num.nullish(),
    /** 기준가 */
    ovtm_untp_sdpr: num.nullish(),
    /** 상한가 */
    ovtm_untp_mxpr: num.nullish(),
    /** 하한가 */
    ovtm_untp_llam: num.nullish(),
    /** 체결시간 */
    ovtm_cntg_hour: z.string().nullish(),
    /** 체결가 */
    ovtm_untp_prpr: num.nullish(),
    /** 체결등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 체결등락폭 */
    ovtm_prdy_vrss: num.nullish(),
    /** 체결등락률 */
    ovtm_prdy_ctrt: num.nullish(),
    /** 시가 */
    ovtm_untp_oprc: num.nullish(),
    /** 고가 */
    ovtm_untp_hgpr: num.nullish(),
    /** 저가 */
    ovtm_untp_lwpr: num.nullish(),
    /** 거래량 */
    ovtm_untp_vol: num.nullish(),
    /** 거래대금 */
    ovtm_tr_pbmn: num.nullish(),
    /** 매도호가 */
    ovtm_untp_askp: num.nullish(),
    /** 매수호가 */
    ovtm_untp_bidp: num.nullish(),
    /** 호가시간 */
    ovtm_bsop_hour: z.string().nullish(),
    /** 매도1차선호가 */
    ovtm_untp_askp1: num.nullish(),
    /** 매도2차선호가 */
    ovtm_untp_askp2: num.nullish(),
    /** 매도3차선호가 */
    ovtm_untp_askp3: num.nullish(),
    /** 매도4차선호가 */
    ovtm_untp_askp4: num.nullish(),
    /** 매도5차선호가 */
    ovtm_untp_askp5: num.nullish(),
    /** 매도6차선호가 */
    ovtm_untp_askp6: num.nullish(),
    /** 매도7차선호가 */
    ovtm_untp_askp7: num.nullish(),
    /** 매도8차선호가 */
    ovtm_untp_askp8: num.nullish(),
    /** 매도9차선호가 */
    ovtm_untp_askp9: num.nullish(),
    /** 매도10차선호가 */
    ovtm_untp_askp10: num.nullish(),
    /** 매수1차선호가 */
    ovtm_untp_bidp1: num.nullish(),
    /** 매수2차선호가 */
    ovtm_untp_bidp2: num.nullish(),
    /** 매수3차선호가 */
    ovtm_untp_bidp3: num.nullish(),
    /** 매수4차선호가 */
    ovtm_untp_bidp4: num.nullish(),
    /** 매수5차선호가 */
    ovtm_untp_bidp5: num.nullish(),
    /** 매수6차선호가 */
    ovtm_untp_bidp6: num.nullish(),
    /** 매수7차선호가 */
    ovtm_untp_bidp7: num.nullish(),
    /** 매수8차선호가 */
    ovtm_untp_bidp8: num.nullish(),
    /** 매수9차선호가 */
    ovtm_untp_bidp9: num.nullish(),
    /** 매수10차선호가 */
    ovtm_untp_bidp10: num.nullish(),
    /** 매도1차선잔량 */
    ovtm_askp_rsqn1: num.nullish(),
    /** 매도2차선잔량 */
    ovtm_askp_rsqn2: num.nullish(),
    /** 매도3차선잔량 */
    ovtm_askp_rsqn3: num.nullish(),
    /** 매도4차선잔량 */
    ovtm_askp_rsqn4: num.nullish(),
    /** 매도5차선잔량 */
    ovtm_askp_rsqn5: num.nullish(),
    /** 매도6차선잔량 */
    ovtm_askp_rsqn6: num.nullish(),
    /** 매도7차선잔량 */
    ovtm_askp_rsqn7: num.nullish(),
    /** 매도8차선잔량 */
    ovtm_askp_rsqn8: num.nullish(),
    /** 매도9차선잔량 */
    ovtm_askp_rsqn9: num.nullish(),
    /** 매도10차선잔량 */
    ovtm_askp_rsqn10: num.nullish(),
    /** 매수1차선잔량 */
    ovtm_bidp_rsqn1: num.nullish(),
    /** 매수2차선잔량 */
    ovtm_bidp_rsqn2: num.nullish(),
    /** 매수3차선잔량 */
    ovtm_bidp_rsqn3: num.nullish(),
    /** 매수4차선잔량 */
    ovtm_bidp_rsqn4: num.nullish(),
    /** 매수5차선잔량 */
    ovtm_bidp_rsqn5: num.nullish(),
    /** 매수6차선잔량 */
    ovtm_bidp_rsqn6: num.nullish(),
    /** 매수7차선잔량 */
    ovtm_bidp_rsqn7: num.nullish(),
    /** 매수8차선잔량 */
    ovtm_bidp_rsqn8: num.nullish(),
    /** 매수9차선잔량 */
    ovtm_bidp_rsqn9: num.nullish(),
    /** 매수10차선잔량 */
    ovtm_bidp_rsqn10: num.nullish(),
    /** 매도잔량합 */
    total_askp_rsqn: num.nullish(),
    /** 매수잔량합 */
    total_bidp_rsqn: num.nullish(),
    /** 동시구분 — 1.동시호가 이외 정규시장 */
    ecn_dongsi: z.string().nullish(),
    /** 예상체결가 */
    ovtm_antc_cnpr: num.nullish(),
    /** 예상체결부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    antc_vrss_sign: z.string().nullish(),
    /** 예상체결등락폭 */
    antc_cntg_vrss: num.nullish(),
    /** 예상체결등락률 */
    antc_cntg_ctrt: num.nullish(),
    /** 예상체결수량 */
    antc_vol: num.nullish(),
    /** 예상대금 */
    antc_tr_pbmn: num.nullish(),
    /** 종목정보 */
    item_info: z.string().nullish(),
    /** 투자유의종목여부 — Y.투자유의종목 */
    ivs_hed_yn: z.string().nullish(),
    /** 단기과열구분코드 — 1.단기과열예고 2.단기과열지정 3.단기과열연장 */
    short_ovh_gb: z.string().nullish(),
    /** 투자주의경고구분코드 — 1.투자주의 2.투자경고 3.투자주의>투자위험예고 4.투자경고투자위험예고 5.투자위험 */
    alert_gb: z.string().nullish(),
    /** 정리매매여부 — Y.정리매매종목 */
    jungri_yn: z.string().nullish(),
  })
  .passthrough();

/** 국내주식 시간외현재가 정규장 종합 정보 (Output_1). */
export const krStockQuoteAfterHoursCurrentRegularOutputSchema = z
  .object({
    /** 일자 */
    bsop_date: z.string().nullish(),
    /** 거래량 */
    acml_vol: z.union([z.string(), num]).nullish(),
    /** 거래량전일비 */
    vol_rate: z.union([z.string(), num]).nullish(),
    /** 거래대금 */
    acml_tr_pbmn: z.union([z.string(), num]).nullish(),
    /** 시가 */
    stck_oprc: z.union([z.string(), num]).nullish(),
    /** 고가 */
    stck_hgpr: z.union([z.string(), num]).nullish(),
    /** 저가 */
    stck_lwpr: z.union([z.string(), num]).nullish(),
    /** 정규장종가 */
    stck_prpr: num.nullish(),
    /** 상한가 */
    stck_mxpr: z.union([z.string(), num]).nullish(),
    /** 하한가 */
    stck_llam: z.union([z.string(), num]).nullish(),
    /** 액면가 */
    stck_fcam: z.union([z.string(), num]).nullish(),
    /** 매도호가 */
    askp: z.union([z.string(), num]).nullish(),
    /** 매수호가 */
    bidp: z.union([z.string(), num]).nullish(),
    /** 매도잔량 */
    askp_rsqn: z.union([z.string(), num]).nullish(),
    /** 매수잔량 */
    bidp_rsqn: z.union([z.string(), num]).nullish(),
    /** 매도잔량합 */
    total_askp_rsqn: num.nullish(),
    /** 매수잔량합 */
    total_bidp_rsqn: num.nullish(),
    /** 시간외매도잔량 */
    ovtm_askp_rsqn: z.union([z.string(), num]).nullish(),
    /** 시간외매수잔량 */
    ovtm_bidp_rsqn: z.union([z.string(), num]).nullish(),
    /** 외국인시간 */
    frgn_hour: z.string().nullish(),
    /** 외국인지분율 */
    for_rate: z.union([z.string(), num]).nullish(),
    /** 체결등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: z.union([z.string(), num]).nullish(),
    /** 등락률 */
    prdy_ctrt: z.union([z.string(), num]).nullish(),
    /** 코스피구분 */
    sosokz6: z.string().nullish(),
    /** 업종명 */
    bstp_kor_isnm: z.string().nullish(),
    /** 업종코드 */
    bstp_cls_code: z.string().nullish(),
    /** 자본금규모 */
    cap_size: z.string().nullish(),
    /** 신규거래량 */
    new_volume: z.union([z.string(), num]).nullish(),
  })
  .passthrough();

/** 국내주식 시간외현재가 (`POST /krstock/quote/v1/afterHoursCurrent`) 응답. */
export const krStockQuoteAfterHoursCurrentResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 시간외 단일가 종합 정보 */
    Output_0: krStockQuoteAfterHoursCurrentOutputSchema.nullish(),
    /** 정규장 종합 정보 */
    Output_1: krStockQuoteAfterHoursCurrentRegularOutputSchema.nullish(),
  })
  .passthrough();

/** 주식현재가 시간외일자별주가 시간외 체결 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteCurrentAfterHoursDailyTickOutputSchema = z
  .object({
    /** 일자 */
    qry_date: z.string().nullish(),
    /** 시가 */
    qry_time: z.string().nullish(),
    /** 고가 */
    shrn_iscd: z.string().nullish(),
    /** 저가 */
    hts_kor_isnm: z.string().nullish(),
    /** 락구분 */
    stck_prpr: z.string().nullish(),
    /** Filler */
    prdy_vrss_sign: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시간외일자별주가 종합 상세 (Output_1 배열의 각 항목). */
export const krStockQuoteCurrentAfterHoursDailyOutputSchema = z
  .object({
    /** 현재가 */
    prdy_ctrt: z.string().nullish(),
    /** 거래량 */
    acml_vol: z.union([z.string(), num]).nullish(),
    /** 거래대금 */
    acml_tr_pbmn: z.union([z.string(), num]).nullish(),
    /** Filler */
    prdy_vol: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시간외일자별주가 (`POST /krstock/quote/v1/currentAfterHoursDaily`) 응답. */
export const krStockQuoteCurrentAfterHoursDailyResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 시간외 체결 상세 목록 */
    Output_0: z.array(krStockQuoteCurrentAfterHoursDailyTickOutputSchema).nullish(),
    /** 종합 상세 목록 */
    Output_1: z.array(krStockQuoteCurrentAfterHoursDailyOutputSchema).nullish(),
  })
  .passthrough();

/** 주식현재가 시간외시간별체결 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteCurrentAfterHoursExecutionOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 시간 */
    bsop_hour: z.string().nullish(),
    /** 시가 */
    open: num.nullish(),
    /** 고가 */
    high: num.nullish(),
    /** 저가 */
    low: num.nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
    /** 변동거래량 */
    cntg_vol: num.nullish(),
    /** 거래대금 */
    cntg_tr_pbmn: num.nullish(),
    /** 매도호가 */
    askp1: num.nullish(),
    /** 매수호가 */
    bidp1: num.nullish(),
    /** Filler */
    filler: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시간외시간별체결 (`POST /krstock/quote/v1/currentAfterHoursExecution`) 응답. */
export const krStockQuoteCurrentAfterHoursExecutionResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 시간외 시간별 체결 상세 목록 */
    Output_0: z.array(krStockQuoteCurrentAfterHoursExecutionOutputSchema).nullish(),
  })
  .passthrough();

/** 주식현재가 시간외시간별예상 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteAfterHoursExpectedOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 시간 */
    bsop_hour: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 거래량 */
    cntg_vol: num.nullish(),
    /** 매도호가 */
    askp1: num.nullish(),
    /** 매수호가 */
    bidp1: num.nullish(),
    /** 매도잔량 */
    askp_rsqn1: num.nullish(),
    /** 매수잔량 */
    bidp_rsqn1: num.nullish(),
    /** Filler */
    filler: z.string().nullish(),
  })
  .passthrough();

/** 주식현재가 시간외시간별예상 (`POST /krstock/quote/v1/afterHoursExpected`) 응답. */
export const krStockQuoteAfterHoursExpectedResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 시간외 시간별 예상체결 상세 목록 */
    Output_0: z.array(krStockQuoteAfterHoursExpectedOutputSchema).nullish(),
  })
  .passthrough();

/** ETF/ETN 현재가 종합 정보 (Output_0). */
export const krStockQuoteEtfCurrentOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
    /** 거래비율 */
    acml_rate: num.nullish(),
    /** 유동주회전율 */
    yu_rate: num.nullish(),
    /** 거래대금 */
    acml_tr_pbmn: num.nullish(),
    /** 상한가 */
    stck_mxpr: num.nullish(),
    /** 고가 */
    stck_hgpr: num.nullish(),
    /** 시가 */
    stck_oprc: num.nullish(),
    /** 시가대비부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    oprc_sign: z.string().nullish(),
    /** 시가대비등락폭 */
    oprc_vrss: num.nullish(),
    /** 저가 */
    stck_lwpr: num.nullish(),
    /** 하한가 */
    stck_llam: num.nullish(),
    /** 호가시간 */
    bsop_hour: z.string().nullish(),
    /** 매도1호가 */
    askp1: num.nullish(),
    /** 매도2호가 */
    askp2: num.nullish(),
    /** 매도3호가 */
    askp3: num.nullish(),
    /** 매도4호가 */
    askp4: num.nullish(),
    /** 매도5호가 */
    askp5: num.nullish(),
    /** 매도6호가 */
    askp6: num.nullish(),
    /** 매도7호가 */
    askp7: num.nullish(),
    /** 매도8호가 */
    askp8: num.nullish(),
    /** 매도9호가 */
    askp9: num.nullish(),
    /** 매도10호가 */
    askp10: num.nullish(),
    /** 매수1호가 */
    bidp1: num.nullish(),
    /** 매수2호가 */
    bidp2: num.nullish(),
    /** 매수3호가 */
    bidp3: num.nullish(),
    /** 매수4호가 */
    bidp4: num.nullish(),
    /** 매수5호가 */
    bidp5: num.nullish(),
    /** 매수6호가 */
    bidp6: num.nullish(),
    /** 매수7호가 */
    bidp7: num.nullish(),
    /** 매수8호가 */
    bidp8: num.nullish(),
    /** 매수9호가 */
    bidp9: num.nullish(),
    /** 매수10호가 */
    bidp10: num.nullish(),
    /** 매도1호가잔량 */
    askp_rsqn1: num.nullish(),
    /** 매도2호가잔량 */
    askp_rsqn2: num.nullish(),
    /** 매도3호가잔량 */
    askp_rsqn3: num.nullish(),
    /** 매도4호가잔량 */
    askp_rsqn4: num.nullish(),
    /** 매도5호가잔량 */
    askp_rsqn5: num.nullish(),
    /** 매도6호가잔량 */
    askp_rsqn6: num.nullish(),
    /** 매도7호가잔량 */
    askp_rsqn7: num.nullish(),
    /** 매도8호가잔량 */
    askp_rsqn8: num.nullish(),
    /** 매도9호가잔량 */
    askp_rsqn9: num.nullish(),
    /** 매도10호가잔량 */
    askp_rsqn10: num.nullish(),
    /** 매수1호가잔량 */
    bidp_rsqn1: num.nullish(),
    /** 매수2호가잔량 */
    bidp_rsqn2: num.nullish(),
    /** 매수3호가잔량 */
    bidp_rsqn3: num.nullish(),
    /** 매수4호가잔량 */
    bidp_rsqn4: num.nullish(),
    /** 매수5호가잔량 */
    bidp_rsqn5: num.nullish(),
    /** 매수6호가잔량 */
    bidp_rsqn6: num.nullish(),
    /** 매수7호가잔량 */
    bidp_rsqn7: num.nullish(),
    /** 매수8호가잔량 */
    bidp_rsqn8: num.nullish(),
    /** 매수9호가잔량 */
    bidp_rsqn9: num.nullish(),
    /** 매수10호가잔량 */
    bidp_rsqn10: num.nullish(),
    /** 총매도호가잔량 */
    total_askp_rsqn: num.nullish(),
    /** 총매수호가잔량 */
    total_bidp_rsqn: num.nullish(),
    /** 시간외매도잔량 */
    ovtm_askp_rsqn: num.nullish(),
    /** 시간외매수잔량 */
    ovtm_bidp_rsqn: num.nullish(),
    /** 피벗2차저항 */
    pvt_scnd_dmrs: num.nullish(),
    /** 피벗1차저항 */
    pvt_frst_dmrs: num.nullish(),
    /** 피벗가 */
    pvt_pont_val: num.nullish(),
    /** 피벗1차지지 */
    pvt_frst_dmsp: num.nullish(),
    /** 피벗2차지지 */
    pvt_scnd_dmsp: num.nullish(),
    /** 코스닥코스피구분 */
    mrkt_div_code: z.string().nullish(),
    /** 지수코드 */
    bstp_cls_code: z.string().nullish(),
    /** 업종명 */
    bstp_kor_isnm: z.string().nullish(),
    /** 자본금규모 */
    cap_size: z.string().nullish(),
    /** 결산월 */
    stac_month: z.string().nullish(),
    /** 시장조치1 */
    market1: z.string().nullish(),
    /** 시장조치2 */
    market2: z.string().nullish(),
    /** 시장조치3 */
    market3: z.string().nullish(),
    /** 시장조치4 */
    market4: z.string().nullish(),
    /** 시장조치5 */
    market5: z.string().nullish(),
    /** 시장조치6 */
    market6: z.string().nullish(),
    /** CB구분 */
    cb_text: z.string().nullish(),
    /** 액면가 */
    stck_fcam: num.nullish(),
    /** 전일종가타이틀 */
    prdy_clpr_title: z.string().nullish(),
    /** 전일종가 */
    prdy_clpr: num.nullish(),
    /** 대용가 */
    stck_sspr: num.nullish(),
    /** 공모가 */
    gongprice: num.nullish(),
    /** 5일고가 */
    d5_hgpr: num.nullish(),
    /** 5일저가 */
    d5_lwpr: num.nullish(),
    /** 20일고가 */
    d20_hgpr: num.nullish(),
    /** 20일저가 */
    d20_lwpr: num.nullish(),
    /** 52주최고가 */
    w52_hgpr: num.nullish(),
    /** 52주최저가 */
    w52_lwpr: num.nullish(),
    /** 유동주식수 */
    move_stcn: num.nullish(),
    /** 상장주식수_천주 */
    lstn_stcn1: num.nullish(),
    /** 시가총액 */
    hts_avls: num.nullish(),
    /** 시간 */
    cntg_hour: z.string().nullish(),
    /** 매도거래원1 */
    seln_mbcr_no1: z.string().nullish(),
    /** 매수거래원1 */
    shnu_mbcr_no1: z.string().nullish(),
    /** 매도거래량1 */
    seln_acml_vol1: num.nullish(),
    /** 매수거래량1 */
    shnu_acml_vol1: num.nullish(),
    /** 매도거래원2 */
    seln_mbcr_no2: z.string().nullish(),
    /** 매수거래원2 */
    shnu_mbcr_no2: z.string().nullish(),
    /** 매도거래량2 */
    seln_acml_vol2: num.nullish(),
    /** 매수거래량2 */
    shnu_acml_vol2: num.nullish(),
    /** 매도거래원3 */
    seln_mbcr_no3: z.string().nullish(),
    /** 매수거래원3 */
    shnu_mbcr_no3: z.string().nullish(),
    /** 매도거래량3 */
    seln_acml_vol3: num.nullish(),
    /** 매수거래량3 */
    shnu_acml_vol3: num.nullish(),
    /** 매도거래원4 */
    seln_mbcr_no4: z.string().nullish(),
    /** 매수거래원4 */
    shnu_mbcr_no4: z.string().nullish(),
    /** 매도거래량4 */
    seln_acml_vol4: num.nullish(),
    /** 매수거래량4 */
    shnu_acml_vol4: num.nullish(),
    /** 매도거래원5 */
    seln_mbcr_no5: z.string().nullish(),
    /** 매수거래원5 */
    shnu_mbcr_no5: z.string().nullish(),
    /** 매도거래량5 */
    seln_acml_vol5: num.nullish(),
    /** 매수거래량5 */
    shnu_acml_vol5: num.nullish(),
    /** 매도외국인거래량 */
    seln_frgn_vol: num.nullish(),
    /** 매수외국인거래량 */
    shnu_frgn_vol: num.nullish(),
    /** 외국인시간 */
    frgn_hour: z.string().nullish(),
    /** 외국인지분율 */
    for_rate: num.nullish(),
    /** 결제일 */
    settdate: z.string().nullish(),
    /** 잔고비율(%) */
    crate: num.nullish(),
    /** 유상기준일 */
    yudate: z.string().nullish(),
    /** 무상기준일 */
    mudate: z.string().nullish(),
    /** 유상배정비율 */
    yurate: num.nullish(),
    /** 무상배정비율 */
    murate: num.nullish(),
    /** 상장일 */
    lstn_date: z.string().nullish(),
    /** 상장주식수_주 */
    lstn_stcn: num.nullish(),
    /** 전체거래원매도합 */
    total_seln_qty: num.nullish(),
    /** 전체거래원매수합 */
    total_shnu_qty: num.nullish(),
    /** 신규거래량 */
    new_volume: num.nullish(),
  })
  .passthrough();

/** ETF/ETN 시간대별 체결 상세 (Output_1 배열의 각 항목). */
export const krStockQuoteEtfCurrentTickOutputSchema = z
  .object({
    /** 호가시간 */
    bsop_hour: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 매도호가 */
    askp: num.nullish(),
    /** 매수호가 */
    bidp: num.nullish(),
    /** 변동거래량 */
    cntg_vol: z.union([z.string(), num]).nullish(),
    /** 거래량 */
    acml_vol: num.nullish(),
  })
  .passthrough();

/** ETF/ETN 예상체결 정보 (Output_2). */
export const krStockQuoteEtfCurrentExpectedOutputSchema = z
  .object({
    /** 동시호가구분 — 1.동시호가 이외 정규시장 */
    aspr_cls_code: z.string().nullish(),
    /** 예상체결가 */
    antc_cnpr: z.union([z.string(), num]).nullish(),
    /** 예상체결부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    antc_sign: z.string().nullish(),
    /** 예상체결등락폭 */
    antc_vrss: z.union([z.string(), num]).nullish(),
    /** 예상체결등락률 */
    antc_ctrt: z.union([z.string(), num]).nullish(),
    /** 예상체결수량 */
    antc_vol: z.union([z.string(), num]).nullish(),
  })
  .passthrough();

/** ETF/ETN NAV·괴리율·LP 잔량 상세 (Output_3, 공식 스펙 문서에는 없고 예시 응답에만 존재). */
export const krStockQuoteEtfCurrentNavOutputSchema = z
  .object({
    /** ETF구분 */
    bu12: z.string().nullish(),
    /** 장중/최종NAV */
    itmt_last_nav: z.union([z.string(), num]).nullish(),
    /** NAV등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    nav_sign: z.string().nullish(),
    /** NAV등락폭 */
    nav_vrss: z.union([z.string(), num]).nullish(),
    /** 전일NAV */
    prdy_last_nav: z.union([z.string(), num]).nullish(),
    /** 괴리율 */
    dprt: z.union([z.string(), num]).nullish(),
    /** 괴리율부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    dprt_sign: z.string().nullish(),
    /** 구성종목수 */
    cnfg_cnt: z.union([z.string(), num]).nullish(),
    /** 순자산총액(억원) */
    totvalue: z.union([z.string(), num]).nullish(),
    /** 추적오차율 */
    trc_errt: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량1 */
    lp_askp_rsqn1: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량2 */
    lp_askp_rsqn2: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량3 */
    lp_askp_rsqn3: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량4 */
    lp_askp_rsqn4: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량5 */
    lp_askp_rsqn5: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량6 */
    lp_askp_rsqn6: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량7 */
    lp_askp_rsqn7: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량8 */
    lp_askp_rsqn8: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량9 */
    lp_askp_rsqn9: z.union([z.string(), num]).nullish(),
    /** LP매도호가잔량10 */
    lp_askp_rsqn10: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량1 */
    lp_bidp_rsqn1: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량2 */
    lp_bidp_rsqn2: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량3 */
    lp_bidp_rsqn3: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량4 */
    lp_bidp_rsqn4: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량5 */
    lp_bidp_rsqn5: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량6 */
    lp_bidp_rsqn6: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량7 */
    lp_bidp_rsqn7: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량8 */
    lp_bidp_rsqn8: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량9 */
    lp_bidp_rsqn9: z.union([z.string(), num]).nullish(),
    /** LP매수호가잔량10 */
    lp_bidp_rsqn10: z.union([z.string(), num]).nullish(),
    /** ETF복제방법구분코드 */
    clon_cls_code: z.string().nullish(),
    /** ETF과세유형코드 */
    txtn_type_code: z.string().nullish(),
  })
  .passthrough();

/** ETF/ETN 기초지수 상세 (Output_4, 공식 스펙 문서에는 없고 예시 응답에만 존재). */
export const krStockQuoteEtfCurrentIndexOutputSchema = z
  .object({
    /** 지수코드 */
    bstp_cls_code: z.string().nullish(),
    /** 업종명 */
    bstp_kor_isnm: z.string().nullish(),
    /** 지수 */
    prpr_nmix: z.union([z.string(), num]).nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 — 길이 10 (스펙은 int 지만 실측은 소수부 있는 float) */
    prdy_vrss: num.nullish(),
    /** 채권지수코드 */
    ubjiid: z.string().nullish(),
    /** 채권지수세부코드 */
    ubjiid2: z.string().nullish(),
    /** 채권지수 */
    ubjisu: z.union([z.string(), num, num]).nullish(),
    /** 채권등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    ubsign: z.string().nullish(),
    /** 채권등락폭 */
    ubchange: z.union([z.string(), num, num]).nullish(),
    /** 해외지수심볼 */
    symbol: z.string().nullish(),
    /** 해외지수 */
    ovrs_nmix: z.union([z.string(), num, num]).nullish(),
    /** 해외지수등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    ovrs_sign: z.string().nullish(),
    /** 해외지수등락폭 */
    ovrs_vrss: z.union([z.string(), num, num]).nullish(),
    /** 지수거래소구분 — 1.코스피 2.코스닥 */
    jisukpgubun: z.string().nullish(),
  })
  .passthrough();

/** ETF/ETN 현재가 (`POST /krstock/quote/v1/etfCurrent`) 응답. */
export const krStockQuoteEtfCurrentResponseSchema = z
  .object({
    ...assetEnvelope,
    /** ETF/ETN 현재가 종합 정보 */
    Output_0: krStockQuoteEtfCurrentOutputSchema.nullish(),
    /** 시간대별 체결 상세 목록 */
    Output_1: z.array(krStockQuoteEtfCurrentTickOutputSchema).nullish(),
    /** 예상체결 정보 */
    Output_2: krStockQuoteEtfCurrentExpectedOutputSchema.nullish(),
    /** NAV·괴리율·LP 잔량 상세 (스펙 문서 미기재, 예시 응답에만 존재) */
    Output_3: krStockQuoteEtfCurrentNavOutputSchema.nullish(),
    /** 기초지수 상세 (스펙 문서 미기재, 예시 응답에만 존재) */
    Output_4: krStockQuoteEtfCurrentIndexOutputSchema.nullish(),
  })
  .passthrough();

/** ETF 구성종목시세 상세 (Output_0 배열의 각 항목). */
export const krStockQuoteEtfComponentsOutputSchema = z
  .object({
    /** 종목코드 */
    iem_cd: z.string().nullish(),
    /** 종목명 */
    iem_nm: z.string().nullish(),
    /** 현재가 */
    stck_prpr: num.nullish(),
    /** 등락부호 — 1or6.상한가 2or7.상승 3or0.보합 4or8.하한 5or9.하락 그외.보합+리버스(기세) */
    prdy_vrss_sign: z.string().nullish(),
    /** 등락폭 */
    prdy_vrss: num.nullish(),
    /** 등락률 */
    prdy_ctrt: num.nullish(),
    /** 1CU단위증권수(주) */
    cu_unit: num.nullish(),
    /** 평가금액2 */
    totprice: num.nullish(),
    /** 비중 */
    vol: num.nullish(),
    /** 평가금액 */
    vltn_amt: num.nullish(),
    /** Filler */
    filler: z.string().nullish(),
  })
  .passthrough();

/** ETF 구성종목시세 (`POST /krstock/quote/v1/etfComponents`) 응답. */
export const krStockQuoteEtfComponentsResponseSchema = z
  .object({
    ...assetEnvelope,
    /** 구성종목 상세 목록 */
    Output_0: z.array(krStockQuoteEtfComponentsOutputSchema).nullish(),
  })
  .passthrough();

// ── Response Types ──

export type KrStockQuoteCurrentPriceResponse = CamelizeKeys<z.infer<typeof krStockQuoteCurrentPriceResponseSchema>>;
export type KrStockQuoteCurrentExecutionResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteCurrentExecutionResponseSchema>
>;
export type KrStockQuoteCurrentDailyResponse = CamelizeKeys<z.infer<typeof krStockQuoteCurrentDailyResponseSchema>>;
export type KrStockQuoteCurrentInvestorResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteCurrentInvestorResponseSchema>
>;
export type KrStockQuotePeriodResponse = CamelizeKeys<z.infer<typeof krStockQuotePeriodResponseSchema>>;
export type KrStockQuoteAfterHoursCurrentResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteAfterHoursCurrentResponseSchema>
>;
export type KrStockQuoteCurrentAfterHoursDailyResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteCurrentAfterHoursDailyResponseSchema>
>;
export type KrStockQuoteCurrentAfterHoursExecutionResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteCurrentAfterHoursExecutionResponseSchema>
>;
export type KrStockQuoteAfterHoursExpectedResponse = CamelizeKeys<
  z.infer<typeof krStockQuoteAfterHoursExpectedResponseSchema>
>;
export type KrStockQuoteEtfCurrentResponse = CamelizeKeys<z.infer<typeof krStockQuoteEtfCurrentResponseSchema>>;
export type KrStockQuoteEtfComponentsResponse = CamelizeKeys<z.infer<typeof krStockQuoteEtfComponentsResponseSchema>>;

// ── Response Map ──

export interface KrstockQuoteResponseMap {
  currentPrice: KrStockQuoteCurrentPriceResponse;
  currentExecution: KrStockQuoteCurrentExecutionResponse;
  currentDaily: KrStockQuoteCurrentDailyResponse;
  currentInvestor: KrStockQuoteCurrentInvestorResponse;
  period: KrStockQuotePeriodResponse;
  afterHoursCurrent: KrStockQuoteAfterHoursCurrentResponse;
  currentAfterHoursDaily: KrStockQuoteCurrentAfterHoursDailyResponse;
  currentAfterHoursExecution: KrStockQuoteCurrentAfterHoursExecutionResponse;
  afterHoursExpected: KrStockQuoteAfterHoursExpectedResponse;
  etfCurrent: KrStockQuoteEtfCurrentResponse;
  etfComponents: KrStockQuoteEtfComponentsResponse;
}
