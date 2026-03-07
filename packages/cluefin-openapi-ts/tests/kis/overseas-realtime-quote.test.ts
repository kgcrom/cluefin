import { describe, expect, it, vi } from 'vitest';
import { OverseasRealtimeQuote } from '../../src/kis/overseas-realtime-quote';
import type { KisSocketClient } from '../../src/kis/socket-client';
import {
  OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
  OVERSEAS_EXECUTION_FIELD_NAMES,
  OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES,
  OVERSEAS_ORDERBOOK_FIELD_NAMES,
} from '../../src/kis/metadata/overseas-realtime-quote';

function createMockSocketClient(env: 'prod' | 'dev' = 'prod'): KisSocketClient {
  return {
    env,
    subscribe: vi.fn().mockResolvedValue(undefined),
    unsubscribe: vi.fn().mockResolvedValue(undefined),
  } as unknown as KisSocketClient;
}

// Sample test data — 71 fields for orderbook
const sampleOrderbookData: string[] = [
  'DNASAAPL',
  'AAPL',
  '2',
  '20260307',
  '100000',
  '20260308',
  '020000',
  '50000',
  '60000',
  '100',
  '-200',
  '190.50',
  '190.60',
  '1000',
  '2000',
  '100',
  '-200',
  '190.40',
  '190.70',
  '1100',
  '2100',
  '110',
  '-210',
  '190.30',
  '190.80',
  '1200',
  '2200',
  '120',
  '-220',
  '190.20',
  '190.90',
  '1300',
  '2300',
  '130',
  '-230',
  '190.10',
  '191.00',
  '1400',
  '2400',
  '140',
  '-240',
  '190.00',
  '191.10',
  '1500',
  '2500',
  '150',
  '-250',
  '189.90',
  '191.20',
  '1600',
  '2600',
  '160',
  '-260',
  '189.80',
  '191.30',
  '1700',
  '2700',
  '170',
  '-270',
  '189.70',
  '191.40',
  '1800',
  '2800',
  '180',
  '-280',
  '189.60',
  '191.50',
  '1900',
  '2900',
  '190',
  '-290',
];

// Sample test data — 17 fields for delayed orderbook
const sampleDelayedOrderbookData: string[] = [
  'DHKS00003',
  '00003',
  '2',
  '20260307',
  '100000',
  '20260308',
  '020000',
  '30000',
  '40000',
  '50',
  '-50',
  '25.50',
  '25.60',
  '500',
  '600',
  '50',
  '-60',
];

// Sample test data — 26 fields for execution
const sampleExecutionData: string[] = [
  'DNASAAPL',
  'AAPL',
  '2',
  '20260307',
  '20260307',
  '100000',
  '20260308',
  '020000',
  '189.00',
  '191.50',
  '188.50',
  '190.50',
  '2',
  '1.50',
  '0.79',
  '190.40',
  '190.60',
  '1000',
  '2000',
  '100',
  '5000000',
  '950000000',
  '2500000',
  '2500000',
  '118.00',
  '1',
];

// Sample test data — 25 fields for execution notification
const sampleExecutionNotificationData: string[] = [
  'CUST0001',
  '1234567890',
  '0000000001',
  '0000000000',
  '02',
  '0',
  '00',
  'AAPL',
  '100',
  '190.50',
  '100000',
  '0',
  '2',
  '2',
  '00001',
  '100',
  '홍길동계좌',
  'APPLE INC',
  'NAS',
  '00',
  '        ',
  '090000',
  '160000',
  '1',
  '190.500000000000',
];

