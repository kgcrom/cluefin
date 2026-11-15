# cluefin-openapi (TypeScript)

한국투자증권(KIS)·키움증권·NH투자증권(PLUG) 주문·시세 API와 금융감독원 OpenDART(공시·재무제표), 한국은행 ECOS(경제통계)를 한 패키지로.

- **KIS**: 국내/해외주식·장내채권 REST + 실시간 WebSocket
- **키움**: 국내주식 REST (해외주식·WebSocket은 파이썬 패키지 `cluefin-openapi` 전용)
- **NH PLUG**: 공통·국내주식·해외주식 REST + 실시간 WebSocket
- **OpenDART**: 공시검색·기업개황·재무제표·주요사항보고서 — 토큰 없이 키 하나로 조회
- **ECOS**: 한국은행 경제통계 — 키 없이 공개 시험 키 `sample`로 바로
- 요청/응답 Zod 검증, 응답 키 camelCase 변환, 재시도·rate limit 내장

> 실시간(WebSocket) 통합 테스트는 장중(국내 주식 09:00–15:20 KST)에만 데이터를 받아 검증합니다.
> 웹소켓 쪽 변경은 실서버 확인이 늦을 수 있으니, 쓰기 전에 장중에 한 번 직접 받아 보세요.

## 설치

```bash
npm install cluefin-openapi  # Node.js 20+
```

