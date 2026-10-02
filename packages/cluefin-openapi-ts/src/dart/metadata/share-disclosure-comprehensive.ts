import type { DartEndpointDefinition } from '../../core/types.js';

export const shareDisclosureComprehensiveEndpoints: DartEndpointDefinition[] = [
  {
    methodName: 'largeHoldingReport',
    path: '/api/majorstock.json',
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
    methodName: 'executiveMajorShareholderOwnershipReport',
    path: '/api/elestock.json',
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
];

export type ShareDisclosureComprehensiveMethodName = 'largeHoldingReport' | 'executiveMajorShareholderOwnershipReport';
