# cluefin-openapi (TypeScript)

> **cluefin-openapi (TypeScript)**: KIS/키움 OpenAPI를 위한 타입 안전 TypeScript 클라이언트

![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)
![Node](https://img.shields.io/badge/Node-20%2B-green)
![npm](https://img.shields.io/badge/npm-10%2B-cb3837)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 주요 기능

- **KIS + 키움 통합 지원**: 하나의 패키지에서 두 증권사 OpenAPI 클라이언트 제공
- **타입 안전 입력/응답 처리**: camelCase 기반 메서드와 런타임 검증 제공
- **자동 재시도/요청 제한 관리**: 기본 retry, timeout, rate limit 내장
- **일관된 에러 모델**: 인증/권한/네트워크/서버 오류를 명시적 에러 타입으로 구분
- **도메인별 API 접근**: 국내 시세/종목정보/차트 등 엔드포인트를 도메인 단위로 구성

## ⚡ 빠른 시작

### 설치

```bash
# 패키지 설치
npm install cluefin-openapi
```

### 런타임 요구사항

- Node.js 20+

## 🎯 왜 cluefin-openapi (TypeScript)인가요?

### 통합 인터페이스
KIS, 키움 OpenAPI를 일관된 TypeScript 인터페이스로 사용합니다.

### 타입 기반 개발 생산성
엔드포인트 메서드와 입력 파라미터를 타입으로 제공해 실수를 줄입니다.

### 안정적인 API 호출
기본 timeout/retry/rate-limit 정책으로 불안정한 네트워크 환경에 대응합니다.

## 📖 시작하기

### 1. API 키 발급

- 키움증권 OpenAPI: [https://apiportal.kiwoom.com/](https://apiportal.kiwoom.com/)
- 한국투자증권 OpenAPI: [https://apiportal.koreainvestment.com/](https://apiportal.koreainvestment.com/)

### 2. 환경 변수 설정

```bash
# 워크스페이스 루트 기준
cp apps/cluefin-cli/.env.sample .env
```

`.env` 예시:

```bash
KIWOOM_APP_KEY=your_kiwoom_app_key
KIWOOM_SECRET_KEY=your_kiwoom_secret_key
KIWOOM_ENV=dev

KIS_APP_KEY=your_kis_app_key
KIS_SECRET_KEY=your_kis_secret_key
KIS_ENV=dev
```

## 📚 API 사용 예제

### 키움 인증 + 클라이언트 호출

```ts
import { KiwoomAuth, KiwoomClient } from 'cluefin-openapi';

const auth = new KiwoomAuth({
  appKey: process.env.KIWOOM_APP_KEY!,
  secretKey: process.env.KIWOOM_SECRET_KEY!,
  env: (process.env.KIWOOM_ENV as 'dev' | 'prod') ?? 'dev',
});

const token = await auth.generateToken();

const client = new KiwoomClient({
  token: token.token,
  env: (process.env.KIWOOM_ENV as 'dev' | 'prod') ?? 'dev',
});

const response = await client.domesticStockInfo.getStockInfo({
  stkCd: '005930',
});

console.log(response.body);
```

### KIS 인증 + 국내 시세 조회

```ts
import { KisAuth, KisHttpClient } from 'cluefin-openapi';

const auth = new KisAuth({
  appKey: process.env.KIS_APP_KEY!,
  secretKey: process.env.KIS_SECRET_KEY!,
  env: (process.env.KIS_ENV as 'dev' | 'prod') ?? 'dev',
});

const token = await auth.generate();

const client = new KisHttpClient({
  token: token.accessToken,
  appKey: process.env.KIS_APP_KEY!,
  secretKey: process.env.KIS_SECRET_KEY!,
  env: (process.env.KIS_ENV as 'dev' | 'prod') ?? 'dev',
});

const response = await client.domesticBasicQuote.getStockCurrentPrice({
  fidCondMrktDivCode: 'J',
  fidInputIscd: '005930',
});

console.log(response.body);
```

## ⚠️ 에러 처리

```ts
import {
  KisAuthenticationError,
  KisRateLimitError,
  KiwoomAuthenticationError,
  KiwoomRateLimitError,
} from 'cluefin-openapi';

try {
  // API 호출
} catch (error) {
  if (error instanceof KisAuthenticationError || error instanceof KiwoomAuthenticationError) {
    console.error('인증 실패:', error.message);
  } else if (error instanceof KisRateLimitError || error instanceof KiwoomRateLimitError) {
    console.error('요청 제한 초과:', error.message);
  } else {
    console.error('알 수 없는 오류:', error);
  }
}
```

## 🛠️ 개발

```bash
cd packages/cluefin-openapi-ts

npm install
npm run build
npm run check
npm run typecheck
npm run test:unit
npm run test:integration
```

## ✅ 테스트와 .env 로딩

`npm run test`와 `npm run test:unit`은 Vitest `setupFiles`로 `tests/setup-env.ts`를 먼저 실행해 환경 변수를 로드합니다.

- `PROJECT_ROOT_DIR`가 설정되어 있으면 `${PROJECT_ROOT_DIR}/.env`를 읽습니다.
- 미설정 시 모노레포 루트의 `.env`를 기본 경로로 사용합니다.
- 이미 설정된 환경 변수는 덮어쓰지 않습니다.

`npm run test:integration`은 Vitest `setupFiles`로 `tests/setup-integration-env.ts`를 먼저 실행합니다.

- `${PROJECT_ROOT_DIR}/.env.test`를 먼저 읽고, 없으면 `${PROJECT_ROOT_DIR}/.env`로 fallback합니다.
- `CLUEFIN_OPENAPI_TS_RUN_INTEGRATION=1` 플래그로 integration 테스트를 실행합니다.
- 키움 인증 integration 테스트는 `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`가 없으면 실패합니다.

예시:

```bash
PROJECT_ROOT_DIR=/path/to/cluefin npm run test:unit
PROJECT_ROOT_DIR=/path/to/cluefin npm run test:integration
```

## 🚢 배포 (npm publish)

### 1. npm 로그인

```bash
npm login          # 브라우저 인증으로 로그인
npm whoami         # 로그인 확인
```

### 2. 빌드 & 검증

```bash
npm run publish:check    # clean → build → lint → typecheck → test
```

### 3. 배포 파일 확인

```bash
npm pack --dry-run    # 실제 배포될 파일 목록 미리 확인
```

### 4. 배포

```bash
npm run publish:manual    # npm publish --access public
```

### 5. 버전 업데이트 (이후 배포 시)

```bash
npm version patch    # 0.1.0 → 0.1.1 (버그픽스)
npm version minor    # 0.1.0 → 0.2.0 (기능 추가)
npm version major    # 0.1.0 → 1.0.0 (Breaking change)
npm run publish:check
npm run publish:manual
```
