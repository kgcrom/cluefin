# Kiwoom 에이전트 라우팅 시스템 구현 계획

## 🎯 프로젝트 개요

사용자의 자연어 프롬프트를 분석하여 적절한 Kiwoom 전문 에이전트로 라우팅하는 지능형 시스템을 LangGraph로 구현합니다.

## 🏗️ 아키텍처 설계

### 1. 전체 시스템 구조

```
사용자 입력 프롬프트
      ↓
  Routing Agent (프롬프트 분석 및 의도 파악)
      ↓
  Intent Classification (의도 분류)
      ↓
특정 Kiwoom Agent로 라우팅
      ↓
API 호출 및 결과 반환
```

### 2. 에이전트 구성

- **Routing Agent**: 최상위 라우터 에이전트
- **Account Agent**: 계좌 관련 업무 (잔고, 보유종목 등)
- **Chart Agent**: 차트 및 시세 데이터 조회
- **Market Info Agent**: 시장 정보 및 종목 정보
- **ETF Agent**: ETF 관련 정보
- **Theme/Sector Agent**: 테마주 및 섹터 정보

## 📋 단계별 구현 계획

### Phase 1: 기본 구조 설정 (1주차)

#### 1.1 프로젝트 구조 생성
- [x] 디렉토리 구조 생성
```
packages/cluefin-langgraph/src/cluefin_langgraph/agents/kiwoom/
├── __init__.py
├── routing/
│   ├── __init__.py
│   ├── router_agent.py           # 메인 라우터 에이전트
│   ├── intent_classifier.py      # 의도 분류기
│   └── routing_types.py          # 라우팅 관련 타입 정의
├── specialized/
│   ├── __init__.py
│   ├── account_agent.py          # 계좌 전용 에이전트
│   ├── chart_agent.py            # 차트 전용 에이전트
│   ├── market_info_agent.py      # 시장정보 전용 에이전트
│   ├── etf_agent.py              # ETF 전용 에이전트
│   └── theme_sector_agent.py     # 테마/섹터 전용 에이전트
└── base/
    ├── __init__.py
    ├── base_agent.py             # 기본 에이전트 클래스
    └── kiwoom_tools.py           # Kiwoom API 툴 래퍼
```

#### 1.2 기본 타입 및 모델 정의
- [x] `routing_types.py` 구현 (AgentType, IntentClassification, RoutingRequest, RoutingResponse)

### Phase 2: 의도 분류 시스템 구현 (2주차)

#### 2.1 Intent Classifier 개발
- [x] `IntentClassifier` 클래스 구현
- [x] 분류 프롬프트 템플릿 작성
- [x] LLM 기반 의도 분류 로직 개발

#### 2.2 키워드 기반 보조 분류기
- [x] `KeywordBasedClassifier` 클래스 구현
- [x] 각 에이전트별 키워드 매핑 정의
- [x] LLM 분류 결과 검증 로직 추가

### Phase 3: 기본 에이전트 클래스 구현 (3주차)

#### 3.1 Base Agent 클래스
- [x] `BaseKiwoomAgent` 추상 클래스 구현
- [x] 공통 메서드 정의 (`_initialize_tools`, `process_request`, `_format_response`)
- [x] Kiwoom 클라이언트 통합

#### 3.2 Kiwoom API 툴 래퍼
- [x] `KiwoomToolFactory` 클래스 구현
- [x] 계좌 관련 도구 래퍼 작성 (`create_account_tools`)
- [x] 차트 관련 도구 래퍼 작성 (`create_chart_tools`)
- [x] 기타 API 도구 래퍼 작성

### Phase 4: 특화 에이전트 구현 (4-5주차)

#### 4.1 Account Agent
- [x] `AccountAgent` 클래스 구현
- [x] 계좌 조회 로직 구현
- [x] 보유종목 조회 로직 구현
- [x] 손익 계산 로직 구현

#### 4.2 Chart Agent
- [x] `ChartAgent` 클래스 구현
- [x] 일봉/분봉/시간봉 차트 조회 로직
- [x] 종목코드 및 기간 파라미터 추출
- [x] 차트 데이터 분석 및 시각화

#### 4.3 기타 전문 에이전트들
<!-- - [ ] `MarketInfoAgent` 구현 (시장정보 관련)
- [ ] `ETFAgent` 구현 (ETF 관련)
- [ ] `ThemeSectorAgent` 구현 (테마/섹터 관련) -->

### Phase 5: 라우터 에이전트 구현 (6주차)

