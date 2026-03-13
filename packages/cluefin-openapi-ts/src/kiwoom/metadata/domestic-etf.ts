import type { KiwoomEndpointDefinition } from '../../core/types';
import {
  etfDailyExecutionResponseSchema,
  etfDailyTrendResponseSchema,
  etfFullPriceResponseSchema,
  etfHourlyExecutionResponseSchema,
  etfHourlyExecutionV2ResponseSchema,
  etfHourlyTrendResponseSchema,
  etfHourlyTrendV2ResponseSchema,
  etfItemInfoResponseSchema,
  etfReturnRateResponseSchema,
} from '../schemas/domestic-etf';

export const domesticEtfEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getEtfReturnRate',
    responseSchema: etfReturnRateResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40001',
    bodyMap: {
      stk_cd: 'stkCd',
      etfobjt_idex_cd: 'etfobjtIdexCd',
      dt: 'dt',
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
        name: 'etfobjtIdexCd',
        required: true,
      },
      {
        name: 'dt',
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
    methodName: 'getEtfItemInfo',
    responseSchema: etfItemInfoResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40002',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfDailyTrend',
    responseSchema: etfDailyTrendResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40003',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfFullPrice',
    responseSchema: etfFullPriceResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40004',
    bodyMap: {
      txon_type: 'txonType',
      navpre: 'navpre',
      mngmcomp: 'mngmcomp',
      txon_yn: 'txonYn',
      trace_idex: 'traceIdex',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'txonType',
        required: true,
      },
      {
        name: 'navpre',
        required: true,
      },
      {
        name: 'mngmcomp',
        required: true,
      },
      {
        name: 'txonYn',
        required: true,
      },
      {
        name: 'traceIdex',
        required: true,
      },
      {
        name: 'stexTp',
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
    methodName: 'getEtfHourlyTrend',
    responseSchema: etfHourlyTrendResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40006',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfHourlyExecution',
    responseSchema: etfHourlyExecutionResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40007',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfDailyExecution',
    responseSchema: etfDailyExecutionResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40008',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfHourlyExecutionV2',
    responseSchema: etfHourlyExecutionV2ResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40009',
    bodyMap: {
      stk_cd: 'stkCd',
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
    methodName: 'getEtfHourlyTrendV2',
    responseSchema: etfHourlyTrendV2ResponseSchema,
    path: '/api/dostk/etf',
    apiId: 'ka40010',
    bodyMap: {
      stk_cd: 'stkCd',
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

export type DomesticEtfMethodName =
  | 'getEtfReturnRate'
  | 'getEtfItemInfo'
  | 'getEtfDailyTrend'
  | 'getEtfFullPrice'
  | 'getEtfHourlyTrend'
  | 'getEtfHourlyExecution'
  | 'getEtfDailyExecution'
  | 'getEtfHourlyExecutionV2'
  | 'getEtfHourlyTrendV2';
