import type { NhplugEndpointDefinition } from '../../core/types.js';

export const overseasStockOrderEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'buy',
    path: '/gbstock/order/v1/buy',
    bodyMap: {
      act_no: 'actNo',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      ahi_nmn_pr_tp_cd: 'ahiNmnPrTpCd',
      wtm_cur_knd_cd: 'wtmCurKndCd',
      fc_orr_uit_pr: 'fcOrrUitPr',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'orrQty',
        required: true,
      },
      {
        name: 'ahiNmnPrTpCd',
        required: true,
      },
      {
        name: 'wtmCurKndCd',
        required: true,
      },
      {
        name: 'fcOrrUitPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'sell',
    path: '/gbstock/order/v1/sell',
    bodyMap: {
      act_no: 'actNo',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      ahi_nmn_pr_tp_cd: 'ahiNmnPrTpCd',
      fc_orr_uit_pr: 'fcOrrUitPr',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'orrQty',
        required: true,
      },
      {
        name: 'ahiNmnPrTpCd',
        required: true,
      },
      {
        name: 'fcOrrUitPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'modify',
    path: '/gbstock/order/v1/modify',
    bodyMap: {
      act_no: 'actNo',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      org_orr_no: 'orgOrrNo',
      fc_orr_uit_pr: 'fcOrrUitPr',
      fc_stop_orr_bse_pr: 'fcStopOrrBsePr',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'orgOrrNo',
        required: true,
      },
      {
        name: 'fcOrrUitPr',
        required: true,
      },
      {
        name: 'fcStopOrrBsePr',
        required: false,
      },
    ],
  },
  {
    methodName: 'cancel',
    path: '/gbstock/order/v1/cancel',
    bodyMap: {
      act_no: 'actNo',
      org_orr_no: 'orgOrrNo',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      all_pat_dit_cd: 'allPatDitCd',
      can_qty: 'canQty',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'orgOrrNo',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'allPatDitCd',
        required: true,
      },
      {
        name: 'canQty',
        required: false,
      },
    ],
  },
  {
    methodName: 'reservedSubmit',
    path: '/gbstock/order/v1/reservedSubmit',
    bodyMap: {
      act_no: 'actNo',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      oss_sby_dit_cd: 'ossSbyDitCd',
      orr_qty: 'orrQty',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      fc_orr_uit_pr: 'fcOrrUitPr',
      oss_orr_knd_cd: 'ossOrrKndCd',
      ose_ivs_sgy_cd: 'oseIvsSgyCd',
      bkg_orr_tp_cd: 'bkgOrrTpCd',
      bkg_orr_sta_dt: 'bkgOrrStaDt',
      bkg_orr_end_dt: 'bkgOrrEndDt',
      wtm_cur_knd_cd: 'wtmCurKndCd',
      fc_stop_orr_bse_pr: 'fcStopOrrBsePr',
      orr_pdt_dit_cd: 'orrPdtDitCd',
      lon_dt: 'lonDt',
      cfd_lon_cd: 'cfdLonCd',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'ossSbyDitCd',
        required: true,
      },
      {
        name: 'orrQty',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'fcOrrUitPr',
        required: false,
      },
      {
        name: 'ossOrrKndCd',
        required: false,
      },
      {
        name: 'oseIvsSgyCd',
        required: false,
      },
      {
        name: 'bkgOrrTpCd',
        required: false,
      },
      {
        name: 'bkgOrrStaDt',
        required: false,
      },
      {
        name: 'bkgOrrEndDt',
        required: false,
      },
      {
        name: 'wtmCurKndCd',
        required: false,
      },
      {
        name: 'fcStopOrrBsePr',
        required: false,
      },
      {
        name: 'orrPdtDitCd',
        required: false,
      },
      {
        name: 'lonDt',
        required: false,
      },
      {
        name: 'cfdLonCd',
        required: false,
      },
    ],
  },
  {
    methodName: 'reservedCancel',
    path: '/gbstock/order/v1/reservedCancel',
    bodyMap: {
      act_no: 'actNo',
      fc_mkt_dit_cd: 'fcMktDitCd',
      bkg_orr_dt: 'bkgOrrDt',
      bkg_rtn_orr_no: 'bkgRtnOrrNo',
      iem_cd: 'iemCd',
      orr_pdt_dit_cd: 'orrPdtDitCd',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'fcMktDitCd',
        required: true,
      },
      {
        name: 'bkgOrrDt',
        required: true,
      },
      {
        name: 'bkgRtnOrrNo',
        required: true,
      },
      {
        name: 'iemCd',
        required: false,
      },
      {
        name: 'orrPdtDitCd',
        required: false,
      },
    ],
  },
];

export type OverseasStockOrderMethodName = 'buy' | 'sell' | 'modify' | 'cancel' | 'reservedSubmit' | 'reservedCancel';
