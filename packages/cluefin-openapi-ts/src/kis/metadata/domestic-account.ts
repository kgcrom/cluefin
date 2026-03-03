import type { KisEndpointDefinition } from '../../core/types';

export const domesticAccountEndpoints: KisEndpointDefinition[] = [
  {
    "methodName": "requestStockQuoteCurrent",
    "method": "POST",
    "path": "/uapi/domestic-stock/v1/trading/order-cash",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "SLL_TYPE": "sllType",
      "ORD_DVSN": "ordDvsn",
      "ORD_QTY": "ordQty",
      "ORD_UNPR": "ordUnpr",
      "CNDT_PRIC": "cndtPric",
      "EXCG_ID_DVSN_CD": "excgIdDvsnCd"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "ordDvsn",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "sllType",
        "required": false,
        "defaultValue": "01"
      },
      {
        "name": "cndtPric",
        "required": false
      },
      {
        "name": "excgIdDvsnCd",
        "required": false
      }
    ]
  },
  {
    "methodName": "requestStockQuoteCredit",
    "method": "POST",
    "path": "/uapi/domestic-stock/v1/trading/order-credit",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "CRDT_TYPE": "crdtType",
      "LOAN_DT": "loanDt",
      "ORD_DVSN": "ordDvsn",
      "ORD_QTY": "ordQty",
      "ORD_UNPR": "ordUnpr",
      "RSVN_ORD_YN": "rsvnOrdYn",
      "EMGC_ORD_YN": "emgcOrdYn",
      "PGTR_DVSN": "pgtrDvsn",
      "LQTY_TR_NGTN_DTL_NO": "lqtyTrNgtnDtlNo",
      "LQTY_TR_AGMT_NO": "lqtyTrAgmtNo",
      "LQTY_TR_NGTN_ID": "lqtyTrNgtnId",
      "LP_ORD_YN": "lpOrdYn",
      "MDIA_ODNO": "mdiaOdno",
      "ORD_SVR_DVSN_CD": "ordSvrDvsnCd",
      "PGM_NMPR_STMT_DVSN_CD": "pgmNmprStmtDvsnCd",
      "CVRG_SLCT_RSON_CD": "cvrgSlctRsonCd",
      "CVRG_SEQ": "cvrgSeq",
      "EXCG_ID_DVSN_CD": "excgIdDvsnCd",
      "CNDT_PRIC": "cndtPric"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "crdtType",
        "required": true
      },
      {
        "name": "loanDt",
        "required": true
      },
      {
        "name": "ordDvsn",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "rsvnOrdYn",
        "required": false
      },
      {
        "name": "emgcOrdYn",
        "required": false
      },
      {
        "name": "pgtrDvsn",
        "required": false
      },
      {
        "name": "lqtyTrNgtnDtlNo",
        "required": false
      },
      {
        "name": "lqtyTrAgmtNo",
        "required": false
      },
      {
        "name": "lqtyTrNgtnId",
        "required": false
      },
      {
        "name": "lpOrdYn",
        "required": false
      },
      {
        "name": "mdiaOdno",
        "required": false
      },
      {
        "name": "ordSvrDvsnCd",
        "required": false
      },
      {
        "name": "pgmNmprStmtDvsnCd",
        "required": false
      },
      {
        "name": "cvrgSlctRsonCd",
        "required": false
      },
      {
        "name": "cvrgSeq",
        "required": false
      },
      {
        "name": "excgIdDvsnCd",
        "required": false
      },
      {
        "name": "cndtPric",
        "required": false
      }
    ]
  },
  {
    "methodName": "requestStockQuoteCorrection",
    "method": "POST",
    "path": "/uapi/domestic-stock/v1/trading/order-rvsecncl",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "KRX_FWDG_ORD_ORGNO": "krxFwdgOrdOrgno",
      "ORGN_ODNO": "orgnOdno",
      "ORD_DVSN": "ordDvsn",
      "RVSE_CNCL_DVSN_CD": "rvseCnclDvsnCd",
      "ORD_QTY": "ordQty",
      "ORD_UNPR": "ordUnpr",
      "QTY_ALL_ORD_YN": "qtyAllOrdYn",
      "EXCG_ID_DVSN_CD": "excgIdDvsnCd"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "krxFwdgOrdOrgno",
        "required": true
      },
      {
        "name": "orgnOdno",
        "required": true
      },
      {
        "name": "ordDvsn",
        "required": true
      },
      {
        "name": "rvseCnclDvsnCd",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "qtyAllOrdYn",
        "required": true
      },
      {
        "name": "excgIdDvsnCd",
        "required": false
      }
    ]
  },
  {
    "methodName": "getStockCorrectionCancellableQty",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100",
      "INQR_DVSN_1": "inqrDvsn1",
      "INQR_DVSN_2": "inqrDvsn2"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "inqrDvsn1",
        "required": true
      },
      {
        "name": "inqrDvsn2",
        "required": true
      }
    ]
  },
  {
    "methodName": "getStockDailySeparateConclusion",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-daily-ccld",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "INQR_STRT_DT": "inqrStrtDt",
      "INQR_END_DT": "inqrEndDt",
      "SLL_BUY_DVSN_CD": "sllBuyDvsnCd",
      "ORD_GNO_BRNO": "ordGnoBrno",
      "CCLD_DVSN": "ccldDvsn",
      "INQR_DVSN": "inqrDvsn",
      "INQR_DVSN_1": "inqrDvsn1",
      "INQR_DVSN_3": "inqrDvsn3",
      "EXCG_ID_DVSN_CD": "excgIdDvsnCd",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100",
      "PDNO": "pdno",
      "ODNO": "odno"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "inqrStrtDt",
        "required": true
      },
      {
        "name": "inqrEndDt",
        "required": true
      },
      {
        "name": "sllBuyDvsnCd",
        "required": true
      },
      {
        "name": "ccldDvsn",
        "required": true
      },
      {
        "name": "inqrDvsn",
        "required": true
      },
      {
        "name": "inqrDvsn1",
        "required": true
      },
      {
        "name": "inqrDvsn3",
        "required": true
      },
      {
        "name": "excgIdDvsnCd",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "ordGnoBrno",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "pdno",
        "required": false
      },
      {
        "name": "odno",
        "required": false
      }
    ]
  },
  {
    "methodName": "getStockBalance",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-balance",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "AFHR_FLPR_YN": "afhrFlprYn",
      "INQR_DVSN": "inqrDvsn",
      "FUND_STTL_ICLD_YN": "fundSttlIcldYn",
      "PRCS_DVSN": "prcsDvsn",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "inqrDvsn",
        "required": true
      },
      {
        "name": "fundSttlIcldYn",
        "required": true
      },
      {
        "name": "prcsDvsn",
        "required": true
      },
      {
        "name": "afhrFlprYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "ctxAreaFk100",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "ctxAreaNk100",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "getBuyTradableInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-psbl-order",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "AFHR_FLPR_YN": "afhrFlprYn",
      "INQR_DVSN": "inqrDvsn",
      "FUND_STTL_ICLD_YN": "fundSttlIcldYn",
      "PRCS_DVSN": "prcsDvsn",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "afhrFlprYn",
        "required": true
      },
      {
        "name": "inqrDvsn",
        "required": true
      },
      {
        "name": "fundSttlIcldYn",
        "required": true
      },
      {
        "name": "prcsDvsn",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "ctxAreaNk100",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "getSellTradableInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-psbl-sell",
    "trId": "TTTC8408R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      }
    ]
  },
  {
    "methodName": "getCreditTradableInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-credit-psamount",
    "trId": "TTTC8909R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "ORD_UNPR": "ordUnpr",
      "ORD_DVSN": "ordDvsn",
      "CRDT_TYPE": "crdtType",
      "CMA_EVLU_AMT_ICLD_YN": "cmaEvluAmtIcldYn",
      "OVRS_ICLD_YN": "ovrsIcldYn"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "ordDvsn",
        "required": true
      },
      {
        "name": "crdtType",
        "required": true
      },
      {
        "name": "cmaEvluAmtIcldYn",
        "required": true
      },
      {
        "name": "ovrsIcldYn",
        "required": true
      }
    ]
  },
  {
    "methodName": "requestStockReserveQuote",
    "method": "POST",
    "path": "/uapi/domestic-stock/v1/trading/order-resv",
    "trId": "CTSC0008U",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "ORD_QTY": "ordQty",
      "ORD_UNPR": "ordUnpr",
      "SLL_BUY_DVSN_CD": "sllBuyDvsnCd",
      "ORD_DVSN_CD": "ordDvsnCd",
      "ORD_OBJT_CBLC_DVSN_CD": "ordObjtCblcDvsnCd",
      "LOAN_DT": "loanDt",
      "RSVN_ORD_END_DT": "rsvnOrdEndDt",
      "LDNG_DT": "ldngDt"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "sllBuyDvsnCd",
        "required": true
      },
      {
        "name": "ordDvsnCd",
        "required": true
      },
      {
        "name": "ordObjtCblcDvsnCd",
        "required": true
      },
      {
        "name": "loanDt",
        "required": false
      },
      {
        "name": "rsvnOrdEndDt",
        "required": false
      },
      {
        "name": "ldngDt",
        "required": false
      }
    ]
  },
  {
    "methodName": "requestStockReserveQuoteCorrection",
    "method": "POST",
    "path": "/uapi/domestic-stock/v1/trading/order-resv-rvsecncl",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "RSVN_ORD_SEQ": "rsvnOrdSeq",
      "ORD_QTY": "ordQty",
      "ORD_UNPR": "ordUnpr",
      "SLL_BUY_DVSN_CD": "sllBuyDvsnCd",
      "ORD_DVSN_CD": "ordDvsnCd",
      "ORD_OBJT_CBLC_DVSN_CD": "ordObjtCblcDvsnCd",
      "CTAL_TLNO": "ctalTlno",
      "LOAN_DT": "loanDt",
      "RSVN_ORD_END_DT": "rsvnOrdEndDt",
      "RSVN_ORD_ORGNO": "rsvnOrdOrgno",
      "RSVN_ORD_ORD_DT": "rsvnOrdOrdDt"
    },
    "params": [
      {
        "name": "trId",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "rsvnOrdSeq",
        "required": true
      },
      {
        "name": "ordQty",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "sllBuyDvsnCd",
        "required": true
      },
      {
        "name": "ordDvsnCd",
        "required": true
      },
      {
        "name": "ordObjtCblcDvsnCd",
        "required": true
      },
      {
        "name": "ctalTlno",
        "required": true
      },
      {
        "name": "loanDt",
        "required": false
      },
      {
        "name": "rsvnOrdEndDt",
        "required": false
      },
      {
        "name": "rsvnOrdOrgno",
        "required": false
      },
      {
        "name": "rsvnOrdOrdDt",
        "required": false
      }
    ]
  },
  {
    "methodName": "getStockReserveQuoteInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/order-resv-ccnl",
    "trId": "CTSC0004R",
    "requestMap": {
      "RSVN_ORD_ORD_DT": "rsvnOrdOrdDt",
      "RSVN_ORD_END_DT": "rsvnOrdEndDt",
      "RSVN_ORD_SEQ": "rsvnOrdSeq",
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PRCS_DVSN_CD": "prcsDvsnCd",
      "CNCL_YN": "cnclYn",
      "PDNO": "pdno",
      "SLL_BUY_DVSN_CD": "sllBuyDvsnCd",
      "CTX_AREA_FK200": "ctxAreaFk200",
      "CTX_AREA_NK200": "ctxAreaNk200"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "rsvnOrdOrdDt",
        "required": true
      },
      {
        "name": "rsvnOrdEndDt",
        "required": true
      },
      {
        "name": "rsvnOrdSeq",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "prcsDvsnCd",
        "required": true
      },
      {
        "name": "cnclYn",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "sllBuyDvsnCd",
        "required": true
      },
      {
        "name": "ctxAreaFk200",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "ctxAreaNk200",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "getPensionConclusionBalance",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/pension/inquire-present-balance",
    "trId": "TTTC2202R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "USER_DVSN_CD": "userDvsnCd",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": false,
        "defaultValue": "29"
      },
      {
        "name": "userDvsnCd",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getPensionNotConclusionHistory",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/pension/inquire-daily-ccld",
    "trId": "TTTC2210R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "USER_DVSN_CD": "userDvsnCd",
      "SLL_BUY_DVSN_CD": "sllBuyDvsnCd",
      "CCLD_NCCS_DVSN": "ccldNccsDvsn",
      "INQR_DVSN_3": "inqrDvsn3",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "sllBuyDvsnCd",
        "required": true
      },
      {
        "name": "ccldNccsDvsn",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": false,
        "defaultValue": "29"
      },
      {
        "name": "inqrDvsn3",
        "required": false,
        "defaultValue": "00"
      },
      {
        "name": "userDvsnCd",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getPensionBuyTradableInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/pension/inquire-psbl-order",
    "trId": "TTTC0503R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "ACCA_DVSN_CD": "accaDvsnCd",
      "CMA_EVLU_AMT_ICLD_YN": "cmaEvluAmtIcldYn",
      "ORD_DVSN": "ordDvsn",
      "ORD_UNPR": "ordUnpr"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "cmaEvluAmtIcldYn",
        "required": true
      },
      {
        "name": "ordDvsn",
        "required": true
      },
      {
        "name": "ordUnpr",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": false,
        "defaultValue": "29"
      },
      {
        "name": "accaDvsnCd",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getPensionReserveDepositInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/pension/inquire-deposit",
    "trId": "TTTC0506R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "USER_DVSN_CD": "userDvsnCd"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": false,
        "defaultValue": "29"
      },
      {
        "name": "userDvsnCd",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getPensionBalanceInquiry",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/pension/inquire-balance",
    "trId": "TTTC2208R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "USER_DVSN_CD": "userDvsnCd",
      "INQR_DVSN": "inqrDvsn",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": false,
        "defaultValue": "29"
      },
      {
        "name": "userDvsnCd",
        "required": false,
        "defaultValue": "00"
      },
      {
        "name": "inqrDvsn",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getStockBalanceLossProfit",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-balance-rlz-pl",
    "trId": "TTTC8494R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "AFHR_FLPR_YN": "afhrFlprYn",
      "OFL_YN": "oflYn",
      "INQR_DVSN": "inqrDvsn",
      "UNPR_DVSN": "unprDvsn",
      "FUND_STTL_ICLD_YN": "fundSttlIcldYn",
      "FNCG_AMT_AUTO_RDPT_YN": "fncgAmtAutoRdptYn",
      "PRCS_DVSN": "prcsDvsn",
      "COST_ICLD_YN": "costIcldYn",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CTX_AREA_NK100": "ctxAreaNk100"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "afhrFlprYn",
        "required": true
      },
      {
        "name": "costIcldYn",
        "required": true
      },
      {
        "name": "oflYn",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "inqrDvsn",
        "required": false,
        "defaultValue": "00"
      },
      {
        "name": "unprDvsn",
        "required": false,
        "defaultValue": "01"
      },
      {
        "name": "fundSttlIcldYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "fncgAmtAutoRdptYn",
        "required": false,
        "defaultValue": "N"
      },
      {
        "name": "prcsDvsn",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getInvestmentAccountCurrentStatus",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-account-balance",
    "trId": "CTRP6548R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "INQR_DVSN_1": "inqrDvsn1",
      "BSPR_BF_DT_APLY_YN": "bsprBfDtAplyYn"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "inqrDvsn1",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "bsprBfDtAplyYn",
        "required": false,
        "defaultValue": ""
      }
    ]
  },
  {
    "methodName": "getPeriodProfitSummary",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-period-profit",
    "trId": "TTTC8708R",
    "requestMap": {
      "ACNT_PRDT_CD": "acntPrdtCd",
      "CANO": "cano",
      "INQR_STRT_DT": "inqrStrtDt",
      "INQR_END_DT": "inqrEndDt",
      "PDNO": "pdno",
      "CTX_AREA_NK100": "ctxAreaNk100",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "SORT_DVSN": "sortDvsn",
      "INQR_DVSN": "inqrDvsn",
      "CBLC_DVSN": "cblcDvsn"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "inqrStrtDt",
        "required": true
      },
      {
        "name": "inqrEndDt",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "sortDvsn",
        "required": true
      },
      {
        "name": "inqrDvsn",
        "required": false,
        "defaultValue": "00"
      },
      {
        "name": "cblcDvsn",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getPeriodTradingProfitStatus",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/inquire-period-trade-profit",
    "trId": "TTTC8715R",
    "requestMap": {
      "CANO": "cano",
      "SORT_DVSN": "sortDsvn",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "PDNO": "pdno",
      "INQR_STRT_DT": "inqrStrtDt",
      "INQR_END_DT": "inqrEndDt",
      "CTX_AREA_NK100": "ctxAreaNk100",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "CBLC_DVSN": "cblcDvsn"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "sortDsvn",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "pdno",
        "required": true
      },
      {
        "name": "inqrStrtDt",
        "required": true
      },
      {
        "name": "inqrEndDt",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "cblcDvsn",
        "required": false,
        "defaultValue": "00"
      }
    ]
  },
  {
    "methodName": "getStockIntegratedDepositBalance",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/intgr-margin",
    "trId": "TTTC0869R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "WCRC_FRCR_DVSN_CD": "wcrcFrcrDvsnCd",
      "FWEX_CTRT_FRCR_DVSN_CD": "fwexCtrtFrcrDvsnCd",
      "CMA_EVLU_AMT_ICLD_YN": "cmaEvluAmtIcldYn"
    },
    "params": [
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "wcrcFrcrDvsnCd",
        "required": true
      },
      {
        "name": "fwexCtrtFrcrDvsnCd",
        "required": true
      },
      {
        "name": "cmaEvluAmtIcldYn",
        "required": false,
        "defaultValue": "N"
      }
    ]
  },
  {
    "methodName": "getPeriodAccountingCurrentStatus",
    "method": "GET",
    "path": "/uapi/domestic-stock/v1/trading/period-rights",
    "trId": "CTRGA011R",
    "requestMap": {
      "CANO": "cano",
      "ACNT_PRDT_CD": "acntPrdtCd",
      "INQR_STRT_DT": "inqrStrtDt",
      "INQR_END_DT": "inqrEndDt",
      "CTX_AREA_NK100": "ctxAreaNk100",
      "CTX_AREA_FK100": "ctxAreaFk100",
      "INQR_DVSN": "inqrDvsn",
      "CUST_RNCNO25": "custRncno25",
      "HMID": "hmid",
      "RGHT_TYPE_CD": "rghtTypeCd",
      "PDNO": "pdno",
      "PRDT_TYPE_CD": "prdtTypeCd"
    },
    "params": [
      {
        "name": "trCont",
        "required": true
      },
      {
        "name": "cano",
        "required": true
      },
      {
        "name": "acntPrdtCd",
        "required": true
      },
      {
        "name": "inqrStrtDt",
        "required": true
      },
      {
        "name": "inqrEndDt",
        "required": true
      },
      {
        "name": "ctxAreaNk100",
        "required": true
      },
      {
        "name": "ctxAreaFk100",
        "required": true
      },
      {
        "name": "inqrDvsn",
        "required": false,
        "defaultValue": "03"
      },
      {
        "name": "custRncno25",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "hmid",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "rghtTypeCd",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "pdno",
        "required": false,
        "defaultValue": ""
      },
      {
        "name": "prdtTypeCd",
        "required": false,
        "defaultValue": ""
      }
    ]
  }
];

export type DomesticAccountMethodName =
  | 'requestStockQuoteCurrent'
  | 'requestStockQuoteCredit'
  | 'requestStockQuoteCorrection'
  | 'getStockCorrectionCancellableQty'
  | 'getStockDailySeparateConclusion'
  | 'getStockBalance'
  | 'getBuyTradableInquiry'
  | 'getSellTradableInquiry'
  | 'getCreditTradableInquiry'
  | 'requestStockReserveQuote'
  | 'requestStockReserveQuoteCorrection'
  | 'getStockReserveQuoteInquiry'
  | 'getPensionConclusionBalance'
  | 'getPensionNotConclusionHistory'
  | 'getPensionBuyTradableInquiry'
  | 'getPensionReserveDepositInquiry'
  | 'getPensionBalanceInquiry'
  | 'getStockBalanceLossProfit'
  | 'getInvestmentAccountCurrentStatus'
  | 'getPeriodProfitSummary'
  | 'getPeriodTradingProfitStatus'
  | 'getStockIntegratedDepositBalance'
  | 'getPeriodAccountingCurrentStatus';
