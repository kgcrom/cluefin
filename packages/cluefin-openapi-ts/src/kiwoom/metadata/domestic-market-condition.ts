import type { KiwoomEndpointDefinition } from '../../core/types';

export const domesticMarketConditionEndpoints: KiwoomEndpointDefinition[] = [
  {
    "methodName": "getStockQuote",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10004",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getStockQuoteByDate",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10005",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getStockPrice",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10006",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getMarketSentimentInfo",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10007",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getNewStockWarrantPrice",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10011",
    "bodyMap": {
      "newstk_recvrht_tp": "newstkRecvrhtTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "newstkRecvrhtTp",
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
  },
  {
    "methodName": "getDailyInstitutionalTradingItems",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10044",
    "bodyMap": {
      "strt_dt": "strtDt",
      "end_dt": "endDt",
      "trde_tp": "trdeTp",
      "mrkt_tp": "mrktTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "strtDt",
        "required": true
      },
      {
        "name": "endDt",
        "required": true
      },
      {
        "name": "trdeTp",
        "required": true
      },
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getInstitutionalTradingTrendByStock",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10045",
    "bodyMap": {
      "stk_cd": "stkCd",
      "strt_dt": "strtDt",
      "end_dt": "endDt",
      "orgn_prsm_unp_tp": "orgnPrsmUnpTp",
      "for_prsm_unp_tp": "forPrsmUnpTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "strtDt",
        "required": true
      },
      {
        "name": "endDt",
        "required": true
      },
      {
        "name": "orgnPrsmUnpTp",
        "required": true
      },
      {
        "name": "forPrsmUnpTp",
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
  },
  {
    "methodName": "getExecutionIntensityTrendByTime",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10046",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getExecutionIntensityTrendByDate",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10047",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getIntradayTradingByInvestor",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10063",
    "bodyMap": {
      "mrkt_tp": "mrktTp",
      "amt_qty_tp": "amtQtyTp",
      "invsr": "invsr",
      "frgn_all": "frgnAll",
      "smtm_netprps_tp": "smtmNetprpsTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "invsr",
        "required": true
      },
      {
        "name": "frgnAll",
        "required": true
      },
      {
        "name": "smtmNetprpsTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getAfterMarketTradingByInvestor",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10066",
    "bodyMap": {
      "mrkt_tp": "mrktTp",
      "amt_qty_tp": "amtQtyTp",
      "trde_tp": "trdeTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "trdeTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getSecuritiesFirmTradingTrendByStock",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10078",
    "bodyMap": {
      "mmcm_cd": "mmcmCd",
      "stk_cd": "stkCd",
      "strt_dt": "strtDt",
      "end_dt": "endDt"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "mmcmCd",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "strtDt",
        "required": true
      },
      {
        "name": "endDt",
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
  },
  {
    "methodName": "getDailyStockPrice",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10086",
    "bodyMap": {
      "stk_cd": "stkCd",
      "qry_dt": "qryDt",
      "indc_tp": "indcTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "qryDt",
        "required": true
      },
      {
        "name": "indcTp",
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
  },
  {
    "methodName": "getAfterHoursSinglePrice",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10087",
    "bodyMap": {
      "stk_cd": "stkCd"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "stkCd",
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
  },
  {
    "methodName": "getProgramTradingTrendByTime",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90005",
    "bodyMap": {
      "date": "date",
      "amt_qty_tp": "amtQtyTp",
      "mrkt_tp": "mrktTp",
      "min_tic_tp": "minTicTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "date",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "minTicTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getProgramTradingArbitrageBalanceTrend",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90006",
    "bodyMap": {
      "date": "date",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "date",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getProgramTradingCumulativeTrend",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90007",
    "bodyMap": {
      "date": "date",
      "amt_qty_tp": "amtQtyTp",
      "mrkt_tp": "mrktTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "date",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getProgramTradingTrendByStockAndTime",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90008",
    "bodyMap": {
      "amt_qty_tp": "amtQtyTp",
      "stk_cd": "stkCd",
      "date": "date"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "date",
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
  },
  {
    "methodName": "getProgramTradingTrendByDate",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90010",
    "bodyMap": {
      "date": "date",
      "amt_qty_tp": "amtQtyTp",
      "mrkt_tp": "mrktTp",
      "min_tic_tp": "minTicTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "date",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "minTicTp",
        "required": true
      },
      {
        "name": "stexTp",
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
  },
  {
    "methodName": "getProgramTradingTrendByStockAndDate",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka90013",
    "bodyMap": {
      "amt_qty_tp": "amtQtyTp",
      "stk_cd": "stkCd",
      "date": "date"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "stkCd",
        "required": true
      },
      {
        "name": "date",
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
  },
  {
    "methodName": "getTopIntradayTradingByInvestor",
    "path": "/api/dostk/mrkcond",
    "apiId": "ka10063",
    "bodyMap": {
      "trde_tp": "trdeTp",
      "mrkt_tp": "mrktTp",
      "orgn_tp": "orgnTp",
      "amt_qty_tp": "amtQtyTp",
      "invsr": "invsr",
      "frgn_all": "frgnAll",
      "smtm_netprps_tp": "smtmNetprpsTp",
      "stex_tp": "stexTp"
    },
    "headerParamMap": {
      "cont-yn": "contYn",
      "next-key": "nextKey"
    },
    "params": [
      {
        "name": "trdeTp",
        "required": true
      },
      {
        "name": "mrktTp",
        "required": true
      },
      {
        "name": "orgnTp",
        "required": true
      },
      {
        "name": "amtQtyTp",
        "required": true
      },
      {
        "name": "invsr",
        "required": true
      },
      {
        "name": "frgnAll",
        "required": true
      },
      {
        "name": "smtmNetprpsTp",
        "required": true
      },
      {
        "name": "stexTp",
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

export type DomesticMarketConditionMethodName =
  | 'getStockQuote'
  | 'getStockQuoteByDate'
  | 'getStockPrice'
  | 'getMarketSentimentInfo'
  | 'getNewStockWarrantPrice'
  | 'getDailyInstitutionalTradingItems'
  | 'getInstitutionalTradingTrendByStock'
  | 'getExecutionIntensityTrendByTime'
  | 'getExecutionIntensityTrendByDate'
  | 'getIntradayTradingByInvestor'
  | 'getAfterMarketTradingByInvestor'
  | 'getSecuritiesFirmTradingTrendByStock'
  | 'getDailyStockPrice'
  | 'getAfterHoursSinglePrice'
  | 'getProgramTradingTrendByTime'
  | 'getProgramTradingArbitrageBalanceTrend'
  | 'getProgramTradingCumulativeTrend'
  | 'getProgramTradingTrendByStockAndTime'
  | 'getProgramTradingTrendByDate'
  | 'getProgramTradingTrendByStockAndDate'
  | 'getTopIntradayTradingByInvestor';
