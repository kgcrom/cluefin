import type { DartEndpointDefinition } from '../../core/types.js';

export const majorMattersReportEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'assetTransferPutbackOption',
    path: '/api/astInhtrfEtcPtbkOpt.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'defaultOccurrence',
    path: '/api/dfOcr.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'businessSuspension',
    path: '/api/bsnSp.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'corporateRehabilitationProceedings',
    path: '/api/ctrcvsBgrq.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'dissolutionOccurrence',
    path: '/api/dsRsOcr.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'paidInCapitalIncreaseDecision',
    path: '/api/piicDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'freeCapitalIncreaseDecision',
    path: '/api/fricDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'paidInAndFreeCapitalIncreaseDecision',
    path: '/api/pifricDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'capitalReductionDecision',
    path: '/api/crDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'creditorBankManagementProcedureCommencement',
    path: '/api/bnkMngtPcbg.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'lawsuitFiling',
    path: '/api/lwstLg.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'overseasSecuritiesMarketListingDecision',
    path: '/api/ovLstDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'overseasSecuritiesMarketDelistingDecision',
    path: '/api/ovDlstDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'overseasSecuritiesMarketListingStatus',
    path: '/api/ovLst.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'overseasSecuritiesMarketDelistingStatus',
    path: '/api/ovDlst.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'convertibleBondIssuanceDecision',
    path: '/api/cvbdIsDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'newStockWarrantBondIssuanceDecision',
    path: '/api/bdwtIsDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'exchangeableBondIssuanceDecision',
    path: '/api/exbdIsDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'creditorBankManagementProcedureTermination',
    path: '/api/bnkMngtPcsp.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'writeDownContingentCapitalSecuritiesIssuanceDecision',
    path: '/api/wdCocobdIsDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'treasuryStockAcquisitionDecision',
    path: '/api/tsstkAqDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'treasuryStockDisposalDecision',
    path: '/api/tsstkDpDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'treasuryStockTrustContractDecision',
    path: '/api/tsstkAqTrctrCnsDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'treasuryStockTrustContractTerminationDecision',
    path: '/api/tsstkAqTrctrCcDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'businessAcquisitionDecision',
    path: '/api/bsnInhDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'businessTransferDecision',
    path: '/api/bsnTrfDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'tangibleAssetAcquisitionDecision',
    path: '/api/tgastInhDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'tangibleAssetTransferDecision',
    path: '/api/tgastTrfDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'otherCorporationSecuritiesAcquisitionDecision',
    path: '/api/otcprStkInvscrInhDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'otherCorporationSecuritiesTransferDecision',
    path: '/api/otcprStkInvscrTrfDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'stockRelatedBondAcquisitionDecision',
    path: '/api/stkrtbdInhDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'stockRelatedBondTransferDecision',
    path: '/api/stkrtbdTrfDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'companyMergerDecision',
    path: '/api/cmpMgDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'corporateDivisionDecision',
    path: '/api/cmpDvDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'companyDivisionMergerDecision',
    path: '/api/cmpDvmgDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
  {
    methodName: 'stockExchangeTransferDecision',
    path: '/api/stkExtrDecsn.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bgnDe',
        required: true,
      },
      {
        name: 'endDe',
        required: true,
      },
    ],
  },
];

export type MajorMattersReportMethodName =
  | 'assetTransferPutbackOption'
  | 'defaultOccurrence'
  | 'businessSuspension'
  | 'corporateRehabilitationProceedings'
  | 'dissolutionOccurrence'
  | 'paidInCapitalIncreaseDecision'
  | 'freeCapitalIncreaseDecision'
  | 'paidInAndFreeCapitalIncreaseDecision'
  | 'capitalReductionDecision'
  | 'creditorBankManagementProcedureCommencement'
  | 'lawsuitFiling'
  | 'overseasSecuritiesMarketListingDecision'
  | 'overseasSecuritiesMarketDelistingDecision'
  | 'overseasSecuritiesMarketListingStatus'
  | 'overseasSecuritiesMarketDelistingStatus'
  | 'convertibleBondIssuanceDecision'
  | 'newStockWarrantBondIssuanceDecision'
  | 'exchangeableBondIssuanceDecision'
  | 'creditorBankManagementProcedureTermination'
  | 'writeDownContingentCapitalSecuritiesIssuanceDecision'
  | 'treasuryStockAcquisitionDecision'
  | 'treasuryStockDisposalDecision'
  | 'treasuryStockTrustContractDecision'
  | 'treasuryStockTrustContractTerminationDecision'
  | 'businessAcquisitionDecision'
  | 'businessTransferDecision'
  | 'tangibleAssetAcquisitionDecision'
  | 'tangibleAssetTransferDecision'
  | 'otherCorporationSecuritiesAcquisitionDecision'
  | 'otherCorporationSecuritiesTransferDecision'
  | 'stockRelatedBondAcquisitionDecision'
  | 'stockRelatedBondTransferDecision'
  | 'companyMergerDecision'
  | 'corporateDivisionDecision'
  | 'companyDivisionMergerDecision'
  | 'stockExchangeTransferDecision';
