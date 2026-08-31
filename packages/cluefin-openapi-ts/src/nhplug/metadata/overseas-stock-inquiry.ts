import type { NhplugEndpointDefinition } from '../../core/types.js';

export const overseasStockInquiryEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'buyableAmount',
    path: '/gbstock/inquiry/v1/buyableAmount',
    bodyMap: {
      act_no: 'actNo',
      pcs_dit: 'pcsDit',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      iem_cd: 'iemCd',
      wtm_cur_knd_cd: 'wtmCurKndCd',
      oss_orr_knd_cd: 'ossOrrKndCd',
      ahi_nmn_pr_tp_cd: 'ahiNmnPrTpCd',
      fc_orr_uit_pr: 'fcOrrUitPr',
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
        name: 'pcsDit',
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
        name: 'wtmCurKndCd',
        required: true,
      },
      {
        name: 'ossOrrKndCd',
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
    methodName: 'unexecuted',
    path: '/gbstock/inquiry/v1/unexecuted',
    bodyMap: {
      orr_dt: 'orrDt',
      act_no: 'actNo',
      oss_sby_dit_cd: 'ossSbyDitCd',
      sot_dit: 'sotDit',
      ost_cns_dit: 'ostCnsDit',
      iem_cd: 'iemCd',
      orr_no: 'orrNo',
    },
    supportsCts: true,
    params: [
      {
        name: 'orrDt',
        required: true,
      },
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'ossSbyDitCd',
        required: true,
      },
      {
        name: 'sotDit',
        required: true,
      },
      {
        name: 'ostCnsDit',
        required: true,
      },
      {
        name: 'iemCd',
        required: false,
      },
      {
        name: 'orrNo',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'balance',
    path: '/gbstock/inquiry/v1/balance',
    bodyMap: {
      act_no: 'actNo',
      qut_iqr_dit_cd: 'qutIqrDitCd',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      cur_cd: 'curCd',
      xns_dit_cd: 'xnsDitCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'qutIqrDitCd',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'curCd',
        required: true,
      },
      {
        name: 'xnsDitCd',
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
    path: '/gbstock/inquiry/v1/reservedInquiry',
    bodyMap: {
      fc_mkt_dit_cd: 'fcMktDitCd',
      bkg_orr_dt: 'bkgOrrDt',
      act_no: 'actNo',
      sby_dit_cd: 'sbyDitCd',
      bkg_orr_can_yn: 'bkgOrrCanYn',
      oss_orr_knd_cd: 'ossOrrKndCd',
      bkg_orr_tp_cd: 'bkgOrrTpCd',
      wtm_cur_knd_cd: 'wtmCurKndCd',
      iem_cd: 'iemCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'fcMktDitCd',
        required: true,
      },
      {
        name: 'bkgOrrDt',
        required: true,
      },
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'sbyDitCd',
        required: true,
      },
      {
        name: 'bkgOrrCanYn',
        required: true,
      },
      {
        name: 'ossOrrKndCd',
        required: true,
      },
      {
        name: 'bkgOrrTpCd',
        required: true,
      },
      {
        name: 'wtmCurKndCd',
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
    methodName: 'dailyTransaction',
    path: '/gbstock/inquiry/v1/dailyTransaction',
    bodyMap: {
      act_no: 'actNo',
      iqr_sta_dt: 'iqrStaDt',
      iqr_end_dt: 'iqrEndDt',
      act_trd_cfc_cd: 'actTrdCfcCd',
      iem_mlf_cd: 'iemMlfCd',
      iem_cd: 'iemCd',
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
        name: 'actTrdCfcCd',
        required: true,
      },
      {
        name: 'iemMlfCd',
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
    methodName: 'periodPnl',
    path: '/gbstock/inquiry/v1/periodPnl',
    bodyMap: {
      act_no: 'actNo',
      iqr_dit: 'iqrDit',
      sta_orr_dt: 'staOrrDt',
      end_orr_dt: 'endOrrDt',
      iem_cd: 'iemCd',
      trd_cur_cd: 'trdCurCd',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iqrDit',
        required: true,
      },
      {
        name: 'staOrrDt',
        required: true,
      },
      {
        name: 'endOrrDt',
        required: true,
      },
      {
        name: 'iemCd',
        required: false,
      },
      {
        name: 'trdCurCd',
        required: false,
      },
      {
        name: 'fcSecTrdNatCd',
        required: false,
      },
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'periodPnlDetail',
    path: '/gbstock/inquiry/v1/periodPnlDetail',
    bodyMap: {
      act_no: 'actNo',
      iqr_dit: 'iqrDit',
      orr_dt: 'orrDt',
      fc_sec_trd_nat_cd: 'fcSecTrdNatCd',
      trd_cur_cd: 'trdCurCd',
      iem_cd: 'iemCd',
    },
    supportsCts: true,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'iqrDit',
        required: true,
      },
      {
        name: 'orrDt',
        required: true,
      },
      {
        name: 'fcSecTrdNatCd',
        required: true,
      },
      {
        name: 'trdCurCd',
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
    methodName: 'margin',
    path: '/gbstock/inquiry/v1/margin',
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

export type OverseasStockInquiryMethodName =
  | 'buyableAmount'
  | 'unexecuted'
  | 'balance'
  | 'reservedInquiry'
  | 'dailyTransaction'
  | 'periodPnl'
  | 'periodPnlDetail'
  | 'margin';
