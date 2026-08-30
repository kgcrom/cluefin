import type { NhplugEndpointDefinition } from '../../core/types';

export const krstockInquiryEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'balance',
    path: '/krstock/inquiry/v1/balance',
    bodyMap: {
      act_no: 'actNo',
      bnc_bse_cd: 'bncBseCd',
      ltg_aot_dit_cd: 'ltgAotDitCd',
      aet_bse: 'aetBse',
      qut_dit_cd: 'qutDitCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'bncBseCd',
        required: true,
      },
      {
        name: 'ltgAotDitCd',
        required: true,
      },
      {
        name: 'aetBse',
        required: true,
      },
      {
        name: 'qutDitCd',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'dailyOrderExecution',
    path: '/krstock/inquiry/v1/dailyOrderExecution',
    bodyMap: {
      orr_dt: 'orrDt',
      act_no: 'actNo',
      itg_orr_no: 'itgOrrNo',
      orr_mkt_cd: 'orrMktCd',
      ost_cns_dit: 'ostCnsDit',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'orrDt',
        required: true,
      },
      {
        name: 'ostCnsDit',
        required: true,
      },
      {
        name: 'itgOrrNo',
        required: false,
      },
      {
        name: 'orrMktCd',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'buyableQuantity',
    path: '/krstock/inquiry/v1/buyableQuantity',
    bodyMap: {
      ost_dit_cd: 'ostDitCd',
      act_no: 'actNo',
      iem_cd: 'iemCd',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      orr_pr: 'orrPr',
      cfd_lon_cd: 'cfdLonCd',
      lon_dt: 'lonDt',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'ostDitCd',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'orrPr',
        required: false,
      },
      {
        name: 'cfdLonCd',
        required: false,
      },
      {
        name: 'lonDt',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'sellableQuantity',
    path: '/krstock/inquiry/v1/sellableQuantity',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      lon_dt: 'lonDt',
      cfd_lon_cd: 'cfdLonCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'cfdLonCd',
        required: true,
      },
      {
        name: 'lonDt',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'reservedInquiry',
    path: '/krstock/inquiry/v1/reservedInquiry',
    bodyMap: {
      bkg_orr_rtn_dt: 'bkgOrrRtnDt',
      act_no: 'actNo',
      iem_cd: 'iemCd',
      sby_dit_cd: 'sbyDitCd',
      cfd_lon_cd: 'cfdLonCd',
      bkg_orr_tp_cd: 'bkgOrrTpCd',
      bkg_orr_can_dit_cd: 'bkgOrrCanDitCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'sbyDitCd',
        required: true,
      },
      {
        name: 'bkgOrrTpCd',
        required: true,
      },
      {
        name: 'bkgOrrRtnDt',
        required: false,
      },
      {
        name: 'iemCd',
        required: false,
      },
      {
        name: 'cfdLonCd',
        required: false,
      },
      {
        name: 'bkgOrrCanDitCd',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'realizedPnl',
    path: '/krstock/inquiry/v1/realizedPnl',
    bodyMap: {
      act_no: 'actNo',
      iqr_dit_cd1: 'iqrDitCd1',
      fee_dit_cd: 'feeDitCd',
      qut_dit_cd: 'qutDitCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iqrDitCd1',
        required: true,
      },
      {
        name: 'feeDitCd',
        required: true,
      },
      {
        name: 'qutDitCd',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'assetStatus',
    path: '/krstock/inquiry/v1/assetStatus',
    bodyMap: {
      act_no: 'actNo',
      eal_aly_cd: 'ealAlyCd',
      aet_bse: 'aetBse',
      qut_dit_cd: 'qutDitCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'ealAlyCd',
        required: true,
      },
      {
        name: 'aetBse',
        required: true,
      },
      {
        name: 'qutDitCd',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'dailyPnl',
    path: '/krstock/inquiry/v1/dailyPnl',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      iqr_sta_dt: 'iqrStaDt',
      iqr_end_dt: 'iqrEndDt',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iqrStaDt',
        required: true,
      },
      {
        name: 'iqrEndDt',
        required: true,
      },
      {
        name: 'iemCd',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'tradingPnl',
    path: '/krstock/inquiry/v1/tradingPnl',
    bodyMap: {
      act_no: 'actNo',
      iqr_sta_dt: 'iqrStaDt',
      iqr_end_dt: 'iqrEndDt',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iqrStaDt',
        required: true,
      },
      {
        name: 'iqrEndDt',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'integratedMargin',
    path: '/krstock/inquiry/v1/integratedMargin',
    bodyMap: {
      act_no: 'actNo',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'rightsHeld',
    path: '/krstock/inquiry/v1/rightsHeld',
    bodyMap: {
      sta_dt: 'staDt',
      act_no: 'actNo',
      rit_tp_cd: 'ritTpCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'staDt',
        required: false,
      },
      {
        name: 'ritTpCd',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'rightsScheduled',
    path: '/krstock/inquiry/v1/rightsScheduled',
    bodyMap: {
      act_no: 'actNo',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
];

export type KrstockInquiryMethodName =
  | 'balance'
  | 'dailyOrderExecution'
  | 'buyableQuantity'
  | 'sellableQuantity'
  | 'reservedInquiry'
  | 'realizedPnl'
  | 'assetStatus'
  | 'dailyPnl'
  | 'tradingPnl'
  | 'integratedMargin'
  | 'rightsHeld'
  | 'rightsScheduled';
