import type { DartEndpointDefinition } from '../../core/types.js';

export const publicDisclosureEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'publicDisclosureSearch',
    path: '/api/list.json',
    queryMap: {
      corp_code: 'corpCode',
      bgn_de: 'bgnDe',
      end_de: 'endDe',
      last_reprt_at: 'lastReprtAt',
      pblntf_ty: 'pblntfTy',
      pblntf_detail_ty: 'pblntfDetailTy',
      corp_cls: 'corpCls',
      sort: 'sort',
      sort_mth: 'sortMth',
      page_no: 'pageNo',
      page_count: 'pageCount',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: false,
      },
      {
        name: 'bgnDe',
        required: false,
      },
      {
        name: 'endDe',
        required: false,
      },
      {
        name: 'lastReprtAt',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'pblntfTy',
        required: false,
      },
      {
        name: 'pblntfDetailTy',
        required: false,
      },
      {
        name: 'corpCls',
        required: false,
      },
      {
        name: 'sort',
        required: false,
      },
      {
        name: 'sortMth',
        required: false,
      },
      {
        name: 'pageNo',
        required: false,
      },
      {
        name: 'pageCount',
        required: false,
      },
    ],
  },
  {
    methodName: 'companyOverview',
    path: '/api/company.json',
    queryMap: {
      corp_code: 'corpCode',
    },
    responseKind: 'json',
    params: [
      {
        name: 'corpCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'disclosureDocumentFile',
    path: '/api/document.xml',
    queryMap: {
      rcept_no: 'rceptNo',
    },
    responseKind: 'binary',
    params: [
      {
        name: 'rceptNo',
        required: true,
      },
    ],
  },
  {
    methodName: 'corpCode',
    path: '/api/corpCode.xml',
    queryMap: {},
    responseKind: 'binary',
    params: [],
  },
];

export type PublicDisclosureMethodName =
  | 'publicDisclosureSearch'
  | 'companyOverview'
  | 'disclosureDocumentFile'
  | 'corpCode';
