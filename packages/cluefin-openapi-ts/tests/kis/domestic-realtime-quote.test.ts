import { describe, expect, it, vi } from 'vitest';
import { DomesticRealtimeQuote } from '../../src/kis/domestic-realtime-quote';
import type { KisSocketClient } from '../../src/kis/socket-client';
import {
  EXECUTION_FIELD_NAMES,
  EXECUTION_NOTIFICATION_FIELD_NAMES,
  ORDERBOOK_FIELD_NAMES,
} from '../../src/kis/metadata/domestic-realtime-quote';

function createMockSocketClient(env: 'prod' | 'dev' = 'prod'): KisSocketClient {
  return {
    env,
    subscribe: vi.fn().mockResolvedValue(undefined),
    unsubscribe: vi.fn().mockResolvedValue(undefined),
  } as unknown as KisSocketClient;
}

// Sample test data
const sampleExecutionData: string[] = [
  '005930', '093000', '70000', '2', '1000', '1.45', '69500', '69000', '70500', '68500',
  '70100', '70000', '100', '5000000', '350000000000', '1234', '1456', '222', '118.00',
  '2500000', '2950000', '1', '54.12', '110.50', '090000', '2', '1000', '091530', '2',
  '-500', '093500', '5', '1500', '20251224', '20', 'N', '50000', '45000', '500000',
  '450000', '0.83', '4500000', '111.11', '0', '0', '68000',
];

const sampleOrderbookData: string[] = [
  '005930', '093000', '0', '70100', '70200', '70300', '70400', '70500', '70600', '70700',
  '70800', '70900', '71000', '70000', '69900', '69800', '69700', '69600', '69500', '69400',
  '69300', '69200', '69100', '10000', '20000', '30000', '40000', '50000', '60000', '70000',
  '80000', '90000', '100000', '15000', '25000', '35000', '45000', '55000', '65000', '75000',
  '85000', '95000', '105000', '550000', '600000', '1000', '2000', '70050', '5000',
  '10000000', '50', '2', '0.07', '5000000', '10000', '-5000', '100', '-200', '00',
];

const sampleExecutionNotificationData: string[] = [
  'CUST0001', '1234567890', '0000000001', '0000000000', '02', '0', '00', '0', '005930',
  '100', '70000', '093000', '0', '2', '2', '00001', '100', '홍길동계좌', '0', '1', 'Y',
  '   ', '00', '        ', '삼성전자', '70000',
];

