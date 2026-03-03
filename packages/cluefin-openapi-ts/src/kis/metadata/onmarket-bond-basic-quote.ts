import type { KisEndpointDefinition } from '../../core/types';

export const onmarketBondBasicQuoteEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getBondAskingPrice',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/inquire-asking-price',
    trId: 'FHKBJ773401C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'B',
      },
    ],
  },
  {
    methodName: 'getBondPrice',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/inquire-price',
    trId: 'FHKBJ773400C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'B',
      },
    ],
  },
  {
    methodName: 'getBondExecution',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/inquire-ccnl',
    trId: 'FHKBJ773403C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'B',
      },
    ],
  },
  {
    methodName: 'getBondDailyPrice',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/inquire-daily-price',
    trId: 'FHKBJ773404C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'B',
      },
    ],
  },
  {
    methodName: 'getBondDailyChartPrice',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/inquire-daily-itemchartprice',
    trId: 'FHKBJ773701C0',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
    },
    params: [
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: false,
        defaultValue: 'B',
      },
    ],
  },
  {
    methodName: 'getBondAvgUnitPrice',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/avg-unit',
    trId: 'CTPF2005R',
    requestMap: {
      INQR_STRT_DT: 'inqrStrtDt',
      INQR_END_DT: 'inqrEndDt',
      PDNO: 'pdno',
      PRDT_TYPE_CD: 'prdtTypeCd',
      VRFC_KIND_CD: 'vrfcKindCd',
    },
    params: [
      {
        name: 'inqrStrtDt',
        required: true,
      },
      {
        name: 'inqrEndDt',
        required: true,
      },
      {
        name: 'pdno',
        required: false,
        defaultValue: '',
      },
      {
        name: 'prdtTypeCd',
        required: false,
        defaultValue: '302',
      },
      {
        name: 'vrfcKindCd',
        required: false,
        defaultValue: '00',
      },
      {
        name: 'custtype',
        required: false,
        defaultValue: 'P',
      },
    ],
  },
  {
    methodName: 'getBondInfo',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/search-bond-info',
    trId: 'CTPF1114R',
    requestMap: {
      PDNO: 'pdno',
      PRDT_TYPE_CD: 'prdtTypeCd',
    },
    params: [
      {
        name: 'pdno',
        required: true,
      },
      {
        name: 'prdtTypeCd',
        required: false,
        defaultValue: '302',
      },
    ],
  },
  {
    methodName: 'getBondIssueInfo',
    method: 'GET',
    path: '/uapi/domestic-bond/v1/quotations/issue-info',
    trId: 'CTPF1101R',
    requestMap: {
      PDNO: 'pdno',
      PRDT_TYPE_CD: 'prdtTypeCd',
    },
    params: [
      {
        name: 'pdno',
        required: true,
      },
      {
        name: 'prdtTypeCd',
        required: false,
        defaultValue: '302',
      },
    ],
  },
];
