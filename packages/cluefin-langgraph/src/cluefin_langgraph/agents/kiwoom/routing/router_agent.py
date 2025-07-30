"""메인 라우터 에이전트

사용자의 자연어 프롬프트를 분석하여 적절한 Kiwoom 전문 에이전트로 라우팅하는
LangGraph 기반 라우터 에이전트
"""

from typing import Any, TypedDict

# from langgraph import StateGraph
# from cluefin_openapi.kiwoom import Client as KiwoomClient


# TODO: Phase 5에서 구현 예정
class RouterState(TypedDict):
    """라우터 상태를 나타내는 TypedDict"""

    user_prompt: str
    classification: Any  # IntentClassification
    agent_response: Any
    final_response: str


class KiwoomRouterAgent:
    """메인 Kiwoom 라우터 에이전트"""

    def __init__(self, kiwoom_client, llm):
        """라우터 에이전트 초기화

        Args:
            kiwoom_client: Kiwoom API 클라이언트
            llm: LLM 인스턴스
        """
        self.kiwoom_client = kiwoom_client
        self.llm = llm
        # TODO: Phase 5에서 구현
        # self.classifier = IntentClassifier(llm)
        # self.agents = self._initialize_agents()
        # self.graph = self._build_graph()

    async def process(self, user_prompt: str) -> str:
        """사용자 프롬프트를 처리하여 최종 응답 반환

        Args:
            user_prompt: 사용자 입력 프롬프트

        Returns:
            처리된 최종 응답
        """
        # TODO: Phase 5에서 LangGraph 워크플로우 구현
        return f"처리 예정: {user_prompt}"
