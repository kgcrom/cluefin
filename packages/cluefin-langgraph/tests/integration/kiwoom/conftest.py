"""Shared fixtures and configuration for Kiwoom integration tests."""

import os
from typing import Dict, List
from unittest.mock import Mock

import dotenv
import pytest
from cluefin_openapi.kiwoom import Client as KiwoomClient
from cluefin_openapi.kiwoom._auth import Auth
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


@pytest.fixture(scope="session")
def integration_test_env() -> Dict[str, SecretStr]:
    """Load environment variables required for integration tests.

    Returns:
        Dictionary of required environment variables

    Raises:
        pytest.skip: If required API keys are not available
    """
    dotenv.load_dotenv(dotenv_path=".env.test")

    required_env_vars: Dict[str, SecretStr] = {
        "KIWOOM_APP_KEY": SecretStr(os.getenv("KIWOOM_APP_KEY")),
        "KIWOOM_SECRET_KEY": SecretStr(os.getenv("KIWOOM_SECRET_KEY")),
        "OPENAI_API_KEY": SecretStr(os.getenv("OPENAI_API_KEY")),
    }

    missing_vars = [key for key, value in required_env_vars.items() if not value]

    if missing_vars:
        pytest.skip(f"Integration tests require environment variables: {', '.join(missing_vars)}")

    # Filter out None values to ensure type Dict[str, str]
    return {k: v for k, v in required_env_vars.items() if v is not None}


@pytest.fixture(scope="session")
def kiwoom_client(integration_test_env) -> KiwoomClient:
    """Create authenticated Kiwoom client for integration tests.

    Args:
        integration_test_env: Environment variables fixture

    Returns:
        Authenticated Kiwoom client instance
    """
    auth = Auth(
        app_key=integration_test_env["KIWOOM_APP_KEY"],
        secret_key=integration_test_env["KIWOOM_SECRET_KEY"],
        env="dev",
    )
    client = KiwoomClient(
        token=auth.generate_token().token,
        env="dev",
    )

    return client


@pytest.fixture(scope="session")
def openai_llm(integration_test_env) -> ChatOpenAI:
    """Create OpenAI LLM instance for integration tests.

    Args:
        integration_test_env: Environment variables fixture

    Returns:
        ChatOpenAI instance configured for testing
    """
    return ChatOpenAI(
        api_key=integration_test_env["OPENAI_API_KEY"],
        model="gpt-3.5-turbo",
        temperature=0.1,  # Low temperature for consistent results
        # max_tokens=1000,
        timeout=30,
    )


@pytest.fixture
def test_stock_data() -> Dict[str, Dict[str, str]]:
    """Test data with Korean stock information.

    Returns:
        Dictionary mapping stock names to their information
    """
    return {
        "삼성전자": {
            "code": "005930",
            "market": "KOSPI",
            "sector": "반도체",
        },
        "SK하이닉스": {
            "code": "000660",
            "market": "KOSPI",
            "sector": "반도체",
        },
        "NAVER": {
            "code": "035420",
            "market": "KOSPI",
            "sector": "인터넷",
        },
        "LG화학": {
            "code": "051910",
            "market": "KOSPI",
            "sector": "화학",
        },
        "현대자동차": {
            "code": "005380",
            "market": "KOSPI",
            "sector": "자동차",
        },
    }


@pytest.fixture
def test_etf_data() -> Dict[str, Dict[str, str]]:
    """Test data with Korean ETF information.

    Returns:
        Dictionary mapping ETF names to their information
    """
    return {
        "KODEX 200": {
            "code": "069500",
            "type": "인덱스",
            "underlying": "KOSPI 200",
        },
        "TIGER 2차전지테마": {
            "code": "305540",
            "type": "테마",
            "underlying": "2차전지",
        },
        "ACE 반도체TOP10": {
            "code": "365040",
            "type": "섹터",
            "underlying": "반도체",
        },
    }


@pytest.fixture
def test_account_data() -> Dict[str, str]:
    """Test account information.

    Note: These are dummy account numbers for testing.
    Real account numbers should never be hardcoded.

    Returns:
        Dictionary with test account information
    """
    return {
        "account_number": "12345678901",  # Dummy account number
        "account_name": "테스트계좌",
        "account_type": "위탁",
    }


