"""기본 에이전트 클래스

모든 Kiwoom 전문 에이전트의 기본 클래스를 정의
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseKiwoomAgent(ABC):
    """모든 Kiwoom 에이전트의 기본 추상 클래스"""

    def __init__(self, kiwoom_client, llm):
        """기본 에이전트 초기화

        Args:
            kiwoom_client: Kiwoom API 클라이언트
            llm: LLM 인스턴스
        """
        self.kiwoom_client = kiwoom_client
        self.llm = llm
        self.tools = self._initialize_tools()

    @abstractmethod
    def _initialize_tools(self) -> List[Any]:
        """각 에이전트별 특화 도구 초기화

        Returns:
            도구 리스트
        """
        pass

    @abstractmethod
    def process_request(self, request: str, params: Dict[str, Any]) -> Any:
        """요청 처리 메인 로직

        Args:
            request: 사용자 요청
            params: 추출된 매개변수

        Returns:
            처리 결과
        """
        pass

    def _format_response(self, data: Any) -> str:
        """응답 데이터를 사용자 친화적으로 포맷팅

        Args:
            data: 원시 응답 데이터

        Returns:
            포맷팅된 응답 문자열
        """
        # TODO: Phase 3에서 구체적인 포맷팅 로직 구현
        return str(data)
