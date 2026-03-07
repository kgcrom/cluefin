import { describe, expect, it, vi } from 'vitest';
import { OnmarketBondRealtimeQuote } from '../../src/kis/onmarket-bond-realtime-quote';
import type { KisSocketClient } from '../../src/kis/socket-client';
import {
  BOND_EXECUTION_FIELD_NAMES,
  BOND_INDEX_EXECUTION_FIELD_NAMES,
  BOND_ORDERBOOK_FIELD_NAMES,
} from '../../src/kis/metadata/onmarket-bond-realtime-quote';

function createMockSocketClient(env: 'prod' | 'dev' = 'prod'): KisSocketClient {
  return {
    env,
    subscribe: vi.fn().mockResolvedValue(undefined),
    unsubscribe: vi.fn().mockResolvedValue(undefined),
  } as unknown as KisSocketClient;
}

// Sample test data (19 fields)
const sampleBondExecutionData: string[] = [
  'KR1035010001', '국고채권03250-2503', '100000', '2', '50', '0.05',
  '10050', '1000', '10000', '10100', '9950', '10000',
  '3.250', '3.300', '3.200', '3.350', '500000', '450000', '1',
];

// Sample orderbook data (34 fields)
const sampleBondOrderbookData: string[] = [
  'KR1035010001', '100000',
  '3.250', '3.260', '3.270', '3.280', '3.290',
  '3.240', '3.230', '3.220', '3.210', '3.200',
  '10050', '10060', '10070', '10080', '10090',
  '10040', '10030', '10020', '10010', '10000',
  '5000', '4000', '3000', '2000', '1000',
  '6000', '5000', '4000', '3000', '2000',
  '15000', '20000',
];

// Sample index execution data (20 fields)
const sampleBondIndexExecutionData: string[] = [
  'BOND001', '20260307', '100000',
  '1050.00', '1055.00', '1045.00', '1052.50',
  '1050.00', '2.50', '2', '0.24',
  '1051.00', '1053.00', '1048.00', '1047.00',
  '105.25', '5.23', '0.45', '3.15', '3.20',
];

describe('OnmarketBondRealtimeQuote', () => {
  describe('TR_ID constants', () => {
    it('should have correct TR_ID values', () => {
      expect(OnmarketBondRealtimeQuote.TR_ID_BOND_EXECUTION).toBe('H0BJCNT0');
      expect(OnmarketBondRealtimeQuote.TR_ID_BOND_ORDERBOOK).toBe('H0BJASP0');
      expect(OnmarketBondRealtimeQuote.TR_ID_BOND_INDEX_EXECUTION).toBe('H0BICNT0');
    });
  });

  describe('subscribe/unsubscribe bond execution', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.subscribeBondExecution('KR1035010001');
      expect(mock.subscribe).toHaveBeenCalledWith('H0BJCNT0', 'KR1035010001');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.unsubscribeBondExecution('KR1035010001');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0BJCNT0', 'KR1035010001');
    });

    it('should throw in dev env for subscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.subscribeBondExecution('KR1035010001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });

    it('should throw in dev env for unsubscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.unsubscribeBondExecution('KR1035010001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });
  });

  describe('subscribe/unsubscribe bond orderbook', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.subscribeBondOrderbook('KR1035010001');
      expect(mock.subscribe).toHaveBeenCalledWith('H0BJASP0', 'KR1035010001');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.unsubscribeBondOrderbook('KR1035010001');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0BJASP0', 'KR1035010001');
    });

    it('should throw in dev env for subscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.subscribeBondOrderbook('KR1035010001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });

    it('should throw in dev env for unsubscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.unsubscribeBondOrderbook('KR1035010001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });
  });

  describe('subscribe/unsubscribe bond index execution', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.subscribeBondIndexExecution('BOND001');
      expect(mock.subscribe).toHaveBeenCalledWith('H0BICNT0', 'BOND001');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OnmarketBondRealtimeQuote(mock);
      await quote.unsubscribeBondIndexExecution('BOND001');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0BICNT0', 'BOND001');
    });

    it('should throw in dev env for subscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.subscribeBondIndexExecution('BOND001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });

    it('should throw in dev env for unsubscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OnmarketBondRealtimeQuote(mock);
      await expect(quote.unsubscribeBondIndexExecution('BOND001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });
  });
});

