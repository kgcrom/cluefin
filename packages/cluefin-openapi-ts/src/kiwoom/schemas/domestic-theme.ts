import { z } from 'zod';

import type { CamelizeKeys } from '../../core/types.js';

const s = () => z.string().default('');

const envelope = {
  return_code: z.union([z.string(), z.number()]).optional(),
  return_msg: z.string().optional(),
};

// ── ka90001: 테마그룹 ──

export const themeGroupItemSchema = z
  .object({
    thema_grp_cd: s(),
    thema_nm: s(),
    stk_num: s(),
    flu_sig: s(),
    flu_rt: s(),
    rising_stk_num: s(),
    fall_stk_num: s(),
    dt_prft_rt: s(),
    main_stk: s(),
  })
  .passthrough();

export const themeGroupResponseSchema = z
  .object({
    ...envelope,
    thema_grp: z.array(themeGroupItemSchema).default([]),
  })
  .passthrough();

// ── ka90002: 테마구성종목 ──

export const themeGroupStocksItemSchema = z
  .object({
    stk_cd: s(),
    stk_nm: s(),
    cur_prc: s(),
    flu_sig: s(),
    pred_pre: s(),
    flu_rt: s(),
    acc_trde_qty: s(),
    sel_bid: s(),
    sel_req: s(),
    buy_bid: s(),
    buy_req: s(),
    dt_prft_rt_n: s(),
  })
  .passthrough();

export const themeGroupStocksResponseSchema = z
  .object({
    ...envelope,
    flu_rt: s(),
    dt_prft_rt: s(),
    thema_comp_stk: z.array(themeGroupStocksItemSchema).default([]),
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
