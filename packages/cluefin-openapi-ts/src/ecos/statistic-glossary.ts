import { z } from 'zod';

import type { EcosClient } from './client.js';
import { type EcosPage, type EcosPageOptions, ecosText } from './types.js';

/** StatisticWord 한 행 — 통계용어사전 항목. */
export const statisticWordSchema = z.looseObject({
  /** 용어 */
  word: ecosText,
  /** 용어설명 */
  content: ecosText.nullish(),
});

/** StatisticMeta 한 행 — 통계메타DB 의 트리 노드 하나. */
export const statisticMetaItemSchema = z.looseObject({
  /** 트리 깊이 (1부터, 문자열로 온다) */
  lvl: ecosText.nullish(),
  /** 상위통계항목코드 */
  pContCode: ecosText.nullish(),
  /** 통계항목코드 */
  contCode: ecosText,
  /** 통계항목명 */
  contName: ecosText,
  metaData: ecosText.nullish(),
});

export type StatisticWord = z.infer<typeof statisticWordSchema>;
export type StatisticMetaItem = z.infer<typeof statisticMetaItemSchema>;

export interface WordInput extends EcosPageOptions {
  /** 용어 (예: `소비자동향지수`) */
  term: string;
}

export interface MetaInput extends EcosPageOptions {
  /** 데이터명. 부분 일치한다(`경제심리` = `경제심리지수`, 2026-10-19 실측) */
  dataName: string;
}

/** 통계용어사전과 통계메타DB */
export class StatisticGlossary {
  public constructor(private readonly client: EcosClient) {}

  /** 통계용어사전 (OA-1060) */
  public async word(input: WordInput): Promise<EcosPage<StatisticWord>> {
    const { term, ...options } = input;
    return this.client.getRows('StatisticWord', [term], statisticWordSchema, options);
  }

  /** 통계메타DB (OA-1050) */
  public async meta(input: MetaInput): Promise<EcosPage<StatisticMetaItem>> {
    const { dataName, ...options } = input;
    return this.client.getRows('StatisticMeta', [dataName], statisticMetaItemSchema, options);
  }
}
