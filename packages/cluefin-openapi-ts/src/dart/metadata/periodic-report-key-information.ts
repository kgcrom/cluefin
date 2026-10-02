import type { DartEndpointDefinition } from '../../core/types.js';

export const periodicReportKeyInformationEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'getCapitalChangeStatus',
    path: '/api/irdsSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getDividendInformation',
    path: '/api/alotMatter.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getTreasuryStockActivity',
    path: '/api/tesstkAcqsDspsSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMajorShareholderStatus',
    path: '/api/hyslrSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMajorShareholderChanges',
    path: '/api/hyslrChgSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMinorityShareholderStatus',
    path: '/api/mrhlSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getExecutiveStatus',
    path: '/api/exctvSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getEmployeeStatus',
    path: '/api/empSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getBoardAndAuditCompensationAbove500m',
    path: '/api/hmvAuditIndvdlBySttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getBoardAndAuditTotalCompensation',
    path: '/api/hmvAuditAllSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getTopFiveIndividualCompensation',
    path: '/api/indvdlByPay.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOtherCorporationInvestments',
    path: '/api/otrCprInvstmntSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getTotalNumberOfShares',
    path: '/api/stockTotqySttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getDebtSecuritiesIssuancePerformance',
    path: '/api/detScritsIsuAcmslt.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutstandingCommercialPaperBalance',
    path: '/api/entrprsBilScritsNrdmpBlce.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutstandingShortTermBonds',
    path: '/api/srtpdPsndbtNrdmpBlce.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutstandingCorporateBonds',
    path: '/api/cprndNrdmpBlce.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutstandingHybridCapitalSecurities',
    path: '/api/newCaplScritsNrdmpBlce.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutstandingContingentCapitalSecurities',
    path: '/api/cndlCaplScritsNrdmpBlce.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getAuditorNameAndOpinion',
    path: '/api/accnutAdtorNmNdAdtOpinion.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getAuditServiceContracts',
    path: '/api/adtServcCnclsSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getNonAuditServiceContracts',
    path: '/api/accnutAdtorNonAdtServcCnclsSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getOutsideDirectorStatus',
    path: '/api/outcmpnyDrctrNdChangeSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getUnregisteredExecutiveCompensation',
    path: '/api/unrstExctvMendngSttus.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getBoardAndAuditCompensationShareholderApproved',
    path: '/api/drctrAdtAllMendngSttusGmtsckConfmAmount.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getBoardAndAuditCompensationByType',
    path: '/api/drctrAdtAllMendngSttusMendngPymntamtTyCl.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getPublicOfferingFundUsage',
    path: '/api/pssrpCptalUseDtls.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getPrivatePlacementFundUsage',
    path: '/api/prvsrpCptalUseDtls.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
      {
        name: 'bsnsYear',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
];

export type PeriodicReportKeyInformationMethodName =
  | 'getCapitalChangeStatus'
  | 'getDividendInformation'
  | 'getTreasuryStockActivity'
  | 'getMajorShareholderStatus'
  | 'getMajorShareholderChanges'
  | 'getMinorityShareholderStatus'
  | 'getExecutiveStatus'
  | 'getEmployeeStatus'
  | 'getBoardAndAuditCompensationAbove500m'
  | 'getBoardAndAuditTotalCompensation'
  | 'getTopFiveIndividualCompensation'
  | 'getOtherCorporationInvestments'
  | 'getTotalNumberOfShares'
  | 'getDebtSecuritiesIssuancePerformance'
  | 'getOutstandingCommercialPaperBalance'
  | 'getOutstandingShortTermBonds'
  | 'getOutstandingCorporateBonds'
  | 'getOutstandingHybridCapitalSecurities'
  | 'getOutstandingContingentCapitalSecurities'
  | 'getAuditorNameAndOpinion'
  | 'getAuditServiceContracts'
  | 'getNonAuditServiceContracts'
  | 'getOutsideDirectorStatus'
  | 'getUnregisteredExecutiveCompensation'
  | 'getBoardAndAuditCompensationShareholderApproved'
  | 'getBoardAndAuditCompensationByType'
  | 'getPublicOfferingFundUsage'
  | 'getPrivatePlacementFundUsage';
