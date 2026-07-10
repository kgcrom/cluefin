## 관련 이슈

<!-- Closes #이슈번호 — 없으면 "없음"이라고 적어주세요 -->

## 변경 사항

<!-- 무엇을 왜 변경했는지 설명해주세요. 배경(문제·원인)이 있으면 함께 적어주세요 -->

## 변경 유형

- [ ] 버그 수정 (`fix`)
- [ ] 기능 추가/개선 (`feat`)
- [ ] 리팩토링 (`refactor`)
- [ ] 테스트 추가/수정 (`test`)
- [ ] 문서 수정 (`docs`)
- [ ] 의존성/설정 (`chore`)
- [ ] CI/CD (`ci`)

## 영향 범위

<!-- 변경된 패키지/앱을 선택해주세요 -->

- [ ] packages/cluefin-openapi
- [ ] packages/cluefin-ta
- [ ] packages/cluefin-xbrl
- [ ] packages/cluefin-openapi-ts
- [ ] apps/cluefin-cli
- [ ] apps/cluefin-openapi-cli
- [ ] apps/cluefin-desk
- [ ] 루트 프로젝트 설정

## 검증

<!-- 실행한 명령과 결과를 적어주세요. 예:
`uv run pytest -m "not integration"` → 931 passed, 449 deselected
미실행 항목은 사유를 남겨주세요 (예: 통합 테스트 — 실제 API 키 필요, 미실행) -->

- [ ] 단위 테스트 통과 (`uv run pytest -m "not integration"`)
- [ ] 통합 테스트 통과 (`uv run pytest -m integration`)
- [ ] TypeScript 테스트 통과 (`npm run test:unit` — cluefin-openapi-ts 변경 시)
- [ ] 테스트 불필요 (문서, 설정 변경 등)

## 체크리스트

- [ ] `uv run ruff format . && uv run ruff check . --fix` 실행
- [ ] 커밋 메시지가 컨벤션을 따름 (`type(scope): 설명`)
- [ ] `.env`, 시크릿, 인증 정보 미포함
- [ ] 관련 문서 업데이트 완료 (해당 시)

## 브레이킹 체인지 / 참고 사항

<!-- 브레이킹 체인지·마이그레이션 노트는 "없음"이라도 명시해주세요.
알려진 제한사항, 범위 밖으로 남긴 후속 작업도 여기에 적어주세요 -->
