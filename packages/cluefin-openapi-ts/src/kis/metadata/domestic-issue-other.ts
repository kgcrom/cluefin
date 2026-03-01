import type { KisEndpointDefinition } from '../../core/types';

export const domesticIssueOtherEndpoints: KisEndpointDefinition[] = [
  {
    "methodName": "getSectorCurrentIndex",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-index-price",
    "trId": "FHPUP02100000",
    "requestMap": {
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_INPUT_ISCD": "fidInputIscd"
    },
    "params": [
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorDailyIndex",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-index-daily-price",
    "trId": "FHPUP02120000",
    "requestMap": {
      "FID_PERIOD_DIV_CODE": "fidPeriodDivCode",
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_INPUT_DATE_1": "fidInputDate1"
    },
    "params": [
      {
        "name": "fidPeriodDivCode",
        "required": true
      },
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidInputDate1",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorTimeIndexSecond",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-index-tickprice",
    "trId": "FHPUP02110100",
    "requestMap": {
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode"
    },
    "params": [
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidCondMrktDivCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorTimeIndexMinute",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-index-timeprice",
    "trId": "FHPUP02110200",
    "requestMap": {
      "FID_INPUT_HOUR_1": "fidInputHour1",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode"
    },
    "params": [
      {
        "name": "fidInputHour1",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidCondMrktDivCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorMinuteInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-time-indexchartprice",
    "trId": "FHKUP03500200",
    "requestMap": {
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_ETC_CLS_CODE": "fidEtcClsCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_INPUT_HOUR_1": "fidInputHour1",
      "FID_PW_DATA_INCU_YN": "fidPwDataIncuYn"
    },
    "params": [
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidEtcClsCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidInputHour1",
        "required": true
      },
      {
        "name": "fidPwDataIncuYn",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorPeriodQuote",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice",
    "trId": "FHKUP03500100",
    "requestMap": {
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_INPUT_DATE_1": "fidInputDate1",
      "FID_INPUT_DATE_2": "fidInputDate2",
      "FID_PERIOD_DIV_CODE": "fidPeriodDivCode"
    },
    "params": [
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidInputDate1",
        "required": true
      },
      {
        "name": "fidInputDate2",
        "required": true
      },
      {
        "name": "fidPeriodDivCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getSectorAllQuoteByCategory",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-index-category-price",
    "trId": "FHPUP02140000",
    "requestMap": {
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_COND_SCR_DIV_CODE": "fidCondScrDivCode",
      "FID_MRKT_CLS_CODE": "fidMrktClsCode",
      "FID_BLNG_CLS_CODE": "fidBlngClsCode"
    },
    "params": [
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidCondScrDivCode",
        "required": true
      },
      {
        "name": "fidMrktClsCode",
        "required": true
      },
      {
        "name": "fidBlngClsCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getExpectedIndexTrend",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/exp-index-trend",
    "trId": "FHPST01840000",
    "requestMap": {
      "FID_MKOP_CLS_CODE": "fidMkopClsCode",
      "FID_INPUT_HOUR_1": "fidInputHour1",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode"
    },
    "params": [
      {
        "name": "fidMkopClsCode",
        "required": true
      },
      {
        "name": "fidInputHour1",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidCondMrktDivCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getExpectedIndexAll",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/exp-total-index",
    "trId": "FHKUP11750000",
    "requestMap": {
      "fid_mrkt_cls_code": "fidMrktClsCode",
      "fid_cond_mrkt_div_code": "fidCondMrktDivCode",
      "fid_cond_scr_div_code": "fidCondScrDivCode",
      "fid_input_iscd": "fidInputIscd",
      "fid_mkop_cls_code": "fidMkopClsCode"
    },
    "params": [
      {
        "name": "fidMrktClsCode",
        "required": true
      },
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidCondScrDivCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidMkopClsCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getVolatilityInterruptionStatus",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/inquire-vi-status",
    "trId": "FHPST01390000",
    "requestMap": {
      "FID_DIV_CLS_CODE": "fidDivClsCode",
      "FID_COND_SCR_DIV_CODE": "fidCondScrDivCode",
      "FID_MRKT_CLS_CODE": "fidMrktClsCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_RANK_SORT_CLS_CODE": "fidRankSortClsCode",
      "FID_INPUT_DATE_1": "fidInputDate1",
      "FID_TRGT_CLS_CODE": "fidTrgtClsCode",
      "FID_TRGT_EXLS_CLS_CODE": "fidTrgtExlsClsCode"
    },
    "params": [
      {
        "name": "fidDivClsCode",
        "required": true
      },
      {
        "name": "fidCondScrDivCode",
        "required": true
      },
      {
        "name": "fidMrktClsCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidRankSortClsCode",
        "required": true
      },
      {
        "name": "fidInputDate1",
        "required": true
      },
      {
        "name": "fidTrgtClsCode",
        "required": true
      },
      {
        "name": "fidTrgtExlsClsCode",
        "required": true
      }
    ]
  },
  {
    "methodName": "getInterestRateSummary",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/comp-interest",
    "trId": "FHPST07020000",
    "requestMap": {
      "FID_COND_MRKT_DIV_CODE": "fidCondMrktDivCode",
      "FID_COND_SCR_DIV_CODE": "fidCondScrDivCode",
      "FID_DIV_CLS_CODE": "fidDivClsCode",
      "FID_DIV_CLS_CODE1": "fidDivClsCode1"
    },
    "params": [
      {
        "name": "fidCondMrktDivCode",
        "required": true
      },
      {
        "name": "fidCondScrDivCode",
        "required": true
      },
      {
        "name": "fidDivClsCode",
        "required": true
      },
      {
        "name": "fidDivClsCode1",
        "required": true
      }
    ]
  },
  {
    "methodName": "getMarketAnnouncementSchedule",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/news-title",
    "trId": "FHKST01011800",
    "requestMap": {
      "FID_NEWS_OFER_ENTP_CODE": "fidNewsOferEntpCode",
      "FID_COND_MRKT_CLS_CODE": "fidCondMrktClsCode",
      "FID_INPUT_ISCD": "fidInputIscd",
      "FID_TITL_CNTT": "fidTitlCntt",
      "FID_INPUT_DATE_1": "fidInputDate1",
      "FID_INPUT_HOUR_1": "fidInputHour1",
      "FID_RANK_SORT_CLS_CODE": "fidRankSortClsCode",
      "FID_INPUT_SRNO": "fidInputSrno"
    },
    "params": [
      {
        "name": "fidNewsOferEntpCode",
        "required": true
      },
      {
        "name": "fidCondMrktClsCode",
        "required": true
      },
      {
        "name": "fidInputIscd",
        "required": true
      },
      {
        "name": "fidTitlCntt",
        "required": true
      },
      {
        "name": "fidInputDate1",
        "required": true
      },
      {
        "name": "fidInputHour1",
        "required": true
      },
      {
        "name": "fidRankSortClsCode",
        "required": true
      },
      {
        "name": "fidInputSrno",
        "required": true
      }
    ]
  },
  {
    "methodName": "getHolidayInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/chk-holiday",
    "trId": "CTCA0903R",
    "requestMap": {
      "BASS_DT": "bassDt",
      "CTX_AREA_NK": "ctxAreaNk",
      "CTX_AREA_FK": "ctxAreaFk"
    },
    "params": [
      {
        "name": "bassDt",
        "required": true
      },
      {
        "name": "ctxAreaNk",
        "required": true
      },
      {
        "name": "ctxAreaFk",
        "required": true
      }
    ]
  },
  {
    "methodName": "getFuturesBusinessDayInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/quotations/market-time",
    "trId": "HHMCM000002C0",
    "requestMap": {},
    "params": []
  }
];
