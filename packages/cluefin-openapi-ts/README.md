# cluefin-openapi (TypeScript)

KIS/키움 OpenAPI를 위한 타입 안전 TypeScript 클라이언트. REST API 호출, 실시간 WebSocket 시세, 토큰 캐시를 지원합니다.

## 설치

```bash
npm install cluefin-openapi
```

Node.js 20 이상 필요.

## 환경 변수

```bash
# KIS (한국투자증권)
KIS_APP_KEY=your_app_key
KIS_SECRET_KEY=your_secret_key
KIS_ENV=dev  # dev | prod

# 키움증권
KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key
KIWOOM_ENV=dev  # dev | prod
```

API 키 발급: [KIS](https://apiportal.koreainvestment.com/) / [키움](https://apiportal.kiwoom.com/)

## 사용법

### KIS 인증 + API 호출

```ts
import { KisAuth, KisHttpClient } from 'cluefin-openapi';

const auth = new KisAuth({
  appKey: process.env.KIS_APP_KEY!,
  secretKey: process.env.KIS_SECRET_KEY!,
  env: 'dev',
});

const token = await auth.generateToken();

const client = new KisHttpClient({
  token: token.accessToken,
  appKey: process.env.KIS_APP_KEY!,
  secretKey: process.env.KIS_SECRET_KEY!,
  env: 'dev',
});

// 삼성전자 현재가 조회
const response = await client.domesticBasicQuote.getStockCurrentPrice({
  fidCondMrktDivCode: 'J',
  fidInputIscd: '005930',
});
console.log(response.body);
```

`KisAuth`는 `FileTokenCacheStore` / `MemoryTokenCacheStore`로 토큰 캐싱을 지원합니다.

### 실시간 시세 (WebSocket)

```ts
import { KisAuth, KisSocketClient, DomesticRealtimeQuote } from 'cluefin-openapi';

const auth = new KisAuth({ appKey, secretKey, env: 'dev' });
const approval = await auth.getApprovalKey();

const socket = new KisSocketClient({ approvalKey: approval.approvalKey, env: 'dev' });
const realtimeQuote = new DomesticRealtimeQuote();

socket.on('data', (trId, rawData) => {
  const items = realtimeQuote.parse(trId, rawData);
  console.log(items);
});

await socket.connect();
await socket.subscribe('H0STCNT0', '005930'); // 삼성전자 체결가
```

### 키움 인증 + API 호출

```ts
import { KiwoomAuth, KiwoomClient } from 'cluefin-openapi';

const auth = new KiwoomAuth({
  appKey: process.env.KIWOOM_APP_KEY!,
  secretKey: process.env.KIWOOM_SECRET_KEY!,
  env: 'dev',
});

const token = await auth.generateToken();

const client = new KiwoomClient({
  token: token.token,
  env: 'dev',
});

const response = await client.domesticStockInfo.getStockInfo({ stkCd: '005930' });
console.log(response.body);
```

## KIS API 모듈

### REST

| 모듈 | 설명 |
|------|------|
| `domesticBasicQuote` | 국내주식 기초시세 (현재가, 체결, 호가 등) |
| `domesticStockInfo` | 국내주식 종목정보 |
| `domesticMarketAnalysis` | 국내주식 시장분석 |
| `domesticRankingAnalysis` | 국내주식 순위분석 |
| `domesticIssueOther` | 국내주식 기타이슈 |
| `domesticAccount` | 국내주식 계좌 |
| `overseasBasicQuote` | 해외주식 기초시세 |
| `overseasMarketAnalysis` | 해외주식 시장분석 |
| `overseasAccount` | 해외주식 계좌 |
| `onmarketBondBasicQuote` | 장내채권 기초시세 |

### 실시간 (WebSocket)

| 모듈 | 설명 |
|------|------|
| `DomesticRealtimeQuote` | 국내주식 실시간 체결/호가 |
| `OverseasRealtimeQuote` | 해외주식 실시간 체결/호가 |
| `OnmarketBondRealtimeQuote` | 장내채권 실시간 체결/호가 |

## 키움 API 모듈

| 모듈 | 설명 |
|------|------|
| `domesticStockInfo` | 국내주식 종목정보 |
| `domesticAccount` | 국내주식 계좌 |
| `domesticChart` | 국내주식 차트 |
| `domesticOrder` | 국내주식 주문 |
| `domesticETF` | 국내 ETF |
| `domesticForeign` | 국내주식 외국인거래 |
| `domesticMarketCondition` | 국내주식 시장상황 |
| `domesticRankInfo` | 국내주식 순위정보 |
| `domesticSector` | 국내주식 섹터 |
| `domesticTheme` | 국내주식 테마 |

## 에러 처리

KIS와 키움 각각 전용 에러 클래스를 제공합니다. 공통 베이스(`ApiError`)를 상속합니다.

```ts
import {
  KisAuthenticationError,
  KisRateLimitError,
  KiwoomAuthenticationError,
} from 'cluefin-openapi';

try {
  const response = await client.domesticBasicQuote.getStockCurrentPrice({ ... });
} catch (error) {
  if (error instanceof KisAuthenticationError) {
    // 인증 실패 — 토큰 재발급 필요
  } else if (error instanceof KisRateLimitError) {
    // 요청 제한 초과 — error.retryAfter 확인
  }
}
```

에러 타입: `Authentication`, `Authorization`, `Validation`, `Server`, `Network`, `Timeout`, `RateLimit`

## 개발

```bash
cd packages/cluefin-openapi-ts

npm install
npm run build
npm run check          # ruff lint
npm run typecheck      # tsc --noEmit
npm run test:unit
npm run test:integration
```
