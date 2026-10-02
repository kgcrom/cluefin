import type { DartEndpointDefinition } from '../../core/types.js';

export const majorShareholderDisclosureEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'treasuryStockAcquisitionDisposalPlan',
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
    methodName: 'realEstateDevelopment',
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
    methodName: 'businessLetter',
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
    methodName: 'securitiesGrantedDecision',
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
    methodName: 'freeSecuritiesDecision',
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
    methodName: 'paidInCapitalReductionDecision',
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
    methodName: 'governmentBondManagerReplacement',
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
    methodName: 'profitRevocation',
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
    methodName: 'overseasSecuritiesTradingResolution',
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
    methodName: 'overseasSecuritiesTradingDelistingResolution',
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
    methodName: 'overseasSecuritiesTradingStatus',
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
    methodName: 'overseasSecuritiesTradingStatusDelisting',
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
    methodName: 'corporateBondIssuanceDecision',
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
    methodName: 'governmentBondManagerTransferTermination',
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
    methodName: 'reorganizationPlanApprovedRuling',
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
    methodName: 'businessPlanDecision',
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
    methodName: 'tangibleAssetPlanDecision',
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
    methodName: 'retirementStockInvestmentPlanDecision',
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
    methodName: 'retirementStockInvestmentTransferDecision',
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
    methodName: 'stockRelatedBondPlanDecision',
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
    methodName: 'corporateLawDecision',
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
    methodName: 'corporateLawMethodDecision',
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
    methodName: 'stockTradingOtherDecision',
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

export type MajorShareholderDisclosureMethodName =
  | 'treasuryStockAcquisitionDisposalPlan'
  | 'realEstateDevelopment'
  | 'businessLetter'
  | 'corporateRehabilitationProceedings'
  | 'dissolutionOccurrence'
  | 'securitiesGrantedDecision'
  | 'freeSecuritiesDecision'
  | 'paidInCapitalReductionDecision'
  | 'capitalReductionDecision'
  | 'governmentBondManagerReplacement'
  | 'profitRevocation'
  | 'overseasSecuritiesTradingResolution'
  | 'overseasSecuritiesTradingDelistingResolution'
  | 'overseasSecuritiesTradingStatus'
  | 'overseasSecuritiesTradingStatusDelisting'
  | 'convertibleBondIssuanceDecision'
  | 'newStockWarrantBondIssuanceDecision'
  | 'corporateBondIssuanceDecision'
  | 'governmentBondManagerTransferTermination'
  | 'reorganizationPlanApprovedRuling'
  | 'treasuryStockAcquisitionDecision'
  | 'treasuryStockDisposalDecision'
  | 'treasuryStockTrustContractDecision'
  | 'treasuryStockTrustContractTerminationDecision'
  | 'businessPlanDecision'
  | 'businessTransferDecision'
  | 'tangibleAssetPlanDecision'
  | 'tangibleAssetTransferDecision'
  | 'retirementStockInvestmentPlanDecision'
  | 'retirementStockInvestmentTransferDecision'
  | 'stockRelatedBondPlanDecision'
  | 'stockRelatedBondTransferDecision'
  | 'corporateLawDecision'
  | 'corporateDivisionDecision'
  | 'corporateLawMethodDecision'
  | 'stockTradingOtherDecision';
