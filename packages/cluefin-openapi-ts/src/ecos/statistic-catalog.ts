import { z } from 'zod';

import type { EcosClient } from './client.js';
import { type EcosPage, type EcosPageOptions, ecosCount, ecosText } from './types.js';

/** StatisticTableList 한 행 — 통계표 또는 그 상위 분류. */
export const statisticTableSchema = z.looseObject({
  /** 상위통계표코드. 최상위는 '*' */
  pStatCode: ecosText.nullish(),
  /** 통계표코드 (분류 행은 10자리 숫자) */
  statCode: ecosText,
  statName: ecosText,
  /** 주기 (A·S·Q·M·SM·D). 분류 행은 null */
  cycle: ecosText.nullish(),
  /** StatisticSearch 로 조회 가능 여부 Y/N */
  srchYn: ecosText.nullish(),
  /** 출처 */
  orgName: ecosText.nullish(),
});

/** StatisticItemList 한 행 — 통계표의 세부 항목. */
export const statisticItemSchema = z.looseObject({
  statCode: ecosText,
  statName: ecosText,
  /** 항목그룹코드 (Group1 → ITEM_CODE1 자리) */
  grpCode: ecosText.nullish(),
  grpName: ecosText.nullish(),
  /** 통계항목코드 — StatisticSearch 의 itemCodes 에 넣는 값 */
  itemCode: ecosText,
  itemName: ecosText,
  pItemCode: ecosText.nullish(),
  pItemName: ecosText.nullish(),
  cycle: ecosText.nullish(),
  /** 수록시작일자 */
  startTime: ecosText.nullish(),
  /** 수록종료일자 */
  endTime: ecosText.nullish(),
  /** 자료수 */
  dataCnt: ecosCount.nullish(),
  unitName: ecosText.nullish(),
  weight: ecosText.nullish(),
});

/** KeyStatisticList 한 행 — 100대 통계지표의 최근 값. */
export const keyStatisticSchema = z.looseObject({
  /** 통계그룹명 */
  className: ecosText,
  keystatName: ecosText,
  /** 값 원문 */
  dataValue: ecosText.nullish(),
  /** 최근 수록 시점 (202608, 20261019 …) */
  cycle: ecosText.nullish(),
  unitName: ecosText.nullish(),
});

export type StatisticTable = z.infer<typeof statisticTableSchema>;
export type StatisticItem = z.infer<typeof statisticItemSchema>;
export type KeyStatistic = z.infer<typeof keyStatisticSchema>;

export interface TableListInput extends EcosPageOptions {
  /** 통계표코드. 생략하면 분류 행까지 포함한 전체 목록(2026-10 기준 844행) */
  statCode?: string;
}

export interface ItemListInput extends EcosPageOptions {
  statCode: string;
}

/** 어떤 통계표·항목이 있는지 찾는 서비스들 */
export class StatisticCatalog {
  public constructor(private readonly client: EcosClient) {}

  /** 서비스 통계 목록 (OA-1020) */
  public async tableList(input: TableListInput = {}): Promise<EcosPage<StatisticTable>> {
    const { statCode, ...options } = input;
    return this.client.getRows('StatisticTableList', statCode ? [statCode] : [], statisticTableSchema, options);
  }

  /** 통계 세부항목 목록 (OA-1030). StatisticSearch 에 넣을 항목코드를 찾는 데 쓴다. */
  public async itemList(input: ItemListInput): Promise<EcosPage<StatisticItem>> {
    const { statCode, ...options } = input;
    return this.client.getRows('StatisticItemList', [statCode], statisticItemSchema, options);
  }

  /** 100대 통계지표 (OA-1010) — 지표마다 최근 값 하나. 행 순서는 호출마다 같다는 보장이 없다. */
  public async keyStatisticList(options: EcosPageOptions = {}): Promise<EcosPage<KeyStatistic>> {
    return this.client.getRows('KeyStatisticList', [], keyStatisticSchema, options);
  }
}
