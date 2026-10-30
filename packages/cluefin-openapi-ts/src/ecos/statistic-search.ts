import { z } from 'zod';

import type { EcosClient } from './client.js';
import type { EcosSeries } from './constants.js';
import { type EcosCycle, type EcosLang, type EcosPage, type EcosPageOptions, ecosText } from './types.js';

const MAX_ITEM_CODES = 4;

/** StatisticSearch 한 행 — 통계표·항목·시점 하나의 값. 키는 와이어 이름의 camelCase. */
export const statisticObservationSchema = z.looseObject({
  /** 통계표코드 */
  statCode: ecosText,
  /** 통계명 */
  statName: ecosText,
  itemCode1: ecosText.nullish(),
  itemName1: ecosText.nullish(),
  itemCode2: ecosText.nullish(),
  itemName2: ecosText.nullish(),
  itemCode3: ecosText.nullish(),
  itemName3: ecosText.nullish(),
  itemCode4: ecosText.nullish(),
  itemName4: ecosText.nullish(),
  /** 단위 (연%, 원, 2020=100 …) */
  unitName: ecosText.nullish(),
  /** 가중치 (와이어 `WGT`) */
  wgt: ecosText.nullish(),
  /** 시점. 주기를 따른다: 2026, 2026Q3, 202609, 20261016 … */
  time: ecosText,
  /** 값 원문. 휴일·미집계면 빈 문자열 */
  dataValue: ecosText.nullish(),
});

export type StatisticObservation = z.infer<typeof statisticObservationSchema>;

export interface StatisticSearchInput extends EcosPageOptions {
  /** 통계표코드 (예: `817Y002` 시장금리(일별)) */
  statCode: string;
  cycle: EcosCycle;
  /** 검색시작일자. 주기 형식을 따른다 — 2015, 2015S1, 2015Q1, 201501, 201501S1, 20150101 */
  start: string;
  /** 검색종료일자 (형식은 start 와 같다) */
  end: string;
  /** 통계항목코드1~4. 생략하면 통계표의 모든 항목이 온다 */
  itemCodes?: readonly string[];
}

/** `dataValue` 를 숫자로. 비었거나 숫자가 아니면 null. */
export const parseEcosValue = (dataValue: string | null | undefined): number | null => {
  if (!dataValue?.trim()) {
    return null;
  }
  const value = Number(dataValue);
  return Number.isFinite(value) ? value : null;
};

/** 통계 조회 조건 설정 (OA-1040) */
export class StatisticSearch {
  public constructor(private readonly client: EcosClient) {}

  /** 통계표의 시계열 값을 받는다. 휴일에는 행이 없고, 데이터가 없으면 빈 rows. */
  public async search(input: StatisticSearchInput): Promise<EcosPage<StatisticObservation>> {
    const { statCode, cycle, start, end, itemCodes = [], ...options } = input;
    if (itemCodes.length > MAX_ITEM_CODES) {
      throw new RangeError(`항목코드는 ${MAX_ITEM_CODES}개까지입니다. 받은 개수: ${itemCodes.length}`);
    }
    return this.client.getRows(
      'StatisticSearch',
      [statCode, cycle, start, end, ...itemCodes],
      statisticObservationSchema,
      options,
    );
  }

  /** 상수 계열 하나(예: `KTB_10Y`)를 기간으로 받는다. */
  public searchSeries(
    series: EcosSeries,
    start: string,
    end: string,
    options: { lang?: EcosLang } = {},
  ): Promise<EcosPage<StatisticObservation>> {
    return this.search({
      statCode: series.statCode,
      cycle: series.cycle,
      start,
      end,
      itemCodes: [series.itemCode],
      ...options,
    });
  }
}