describe('DomesticRealtimeQuote', () => {
  describe('TR_ID constants', () => {
    it('should have correct TR_ID values', () => {
      expect(DomesticRealtimeQuote.TR_ID_EXECUTION).toBe('H0UNCNT0');
      expect(DomesticRealtimeQuote.TR_ID_ORDERBOOK).toBe('H0STASP0');
      expect(DomesticRealtimeQuote.TR_ID_EXECUTION_NOTIFICATION).toBe('H0STCNI0');
    });
  });

  describe('subscribe/unsubscribe execution', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new DomesticRealtimeQuote(mock);
      await quote.subscribeExecution('005930');
      expect(mock.subscribe).toHaveBeenCalledWith('H0UNCNT0', '005930');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new DomesticRealtimeQuote(mock);
      await quote.unsubscribeExecution('005930');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0UNCNT0', '005930');
    });
  });

  describe('subscribe/unsubscribe orderbook', () => {
    it('should call socketClient.subscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new DomesticRealtimeQuote(mock);
      await quote.subscribeOrderbook('005930');
      expect(mock.subscribe).toHaveBeenCalledWith('H0STASP0', '005930');
    });

    it('should call socketClient.unsubscribe with correct args', async () => {
      const mock = createMockSocketClient();
      const quote = new DomesticRealtimeQuote(mock);
      await quote.unsubscribeOrderbook('005930');
      expect(mock.unsubscribe).toHaveBeenCalledWith('H0STASP0', '005930');
    });
  });

  describe('subscribe/unsubscribe execution notification', () => {
    it('should call socketClient.subscribe in prod env', async () => {
      const mock = createMockSocketClient('prod');
      const quote = new DomesticRealtimeQuote(mock);
      await quote.subscribeExecutionNotification('HTSID0000001');
      expect(mock.subscribe).toHaveBeenCalledWith('H0STCNI0', 'HTSID0000001');
    });

    it('should throw in dev env for subscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new DomesticRealtimeQuote(mock);
      await expect(quote.subscribeExecutionNotification('HTSID0000001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });

    it('should throw in dev env for unsubscribe', async () => {
      const mock = createMockSocketClient('dev');
      const quote = new DomesticRealtimeQuote(mock);
      await expect(quote.unsubscribeExecutionNotification('HTSID0000001')).rejects.toThrow(
        '운영 서버(prod)에서만 사용 가능',
      );
    });
  });
});

describe('parseExecutionData', () => {
  it('should parse single record correctly', () => {
    const result = DomesticRealtimeQuote.parseExecutionData(sampleExecutionData);
    expect(result).toHaveLength(1);
    expect(result[0]!.mkscShrnIscd).toBe('005930');
    expect(result[0]!.stckCntgHour).toBe('093000');
    expect(result[0]!.stckPrpr).toBe('70000');
    expect(result[0]!.prdyVrssSign).toBe('2');
    expect(result[0]!.acmlVol).toBe('5000000');
    expect(result[0]!.cttr).toBe('118.00');
    expect(result[0]!.bsopDate).toBe('20251224');
    expect(result[0]!.trhtYn).toBe('N');
    expect(result[0]!.viStndPrc).toBe('68000');
  });

  it('should parse batched records (12 x 46)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 12; i++) {
      const record = [...sampleExecutionData];
      record[2] = String(70000 + i * 100);
      batched.push(...record);
    }
    const result = DomesticRealtimeQuote.parseExecutionData(batched);
    expect(result).toHaveLength(12);
    for (let i = 0; i < 12; i++) {
      expect(result[i]!.stckPrpr).toBe(String(70000 + i * 100));
    }
  });

  it('should handle extra fields (forward compatibility)', () => {
    const data = [...sampleExecutionData, 'extra1', 'extra2', 'extra3'];
    const result = DomesticRealtimeQuote.parseExecutionData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.mkscShrnIscd).toBe('005930');
    expect(result[0]!.viStndPrc).toBe('68000');
  });

  it('should throw on insufficient fields', () => {
    expect(() => DomesticRealtimeQuote.parseExecutionData(['005930', '093000', '70000'])).toThrow(
      'Expected at least 46 fields, got 3',
    );
  });

  it('should throw on empty data', () => {
    expect(() => DomesticRealtimeQuote.parseExecutionData([])).toThrow(
      'Expected at least 46 fields, got 0',
    );
  });

  it('should parse large batch (50 x 46)', () => {
    const data = Array(50 * 46).fill('value');
    const result = DomesticRealtimeQuote.parseExecutionData(data);
    expect(result).toHaveLength(50);
  });
});

describe('parseOrderbookData', () => {
  it('should parse single record correctly', () => {
    const result = DomesticRealtimeQuote.parseOrderbookData(sampleOrderbookData);
    expect(result).toHaveLength(1);
    expect(result[0]!.mkscShrnIscd).toBe('005930');
    expect(result[0]!.bsopHour).toBe('093000');
    expect(result[0]!.askp1).toBe('70100');
    expect(result[0]!.bidp1).toBe('70000');
    expect(result[0]!.totalAskpRsqn).toBe('550000');
    expect(result[0]!.totalBidpRsqn).toBe('600000');
    expect(result[0]!.antcCnpr).toBe('70050');
    expect(result[0]!.acmlVol).toBe('5000000');
  });

  it('should parse batched records (10 x 59)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 10; i++) {
      const record = [...sampleOrderbookData];
      record[3] = String(70100 + i * 10);
      batched.push(...record);
    }
    const result = DomesticRealtimeQuote.parseOrderbookData(batched);
    expect(result).toHaveLength(10);
    for (let i = 0; i < 10; i++) {
      expect(result[i]!.askp1).toBe(String(70100 + i * 10));
    }
  });

  it('should handle extra fields', () => {
    const data = [...sampleOrderbookData, 'extra1', 'extra2', 'extra3'];
    const result = DomesticRealtimeQuote.parseOrderbookData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.stckDealClsCode).toBe('00');
  });

  it('should throw on insufficient fields', () => {
    expect(() => DomesticRealtimeQuote.parseOrderbookData(['005930', '093000', '0'])).toThrow(
      'Expected at least 59 fields, got 3',
    );
  });

  it('should throw on empty data', () => {
    expect(() => DomesticRealtimeQuote.parseOrderbookData([])).toThrow(
      'Expected at least 59 fields, got 0',
    );
  });
});

