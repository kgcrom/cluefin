# cluefin-openapi (TypeScript)

> ⚠️ **웹소켓(실시간 시세) 코드 주의사항**
>
> 웹소켓 연결 관련 integration 테스트는 **장중(09:00–15:30 KST)에만** 실제 검증이 가능합니다.
> 메인테이너가 본업으로 인해 장중 테스트가 어려워, 웹소켓 관련 변경사항은 실서버 검증이
> 지연되거나 충분히 이루어지지 않았을 수 있습니다. 웹소켓 기능을 사용하거나 수정할 때는
> 이 점을 감안하고, 가능하면 장중에 직접 동작을 확인해 주세요.

한국투자증권(KIS)·키움증권 OpenAPI TypeScript 클라이언트.

- **KIS**: 국내/해외주식·장내채권 REST API + 실시간 WebSocket 시세, 토큰 파일 캐시
- **키움**: 국내주식 REST API (해외주식·WebSocket은 파이썬 패키지 `cluefin-openapi` 전용)
- 요청/응답 Zod 검증, 응답 키 자동 camelCase 변환, 재시도·rate limit 내장

## 설치

```bash
npm install cluefin-openapi  # Node.js 20+
```

## 환경 변수

```bash
# .env
KIS_APP_KEY=your_app_key
KIS_SECRET_KEY=your_secret_key
KIS_ENV=dev                    # dev(모의투자) | prod(실전)

KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key
KIWOOM_ENV=dev                 # dev(모의투자) | prod(실전)
```

API 키 발급: [KIS](https://apiportal.koreainvestment.com/) / [키움](https://apiportal.kiwoom.com/)

## 빠른 시작

### KIS

```ts
import { KisAuth, KisHttpClient } from 'cluefin-openapi';

const auth = new KisAuth({ appKey, secretKey, env: 'dev' });
const { accessToken } = await auth.generate();

const client = new KisHttpClient({ token: accessToken, appKey, secretKey, env: 'dev' });

const res = await client.domesticBasicQuote.getStockCurrentPrice({
  fidCondMrktDivCode: 'J',
  fidInputIscd: '005930',
});
console.log(res.body); // 응답 키는 camelCase로 변환됨
```

모든 REST 호출은 `{ headers, body }` 형태의 `ApiResponse`를 반환합니다. 와이어 포맷은
snake_case지만 응답 키는 자동으로 camelCase로 변환됩니다.

#### 토큰 캐시

KIS는 토큰 발급을 **분당 1회**로 제한합니다. 기본은 메모리 캐시이며,
`FileTokenCacheStore`를 쓰면 파일에 캐시되어 프로세스를 재시작해도 재사용됩니다.
파일 포맷은 파이썬 패키지(`cluefin_openapi.kis`)와 동일해서 두 언어가 캐시 파일 하나를
공유할 수 있습니다.

```ts
import { KisAuth, FileTokenCacheStore } from 'cluefin-openapi';

const auth = new KisAuth({
  appKey,
  secretKey,
  env: 'dev',
  tokenCacheStore: new FileTokenCacheStore('./data/.kis_token_cache.json'),
});
```

### 키움

```ts
import { KiwoomAuth, KiwoomClient } from 'cluefin-openapi';

const auth = new KiwoomAuth({ appKey, secretKey, env: 'dev' });
const { token } = await auth.generateToken();

const client = new KiwoomClient({ token, env: 'dev' });

const res = await client.domesticStockInfo.getStockInfo({ stkCd: '005930' });
console.log(res.body);
```

### 실시간 시세 (KIS WebSocket)

approval key를 발급받아 소켓에 연결하고, TR별 도우미 클래스로 구독/파싱합니다.

```ts
import { KisAuth, KisSocketClient, DomesticRealtimeQuote } from 'cluefin-openapi';

const auth = new KisAuth({ appKey, secretKey, env: 'dev' });
const { approvalKey } = await auth.approve();

const socket = new KisSocketClient({ approvalKey, appKey, secretKey, env: 'dev' });
const quote = new DomesticRealtimeQuote(socket);

socket.on('connected', async () => {
  await quote.subscribeExecution('005930'); // 실시간 체결가 구독
});

socket.on('data', (event) => {
  if (event.trId === DomesticRealtimeQuote.TR_ID_EXECUTION && event.data) {
    const items = DomesticRealtimeQuote.parseExecutionData(event.data.values);
    console.log(items[0]?.stckPrpr); // 현재가
  }
});

socket.connect();
```

체결(`subscribeExecution`)·호가(`subscribeOrderbook`)·체결통보(`subscribeExecutionNotification`,
prod 전용)를 지원하며, 해외주식·장내채권도 같은 패턴으로 `OverseasRealtimeQuote`,
`OnmarketBondRealtimeQuote`를 사용합니다.

## API 모듈

### KIS REST (`KisHttpClient`의 getter)

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

| 클래스 | 설명 |
|------|------|
| `DomesticRealtimeQuote` | 국내주식 실시간 체결/호가/체결통보 |
| `OverseasRealtimeQuote` | 해외주식 실시간 체결/호가/체결통보 |
| `OnmarketBondRealtimeQuote` | 장내채권 실시간 체결/호가/지수 |

### 키움 REST (`KiwoomClient`의 getter, 국내 전용)

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
import { KisAuthenticationError, KiwoomRateLimitError } from 'cluefin-openapi';

try {
  await client.domesticBasicQuote.getStockCurrentPrice({ ... });
} catch (err) {
  if (err instanceof KisAuthenticationError) {
    // 토큰 만료 → 재발급
  }
}
```

## 개발

```bash
npm install && npm run build
npm run check             # biome lint + format
npm run typecheck
npm run test:unit
npm run test:integration  # 실제 API 키 필요 (repo 루트 .env.test / .env 로드)
```
