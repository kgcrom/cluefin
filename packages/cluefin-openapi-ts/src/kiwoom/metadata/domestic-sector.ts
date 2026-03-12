import type { KiwoomEndpointDefinition } from '../../core/types';
import {
  allIndustryIndexResponseSchema,
  dailyIndustryCurrentPriceResponseSchema,
  industryCurrentPriceResponseSchema,
  industryInvestorNetBuyResponseSchema,
  industryPriceBySectorResponseSchema,
  industryProgramResponseSchema,
} from '../schemas/domestic-sector';

export const domesticSectorEndpoints: KiwoomEndpointDefinition[] = [
  {
    methodName: 'getIndustryProgram',
    responseSchema: industryProgramResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka10010',
    bodyMap: {
      stk_cd: 'stkCode',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'stkCode',
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
    methodName: 'getIndustryInvestorNetBuy',
    responseSchema: industryInvestorNetBuyResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka10051',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      amt_qty_tp: 'amtQtyTp',
      base_dt: 'baseDt',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'amtQtyTp',
        required: true,
      },
      {
        name: 'baseDt',
        required: true,
      },
      {
        name: 'stexTp',
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
    methodName: 'getIndustryCurrentPrice',
    responseSchema: industryCurrentPriceResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka20001',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      inds_cd: 'indsCd',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'indsCd',
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
    methodName: 'getIndustryPriceBySector',
    responseSchema: industryPriceBySectorResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka20002',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      inds_cd: 'indsCd',
      stex_tp: 'stexTp',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'indsCd',
        required: true,
      },
      {
        name: 'stexTp',
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
    methodName: 'getAllIndustryIndex',
    responseSchema: allIndustryIndexResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka20003',
    bodyMap: {
      inds_cd: 'indsCd',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'indsCd',
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
    methodName: 'getDailyIndustryCurrentPrice',
    responseSchema: dailyIndustryCurrentPriceResponseSchema,
    path: '/api/dostk/sect',
    apiId: 'ka20009',
    bodyMap: {
      mrkt_tp: 'mrktTp',
      inds_cd: 'indsCd',
    },
    headerParamMap: {
      'cont-yn': 'contYn',
      'next-key': 'nextKey',
    },
    params: [
      {
        name: 'mrktTp',
        required: true,
      },
      {
        name: 'indsCd',
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
];

export type DomesticSectorMethodName =
  | 'getIndustryProgram'
  | 'getIndustryInvestorNetBuy'
  | 'getIndustryCurrentPrice'
  | 'getIndustryPriceBySector'
  | 'getAllIndustryIndex'
  | 'getDailyIndustryCurrentPrice';
