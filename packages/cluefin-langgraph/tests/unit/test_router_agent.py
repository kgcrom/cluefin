"""Unit tests for KiwoomRouterAgent."""

import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest
from cluefin_langgraph.agents.kiwoom.routing.router_agent import (
    KiwoomRouterAgent,
    RouterState,
)
from cluefin_langgraph.agents.kiwoom.routing.routing_types import (
    AgentType,
    IntentClassification,
    RoutingResponse,
)


class TestKiwoomRouterAgent:
    """Test cases for KiwoomRouterAgent."""

    @pytest.fixture
    def mock_kiwoom_client(self):
        """Mock Kiwoom client for testing."""
        return Mock()

    @pytest.fixture
    def mock_llm(self):
        """Mock language model for testing."""
        return Mock()

    @pytest.fixture
    def mock_classification(self):
        """Mock intent classification result."""
        return IntentClassification(
            agent_type=AgentType.ACCOUNT,
            confidence=0.9,
            reasoning="Account balance request",
            extracted_params={"account_number": "12345678"},
        )

    @pytest.fixture
    def mock_agent_response(self):
        """Mock agent response."""
        return {"total_asset": 10000000, "deposit": 2000000, "stock_value": 8000000, "profit_loss": 500000}

    @pytest.fixture
    def router_agent(self, mock_kiwoom_client, mock_llm):
        """Create KiwoomRouterAgent instance for testing."""
        with (
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.account_agent",
                AccountAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.chart_agent",
                ChartAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.market_info_agent",
                MarketInfoAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.etf_agent",
                ETFAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.theme_sector_agent",
                ThemeSectorAgent=Mock,
            ),
        ):
            return KiwoomRouterAgent(mock_kiwoom_client, mock_llm, verbose=True)

    def test_initialization(self, router_agent):
        """Test router agent initialization."""
        assert router_agent.kiwoom_client is not None
        assert router_agent.llm is not None
        assert router_agent.classifier is not None
        assert len(router_agent.agents) == 5
        assert AgentType.ACCOUNT in router_agent.agents
        assert AgentType.CHART in router_agent.agents

    def test_agent_initialization(self, router_agent):
        """Test that all specialized agents are initialized."""
        expected_agent_types = {
            AgentType.ACCOUNT,
            AgentType.CHART,
            AgentType.MARKET_INFO,
            AgentType.ETF,
            AgentType.THEME_SECTOR,
        }

        assert set(router_agent.agents.keys()) == expected_agent_types

    def test_classify_intent_success(self, router_agent, mock_classification):
        """Test successful intent classification."""
        router_agent.classifier.classify = Mock(return_value=mock_classification)

        state: RouterState = {
            "user_prompt": "내 계좌 잔고를 알려줘",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._classify_intent(state)

        assert result["classification"] == mock_classification
        assert result["error"] is None
        router_agent.classifier.classify.assert_called_once_with("내 계좌 잔고를 알려줘")

    def test_classify_intent_error(self, router_agent):
        """Test intent classification error handling."""
        router_agent.classifier.classify = Mock(side_effect=Exception("Classification error"))

        state: RouterState = {
            "user_prompt": "test prompt",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._classify_intent(state)

        assert result["classification"] is None
        assert "Intent classification failed" in result["error"]

    def test_route_to_agent_success(self, router_agent, mock_classification, mock_agent_response):
        """Test successful routing to specialized agent."""
        # Mock the account agent
        mock_account_agent = Mock()
        mock_account_agent.process_request.return_value = mock_agent_response
        router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

        state: RouterState = {
            "user_prompt": "내 계좌 잔고를 알려줘",
            "classification": mock_classification,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._route_to_agent(state)

        assert result["agent_response"] == mock_agent_response
        assert result["error"] is None
        mock_account_agent.process_request.assert_called_once_with(
            "내 계좌 잔고를 알려줘", {"account_number": "12345678"}
        )

    def test_route_to_agent_missing_agent(self, router_agent, mock_classification):
        """Test routing when specified agent is not available."""
        # Remove the account agent
        del router_agent.agents[AgentType.ACCOUNT]

        state: RouterState = {
            "user_prompt": "내 계좌 잔고를 알려줘",
            "classification": mock_classification,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._route_to_agent(state)

        assert result["agent_response"] is None
        assert "No agent available for type" in result["error"]

    def test_route_to_agent_processing_error(self, router_agent, mock_classification):
        """Test agent processing error handling."""
        # Mock the account agent to raise an exception
        mock_account_agent = Mock()
        mock_account_agent.process_request.side_effect = Exception("Agent error")
        router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

        state: RouterState = {
            "user_prompt": "내 계좌 잔고를 알려줘",
            "classification": mock_classification,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._route_to_agent(state)

        assert result["agent_response"] is None
        assert "Agent processing failed" in result["error"]

    def test_should_route_or_error_with_error(self, router_agent):
        """Test conditional routing when error exists."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": "Some error",
        }

        result = router_agent._should_route_or_error(state)

        assert result == "error"

    def test_should_route_or_error_without_classification(self, router_agent):
        """Test conditional routing when classification is missing."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._should_route_or_error(state)

        assert result == "error"

    def test_should_route_or_error_success(self, router_agent, mock_classification):
        """Test conditional routing with successful classification."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": mock_classification,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._should_route_or_error(state)

        assert result == "route"

    def test_format_final_response_with_error(self, router_agent):
        """Test final response formatting when error exists."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": "Test error",
        }

        result = router_agent._format_final_response(state)

        assert "오류가 발생했습니다" in result["final_response"]
        assert "Test error" in result["final_response"]

    def test_format_final_response_success(self, router_agent, mock_classification, mock_agent_response):
        """Test final response formatting with successful response."""
        # Mock the account agent's format method
        mock_account_agent = Mock()
        mock_account_agent._format_response.return_value = "Formatted response"
        router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

        state: RouterState = {
            "user_prompt": "test",
            "classification": mock_classification,
            "agent_response": mock_agent_response,
            "final_response": None,
            "error": None,
        }

        result = router_agent._format_final_response(state)

        assert result["final_response"] == "Formatted response"
        mock_account_agent._format_response.assert_called_once_with(mock_agent_response)

    def test_format_final_response_no_response(self, router_agent):
        """Test final response formatting when no agent response."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        result = router_agent._format_final_response(state)

        assert result["final_response"] == "요청을 처리할 수 없습니다."

    def test_handle_error(self, router_agent):
        """Test error handling."""
        state: RouterState = {
            "user_prompt": "test",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": "Test error",
        }

        result = router_agent._handle_error(state)

        # Should pass through unchanged
        assert result == state

    def test_process_success(self, router_agent, mock_classification, mock_agent_response):
        """Test synchronous processing success."""
        # Mock the workflow components
        with patch.object(router_agent, "classifier") as mock_classifier:
            mock_classifier.classify.return_value = mock_classification

            mock_account_agent = Mock()
            mock_account_agent.process_request.return_value = mock_agent_response
            mock_account_agent._format_response.return_value = "Formatted response"
            router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

            result = router_agent.process("내 계좌 잔고를 알려줘")

            assert isinstance(result, RoutingResponse)
            assert result.agent_type == AgentType.ACCOUNT
            assert result.classification == mock_classification
            assert result.result == mock_agent_response
            assert result.formatted_response == "Formatted response"

    def test_process_error(self, router_agent):
        """Test synchronous processing with error."""
        # Mock the classifier to raise an exception
        with patch.object(router_agent, "classifier") as mock_classifier:
            mock_classifier.classify.side_effect = Exception("Classification error")

            result = router_agent.process("test prompt")

            assert isinstance(result, RoutingResponse)
            assert result.agent_type == AgentType.ACCOUNT  # Default on error
            assert result.classification.confidence == 0.0
            assert "error" in result.result
            assert "오류가 발생했습니다" in result.formatted_response

    @pytest.mark.asyncio
    async def test_aprocess_success(self, router_agent, mock_classification, mock_agent_response):
        """Test asynchronous processing success."""
        # Mock the workflow components
        with patch.object(router_agent, "classifier") as mock_classifier:
            mock_classifier.classify.return_value = mock_classification

            mock_account_agent = Mock()
            mock_account_agent.process_request.return_value = mock_agent_response
            mock_account_agent._format_response.return_value = "Formatted response"
            router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

            result = await router_agent.aprocess("내 계좌 잔고를 알려줘")

            assert isinstance(result, RoutingResponse)
            assert result.agent_type == AgentType.ACCOUNT
            assert result.classification == mock_classification
            assert result.result == mock_agent_response
            assert result.formatted_response == "Formatted response"

    @pytest.mark.asyncio
    async def test_aprocess_error(self, router_agent):
        """Test asynchronous processing with error."""
        # Mock the classifier to raise an exception
        with patch.object(router_agent, "classifier") as mock_classifier:
            mock_classifier.classify.side_effect = Exception("Classification error")

            result = await router_agent.aprocess("test prompt")

            assert isinstance(result, RoutingResponse)
            assert result.agent_type == AgentType.ACCOUNT  # Default on error
            assert result.classification.confidence == 0.0
            assert "error" in result.result
            assert "오류가 발생했습니다" in result.formatted_response

    def test_verbose_logging(self, mock_kiwoom_client, mock_llm, mock_classification):
        """Test verbose logging functionality."""
        with (
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.account_agent",
                AccountAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.chart_agent",
                ChartAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.market_info_agent",
                MarketInfoAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.etf_agent",
                ETFAgent=Mock,
            ),
            patch.multiple(
                "cluefin_langgraph.agents.kiwoom.specialized.theme_sector_agent",
                ThemeSectorAgent=Mock,
            ),
        ):
            verbose_router = KiwoomRouterAgent(mock_kiwoom_client, mock_llm, verbose=True)

            with patch("loguru.logger.info") as mock_logger_info:
                verbose_router.classifier.classify = Mock(return_value=mock_classification)

                state: RouterState = {
                    "user_prompt": "내 계좌 잔고를 알려줘",
                    "classification": None,
                    "agent_response": None,
                    "final_response": None,
                    "error": None,
                }

                verbose_router._classify_intent(state)

                # Should have logged classification info
                assert mock_logger_info.call_count >= 1
                call_args = str(mock_logger_info.call_args_list)
                assert "Classifying intent" in call_args
                assert "Classified as" in call_args

    def test_different_agent_types_routing(self, router_agent):
        """Test routing to different agent types."""
        agent_types_and_prompts = [
            (AgentType.ACCOUNT, "내 계좌 잔고"),
            (AgentType.CHART, "삼성전자 차트"),
            (AgentType.MARKET_INFO, "LG화학 기업정보"),
            (AgentType.ETF, "KODEX 200 정보"),
            (AgentType.THEME_SECTOR, "반도체 관련주"),
        ]

        for agent_type, prompt in agent_types_and_prompts:
            classification = IntentClassification(
                agent_type=agent_type, confidence=0.9, reasoning=f"Test {agent_type.value}", extracted_params={}
            )

            # Mock the specific agent
            mock_agent = Mock()
            mock_agent.process_request.return_value = {"test": "response"}
            router_agent.agents[agent_type] = mock_agent

            state: RouterState = {
                "user_prompt": prompt,
                "classification": classification,
                "agent_response": None,
                "final_response": None,
                "error": None,
            }

            result = router_agent._route_to_agent(state)

            assert result["agent_response"] == {"test": "response"}
            assert result["error"] is None
            mock_agent.process_request.assert_called_once()

    def test_graph_compilation(self, router_agent):
        """Test that the LangGraph workflow compiles successfully."""
        assert router_agent.graph is not None

        # Test that we can get the graph structure
        assert hasattr(router_agent.graph, "invoke")
        assert hasattr(router_agent.graph, "ainvoke")

    def test_state_transitions(self, router_agent, mock_classification, mock_agent_response):
        """Test complete state transitions through the workflow."""
        # Mock all components
        router_agent.classifier.classify = Mock(return_value=mock_classification)

        mock_account_agent = Mock()
        mock_account_agent.process_request.return_value = mock_agent_response
        mock_account_agent._format_response.return_value = "Final formatted response"
        router_agent.agents[AgentType.ACCOUNT] = mock_account_agent

        initial_state: RouterState = {
            "user_prompt": "내 계좌 잔고를 알려줘",
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }

        # Test each step individually
        # Step 1: Classification
        state = router_agent._classify_intent(initial_state.copy())
        assert state["classification"] == mock_classification

        # Step 2: Routing decision
        decision = router_agent._should_route_or_error(state)
        assert decision == "route"

        # Step 3: Route to agent
        state = router_agent._route_to_agent(state)
        assert state["agent_response"] == mock_agent_response

        # Step 4: Format response
        state = router_agent._format_final_response(state)
        assert state["final_response"] == "Final formatted response"
