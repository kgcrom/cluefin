# `.d.ts` 생성 방식 이관 계획 — 수기 템플릿에서 컴파일러 산출물로

**상태**: 완료(2026-08-31, `refactor/ts-dts-emit`). 방안 1로 이관했고, 그 과정에서 생긴 NodeNext 회귀까지 수정했다. 실측 결과는 맨 아래 「이관 결과」와 「이관이 만든 회귀와 그 수정」 참고.
**작성**: 2026-08-30, `fix/ts-dts-exports` 작업 중 파생.

## 왜

`dist/types/index.d.ts` 는 `tsc` 산출물이 아니다. `scripts/generate-types.mjs`(546줄)가
문자열로 조립한다. 도메인 클래스만 메타데이터에서 자동 생성되고, 나머지 — 인증, 토큰
캐시, 소켓 클라이언트, 상수, Zod 스키마 — 는 사람이 손으로 적어야 한다.

**적지 않으면 조용히 빠진다.** 2026-08-30 실측:

| 벤더 | 런타임 export | 선언 누락 |
|---|---|---|
| nhplug | 17 | 0 (직전 작업에서 보강) |
| KIS | 32 | 27 |
| 키움 | 5 | 3 |

누락된 export 는 런타임에는 정상 동작하는데 소비자의 타입스크립트가 "그런 export 없다"고
거절한다. README 가 이미 문서화한 `KisSocketClient` 같은 것들이라, 문서 보고 따라 한
사용자가 곧바로 막힌다. 그리고 이 결함은 **우리 CI 로는 잡히지 않는다** — 유닛테스트는
`src` 를 직접 import 하고, `npm run typecheck` 는 tsdown 번들러라 배포될 `.d.ts` 를
검사하지 않는다.

드리프트 테스트(`tests/core/dts-drift.test.ts`)로 누락 자체는 막게 됐지만, 그건 증상을
잡는 그물이지 원인을 없앤 게 아니다. 새 export 를 추가할 때마다 사람이 선언을 두 번
쓰는 구조는 그대로다.

### 수기 템플릿으로는 못 메우는 부분

위 표는 **런타임 export** 기준이고 그건 다 채웠다. 하지만 각 벤더의 `schemas/` 가
내보내는 **응답 타입은 한 건도 선언돼 있지 않다**(2026-08-30 실측):

| 벤더 | `schemas/*` 응답 타입 | `.d.ts` 누락 |
|---|---|---|
| KIS | 164 | 164 |
| 키움 | 130 | 130 |
| nhplug | 51 | 51 |

합계 345건이다. `import type { StockInfoResponse } from 'cluefin-openapi'` 가 지금
소비자에게서 실패한다. 이걸 생성기에 손으로 적는 건 현실적이지 않고, 적더라도 필드가
바뀔 때마다 같은 방식으로 다시 낡는다. **이관이 필요한 진짜 이유가 이 345건이다** —
컴파일러가 뽑으면 공짜로 따라오고, 손으로 적으면 영원히 따라잡지 못한다.

(드리프트 테스트가 이 345건을 잡지 않는 것은 의도적이다. 타입 전용 export 는 벤더별
허용목록으로만 검사한다 — 지금 구조에서 전수 검사를 켜면 고칠 방법이 없는 실패가
상시로 남는다.)

## 무엇으로 바꾸나

컴파일러가 `src` 에서 직접 선언을 뽑게 한다. 두 가지 방법이 있다.

### 방안 1 — `tsc --emitDeclarationOnly` (권장)

별도 `tsconfig.build.json` 으로 `src` 만 컴파일해 `dist/types/` 에 선언 트리를 뽑는다.

- 장점: 표준적이고, 소스가 곧 정본이라 누락이 원천적으로 불가능하다.
- 단점: 단일 파일이 아니라 `src` 구조를 그대로 미러링한 트리가 나온다.
  `package.json` 의 `types` 는 `dist/types/index.d.ts` 를 가리키면 되고 그 파일이
  나머지를 re-export 하므로 동작에는 문제없다. 다만 배포 파일 수가 112개 늘어난다.

