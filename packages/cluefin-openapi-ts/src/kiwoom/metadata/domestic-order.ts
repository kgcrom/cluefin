import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticOrderEndpoints: KiwoomEndpointDefinition[] = [
  {
    "methodName": "requestBuyOrder",
    "path": "/api/dostk/ordr",
    "apiId": "kt10000",
    "bodyMap": {
      "dmst_stex_tp": "dmstStexTp",
      "stk_cd": "stkCd",
      "ord_qty": "ordQty",
      "trde_tp": "trdeTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "dmstStexTp",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "trdeTp",
        "required": true
      },
      {
        "name": "ordUv",
        "required": false
      },
      {
        "name": "condUv",
        "required": false
      },
      {
        "name": "contYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "nextKey",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "requestSellOrder",
    "path": "/api/dostk/ordr",
    "apiId": "kt10001",
    "bodyMap": {
      "dmst_stex_tp": "dmstStexTp",
      "stk_cd": "stkCd",
      "ord_qty": "ordQty",
      "trde_tp": "trdeTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "dmstStexTp",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "trdeTp",
        "required": true
      },
      {
        "name": "ordUv",
        "required": false
      },
      {
        "name": "condUv",
        "required": false
      },
      {
        "name": "contYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "nextKey",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "requestModifyOrder",
    "path": "/api/dostk/ordr",
    "apiId": "kt10002",
    "bodyMap": {
      "dmst_stex_tp": "dmstStexTp",
      "orig_ord_no": "origOrdNo",
      "stk_cd": "stkCd",
      "mdfy_qty": "mdfyQty",
      "mdfy_uv": "mdfyUv"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "dmstStexTp",
        "required": true
      },
      {
        "name": "origOrdNo",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "mdfyQty",
        "required": true
      },
      {
        "name": "mdfyUv",
        "required": true
      },
      {
        "name": "mdfyCondUv",
        "required": false
      },
      {
        "name": "contYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "nextKey",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "requestCancelOrder",
    "path": "/api/dostk/ordr",
    "apiId": "kt10003",
    "bodyMap": {
      "dmst_stex_tp": "dmstStexTp",
      "orig_ord_no": "origOrdNo",
      "stk_cd": "stkCd",
      "cncl_qty": "cnclQty"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "dmstStexTp",
        "required": true
      },
      {
        "name": "origOrdNo",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "cnclQty",
        "required": true
      },
      {
        "name": "contYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "nextKey",
        "required": false,
        "defaultValue": ""
      }
    ]
  }
];

export type DomesticOrderMethodName =
  | 'requestBuyOrder'
  | 'requestSellOrder'
  | 'requestModifyOrder'
  | 'requestCancelOrder';