describe('parseBondExecutionData', () => {
  it('should parse single record correctly', () => {
    const result = OnmarketBondRealtimeQuote.parseBondExecutionData(sampleBondExecutionData);
    expect(result).toHaveLength(1);
    expect(result[0]!.stndIscd).toBe('KR1035010001');
    expect(result[0]!.bondIsnm).toBe('국고채권03250-2503');
    expect(result[0]!.stckCntgHour).toBe('100000');
    expect(result[0]!.prdyVrssSign).toBe('2');
    expect(result[0]!.stckPrpr).toBe('10050');
    expect(result[0]!.bondCntgErt).toBe('3.250');
    expect(result[0]!.acmlVol).toBe('500000');
    expect(result[0]!.cntgTypeClsCode).toBe('1');
  });

  it('should parse batched records (5 x 19)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 5; i++) {
      const record = [...sampleBondExecutionData];
      record[6] = String(10050 + i * 10);
      batched.push(...record);
    }
    const result = OnmarketBondRealtimeQuote.parseBondExecutionData(batched);
    expect(result).toHaveLength(5);
    for (let i = 0; i < 5; i++) {
      expect(result[i]!.stckPrpr).toBe(String(10050 + i * 10));
    }
  });

  it('should handle extra fields (forward compatibility)', () => {
    const data = [...sampleBondExecutionData, 'extra1', 'extra2', 'extra3'];
    const result = OnmarketBondRealtimeQuote.parseBondExecutionData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.stndIscd).toBe('KR1035010001');
    expect(result[0]!.cntgTypeClsCode).toBe('1');
  });

  it('should throw on insufficient fields', () => {
    expect(() =>
      OnmarketBondRealtimeQuote.parseBondExecutionData(['KR1035010001', '국고채권', '100000']),
    ).toThrow('Expected at least 19 fields, got 3');
  });

  it('should throw on empty data', () => {
    expect(() => OnmarketBondRealtimeQuote.parseBondExecutionData([])).toThrow(
      'Expected at least 19 fields, got 0',
    );
  });

  it('should parse large batch (50 x 19)', () => {
    const data = Array(50 * 19).fill('value');
    const result = OnmarketBondRealtimeQuote.parseBondExecutionData(data);
    expect(result).toHaveLength(50);
  });
});

describe('parseBondOrderbookData', () => {
  it('should parse single record correctly', () => {
    const result = OnmarketBondRealtimeQuote.parseBondOrderbookData(sampleBondOrderbookData);
    expect(result).toHaveLength(1);
    expect(result[0]!.stndIscd).toBe('KR1035010001');
    expect(result[0]!.stckCntgHour).toBe('100000');
    expect(result[0]!.askpErt1).toBe('3.250');
    expect(result[0]!.bidpErt1).toBe('3.240');
    expect(result[0]!.askp1).toBe('10050');
    expect(result[0]!.bidp1).toBe('10040');
    expect(result[0]!.totalAskpRsqn).toBe('15000');
    expect(result[0]!.totalBidpRsqn).toBe('20000');
  });

  it('should parse batched records (10 x 34)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 10; i++) {
      const record = [...sampleBondOrderbookData];
      record[2] = String(3.25 + i * 0.01);
      batched.push(...record);
    }
    const result = OnmarketBondRealtimeQuote.parseBondOrderbookData(batched);
    expect(result).toHaveLength(10);
    for (let i = 0; i < 10; i++) {
      expect(result[i]!.askpErt1).toBe(String(3.25 + i * 0.01));
    }
  });

  it('should handle extra fields', () => {
    const data = [...sampleBondOrderbookData, 'extra1', 'extra2', 'extra3'];
    const result = OnmarketBondRealtimeQuote.parseBondOrderbookData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.totalBidpRsqn).toBe('20000');
  });

  it('should throw on insufficient fields', () => {
    expect(() =>
      OnmarketBondRealtimeQuote.parseBondOrderbookData(['KR1035010001', '100000', '3.250']),
    ).toThrow('Expected at least 34 fields, got 3');
  });

  it('should throw on empty data', () => {
    expect(() => OnmarketBondRealtimeQuote.parseBondOrderbookData([])).toThrow(
      'Expected at least 34 fields, got 0',
    );
  });
});

