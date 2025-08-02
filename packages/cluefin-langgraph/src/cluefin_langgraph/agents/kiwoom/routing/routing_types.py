"""Routing types and models for Kiwoom agent system."""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class AgentType(Enum):
    """Available agent types for Kiwoom routing."""

    ACCOUNT = "account"
    CHART = "chart"
    MARKET_INFO = "market_info"
    ETF = "etf"
    THEME_SECTOR = "theme_sector"


class IntentClassification(BaseModel):
    """Intent classification result from LLM."""

    agent_type: AgentType = Field(..., description="The classified agent type")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score of the classification"
    )
    reasoning: str = Field(..., description="Reasoning behind the classification")
    extracted_params: Dict[str, Any] = Field(
        default_factory=dict, description="Extracted parameters from user prompt"
    )


class RoutingRequest(BaseModel):
    """Request object for routing system."""

    user_prompt: str = Field(..., description="User's natural language prompt")
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional context for routing"
    )


class RoutingResponse(BaseModel):
    """Response object from routing system."""

    agent_type: AgentType = Field(..., description="The agent that handled the request")
    classification: IntentClassification = Field(
        ..., description="Classification details"
    )
    result: Any = Field(..., description="The result from the specialized agent")
    formatted_response: Optional[str] = Field(
        default=None, description="Human-readable formatted response"
    )


class AgentMetadata(BaseModel):
    """Metadata for each agent type."""

    name: str = Field(..., description="Display name of the agent")
    description: str = Field(..., description="Description of agent capabilities")
    keywords: list[str] = Field(
        default_factory=list, description="Keywords associated with this agent"
    )
    examples: list[str] = Field(
        default_factory=list, description="Example prompts this agent can handle"
    )


# Agent metadata definitions
AGENT_METADATA: Dict[AgentType, AgentMetadata] = {
    AgentType.ACCOUNT: AgentMetadata(
        name="계좌 에이전트",
        description="계좌 잔고, 보유종목, 손익 조회 등 계좌 관련 업무를 처리합니다.",
        keywords=[
            "계좌",
            "잔고",
            "보유",
            "종목",
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
            "매수가능금액이 얼마인가요?",
        ],
    ),
    AgentType.CHART: AgentMetadata(
        name="차트 에이전트",
        description="주가 차트, 시세 데이터 조회 등 차트 관련 업무를 처리합니다.",
        keywords=[
            "차트",
            "시세",
            "주가",
            "캔들",
            "일봉",
            "분봉",
            "시간봉",
            "가격",
            "거래량",
            "이동평균",
        ],
        examples=[
            "삼성전자 일봉 차트를 보여줘",
            "NAVER 최근 한달 차트 분석해줘",
            "코스피 지수 차트를 보여줘",
        ],
    ),
    AgentType.MARKET_INFO: AgentMetadata(
        name="시장정보 에이전트",
        description="종목 정보, 시장 정보, 공시 등을 조회합니다.",
        keywords=[
            "종목정보",
            "기업정보",
            "재무",
            "공시",
            "배당",
            "주주",
            "시가총액",
            "업종",
            "실적",
            "뉴스",
        ],
        examples=[
            "삼성전자 기업정보를 알려줘",
            "LG화학 재무제표 보여줘",
            "최근 공시 내역을 확인하고 싶어",
            "배당금 지급일이 언제인가요?",
        ],
    ),
    AgentType.ETF: AgentMetadata(
        name="ETF 에이전트",
        description="ETF 정보 조회 및 ETF 관련 업무를 처리합니다.",
        keywords=[
            "ETF",
            "상장지수펀드",
            "인덱스펀드",
            "섹터ETF",
            "테마ETF",
            "KODEX",
            "TIGER",
            "ACE",
        ],
        examples=[
            "KODEX 200 정보를 알려줘",
            "반도체 ETF 추천해줘",
            "ETF 수익률 순위를 보여줘",
            "인버스 ETF 종류가 뭐가 있나요?",
        ],
    ),
    AgentType.THEME_SECTOR: AgentMetadata(
        name="테마/섹터 에이전트",
        description="테마주, 섹터별 종목 정보를 조회합니다.",
        keywords=[
            "테마",
            "섹터",
            "업종",
            "그룹",
            "바이오",
            "게임",
            "반도체",
            "자동차",
            "2차전지",
            "AI",
        ],
        examples=[
            "반도체 관련주를 알려줘",
            "바이오 섹터 상승률 TOP 10",
            "AI 테마주 추천해줘",
            "자동차 업종 시황은 어때?",
        ],
    ),
}
