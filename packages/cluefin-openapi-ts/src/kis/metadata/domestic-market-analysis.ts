import type { KisEndpointDefinition } from '../../core/types.js';

export const domesticMarketAnalysisEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getConditionSearchList',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/psearch-title',
    trId: 'HHKST03900300',
    requestMap: {
      user_id: 'userId',
    },
    params: [
      {
        name: 'userId',
        required: true,
      },
    ],
  },
  {
    methodName: 'getConditionSearchResult',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/psearch-result',
    trId: 'HHKST03900400',
    requestMap: {
      user_id: 'userId',
      seq: 'seq',
    },
    params: [
      {
        name: 'userId',
        required: true,
      },
      {
        name: 'seq',
        required: true,
      },
    ],
  },
  {
    methodName: 'getWatchlistGroups',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/intstock-grouplist',
    trId: 'HHKCM113004C7',
    requestMap: {
      TYPE: 'interestType',
      FID_ETC_CLS_CODE: 'fidEtcClsCode',
      USER_ID: 'userId',
    },
    params: [
      {
        name: 'interestType',
        required: true,
      },
      {
        name: 'fidEtcClsCode',
        required: true,
      },
      {
        name: 'userId',
        required: true,
      },
    ],
  },
  {
    methodName: 'getWatchlistMultiQuote',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/intstock-multprice',
    trId: 'FHKST11300006',
    requestMap: {
      FID_COND_MRKT_DIV_CODE_1: 'fidCondMrktDivCode1',
      FID_INPUT_ISCD_1: 'fidInputIscd1',
      FID_COND_MRKT_DIV_CODE_2: 'fidCondMrktDivCode2',
      FID_INPUT_ISCD_2: 'fidInputIscd2',
      FID_COND_MRKT_DIV_CODE_3: 'fidCondMrktDivCode3',
      FID_INPUT_ISCD_3: 'fidInputIscd3',
      FID_COND_MRKT_DIV_CODE_4: 'fidCondMrktDivCode4',
      FID_INPUT_ISCD_4: 'fidInputIscd4',
      FID_COND_MRKT_DIV_CODE_5: 'fidCondMrktDivCode5',
      FID_INPUT_ISCD_5: 'fidInputIscd5',
      FID_COND_MRKT_DIV_CODE_6: 'fidCondMrktDivCode6',
      FID_INPUT_ISCD_6: 'fidInputIscd6',
      FID_COND_MRKT_DIV_CODE_7: 'fidCondMrktDivCode7',
      FID_INPUT_ISCD_7: 'fidInputIscd7',
      FID_COND_MRKT_DIV_CODE_8: 'fidCondMrktDivCode8',
      FID_INPUT_ISCD_8: 'fidInputIscd8',
      FID_COND_MRKT_DIV_CODE_9: 'fidCondMrktDivCode9',
      FID_INPUT_ISCD_9: 'fidInputIscd9',
      FID_COND_MRKT_DIV_CODE_10: 'fidCondMrktDivCode10',
      FID_INPUT_ISCD_10: 'fidInputIscd10',
      FID_COND_MRKT_DIV_CODE_11: 'fidCondMrktDivCode11',
      FID_INPUT_ISCD_11: 'fidInputIscd11',
      FID_COND_MRKT_DIV_CODE_12: 'fidCondMrktDivCode12',
      FID_INPUT_ISCD_12: 'fidInputIscd12',
      FID_COND_MRKT_DIV_CODE_13: 'fidCondMrktDivCode13',
      FID_INPUT_ISCD_13: 'fidInputIscd13',
      FID_COND_MRKT_DIV_CODE_14: 'fidCondMrktDivCode14',
      FID_INPUT_ISCD_14: 'fidInputIscd14',
      FID_COND_MRKT_DIV_CODE_15: 'fidCondMrktDivCode15',
      FID_INPUT_ISCD_15: 'fidInputIscd15',
      FID_COND_MRKT_DIV_CODE_16: 'fidCondMrktDivCode16',
      FID_INPUT_ISCD_16: 'fidInputIscd16',
      FID_COND_MRKT_DIV_CODE_17: 'fidCondMrktDivCode17',
      FID_INPUT_ISCD_17: 'fidInputIscd17',
      FID_COND_MRKT_DIV_CODE_18: 'fidCondMrktDivCode18',
      FID_INPUT_ISCD_18: 'fidInputIscd18',
      FID_COND_MRKT_DIV_CODE_19: 'fidCondMrktDivCode19',
      FID_INPUT_ISCD_19: 'fidInputIscd19',
      FID_COND_MRKT_DIV_CODE_20: 'fidCondMrktDivCode20',
      FID_INPUT_ISCD_20: 'fidInputIscd20',
      FID_COND_MRKT_DIV_CODE_21: 'fidCondMrktDivCode21',
      FID_INPUT_ISCD_21: 'fidInputIscd21',
      FID_COND_MRKT_DIV_CODE_22: 'fidCondMrktDivCode22',
      FID_INPUT_ISCD_22: 'fidInputIscd22',
      FID_COND_MRKT_DIV_CODE_23: 'fidCondMrktDivCode23',
      FID_INPUT_ISCD_23: 'fidInputIscd23',
      FID_COND_MRKT_DIV_CODE_24: 'fidCondMrktDivCode24',
      FID_INPUT_ISCD_24: 'fidInputIscd24',
      FID_COND_MRKT_DIV_CODE_25: 'fidCondMrktDivCode25',
      FID_INPUT_ISCD_25: 'fidInputIscd25',
      FID_COND_MRKT_DIV_CODE_26: 'fidCondMrktDivCode26',
      FID_INPUT_ISCD_26: 'fidInputIscd26',
      FID_COND_MRKT_DIV_CODE_27: 'fidCondMrktDivCode27',
      FID_INPUT_ISCD_27: 'fidInputIscd27',
      FID_COND_MRKT_DIV_CODE_28: 'fidCondMrktDivCode28',
      FID_INPUT_ISCD_28: 'fidInputIscd28',
      FID_COND_MRKT_DIV_CODE_29: 'fidCondMrktDivCode29',
      FID_INPUT_ISCD_29: 'fidInputIscd29',
      FID_COND_MRKT_DIV_CODE_30: 'fidCondMrktDivCode30',
      FID_INPUT_ISCD_30: 'fidInputIscd30',
    },
    params: [
      {
        name: 'fidCondMrktDivCode1',
        required: true,
      },
      {
        name: 'fidInputIscd1',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode2',
        required: false,
      },
      {
        name: 'fidInputIscd2',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode3',
        required: false,
      },
      {
        name: 'fidInputIscd3',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode4',
        required: false,
      },
      {
        name: 'fidInputIscd4',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode5',
        required: false,
      },
      {
        name: 'fidInputIscd5',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode6',
        required: false,
      },
      {
        name: 'fidInputIscd6',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode7',
        required: false,
      },
      {
        name: 'fidInputIscd7',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode8',
        required: false,
      },
      {
        name: 'fidInputIscd8',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode9',
        required: false,
      },
      {
        name: 'fidInputIscd9',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode10',
        required: false,
      },
      {
        name: 'fidInputIscd10',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode11',
        required: false,
      },
      {
        name: 'fidInputIscd11',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode12',
        required: false,
      },
      {
        name: 'fidInputIscd12',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode13',
        required: false,
      },
      {
        name: 'fidInputIscd13',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode14',
        required: false,
      },
      {
        name: 'fidInputIscd14',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode15',
        required: false,
      },
      {
        name: 'fidInputIscd15',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode16',
        required: false,
      },
      {
        name: 'fidInputIscd16',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode17',
        required: false,
      },
      {
        name: 'fidInputIscd17',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode18',
        required: false,
      },
      {
        name: 'fidInputIscd18',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode19',
        required: false,
      },
      {
        name: 'fidInputIscd19',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode20',
        required: false,
      },
      {
        name: 'fidInputIscd20',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode21',
        required: false,
      },
      {
        name: 'fidInputIscd21',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode22',
        required: false,
      },
      {
        name: 'fidInputIscd22',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode23',
        required: false,
      },
      {
        name: 'fidInputIscd23',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode24',
        required: false,
      },
      {
        name: 'fidInputIscd24',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode25',
        required: false,
      },
      {
        name: 'fidInputIscd25',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode26',
        required: false,
      },
      {
        name: 'fidInputIscd26',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode27',
        required: false,
      },
      {
        name: 'fidInputIscd27',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode28',
        required: false,
      },
      {
        name: 'fidInputIscd28',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode29',
        required: false,
      },
      {
        name: 'fidInputIscd29',
        required: false,
      },
      {
        name: 'fidCondMrktDivCode30',
        required: false,
      },
      {
        name: 'fidInputIscd30',
        required: false,
      },
    ],
  },
  {
    methodName: 'getWatchlistStocksByGroup',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/intstock-stocklist-by-group',
    trId: 'HHKCM113004C6',
    requestMap: {
      TYPE: 'type',
      USER_ID: 'userId',
      DATA_RANK: 'dataRank',
      INTER_GRP_CODE: 'interGrpCode',
      INTER_GRP_NAME: 'interGrpName',
      HTS_KOR_ISNM: 'htsKorIsnm',
      CNTG_CLS_CODE: 'cntgClsCode',
      FID_ETC_CLS_CODE: 'fidEtcClsCode',
    },
    params: [
      {
        name: 'type',
        required: true,
      },
      {
        name: 'userId',
        required: true,
      },
      {
        name: 'dataRank',
        required: true,
      },
      {
        name: 'interGrpCode',
        required: true,
      },
      {
        name: 'interGrpName',
        required: true,
      },
      {
        name: 'htsKorIsnm',
        required: true,
      },
      {
        name: 'cntgClsCode',
        required: true,
      },
      {
        name: 'fidEtcClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getInstitutionalForeignTradingAggregate',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/foreign-institution-total',
    trId: 'FHPTJ04400000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
      FID_ETC_CLS_CODE: 'fidEtcClsCode',
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
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidEtcClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getForeignBrokerageTradingAggregate',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/frgnmem-trade-estimate',
    trId: 'FHKST644100C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
      FID_RANK_SORT_CLS_CODE_2: 'fidRankSortClsCode2',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidRankSortClsCode2',
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
        defaultValue: '16441',
      },
    ],
  },
  {
    methodName: 'getInvestorTradingTrendByStockDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/investor-trade-by-stock-daily',
    trId: 'FHPTJ04160001',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_ORG_ADJ_PRC: 'fidOrgAdjPrc',
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
        name: 'fidInputDate1',
        required: true,
      },
      {
        name: 'fidOrgAdjPrc',
        required: false,
        defaultValue: '',
      },
      {
        name: 'fidEtcClsCode',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getInvestorTradingTrendByMarketIntraday',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market',
    trId: 'FHPTJ04030000',
    requestMap: {
      fid_input_iscd: 'fidInputIscd',
      fid_input_iscd_2: 'fidInputIscd2',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputIscd2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getInvestorTradingTrendByMarketDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-investor-daily-by-market',
    trId: 'FHPTJ04040000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_ISCD_1: 'fidInputIscd1',
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_INPUT_ISCD_2: 'fidInputIscd2',
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
        name: 'fidInputIscd1',
        required: true,
      },
      {
        name: 'fidInputDate2',
        required: true,
      },
      {
        name: 'fidInputIscd2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getForeignNetBuyTrendByStock',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/frgnmem-pchs-trend',
    trId: 'FHKST644400C0',
    requestMap: {
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_ISCD_2: 'fidInputIscd2',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidInputIscd2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMemberTradingTrendTick',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/frgnmem-trade-trend',
    trId: 'FHPST04320000',
    requestMap: {
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_ISCD_2: 'fidInputIscd2',
      FID_MRKT_CLS_CODE: 'fidMrktClsCode',
      FID_VOL_CNT: 'fidVolCnt',
    },
    params: [
      {
        name: 'fidCondScrDivCode',
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
      {
        name: 'fidInputIscd2',
        required: true,
      },
      {
        name: 'fidMrktClsCode',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMemberTradingTrendByStock',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-member-daily',
    trId: 'FHPST04540000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_ISCD_2: 'fidInputIscd2',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_SCTN_CLS_CODE: 'fidSctnClsCode',
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
        name: 'fidInputIscd2',
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
        name: 'fidSctnClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getProgramTradingTrendByStockIntraday',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/program-trade-by-stock',
    trId: 'FHPPG04650101',
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
    methodName: 'getProgramTradingTrendByStockDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/program-trade-by-stock-daily',
    trId: 'FHPPG04650201',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
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
    ],
  },
  {
    methodName: 'getForeignInstitutionalEstimateByStock',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/investor-trend-estimate',
    trId: 'HHPTJ04160200',
    requestMap: {
      MKSC_SHRN_ISCD: 'mkscShrnIscd',
    },
    params: [
      {
        name: 'mkscShrnIscd',
        required: true,
      },
    ],
  },
  {
    methodName: 'getBuySellVolumeByStockDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/inquire-daily-trade-volume',
    trId: 'FHKST03010800',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_PERIOD_DIV_CODE: 'fidPeriodDivCode',
      FID_COND_MRKT_DIV_CODE_1: 'fidCondMrktDivCode1',
      FID_INPUT_ISCD_1: 'fidInputIscd1',
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
        name: 'fidCondMrktDivCode1',
        required: false,
      },
      {
        name: 'fidInputIscd1',
        required: false,
      },
    ],
  },
  {
    methodName: 'getProgramTradingSummaryIntraday',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/comp-program-trade-today',
    trId: 'FHPPG04600101',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_MRKT_CLS_CODE: 'fidMrktClsCode',
      FID_SCTN_CLS_CODE: 'fidSctnClsCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_MRKT_DIV_CODE1: 'fidCondMrktDivCode1',
      FID_INPUT_HOUR_1: 'fidInputHour1',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidMrktClsCode',
        required: true,
      },
      {
        name: 'fidSctnClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode1',
        required: true,
      },
      {
        name: 'fidInputHour1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getProgramTradingSummaryDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/comp-program-trade-daily',
    trId: 'FHPPG04600001',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_MRKT_CLS_CODE: 'fidMrktClsCode',
      FID_INPUT_DATE_1: 'fidInputDate1',
      FID_INPUT_DATE_2: 'fidInputDate2',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidMrktClsCode',
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
    methodName: 'getProgramTradingInvestorTrendToday',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/investor-program-trade-today',
    trId: 'HHPPG046600C1',
    requestMap: {
      EXCH_DIV_CLS_CODE: 'exchDivClsCode',
      MRKT_DIV_CLS_CODE: 'mrktDivClsCode',
    },
    params: [
      {
        name: 'exchDivClsCode',
        required: true,
      },
      {
        name: 'mrktDivClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getCreditBalanceTrendDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/daily-credit-balance',
    trId: 'FHPST04760000',
    requestMap: {
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_input_date_1: 'fidInputDate1',
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
    ],
  },
  {
    methodName: 'getExpectedPriceTrend',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/exp-price-trend',
    trId: 'FHPST01810000',
    requestMap: {
      fid_mkop_cls_code: 'fidMkopClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_input_iscd: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidMkopClsCode',
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
    methodName: 'getShortSellingTrendDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/daily-short-sale',
    trId: 'FHPST04830000',
    requestMap: {
      FID_INPUT_DATE_2: 'fidInputDate2',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_INPUT_DATE_1: 'fidInputDate1',
    },
    params: [
      {
        name: 'fidInputDate2',
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
      {
        name: 'fidInputDate1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getAfterHoursExpectedFluctuation',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/overtime-exp-trans-fluct',
    trId: 'FHKST11860000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_INPUT_PRICE_1: 'fidInputPrice1',
      FID_INPUT_PRICE_2: 'fidInputPrice2',
      FID_INPUT_VOL_1: 'fidInputVol1',
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
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidInputVol1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getTradingWeightByAmount',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/tradprt-byamt',
    trId: 'FHKST111900C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
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
    ],
  },
  {
    methodName: 'getMarketFundSummary',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/mktfunds',
    trId: 'FHKST649100C0',
    requestMap: {
      FID_INPUT_DATE_1: 'fidInputDate1',
    },
    params: [
      {
        name: 'fidInputDate1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockLoanTrendDaily',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/daily-loan-trans',
    trId: 'HHPST074500C0',
    requestMap: {
      MRKT_DIV_CLS_CODE: 'mrktDivClsCode',
      MKSC_SHRN_ISCD: 'mkscShrnIscd',
      START_DATE: 'startDate',
      END_DATE: 'endDate',
      CTS: 'cts',
    },
    params: [
      {
        name: 'mrktDivClsCode',
        required: true,
      },
      {
        name: 'mkscShrnIscd',
        required: true,
      },
      {
        name: 'startDate',
        required: true,
      },
      {
        name: 'endDate',
        required: true,
      },
      {
        name: 'cts',
        required: true,
      },
    ],
  },
  {
    methodName: 'getLimitPriceStocks',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/capture-uplowprice',
    trId: 'FHKST130000C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_PRC_CLS_CODE: 'fidPrcClsCode',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_TRGT_CLS_CODE: 'fidTrgtClsCode',
      FID_TRGT_EXLS_CLS_CODE: 'fidTrgtExlsClsCode',
      FID_INPUT_PRICE_1: 'fidInputPrice1',
      FID_INPUT_PRICE_2: 'fidInputPrice2',
      FID_VOL_CNT: 'fidVolCnt',
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
        name: 'fidPrcClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getResistanceLevelTradingWeight',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/pbar-tratio',
    trId: 'FHPST01130000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
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
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputHour1',
        required: true,
      },
    ],
  },
];

export type DomesticMarketAnalysisMethodName =
  | 'getConditionSearchList'
  | 'getConditionSearchResult'
  | 'getWatchlistGroups'
  | 'getWatchlistMultiQuote'
  | 'getWatchlistStocksByGroup'
  | 'getInstitutionalForeignTradingAggregate'
  | 'getForeignBrokerageTradingAggregate'
  | 'getInvestorTradingTrendByStockDaily'
  | 'getInvestorTradingTrendByMarketIntraday'
  | 'getInvestorTradingTrendByMarketDaily'
  | 'getForeignNetBuyTrendByStock'
  | 'getMemberTradingTrendTick'
  | 'getMemberTradingTrendByStock'
  | 'getProgramTradingTrendByStockIntraday'
  | 'getProgramTradingTrendByStockDaily'
  | 'getForeignInstitutionalEstimateByStock'
  | 'getBuySellVolumeByStockDaily'
  | 'getProgramTradingSummaryIntraday'
  | 'getProgramTradingSummaryDaily'
  | 'getProgramTradingInvestorTrendToday'
  | 'getCreditBalanceTrendDaily'
  | 'getExpectedPriceTrend'
  | 'getShortSellingTrendDaily'
  | 'getAfterHoursExpectedFluctuation'
  | 'getTradingWeightByAmount'
  | 'getMarketFundSummary'
  | 'getStockLoanTrendDaily'
  | 'getLimitPriceStocks'
  | 'getResistanceLevelTradingWeight';
