import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticEtfEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getEtfReturnRate',
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