### 방안 2 — tsdown 의 `dts: true`

`tsdown.config.ts` 가 지금 `dts: false` 로 꺼 놓았다. 켜면 번들된 단일 `.d.ts` 가 나온다.

- 장점: 지금과 같은 단일 파일 배포 형태를 유지한다.
- 단점: 롤업 과정에서 이름 충돌 시 자동 리네임이 일어날 수 있다. 이 패키지는
  `FileTokenCacheStore` 같은 이름이 KIS·nhplug 양쪽에 있고 배럴에서 접두어로 구분하는
  구조라 실제로 부딪힌다.

**권장은 방안 1이다.** 방안 2의 롤업 리네임이 공개 타입 이름을 바꿔 버리면 그게 곧
브레이킹 체인지고, 파일 수가 느는 건 사용자에게 보이지 않는 비용이다.

## 선행 조건 — 생각보다 가볍다

착수 전 가장 큰 걱정은 "기존 코드가 `tsc` 를 통과하지 못한다"였는데, 실측해보니 아니다.

```
tsc --noEmit -p tsconfig.json  →  에러 62건
  그중 src/ 하위        1건
  그중 tests/ 하위     61건
```

`tsconfig.json` 의 `include` 가 `["src", "tests"]` 라 테스트까지 끌고 들어와서 커 보였을
뿐이다. **선언 생성은 `src` 만 필요하므로 실제 걸림돌은 1건이다.**

```
src/core/retry.ts(21,22): error TS18048: 'randomValue' is possibly 'undefined'.
```

`noUncheckedIndexedAccess` 때문에 `values[0]` 이 `number | undefined` 로 좁혀지는 건인데,
`new Uint32Array(1)` 의 0번 인덱스라 런타임에는 항상 존재한다. 단언이 아니라 기본값
(`values[0] ?? 0`)으로 처리하는 게 낫다 — 이 경로는 재시도 지터 계산이라 0이어도 무해하다.

경로 별칭 걱정도 없다. `tsconfig.json` 에 `paths: {"@/*": ["src/*"]}` 가 선언돼 있지만
`src` 에서 실제 사용처는 **0건**이다(전부 상대 경로). 별칭이 섞여 있었다면 emit 된
`.d.ts` 에 `@/` 가 그대로 남아 소비자가 해석하지 못했을 텐데, 그 문제가 없다.

## 단계

**Phase 1 — `src` 를 tsc 클린하게**
`src/core/retry.ts` 1건 수정. 유닛테스트로 재시도 지터 동작이 그대로인지 확인.

**Phase 2 — `tsconfig.build.json` 추가**
`tsconfig.json` 을 extends 하고 `include: ["src"]`, `emitDeclarationOnly: true`,
`declarationDir: "dist/types"`, `noEmit: false`. 기존 `tsconfig.json` 은 에디터·테스트용으로
그대로 둔다(테스트의 61건은 이 작업 범위가 아니다).

**Phase 3 — 생성기 대체**
`package.json` 의 `build:types` 를 `tsc -p tsconfig.build.json` 으로 교체하고
`scripts/generate-types.mjs` 를 삭제한다. `scripts/generate-metadata.mjs` 는 **남긴다** —
그건 파이썬 소스에서 엔드포인트 메타데이터를 뽑는 별개 역할이고 이 이관과 무관하다.

**Phase 4 — 산출물 대조**
이관 전후의 공개 타입 표면이 같은지 확인한다. 이관 전 `.d.ts` 를 보관해 두고, 이관 후
산출물과 export 이름 집합을 비교한다. **여기서 이름이 늘어나는 건 정상이다**(지금까지
빠져 있던 것들이 나타나므로). 줄어들면 회귀다.

특히 확인할 것:
- Zod 스키마의 추론 타입이 거대한 `z.ZodObject<...>` 로 펼쳐져 파일이 비대해지는 정도.
  심하면 `src` 쪽에 명시적 타입 주석을 달아 접는다.
