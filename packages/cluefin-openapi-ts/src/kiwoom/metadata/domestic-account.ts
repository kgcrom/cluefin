import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticAccountEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getDailyStockRealizedProfitLossByDate',
    path: '/api/dostk/acnt',
    apiId: 'ka10072',
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
    },
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getDailyStockRealizedProfitLossByPeriod',
    path: '/api/dostk/acnt',
    apiId: 'ka10073',
    bodyMap: {
      stk_cd: 'stkCd',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
    },
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getDailyRealizedProfitLoss',
    path: '/api/dostk/acnt',
    apiId: 'ka10074',
    bodyMap: {
      strt_dt: 'strtDt',
      end_dt: 'endDt',
    },
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getUnexecuted',
    path: '/api/dostk/acnt',
    apiId: 'ka10075',
    bodyMap: {
      all_stk_tp: 'allStkTp',
      trde_tp: 'trdeTp',
      stex_tp: 'stexTp',
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'allStkTp',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'stkCd',
        required: false,
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
    methodName: 'getExecuted',
    path: '/api/dostk/acnt',
    apiId: 'ka10076',
    bodyMap: {
      qry_tp: 'qryTp',
      sell_tp: 'sellTp',
      stex_tp: 'stexTp',
      stk_cd: 'stkCd',
      ord_no: 'ordNo',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'sellTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'stkCd',
        required: false,
      },
      {
        name: 'ordNo',
        required: false,
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
    methodName: 'getDailyRealizedProfitLossDetails',
    path: '/api/dostk/acnt',
    apiId: 'ka10077',
    bodyMap: {
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getAccountProfitRate',
    path: '/api/dostk/acnt',
    apiId: 'ka10085',
    bodyMap: {
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
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
    methodName: 'getUnexecutedSplitOrderDetails',
    path: '/api/dostk/acnt',
    apiId: 'ka10088',
    bodyMap: {
      ord_no: 'ordNo',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'ordNo',
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
    methodName: 'getCurrentDayTradingJournal',
    path: '/api/dostk/acnt',
    apiId: 'ka10170',
    bodyMap: {
      ottks_tp: 'ottksTp',
      ch_crd_tp: 'chCrdTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'ottksTp',
        required: true,
      },
      {
        name: 'chCrdTp',
        required: true,
      },
      {
        name: 'baseDt',
        required: false,
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
    methodName: 'getDepositBalanceDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00001',
    bodyMap: {
      qry_tp: 'qryTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
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
    methodName: 'getDailyEstimatedDepositAssetBalance',
    path: '/api/dostk/acnt',
    apiId: 'kt00002',
    bodyMap: {
      start_dt: 'startDt',
      end_dt: 'endDt',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'startDt',
        required: true,
      },
      {
        name: 'endDt',
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
    methodName: 'getEstimatedAssetBalance',
    path: '/api/dostk/acnt',
    apiId: 'kt00003',
    bodyMap: {
      qry_tp: 'qryTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
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
    methodName: 'getAccountEvaluationStatus',
    path: '/api/dostk/acnt',
    apiId: 'kt00004',
    bodyMap: {
      qry_tp: 'qryTp',
      dmst_stex_tp: 'dmstStexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'dmstStexTp',
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
    methodName: 'getExecutionBalance',
    path: '/api/dostk/acnt',
    apiId: 'kt00005',
    bodyMap: {
      dmst_stex_tp: 'dmstStexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'dmstStexTp',
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
    methodName: 'getAccountOrderExecutionDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00007',
    bodyMap: {
      qry_tp: 'qryTp',
      stk_bond_tp: 'stkBondTp',
      sell_tp: 'sellTp',
      dmst_stex_tp: 'dmstStexTp',
      ord_dt: 'ordDt',
      stk_cd: 'stkCd',
      fr_ord_no: 'frOrdNo',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'stkBondTp',
        required: true,
      },
      {
        name: 'sellTp',
        required: true,
      },
      {
        name: 'dmstStexTp',
        required: true,
      },
      {
        name: 'ordDt',
        required: false,
        defaultValue: '',
      },
      {
        name: 'stkCd',
        required: false,
        defaultValue: '',
      },
      {
        name: 'frOrdNo',
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
    methodName: 'getAccountNextDaySettlementDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00008',
    bodyMap: {
      strt_dcd_seq: 'strtDcdSeq',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'strtDcdSeq',
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
    methodName: 'getAccountOrderExecutionStatus',
    path: '/api/dostk/acnt',
    apiId: 'kt00009',
    bodyMap: {
      stk_bond_tp: 'stkBondTp',
      mrkt_tp: 'mrktTp',
      sell_tp: 'sellTp',
      qry_tp: 'qryTp',
      dmst_stex_tp: 'dmstStexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkBondTp',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'sellTp',
        required: true,
      },
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'dmstStexTp',
        required: true,
      },
      {
        name: 'ordDt',
        required: false,
      },
      {
        name: 'stkCd',
        required: false,
      },
      {
        name: 'frOrdNo',
        required: false,
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
    methodName: 'getAvailableWithdrawalAmount',
    path: '/api/dostk/acnt',
    apiId: 'kt00010',
    bodyMap: {
      stk_cd: 'stkCd',
      trde_tp: 'trdeTp',
      uv: 'uv',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'trdeTp',
        required: true,
      },
      {
        name: 'uv',
        required: true,
      },
      {
        name: 'ioAmt',
        required: false,
      },
      {
        name: 'trdeQty',
        required: false,
      },
      {
        name: 'expBuyUnp',
        required: false,
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
    methodName: 'getAvailableOrderQuantityByMarginRate',
    path: '/api/dostk/acnt',
    apiId: 'kt00011',
    bodyMap: {
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'uv',
        required: false,
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
    methodName: 'getAvailableOrderQuantityByMarginLoanStock',
    path: '/api/dostk/acnt',
    apiId: 'kt00012',
    bodyMap: {
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'uv',
        required: false,
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
    methodName: 'getMarginDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00013',
    bodyMap: {},
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getConsignmentComprehensiveTransactionHistory',
    path: '/api/dostk/acnt',
    apiId: 'kt00015',
    bodyMap: {
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      tp: 'tp',
      gds_tp: 'gdsTp',
      dmst_stex_tp: 'dmstStexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
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
        name: 'tp',
        required: true,
      },
      {
        name: 'gdsTp',
        required: true,
      },
      {
        name: 'dmstStexTp',
        required: true,
      },
      {
        name: 'stkCd',
        required: false,
      },
      {
        name: 'crncCd',
        required: false,
      },
      {
        name: 'frgnStexCode',
        required: false,
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
    methodName: 'getDailyAccountProfitRateDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00016',
    bodyMap: {
      fr_dt: 'frDt',
      to_dt: 'toDt',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'frDt',
        required: true,
      },
      {
        name: 'toDt',
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
    methodName: 'getAccountCurrentDayStatus',
    path: '/api/dostk/acnt',
    apiId: 'kt00017',
    bodyMap: {},
    headerParamMap: {
      'con-yn': 'contYn',
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
    methodName: 'getAccountEvaluationBalanceDetails',
    path: '/api/dostk/acnt',
    apiId: 'kt00018',
    bodyMap: {
      qry_tp: 'qryTp',
      dmst_stex_tp: 'dmstStexTp',
    },
    headerParamMap: {
      'con-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'qryTp',
        required: true,
      },
      {
        name: 'dmstStexTp',
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

export type DomesticAccountMethodName =
  | 'getDailyStockRealizedProfitLossByDate'
  | 'getDailyStockRealizedProfitLossByPeriod'
  | 'getDailyRealizedProfitLoss'
  | 'getUnexecuted'
  | 'getExecuted'
  | 'getDailyRealizedProfitLossDetails'
  | 'getAccountProfitRate'
  | 'getUnexecutedSplitOrderDetails'
  | 'getCurrentDayTradingJournal'
  | 'getDepositBalanceDetails'
  | 'getDailyEstimatedDepositAssetBalance'
  | 'getEstimatedAssetBalance'
  | 'getAccountEvaluationStatus'
  | 'getExecutionBalance'
  | 'getAccountOrderExecutionDetails'
  | 'getAccountNextDaySettlementDetails'
  | 'getAccountOrderExecutionStatus'
  | 'getAvailableWithdrawalAmount'
  | 'getAvailableOrderQuantityByMarginRate'
  | 'getAvailableOrderQuantityByMarginLoanStock'
  | 'getMarginDetails'
  | 'getConsignmentComprehensiveTransactionHistory'
  | 'getDailyAccountProfitRateDetails'
  | 'getAccountCurrentDayStatus'
  | 'getAccountEvaluationBalanceDetails';
