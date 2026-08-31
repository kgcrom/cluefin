# `.d.ts` 생성 방식 이관 계획 — 수기 템플릿에서 컴파일러 산출물로

**상태**: 제안. 아직 착수하지 않았다.
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
