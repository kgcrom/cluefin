import type { KiwoomEndpointDefinition } from '../../core/types';
import {
  afterHoursSinglePriceChangeRateRankingResponseSchema,
  rapidlyIncreasingRemainingOrderQuantityResponseSchema,
  rapidlyIncreasingTotalSellOrdersResponseSchema,
  rapidlyIncreasingTradingVolumeResponseSchema,
  sameNetBuySellRankingResponseSchema,
  stockSpecificSecuritiesFirmRankingResponseSchema,
  topConsecutiveNetBuySellByForeignersResponseSchema,
  topCurrentDayDeviationSourcesResponseSchema,
  topCurrentDayMajorTradersResponseSchema,
  topCurrentDayTradingVolumeResponseSchema,
  topExpectedConclusionPercentageChangeResponseSchema,
  topForeignAccountGroupTradingResponseSchema,
  topForeignerInstitutionTradingResponseSchema,
  topForeignerPeriodTradingResponseSchema,
  topLimitExhaustionRateForeignerResponseSchema,
  topMarginRatioResponseSchema,
  topNetBuyTraderRankingResponseSchema,
  topPercentageChangeFromPreviousDayResponseSchema,
  topPreviousDayTradingVolumeResponseSchema,
  topRemainingOrderQuantityResponseSchema,
  topSecuritiesFirmTradingResponseSchema,
  topTransactionValueResponseSchema,
} from '../schemas/domestic-rank-info';

