import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticThemeEndpoints: KiwoomEndpointDefinition[] = [
  {
    "methodName": "getThemeGroup",
    "path": "/api/dostk/thme",
    "apiId": "ka90001",
    "bodyMap": {
      "qry_tp": "qryTp",
      "date_tp": "dateTp",
      "thema_nm": "themaNm",
      "flu_pl_amt_tp": "fluPlAmtTp",
      "stex_tp": "stexTp",
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "qryTp",
        "required": true
      },
      {
        "name": "dateTp",
        "required": true
      },
      {
        "name": "themaNm",
        "required": true
      },
      {
        "name": "fluPlAmtTp",
        "required": true
      },
      {
        "name": "stexTp",
        "required": true
      },
      {
        "name": "stkCd",
        "required": false,
        "defaultValue": ""
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
    "methodName": "getThemeGroupStocks",
    "path": "/api/dostk/thme",
    "apiId": "ka90002",
    "bodyMap": {
      "thema_grp_cd": "themaGrpCd",
      "stex_tp": "stexTp",
      "date_tp": "dateTp"
    },
    "headerParamMap": {
      "cond-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "themaGrpCd",
        "required": true
      },
      {
        "name": "stexTp",
        "required": true
      },
      {
        "name": "dateTp",
        "required": false,
        "defaultValue": ""
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

export type DomesticThemeMethodName =
  | 'getThemeGroup'
  | 'getThemeGroupStocks';
