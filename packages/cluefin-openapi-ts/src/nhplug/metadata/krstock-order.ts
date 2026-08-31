import type { NhplugEndpointDefinition } from '../../core/types.js';

export const krstockOrderEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'cashBuy',
    path: '/krstock/order/v1/cashBuy',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      orr_pr: 'orrPr',
      orr_amt: 'orrAmt',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      orr_cnd_dit_cd: 'orrCndDitCd',
      ssl_nmn_pr_dit_cd: 'sslNmnPrDitCd',
      sop_cnd_pr: 'sopCndPr',
      rmt_mkt_cd: 'rmtMktCd',
      sor_mkt_sli_yn: 'sorMktSliYn',
    },
    supportsCts: false,
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
        name: 'orrQty',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'sorMktSliYn',
        required: true,
      },
      {
        name: 'orrCndDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'sslNmnPrDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'orrPr',
        required: false,
      },
      {
        name: 'orrAmt',
        required: false,
      },
      {
        name: 'sopCndPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'cashSell',
    path: '/krstock/order/v1/cashSell',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      orr_pr: 'orrPr',
      orr_amt: 'orrAmt',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      orr_cnd_dit_cd: 'orrCndDitCd',
      ssl_nmn_pr_dit_cd: 'sslNmnPrDitCd',
      sop_cnd_pr: 'sopCndPr',
      rmt_mkt_cd: 'rmtMktCd',
      sor_mkt_sli_yn: 'sorMktSliYn',
    },
    supportsCts: false,
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
        name: 'orrQty',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'sorMktSliYn',
        required: true,
      },
      {
        name: 'orrCndDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'sslNmnPrDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'orrPr',
        required: false,
      },
      {
        name: 'orrAmt',
        required: false,
      },
      {
        name: 'sopCndPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'creditBuy',
    path: '/krstock/order/v1/creditBuy',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      orr_pr: 'orrPr',
      orr_amt: 'orrAmt',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      orr_cnd_dit_cd: 'orrCndDitCd',
      cfd_lon_cd: 'cfdLonCd',
      lon_dt: 'lonDt',
      sop_cnd_pr: 'sopCndPr',
      rmt_mkt_cd: 'rmtMktCd',
      sor_mkt_sli_yn: 'sorMktSliYn',
    },
    supportsCts: false,
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
        name: 'orrQty',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'cfdLonCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'sorMktSliYn',
        required: true,
      },
      {
        name: 'orrCndDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'orrPr',
        required: false,
      },
      {
        name: 'orrAmt',
        required: false,
      },
      {
        name: 'lonDt',
        required: false,
      },
      {
        name: 'sopCndPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'creditSell',
    path: '/krstock/order/v1/creditSell',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      orr_qty: 'orrQty',
      orr_pr: 'orrPr',
      orr_amt: 'orrAmt',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      orr_cnd_dit_cd: 'orrCndDitCd',
      cfd_lon_cd: 'cfdLonCd',
      lon_dt: 'lonDt',
      sop_cnd_pr: 'sopCndPr',
      rmt_mkt_cd: 'rmtMktCd',
      sor_mkt_sli_yn: 'sorMktSliYn',
    },
    supportsCts: false,
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
        name: 'orrQty',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'cfdLonCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'sorMktSliYn',
        required: true,
      },
      {
        name: 'orrCndDitCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'orrPr',
        required: false,
      },
      {
        name: 'orrAmt',
        required: false,
      },
      {
        name: 'lonDt',
        required: false,
      },
      {
        name: 'sopCndPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'modify',
    path: '/krstock/order/v1/modify',
    bodyMap: {
      act_no: 'actNo',
      org_mkt_orr_no: 'orgMktOrrNo',
      all_pat_dit_cd: 'allPatDitCd',
      iem_cd: 'iemCd',
      cor_qty: 'corQty',
      cor_pr: 'corPr',
      sop_cnd_pr: 'sopCndPr',
      rmt_mkt_cd: 'rmtMktCd',
      sor_mkt_sli_yn: 'sorMktSliYn',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'orgMktOrrNo',
        required: true,
      },
      {
        name: 'allPatDitCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'corQty',
        required: true,
      },
      {
        name: 'corPr',
        required: true,
      },
      {
        name: 'sopCndPr',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'sorMktSliYn',
        required: true,
      },
    ],
  },
  {
    methodName: 'cancel',
    path: '/krstock/order/v1/cancel',
    bodyMap: {
      act_no: 'actNo',
      org_mkt_orr_no: 'orgMktOrrNo',
      all_pat_dit_cd: 'allPatDitCd',
      iem_cd: 'iemCd',
      cor_qty: 'corQty',
    },
    supportsCts: false,
    params: [
      {
        name: 'actNo',
        required: true,
      },
      {
        name: 'orgMktOrrNo',
        required: true,
      },
      {
        name: 'allPatDitCd',
        required: true,
      },
      {
        name: 'iemCd',
        required: true,
      },
      {
        name: 'corQty',
        required: true,
      },
    ],
  },
  {
    methodName: 'reservedOrder',
    path: '/krstock/order/v1/reservedOrder',
    bodyMap: {
      act_no: 'actNo',
      iem_cd: 'iemCd',
      sby_dit_cd: 'sbyDitCd',
      frs_sba_orr_yn: 'frsSbaOrrYn',
      nmn_pr_tp_cd: 'nmnPrTpCd',
      cfd_lon_cd: 'cfdLonCd',
      lon_dt: 'lonDt',
      orr_qty: 'orrQty',
      orr_uit_pr: 'orrUitPr',
      bkg_orr_tp_cd: 'bkgOrrTpCd',
      bkg_orr_sta_dt: 'bkgOrrStaDt',
      bkg_orr_end_dt: 'bkgOrrEndDt',
      bkg_orr_enf_tp_cd: 'bkgOrrEnfTpCd',
      end_pr_cmp_ftw_amt: 'endPrCmpFtwAmt',
      orr_pr_rge_hlm_pr: 'orrPrRgeHlmPr',
      orr_pr_rge_llm_pr: 'orrPrRgeLlmPr',
      rmt_mkt_cd: 'rmtMktCd',
    },
    supportsCts: false,
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
        name: 'sbyDitCd',
        required: true,
      },
      {
        name: 'frsSbaOrrYn',
        required: true,
      },
      {
        name: 'nmnPrTpCd',
        required: true,
      },
      {
        name: 'cfdLonCd',
        required: true,
      },
      {
        name: 'orrQty',
        required: true,
      },
      {
        name: 'orrUitPr',
        required: true,
      },
      {
        name: 'bkgOrrTpCd',
        required: true,
      },
      {
        name: 'bkgOrrEnfTpCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'lonDt',
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
        name: 'endPrCmpFtwAmt',
        required: false,
      },
      {
        name: 'orrPrRgeHlmPr',
        required: false,
      },
      {
        name: 'orrPrRgeLlmPr',
        required: false,
      },
    ],
  },
  {
    methodName: 'reservedCancel',
    path: '/krstock/order/v1/reservedCancel',
    bodyMap: {
      act_no: 'actNo',
      sby_dit_cd: 'sbyDitCd',
      iem_cd: 'iemCd',
      bkg_orr_no: 'bkgOrrNo',
      bkg_orr_tp_cd: 'bkgOrrTpCd',
      bkg_rtn_dt: 'bkgRtnDt',
      rmt_mkt_cd: 'rmtMktCd',
    },
    supportsCts: false,
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
        name: 'iemCd',
        required: true,
      },
      {
        name: 'bkgOrrNo',
        required: true,
      },
      {
        name: 'bkgOrrTpCd',
        required: true,
      },
      {
        name: 'rmtMktCd',
        required: true,
      },
      {
        name: 'bkgRtnDt',
        required: false,
      },
    ],
  },
];

export type KrstockOrderMethodName =
  | 'cashBuy'
  | 'cashSell'
  | 'creditBuy'
  | 'creditSell'
  | 'modify'
  | 'cancel'
  | 'reservedOrder'
  | 'reservedCancel';
