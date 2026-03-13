import type { KiwoomEndpointDefinition } from '../../core/types';
import {
  consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema,
  foreignInvestorTradingTrendByStockResponseSchema,
  stockInstitutionResponseSchema,
} from '../schemas/domestic-foreign';

export const domesticForeignEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getForeignInvestorTradingTrendByStock',
    responseSchema: foreignInvestorTradingTrendByStockResponseSchema,
    path: '/api/dostk/frgnistt',
    apiId: 'ka10008',
    bodyMap: {
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getStockInstitution',
    responseSchema: stockInstitutionResponseSchema,
    path: '/api/dostk/frgnistt',
    apiId: 'ka10009',
    bodyMap: {
      stk_cd: 'stkCd',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCd',
        required: true,
      },
      {
        name: 'contYn',
        required: false,
        defaultValue: 'N',
      },
      {
        name: 'nextKey',
        required: false,
        defaultValue: '',
      },
    ],
  },
  {
    methodName: 'getConsecutiveNetBuySellStatusByInstitutionForeigner',
    responseSchema: consecutiveNetBuySellStatusByInstitutionForeignerResponseSchema,
    path: '/api/dostk/frgnistt',
    apiId: 'ka10131',
    bodyMap: {
      dt: 'dt',
      strt_dt: 'strtDt',
      end_dt: 'endDt',
      mrkt_tp: 'mrktTp',
      stk_inds_tp: 'stkIndsTp',
      amt_qty_tp: 'amtQtyTp',
      stex_tp: 'stexTp',
      netslmt_tp: 'netslmtTp',
    },
    headerParamMap: {},
    params: [
      {
        name: 'dt',
        required: true,
      },
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'stkIndsTp',
        required: true,
      },
      {
        name: 'amtQtyTp',
        required: true,
      },
      {
        name: 'stexTp',
        required: true,
      },
      {
        name: 'netslmtTp',
        required: false,
        defaultValue: '2',
      },
      {
        name: 'strtDt',
        required: false,
        defaultValue: '',
      },
      {
        name: 'endDt',
        required: false,
        defaultValue: '',
      },
    ],
  },
];

export type DomesticForeignMethodName =
  | 'getForeignInvestorTradingTrendByStock'
  | 'getStockInstitution'
  | 'getConsecutiveNetBuySellStatusByInstitutionForeigner';
