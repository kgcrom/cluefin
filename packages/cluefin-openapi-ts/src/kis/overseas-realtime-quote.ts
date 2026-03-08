import {
  OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES,
  OVERSEAS_EXECUTION_FIELD_NAMES,
  OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES,
  OVERSEAS_ORDERBOOK_FIELD_NAMES,
  type OverseasRealtimeDelayedOrderbookItem,
  type OverseasRealtimeExecutionItem,
  type OverseasRealtimeExecutionNotificationItem,
  type OverseasRealtimeOrderbookItem,
} from './metadata/overseas-realtime-quote';
import type { KisSocketClient } from './socket-client';

const TR_ID_ORDERBOOK = 'HDFSASP0';
const TR_ID_EXECUTION = 'HDFSCNT0';
const TR_ID_DELAYED_ORDERBOOK = 'HDFSASP1';
const TR_ID_EXECUTION_NOTIFICATION = 'H0GSCNI0';

function parseRecords<T>(data: string[], fieldNames: readonly string[]): T[] {
  const fieldCount = fieldNames.length;

  if (data.length < fieldCount) {
    throw new Error(`Expected at least ${fieldCount} fields, got ${data.length}. First field: ${data[0] ?? 'empty'}`);
  }

  const numRecords = Math.floor(data.length / fieldCount);
  const results: T[] = [];

  for (let i = 0; i < numRecords; i++) {
    const startIdx = i * fieldCount;
    const entries = fieldNames.map((name, j) => [name, data[startIdx + j] ?? ''] as const);
    results.push(Object.fromEntries(entries) as T);
  }

  return results;
}

export class OverseasRealtimeQuote {
  static readonly TR_ID_ORDERBOOK = TR_ID_ORDERBOOK;
  static readonly TR_ID_EXECUTION = TR_ID_EXECUTION;
  static readonly TR_ID_DELAYED_ORDERBOOK = TR_ID_DELAYED_ORDERBOOK;
  static readonly TR_ID_EXECUTION_NOTIFICATION = TR_ID_EXECUTION_NOTIFICATION;

  constructor(private readonly socketClient: KisSocketClient) {}

  private requireProdEnv(): void {
    if (this.socketClient.env !== 'prod') {
      throw new Error(
        `해외주식 실시간시세는 운영 서버(prod)에서만 사용 가능합니다. 현재 환경: ${this.socketClient.env}`,
      );
    }
  }

  private generateTrKey(stockCode: string, marketCode: string, serviceType: string = 'R'): string {
    return `${serviceType}${marketCode}${stockCode}`;
  }

  // 호가
  async subscribeOrderbook(stockCode: string, marketCode: string, serviceType: string = 'R'): Promise<void> {
    this.requireProdEnv();
    const trKey = this.generateTrKey(stockCode, marketCode, serviceType);
    await this.socketClient.subscribe(TR_ID_ORDERBOOK, trKey);
  }

  async unsubscribeOrderbook(stockCode: string, marketCode: string, serviceType: string = 'R'): Promise<void> {
    this.requireProdEnv();
    const trKey = this.generateTrKey(stockCode, marketCode, serviceType);
    await this.socketClient.unsubscribe(TR_ID_ORDERBOOK, trKey);
  }

  static parseOrderbookData(data: string[]): OverseasRealtimeOrderbookItem[] {
    return parseRecords<OverseasRealtimeOrderbookItem>(data, OVERSEAS_ORDERBOOK_FIELD_NAMES);
  }

  // 체결
  async subscribeExecution(trKey: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_EXECUTION, trKey);
  }

  async unsubscribeExecution(trKey: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_EXECUTION, trKey);
  }

  static parseExecutionData(data: string[]): OverseasRealtimeExecutionItem[] {
    return parseRecords<OverseasRealtimeExecutionItem>(data, OVERSEAS_EXECUTION_FIELD_NAMES);
  }

  // 지연호가(아시아)
  async subscribeDelayedOrderbook(trKey: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_DELAYED_ORDERBOOK, trKey);
  }

  async unsubscribeDelayedOrderbook(trKey: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_DELAYED_ORDERBOOK, trKey);
  }

  static parseDelayedOrderbookData(data: string[]): OverseasRealtimeDelayedOrderbookItem[] {
    return parseRecords<OverseasRealtimeDelayedOrderbookItem>(data, OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES);
  }

  // 체결통보
  async subscribeExecutionNotification(htsId: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_EXECUTION_NOTIFICATION, htsId);
  }

  async unsubscribeExecutionNotification(htsId: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_EXECUTION_NOTIFICATION, htsId);
  }

  static parseExecutionNotificationData(data: string[]): OverseasRealtimeExecutionNotificationItem[] {
    return parseRecords<OverseasRealtimeExecutionNotificationItem>(data, OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES);
  }
}
