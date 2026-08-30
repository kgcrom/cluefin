import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);
const packageRoot = path.resolve(scriptDir, '..');
const typesDir = path.join(packageRoot, 'dist', 'types');
const typesPath = path.join(typesDir, 'index.d.ts');

const extractMethodNames = (metadataRelPath) => {
  const fullPath = path.join(packageRoot, metadataRelPath);
  const source = fs.readFileSync(fullPath, 'utf8');
  const matches = [...source.matchAll(/methodName:\s*'([^']+)'/g)];
  return matches.map((m) => m[1]);
};

const renderDomainClass = (className, methods) => {
  const methodLines = methods.map((m) => `  ${m}(input: Record<string, unknown>): Promise<ApiResponse>;`).join('\n');
  return `export declare class ${className} {\n${methodLines}\n}`;
};

const kisDomains = [
  { className: 'DomesticAccount', metadataPath: 'src/kis/metadata/domestic-account.ts', prop: 'domesticAccount' },
  {
    className: 'DomesticBasicQuote',
    metadataPath: 'src/kis/metadata/domestic-basic-quote.ts',
    prop: 'domesticBasicQuote',
  },
  {
    className: 'DomesticIssueOther',
    metadataPath: 'src/kis/metadata/domestic-issue-other.ts',
    prop: 'domesticIssueOther',
  },
  {
    className: 'DomesticMarketAnalysis',
    metadataPath: 'src/kis/metadata/domestic-market-analysis.ts',
    prop: 'domesticMarketAnalysis',
  },
  {
    className: 'DomesticRankingAnalysis',
    metadataPath: 'src/kis/metadata/domestic-ranking-analysis.ts',
    prop: 'domesticRankingAnalysis',
  },
  {
    className: 'DomesticStockInfo',
    metadataPath: 'src/kis/metadata/domestic-stock-info.ts',
    prop: 'domesticStockInfo',
  },
  {
    className: 'OnmarketBondBasicQuote',
    metadataPath: 'src/kis/metadata/onmarket-bond-basic-quote.ts',
    prop: 'onmarketBondBasicQuote',
  },
  {
    className: 'OverseasBasicQuote',
    metadataPath: 'src/kis/metadata/overseas-basic-quote.ts',
    prop: 'overseasBasicQuote',
  },
  { className: 'OverseasAccount', metadataPath: 'src/kis/metadata/overseas-account.ts', prop: 'overseasAccount' },
  {
    className: 'OverseasMarketAnalysis',
    metadataPath: 'src/kis/metadata/overseas-market-analysis.ts',
    prop: 'overseasMarketAnalysis',
  },
];

const kiwoomDomains = [
  {
    className: 'KiwoomDomesticAccount',
    metadataPath: 'src/kiwoom/metadata/domestic-account.ts',
    prop: 'domesticAccount',
  },
  { className: 'KiwoomDomesticChart', metadataPath: 'src/kiwoom/metadata/domestic-chart.ts', prop: 'domesticChart' },
  { className: 'KiwoomDomesticETF', metadataPath: 'src/kiwoom/metadata/domestic-etf.ts', prop: 'domesticEtf' },
  {
    className: 'KiwoomDomesticForeign',
    metadataPath: 'src/kiwoom/metadata/domestic-foreign.ts',
    prop: 'domesticForeign',
  },
  {
    className: 'KiwoomDomesticMarketCondition',
    metadataPath: 'src/kiwoom/metadata/domestic-market-condition.ts',
    prop: 'domesticMarketCondition',
  },
  { className: 'KiwoomDomesticOrder', metadataPath: 'src/kiwoom/metadata/domestic-order.ts', prop: 'domesticOrder' },
  {
    className: 'KiwoomDomesticRankInfo',
    metadataPath: 'src/kiwoom/metadata/domestic-rank-info.ts',
    prop: 'domesticRankInfo',
  },
  {
    className: 'KiwoomDomesticSector',
    metadataPath: 'src/kiwoom/metadata/domestic-sector.ts',
    prop: 'domesticSector',
  },
  {
    className: 'KiwoomDomesticStockInfo',
    metadataPath: 'src/kiwoom/metadata/domestic-stock-info.ts',
    prop: 'domesticStockInfo',
  },
  { className: 'KiwoomDomesticTheme', metadataPath: 'src/kiwoom/metadata/domestic-theme.ts', prop: 'domesticTheme' },
];

