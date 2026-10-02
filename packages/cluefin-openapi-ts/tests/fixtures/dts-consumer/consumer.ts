/**
 * 배포될 `dist/types` 선언을 **소비자 관점**으로 컴파일하는 픽스처.
 *
 * 패키지 이름으로 import 하므로 `package.json` 의 `exports["."].types` 를 그대로 탄다.
 * `tests/core/dts-consumer.test.ts` 가 이 파일을 `tsconfig.json`(Bundler)과
 * `tsconfig.nodenext.json`(NodeNext) **두 가지 moduleResolution 으로** 검사한다.
 * 한 가지만 보면 확장자 없는 상대 import 회귀(TS2834 → 전 export TS2305)를 놓친다.
 * 루트 `tsconfig.json` 은 이 디렉터리를 exclude 한다 — 빌드 전에는 해석되지 않는다.
 */
import type {
  CorpCodeResponse,
  DartXbrlFiles,
  DomesticAccountResponseMap,
  KrStockQuoteCurrentPriceResponse,
  NhplugTokenCacheEntry,
  PublicDisclosureSearchResponse,
  StockInfoResponse,
} from 'cluefin-openapi';
import {
  DartApiError,
  DartClient,
  KisAuth,
  KisHttpClient,
  KisSocketClient,
  KiwoomAuth,
  KiwoomClient,
  NHPLUG_SUCCESS_RSP_CODES,
  NhplugAuth,
  NhplugClient,
  NhplugFileTokenCacheStore,
  NhplugSocketClient,
} from 'cluefin-openapi';

// 이 세 타입은 수기 템플릿 시절 선언 자체가 없었다 — 이관의 실질적 이득.
declare const info: StockInfoResponse;
declare const quote: KrStockQuoteCurrentPriceResponse;
declare const executed: DomesticAccountResponseMap['getExecuted'];

// 이름 존재만이 아니라 필드 타입까지 추론되는지 확인한다.
export const stockCode: string = info.stkCd;
export const stockName: string = info.stkNm;
export const iemCd: string | null | undefined = quote.output0?.iemCd;
export const executedRows = executed.oso;

// 값 export 도 "이름이 있다" 로 끝내지 않고 실제로 멤버를 읽는다.
declare const kiwoom: KiwoomClient;
export const kiwoomChart = kiwoom.domesticChart;
export const kiwoomStockInfo = kiwoom.domesticStockInfo;

declare const kisSocket: KisSocketClient;
export const kisSocketEnv: 'prod' | 'dev' = kisSocket.env;

declare const nhplugCache: NhplugFileTokenCacheStore;
export const cachedToken: Promise<NhplugTokenCacheEntry | null> = nhplugCache.get();
export const cachedAccessToken = async (): Promise<string | undefined> => (await nhplugCache.get())?.accessToken;

// OpenDART: 도메인 getter·생성된 응답 타입·직접 정의한 반환 타입(고유번호/XBRL)이 소비자에게 보이는지.
declare const dart: DartClient;
export const dartSearch = dart.publicDisclosure.publicDisclosureSearch({ corpCode: '00126380' });
export const dartDividend = dart.periodicReportKeyInformation.getDividendInformation;
export const dartMajorReport = dart.majorShareholderDisclosure.corporateLawDecision;
declare const search: PublicDisclosureSearchResponse;
export const searchTotal: number | string | null | undefined = search.totalCount;
export const firstReportName: string | undefined = search.list?.[0]?.reportNm;
declare const corpCodes: CorpCodeResponse;
export const firstStockCode: string | undefined = corpCodes.list[0]?.stockCode;
declare const xbrl: DartXbrlFiles;
export const xbrlFileNames: string[] = [...xbrl.keys()];
export const dartErrorIsApiError: boolean = new DartApiError('x') instanceof Error;

export const successCodes: readonly string[] = NHPLUG_SUCCESS_RSP_CODES;
export const successCodeCount: number = NHPLUG_SUCCESS_RSP_CODES.length;

export const runtimeClasses = [
  DartClient,
  KisAuth,
  KisHttpClient,
  KisSocketClient,
  KiwoomAuth,
  KiwoomClient,
  NhplugAuth,
  NhplugClient,
  NhplugFileTokenCacheStore,
  NhplugSocketClient,
];