- 직전 작업에서 방안 (a)로 처리한 KIS 실시간 스키마 18건이 이관 후 제대로 된 추론
  타입을 갖는지 — 이관의 실질적 이득이 바로 이 부분이다.

**Phase 5 — 드리프트 테스트 정리**
`tests/core/dts-drift.test.ts` 의 "생성기 출력에 이름이 있는가" 검사는 생성기가 사라지면
의미가 없다. 대신 **빌드된 `.d.ts` 를 임시 `node_modules` 에 설치해 소비자 관점으로
컴파일하는 검사**로 바꾼다. 이 방식은 이미 `tests/nhplug/readme-samples.test.ts` 작업에서
써 봤다 — 이름 존재 여부보다 강한 보증이다.

**Phase 6 — 배포 확인**
`npm run publish:check`, `npm pack --dry-run` 으로 파일 목록과 크기 변화를 본다.
`package.json` 의 `files` 가 `dist` 전체를 포함하므로 추가 설정은 필요 없다.

## 왜 지금 하지 않았나

직전 작업(`fix/ts-dts-exports`)은 누락된 선언을 채워 사용자가 겪는 문제를 먼저 없애는
게 목적이었다. 이관은 KIS·키움·nhplug 세 벤더의 공개 타입 표면을 한꺼번에 재생성하므로,
같은 릴리스에 섞으면 회귀가 생겼을 때 원인이 "채워 넣은 선언"인지 "생성 방식 변경"인지
가릴 수 없다.

이관은 별도 브랜치·별도 릴리스로 진행한다. 선행 조건이 1건뿐이라 착수 비용은 낮다.

## 관련

- `packages/cluefin-openapi-ts/AGENTS.md` — "Coupling to the Python sibling" 에 수기
  템플릿의 함정이 기록돼 있다. 이관이 끝나면 그 항목을 갱신할 것.

## 이관 결과 (2026-08-30 실측)

방안 1 그대로 진행했다. 계획이 실제와 어긋난 부분만 적는다.

### 공개 표면 diff

`dist/types/index.d.ts` 를 모듈로 해석해 export 이름 집합을 비교했다.

| | 이관 전 | 이관 후 |
|---|---|---|
| export 이름 | 153 | 449 |

- **추가 315건** — `*Response` 181(키움 130 + nhplug 51), `*ResponseMap` 16, Zod 스키마 상수 118.
- **감소 19건** — 전부 수기 템플릿이 **없는 것을 선언하던** 항목이다. 런타임 번들(`dist/esm/index.js`)에
  대조해 19건 모두 실제로 존재하지 않음을 확인했다. 즉 회귀가 아니라 유령 선언 제거다.
  - 도메인 클래스 18건(`DomesticAccount`, `KiwoomDomesticChart`, `OverseasBasicQuote` 등):
    배럴이 내보낸 적이 없고 클라이언트 프로퍼티(`client.domesticAccount`)로만 닿는다.
  - `RealtimeSchema<T>` 1건: 생성기가 지어낸 인터페이스. 이제 KIS 실시간 스키마 18건이
    진짜 `z.ZodObject<...>` 추론 타입을 갖는다(계획이 기대한 이득 그대로).
  - `RealtimeSchema<T>` 만은 타입 전용이라 소비자가 쓰고 있었을 수 있다 — 유일한 타입 브레이킹.

### 계획이 틀린 것 — KIS 164건은 "공짜로" 따라오지 않는다

계획은 KIS 164 + 키움 130 + nhplug 51 = 345건이 컴파일러 이관만으로 소비자에게 열린다고 봤는데,
실제로 열린 건 **181건(키움·nhplug)** 뿐이다. `src/kis/index.ts` 가 `schemas/*` 를 **한 건도
re-export 하지 않기** 때문이다(키움은 9개 모듈, nhplug 는 7개 모듈을 re-export 한다).
KIS 선언 파일 자체는 `dist/types/kis/schemas/*.d.ts` 로 정상 emit 되지만 엔트리에서 닿지 않는다.