const nhplugDomains = [
  { className: 'NhplugCommon', metadataPath: 'src/nhplug/metadata/common.ts', prop: 'common' },
  {
    className: 'NhplugKrstockOrder',
    metadataPath: 'src/nhplug/metadata/krstock-order.ts',
    prop: 'krstockOrder',
  },
  {
    className: 'NhplugKrstockInquiry',
    metadataPath: 'src/nhplug/metadata/krstock-inquiry.ts',
    prop: 'krstockInquiry',
  },
  {
    className: 'NhplugKrstockQuote',
    metadataPath: 'src/nhplug/metadata/krstock-quote.ts',
    prop: 'krstockQuote',
  },
  {
    className: 'NhplugOverseasStockOrder',
    metadataPath: 'src/nhplug/metadata/overseas-stock-order.ts',
    prop: 'overseasStockOrder',
  },
  {
    className: 'NhplugOverseasStockInquiry',
    metadataPath: 'src/nhplug/metadata/overseas-stock-inquiry.ts',
    prop: 'overseasStockInquiry',
  },
  {
    className: 'NhplugOverseasStockQuote',
    metadataPath: 'src/nhplug/metadata/overseas-stock-quote.ts',
    prop: 'overseasStockQuote',
  },
];

const kisDomainDecls = kisDomains
  .map((d) => renderDomainClass(d.className, extractMethodNames(d.metadataPath)))
  .join('\n\n');

const kiwoomDomainDecls = kiwoomDomains
  .map((d) => renderDomainClass(d.className, extractMethodNames(d.metadataPath)))
  .join('\n\n');

const nhplugDomainDecls = nhplugDomains
  .map((d) => renderDomainClass(d.className, extractMethodNames(d.metadataPath)))
  .join('\n\n');

const kisClientProps = kisDomains.map((d) => `  readonly ${d.prop}: ${d.className};`).join('\n');
const kiwoomClientProps = kiwoomDomains.map((d) => `  readonly ${d.prop}: ${d.className};`).join('\n');
const nhplugClientProps = nhplugDomains.map((d) => `  readonly ${d.prop}: ${d.className};`).join('\n');

