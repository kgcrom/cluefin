import type { KisSocketClient } from './socket-client';
import {
  EXECUTION_FIELD_NAMES,
  EXECUTION_NOTIFICATION_FIELD_NAMES,
  ORDERBOOK_FIELD_NAMES,
  type DomesticRealtimeExecutionItem,
  type DomesticRealtimeExecutionNotificationItem,
  type DomesticRealtimeOrderbookItem,
} from './metadata/domestic-realtime-quote';

const TR_ID_EXECUTION = 'H0UNCNT0';
const TR_ID_ORDERBOOK = 'H0STASP0';
const TR_ID_EXECUTION_NOTIFICATION = 'H0STCNI0';

function parseRecords<T>(data: string[], fieldNames: readonly string[]): T[] {
  const fieldCount = fieldNames.length;

  if (data.length < fieldCount) {
    throw new Error(
      `Expected at least ${fieldCount} fields, got ${data.length}. First field: ${data[0] ?? 'empty'}`,
    );
  }

  const numRecords = Math.floor(data.length / fieldCount);
  const results: T[] = [];

  for (let i = 0; i < numRecords; i++) {
    const startIdx = i * fieldCount;
    const record: Record<string, string> = {};
    for (let j = 0; j < fieldCount; j++) {
      record[fieldNames[j]!] = data[startIdx + j]!;
    }
    results.push(record as T);
  }

  return results;
}

export class DomesticRealtimeQuote {
  static readonly TR_ID_EXECUTION = TR_ID_EXECUTION;
  static readonly TR_ID_ORDERBOOK = TR_ID_ORDERBOOK;
  static readonly TR_ID_EXECUTION_NOTIFICATION = TR_ID_EXECUTION_NOTIFICATION;

  constructor(private readonly socketClient: KisSocketClient) {}

  private requireProdEnv(): void {
    if (this.socketClient.env !== 'prod') {
      throw new Error(
        `실시간 체결통보는 운영 서버(prod)에서만 사용 가능합니다. 현재 환경: ${this.socketClient.env}`,
      );
    }
  }

  async subscribeExecution(stockCode: string): Promise<void> {
    await this.socketClient.subscribe(TR_ID_EXECUTION, stockCode);
  }

  async unsubscribeExecution(stockCode: string): Promise<void> {
    await this.socketClient.unsubscribe(TR_ID_EXECUTION, stockCode);
  }

  static parseExecutionData(data: string[]): DomesticRealtimeExecutionItem[] {
    return parseRecords<DomesticRealtimeExecutionItem>(data, EXECUTION_FIELD_NAMES);
  }

  async subscribeOrderbook(stockCode: string): Promise<void> {
    await this.socketClient.subscribe(TR_ID_ORDERBOOK, stockCode);
  }

  async unsubscribeOrderbook(stockCode: string): Promise<void> {
    await this.socketClient.unsubscribe(TR_ID_ORDERBOOK, stockCode);
  }

  static parseOrderbookData(data: string[]): DomesticRealtimeOrderbookItem[] {
    return parseRecords<DomesticRealtimeOrderbookItem>(data, ORDERBOOK_FIELD_NAMES);
  }

  async subscribeExecutionNotification(htsId: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_EXECUTION_NOTIFICATION, htsId);
  }

  async unsubscribeExecutionNotification(htsId: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_EXECUTION_NOTIFICATION, htsId);
  }

  static parseExecutionNotificationData(data: string[]): DomesticRealtimeExecutionNotificationItem[] {
    return parseRecords<DomesticRealtimeExecutionNotificationItem>(data, EXECUTION_NOTIFICATION_FIELD_NAMES);
  }
}