describe('OverseasRealtimeQuote', () => {
  describe('TR_ID constants', () => {
    it('should have correct TR_ID values', () => {
      expect(OverseasRealtimeQuote.TR_ID_ORDERBOOK).toBe('HDFSASP0');
      expect(OverseasRealtimeQuote.TR_ID_EXECUTION).toBe('HDFSCNT0');
      expect(OverseasRealtimeQuote.TR_ID_DELAYED_ORDERBOOK).toBe('HDFSASP1');
      expect(OverseasRealtimeQuote.TR_ID_EXECUTION_NOTIFICATION).toBe('H0GSCNI0');
    });
  });

  describe('generateTrKey', () => {
    it('should generate correct tr_key format', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeOrderbook('AAPL', 'NAS');
      expect(mock.subscribe).toHaveBeenCalledWith('HDFSASP0', 'RNASAAPL');
    });

    it('should use custom serviceType', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeOrderbook('AAPL', 'NAS', 'D');
      expect(mock.subscribe).toHaveBeenCalledWith('HDFSASP0', 'DNASAAPL');
    });
  });

  describe('requireProdEnv', () => {
    it('should throw in dev env for subscribeOrderbook', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.subscribeOrderbook('AAPL', 'NAS')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for subscribeExecution', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.subscribeExecution('RNASAAPL')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for subscribeDelayedOrderbook', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.subscribeDelayedOrderbook('DHKS00003')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for subscribeExecutionNotification', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.subscribeExecutionNotification('HTSID0001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });

    it('should throw in dev env for unsubscribeOrderbook', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.unsubscribeOrderbook('AAPL', 'NAS')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for unsubscribeExecution', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.unsubscribeExecution('RNASAAPL')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for unsubscribeDelayedOrderbook', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.unsubscribeDelayedOrderbook('DHKS00003')).rejects.toThrow('운영 서버(prod)에서만 사용 가능');
    });

    it('should throw in dev env for unsubscribeExecutionNotification', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new OverseasRealtimeQuote(mock);
      await expect(quote.unsubscribeExecutionNotification('HTSID0001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });
  });

  describe('subscribe/unsubscribe orderbook', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeOrderbook('AAPL', 'NAS');
      expect(mock.subscribe).toHaveBeenCalledWith('HDFSASP0', 'RNASAAPL');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.unsubscribeOrderbook('AAPL', 'NAS');
      expect(mock.unsubscribe).toHaveBeenCalledWith('HDFSASP0', 'RNASAAPL');
    });
  });

  describe('subscribe/unsubscribe execution', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeExecution('DNASAAPL');
      expect(mock.subscribe).toHaveBeenCalledWith('HDFSCNT0', 'DNASAAPL');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.unsubscribeExecution('DNASAAPL');
      expect(mock.unsubscribe).toHaveBeenCalledWith('HDFSCNT0', 'DNASAAPL');
    });
  });

  describe('subscribe/unsubscribe delayed orderbook', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeDelayedOrderbook('DHKS00003');
      expect(mock.subscribe).toHaveBeenCalledWith('HDFSASP1', 'DHKS00003');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.unsubscribeDelayedOrderbook('DHKS00003');
      expect(mock.unsubscribe).toHaveBeenCalledWith('HDFSASP1', 'DHKS00003');
    });
  });

  describe('subscribe/unsubscribe execution notification', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.subscribeExecutionNotification('HTSID0001');
      expect(mock.subscribe).toHaveBeenCalledWith('H0GSCNI0', 'HTSID0001');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new OverseasRealtimeQuote(mock);
      await quote.unsubscribeExecutionNotification('HTSID0001');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0GSCNI0', 'HTSID0001');
    });
  });
});

describe('parseOrderbookData', () => {
  it('should parse single record correctly', () => {
    const result = OverseasRealtimeQuote.parseOrderbookData(sampleOrderbookData);
    expect(result).toHaveLength(1);
    expect(result[0]!.rsym).toBe('DNASAAPL');
    expect(result[0]!.symb).toBe('AAPL');
    expect(result[0]!.zdiv).toBe('2');
    expect(result[0]!.pbid1).toBe('190.50');
    expect(result[0]!.pask1).toBe('190.60');
    expect(result[0]!.pbid10).toBe('189.60');
    expect(result[0]!.dask10).toBe('-290');
  });

  it('should throw on insufficient fields', () => {
    expect(() => OverseasRealtimeQuote.parseOrderbookData(['DNASAAPL', 'AAPL'])).toThrow(
      'Expected at least 71 fields, got 2',
    );
  });

  it('should throw on empty data', () => {
    expect(() => OverseasRealtimeQuote.parseOrderbookData([])).toThrow('Expected at least 71 fields, got 0');
  });

  it('should handle extra fields (forward compatibility)', () => {
    const data = [...sampleOrderbookData, 'extra1', 'extra2'];
    const result = OverseasRealtimeQuote.parseOrderbookData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.rsym).toBe('DNASAAPL');
  });
});

describe('parseDelayedOrderbookData', () => {
  it('should parse single record correctly', () => {
    const result = OverseasRealtimeQuote.parseDelayedOrderbookData(sampleDelayedOrderbookData);
    expect(result).toHaveLength(1);
    expect(result[0]!.rsym).toBe('DHKS00003');
    expect(result[0]!.symb).toBe('00003');
    expect(result[0]!.pbid1).toBe('25.50');
    expect(result[0]!.pask1).toBe('25.60');
    expect(result[0]!.dask1).toBe('-60');
  });

  it('should parse batched records (2 x 17)', () => {
    const batched = [...sampleDelayedOrderbookData, ...sampleDelayedOrderbookData];
    batched[17] = 'DHKS00005';
    const result = OverseasRealtimeQuote.parseDelayedOrderbookData(batched);
    expect(result).toHaveLength(2);
    expect(result[0]!.rsym).toBe('DHKS00003');
    expect(result[1]!.rsym).toBe('DHKS00005');
  });

  it('should throw on insufficient fields', () => {
    expect(() => OverseasRealtimeQuote.parseDelayedOrderbookData(['DHKS00003', '00003'])).toThrow(
      'Expected at least 17 fields, got 2',
    );
  });

  it('should throw on empty data', () => {
    expect(() => OverseasRealtimeQuote.parseDelayedOrderbookData([])).toThrow('Expected at least 17 fields, got 0');
  });
});