const content = `export type ApiEnv = 'dev' | 'prod';

export interface ApiResponse<TBody = Record<string, unknown>> {
  headers: Record<string, string>;
  body: TBody;
}

export interface RateLimitOptions {
  requestsPerSecond: number;
  burst: number;
}

export interface Logger {
  debug(message: string, context?: Record<string, unknown>): void;
  warn(message: string, context?: Record<string, unknown>): void;
  error(message: string, context?: Record<string, unknown>): void;
}

export const consoleLogger: Logger;
export const silentLogger: Logger;

export type SubscriptionType = '1' | '2';
export type MessageType = 'PINGPONG' | 'DATA' | 'SYSTEM';
export type WebSocketEventType =
  | 'data'
  | 'connected'
  | 'disconnected'
  | 'error'
  | 'subscribed'
  | 'unsubscribed'
  | 'system';

export interface WebSocketMessage {
  messageType: MessageType;
  trId?: string | undefined;
  trKey?: string | undefined;
  data?: string[] | undefined;
  body?: Record<string, unknown> | undefined;
  raw: string;
  encrypted: boolean;
}

export interface WebSocketEvent {
  eventType: WebSocketEventType;
  trId?: string;
  trKey?: string;
  data?: { values: string[]; encrypted: boolean };
  body?: Record<string, unknown>;
  error?: Error;
  raw?: string;
}

export interface BaseWebSocketClientOptions {
  url: string;
  rateLimitBurst: number;
  rateLimitRequestsPerSecond: number;
}

export interface BaseWebSocketClientEvents {
  data: [event: WebSocketEvent];
  connected: [event: WebSocketEvent];
  disconnected: [event: WebSocketEvent];
  error: [event: WebSocketEvent];
  subscribed: [event: WebSocketEvent];
  unsubscribed: [event: WebSocketEvent];
  system: [event: WebSocketEvent];
}

export class BaseWebSocketClient {
  constructor(options: BaseWebSocketClientOptions);
  readonly connected: boolean;
  readonly subscriptions: Map<string, string>;
  connect(): void;
  close(): void;
  subscribe(trId: string, trKey: string): Promise<void>;
  unsubscribe(trId: string, trKey: string): Promise<void>;
  parseMessage(raw: string): WebSocketMessage;
  on<K extends keyof BaseWebSocketClientEvents>(
    eventType: K,
    listener: (...args: BaseWebSocketClientEvents[K]) => void,
  ): this;
  once<K extends keyof BaseWebSocketClientEvents>(
    eventType: K,
    listener: (...args: BaseWebSocketClientEvents[K]) => void,
  ): this;
  off<K extends keyof BaseWebSocketClientEvents>(
    eventType: K,
    listener: (...args: BaseWebSocketClientEvents[K]) => void,
  ): this;
}

export interface EndpointParamDefinition {
  name: string;
  required: boolean;
  defaultValue?: string | number | boolean;
}

export interface KisEndpointDefinition {
  methodName: string;
  method: 'GET' | 'POST';
  path: string;
  trId: string;
  requestMap: Record<string, string>;
  params: EndpointParamDefinition[];
}

export interface KiwoomEndpointDefinition {
  methodName: string;
  path: string;
  apiId: string;
  bodyMap: Record<string, string>;
  headerParamMap: Record<string, string>;
  params: EndpointParamDefinition[];
}

export interface NhplugEndpointDefinition {
  methodName: string;
  path: string;
  bodyMap: Record<string, string>;
  supportsCts: boolean;
  params: EndpointParamDefinition[];
}

export class ApiError extends Error {
  statusCode?: number;
  responseData?: unknown;
  requestContext?: Record<string, unknown>;
  constructor(message: string, details?: {
    statusCode?: number;
    responseData?: unknown;
    requestContext?: Record<string, unknown>;
    retryAfter?: number;
  });
}

export class ApiAuthenticationError extends ApiError {}
export class ApiAuthorizationError extends ApiError {}
export class ApiValidationError extends ApiError {}
export class ApiServerError extends ApiError {}
export class ApiNetworkError extends ApiError {}
export class ApiTimeoutError extends ApiError {}
export class ApiRateLimitError extends ApiError {
  retryAfter?: number;
}

export class KisApiError extends ApiError {}
export class KisAuthenticationError extends ApiAuthenticationError {}
export class KisAuthorizationError extends ApiAuthorizationError {}
export class KisValidationError extends ApiValidationError {}
export class KisServerError extends ApiServerError {}
export class KisNetworkError extends ApiNetworkError {}
export class KisTimeoutError extends ApiTimeoutError {}
export class KisRateLimitError extends ApiRateLimitError {}

export class KiwoomApiError extends ApiError {}
export class KiwoomAuthenticationError extends ApiAuthenticationError {}
export class KiwoomAuthorizationError extends ApiAuthorizationError {}
export class KiwoomValidationError extends ApiValidationError {}
export class KiwoomServerError extends ApiServerError {}
export class KiwoomNetworkError extends ApiNetworkError {}
export class KiwoomTimeoutError extends ApiTimeoutError {}
export class KiwoomRateLimitError extends ApiRateLimitError {}

export class NhplugApiError extends ApiError {}
export class NhplugAuthenticationError extends ApiAuthenticationError {}
export class NhplugAuthorizationError extends ApiAuthorizationError {}
export class NhplugValidationError extends ApiValidationError {}
export class NhplugServerError extends ApiServerError {}
export class NhplugNetworkError extends ApiNetworkError {}
export class NhplugTimeoutError extends ApiTimeoutError {}
export class NhplugRateLimitError extends ApiRateLimitError {}

export interface TokenCacheEntry {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  accessTokenTokenExpired: string;
  cachedAt: string;
}

export interface TokenCacheStore {
  get(): Promise<TokenCacheEntry | null>;
  set(entry: TokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

export class MemoryTokenCacheStore implements TokenCacheStore {
  get(): Promise<TokenCacheEntry | null>;
  set(entry: TokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

export interface KisAuthOptions {
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  tokenCacheStore?: TokenCacheStore;
  fetchImpl?: typeof fetch;
}

export interface KisTokenResponse {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  accessTokenTokenExpired: string;
}

export interface KisApprovalResponse {
  approvalKey: string;
}

export class KisAuth {
  constructor(options: KisAuthOptions);
  generate(): Promise<KisTokenResponse>;
  revoke(token?: string): Promise<boolean>;
  approve(): Promise<KisApprovalResponse>;
}

export interface KisHttpClientOptions {
  token: string;
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  debug?: boolean;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
}

${kisDomainDecls}

export class KisHttpClient {
  constructor(options: KisHttpClientOptions);
${kisClientProps}
}

export interface KiwoomAuthOptions {
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  fetchImpl?: typeof fetch;
}

export interface KiwoomTokenResponse {
  tokenType: string;
  token: string;
  expiresDt: string;
}

export class KiwoomAuth {
  constructor(options: KiwoomAuthOptions);
  generateToken(): Promise<KiwoomTokenResponse>;
  revokeToken(token: string): Promise<boolean>;
}

export interface KiwoomClientOptions {
  token: string;
  env?: ApiEnv;
  debug?: boolean;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
}

${kiwoomDomainDecls}

export class KiwoomClient {
  constructor(options: KiwoomClientOptions);
${kiwoomClientProps}
}

export const NHPLUG_AUTH_BASE_URL: string;

export interface NhplugTokenCacheEntry {
  accessToken: string;
  scope: string;
  tokenType: string;
  expiresIn: number;
  cachedAt: string;
}

export interface NhplugTokenCacheStore {
  get(): Promise<NhplugTokenCacheEntry | null>;
  set(entry: NhplugTokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

export class NhplugMemoryTokenCacheStore implements NhplugTokenCacheStore {
  get(): Promise<NhplugTokenCacheEntry | null>;
  set(entry: NhplugTokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

export class NhplugFileTokenCacheStore implements NhplugTokenCacheStore {
  constructor(filePath: string);
  get(): Promise<NhplugTokenCacheEntry | null>;
  set(entry: NhplugTokenCacheEntry): Promise<void>;
  clear(): Promise<void>;
}

export function nhplugTokenCacheFileName(appKey?: string): string;

export interface NhplugAuthOptions {
  appKey: string;
  secretKey: string;
  tokenCacheStore?: NhplugTokenCacheStore;
  fetchImpl?: typeof fetch;
}

export interface NhplugTokenResponse {
  accessToken: string;
  scope: string;
  tokenType: string;
  expiresIn: number;
}

export interface NhplugTokenRevokeResponse {
  code?: string | number | undefined;
  message?: string | undefined;
  errorCode?: string | undefined;
  errorDescription?: string | undefined;
}

export class NhplugAuth {
  constructor(options: NhplugAuthOptions);
  generate(): Promise<NhplugTokenResponse>;
  revoke(
    token?: string,
    tokenTypeHint?: 'access_token' | 'refresh_token',
  ): Promise<NhplugTokenRevokeResponse>;
}

export const NHPLUG_SUCCESS_RSP_CODES: readonly string[];

export interface NhplugClientOptions {
  token: string;
  appKey: string;
  secretKey: string;
  env?: ApiEnv;
  debug?: boolean;
  timeoutMs?: number;
  maxRetries?: number;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
  fetchImpl?: typeof fetch;
  logger?: Logger;
}

export declare class NhplugDomainBase {
  constructor(client: NhplugClient, endpoints: readonly NhplugEndpointDefinition[]);
}

${nhplugDomainDecls}

export class NhplugClient {
  constructor(options: NhplugClientOptions);
${nhplugClientProps}
  invokeEndpoint(definition: NhplugEndpointDefinition, input: Record<string, unknown>): Promise<ApiResponse>;
}

export type NhplugMarket = 'kr' | 'gb';

export interface NhplugSocketClientOptions {
  token: string;
  env?: ApiEnv;
  market?: NhplugMarket;
  rateLimitRequestsPerSecond?: number;
  rateLimitBurst?: number;
}

export function getNhplugSocketUrl(env: ApiEnv, market: NhplugMarket): string;

export class NhplugSocketClient extends BaseWebSocketClient {
  constructor(options: NhplugSocketClientOptions);
  readonly env: ApiEnv;
  readonly market: NhplugMarket;
}
`;

/** 생성될 `dist/types/index.d.ts` 본문. 드리프트 테스트가 빌드 없이 검사할 수 있도록 export 한다. */
export const typesContent = content;

// 스크립트로 직접 실행될 때만 파일을 쓴다 (테스트에서 import 해도 dist 를 건드리지 않도록).
if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  fs.mkdirSync(typesDir, { recursive: true });
  fs.writeFileSync(typesPath, content, 'utf8');
  console.log(`Wrote ${path.relative(packageRoot, typesPath)}`);
}
