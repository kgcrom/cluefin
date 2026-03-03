import type { KisEndpointDefinition } from '../../core/types';

export const domesticBasicQuoteEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getStockCurrentPrice',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-price',
    trId: 'FHKST01010100',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPrice2',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-price-2',
    trId: 'FHPST01010000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceConclusion',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-ccnl',
    trId: 'FHKST01010300',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-daily-price',
    trId: 'FHKST01010400',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_PERIOD_DIV_CODE: 'fidPeriodDivCode',
      FID_ORG_ADJ_PRC: 'fidOrgAdjPrc',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidPeriodDivCode',
        required: true,
      },
      {
        name: 'fidOrgAdjPrc',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceAskingExpectedConclusion',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn',
    trId: 'FHKST01010200',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceInvestor',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-investor',
    trId: 'FHKST01010900',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceMember',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-member',
    trId: 'FHKST01010600',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockPeriodQuote',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice',
    trId: 'FHKST03010100',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_PERIOD_DIV_CODE: 'fidPeriodDivCode',
      FID_ORG_ADJ_PRC: 'fidOrgAdjPrc',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputDate1',
        required: true,
      },
      {
        name: 'fidInputDate2',
        required: true,
      },
      {
        name: 'fidPeriodDivCode',
        required: true,
      },
      {
        name: 'fidOrgAdjPrc',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockTodayMinuteChart',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice',
    trId: 'FHKST03010200',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_HOUR_1: 'fidInputHour1',
      FID_PW_DATA_INCU_YN: 'fidPwDataIncuYn',
      FID_ETC_CLS_CODE: 'fidEtcClsCode',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputHour1',
        required: true,
      },
      {
        name: 'fidPwDataIncuYn',
        required: true,
      },
      {
        name: 'fidEtcClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockDailyMinuteChart',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice',
    trId: 'FHKST03010230',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_HOUR_1: 'fidInputHour1',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_PW_DATA_INCU_YN: 'fidPwDataIncuYn',
      FID_FAKE_TICK_INCU_YN: 'fidFakeTickIncuYn',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputHour1',
        required: true,
      },
      {
        name: 'fidInputDate1',
        required: true,
      },
      {
        name: 'fidPwDataIncuYn',
        required: true,
      },
      {
        name: 'fidFakeTickIncuYn',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceTimeItemConclusion',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion',
    trId: 'FHPST01060000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_HOUR_1: 'fidInputHour1',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputHour1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceDailyOvertimePrice',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-daily-overtimeprice',
    trId: 'FHPST02320000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceOvertimeConclusion',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion',
    trId: 'FHPST02310000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockOvertimeCurrentPrice',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-overtime-price',
    trId: 'FHPST02300000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockOvertimeAskingPrice',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price',
    trId: 'FHPST02300400',
    requestMap: {
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
    ],
  },
  {
    methodName: 'getStockClosingExpectedPrice',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/exp-closing-price',
    trId: 'FHKST117300C0',
    requestMap: {
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_BLNG_CLS_CODE: 'fidBlngClsCode',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
    },
    params: [
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
      {
        name: 'fidCondScrDivCode',
        required: false,
        defaultValue: '11173',
      },
    ],
  },
  {
    methodName: 'getEtfetnCurrentPrice',
    method: 'GET',
    path: '/uapi/etfetn/v1/quotations/inquire-price',
    trId: 'FHPST02400000',
    requestMap: {
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
    ],
  },
  {
    methodName: 'getEtfComponentStockPrice',
    method: 'GET',
    path: '/uapi/etfetn/v1/quotations/inquire-component-stock-price',
    trId: 'FHKST121600C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_COND_MRKT_DIV_CODE_1: 'fidCondMrktDivCode',
      FID_INPUT_ISCD_1: 'fidInputIscd',
      FID_COND_SCR_DIV_CODE_1: 'fidCondScrDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
      {
        name: 'fidCondScrDivCode',
        required: false,
        defaultValue: '11216',
      },
    ],
  },
  {
    methodName: 'getEtfNavComparisonTrend',
    method: 'GET',
    path: '/uapi/etfetn/v1/quotations/nav-comparison-trend',
    trId: 'FHPST02440000',
    requestMap: {
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
    ],
  },
  {
    methodName: 'getEtfNavComparisonDailyTrend',
    method: 'GET',
    path: '/uapi/etfetn/v1/quotations/nav-comparison-daily-trend',
    trId: 'FHPST02440200',
    requestMap: {
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_input_date_1: 'fidInputDate1',
      fid_input_date_2: 'fidInputDate2',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputDate1',
        required: true,
      },
      {
        name: 'fidInputDate2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'J',
      },
    ],
  },
  {
    methodName: 'getEtfNavComparisonTimeTrend',
    method: 'GET',
    path: '/uapi/etfetn/v1/quotations/nav-comparison-time-trend',
    trId: 'FHPST02440100',
    requestMap: {
      fid_hour_cls_code: 'fidHourClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidHourClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'E',
      },
    ],
  },
];
