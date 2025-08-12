# cluefin-langgraph routing 클래스 Integration Test 작성 계획

## 📋 테스트 대상 클래스
1. **KiwoomRouterAgent** - 메인 라우터 에이전트
2. **IntentClassifier** - 의도 분류기  
3. **KeywordBasedClassifier** - 키워드 기반 분류기

## 🎯 Integration Test 작성 전략

### 테스트 파일 구조
```
tests/integration/kiwoom/
├── test_router_agent.py       # KiwoomRouterAgent 통합 테스트
├── test_intent_classifier.py  # IntentClassifier 통합 테스트
└── conftest.py               # 공통 fixtures 및 설정
```

### 각 파일별 테스트 케이스

#### A. test_router_agent.py
- **End-to-End 워크플로우 테스트**
  - 실제 LLM과 연동한 의도 분류 → 에이전트 라우팅 → 응답 포매팅
  - 다양한 사용자 프롬프트에 대한 전체 처리 과정 검증
  
- **실제 에이전트 통합 테스트**
  - 각 specialized agent와의 실제 통합
  - 에이전트 간 전환 및 상태 관리
  
- **오류 복구 시나리오**
  - API 호출 실패 시 복구
  - 타임아웃 처리
  - 잘못된 분류 시 폴백 메커니즘

#### B. test_intent_classifier.py  
- **실제 LLM 통합 테스트**
  - OpenAI/Claude 등 실제 LLM과 연동
  - 다양한 한국어 금융 프롬프트 분류 정확도
  
- **LLM + 키워드 분류기 협업**
  - 실제 환경에서의 하이브리드 분류
  - 신뢰도 조정 메커니즘 검증

#### C. conftest.py
- **공통 Fixtures**
  - 실제 Kiwoom Client 인스턴스 (테스트 환경)
  - LLM 인스턴스 (API 키 필요)
  - 테스트용 계좌 정보 및 종목 데이터

### 테스트 환경 설정
- `.env` 파일에서 실제 API 키 로드
- 테스트 실행 시 API 키 존재 여부 확인
- API 키가 없으면 테스트 스킵 처리

### 테스트 데이터 준비
- 실제 한국 주식 종목 코드 사용 (삼성전자, SK하이닉스 등)
- 다양한 금융 용어가 포함된 프롬프트 세트
- 엣지 케이스 및 복잡한 요청 시나리오

### 검증 항목
- 응답 시간 측정 (성능 테스트)
- 분류 정확도 측정
- 에러 핸들링 적절성
- 한글 처리 정확성
- LangGraph 상태 전이 정확성

## 🚀 구현 체크리스트

### Phase 1: 기본 설정
- [x] conftest.py 작성
  - [x] pytest fixtures 설정
  - [x] 환경 변수 로딩 (KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, OPENAI_API_KEY)
  - [x] Kiwoom Client 초기화 fixture
  - [x] LLM (OpenAI/Claude) 초기화 fixture
  - [x] 테스트 데이터 fixture (종목 코드, 계좌 번호 등)
  - [x] API 키 없을 시 스킵 마커 설정

### Phase 2: IntentClassifier 통합 테스트
- [x] test_intent_classifier.py 작성
  - [x] 실제 LLM 연동 테스트
    - [x] 계좌 관련 프롬프트 분류
    - [x] 차트 관련 프롬프트 분류
    - [x] 시장정보 관련 프롬프트 분류
    - [x] ETF 관련 프롬프트 분류
    - [x] 테마/섹터 관련 프롬프트 분류
  - [x] 복잡한 프롬프트 처리
    - [x] 여러 의도가 섞인 프롬프트
    - [x] 모호한 프롬프트
    - [x] 금융 전문용어 포함 프롬프트
  - [x] 파라미터 추출 정확도
    - [x] 종목코드 추출
    - [x] 수량 추출
    - [x] 날짜 추출
  - [x] 성능 측정
    - [x] 평균 응답 시간
    - [x] 분류 정확도 통계

### Phase 3: RouterAgent 통합 테스트
- [ ] test_router_agent.py 작성
  - [ ] End-to-End 워크플로우
    - [ ] 계좌 잔고 조회 플로우
    - [ ] 차트 데이터 조회 플로우
    - [ ] 종목 정보 조회 플로우
    - [ ] ETF 정보 조회 플로우
    - [ ] 테마 종목 조회 플로우
  - [ ] 에이전트 간 연계
    - [ ] 정확한 에이전트 라우팅
    - [ ] 에이전트 응답 포매팅
    - [ ] 상태 관리 검증
  - [ ] 오류 처리
    - [ ] API 호출 실패 시나리오
    - [ ] 타임아웃 처리
    - [ ] 잘못된 분류 복구
    - [ ] 네트워크 오류 처리
  - [ ] 동시성 테스트
    - [ ] 여러 요청 동시 처리
    - [ ] 비동기 처리 검증
  - [ ] 실제 Kiwoom API 연동
    - [ ] 실제 계좌 데이터 조회
    - [ ] 실제 시세 데이터 조회
    - [ ] Rate limiting 처리

### Phase 4: 검증 및 마무리
- [ ] 전체 테스트 실행
- [ ] 테스트 커버리지 확인
- [ ] 성능 벤치마크 문서화
- [ ] 실패 케이스 분석 및 수정
- [ ] CI/CD 파이프라인 설정

## 📚 참고사항

### 실행 명령어
```bash
# integration test 실행
uv run pytest -m "integration and requires_auth" packages/cluefin-langgraph/tests/integration/ -v

# 특정 테스트 파일 실행
uv run pytest -m "integration and requires_auth" packages/cluefin-langgraph/tests/integration/kiwoom/test_router_agent.py -v

# 커버리지와 함께 실행
uv run coverage run --source=packages/cluefin-langgraph/src -m "integration and requires_auth" pytest packages/cluefin-langgraph/tests/integration/
uv run coverage xml
```

### 환경 변수 설정
```bash
# .env 파일 생성
cp packages/cluefin-openapi/.env.sample packages/cluefin-openapi/.env

# 필요한 API 키 설정
KIWOOM_APP_KEY=your_app_key
KIWOOM_SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key  # LLM 테스트용
```

### 주의사항
- Integration test는 실제 API를 호출하므로 비용이 발생할 수 있습니다. 테스트는 gpt-3.5-turbo 사용
- 테스트 데이터는 실제 거래에 영향을 주지 않도록 주의해야 합니다
- Rate limit을 고려하여 적절한 지연 시간을 설정해야 합니다
