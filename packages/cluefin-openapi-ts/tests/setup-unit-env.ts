import { loadProjectRootEnv } from './setup-env';

// 단위 테스트 전용 setupFile. `setup-env.ts` 는 부수효과 없이 함수만 내보낸다 —
// 여기서 명시적으로 호출해야 vitest.config.ts(단위 테스트)에서 루트 `.env` 가 로드된다.
// `setup-integration-env.ts` 는 별도로 `.env.test` 를 `.env` 보다 우선해 로드한다.
loadProjectRootEnv();
