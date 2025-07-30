"""의도 분류기

사용자 프롬프트를 분석하여 적절한 에이전트 타입을 결정하는 분류기
"""

from typing import Any, Dict

from .routing_types import AgentType, IntentClassification


class IntentClassifier:
    """LLM 기반 의도 분류기"""

    def __init__(self, llm):
        """의도 분류기 초기화

        Args:
            llm: LLM 인스턴스
        """
        self.llm = llm
        self.classification_prompt = self._build_classification_prompt()
        self.keyword_classifier = KeywordBasedClassifier()

    def classify(self, user_prompt: str) -> IntentClassification:
        """사용자 프롬프트를 분석하여 적절한 에이전트 타입을 결정

        Args:
            user_prompt: 사용자 입력 프롬프트

        Returns:
            의도 분류 결과
        """
        # TODO: Phase 2에서 LLM 기반 분류 로직 구현
        # 현재는 키워드 기반 분류로 대체
        return self.keyword_classifier.classify(user_prompt)

    def _build_classification_prompt(self) -> str:
        """분류를 위한 프롬프트 템플릿 구성"""
        return """
        다음 사용자 요청을 분석하여 적절한 Kiwoom 에이전트로 분류해주세요:

        에이전트 유형:
        1. ACCOUNT: 계좌 잔고, 보유종목, 손익 조회
        2. CHART: 주가 차트, 시세 데이터 조회
        3. ORDER: 주식 매수/매도 주문
        4. FOREIGN: 해외주식 관련 업무
        5. MARKET_INFO: 종목 정보, 시장 정보 조회
        6. ETF: ETF 관련 정보 조회
        7. THEME_SECTOR: 테마주, 섹터 정보 조회

        사용자 요청: {user_prompt}

        결과를 JSON 형태로 반환해주세요:
        {{
            "agent_type": "적절한_에이전트_타입",
            "confidence": 0.0-1.0,
            "reasoning": "분류 근거",
            "extracted_params": {{추출된_매개변수}}
        }}
        """


class KeywordBasedClassifier:
    """LLM 분류를 보완하는 키워드 기반 분류기"""

    KEYWORD_MAPPING = {
        AgentType.ACCOUNT: ["계좌", "잔고", "보유", "종목", "손익", "평가금액", "예수금", "매수가능금액"],
        AgentType.CHART: ["차트", "시세", "주가", "캔들", "일봉", "분봉", "시간봉", "가격"],
        AgentType.ORDER: ["매수", "매도", "주문", "거래", "체결", "미체결", "정정", "취소"],
        AgentType.FOREIGN: ["해외", "미국", "나스닥", "다우", "S&P", "외국주식", "해외종목"],
        AgentType.MARKET_INFO: ["종목정보", "기업정보", "재무", "공시", "배당", "주주", "시가총액"],
        AgentType.ETF: ["ETF", "상장지수펀드", "인덱스펀드", "섹터ETF", "테마ETF"],
        AgentType.THEME_SECTOR: ["테마", "섹터", "업종", "그룹", "바이오", "게임", "반도체", "자동차"],
    }

    def classify(self, user_prompt: str) -> IntentClassification:
        """키워드 기반으로 의도 분류

        Args:
            user_prompt: 사용자 입력 프롬프트

        Returns:
            의도 분류 결과
        """
        user_prompt_lower = user_prompt.lower()
        scores = {}

        for agent_type, keywords in self.KEYWORD_MAPPING.items():
            score = sum(1 for keyword in keywords if keyword in user_prompt_lower)
            if score > 0:
                scores[agent_type] = score / len(keywords)

        if not scores:
            # 기본값으로 MARKET_INFO 반환
            return IntentClassification(
                agent_type=AgentType.MARKET_INFO,
                confidence=0.5,
                reasoning="키워드 매칭되지 않음, 기본값으로 시장정보 에이전트 선택",
                extracted_params={},
            )

        best_agent = max(scores.keys(), key=lambda k: scores[k])
        confidence = scores[best_agent]

        return IntentClassification(
            agent_type=best_agent,
            confidence=confidence,
            reasoning=f"키워드 기반 분류: {best_agent.value}",
            extracted_params={},
        )