describe('parseExecutionData', () => {
  it('should parse single record correctly', () => {
    const result = OverseasRealtimeQuote.parseExecutionData(sampleExecutionData);
    expect(result).toHaveLength(1);
    expect(result[0]!.rsym).toBe('DNASAAPL');
    expect(result[0]!.symb).toBe('AAPL');
    expect(result[0]!.open).toBe('189.00');
    expect(result[0]!.high).toBe('191.50');
    expect(result[0]!.last).toBe('190.50');
    expect(result[0]!.sign).toBe('2');
    expect(result[0]!.diff).toBe('1.50');
    expect(result[0]!.rate).toBe('0.79');
    expect(result[0]!.strn).toBe('118.00');
    expect(result[0]!.mtyp).toBe('1');
  });

  it('should parse batched records (2 x 26 = 52 fields)', () => {
    const batched = [...sampleExecutionData, ...sampleExecutionData];
    batched[26 + 11] = '191.00'; // second record's last price
    const result = OverseasRealtimeQuote.parseExecutionData(batched);
    expect(result).toHaveLength(2);
    expect(result[0]!.last).toBe('190.50');
    expect(result[1]!.last).toBe('191.00');
  });

  it('should handle extra fields (forward compatibility)', () => {
    const data = [...sampleExecutionData, 'extra1', 'extra2'];
    const result = OverseasRealtimeQuote.parseExecutionData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.mtyp).toBe('1');
  });

  it('should throw on insufficient fields', () => {
    expect(() => OverseasRealtimeQuote.parseExecutionData(['DNASAAPL', 'AAPL'])).toThrow(
      'Expected at least 26 fields, got 2',
    );
  });

  it('should throw on empty data', () => {
    expect(() => OverseasRealtimeQuote.parseExecutionData([])).toThrow('Expected at least 26 fields, got 0');
  });

  it('should parse large batch (50 x 26)', () => {
    const data = Array(50 * 26).fill('value');
    const result = OverseasRealtimeQuote.parseExecutionData(data);
    expect(result).toHaveLength(50);
  });
});

describe('parseExecutionNotificationData', () => {
  it('should parse single record correctly', () => {
    const result = OverseasRealtimeQuote.parseExecutionNotificationData(sampleExecutionNotificationData);
    expect(result).toHaveLength(1);
    expect(result[0]!.custId).toBe('CUST0001');
    expect(result[0]!.acntNo).toBe('1234567890');
    expect(result[0]!.oderNo).toBe('0000000001');
    expect(result[0]!.selnByovCls).toBe('02');
    expect(result[0]!.stckShrnIscd).toBe('AAPL');
    expect(result[0]!.cntgQty).toBe('100');
    expect(result[0]!.cntgUnpr).toBe('190.50');
    expect(result[0]!.acntName).toBe('홍길동계좌');
    expect(result[0]!.cntgIsnm).toBe('APPLE INC');
    expect(result[0]!.cntgUnpr12).toBe('190.500000000000');
  });

  it('should parse batched records (3 x 25)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 3; i++) {
      const record = [...sampleExecutionNotificationData];
      record[2] = `000000000${i + 1}`;
      batched.push(...record);
    }
    const result = OverseasRealtimeQuote.parseExecutionNotificationData(batched);
    expect(result).toHaveLength(3);
    for (let i = 0; i < 3; i++) {
      expect(result[i]!.oderNo).toBe(`000000000${i + 1}`);
    }
  });

  it('should handle extra fields', () => {
    const data = [...sampleExecutionNotificationData, 'extra1', 'extra2'];
    const result = OverseasRealtimeQuote.parseExecutionNotificationData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.custId).toBe('CUST0001');
  });

  it('should throw on insufficient fields', () => {
    expect(() => OverseasRealtimeQuote.parseExecutionNotificationData(['CUST0001', '1234567890'])).toThrow(
      'Expected at least 25 fields, got 2',
    );
  });

  it('should throw on empty data', () => {
    expect(() => OverseasRealtimeQuote.parseExecutionNotificationData([])).toThrow(
      'Expected at least 25 fields, got 0',
    );
  });
});

describe('Field name constants', () => {
  it('OVERSEAS_ORDERBOOK_FIELD_NAMES should have 71 entries', () => {
    expect(OVERSEAS_ORDERBOOK_FIELD_NAMES).toHaveLength(71);
  });

  it('OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES should have 17 entries', () => {
    expect(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES).toHaveLength(17);
  });

  it('OVERSEAS_EXECUTION_FIELD_NAMES should have 26 entries', () => {
    expect(OVERSEAS_EXECUTION_FIELD_NAMES).toHaveLength(26);
  });

  it('OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES should have 25 entries', () => {
    expect(OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES).toHaveLength(25);
  });

  it('should have no duplicate field names in each list', () => {
    expect(new Set(OVERSEAS_ORDERBOOK_FIELD_NAMES).size).toBe(OVERSEAS_ORDERBOOK_FIELD_NAMES.length);
    expect(new Set(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES).size).toBe(OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES.length);
    expect(new Set(OVERSEAS_EXECUTION_FIELD_NAMES).size).toBe(OVERSEAS_EXECUTION_FIELD_NAMES.length);
    expect(new Set(OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES).size).toBe(
      OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES.length,
    );
  });
});