@pytest.fixture
def test_prompts() -> Dict[str, List[str]]:
    """Collection of test prompts for different agent types.

    Returns:
        Dictionary mapping agent types to list of test prompts
    """
    return {
        "account": [
            "내 계좌 잔고를 알려줘",
            "보유종목 목록을 보여줘",
            "오늘 수익률이 어떻게 되나요?",
            "매수가능금액이 얼마인가요?",
            "총자산 현황을 확인하고 싶어",
            "예수금 잔액 조회해줘",
            "포트폴리오 현황 보여줘",
        ],
        "chart": [
            "삼성전자 차트를 보여줘",
            "NAVER 최근 한달 차트 분석해줘",
            "SK하이닉스 일봉 차트 조회",
            "코스피 지수 차트를 보여줘",
            "현대차 주가 시세 확인",
            "LG화학 5분봉 차트 데이터",
            "005930 일봉 데이터 가져와줘",
        ],
        "market_info": [
            "삼성전자 기업정보를 알려줘",
            "LG화학 재무제표 보여줘",
            "최근 공시 내역을 확인하고 싶어",
            "배당금 지급일이 언제인가요?",
            "현대차 실적 발표 언제야?",
            "NAVER 시가총액 얼마인가요?",
        ],
        "etf": [
            "KODEX 200 정보를 알려줘",
            "반도체 ETF 추천해줘",
            "ETF 수익률 순위를 보여줘",
            "인버스 ETF 종류가 뭐가 있나요?",
            "TIGER 2차전지테마 수익률은?",
            "섹터별 ETF 추천해줘",
            "레버리지 ETF 위험성 알려줘",
        ],
        "theme_sector": [
            "반도체 관련주를 알려줘",
            "바이오 섹터 상승률 TOP 10",
            "AI 테마주 추천해줘",
            "자동차 업종 시황은 어때?",
            "게임주 관련 종목들 보여줘",
            "2차전지 테마 대장주는?",
            "메타버스 관련주 현황은?",
        ],
    }


@pytest.fixture
def complex_test_prompts() -> List[str]:
    """Complex prompts that might contain multiple intents or be ambiguous.

    Returns:
        List of complex test prompts
    """
    return [
        "삼성전자 차트 보고 매수 결정하고 싶은데 계좌 잔고도 확인해줘",
        "반도체 테마 ETF 추천하고 차트도 같이 보여줘",
        "포트폴리오에서 손실 나는 종목들 차트 분석해줘",
        "AI 관련주 중에서 기업정보 좋은 곳 추천해줘",
        "최근 공시 나온 종목들 중 차트 좋은 것 찾아줘",
        "배당주 ETF와 개별 배당주 중 어떤 게 좋을까?",
        "코스닥 바이오 섹터에서 가장 전망 좋은 종목은?",
    ]


@pytest.fixture
def mock_specialized_agents():
    """Mock specialized agents for testing router functionality.

    Returns:
        Dictionary of mock agents for each agent type
    """
    agents = {}

    for agent_type in ["account", "chart", "market_info", "etf", "theme_sector"]:
        mock_agent = Mock()
        mock_agent.process_request.return_value = {
            "agent_type": agent_type,
            "result": f"Mock result from {agent_type} agent",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_agent._format_response.return_value = f"Formatted response from {agent_type} agent"
        agents[agent_type] = mock_agent

    return agents


@pytest.fixture
def performance_thresholds() -> Dict[str, float]:
    """Performance thresholds for integration tests.

    Returns:
        Dictionary with performance thresholds
    """
    return {
        "classification_time_max": 5.0,  # seconds
        "routing_time_max": 10.0,  # seconds
        "end_to_end_time_max": 15.0,  # seconds
        "classification_accuracy_min": 0.8,  # 80% minimum accuracy
        "confidence_threshold": 0.7,  # Minimum confidence for high-confidence classifications
    }


@pytest.fixture
def api_rate_limits() -> Dict[str, float]:
    """API rate limiting configuration.

    Returns:
        Dictionary with rate limiting settings
    """
    return {
        "kiwoom_requests_per_second": 5,  # Kiwoom API rate limit
        "openai_requests_per_minute": 60,  # OpenAI API rate limit
        "delay_between_requests": 0.2,  # seconds
    }


# Skip markers for different test categories
pytestmark = [
    pytest.mark.integration,  # Mark all tests in this module as integration tests
]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test requiring API keys")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_auth: mark test as requiring authentication")
