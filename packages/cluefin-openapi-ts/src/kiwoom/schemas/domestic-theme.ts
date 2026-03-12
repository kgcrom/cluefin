import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka90001: 테마그룹 ──

export const themeGroupItemSchema = z
  .object({
    themaGrpCd: s(),
    themaNm: s(),
    stkNum: s(),
    fluSig: s(),
    fluRt: s(),
    risingStkNum: s(),
    fallStkNum: s(),
    dtPrftRt: s(),
    mainStk: s(),
  })
  .passthrough();

export const themeGroupResponseSchema = z
  .object({
    ...envelope,
    themaGrp: z.array(themeGroupItemSchema).default([]),
  })
  .passthrough();

// ── ka90002: 테마구성종목 ──

export const themeGroupStocksItemSchema = z
  .object({
    stkCd: s(),
    stkNm: s(),
    curPrc: s(),
    fluSig: s(),
    predPre: s(),
    fluRt: s(),
    accTrdeQty: s(),
    selBid: s(),
    selReq: s(),
    buyBid: s(),
    buyReq: s(),
    dtPrftRtN: s(),
  })
  .passthrough();

export const themeGroupStocksResponseSchema = z
  .object({
    ...envelope,
    fluRt: s(),
    dtPrftRt: s(),
    themaCompStk: z.array(themeGroupStocksItemSchema).default([]),
  })
  .passthrough();

// ── Response Types ──

export type ThemeGroupResponse = CamelizeKeys<z.infer<typeof themeGroupResponseSchema>>;
export type ThemeGroupStocksResponse = CamelizeKeys<z.infer<typeof themeGroupStocksResponseSchema>>;

// ── Response Map ──

export interface DomesticThemeResponseMap {
  getThemeGroup: ThemeGroupResponse;
  getThemeGroupStocks: ThemeGroupStocksResponse;
}
