import type { KisEndpointDefinition } from '../../core/types';

export const overseasBasicQuoteEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getStockCurrentPriceDetail',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/price-detail',
    trId: 'HHDFS76200200',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
      SYMB: 'symb',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getCurrentPriceFirstQuote',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-asking-price',
    trId: 'HHDFS76200100',
    requestMap: {
      EXCD: 'excd',
      SYMB: 'symb',
    },
    params: [
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
      {
        name: 'auth',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockCurrentPriceConclusion',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/price',
    trId: 'HHDFS00000300',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
      SYMB: 'symb',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getConclusionTrend',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-ccnl',
    trId: 'HHDFS76200300',
    requestMap: {
      EXCD: 'excd',
      AUTH: 'auth',
      KEYB: 'keyb',
      TDAY: 'tday',
      SYMB: 'symb',
    },
    params: [
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'keyb',
        required: true,
      },
      {
        name: 'tday',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockMinuteChart',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice',
    trId: 'HHDFS76950200',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
      SYMB: 'symb',
      NMIN: 'nmin',
      PINC: 'pinc',
      NEXT: 'next',
      NREC: 'nrec',
      FILL: 'fill',
      KEYB: 'keyb',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
      {
        name: 'nmin',
        required: true,
      },
      {
        name: 'pinc',
        required: true,
      },
      {
        name: 'next',
        required: true,
      },
      {
        name: 'nrec',
        required: true,
      },
      {
        name: 'fill',
        required: true,
      },
      {
        name: 'keyb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getIndexMinuteChart',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice',
    trId: 'FHKST03030200',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_HOUR_CLS_CODE: 'fidHourClsCode',
      FID_PW_DATA_INCU_YN: 'fidPwDataIncuYn',
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
        name: 'fidHourClsCode',
        required: true,
      },
      {
        name: 'fidPwDataIncuYn',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockPeriodQuote',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/dailyprice',
    trId: 'HHDFS76240000',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
      SYMB: 'symb',
      GUBN: 'gubn',
      BYMD: 'bymd',
      MODP: 'modp',
      KEYB: 'keyb',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'symb',
        required: true,
      },
      {
        name: 'gubn',
        required: true,
      },
      {
        name: 'bymd',
        required: true,
      },
      {
        name: 'modp',
        required: true,
      },
      {
        name: 'keyb',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getItemIndexExchangePeriodPrice',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-daily-chartprice',
    trId: 'FHKST03030100',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_PERIOD_DIV_CODE: 'fidPeriodDivCode',
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
    ],
  },
  {
    methodName: 'searchByCondition',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/inquire-search',
    trId: 'HHDFS76410000',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
      CO_YN_PRICECUR: 'coYnPricecur',
      CO_ST_PRICECUR: 'coStPricecur',
      CO_EN_PRICECUR: 'coEnPricecur',
      CO_YN_RATE: 'coYnRate',
      CO_ST_RATE: 'coStRate',
      CO_EN_RATE: 'coEnRate',
      CO_YN_VALX: 'coYnValx',
      CO_ST_VALX: 'coStValx',
      CO_EN_VALX: 'coEnValx',
      CO_YN_SHAR: 'coYnShar',
      CO_ST_SHAR: 'coStShar',
      CO_EN_SHAR: 'coEnShar',
      CO_YN_VOLUME: 'coYnVolume',
      CO_ST_VOLUME: 'coStVolume',
      CO_EN_VOLUME: 'coEnVolume',
      CO_YN_AMT: 'coYnAmt',
      CO_ST_AMT: 'coStAmt',
      CO_EN_AMT: 'coEnAmt',
      CO_YN_EPS: 'coYnEps',
      CO_ST_EPS: 'coStEps',
      CO_EN_EPS: 'coEnEps',
      CO_YN_PER: 'coYnPer',
      CO_ST_PER: 'coStPer',
      CO_EN_PER: 'coEnPer',
      KEYB: 'keyb',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'coYnPricecur',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStPricecur',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnPricecur',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnRate',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStRate',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnRate',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnValx',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStValx',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnValx',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnShar',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStShar',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnShar',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnVolume',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStVolume',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnVolume',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnAmt',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStAmt',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnAmt',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnEps',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStEps',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnEps',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coYnPer',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coStPer',
        required: false,
        defaultValue: '',
      },
      {
        name: 'coEnPer',
        required: false,
        defaultValue: '',
      },
      {
        name: 'keyb',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getSettlementDate',
    method: 'GET',
    path: '/uapi/overseas-stock/v1/quotations/countries-holiday',
    trId: 'CTOS5011R',
    requestMap: {
      TRAD_DT: 'tradDt',
      CTX_AREA_NK: 'ctxAreaNk',
      CTX_AREA_FK: 'ctxAreaFk',
    },
    params: [
      {
        name: 'tradDt',
        required: true,
      },
      {
        name: 'ctxAreaNk',
        required: true,
      },
      {
        name: 'ctxAreaFk',
        required: true,
      },
    ],
  },
  {
    methodName: 'getProductBaseInfo',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/search-info',
    trId: 'CTPF1702R',
    requestMap: {
      PRDT_TYPE_CD: 'prdtTypeCd',
      PDNO: 'pdno',
    },
    params: [
      {
        name: 'prdtTypeCd',
        required: true,
      },
      {
        name: 'pdno',
        required: true,
      },
    ],
  },
  {
    methodName: 'getSectorPrice',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/industry-theme',
    trId: 'HHDFS76370000',
    requestMap: {
      KEYB: 'keyb',
      AUTH: 'auth',
      EXCD: 'excd',
      ICOD: 'icod',
      VOL_RANG: 'volRang',
    },
    params: [
      {
        name: 'keyb',
        required: true,
      },
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
      {
        name: 'icod',
        required: true,
      },
      {
        name: 'volRang',
        required: true,
      },
    ],
  },
  {
    methodName: 'getSectorCodes',
    method: 'GET',
    path: '/uapi/overseas-price/v1/quotations/industry-price',
    trId: 'HHDFS76370100',
    requestMap: {
      AUTH: 'auth',
      EXCD: 'excd',
    },
    params: [
      {
        name: 'auth',
        required: true,
      },
      {
        name: 'excd',
        required: true,
      },
    ],
  },
];