이건 빌드 방식이 아니라 **배럴 문제**라 이 이관 범위 밖으로 남긴다. 후속 과제로:
`src/kis/index.ts` 에 `schemas/*` re-export 추가(555개 이름). 현재 공개 표면과 이름 충돌 0건으로
확인했다(KIS 는 `GetXxxResponse` 접두, 키움은 접두 없음).

### 크기·파일 수

| | 이관 전 | 이관 후 |
|---|---|---|
| `dist/types` 파일 | 1 | 112 |
| `dist/types` 크기 | 60 kB | 1.29 MB |
| `npm pack` 파일 | 8 | 119 |
| tarball | 240.6 kB | 321.3 kB |
| unpacked | 2.1 MB | 3.3 MB |

Zod 추론이 `z.ZodObject<{...}>` 로 펼쳐지지만 **필드당 한 줄로 평평하게** 나오고 중첩 폭발은
없다(최장 줄 1,019자). 압축 +80 kB 대비 응답 타입 181건을 얻는 거래라 `src` 에 명시적 주석을
달아 접는 작업은 하지 않았다.

### 그 밖의 실측

- 선행 조건은 계획대로 `src/core/retry.ts` 1건뿐이었다(`values[0] ?? 0`). `@/*` 별칭 사용처 0건도 그대로.
- `tsconfig.build.json` 은 base 의 `declarationMap`/`sourceMap` 을 꺼야 한다 — 안 끄면 배포 파일이
  112개 더 늘고 그 맵이 없는 `src` 를 가리킨다.
- 소비자 검사에 심볼릭 링크나 임시 `node_modules` 가 필요 없었다. TypeScript 가 `package.json` 의
  `name` + `exports` 로 **self-reference** 를 해석해 준다 — 패키지 안의 픽스처가 `cluefin-openapi`
  로 import 하면 그대로 배포 경로(`exports["."].types`)를 탄다.
- `npm run typecheck` 는 tsdown 만으로는 선언을 검사하지 못하므로
  `tsc -p tsconfig.build.json --noEmit && tsdown ...` 으로 바꿨다. `publish:check` 가 이걸 문다.
- `tests/core/dts-drift.test.ts` → `tests/core/dts-consumer.test.ts` 로 교체(5 tests).

## 이관이 만든 회귀와 그 수정 — NodeNext 소비자 (2026-08-31)

이관 직후 판정을 「완료」로 적었지만, 소비자 검사를 **`moduleResolution: Bundler` 한 가지로만**
돌렸다. 그 한 가지 모드가 정확히 이 회귀를 통과시켰다.

### 증상

`tsc --emitDeclarationOnly` 는 소스의 상대 지정자를 **그대로** 옮긴다. `src` 가
`from './core/errors'` 라고 쓰면 `dist/types/index.d.ts` 도 `from './core/errors'` 다.
확장자 없는 상대 지정자는 `moduleResolution: node16`/`nodenext` 에서 **불법**이다.

- Bundler 소비자: 정상 컴파일. (그래서 놓쳤다.)
- NodeNext 소비자: 선언 파일에 TS2834, 이어서 소비자가 import 한 **모든** 이름에 TS2305
  (`Module '"cluefin-openapi"' has no exported member 'KiwoomClient'`). 이관 전에도 되던
  `KiwoomClient` 까지 깨진다.

이관 전 `.d.ts` 는 상대 import 가 0건인 단일 파일이라 어느 모드에서도 무사했다. 즉 이건
**이관이 새로 만든 회귀**다.

### 수정 — `src` 의 상대 지정자에 `.js` 붙이기

