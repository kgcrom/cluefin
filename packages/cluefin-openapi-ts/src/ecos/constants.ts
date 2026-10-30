import type { EcosCycle } from './types.js';

/**
 * 자주 쓰는 ECOS 통계표·항목코드 (2026-10-17 dartrail 실측 코드에서 옮김, Python `ecos/_constants.py` 와 같다).
 *
 * 금리는 연 % 원문("4.182")으로 온다. 비율 변환·반올림은 쓰는 쪽에서 한다.
 */
export interface EcosSeries {
  readonly statCode: string;
  readonly cycle: EcosCycle;
  readonly itemCode: string;
  readonly name: string;
}

const series = (statCode: string, cycle: EcosCycle, itemCode: string, name: string): EcosSeries =>
  Object.freeze({ statCode, cycle, itemCode, name });

// 시장금리(일별) 817Y002
export const KTB_1Y = series('817Y002', 'D', '010190000', '국고채(1년)');
export const KTB_3Y = series('817Y002', 'D', '010200000', '국고채(3년)');
export const KTB_5Y = series('817Y002', 'D', '010200001', '국고채(5년)');
export const KTB_10Y = series('817Y002', 'D', '010210000', '국고채(10년)');
export const KTB_20Y = series('817Y002', 'D', '010220000', '국고채(20년)');
export const KTB_30Y = series('817Y002', 'D', '010230000', '국고채(30년)');
export const MSB_91D = series('817Y002', 'D', '010400000', '통안증권(91일)');
export const CD_91D = series('817Y002', 'D', '010502000', 'CD(91일)');
export const CORP_BOND_3Y_AA_MINUS = series('817Y002', 'D', '010300000', '회사채(3년, AA-)');
export const CORP_BOND_3Y_BBB_MINUS = series('817Y002', 'D', '010320000', '회사채(3년, BBB-)');

// 주요국 통화의 대원화환율 731Y001
export const USD_KRW = series('731Y001', 'D', '0000001', '원/미국달러(매매기준율)');

// 소비자물가지수(2020=100) 901Y009 — 작성: 국가데이터처
export const CPI_TOTAL = series('901Y009', 'M', '0', '소비자물가지수 총지수');

export const MARKET_RATES: readonly EcosSeries[] = Object.freeze([
  KTB_1Y,
  KTB_3Y,
  KTB_5Y,
  KTB_10Y,
  KTB_20Y,
  KTB_30Y,
  MSB_91D,
  CD_91D,
  CORP_BOND_3Y_AA_MINUS,
  CORP_BOND_3Y_BBB_MINUS,
]);
