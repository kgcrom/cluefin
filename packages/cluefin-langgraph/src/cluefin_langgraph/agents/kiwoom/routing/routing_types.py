"""라우팅 관련 타입 정의

Kiwoom 에이전트 라우팅 시스템에서 사용되는 타입들을 정의
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AgentType(Enum):
    """에이전트 타입 열거형"""

    ACCOUNT = "account"
    CHART = "chart"
    ORDER = "order"
    FOREIGN = "foreign"
    MARKET_INFO = "market_info"
    ETF = "etf"
    THEME_SECTOR = "theme_sector"


class IntentClassification(BaseModel):
    """의도 분류 결과 모델"""

    agent_type: AgentType
    confidence: float
    reasoning: str
    extracted_params: Dict[str, Any]


class RoutingRequest(BaseModel):
    """라우팅 요청 모델"""

    user_prompt: str
    context: Optional[Dict[str, Any]] = None


class RoutingResponse(BaseModel):
    """라우팅 응답 모델"""

    agent_type: AgentType
    classification: IntentClassification
    result: Any