NodeNext 호환 선언 emit 의 표준 요구사항이다. `src` 전체 **324건**을 바꿨다
(`import` / `import type` / `export … from` / `export type … from` / 인라인
`import('...')` 타입까지). 그중 **3건은 디렉터리 배럴**이라 `.js` 가 아니라 `/index.js` 여야
했다 — `src/index.ts` 의 `./kis` · `./kiwoom` · `./nhplug`. 파일명은 하나도 바꾸지 않았다.

`tests` 는 손대지 않았다. vitest 가 직접 `src` 를 읽으므로 확장자 없이도 그대로 돈다.

**툴체인은 설정 변경이 필요 없었다.** vitest(rolldown 기반 transform)와 tsdown 모두
`./foo.js` 를 `foo.ts` 로 해석한다 — 유닛테스트 485건, ESM·CJS 번들 모두 그대로 통과.

### 두 가지 모드 검사 — 이번 작업의 본체

`tests/fixtures/dts-consumer/` 에 `tsconfig.nodenext.json`(`module` + `moduleResolution`
둘 다 NodeNext)을 추가하고, `tests/core/dts-consumer.test.ts` 가 픽스처를
**Bundler·NodeNext 두 프로젝트로 각각** 컴파일한다. 두 설정이 같은 moduleResolution 을
쓰게 되면 실패하는 가드 테스트도 함께 뒀다(한쪽이 조용히 다른 쪽을 베끼는 걸 막는다).

NodeNext 쪽은 `skipLibCheck: false` 다. 켜져 있으면 TS2834 가 통째로 묵살되고 픽스처가
실제로 import 한 이름에 대해서만 TS2305 가 뜬다 — 즉 픽스처가 건드리지 않는 선언 파일의
같은 결함은 못 잡는다. 끄면 112개 선언 전수 검사가 된다(그래서 `types: ["node"]` 도 필요).

픽스처는 이름만 import 하지 않고 **값의 멤버를 읽는다**: `KiwoomClient.domesticChart`,
`KisSocketClient.env`, `NhplugFileTokenCacheStore.get()` 의 `accessToken`,
`NHPLUG_SUCCESS_RSP_CODES.length`, 그리고 타입 전용으로 `StockInfoResponse`,
`DomesticAccountResponseMap`, `KrStockQuoteCurrentPriceResponse`, `NhplugTokenCacheEntry`.

회귀 재현으로 검사의 유효성을 확인했다. 빌드된 `dist/types/index.d.ts` 의
`'./kiwoom/index.js'` 를 `'./kiwoom/index'` 로 되돌리면 NodeNext 는 TS2305 4건으로 실패하고
Bundler 는 여전히 통과한다.

### `@arethetypeswrong/cli --pack` 매트릭스

| 해석 모드 | 판정 |
|---|---|
| node10 | 🟢 |
| node16 (from CJS) | 👺 Masquerading as ESM |
| node16 (from ESM) | 🟢 (ESM) |
| bundler | 🟢 |

유일한 지적인 `node16 (from CJS)` 는 **이 이관과 무관한 기존 결함**이다. 이관 직전 커밋
(`57f6286`, 수기 템플릿 시절)을 별도 워크트리에서 빌드해 같은 명령을 돌린 결과가
**글자 그대로 동일**했다. 원인은 듀얼 빌드인데 `types` 가 하나뿐인 것 —
`"type": "module"` 패키지에서 `.d.ts` 는 ESM 선언인데 `require` 는 `dist/cjs/index.cjs` 로
간다. 고치려면 `.d.cts` 를 따로 emit 하고 `exports.require.types` 를 붙여야 하는데,
그건 배포 형태를 바꾸는 별개 결정이라 이 PR 범위 밖으로 남긴다.

`node16 (from ESM)` 이 🟢 인 것이 이번 수정의 성과다. `.js` 확장자를 붙이지 않았다면
여기가 깨진 채 배포됐을 것이다.

### 교훈

소비자 검사를 **한 가지 moduleResolution 으로만** 돌리면 이 등급의 회귀는 통과한다.
`dist/types` 관련 변경을 할 때는 두 모드 검사가 여전히 두 모드인지부터 확인할 것.
