import type { NhplugEndpointDefinition } from '../../core/types.js';

export const commonEndpoints: NhplugEndpointDefinition[] = [
  {
    methodName: 'getAccountList',
    path: '/n2/acctinfo',
    bodyMap: {},
    supportsCts: true,
    params: [
      {
        name: 'cts',
        required: false,
      },
    ],
  },
  {
    methodName: 'closeWebsocketSession',
    path: '/websocket/close/session',
    bodyMap: {},
    supportsCts: false,
    params: [],
  },
];

export type CommonMethodName = 'getAccountList' | 'closeWebsocketSession';
