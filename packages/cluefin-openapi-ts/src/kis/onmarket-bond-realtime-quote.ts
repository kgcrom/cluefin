import {
  BOND_EXECUTION_FIELD_NAMES,
  BOND_INDEX_EXECUTION_FIELD_NAMES,
  BOND_ORDERBOOK_FIELD_NAMES,
  type BondRealtimeExecutionItem,
  type BondRealtimeIndexExecutionItem,
  type BondRealtimeOrderbookItem,
} from './metadata/onmarket-bond-realtime-quote';
import type { KisSocketClient } from './socket-client';

const TR_ID_BOND_EXECUTION = 'H0BJCNT0';
const TR_ID_BOND_ORDERBOOK = 'H0BJASP0';
const TR_ID_BOND_INDEX_EXECUTION = 'H0BICNT0';

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

export class OnmarketBondRealtimeQuote {
  static readonly TR_ID_BOND_EXECUTION = TR_ID_BOND_EXECUTION;
  static readonly TR_ID_BOND_ORDERBOOK = TR_ID_BOND_ORDERBOOK;
  static readonly TR_ID_BOND_INDEX_EXECUTION = TR_ID_BOND_INDEX_EXECUTION;

  constructor(private readonly socketClient: KisSocketClient) {}

  private requireProdEnv(): void {
    if (this.socketClient.env !== 'prod') {
      throw new Error(
        `장내채권 실시간시세는 운영 서버(prod)에서만 사용 가능합니다. 현재 환경: ${this.socketClient.env}`,
      );
    }
  }

  async subscribeBondExecution(bondCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_BOND_EXECUTION, bondCode);
  }

  async unsubscribeBondExecution(bondCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_BOND_EXECUTION, bondCode);
  }

  static parseBondExecutionData(data: string[]): BondRealtimeExecutionItem[] {
    return parseRecords<BondRealtimeExecutionItem>(data, BOND_EXECUTION_FIELD_NAMES);
  }

  async subscribeBondOrderbook(bondCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_BOND_ORDERBOOK, bondCode);
  }

  async unsubscribeBondOrderbook(bondCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_BOND_ORDERBOOK, bondCode);
  }

  static parseBondOrderbookData(data: string[]): BondRealtimeOrderbookItem[] {
    return parseRecords<BondRealtimeOrderbookItem>(data, BOND_ORDERBOOK_FIELD_NAMES);
  }

  async subscribeBondIndexExecution(indexCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.subscribe(TR_ID_BOND_INDEX_EXECUTION, indexCode);
  }

  async unsubscribeBondIndexExecution(indexCode: string): Promise<void> {
    this.requireProdEnv();
    await this.socketClient.unsubscribe(TR_ID_BOND_INDEX_EXECUTION, indexCode);
  }

  static parseBondIndexExecutionData(data: string[]): BondRealtimeIndexExecutionItem[] {
    return parseRecords<BondRealtimeIndexExecutionItem>(data, BOND_INDEX_EXECUTION_FIELD_NAMES);
  }
}
