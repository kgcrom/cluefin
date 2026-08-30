# cluefin-openapi (TypeScript)

> ⚠️ **웹소켓(실시간 시세) 코드 주의사항**
>
> 웹소켓 연결 관련 integration 테스트는 **장중(09:00–15:30 KST)에만** 실제 검증이 가능합니다.
> 메인테이너가 본업으로 인해 장중 테스트가 어려워, 웹소켓 관련 변경사항은 실서버 검증이
> 지연되거나 충분히 이루어지지 않았을 수 있습니다. 웹소켓 기능을 사용하거나 수정할 때는
> 이 점을 감안하고, 가능하면 장중에 직접 동작을 확인해 주세요.

한국투자증권(KIS)·키움증권·NH투자증권(PLUG) OpenAPI TypeScript 클라이언트.

- **KIS**: 국내/해외주식·장내채권 REST API + 실시간 WebSocket 시세, 토큰 파일 캐시
- **키움**: 국내주식 REST API (해외주식·WebSocket은 파이썬 패키지 `cluefin-openapi` 전용)
- **NH PLUG**: 공통 2 + 국내주식 31 + 해외주식 18 = REST 51개 엔드포인트 + 실시간 WebSocket 시세
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

NHPLUG_APP_KEY=your_app_key
NHPLUG_SECRET_KEY=your_secret_key
NHPLUG_ENV=dev                 # dev(모의투자, moapi) | prod(운영, 실주문)
```

API 키 발급: [KIS](https://apiportal.koreainvestment.com/) / [키움](https://apiportal.kiwoom.com/) /
[NH PLUG](https://www.nhplug.com/)

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

### NH투자증권 (PLUG)

```ts
import { NhplugAuth, NhplugClient } from 'cluefin-openapi';

// 토큰 발급(`/oauth2/token`)은 **운영 도메인 전용**이고, 발급된 토큰 하나로 운영·모의투자를
// 모두 호출한다. 그래서 `NhplugAuth`는 `env`를 받지 않는다.
const auth = new NhplugAuth({ appKey, secretKey });
const { accessToken } = await auth.generate();

// env: 'dev'(기본값) = 모의투자(moapi.nhplug.com), 'prod' = 운영(api.nhplug.com, 실제 주문 체결)
const client = new NhplugClient({ token: accessToken, appKey, secretKey, env: 'dev' });

// 1) 계좌 목록을 먼저 조회한다. 이후 조회/주문 API는 모두 `actNo`를 요구한다.
const accounts = await client.common.getAccountList({});
const actNo = accounts.body.output0?.[0]?.acctNo;

// 2) 국내주식 현재가 (marketCd: KRX | NXT | UNT(통합시세))
const price = await client.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: '005930' });

// 3) 국내주식 잔고
const balance = await client.krstockInquiry.balance({
  actNo,
  bncBseCd: '1', // 주식관련 총 평가(체결기준)
  ltgAotDitCd: '9', // 전체
  aetBse: '1', // 순자산
  qutDitCd: 'UNT', // 통합시세
});
```

입력 파라미터는 camelCase(`iemCd`)로 넘기면 와이어 포맷(`iem_cd`)으로 변환되고, 요청 본문은
`Input_0` 봉투로 감싸집니다. 응답은 `Output_0` → `output0`처럼 camelCase로 변환됩니다.
연속조회는 이전 응답 헤더의 `cts` 값을 다음 요청 입력의 `cts`로 그대로 넘기면 됩니다.

#### 꼭 알아둘 것

- **`env`를 틀리면 실계좌에 주문이 나갑니다.** `'prod'`는 운영(실제 체결), `'dev'`는
  모의투자입니다. 기본값은 `'dev'`.
- **계좌 목록(`common.getAccountList`)을 먼저 호출하세요.** 조회·주문 API는 모두 `actNo`가
  필요하고, 계좌구분(`acctType`)이 환경과 맞아야 합니다 —
  `01`(자계좌)·`02`(주문대리인계좌)는 **운영 전용**, `03`(모의투자계좌)은 **모의투자 전용**입니다.
- **해외주식 시세 4종(`overseasStockQuote.*`)은 운영 도메인 전용**입니다. 모의투자에서 호출하면
  종목코드와 무관하게 `IGW40019 "종목코드(iem_cd)를 확인해주세요"`로 거절되는데, 이는 잘못된
  종목코드가 아니라 "모의투자 미제공"이라는 뜻입니다.
- HTTP 200이어도 본문 `rsp_cd`가 실패일 수 있어 클라이언트가 이를 검사합니다. 성공 코드는
  `00000`과 `XA102`(모의투자 조회 완료) 두 가지입니다 (`NHPLUG_SUCCESS_RSP_CODES`).

#### 토큰 캐시

토큰 발급은 서버에서 초당 1회로 제한되고, 불필요한 재발급은 계좌 보안 알림을 유발합니다.
기본은 메모리 캐시이며 `NhplugFileTokenCacheStore`를 쓰면 프로세스를 재시작해도 재사용됩니다.
파일 포맷은 파이썬 패키지(`cluefin_openapi.nhplug`)와 동일합니다. 캐시 파일 이름은 env가 아니라
app key로만 구분됩니다 — 토큰 하나를 운영·모의투자가 공유하기 때문입니다.

```ts
import { NhplugAuth, NhplugFileTokenCacheStore, nhplugTokenCacheFileName } from 'cluefin-openapi';

const auth = new NhplugAuth({
  appKey,
  secretKey,
  tokenCacheStore: new NhplugFileTokenCacheStore(`./data/${nhplugTokenCacheFileName(appKey)}`),
});
```

### 실시간 시세 (NH PLUG WebSocket)

REST와 같은 access token을 그대로 씁니다(approval key 없음). 구독 대상은 REST 경로가 아니라
웹소켓 전용 채널 코드(`tr_cd`)이며, 서버 푸시는 평문 JSON이라 `event.body`로 바로 읽습니다.

```ts
import { NhplugAuth, NhplugSocketClient } from 'cluefin-openapi';

const auth = new NhplugAuth({ appKey, secretKey });
const { accessToken } = await auth.generate();

// market: 'kr'(국내, 기본) | 'gb'(해외) — 운영에서만 주소가 갈리고 모의투자는 단일 주소입니다.
const socket = new NhplugSocketClient({ token: accessToken, env: 'dev', market: 'kr' });

socket.on('connected', async () => {
  await socket.subscribe('mc', '005930'); // 국내 통합시세 체결가
});

socket.on('data', (event) => {
  console.log(event.trId, event.body); // { header: { tr_cd, tr_key }, body: {...} } 의 body
});

socket.connect();
```

채널 코드는 대소문자로 갈립니다(해외 실시간 `RC` / 지연 `rc`). 세션을 정리할 때는
`client.common.closeWebsocketSession({})`를 호출하세요.

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

### NH PLUG REST (`NhplugClient`의 getter)

| 모듈 | 설명 | 엔드포인트 |
|------|------|------|
| `common` | 공통 (계좌목록·웹소켓 세션해제) | 2 |
| `krstockOrder` | 국내주식 주문 | 8 |
| `krstockInquiry` | 국내주식 조회 | 12 |
| `krstockQuote` | 국내주식 시세 | 11 |
| `overseasStockOrder` | 해외주식(gbstock) 주문 | 6 |
| `overseasStockInquiry` | 해외주식(gbstock) 조회 | 8 |
| `overseasStockQuote` | 해외주식(gbstock) 시세 (**운영 전용**) | 4 |

## 에러 처리

KIS/키움/NH PLUG 각각 전용 에러 클래스 제공 (`ApiError` 상속):

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