#### 5.1 메인 라우터
- [x] `RouterState` TypedDict 정의
- [x] `KiwoomRouterAgent` 클래스 구현
- [x] LangGraph 워크플로우 구성
- [x] 의도 분류 노드 구현
- [x] 에이전트 라우팅 노드 구현
- [x] 응답 포맷팅 노드 구현
- [x] 비동기 처리 로직 구현

### Phase 6: 테스트 및 최적화 (7주차)

#### 6.1 단위 테스트
- [ ] Intent Classifier 테스트 작성
- [ ] 각 특화 에이전트 테스트 작성
- [ ] Router Agent 워크플로우 테스트 작성
- [ ] API 도구 래퍼 테스트 작성
```python
# tests/unit/test_intent_classifier.py
def test_account_intent_classification():
    classifier = IntentClassifier(mock_llm)
    result = classifier.classify("내 계좌 잔고를 알려줘")
    assert result.agent_type == AgentType.ACCOUNT
    assert result.confidence > 0.8

# tests/unit/test_router_agent.py
def test_routing_workflow():
    router = KiwoomRouterAgent(mock_client, mock_llm)
    response = await router.process("삼성전자 차트를 보여줘")
    assert "차트" in response
```

#### 6.2 통합 테스트
- [ ] 실제 Kiwoom API를 사용한 종단간 테스트
- [ ] 다양한 사용자 시나리오 테스트
- [ ] 성능 및 안정성 테스트
```python
# tests/integration/test_kiwoom_routing.py
def test_end_to_end_routing():
    # 실제 API를 사용한 종단간 테스트
    pass
```

### Phase 7: 고도화 및 배포 (8주차)

#### 7.1 성능 최적화
- [ ] 응답 시간 최적화
- [ ] 캐싱 전략 적용
- [ ] 병렬 처리 구현
- [ ] 메모리 사용량 최적화

#### 7.2 모니터링 및 로깅
- [ ] `RoutingMonitor` 클래스 구현
- [ ] 분류 결과 로깅 시스템
- [ ] 응답 시간 추적 시스템
- [ ] 에러 모니터링 및 알림
```python
# monitoring.py
class RoutingMonitor:
    def log_classification(self, prompt: str, classification: IntentClassification):
        """분류 결과 로깅"""
        pass
    
    def track_response_time(self, agent_type: AgentType, duration: float):
        """응답 시간 추적"""
        pass
```

#### 7.3 사용자 인터페이스
- [ ] 명령줄 인터페이스 구현
- [ ] 사용 예제 및 데모 작성
- [ ] 문서화 및 가이드 작성
- [ ] 패키지 배포 준비
```python
# examples/kiwoom_chat.py
from cluefin_langgraph.agents.kiwoom import KiwoomRouterAgent

async def main():
    router = KiwoomRouterAgent(kiwoom_client, llm)
    
    while True:
        user_input = input("질문을 입력하세요: ")
        if user_input.lower() == 'quit':
            break
            
        response = await router.process(user_input)
        print(f"응답: {response}")
```

## 🎯 예상 사용 시나리오

### 시나리오 1: 계좌 조회
```
사용자: "내 계좌 잔고와 보유종목을 알려줘"
→ Routing Agent가 ACCOUNT로 분류
→ Account Agent가 잔고 및 보유종목 API 호출
→ 결과를 사용자 친화적으로 포맷팅하여 반환
```

### 시나리오 2: 차트 분석
```
사용자: "삼성전자 최근 1개월 차트를 보여줘"
→ Routing Agent가 CHART로 분류하고 종목코드 추출
→ Chart Agent가 일봉 데이터 조회
→ 차트 분석 결과와 함께 반환
```

## 🔧 기술 스택

- **LangGraph**: 워크플로우 오케스트레이션
- **LangChain**: LLM 통합 및 도구 관리
- **Pydantic**: 타입 안전성 및 데이터 검증
- **cluefin-openapi**: Kiwoom API 클라이언트
- **pytest**: 테스트 프레임워크

## 📈 성공 지표

1. **분류 정확도**: 95% 이상의 의도 분류 정확도
2. **응답 시간**: 평균 3초 이내 응답
3. **사용자 만족도**: 자연스러운 대화형 인터페이스
4. **확장성**: 새로운 에이전트 타입 쉽게 추가 가능

## 🚀 향후 확장 계획

1. **멀티모달 지원**: 차트 이미지 생성 및 분석
2. **실시간 알림**: 조건 충족시 자동 알림
3. **포트폴리오 최적화**: AI 기반 투자 제안
4. **음성 인터페이스**: 음성 명령 지원
5. **웹 대시보드**: 웹 기반 사용자 인터페이스
