import type { KisEndpointDefinition } from '../../core/types';

export const domesticStockInfoEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getProductBasicInfo',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/search-info',
    trId: 'CTPF1604R',
    requestMap: {
      PDNO: 'pdno',
      PRDT_TYPE_CD: 'prdtTypeCd',
    },
    params: [
      {
        name: 'pdno',
        required: true,
      },
      {
        name: 'prdtTypeCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockBasicInfo',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/search-stock-info',
    trId: 'CTPF1002R',
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
    methodName: 'getBalanceSheet',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/balance-sheet',
    trId: 'FHKST66430100',
    requestMap: {
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_input_iscd: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidDivClsCode',
        required: true,
      },
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
    methodName: 'getIncomeStatement',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/income-statement',
    trId: 'FHKST66430200',
    requestMap: {
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_input_iscd: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidDivClsCode',
        required: true,
      },
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
    methodName: 'getFinancialRatio',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/financial-ratio',
    trId: 'FHKST66430300',
    requestMap: {
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_input_iscd: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidDivClsCode',
        required: true,
      },
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
    methodName: 'getProfitabilityRatio',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/profit-ratio',
    trId: 'FHKST66430400',
    requestMap: {
      fid_input_iscd: 'fidInputIscd',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOtherKeyRatio',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/other-major-ratios',
    trId: 'FHKST66430500',
    requestMap: {
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStabilityRatio',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/stability-ratio',
    trId: 'FHKST66430600',
    requestMap: {
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getGrowthRatio',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/finance/growth-ratio',
    trId: 'FHKST66430800',
    requestMap: {
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMarginTradableStocks',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/credit-by-company',
    trId: 'FHPST04770000',
    requestMap: {
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_slct_yn: 'fidSlctYn',
      fid_input_iscd: 'fidInputIscd',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidSlctYn',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdDividendDecision',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/dividend',
    trId: 'HHKDB669102C0',
    requestMap: {
      CTS: 'cts',
      GB1: 'gb1',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
      HIGH_GB: 'highGb',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'gb1',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'highGb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdStockDividendDecision',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/purreq',
    trId: 'HHKDB669103C0',
    requestMap: {
      SHT_CD: 'shtCd',
      T_DT: 'tDt',
      F_DT: 'fDt',
      CTS: 'cts',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdMergerSplitDecision',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/merger-split',
    trId: 'HHKDB669104C0',
    requestMap: {
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdParValueChangeDecision',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/rev-split',
    trId: 'HHKDB669105C0',
    requestMap: {
      SHT_CD: 'shtCd',
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
      MARKET_GB: 'marketGb',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'marketGb',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdCapitalReductionSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/cap-dcrs',
    trId: 'HHKDB669106C0',
    requestMap: {
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdListingInfoSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/list-info',
    trId: 'HHKDB669107C0',
    requestMap: {
      SHT_CD: 'shtCd',
      T_DT: 'tDt',
      F_DT: 'fDt',
      CTS: 'cts',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdIpoSubscriptionSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/pub-offer',
    trId: 'HHKDB669108C0',
    requestMap: {
      SHT_CD: 'shtCd',
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdForfeitedShareSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/forfeit',
    trId: 'HHKDB669109C0',
    requestMap: {
      SHT_CD: 'shtCd',
      T_DT: 'tDt',
      F_DT: 'fDt',
      CTS: 'cts',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdDepositSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/mand-deposit',
    trId: 'HHKDB669110C0',
    requestMap: {
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
      F_DT: 'fDt',
      CTS: 'cts',
    },
    params: [
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdPaidInCapitalIncreaseSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/paidin-capin',
    trId: 'HHKDB669100C0',
    requestMap: {
      CTS: 'cts',
      GB1: 'gb1',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'gb1',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdStockDividendSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/bonus-issue',
    trId: 'HHKDB669101C0',
    requestMap: {
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getKsdShareholderMeetingSchedule',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ksdinfo/sharehld-meet',
    trId: 'HHKDB669111C0',
    requestMap: {
      CTS: 'cts',
      F_DT: 'fDt',
      T_DT: 'tDt',
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'cts',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getEstimatedEarnings',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/estimate-perform',
    trId: 'HHKST668300C0',
    requestMap: {
      SHT_CD: 'shtCd',
    },
    params: [
      {
        name: 'shtCd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockLoanableList',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/lendable-by-company',
    trId: 'CTSC2702R',
    requestMap: {
      EXCG_DVSN_CD: 'excgDvsnCd',
      PDNO: 'pdno',
      THCO_STLN_PSBL_YN: 'thcoStlnPsblYn',
      INQR_DVSN_1: 'inqrDvsn1',
      CTX_AREA_FK200: 'ctxAreaFk200',
      CTX_AREA_NK100: 'ctxAreaNk100',
    },
    params: [
      {
        name: 'excgDvsnCd',
        required: true,
      },
      {
        name: 'pdno',
        required: true,
      },
      {
        name: 'thcoStlnPsblYn',
        required: true,
      },
      {
        name: 'inqrDvsn1',
        required: true,
      },
      {
        name: 'ctxAreaFk200',
        required: true,
      },
      {
        name: 'ctxAreaNk100',
        required: true,
      },
    ],
  },
  {
    methodName: 'getInvestmentOpinion',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/invest-opinion',
    trId: 'FHKST663300C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
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
    ],
  },
  {
    methodName: 'getInvestmentOpinionByBrokerage',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/invest-opbysec',
    trId: 'FHKST663400C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
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
    ],
  },
];
