# cluefin-cli → desk 이관(feat/desk-kis) 핸드오프

작성일: 2026-08-31

cluefin-cli의 전 기능을 cluefin-desk와 예제 노트북으로 흡수하고 cli를 삭제하는 작업.
코드는 `feat/desk-kis`에 9커밋으로 완료(작업 트리 클린, 미푸시). **사용자 수동 테스트
직전에 멈췄다** — 이 문서는 무엇이 검증됐고 무엇이 안 됐는지, 남은 순서를 기록한다.

## 검증 상태

| 항목 | 상태 | 근거 |
|---|---|---|
| desk·xbrl 단위 테스트 | ✅ 87 + 85 passed | 매 커밋 전 실행 |
| 예제 노트북 2개 (ta·xbrl) | ✅ 전 셀 실데이터 실행 통과 | KIS 100봉·삼성전자/현대차 사업보고서 실측 |
| DART corp_code 버그 수정 | ✅ 실키로 005930→00126380 해석 확인 | 08996b9 |
| desk TUI 화면 조립·탭 로딩 | ✅ Pilot 하네스로 자동 검증 | 7화면 전부, 실 tcss 물려 실행 (2026-09-01 두 화면 → 09-02 전 화면) |
| **desk TUI 화면 전반(눈으로)** | ❌ 미검증 | 하네스는 재무분석·종목상세만. 나머지 5화면은 여전히 앱을 띄워야 안다 |
| **desk의 KIS 신규 패널 실호출** | ❌ 미검증 | 단위 테스트는 mock. 파라미터 값은 cluefin-openapi의 KIS 통합테스트에서 그대로 가져왔으나 desk 경로로 실서버를 때려본 적 없음 |
| ML예측 탭 실제 실행 | ❌ 미검증 | 파이프라인 단위 테스트만 통과 (cli 테스트 이식분) |

### 2026-09-01 추가 작업 (테스트·버그 수정)

수치 요약(테스트 수·화면별 검증 상태·응답 모델에 남은 `max_length` 분포)은
[`desk-migration-status.html`](desk-migration-status.html) 로 정리해 뒀다 — 브라우저로 열면 된다.

전체 `pytest -m "not integration and not realtime"` 2457 passed. desk 테스트는 173 → 226.

고친 것 (모두 "예외 없이 탭이 Loading 에서 멈춘다" 부류 — 수동 테스트로만 드러난다):

- **주식변동 탭에 로더가 아예 없었다** → 주식의 총수 현황 + 증자(감자) 현황(DART) 구현
- corp_code 를 못 찾으면(ETF/ETN) DART 5개 탭이 조용히 Loading 유지 → 안내 문구 표시.
  corp_code **조회 실패**(키·네트워크)와 **비상장**을 구분해서 보여준다
- 사업보고서가 아직 제출 안 된 연초에 빈 화면 → `_fetch_with_year_fallback` 로 직전
  사업연도 → 그 전년도까지 후퇴 (DART 는 무자료를 status 013 + list=None 로 준다)
- 주요계정에서 연결(CFS)·개별(OFS) 행이 같은 계정명으로 섞여 임의로 골라졌다 →
  연결 우선, 없으면 개별, 기준을 제목에 표시
- 재무제표·배당 탭은 예외를 로그만 남겼다 → 탭별 `_guarded` 로 화면에 표시
- `r` 연타 시 워커 중복 실행 → 전 화면 `load_all_data` 를 `exclusive=True` 로
- 한글 이중폭 무시한 컬럼 정렬 → `cluefin_desk.formatting.pad`
- VerticalScroll 안 패널의 `height: 1fr` → `auto` (내용이 뷰포트에서 잘렸다)
- ml 테스트에 남은 `apps/cluefin-cli/src` sys.path 조작 제거

추가된 테스트: `test_financial_analysis.py`(포매터·연도 후퇴·CFS 선택),
`test_financial_analysis_screen.py`·`test_stock_detail.py`(Textual Pilot 하네스 —
탭이 채워지는지, 한 탭 실패가 다른 탭을 막지 않는지, KIS/DART 키 없을 때 degrade),
`test_formatting.py`. 하네스 사용법은 `apps/cluefin-desk/AGENTS.md` 참조.

