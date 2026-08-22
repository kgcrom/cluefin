# 별도 과제: KIS 주문 통합테스트 추가

작성일: 2026-08-22 (nhplug krstock 세션에서 분리된 과제)

## 배경

브로커별 주문(Order) API 통합테스트 방식이 서로 다르다.

- **Kiwoom**: `tests/kiwoom/test_domestic_order_integration.py` — 모의투자에서 실제 주문을
  제출한다. 매수/매도는 시장가 1주, 정정·취소는 "체결되지 않을 낮은 지정가(기준가 80%,
  1,000원 배수)" 매수주문을 fixture로 접수한 뒤 그 주문번호로 검증. 장종료·휴일·계좌만료
  같은 환경 제약은 `_integration_helpers.skip_if_env_blocked`가 응답 코드 기준으로 런타임 skip.
- **KIS**: 주문 API(`_domestic_account.py`의 `request_stock_quote_*`)는 unit test만 있고
  통합테스트가 없다.

nhplug krstock 주문은 kiwoom 패턴으로 구현하기로 결정했고(2026-08-22), KIS를 같은
패턴으로 정렬하는 작업은 이 문서로 분리한다.

## 할 일

1. `tests/kis/`에 kiwoom 패턴의 주문 통합테스트 추가: 모의(VTS)에서 실제 주문 제출,
   미체결 지정가 fixture로 정정·취소 검증, 환경 제약 런타임 skip 헬퍼 신설.
2. 선행 확인: KIS 모의투자(VTS) 계정 상태. **`.env.test`의 KIS 쪽은 현재 `KIS_ENV=prod`**
   (모의 아님) — VTS 계정 신청/설정부터 필요할 수 있다. prod에서 주문 테스트는 실제
   체결되므로 절대 prod로 돌리지 말 것.
3. KIS 주문 TR은 실전/모의 tr_id가 다르다(`TTTC*`/`VTTC*`) — 테스트에서 env에 맞는
   tr_id를 선택하는 로직 필요.