export const domesticRankInfoEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getTopRemainingOrderQuantity',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10020',
    responseSchema: topRemainingOrderQuantityResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_tp: 'sortTp',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      crd_cnd: 'crdCnd',
      stex_tp: 'stexTp',
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
        name: 'sortTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'crdCnd',
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
    methodName: 'getRapidlyIncreasingRemainingOrderQuantity',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10021',
    responseSchema: rapidlyIncreasingRemainingOrderQuantityResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      trde_tp: 'trdeTp',
      sort_tp: 'sortTp',
      tm_tp: 'tmTp',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      stex_tp: 'stexTp',
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
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'sortTp',
        required: true,
      },
      {
        name: 'tmTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'stkCnd',
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
    methodName: 'getRapidlyIncreasingTotalSellOrders',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10022',
    responseSchema: rapidlyIncreasingTotalSellOrdersResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      rt_tp: 'rtTp',
      tm_tp: 'tmTp',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      stex_tp: 'stexTp',
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
        name: 'rtTp',
        required: true,
      },
      {
        name: 'tmTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'stkCnd',
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
    methodName: 'getRapidlyIncreasingTradingVolume',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10023',
    responseSchema: rapidlyIncreasingTradingVolumeResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_tp: 'sortTp',
      tm_tp: 'tmTp',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      pric_tp: 'pricTp',
      stex_tp: 'stexTp',
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
        name: 'sortTp',
        required: true,
      },
      {
        name: 'tmTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'pricTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'tm',
        required: false,
        defaultValue: '',
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
    methodName: 'getTopPercentageChangeFromPreviousDay',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10027',
    responseSchema: topPercentageChangeFromPreviousDayResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_tp: 'sortTp',
      trde_qty_cnd: 'trdeQtyCnd',
      stk_cnd: 'stkCnd',
      crd_cnd: 'crdCnd',
      updown_incls: 'updownIncls',
      pric_cnd: 'pricCnd',
      trde_prica_cnd: 'trdePricaCnd',
      stex_tp: 'stexTp',
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
        name: 'sortTp',
        required: true,
      },
      {
        name: 'trdeQtyCnd',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'crdCnd',
        required: true,
      },
      {
        name: 'updownIncls',
        required: true,
      },
      {
        name: 'pricCnd',
        required: true,
      },
      {
        name: 'trdePricaCnd',
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
    methodName: 'getTopExpectedConclusionPercentageChange',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10029',
    responseSchema: topExpectedConclusionPercentageChangeResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_tp: 'sortTp',
      trde_qty_cnd: 'trdeQtyCnd',
      stk_cnd: 'stkCnd',
      crd_cnd: 'crdCnd',
      pric_cnd: 'pricCnd',
      stex_tp: 'stexTp',
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
        name: 'sortTp',
        required: true,
      },
      {
        name: 'trdeQtyCnd',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'crdCnd',
        required: true,
      },
      {
        name: 'pricCnd',
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
    methodName: 'getTopCurrentDayTradingVolume',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10030',
    responseSchema: topCurrentDayTradingVolumeResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_tp: 'sortTp',
      mang_stk_incls: 'mangStkIncls',
      crd_tp: 'crdTp',
      trde_qty_tp: 'trdeQtyTp',
      pric_tp: 'pricTp',
      trde_prica_tp: 'trdePricaTp',
      mrkt_open_tp: 'mrktOpenTp',
      stex_tp: 'stexTp',
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
        name: 'sortTp',
        required: true,
      },
      {
        name: 'mangStkIncls',
        required: true,
      },
      {
        name: 'crdTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'pricTp',
        required: true,
      },
      {
        name: 'trdePricaTp',
        required: true,
      },
      {
        name: 'mrktOpenTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: false,
        defaultValue: '1',
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
    methodName: 'getTopPreviousDayTradingVolume',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10031',
    responseSchema: topPreviousDayTradingVolumeResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      qry_tp: 'qryTp',
      rank_strt: 'rankStrt',
      rank_end: 'rankEnd',
      stex_tp: 'stexTp',
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
        name: 'qryTp',
        required: true,
      },
      {
        name: 'rankStrt',
        required: true,
      },
      {
        name: 'rankEnd',
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
    methodName: 'getTopTransactionValue',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10032',
    responseSchema: topTransactionValueResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      mang_stk_incls: 'mangStkIncls',
      stex_tp: 'stexTp',
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
        name: 'mangStkIncls',
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
    methodName: 'getTopMarginRatio',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10033',
    responseSchema: topMarginRatioResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      updown_incls: 'updownIncls',
      crd_cnd: 'crdCnd',
      stex_tp: 'stexTp',
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
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'updownIncls',
        required: true,
      },
      {
        name: 'crdCnd',
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
    methodName: 'getTopForeignerPeriodTrading',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10034',
    responseSchema: topForeignerPeriodTradingResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      trde_tp: 'trdeTp',
      dt: 'dt',
      stex_tp: 'stexTp',
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
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'dt',
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
    methodName: 'getTopConsecutiveNetBuySellByForeigners',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10035',
    responseSchema: topConsecutiveNetBuySellByForeignersResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      trde_tp: 'trdeTp',
      base_dt_tp: 'baseDtTp',
      stex_tp: 'stexTp',
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
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'baseDtTp',
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
    methodName: 'getTopLimitExhaustionRateForeigner',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10036',
    responseSchema: topLimitExhaustionRateForeignerResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      dt: 'dt',
      stex_tp: 'stexTp',
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
        name: 'dt',
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
    methodName: 'getTopForeignAccountGroupTrading',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10037',
    responseSchema: topForeignAccountGroupTradingResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      dt: 'dt',
      trde_tp: 'trdeTp',
      sort_tp: 'sortTp',
      stex_tp: 'stexTp',
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
        name: 'dt',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'sortTp',
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
    methodName: 'getStockSpecificSecuritiesFirmRanking',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10038',
    responseSchema: stockSpecificSecuritiesFirmRankingResponseSchema,
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      qry_tp: 'qryTp',
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
        name: 'strtDt',
        required: true,
      },
      {
        name: 'endDt',
        required: true,
      },
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'dt',
        required: false,
        defaultValue: '1',
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
    methodName: 'getTopSecuritiesFirmTrading',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10039',
    responseSchema: topSecuritiesFirmTradingResponseSchema,
    bodyMap: {
      mmcm_cd: 'mmcmCd',
      trde_qty_tp: 'trdeQtyTp',
      trde_tp: 'trdeTp',
      dt: 'dt',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mmcmCd',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'dt',
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
    methodName: 'getTopCurrentDayMajorTraders',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10040',
    responseSchema: topCurrentDayMajorTradersResponseSchema,
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
    methodName: 'getTopNetBuyTraderRanking',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10042',
    responseSchema: topNetBuyTraderRankingResponseSchema,
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      qry_dt_tp: 'qryDtTp',
      pot_tp: 'potTp',
      dt: 'dt',
      sort_base: 'sortBase',
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
        name: 'strtDt',
        required: true,
      },
      {
        name: 'endDt',
        required: true,
      },
      {
        name: 'qryDtTp',
        required: true,
      },
      {
        name: 'potTp',
        required: true,
      },
      {
        name: 'dt',
        required: true,
      },
      {
        name: 'sortBase',
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
    methodName: 'getTopCurrentDayDeviationSources',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10053',
    responseSchema: topCurrentDayDeviationSourcesResponseSchema,
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
    methodName: 'getSameNetBuySellRanking',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10062',
    responseSchema: sameNetBuySellRankingResponseSchema,
    bodyMap: {
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      mrkt_tp: 'mrktTp',
      trde_tp: 'trdeTp',
      sort_cnd: 'sortCnd',
      unit_tp: 'unitTp',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'strtDt',
        required: true,
      },
      {
        name: 'endDt',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'sortCnd',
        required: true,
      },
      {
        name: 'unitTp',
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
    methodName: 'getAfterHoursSinglePriceChangeRateRanking',
    path: '/api/dostk/rkinfo',
    apiId: 'ka10098',
    responseSchema: afterHoursSinglePriceChangeRateRankingResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      sort_base: 'sortBase',
      stk_cnd: 'stkCnd',
      trde_qty_cnd: 'trdeQtyCnd',
      crd_cnd: 'crdCnd',
      trde_prica: 'trdePrica',
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
        name: 'sortBase',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'trdeQtyCnd',
        required: true,
      },
      {
        name: 'crdCnd',
        required: true,
      },
      {
        name: 'trdePrica',
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
    methodName: 'getTopForeignerInstitutionTrading',
    path: '/api/dostk/rkinfo',
    apiId: 'ka90009',
    responseSchema: topForeignerInstitutionTradingResponseSchema,
    bodyMap: {
      mrkt_tp: 'mrktTp',
      amt_qty_tp: 'amtQtyTp',
      qry_dt_tp: 'qryDtTp',
      stex_tp: 'stexTp',
      date: 'date',
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
        name: 'qryDtTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'date',
        required: false,
        defaultValue: '',
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

export type DomesticRankInfoMethodName =
  | 'getTopRemainingOrderQuantity'
  | 'getRapidlyIncreasingRemainingOrderQuantity'
  | 'getRapidlyIncreasingTotalSellOrders'
  | 'getRapidlyIncreasingTradingVolume'
  | 'getTopPercentageChangeFromPreviousDay'
  | 'getTopExpectedConclusionPercentageChange'
  | 'getTopCurrentDayTradingVolume'
  | 'getTopPreviousDayTradingVolume'
  | 'getTopTransactionValue'
  | 'getTopMarginRatio'
  | 'getTopForeignerPeriodTrading'
  | 'getTopConsecutiveNetBuySellByForeigners'
  | 'getTopLimitExhaustionRateForeigner'
  | 'getTopForeignAccountGroupTrading'
  | 'getStockSpecificSecuritiesFirmRanking'
  | 'getTopSecuritiesFirmTrading'
  | 'getTopCurrentDayMajorTraders'
  | 'getTopNetBuyTraderRanking'
  | 'getTopCurrentDayDeviationSources'
  | 'getSameNetBuySellRanking'
  | 'getAfterHoursSinglePriceChangeRateRanking'
  | 'getTopForeignerInstitutionTrading';