## 남은 것 (순서대로)

### 1. 수동 테스트 — 사용자가 직접, 하나씩 진행하기로 함

`git checkout feat/desk-kis && uv sync --all-packages` 후 리포지토리 루트에서
`uv run cluefin-desk`. desk는 cwd `.env`(운영 키)를 읽는다 — 조회 전용이지만 실계좌
토큰이 발급된다. 키움 dev로는 테스트 불가(모의 키 인증 만료, 메모리 참조).

1. `pytest apps/cluefin-desk/tests packages/cluefin-xbrl/tests -m "not integration"` 재확인
2. 화면 1: 기존 회귀 + 하단 KIS 시장 수급·자금 패널 2개
3. 화면 2: 신규 4탭(배당수익률/공매도/신용상위/이격도) — 배당 탭은 현재가 `-` 가 정상
4. 종목 상세(005930): company info 신규 섹션, 수급 탭 KIS 패널, 투자의견 탭,
   ML예측 탭(`M` 키, 학습 중 UI 프리즈·중복실행 없는지)
5. 재무분석(`F`): KIS 재무/재무제표/공시목록/배당/주요주주/**주식변동**/XBRL 탭.
   주요주주·주식변동 탭에 데이터가 보이면 수정 확인 완료(이전엔 각각 빈 탭·영구 Loading).
   ETF(069500)는 "DART 공시대상 법인이 아닙니다" 가 떠야 정상
6. 화면 4: ETF 선택 후 `N` 키 → NAV 괴리·구성종목
7. 노트북 2개 재실행 (실행 후 커밋 시 nbconvert --clear-output)

### 2. 테스트 통과 후: push + PR (create-pr 스킬)

### 3. 후순위 (계획에서 의도적으로 미룸)

- Phase 2-13: KIS 재무 심화(대차대조표·안정성/성장성), KSD 이벤트 캘린더, 업종지수,
  holiday/VI — 필요해지면 기존 fetcher 패턴 그대로 추가
- 키움 모의투자 재신청 (dev 테스트 경로 복구)
- DART 미노출 데이터: 전체 재무제표(`get_single_company_full_statements` — 지금은
  주요계정만), 감사의견, 자기주식, 소액주주, 임원·직원 현황, 5% 대량보유 보고
- ~~Pilot 하네스를 나머지 5화면으로 확장~~ — 완료 (2026-09-02, 7화면 전부). 랭킹은 탭별 상태줄, ETF 는 시세 상태줄 + NAV 패널 실패 표시까지

## 세션에서 정한 결정 (코드에 이유가 안 남는 것)

- `ta --json`(가공 분석 JSON)은 **대체 없이 폐기** — 사용자 결정. raw 경로는
  cluefin-openapi-cli가 담당
- 다중 기간(1/3/6/12개월) 선택은 desk에 이식하지 않음 — "ta는 examples로 충분,
  필요하면 나중에" (사용자 결정)
- 추정실적(get_estimated_earnings)은 응답이 무라벨 data1~5 그리드라 표시 불가 → 제외
- 외인 순매수 추이 API는 당일 intraday 전용 → 일별 투자자 동향이 커버하므로 제외
- `feat/xbrl-extract-notes-design`은 패키지 몫만 착지(46d96d6), cli 확장분은 desk
  XBRL 탭으로 재구성. 원 브랜치·PR #71은 삭제/close 완료

## 주의

- desk fetcher의 KIS 랭킹 화면코드(`fid_cond_scr_div_code` 등)는 KIS 포털이 요구하는
  고정 키 — 통합테스트 값과 다르게 바꾸면 오류 없이 빈 응답이 올 수 있다
- KIS 재무 시계열은 문서와 달리 진행연도 누적 행이 맨 앞에 온다(실측) —
  `_split_annual_and_ytd`를 우회해 첫 행을 연간으로 쓰면 ROE·성장률이 부풀려진다
