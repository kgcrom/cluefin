import type { DartEndpointDefinition } from '../../core/types.js';

export const periodicReportFinancialStatementEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'getSingleCompanyMajorAccounts',
    path: '/api/fnlttSinglAcnt.json',
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
    methodName: 'getMultiCompanyMajorAccounts',
    path: '/api/fnlttMultiAcnt.json',
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
    methodName: 'getSingleCompanyFullStatements',
    path: '/api/fnlttSinglAcntAll.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
      fs_div: 'fsDiv',
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
      {
        name: 'fsDiv',
        required: false,
        defaultValue: 'CFS',
      },
    ],
  },
  {
    methodName: 'getSingleCompanyMajorIndicators',
    path: '/api/fnlttSinglIndx.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
      idx_cl_code: 'idxClCode',
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
      {
        name: 'idxClCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getMultiCompanyMajorIndicators',
    path: '/api/fnlttCmpnyIndx.json',
    queryMap: {
      corp_code: 'corpCode',
      bsns_year: 'bsnsYear',
      reprt_code: 'reprtCode',
      idx_cl_code: 'idxClCode',
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
      {
        name: 'idxClCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getXbrlTaxonomy',
    path: '/api/xbrlTaxonomy.json',
    queryMap: {
      sj_div: 'sjDiv',
    },
    responseKind: 'json',
    params: [
      {
        name: 'sjDiv',
        required: true,
      },
    ],
  },
  {
    methodName: 'downloadFinancialStatementXbrl',
    path: '/api/fnlttXbrl.xml',
    queryMap: {
      rcept_no: 'rceptNo',
      reprt_code: 'reprtCode',
    },
    responseKind: 'binary',
    params: [
      {
        name: 'rceptNo',
        required: true,
      },
      {
        name: 'reprtCode',
        required: true,
      },
    ],
  },
];

export type PeriodicReportFinancialStatementMethodName =
  | 'getSingleCompanyMajorAccounts'
  | 'getMultiCompanyMajorAccounts'
  | 'getSingleCompanyFullStatements'
  | 'getSingleCompanyMajorIndicators'
  | 'getMultiCompanyMajorIndicators'
  | 'getXbrlTaxonomy'
  | 'downloadFinancialStatementXbrl';
