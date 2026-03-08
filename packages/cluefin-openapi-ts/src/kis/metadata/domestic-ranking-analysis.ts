import type { KisEndpointDefinition } from '../../core/types';

export const domesticRankingAnalysisEndpoints: KisEndpointDefinition[] = [
  {
    methodName: 'getTradingVolumeRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/quotations/volume-rank',
    trId: 'FHPST01710000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_BLNG_CLS_CODE: 'fidBlngClsCode',
      FID_TRGT_CLS_CODE: 'fidTrgtClsCode',
      FID_TRGT_EXLS_CLS_CODE: 'fidTrgtExlsClsCode',
      FID_INPUT_PRICE_1: 'fidInputPrice1',
      FID_INPUT_PRICE_2: 'fidInputPrice2',
      FID_VOL_CNT: 'fidVolCnt',
      FID_INPUT_DATE_1: 'fidInputDate1',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidInputDate1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockFluctuationRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/fluctuation',
    trId: 'FHPST01700000',
    requestMap: {
      fid_rsfl_rate2: 'fidRsflRate2',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_input_cnt_1: 'fidInputCnt1',
      fid_prc_cls_code: 'fidPrcClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_rsfl_rate1: 'fidRsflRate1',
    },
    params: [
      {
        name: 'fidRsflRate2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidInputCnt1',
        required: true,
      },
      {
        name: 'fidPrcClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidRsflRate1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockHogaQuantityRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/quote-balance',
    trId: 'FHPST01720000',
    requestMap: {
      fid_vol_cnt: 'fidVolCnt',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
    },
    params: [
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockProfitabilityIndicatorRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/profit-asset-index',
    trId: 'FHPST01730000',
    requestMap: {
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_input_option_1: 'fidInputOption1',
      fid_input_option_2: 'fidInputOption2',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_blng_cls_code: 'fidBlngClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidInputOption1',
        required: true,
      },
      {
        name: 'fidInputOption2',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockMarketCapTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/market-cap',
    trId: 'FHPST01740000',
    requestMap: {
      fid_input_price_2: 'fidInputPrice2',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_vol_cnt: 'fidVolCnt',
    },
    params: [
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockFinanceRatioRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/finance-ratio',
    trId: 'FHPST01750000',
    requestMap: {
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_input_option_1: 'fidInputOption1',
      fid_input_option_2: 'fidInputOption2',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_blng_cls_code: 'fidBlngClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
    },
    params: [
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidInputOption1',
        required: true,
      },
      {
        name: 'fidInputOption2',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockTimeHogaRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/after-hour-balance',
    trId: 'FHPST01760000',
    requestMap: {
      fid_input_price_1: 'fidInputPrice1',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_vol_cnt: 'fidVolCnt',
      fid_input_price_2: 'fidInputPrice2',
    },
    params: [
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockPreferredStockRatioTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/prefer-disparate-ratio',
    trId: 'FHPST01770000',
    requestMap: {
      fid_vol_cnt: 'fidVolCnt',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
    },
    params: [
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockDisparityIndexRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/disparity',
    trId: 'FHPST01780000',
    requestMap: {
      fid_input_price_2: 'fidInputPrice2',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_hour_cls_code: 'fidHourClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_vol_cnt: 'fidVolCnt',
    },
    params: [
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidHourClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockMarketPriceRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/market-value',
    trId: 'FHPST01790000',
    requestMap: {
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_input_option_1: 'fidInputOption1',
      fid_input_option_2: 'fidInputOption2',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_blng_cls_code: 'fidBlngClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
    },
    params: [
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidInputOption1',
        required: true,
      },
      {
        name: 'fidInputOption2',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockExecutionStrengthTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/volume-power',
    trId: 'FHPST01680000',
    requestMap: {
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_trgt_cls_code: 'fidTrgtClsCode',
    },
    params: [
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockWatchlistRegistrationTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/top-interest-stock',
    trId: 'FHPST01800000',
    requestMap: {
      fid_input_iscd_2: 'fidInputIscd2',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_input_price_2: 'fidInputPrice2',
      fid_vol_cnt: 'fidVolCnt',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_cnt_1: 'fidInputCnt1',
    },
    params: [
      {
        name: 'fidInputIscd2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputCnt1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockExpectedExecutionRiseDeclineTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/exp-trans-updown',
    trId: 'FHPST01820000',
    requestMap: {
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_div_cls_code: 'fidDivClsCode',
      fid_aply_rang_prc_1: 'fidAplyRangPrc1',
      fid_vol_cnt: 'fidVolCnt',
      fid_pbmn: 'fidPbmn',
      fid_blng_cls_code: 'fidBlngClsCode',
      fid_mkop_cls_code: 'fidMkopClsCode',
    },
    params: [
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidAplyRangPrc1',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidPbmn',
        required: true,
      },
      {
        name: 'fidBlngClsCode',
        required: true,
      },
      {
        name: 'fidMkopClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockProprietaryTradingTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/traded-by-company',
    trId: 'FHPST01860000',
    requestMap: {
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_input_date_1: 'fidInputDate1',
      fid_input_date_2: 'fidInputDate2',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_aply_rang_vol: 'fidAplyRangVol',
      fid_aply_rang_prc_2: 'fidAplyRangPrc2',
      fid_aply_rang_prc_1: 'fidAplyRangPrc1',
    },
    params: [
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidInputDate1',
        required: true,
      },
      {
        name: 'fidInputDate2',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidAplyRangVol',
        required: true,
      },
      {
        name: 'fidAplyRangPrc2',
        required: true,
      },
      {
        name: 'fidAplyRangPrc1',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockNewHighLowApproachingTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/near-new-highlow',
    trId: 'FHPST01870000',
    requestMap: {
      fid_aply_rang_vol: 'fidAplyRangVol',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_cnt_1: 'fidInputCnt1',
      fid_input_cnt_2: 'fidInputCnt2',
      fid_prc_cls_code: 'fidPrcClsCode',
      fid_input_iscd: 'fidInputIscd',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_aply_rang_prc_1: 'fidAplyRangPrc1',
      fid_aply_rang_prc_2: 'fidAplyRangPrc2',
    },
    params: [
      {
        name: 'fidAplyRangVol',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputCnt1',
        required: true,
      },
      {
        name: 'fidInputCnt2',
        required: true,
      },
      {
        name: 'fidPrcClsCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidAplyRangPrc1',
        required: true,
      },
      {
        name: 'fidAplyRangPrc2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockDividendYieldTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/dividend-rate',
    trId: 'HHKDB13470100',
    requestMap: {
      CTS_AREA: 'ctsArea',
      GB1: 'gb1',
      UPJONG: 'upjong',
      GB2: 'gb2',
      GB3: 'gb3',
      F_DT: 'fDt',
      T_DT: 'tDt',
      GB4: 'gb4',
    },
    params: [
      {
        name: 'ctsArea',
        required: true,
      },
      {
        name: 'gb1',
        required: true,
      },
      {
        name: 'upjong',
        required: true,
      },
      {
        name: 'gb2',
        required: true,
      },
      {
        name: 'gb3',
        required: true,
      },
      {
        name: 'fDt',
        required: true,
      },
      {
        name: 'tDt',
        required: true,
      },
      {
        name: 'gb4',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockLargeExecutionCountTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/bulk-trans-num',
    trId: 'HHKST1909000C0',
    requestMap: {
      fid_aply_rang_prc_2: 'fidAplyRangPrc2',
      fid_cond_mrkt_div_code: 'fidCondMrktDivCode',
      fid_cond_scr_div_code: 'fidCondScrDivCode',
      fid_input_iscd: 'fidInputIscd',
      fid_rank_sort_cls_code: 'fidRankSortClsCode',
      fid_div_cls_code: 'fidDivClsCode',
      fid_input_price_1: 'fidInputPrice1',
      fid_aply_rang_prc_1: 'fidAplyRangPrc1',
      fid_input_iscd_2: 'fidInputIscd2',
      fid_trgt_exls_cls_code: 'fidTrgtExlsClsCode',
      fid_trgt_cls_code: 'fidTrgtClsCode',
      fid_vol_cnt: 'fidVolCnt',
    },
    params: [
      {
        name: 'fidAplyRangPrc2',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidAplyRangPrc1',
        required: true,
      },
      {
        name: 'fidInputIscd2',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockCreditBalanceTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/credit-balance',
    trId: 'HHKST17010000',
    requestMap: {
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_OPTION: 'fidOption',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
    },
    params: [
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidOption',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockShortSellingTop',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/short-sale',
    trId: 'FHPST04820000',
    requestMap: {
      FID_APLY_RANG_VOL: 'fidAplyRangVol',
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_PERIOD_DIV_CODE: 'fidPeriodDivCode',
      FID_INPUT_CNT_1: 'fidInputCnt1',
      FID_TRGT_EXLS_CLS_CODE: 'fidTrgtExlsClsCode',
      FID_TRGT_CLS_CODE: 'fidTrgtClsCode',
      FID_APLY_RANG_PRC_1: 'fidAplyRangPrc1',
      FID_APLY_RANG_PRC_2: 'fidAplyRangPrc2',
    },
    params: [
      {
        name: 'fidAplyRangVol',
        required: true,
      },
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidPeriodDivCode',
        required: true,
      },
      {
        name: 'fidInputCnt1',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidAplyRangPrc1',
        required: true,
      },
      {
        name: 'fidAplyRangPrc2',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockAfterHoursFluctuationRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/overtime-fluctuation',
    trId: 'FHPST02340000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_MRKT_CLS_CODE: 'fidMrktClsCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_DIV_CLS_CODE: 'fidDivClsCode',
      FID_INPUT_PRICE_1: 'fidInputPrice1',
      FID_INPUT_PRICE_2: 'fidInputPrice2',
      FID_VOL_CNT: 'fidVolCnt',
      FID_TRGT_CLS_CODE: 'fidTrgtClsCode',
      FID_TRGT_EXLS_CLS_CODE: 'fidTrgtExlsClsCode',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidMrktClsCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidDivClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getStockAfterHoursVolumeRank',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/overtime-volume',
    trId: 'FHPST02350000',
    requestMap: {
      FID_COND_MRKT_DIV_CODE: 'fidCondMrktDivCode',
      FID_COND_SCR_DIV_CODE: 'fidCondScrDivCode',
      FID_INPUT_ISCD: 'fidInputIscd',
      FID_RANK_SORT_CLS_CODE: 'fidRankSortClsCode',
      FID_INPUT_PRICE_1: 'fidInputPrice1',
      FID_INPUT_PRICE_2: 'fidInputPrice2',
      FID_VOL_CNT: 'fidVolCnt',
      FID_TRGT_CLS_CODE: 'fidTrgtClsCode',
      FID_TRGT_EXLS_CLS_CODE: 'fidTrgtExlsClsCode',
    },
    params: [
      {
        name: 'fidCondMrktDivCode',
        required: true,
      },
      {
        name: 'fidCondScrDivCode',
        required: true,
      },
      {
        name: 'fidInputIscd',
        required: true,
      },
      {
        name: 'fidRankSortClsCode',
        required: true,
      },
      {
        name: 'fidInputPrice1',
        required: true,
      },
      {
        name: 'fidInputPrice2',
        required: true,
      },
      {
        name: 'fidVolCnt',
        required: true,
      },
      {
        name: 'fidTrgtClsCode',
        required: true,
      },
      {
        name: 'fidTrgtExlsClsCode',
        required: true,
      },
    ],
  },
  {
    methodName: 'getHtsInquiryTop20',
    method: 'GET',
    path: '/uapi/domestic-stock/v1/ranking/hts-top-view',
    trId: 'HHMCM000100C0',
    requestMap: {},
    params: [],
  },
];

export type DomesticRankingAnalysisMethodName =
  | 'getTradingVolumeRank'
  | 'getStockFluctuationRank'
  | 'getStockHogaQuantityRank'
  | 'getStockProfitabilityIndicatorRank'
  | 'getStockMarketCapTop'
  | 'getStockFinanceRatioRank'
  | 'getStockTimeHogaRank'
  | 'getStockPreferredStockRatioTop'
  | 'getStockDisparityIndexRank'
  | 'getStockMarketPriceRank'
  | 'getStockExecutionStrengthTop'
  | 'getStockWatchlistRegistrationTop'
  | 'getStockExpectedExecutionRiseDeclineTop'
  | 'getStockProprietaryTradingTop'
  | 'getStockNewHighLowApproachingTop'
  | 'getStockDividendYieldTop'
  | 'getStockLargeExecutionCountTop'
  | 'getStockCreditBalanceTop'
  | 'getStockShortSellingTop'
  | 'getStockAfterHoursFluctuationRank'
  | 'getStockAfterHoursVolumeRank'
  | 'getHtsInquiryTop20';
