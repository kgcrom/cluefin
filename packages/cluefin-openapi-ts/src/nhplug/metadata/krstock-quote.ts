import type { NhplugEndpointDefinition } from '../../core/types';

export const krstockQuoteEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'currentPrice',
    path: '/krstock/quote/v1/currentPrice',
    bodyMap: {
      market_cd: 'marketCd',
      iem_cd: 'iemCd',
    },
    supportsCts: false,
    params: [
      {
        name: 'marketCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'currentExecution',
    path: '/krstock/quote/v1/currentExecution',
    bodyMap: {
      market_cd: 'marketCd',
      iem_cd: 'iemCd',
      array_cnt: 'arrayCnt',
    },
    supportsCts: false,
    params: [
      {
        name: 'marketCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'arrayCnt',
        required: false,
      },
    ],
  },
  {
    methodName: 'currentDaily',
    path: '/krstock/quote/v1/currentDaily',
    bodyMap: {
      market_cd: 'marketCd',
      iem_cd: 'iemCd',
      array_cnt: 'arrayCnt',
    },
    supportsCts: false,
    params: [
      {
        name: 'marketCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'arrayCnt',
        required: false,
      },
    ],
  },
  {
    methodName: 'currentInvestor',
    path: '/krstock/quote/v1/currentInvestor',
    bodyMap: {
      market_cd: 'marketCd',
      iem_cd: 'iemCd',
      array_cnt: 'arrayCnt',
    },
    supportsCts: false,
    params: [
      {
        name: 'marketCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'arrayCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'period',
    path: '/krstock/quote/v1/period',
    bodyMap: {
      market_cd: 'marketCd',
      iem_cd: 'iemCd',
      mrkt_div_cls_code: 'mrktDivClsCode',
      edate: 'edate',
      array_cnt: 'arrayCnt',
      maxavg: 'maxavg',
      gubun: 'gubun',
      xtick: 'xtick',
      today_cls_code: 'todayClsCode',
      fake_tick: 'fakeTick',
      sur_flag: 'surFlag',
      sur_gb_day_cnt: 'surGbDayCnt',
      sur_bf_end_time: 'surBfEndTime',
      out1_scale_change: 'out1ScaleChange',
      out2_scale_change: 'out2ScaleChange',
    },
    supportsCts: false,
    params: [
      {
        name: 'marketCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'mrktDivClsCode',
        required: false,
      },
      {
        name: 'edate',
        required: false,
      },
      {
        name: 'arrayCnt',
        required: false,
      },
      {
        name: 'maxavg',
        required: false,
      },
      {
        name: 'gubun',
        required: false,
      },
      {
        name: 'xtick',
        required: false,
      },
      {
        name: 'todayClsCode',
        required: false,
      },
      {
        name: 'fakeTick',
        required: false,
      },
      {
        name: 'surFlag',
        required: false,
      },
      {
        name: 'surGbDayCnt',
        required: false,
      },
      {
        name: 'surBfEndTime',
        required: false,
      },
      {
        name: 'out1ScaleChange',
        required: false,
      },
      {
        name: 'out2ScaleChange',
        required: false,
      },
    ],
  },
  {
    methodName: 'afterHoursCurrent',
    path: '/krstock/quote/v1/afterHoursCurrent',
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
    methodName: 'currentAfterHoursDaily',
    path: '/krstock/quote/v1/currentAfterHoursDaily',
    bodyMap: {
      iem_cd: 'iemCd',
      date: 'date',
      array_cnt: 'arrayCnt',
      maxavg: 'maxavg',
      gubun: 'gubun',
    },
    supportsCts: false,
    params: [
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'date',
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
    ],
  },
  {
    methodName: 'currentAfterHoursExecution',
    path: '/krstock/quote/v1/currentAfterHoursExecution',
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
    methodName: 'afterHoursExpected',
    path: '/krstock/quote/v1/afterHoursExpected',
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
    methodName: 'etfCurrent',
    path: '/krstock/quote/v1/etfCurrent',
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
    methodName: 'etfComponents',
    path: '/krstock/quote/v1/etfComponents',
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
];

export type KrstockQuoteMethodName =
  | 'currentPrice'
  | 'currentExecution'
  | 'currentDaily'
  | 'currentInvestor'
  | 'period'
  | 'afterHoursCurrent'
  | 'currentAfterHoursDaily'
  | 'currentAfterHoursExecution'
  | 'afterHoursExpected'
  | 'etfCurrent'
  | 'etfComponents';