describe('parseExecutionNotificationData', () => {
  it('should parse single record correctly', () => {
    const result = DomesticRealtimeQuote.parseExecutionNotificationData(sampleExecutionNotificationData);
    expect(result).toHaveLength(1);
    expect(result[0]!.custId).toBe('CUST0001');
    expect(result[0]!.acntNo).toBe('1234567890');
    expect(result[0]!.oderNo).toBe('0000000001');
    expect(result[0]!.selnByovCls).toBe('02');
    expect(result[0]!.stckShrnIscd).toBe('005930');
    expect(result[0]!.cntgQty).toBe('100');
    expect(result[0]!.cntgUnpr).toBe('70000');
    expect(result[0]!.acntName).toBe('홍길동계좌');
    expect(result[0]!.cntgIsnm40).toBe('삼성전자');
    expect(result[0]!.oderPrc).toBe('70000');
  });

  it('should parse batched records (5 x 26)', () => {
    const batched: string[] = [];
    for (let i = 0; i < 5; i++) {
      const record = [...sampleExecutionNotificationData];
      record[2] = `000000000${i + 1}`;
      batched.push(...record);
    }
    const result = DomesticRealtimeQuote.parseExecutionNotificationData(batched);
    expect(result).toHaveLength(5);
    for (let i = 0; i < 5; i++) {
      expect(result[i]!.oderNo).toBe(`000000000${i + 1}`);
    }
  });

  it('should handle extra fields', () => {
    const data = [...sampleExecutionNotificationData, 'extra1', 'extra2', 'extra3'];
    const result = DomesticRealtimeQuote.parseExecutionNotificationData(data);
    expect(result).toHaveLength(1);
    expect(result[0]!.custId).toBe('CUST0001');
    expect(result[0]!.oderPrc).toBe('70000');
  });

  it('should throw on insufficient fields', () => {
    expect(() =>
      DomesticRealtimeQuote.parseExecutionNotificationData(['CUST0001', '1234567890', '0000000001']),
    ).toThrow('Expected at least 26 fields, got 3');
  });

  it('should throw on empty data', () => {
    expect(() => DomesticRealtimeQuote.parseExecutionNotificationData([])).toThrow(
      'Expected at least 26 fields, got 0',
    );
  });
});

describe('Field name constants', () => {
  it('EXECUTION_FIELD_NAMES should have 46 entries', () => {
    expect(EXECUTION_FIELD_NAMES).toHaveLength(46);
  });

  it('ORDERBOOK_FIELD_NAMES should have 59 entries', () => {
    expect(ORDERBOOK_FIELD_NAMES).toHaveLength(59);
  });

  it('EXECUTION_NOTIFICATION_FIELD_NAMES should have 26 entries', () => {
    expect(EXECUTION_NOTIFICATION_FIELD_NAMES).toHaveLength(26);
  });

  it('should have no duplicate field names in each list', () => {
    expect(new Set(EXECUTION_FIELD_NAMES).size).toBe(EXECUTION_FIELD_NAMES.length);
    expect(new Set(ORDERBOOK_FIELD_NAMES).size).toBe(ORDERBOOK_FIELD_NAMES.length);
    expect(new Set(EXECUTION_NOTIFICATION_FIELD_NAMES).size).toBe(EXECUTION_NOTIFICATION_FIELD_NAMES.length);
  });
});