describe('parseBondIndexExecutionData', () => {
  it('should parse single record correctly', () => {
    const result = OnmarketBondRealtimeQuote.parseBondIndexExecutionData(sampleBondIndexExecutionData);
    expect(result).toHaveLength(1);
    expect(result[0]!.nmixId).toBe('BOND001');
    expect(result[0]!.stndDate1).toBe('20260307');
    expect(result[0]!.trnmHour).toBe('100000');
    expect(result[0]!.totlErnnNmix).toBe('1052.50');
    expect(result[0]!.totlErnnNmixPrdyVrssSign).toBe('2');
    expect(result[0]!.totlErnnNmixPrdyCtrt).toBe('0.24');
    expect(result[0]!.bondAvrgDrtnVal).toBe('5.23');
    expect(result[0]!.bondAvrgFrdlYtmVal).toBe('3.20');
  });

  it('should parse batched records (5 x 20)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 5; i++) {
      const record = [...sampleBondIndexExecutionData];
      record[0] = `BOND00${i + 1}`;
      batched.push(...record);
    }
    const result = OnmarketBondRealtimeQuote.parseBondIndexExecutionData(batched);
    expect(result).toHaveLength(5);
    for (let i = 0; i < 5; i++) {
      expect(result[i]!.nmixId).toBe(`BOND00${i + 1}`);
    }
  });

  it('should handle extra fields', () => {
    const data = [...sampleBondIndexExecutionData, 'extra1', 'extra2', 'extra3'];
    const result = OnmarketBondRealtimeQuote.parseBondIndexExecutionData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.nmixId).toBe('BOND001');
    expect(result[0]!.bondAvrgFrdlYtmVal).toBe('3.20');
  });

  it('should throw on insufficient fields', () => {
    expect(() =>
      OnmarketBondRealtimeQuote.parseBondIndexExecutionData(['BOND001', '20260307', '100000']),
    ).toThrow('Expected at least 20 fields, got 3');
  });

  it('should throw on empty data', () => {
    expect(() => OnmarketBondRealtimeQuote.parseBondIndexExecutionData([])).toThrow(
      'Expected at least 20 fields, got 0',
    );
  });
});

describe('Field name constants', () => {
  it('BOND_EXECUTION_FIELD_NAMES should have 19 entries', () => {
    expect(BOND_EXECUTION_FIELD_NAMES).toHaveLength(19);
  });

  it('BOND_ORDERBOOK_FIELD_NAMES should have 34 entries', () => {
    expect(BOND_ORDERBOOK_FIELD_NAMES).toHaveLength(34);
  });

  it('BOND_INDEX_EXECUTION_FIELD_NAMES should have 20 entries', () => {
    expect(BOND_INDEX_EXECUTION_FIELD_NAMES).toHaveLength(20);
  });

  it('should have no duplicate field names in each list', () => {
    expect(new Set(BOND_EXECUTION_FIELD_NAMES).size).toBe(BOND_EXECUTION_FIELD_NAMES.length);
    expect(new Set(BOND_ORDERBOOK_FIELD_NAMES).size).toBe(BOND_ORDERBOOK_FIELD_NAMES.length);
    expect(new Set(BOND_INDEX_EXECUTION_FIELD_NAMES).size).toBe(BOND_INDEX_EXECUTION_FIELD_NAMES.length);
  });
});
