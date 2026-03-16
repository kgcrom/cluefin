# cluefin-openapi (TypeScript)

KIS/키움 OpenAPI TypeScript 클라이언트. REST API, 실시간 WebSocket 시세, 토큰 캐시 지원.

## 설치

```bash
npm install cluefin-openapi  # Node.js 20+
```

## 환경 변수

```bash
# .env
KIS_APP_KEY=your_app_key
KIS_SECRET_KEY=your_secret_key
KIS_ENV=dev                    # dev | prod

KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key
KIWOOM_ENV=dev                 # dev | prod
```

API 키 발급: [KIS](https://apiportal.koreainvestment.com/) / [키움](https://apiportal.kiwoom.com/)

## 빠른 시작

### KIS

```ts
import { KisAuth, KisHttpClient } from 'cluefin-openapi';

const auth = new KisAuth({ appKey, secretKey, env: 'dev' });
const { accessToken } = await auth.generateToken();
const client = new KisHttpClient({ token: accessToken, appKey, secretKey, env: 'dev' });

const res = await client.domesticBasicQuote.getStockCurrentPrice({
  fidCondMrktDivCode: 'J',
  fidInputIscd: '005930',
});
```

### 키움

```ts
import { KiwoomAuth, KiwoomClient } from 'cluefin-openapi';

const auth = new KiwoomAuth({ appKey, secretKey, env: 'dev' });
const { token } = await auth.generateToken();
const client = new KiwoomClient({ token, env: 'dev' });

const res = await client.domesticStockInfo.getStockInfo({ stkCd: '005930' });
```

### 실시간 시세 (WebSocket)

```ts
import { KisAuth, KisSocketClient, DomesticRealtimeQuote } from 'cluefin-openapi';

const approval = await auth.getApprovalKey();
const socket = new KisSocketClient({ approvalKey: approval.approvalKey, env: 'dev' });
const quote = new DomesticRealtimeQuote();

socket.on('data', (trId, raw) => console.log(quote.parse(trId, raw)));
await socket.connect();
await socket.subscribe('H0STCNT0', '005930');
```

## API 모듈

### KIS REST

| 모듈 | 설명 |
|------|------|
| `domesticBasicQuote` | 국내주식 기초시세 |
| `domesticStockInfo` | 국내주식 종목정보 |
| `domesticMarketAnalysis` | 국내주식 시장분석 |
| `domesticRankingAnalysis` | 국내주식 순위분석 |
| `domesticIssueOther` | 국내주식 기타이슈 |
| `domesticAccount` | 국내주식 계좌 |
| `overseasBasicQuote` | 해외주식 기초시세 |
| `overseasMarketAnalysis` | 해외주식 시장분석 |
| `overseasAccount` | 해외주식 계좌 |
| `onmarketBondBasicQuote` | 장내채권 기초시세 |

### KIS 실시간 (WebSocket)

| 모듈 | 설명 |
|------|------|
| `DomesticRealtimeQuote` | 국내주식 실시간 체결/호가 |
| `OverseasRealtimeQuote` | 해외주식 실시간 체결/호가 |
| `OnmarketBondRealtimeQuote` | 장내채권 실시간 체결/호가 |

### 키움 REST

| 모듈 | 설명 |
|------|------|
| `domesticStockInfo` | 국내주식 종목정보 |
| `domesticAccount` | 국내주식 계좌 |
| `domesticChart` | 국내주식 차트 |
| `domesticOrder` | 국내주식 주문 |
| `domesticEtf` | 국내 ETF |
| `domesticForeign` | 국내주식 외국인거래 |
| `domesticMarketCondition` | 국내주식 시장상황 |
| `domesticRankInfo` | 국내주식 순위정보 |
| `domesticSector` | 국내주식 섹터 |
| `domesticTheme` | 국내주식 테마 |

## 에러 처리

KIS/키움 각각 전용 에러 클래스 제공 (`ApiError` 상속):

`Authentication` · `Authorization` · `Validation` · `Server` · `Network` · `Timeout` · `RateLimit`

```ts
import { KisAuthenticationError, KisRateLimitError } from 'cluefin-openapi';
```

## 개발

```bash
npm install && npm run build
npm run check        # biome lint
npm run typecheck
npm run test:unit
npm run test:integration  # API 키 필요
```
