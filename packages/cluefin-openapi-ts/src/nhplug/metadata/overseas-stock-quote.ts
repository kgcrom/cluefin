import type { NhplugEndpointDefinition } from '../../core/types';

export const overseasStockQuoteEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'current',
    path: '/gbstock/quote/v1/current',
    bodyMap: {
      iem_cd: 'iemCd',
    },
    supportsCts: false,
    params: [
      {
        name: 'iemCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'executionTrend',
    path: '/gbstock/quote/v1/executionTrend',
    bodyMap: {
      period_type: 'periodType',
      req_cnt: 'reqCnt',
      iem_cd: 'iemCd',
    },
    supportsCts: false,
    params: [
      {
        name: 'periodType',
        required: true,
      },
      {
        name: 'reqCnt',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'period',
    path: '/gbstock/quote/v1/period',
    bodyMap: {
      iem_cd: 'iemCd',
      end_dt: 'endDt',
      count: 'count',
      maxavg: 'maxavg',
      gubun: 'gubun',
      xtick: 'xtick',
      today_cls: 'todayCls',
      market_cls: 'marketCls',
    },
    supportsCts: false,
    params: [
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'endDt',
        required: true,
      },
      {
        name: 'count',
        required: true,
      },
      {
        name: 'maxavg',
        required: true,
      },
      {
        name: 'gubun',
        required: true,
      },
      {
        name: 'xtick',
        required: true,
      },
      {
        name: 'todayCls',
        required: true,
      },
      {
        name: 'marketCls',
        required: true,
      },
    ],
  },
  {
    methodName: 'symbolIndexFxPeriod',
    path: '/gbstock/quote/v1/symbolIndexFxPeriod',
    bodyMap: {
      iem_cd: 'iemCd',
      end_dt: 'endDt',
      array_cnt: 'arrayCnt',
      maxavg: 'maxavg',
      gubun: 'gubun',
      today_cls: 'todayCls',
      xtick: 'xtick',
      scale_change: 'scaleChange',
    },
    supportsCts: false,
    params: [
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'endDt',
        required: true,
      },
      {
        name: 'arrayCnt',
        required: true,
      },
      {
        name: 'maxavg',
        required: true,
      },
      {
        name: 'gubun',
        required: true,
      },
      {
        name: 'todayCls',
        required: true,
      },
      {
        name: 'xtick',
        required: false,
      },
      {
        name: 'scaleChange',
        required: false,
      },
    ],
  },
];

export type OverseasStockQuoteMethodName = 'current' | 'executionTrend' | 'period' | 'symbolIndexFxPeriod';
