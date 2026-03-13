import type { KiwoomEndpointDefinition } from '../../core/types';
import {
  individualStockInstitutionalChartResponseSchema,
  industryDailyResponseSchema,
  industryMinuteResponseSchema,
  industryMonthlyResponseSchema,
  industryTickResponseSchema,
  industryWeeklyResponseSchema,
  industryYearlyResponseSchema,
  intradayInvestorTradingResponseSchema,
  stockDailyResponseSchema,
  stockMinuteResponseSchema,
  stockMonthlyResponseSchema,
  stockTickResponseSchema,
  stockWeeklyResponseSchema,
  stockYearlyResponseSchema,
} from '../schemas/domestic-chart';

export const domesticChartEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getIndividualStockInstitutionalChart',
    responseSchema: individualStockInstitutionalChartResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10060',
    bodyMap: {
      dt: 'dt',
      stk_cd: 'stkCd',
      amt_qty_tp: 'amtQtyTp',
      trde_tp: 'trdeTp',
      unit_tp: 'unitTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'dt',
        required: true,
      },
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'amtQtyTp',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'unitTp',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIntradayInvestorTrading',
    responseSchema: intradayInvestorTradingResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10064',
    bodyMap: {
      stk_cd: 'stkCd',
      amt_qty_tp: 'amtQtyTp',
      trde_tp: 'trdeTp',
      mrkt_tp: 'mrktTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'amtQtyTp',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockTick',
    responseSchema: stockTickResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10079',
    bodyMap: {
      stk_cd: 'stkCd',
      tic_scope: 'ticScope',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'ticScope',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: false,
        defaultValue: '0',
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockMinute',
    responseSchema: stockMinuteResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10080',
    bodyMap: {
      stk_cd: 'stkCd',
      tic_scope: 'ticScope',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'ticScope',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: false,
        defaultValue: '0',
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockDaily',
    responseSchema: stockDailyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10081',
    bodyMap: {
      stk_cd: 'stkCd',
      base_dt: 'baseDt',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockWeekly',
    responseSchema: stockWeeklyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10082',
    bodyMap: {
      stk_cd: 'stkCd',
      base_dt: 'baseDt',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockMonthly',
    responseSchema: stockMonthlyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10083',
    bodyMap: {
      stk_cd: 'stkCd',
      base_dt: 'baseDt',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockYearly',
    responseSchema: stockYearlyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka10094',
    bodyMap: {
      stk_cd: 'stkCd',
      base_dt: 'baseDt',
      upd_stkpc_tp: 'updStkpcTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'updStkpcTp',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryTick',
    responseSchema: industryTickResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20004',
    bodyMap: {
      inds_cd: 'indsCd',
      tic_scope: 'ticScope',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'ticScope',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryMinute',
    responseSchema: industryMinuteResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20005',
    bodyMap: {
      inds_cd: 'indsCd',
      tic_scope: 'ticScope',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'ticScope',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryDaily',
    responseSchema: industryDailyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20006',
    bodyMap: {
      inds_cd: 'indsCd',
      base_dt: 'baseDt',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryWeekly',
    responseSchema: industryWeeklyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20007',
    bodyMap: {
      inds_cd: 'indsCd',
      base_dt: 'baseDt',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryMonthly',
    responseSchema: industryMonthlyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20008',
    bodyMap: {
      inds_cd: 'indsCd',
      base_dt: 'baseDt',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getIndustryYearly',
    responseSchema: industryYearlyResponseSchema,
    path: '/api/dostk/chart',
    apiId: 'ka20019',
    bodyMap: {
      inds_cd: 'indsCd',
      base_dt: 'baseDt',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
];

export type DomesticChartMethodName =
  | 'getIndividualStockInstitutionalChart'
  | 'getIntradayInvestorTrading'
  | 'getStockTick'
  | 'getStockMinute'
  | 'getStockDaily'
  | 'getStockWeekly'
  | 'getStockMonthly'
  | 'getStockYearly'
  | 'getIndustryTick'
  | 'getIndustryMinute'
  | 'getIndustryDaily'
  | 'getIndustryWeekly'
  | 'getIndustryMonthly'
  | 'getIndustryYearly';