API 키 발급: [KIS](https://apiportal.koreainvestment.com/) / [키움](https://openapi.kiwoom.com/) /
[NH PLUG](https://www.nhplug.com/) / [OpenDART](https://opendart.fss.or.kr/) / [ECOS](https://ecos.bok.or.kr/api/)

## 먼저 알아둘 것

- **라이브러리는 환경변수나 `.env`를 읽지 않습니다.** 키와 `env`는 생성자에 직접 넘깁니다. 아래 예제의
  `process.env.*` 이름은 예시일 뿐입니다.
- `env`는 `'dev'`(모의투자) 또는 `'prod'`(실전, **실제 주문 체결**)입니다. 생략했을 때 기본값이 클래스마다 다릅니다 —
  `KisHttpClient`만 `'prod'`이고 나머지(`KisAuth`·`KisSocketClient`·키움·NH PLUG)는 `'dev'`입니다. 항상 명시하세요.
- KIS·키움·NH PLUG·DART의 REST 호출은 `{ headers, body }`를 돌려줍니다. 와이어 포맷은 snake_case이고 입력·응답 키는
  camelCase입니다.
- 예제는 ESM(top-level `await`) 기준입니다. CJS(`require`)도 지원합니다.

## KIS

```ts
import { KisAuth, KisHttpClient } from 'cluefin-openapi';

const appKey = process.env.KIS_APP_KEY ?? '';
const secretKey = process.env.KIS_SECRET_KEY ?? '';

const auth = new KisAuth({ appKey, secretKey, env: 'dev' });
const { accessToken } = await auth.generate();

const client = new KisHttpClient({ token: accessToken, appKey, secretKey, env: 'dev' });
const res = await client.domesticBasicQuote.getStockCurrentPrice({
  fidCondMrktDivCode: 'J',
  fidInputIscd: '005930',
});
console.log(res.body);
```

- 모의·실전 토큰은 서로 통하지 않습니다. `KisAuth`와 `KisHttpClient`의 `env`가 다르면 서버가 `EGW00123`
  ("기간이 만료된 token")으로 거절합니다.
- 토큰 발급은 **분당 1회**로 제한됩니다. 기본 캐시는 메모리라 프로세스를 다시 띄우면 재발급합니다.
  `FileTokenCacheStore`로 파일에 두세요. 파일 이름은 `kisTokenCacheFileName(env, appKey)`로 만듭니다 — env가 빠진
  이름 하나를 쓰면 모의·실전 토큰이 같은 파일에 섞입니다.
- 아래 경로·이름은 파이썬 패키지(`cluefin_openapi.kis`)의 기본값과 같아서, 두 언어가 토큰 하나를 같이 씁니다.
  캐시는 만료 전이라도 6시간이 지나면 버리고 새로 받습니다.

```ts
import os from 'node:os';
import path from 'node:path';
import { FileTokenCacheStore, KisAuth, kisTokenCacheFileName } from 'cluefin-openapi';

const cacheFile = path.join(os.tmpdir(), 'cluefin-openapi', kisTokenCacheFileName('dev', appKey));
const auth = new KisAuth({ appKey, secretKey, env: 'dev', tokenCacheStore: new FileTokenCacheStore(cacheFile) });
```

### 실시간 시세

approval key를 따로 발급받아 연결하고, TR별 도우미 클래스로 구독·파싱합니다.

```ts
import { DomesticRealtimeQuote, KisAuth, KisSocketClient } from 'cluefin-openapi';

// 국내 통합 체결가는 모의투자에 없는 TR 이라 prod 로 붙는다(시세 구독은 주문을 내지 않는다).
const { approvalKey } = await new KisAuth({ appKey, secretKey, env: 'prod' }).approve();
const socket = new KisSocketClient({ approvalKey, appKey, secretKey, env: 'prod' });
const quote = new DomesticRealtimeQuote(socket);

socket.on('connected', () => void quote.subscribeExecution('005930'));
socket.on('data', (event) => {
  if (event.trId === DomesticRealtimeQuote.TR_ID_EXECUTION && event.data) {
    console.log(DomesticRealtimeQuote.parseExecutionData(event.data.values)[0]?.stckPrpr); // 현재가
  }
});
socket.on('error', (event) => console.error(event.error?.message));
socket.connect();
```

- **구독 응답을 믿지 마세요.** KIS는 없는 종목코드와 모의투자에 없는 TR에도 `SUBSCRIBE SUCCESS`를 답하고 데이터만
  보내지 않습니다. 데이터가 오는지로 판단하세요.
- **app key 하나에 WebSocket 세션은 하나**이고, `approve()`를 다시 부르면 앞서 받은 approval key가 무효가 됩니다.
  다른 세션이 열려 있으면 `OPSP8996 ALREADY IN USE appkey`, 더 새 key가 있으면 `OPSP0011 invalid approval`이
  `error` 이벤트로 오고 연결이 끊깁니다. 같은 키를 쓰는 다른 프로그램(파이썬 스크립트 포함)이 있는지 먼저 보세요.
- 체결통보(`subscribeExecutionNotification`)는 prod 전용입니다. 해외주식·장내채권은 같은 방식으로
  `OverseasRealtimeQuote`·`OnmarketBondRealtimeQuote`를 씁니다.

## 키움

```ts
import { KiwoomAuth, KiwoomClient } from 'cluefin-openapi';

const auth = new KiwoomAuth({
  appKey: process.env.KIWOOM_APP_KEY ?? '',
  secretKey: process.env.KIWOOM_SECRET_KEY ?? '',
  env: 'dev',
});
const { token } = await auth.generateToken();

const client = new KiwoomClient({ token, env: 'dev' });
const res = await client.domesticStockInfo.getStockInfo({ stkCd: '005930' });
console.log(res.body);
```

- 메서드 이름이 KIS·NH PLUG(`generate`/`revoke`)와 달리 `generateToken`/`revokeToken`입니다.
- `revokeToken(token)`은 캐시를 비우지 않습니다. 폐기한 뒤에도 `generateToken()`은 캐시에 남은 그 토큰을 돌려주니,
  `KiwoomFileTokenCacheStore`를 쓴다면 `clear()`를 직접 부르세요. 파일 이름은 `kiwoomTokenCacheFileName(env, appKey)`.

## NH투자증권 (PLUG)

```ts
import { NhplugAuth, NhplugClient } from 'cluefin-openapi';

const appKey = process.env.NHPLUG_APP_KEY ?? '';
const secretKey = process.env.NHPLUG_SECRET_KEY ?? '';

// 토큰 발급은 운영 도메인 전용이고 토큰 하나로 운영·모의투자를 모두 호출한다 — NhplugAuth 는 env 를 받지 않는다.
const auth = new NhplugAuth({ appKey, secretKey });
const { accessToken } = await auth.generate();

// 조회·주문은 모의투자(dev, moapi.nhplug.com)로 먼저 확인한다.
const mock = new NhplugClient({ token: accessToken, appKey, secretKey, env: 'dev' });

// 1) 계좌 목록 — 이후 조회·주문 API 는 모두 actNo 를 요구한다. 모의투자에서 유효한 계좌는 acctType '03' 뿐이다.
const accounts = await mock.common.getAccountList({});
const actNo = accounts.body.output0?.find((account) => account.acctType === '03')?.acctNo;

// 2) 국내주식 잔고
const balance = await mock.krstockInquiry.balance({
  actNo,
  bncBseCd: '1', // 주식관련 총 평가(체결기준)
  ltgAotDitCd: '9', // 전체
  aetBse: '1', // 순자산
  qutDitCd: 'UNT', // 통합시세
});

// 3) 시세는 운영 전용이다 — 같은 토큰으로 prod 클라이언트를 하나 더 만든다(시세 조회는 주문을 내지 않는다).
const live = new NhplugClient({ token: accessToken, appKey, secretKey, env: 'prod' });
const price = await live.krstockQuote.currentPrice({ marketCd: 'KRX', iemCd: '005930' }); // KRX | NXT | UNT(통합)
```

- **`env: 'prod'` 클라이언트로 주문 메서드를 부르면 실계좌에서 체결됩니다.** 위 예제의 `live`는 시세에만 쓰세요.
- **시세 API는 전부 운영 전용**입니다. 모의투자는 국내 시세(`krstockQuote.*`)를 `IGW40023`으로, 해외 시세
  (`overseasStockQuote.*`)를 `IGW40019 "종목코드(iem_cd)를 확인해주세요"`로 거절합니다. 뒤쪽 메시지는 종목코드가
  틀렸다는 뜻이 아니라 "모의투자 미제공"입니다.
- **계좌구분(`acctType`)이 환경과 맞아야 합니다** — `01`(자계좌)·`02`(주문대리인계좌)는 운영 전용, `03`(모의투자계좌)은
  모의투자 전용입니다.
- 요청은 `Input_0` 봉투로 감싸 보내고 응답은 `Output_0` → `output0`으로 옵니다. 숫자 필드는 **숫자로** 넘기세요
  (`reqCnt: 10`). 문자열 `'10'`은 서버가 `IGW40011`로 거절합니다. 연속조회는 이전 응답 헤더의 `cts`를 다음 입력의
  `cts`로 넘깁니다.
- **HTTP 200이어도 본문 `rsp_cd`가 실패일 수 있어** 클라이언트가 검사합니다. 성공은 `00000`·`XA102`(모의 조회)·
  `00166`(운영 조회)·`00221`(운영 주문가능수량)입니다. **조회 결과 0건은 실패 코드로 옵니다** — `NhplugNoDataError`
  (`13578`·`11512`·`16935`)를 빈 결과로 처리하세요. `NhplugMockUnsupportedError`(`19999`)는 모의투자 미제공,
  `NhplugNotBusinessDayError`(`14100`)는 영업일 아님입니다. 셋 다 `NhplugApiError`의 하위이고 코드는 `error.errorCode`에
  있습니다.
- **토큰을 불필요하게 다시 발급하면 계좌 보안 알림이 옵니다**(발급은 초당 1회 제한). 기본 캐시는 메모리이니,
  프로세스를 자주 띄운다면 KIS 예제처럼 파일 캐시를 쓰세요 —
  `new NhplugFileTokenCacheStore(path.join(os.tmpdir(), 'cluefin-openapi', nhplugTokenCacheFileName(appKey)))`.
  토큰 하나를 운영·모의가 같이 쓰므로 파일 이름은 env 없이 app key로만 갈립니다. 파이썬 패키지와 같은 파일입니다.

### 실시간 시세

REST와 같은 access token을 그대로 씁니다(approval key 없음). 구독 대상은 REST 경로가 아니라 웹소켓 전용 채널 코드
(`tr_cd`)이고, 서버 푸시는 평문 JSON이라 `event.body`로 읽습니다.

```ts
import { NhplugSocketClient } from 'cluefin-openapi';

// accessToken 은 위 예제에서 받은 것. 시세 채널은 운영 전용이다.
// market: 'kr'(국내, 기본) | 'gb'(해외) — 운영에서만 주소가 갈린다.
const socket = new NhplugSocketClient({ token: accessToken, env: 'prod', market: 'kr' });

socket.on('connected', () => void socket.subscribe('mc', '005930')); // 국내 통합시세 체결가
socket.on('data', (event) => console.log(event.trId, event.trKey, event.body));
socket.connect();
```

- 모의 소켓은 시세 채널 구독을 `WSS10006 "허용되지 않는 tr_cd 입니다."`로 거절합니다.
- **채널 코드는 대소문자로 갈립니다** — 해외 `RC`/`RH`는 실시간(유료 시세 약정 필요), `rc`/`rh`는 무료 지연 시세입니다.
  전체 목록은 자산군별 `https://www.nhplug.com/openapi-docs/<krstock|gbstock>/openapi.json`의 `x-realtime-channels`.
- 운영 서버는 없는 종목코드에도 `rsp_cd 00000`을 답하고, 그 구독 응답도 `data` 이벤트로 옵니다(`trKey` 없음).
  `event.trKey`가 맞는 푸시를 받았는지로 판단하세요.
- 세션이 남아 끊기지 않으면 `client.common.closeWebsocketSession({})`으로 정리합니다. 열린 세션이 없을 때 부르면
  서버가 실패로 답해 `NhplugApiError`가 납니다.

## OpenDART (공시·재무제표)

계좌도 토큰도 필요 없습니다. 인증키 하나로 상장사 전체의 공시와 재무제표를 조회합니다 — 조회 전용이라 주문이 나갈 일이 없습니다.

```ts
import { DartClient } from 'cluefin-openapi';

const dart = new DartClient({ authKey: process.env.DART_AUTH_KEY ?? '' });

// 1) DART 는 종목코드가 아니라 고유번호(corpCode, 8자리)로 조회한다. 먼저 변환한다.
//    회사 전체 목록을 ZIP 으로 내려받으니 한 번만 받아 캐시해 둔다.
const { body: corps } = await dart.publicDisclosure.corpCode();
const { corpCode } = corps.list.find((c) => c.stockCode === '005930')!; // '00126380'

// 2) 최근 정기공시
const { body: found } = await dart.publicDisclosure.publicDisclosureSearch({
  corpCode,
  pblntfTy: 'A', // A 정기공시 · B 주요사항보고 · D 지분공시 …
  bgnDe: '20240101',
  pageCount: 3,
});
for (const d of found.list ?? []) console.log(d.rceptDt, d.reportNm, d.rceptNo);
// 20260310 사업보고서 (2025.12) 20260310002820

// 3) 매출액 — reprtCode: 11011 사업보고서 · 11012 반기 · 11013 1분기 · 11014 3분기
const { body: acc } = await dart.periodicReportFinancialStatement.getSingleCompanyMajorAccounts({
  corpCode,
  bsnsYear: '2024',
  reprtCode: '11011',
});
const sales = acc.list?.find((a) => a.accountNm === '매출액' && a.fsDiv === 'CFS'); // CFS 연결 · OFS 별도
console.log(sales?.thstrmAmount, sales?.frmtrmAmount); // 당기 · 전기 → '300,870,903,000,000' '258,935,494,000,000'

// 4) 공시 원문 ZIP 의 XML 전부 — 본문이 첫 번째, 첨부 감사보고서(_00760·_00761)가 뒤에 온다. 디스크에 쓰지 않는다.
const files = await dart.publicDisclosure.disclosureDocumentFiles({ rceptNo: '20260310002820' });
console.log([...files.body.keys()]); // ['20260310002820.xml', '20260310002820_00760.xml', …]
```

어디에 무엇이 있나:

- `publicDisclosure` 공시검색·기업개황·원문·고유번호, `periodicReportFinancialStatement` 재무제표·주요지표·XBRL
- `periodicReportKeyInformation` 배당·최대주주·임원보수·감사의견 같은 정기보고서 항목, `shareDisclosureComprehensive` 대량보유·임원 소유보고
- `majorMattersReport` 증자·자사주·합병 같은 사건성 공시(주요사항보고서). 옛 이름 `majorShareholderDisclosure`는 deprecated 별칭

### 꼭 알아둘 것

- **조회 결과가 없어도, 키가 틀려도 예외가 아닙니다.** HTTP 200 본문의 `status`로 판단하세요 — `'000'` 정상,
  `'013'` 데이터 없음(`list` 없음), `'020'` 요청 제한 초과, `'010'` 등록되지 않은 키. 전체 코드는 OpenDART 개발가이드의
  "에러 및 메시지 설명"에 있습니다. 본문 `status`를 예외(`DartApiError`)로 바꾸는 것은 원문·XBRL 같은 바이너리 조회뿐입니다.
- `publicDisclosureSearch`는 기간(`bgnDe`·`endDe`)을 생략하면 **최근 89일**을 조회합니다. `corpCode` 없이는 3개월을
  넘길 수 없습니다.
- 금액·수량은 **쉼표 섞인 문자열**(`'300,870,903,000,000'`)입니다. 계산 전에 변환하세요.
- 키별 요청 제한(일반적으로 2만 건)을 넘으면 `status: '020'`입니다. 클라이언트 기본 속도 제한은 초당 5건(버스트 10)이고
  `rateLimitRequestsPerSecond`로 바꿉니다.
- `getMultiCompanyMajorAccounts`는 `corpCode`를 쉼표로 이어 **한 번에 최대 100개**까지 받습니다. 101개째부터는 호출
  전체가 `status: '021'`로 실패합니다(부분 결과 아님). 100개씩 나눠 호출하세요.
- 단일/다중회사 주요계정·주요지표 응답에는 **지배/비지배 지분 구분이 없습니다.** 연결 당기순이익·자본 합계는 두 몫을
  합친 값이라, 비지배 지분이 큰 지주회사는 이 값으로 계산한 PBR·ROE가 증권사의 지배주주 기준과 다르게 나옵니다.
  지배주주 몫은 `getSingleCompanyFullStatements`에서 "지배기업 소유주지분"/"비지배지분" 계정을 직접 찾아 분리하세요.
- `new DartClient({ authKey, rawKeys: true })`는 OpenDART 원문(snake_case) 키를 그대로 돌려줍니다. 이때는 메서드의
  응답 타입(camelCase)과 실제 런타임 키가 어긋나니, 원문 키로 직접 읽거나 다른 도구에 그대로 넘길 때만 쓰세요.
- 인증키는 에러 메시지와 로그에서 `***`로 가려집니다.

## 한국은행 ECOS (경제통계)

가입 없이 공개 시험 키 `sample`로 바로 씁니다. `statisticSearch`가 통계 조회, `statisticCatalog`가 통계표·항목·100대 지표
목록, `statisticGlossary`가 용어·메타입니다.

```ts
import { EcosClient, KTB_10Y, parseEcosValue } from 'cluefin-openapi';

const ecos = new EcosClient({ authKey: process.env.ECOS_AUTH_KEY }); // 비우면 sample

// 통계표·주기·기간·항목코드로 조회 — 날짜 형식은 주기를 따른다(A 2024 · Q 2024Q1 · M 202401 · D 20240101)
const { rows } = await ecos.statisticSearch.search({
  statCode: '200Y101',
  cycle: 'A',
  start: '2020',
  end: '2023',
  itemCodes: ['10101'],
});

// 자주 쓰는 계열은 상수로 — 국고채 10년 최근 2주(휴일엔 행이 없다)
const ktb = await ecos.statisticSearch.searchSeries(KTB_10Y, '20261001', '20261017');
const last = ktb.rows.at(-1);
console.log(last?.time, parseEcosValue(last?.dataValue)); // '20261016' 4.182 (연 %)

// 어떤 항목이 있는지
const items = await ecos.statisticCatalog.itemList({ statCode: '817Y002' });
```

### 꼭 알아둘 것

- `sample` 키는 **한 번에 10행**입니다. 행 범위(`startRow`·`endRow`)를 생략하면 클라이언트가 10행씩(실키는 1000행씩) 끝까지
  이어 받습니다. 범위를 직접 주면 그쪽만 받고, sample로 10행을 넘기면 `EcosSampleLimitError`입니다.
- **오류도 HTTP 200**으로 옵니다. 클라이언트가 본문 `RESULT.CODE`를 보고 예외로 바꿉니다(`INFO-100` 인증,
  `ERROR-101` 날짜 형식 …). 데이터 없음(`INFO-200`)과 없는 통계표는 예외가 아니라 빈 `rows`입니다.
- 서버는 60초를 넘는 조회를 `ERROR-400`으로 끊습니다(`EcosQueryTimeoutError`). 기간을 나누거나 항목코드를 지정하세요.
- 응답 키는 와이어 이름의 camelCase(`STAT_CODE` → `statCode`)이고 값은 원문 문자열입니다. 숫자 변환은 `parseEcosValue`로
  하고, 단위(연 %, 억원 …)는 행의 `unitName`을 보세요.
- 인증키는 URL 경로에 들어가므로 에러 메시지·로그에는 키를 가린 경로(`/StatisticSearch/***/json/…`)만 남습니다.

## 에러 처리

브로커마다 `Kis*`·`Kiwoom*`·`Nhplug*`·`Dart*`·`Ecos*` 에러 클래스가 있고 모두 `ApiError`를 상속합니다. 브로커가 준
코드는 `error.errorCode`, HTTP 상태는 `error.statusCode`에 있습니다.

```ts
import { ApiError, KisAuthenticationError } from 'cluefin-openapi';

try {
  await client.domesticBasicQuote.getStockCurrentPrice({ fidCondMrktDivCode: 'J', fidInputIscd: '005930' });
} catch (err) {
  if (err instanceof KisAuthenticationError) {
    // 토큰 만료 → 재발급
  } else if (err instanceof ApiError) {
    console.error(err.name, err.errorCode, err.message);
  }
}
```

**`KisApiError`는 `KisAuthenticationError`·`KisRateLimitError`의 부모가 아닙니다**(키움·NH PLUG·DART·ECOS도 같습니다).
종류별 클래스는 `ApiAuthenticationError` 같은 공통 클래스를 상속하므로, 한 브로커의 오류를 모두 잡으려면 `ApiError`로
잡으세요.
