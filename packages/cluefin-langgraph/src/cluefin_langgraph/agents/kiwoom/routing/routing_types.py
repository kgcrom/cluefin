"""Routing types and models for Kiwoom agent system."""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class AgentType(Enum):
    """Available agent types for Kiwoom routing."""

    ACCOUNT = "account"
    STOCK_INFO = "stock_info"
    MARKET_INFO = "market_info"
    CHART = "chart"
    THEME = "theme"
    ETF = "etf"


class IntentClassification(BaseModel):
    """Intent classification result from LLM."""

    agent_type: AgentType = Field(..., description="The classified agent type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the classification")
    reasoning: str = Field(..., description="Reasoning behind the classification")
    extracted_params: Dict[str, Any] = Field(default_factory=dict, description="Extracted parameters from user prompt")


class RoutingRequest(BaseModel):
    """Request object for routing system."""

    user_prompt: str = Field(..., description="User's natural language prompt")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for routing")


class RoutingResponse(BaseModel):
    """Response object from routing system."""

    agent_type: AgentType = Field(..., description="The agent that handled the request")
    classification: IntentClassification = Field(..., description="Classification details")
    result: Any = Field(..., description="The result from the specialized agent")
    formatted_response: Optional[str] = Field(default=None, description="Human-readable formatted response")


class AgentMetadata(BaseModel):
    """Metadata for each agent type."""

    name: str = Field(..., description="Display name of the agent")
    description: str = Field(..., description="Description of agent capabilities")
    keywords: list[str] = Field(default_factory=list, description="Keywords associated with this agent")
    examples: list[str] = Field(default_factory=list, description="Example prompts this agent can handle")


# Agent metadata definitions
AGENT_METADATA: Dict[AgentType, AgentMetadata] = {
    AgentType.ACCOUNT: AgentMetadata(
        name="계좌 에이전트",
        description="계좌 잔고, 보유종목, 손익 조회 등 계좌 관련 업무를 처리합니다.",
        keywords=[
            "계좌",
            "잔고",
            "보유",
            "손익",
            "평가금액",
            "예수금",
            "매수가능금액",
            "총자산",
            "수익률",
        ],
        examples=[
            "내 계좌 잔고를 알려줘",
            "보유종목 목록을 보여줘",
            "오늘 수익률이 어떻게 되나요?",
        ],
    ),
    AgentType.STOCK_INFO: AgentMetadata(
        name="종목정보 에이전트",
        description="개별 종목의 기업정보, 재무데이터, 종목검색 등을 처리합니다.",
        keywords=[
            "종목정보",
            "기업정보",
            "재무",
            "검색",
            "종목명",
            "종목코드",
            "시가총액",
            "PER",
            "PBR",
            "배당",
        ],
        examples=[
            "삼성전자 기업정보를 알려줘",
            "LG화학 재무제표 보여줘",
            "네이버 종목코드 알려줘",
        ],
    ),
    AgentType.MARKET_INFO: AgentMetadata(
        name="시장정보 에이전트",
        description="공매도, 기관/외국인 거래, 대차거래, 순위정보, 업종 분석 등 시장 전반 데이터를 처리합니다.",
        keywords=[
            "공매도",
            "기관",
            "외국인",
            "대차거래",
            "순위",
            "상위",
            "업종",
            "섹터",
            "거래량",
            "상승률",
        ],
        examples=[
            "거래량 상위 종목 알려줘",
            "반도체 업종 수익률은?",
            "외국인 순매수 상위 종목",
        ],
    ),
    AgentType.CHART: AgentMetadata(
        name="차트 에이전트",
        description="주가 차트, 현재가, 호가 등 가격 데이터를 처리합니다.",
        keywords=[
            "차트",
            "시세",
            "주가",
            "현재가",
            "호가",
            "일봉",
            "분봉",
            "캔들",
            "이동평균",
            "기술분석",
        ],
        examples=[
            "삼성전자 일봉 차트를 보여줘",
            "네이버 현재가 알려줘",
            "코스피 지수 차트",
        ],
    ),
    AgentType.THEME: AgentMetadata(
        name="테마 에이전트",
        description="테마주 발굴, 테마별 종목 분석, 핫테마 추적 등을 처리합니다.",
        keywords=[
            "테마",
            "관련주",
            "AI",
            "반도체",
            "2차전지",
            "바이오",
            "게임",
            "메타버스",
            "핫테마",
            "급등",
        ],
        examples=[
            "AI 관련주를 알려줘",
            "반도체 테마 상승률 TOP 10",
            "현재 핫한 테마는?",
        ],
    ),
    AgentType.ETF: AgentMetadata(
        name="ETF 에이전트",
        description="ETF 정보 조회, ETF 추천, ETF 분석 등을 처리합니다.",
        keywords=[
            "ETF",
            "etf",
            "상장지수펀드",
            "KODEX",
            "TIGER",
            "ARIRANG",
            "인덱스펀드",
            "추천",
        ],
        examples=[
            "KODEX 200 정보를 알려줘",
            "ETF 추천해줘",
            "반도체 ETF 있나요?",
        ],
    ),
}
