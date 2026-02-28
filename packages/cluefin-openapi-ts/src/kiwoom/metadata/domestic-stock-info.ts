import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticStockInfoEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getStockInfo',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10001',
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
    methodName: 'getStockTradingMember',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10002',
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
    methodName: 'getExecution',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10003',
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
    methodName: 'getMarginTradingTrend',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10013',
    bodyMap: {
      stk_cd: 'stkCd',
      dt: 'dt',
      qry_tp: 'qryTp',
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
        name: 'dt',
        required: true,
      },
      {
        name: 'qryTp',
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
    methodName: 'getDailyTradingDetails',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10015',
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
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
    methodName: 'getNewHighLowPrice',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10016',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      ntl_tp: 'ntlTp',
      high_low_close_tp: 'highLowCloseTp',
      stk_cnd: 'stkCnd',
      trde_qty_tp: 'trdeQtyTp',
      crd_cnd: 'crdCnd',
      updown_incls: 'updownIncls',
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
        name: 'ntlTp',
        required: true,
      },
      {
        name: 'highLowCloseTp',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'trdeQtyTp',
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
    methodName: 'getUpperLowerLimitPrice',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10017',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      updown_tp: 'updownTp',
      sort_tp: 'sortTp',
      stk_cnd: 'stkCnd',
      trde_qty_tp: 'trdeQtyTp',
      crd_cnd: 'crdCnd',
      trde_gold_tp: 'trdeGoldTp',
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
        name: 'updownTp',
        required: true,
      },
      {
        name: 'sortTp',
        required: true,
      },
      {
        name: 'stkCnd',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'crdCnd',
        required: true,
      },
      {
        name: 'trdeGoldTp',
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
    methodName: 'getHighLowPriceApproach',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10018',
    bodyMap: {
      high_low_tp: 'highLowTp',
      alacc_rt: 'alaccRt',
      mrkt_tp: 'mrktTp',
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
        name: 'highLowTp',
        required: true,
      },
      {
        name: 'alaccRt',
        required: true,
      },
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
    methodName: 'getPriceVolatility',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10019',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      flu_tp: 'fluTp',
      tm_tp: 'tmTp',
      tm: 'tm',
      trde_qty_tp: 'trdeQtyTp',
      stk_cnd: 'stkCnd',
      crd_cnd: 'crdCnd',
      pric_cnd: 'pricCnd',
      updown_incls: 'updownIncls',
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
        name: 'fluTp',
        required: true,
      },
      {
        name: 'tmTp',
        required: true,
      },
      {
        name: 'tm',
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
        name: 'pricCnd',
        required: true,
      },
      {
        name: 'updownIncls',
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
    methodName: 'getTradingVolumeRenewal',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10024',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      cycle_tp: 'cycleTp',
      trde_qty_tp: 'trdeQtyTp',
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
        name: 'cycleTp',
        required: true,
      },
      {
        name: 'trdeQtyTp',
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
    methodName: 'getSupplyDemandConcentration',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10025',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      prps_cnctr_rt: 'prpsCnctrRt',
      cur_prc_entry: 'curPrcEntry',
      prpscnt: 'prpscnt',
      cycle_tp: 'cycleTp',
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
        name: 'prpsCnctrRt',
        required: true,
      },
      {
        name: 'curPrcEntry',
        required: true,
      },
      {
        name: 'prpscnt',
        required: true,
      },
      {
        name: 'cycleTp',
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
    methodName: 'getHighPer',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10026',
    bodyMap: {
      pertp: 'pertp',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'pertp',
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
    methodName: 'getChangeRateFromOpen',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10028',
    bodyMap: {
      sort_tp: 'sortTp',
      trde_qty_cnd: 'trdeQtyCnd',
      mrkt_tp: 'mrktTp',
      updown_incls: 'updownIncls',
      stk_cnd: 'stkCnd',
      crd_cnd: 'crdCnd',
      trde_prica_cnd: 'trdePricaCnd',
      flu_cnd: 'fluCnd',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'sortTp',
        required: true,
      },
      {
        name: 'trdeQtyCnd',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'updownIncls',
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
        name: 'trdePricaCnd',
        required: true,
      },
      {
        name: 'fluCnd',
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
    methodName: 'getTradingMemberSupplyDemandAnalysis',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10043',
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      qry_dt_tp: 'qryDtTp',
      pot_tp: 'potTp',
      dt: 'dt',
      sort_base: 'sortBase',
      mmcm_cd: 'mmcmCd',
      stex_tp: 'stexTp',
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
        name: 'mmcmCd',
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
    methodName: 'getTradingMemberInstantVolume',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10052',
    bodyMap: {
      stk_cd: 'stkCd',
      mmcm_cd: 'mmcmCd',
      mrkt_tp: 'mrktTp',
      qty_tp: 'qtyTp',
      pric_tp: 'pricTp',
      stex_tp: 'stexTp',
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
        name: 'mmcmCd',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'qtyTp',
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
    methodName: 'getVolatilityControlEvent',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10054',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      bf_mkrt_tp: 'bfMkrtTp',
      motn_tp: 'motnTp',
      skip_stk: 'skipStk',
      trde_qty_tp: 'trdeQtyTp',
      min_trde_qty: 'minTrdeQty',
      max_trde_qty: 'maxTrdeQty',
      trde_prica_tp: 'trdePricaTp',
      min_trde_prica: 'minTrdePrica',
      max_trde_prica: 'maxTrdePrica',
      motn_drc: 'motnDrc',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'bfMkrtTp',
        required: true,
      },
      {
        name: 'motnTp',
        required: true,
      },
      {
        name: 'skipStk',
        required: true,
      },
      {
        name: 'trdeQtyTp',
        required: true,
      },
      {
        name: 'trdePricaTp',
        required: true,
      },
      {
        name: 'motnDrc',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'minTrdeQty',
        required: false,
        defaultValue: '',
      },
      {
        name: 'maxTrdeQty',
        required: false,
        defaultValue: '',
      },
      {
        name: 'minTrdePrica',
        required: false,
        defaultValue: '',
      },
      {
        name: 'maxTrdePrica',
        required: false,
        defaultValue: '',
      },
      {
        name: 'stkCd',
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
    methodName: 'getDailyPreviousDayExecutionVolume',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10055',
    bodyMap: {
      stk_cd: 'stkCd',
      tdy_pred: 'tdyPred',
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
        name: 'tdyPred',
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
    methodName: 'getDailyTradingItemsByInvestor',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10058',
    bodyMap: {
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      trde_tp: 'trdeTp',
      mrkt_tp: 'mrktTp',
      invsr_tp: 'invsrTp',
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
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'invsrTp',
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
    methodName: 'getInstitutionalInvestorByStock',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10059',
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
    methodName: 'getTotalInstitutionalInvestorByStock',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10061',
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
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
    methodName: 'getDailyPreviousDayConclusion',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10084',
    bodyMap: {
      stk_cd: 'stkCd',
      tdy_pred: 'tdyPred',
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
        name: 'tdyPred',
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
    methodName: 'getInterestStockInfo',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10095',
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
    methodName: 'getStockInfoSummary',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10099',
    bodyMap: {
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
    methodName: 'getStockInfoV1',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10100',
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
    methodName: 'getIndustryCode',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10101',
    bodyMap: {
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
    methodName: 'getMemberCompany',
    path: '/api/dostk/stkinfo',
    apiId: 'ka10102',
    bodyMap: {},
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
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
    methodName: 'getTop50ProgramNetBuy',
    path: '/api/dostk/stkinfo',
    apiId: 'ka90003',
    bodyMap: {
      trde_upper_tp: 'trdeUpperTp',
      amt_qty_tp: 'amtQtyTp',
      mrkt_tp: 'mrktTp',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'trdeUpperTp',
        required: true,
      },
      {
        name: 'amtQtyTp',
        required: true,
      },
      {
        name: 'mrktTp',
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
    methodName: 'getProgramTradingStatusByStock',
    path: '/api/dostk/stkinfo',
    apiId: 'ka90004',
    bodyMap: {
      dt: 'dt',
      mrkt_tp: 'mrktTp',
      stex_tp: 'stexTp',
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
        name: 'mrktTp',
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
];
