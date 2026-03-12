import { describe, test } from 'vitest';
import { getKiwoomClient, ONE_MONTH_AGO, runIntegration, SAMSUNG, TODAY } from '../_helpers/integration-setup';

const it = runIntegration ? test : test.skip;

describe('Capture DomesticStockInfo responses', () => {
  it('capture all stock info responses', async () => {
    const client = await getKiwoomClient();

    const calls = [
      ['getStockInfo', { stkCd: SAMSUNG }],
      ['getStockTradingMember', { stkCd: SAMSUNG }],
      ['getExecution', { stkCd: SAMSUNG }],
      ['getMarginTradingTrend', { stkCd: SAMSUNG, dt: TODAY, qryTp: '0' }],
      ['getDailyTradingDetails', { stkCd: SAMSUNG, strtDt: ONE_MONTH_AGO }],
      [
        'getNewHighLowPrice',
        {
          mrktTp: '0',
          ntlTp: '0',
          highLowCloseTp: '0',
          stkCnd: '0',
          trdeQtyTp: '0',
          crdCnd: '0',
          updownIncls: '0',
          dt: TODAY,
          stexTp: '1',
        },
      ],
      [
        'getUpperLowerLimitPrice',
        {
          mrktTp: '0',
          updownTp: '0',
          sortTp: '0',
          stkCnd: '0',
          trdeQtyTp: '0',
          crdCnd: '0',
          trdeGoldTp: '0',
          stexTp: '1',
        },
      ],
      [
        'getHighLowPriceApproach',
        { highLowTp: '0', alaccRt: '5', mrktTp: '0', trdeQtyTp: '0', stkCnd: '0', crdCnd: '0', stexTp: '1' },
      ],
      [
        'getPriceVolatility',
        {
          mrktTp: '0',
          fluTp: '0',
          tmTp: '0',
          tm: '5',
          trdeQtyTp: '0',
          stkCnd: '0',
          crdCnd: '0',
          pricCnd: '0',
          updownIncls: '0',
          stexTp: '1',
        },
      ],
      ['getTradingVolumeRenewal', { mrktTp: '0', cycleTp: '0', trdeQtyTp: '0', stexTp: '1' }],
      [
        'getSupplyDemandConcentration',
        { mrktTp: '001', prpsCnctrRt: '50', curPrcEntry: '0', prpscnt: '10', cycleTp: '100', stexTp: '1' },
      ],
      ['getHighPer', { pertp: '0', stexTp: '1' }],
      [
        'getChangeRateFromOpen',
        {
          sortTp: '0',
          trdeQtyCnd: '0',
          mrktTp: '0',
          updownIncls: '0',
          stkCnd: '0',
          crdCnd: '0',
          trdePricaCnd: '0',
          fluCnd: '0',
          stexTp: '1',
        },
      ],
      [
        'getTradingMemberSupplyDemandAnalysis',
        {
          stkCd: SAMSUNG,
          strtDt: ONE_MONTH_AGO,
          endDt: TODAY,
          qryDtTp: '0',
          potTp: '0',
          dt: TODAY,
          sortBase: '0',
          mmcmCd: '0000',
          stexTp: '1',
        },
      ],
      [
        'getTradingMemberInstantVolume',
        { stkCd: SAMSUNG, mmcmCd: '0000', mrktTp: '0', qtyTp: '0', pricTp: '0', stexTp: '1' },
      ],
      [
        'getVolatilityControlEvent',
        {
          mrktTp: '000',
          bfMkrtTp: '0',
          motnTp: '0',
          skipStk: '000000000',
          trdeQtyTp: '0',
          trdePricaTp: '0',
          motnDrc: '0',
          stexTp: '1',
          minTrdeQty: '0',
          maxTrdeQty: '100000000',
          minTrdePrica: '0',
          maxTrdePrica: '100000000',
        },
      ],
      ['getDailyPreviousDayExecutionVolume', { stkCd: SAMSUNG, tdyPred: '1' }],
      [
        'getDailyTradingItemsByInvestor',
        { strtDt: ONE_MONTH_AGO, endDt: TODAY, trdeTp: '0', mrktTp: '0', invsrTp: '0', stexTp: '1' },
      ],
      ['getInstitutionalInvestorByStock', { dt: TODAY, stkCd: SAMSUNG, amtQtyTp: '1', trdeTp: '0', unitTp: '1' }],
      [
        'getTotalInstitutionalInvestorByStock',
        { stkCd: SAMSUNG, strtDt: ONE_MONTH_AGO, endDt: TODAY, amtQtyTp: '1', trdeTp: '0', unitTp: '1' },
      ],
      ['getDailyPreviousDayConclusion', { stkCd: SAMSUNG, tdyPred: '1', ticMin: '0' }],
      ['getInterestStockInfo', { stkCd: SAMSUNG }],
      ['getStockInfoSummary', { mrktTp: '0' }],
      ['getStockInfoV1', { stkCd: SAMSUNG }],
      ['getIndustryCode', { mrktTp: '0' }],
      ['getMemberCompany', {}],
      ['getTop50ProgramNetBuy', { trdeUpperTp: '0', amtQtyTp: '1', mrktTp: '0', stexTp: '1' }],
      ['getProgramTradingStatusByStock', { dt: TODAY, mrktTp: '0', stexTp: '1' }],
    ] as const;

    for (const [method, params] of calls) {
      const fn = (client.domesticStockInfo as Record<string, Function>)[method];
      const res = await fn.call(client.domesticStockInfo, params);
      console.log(`\n=== ${method} ===`);
      console.log(JSON.stringify(res.body, null, 2));
    }
  }, 120000);
});
