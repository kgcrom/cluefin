import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);
const packageRoot = path.resolve(scriptDir, '..');
const typesDir = path.join(packageRoot, 'dist', 'types');
const typesPath = path.join(typesDir, 'index.d.ts');

fs.mkdirSync(typesDir, { recursive: true });

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
  { className: 'DomesticStockInfo', metadataPath: 'src/kis/metadata/domestic-stock-info.ts', prop: 'domesticStockInfo' },
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

const kisDomainDecls = kisDomains
  .map((d) => renderDomainClass(d.className, extractMethodNames(d.metadataPath)))
  .join('\n\n');

const kiwoomDomainDecls = kiwoomDomains
  .map((d) => renderDomainClass(d.className, extractMethodNames(d.metadataPath)))
  .join('\n\n');

const kisClientProps = kisDomains.map((d) => `  readonly ${d.prop}: ${d.className};`).join('\n');
const kiwoomClientProps = kiwoomDomains.map((d) => `  readonly ${d.prop}: ${d.className};`).join('\n');

const content = `export type ApiEnv = 'dev' | 'prod';

export interface ApiResponse<TBody = Record<string, unknown>> {
  headers: Record<string, string>;
  body: TBody;
}

export interface RateLimitOptions {
  requestsPerSecond: number;
  burst: number;
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
`;

fs.writeFileSync(typesPath, content, 'utf8');
console.log(`Wrote ${path.relative(packageRoot, typesPath)}`);
