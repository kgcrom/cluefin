"""Integration tests for KiwoomRouterAgent.

These tests verify the complete end-to-end workflow of the router agent,
including intent classification, agent routing, and response formatting.
"""

import asyncio
import time
from typing import Any, Dict
from unittest.mock import patch

import pytest
from cluefin_langgraph.agents.kiwoom.routing.router_agent import KiwoomRouterAgent
from cluefin_langgraph.agents.kiwoom.routing.routing_types import AgentType
from cluefin_openapi.kiwoom import Client as KiwoomClient
from langchain_core.language_models.base import BaseLanguageModel
from loguru import logger


@pytest.mark.integration
@pytest.mark.requires_auth
class TestRouterAgentEndToEnd:
    """End-to-end workflow tests for router agent."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent with real dependencies."""
        return KiwoomRouterAgent(kiwoom_client=kiwoom_client, llm=openai_llm, verbose=True)

    @pytest.mark.parametrize(
        "prompt,expected_agent,test_params",
        [
            # Account agent workflows
            ("내 계좌 잔고 좀 보여줘", AgentType.ACCOUNT, {}),
            ("삼성전자 100주 매수 가능한지 확인해줘", AgentType.ACCOUNT, {"stock_code": "005930", "quantity": 100}),
            ("오늘 매매한 거래 내역 조회해줘", AgentType.ACCOUNT, {}),
            # Chart agent workflows
            ("삼성전자 일봉 차트 데이터 가져와줘", AgentType.CHART, {"stock_code": "005930"}),
            ("SK하이닉스 최근 1개월 차트 보여줘", AgentType.CHART, {"stock_code": "000660"}),
            ("005930 5분봉 차트 데이터 필요해", AgentType.CHART, {"stock_code": "005930", "time_frame": "5분"}),
            # Market info agent workflows
            ("현재 코스피 지수 알려줘", AgentType.MARKET_INFO, {}),
            ("오늘 거래량 상위 종목 뭐야?", AgentType.MARKET_INFO, {}),
            ("삼성전자 현재가 얼마야?", AgentType.MARKET_INFO, {"stock_code": "005930"}),
            # ETF agent workflows
            ("KODEX 200 ETF 정보 알려줘", AgentType.ETF, {"etf_name": "KODEX 200"}),
            ("반도체 ETF 추천해줘", AgentType.ETF, {"sector": "반도체"}),
            ("ETF 수익률 순위 보여줘", AgentType.ETF, {}),
            # Theme agent workflows
            ("2차전지 관련주 뭐가 있어?", AgentType.THEME, {"theme": "2차전지"}),
            ("AI 테마주 추천해줘", AgentType.THEME, {"theme": "AI"}),
            ("오늘 상승률 높은 섹터 알려줘", AgentType.THEME, {}),
        ],
    )
    def test_end_to_end_workflow(
        self,
        router_agent: KiwoomRouterAgent,
        prompt: str,
        expected_agent: AgentType,
        test_params: Dict[str, Any],
        measure_performance: callable,
    ):
        """Test complete workflow from prompt to final response."""
        start_time = time.time()

        # Process the prompt
        response = router_agent.process(prompt)

        elapsed_time = time.time() - start_time

        # Verify classification
        assert response.agent_type == expected_agent, f"Expected {expected_agent}, got {response.agent_type}"
        assert response.classification.confidence >= 0.5, f"Low confidence: {response.classification.confidence}"

        # Verify parameter extraction
        extracted_params = response.classification.extracted_params
        for key, expected_value in test_params.items():
            if key == "stock_code":
                # Stock codes might be extracted in different formats
                assert key in extracted_params or extracted_params.get("symbol") == expected_value, (
                    f"Missing or incorrect {key}"
                )
            else:
                assert extracted_params.get(key) == expected_value, (
                    f"Expected {key}={expected_value}, got {extracted_params.get(key)}"
                )

        # Verify response formatting
        assert response.formatted_response is not None
        assert len(response.formatted_response) > 0
        assert "오류" not in response.formatted_response or prompt == "잘못된 요청"

        # Log performance metrics
        logger.info(f"Workflow completed in {elapsed_time:.2f}s for: {prompt[:30]}...")
        measure_performance("end_to_end_workflow", elapsed_time)

        # Performance assertion
        assert elapsed_time < 10.0, f"Workflow took too long: {elapsed_time:.2f}s"

    @pytest.mark.asyncio
    async def test_async_workflow(self, router_agent: KiwoomRouterAgent, measure_performance: callable):
        """Test asynchronous processing capabilities."""
        prompts = [
            "내 계좌 잔고 보여줘",
            "삼성전자 차트 데이터",
            "코스피 지수 현황",
            "KODEX 200 ETF 정보",
            "AI 테마주 추천",
        ]

        start_time = time.time()

        # Process all prompts concurrently
        tasks = [router_agent.aprocess(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)

        elapsed_time = time.time() - start_time

        # Verify all responses
        assert len(responses) == len(prompts)
        for response, prompt in zip(responses, prompts, strict=False):
            assert response.formatted_response is not None
            assert response.classification is not None
            logger.info(f"Async processed: {prompt} -> {response.agent_type}")

        # Log performance
        avg_time = elapsed_time / len(prompts)
        logger.info(f"Async batch completed in {elapsed_time:.2f}s (avg: {avg_time:.2f}s per request)")
        measure_performance("async_batch_processing", elapsed_time)

        # Performance assertion - should be faster than sequential
        assert elapsed_time < len(prompts) * 3.0, f"Async processing too slow: {elapsed_time:.2f}s"


@pytest.mark.integration
@pytest.mark.requires_auth
class TestAgentRouting:
    """Test agent routing and inter-agent communication."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent with mocked specialized agents for testing."""
        agent = KiwoomRouterAgent(kiwoom_client=kiwoom_client, llm=openai_llm, verbose=True)
        return agent

    def test_correct_agent_routing(self, router_agent: KiwoomRouterAgent):
        """Verify requests are routed to correct agents."""
        test_cases = [
            ("계좌 잔고 조회", AgentType.ACCOUNT),
            ("차트 데이터 필요", AgentType.CHART),
            ("시장 현황 알려줘", AgentType.MARKET_INFO),
            ("ETF 정보 조회", AgentType.ETF),
            ("테마주 추천", AgentType.THEME),
        ]

        for prompt, expected_agent in test_cases:
            response = router_agent.process(prompt)
            assert response.agent_type == expected_agent, (
                f"Prompt '{prompt}' routed to {response.agent_type}, expected {expected_agent}"
            )
            logger.info(f"✓ '{prompt}' correctly routed to {expected_agent}")

    def test_agent_state_management(self, router_agent: KiwoomRouterAgent):
        """Test state management across agent transitions."""
        # Process multiple requests in sequence
        prompts = ["삼성전자 현재가 조회", "삼성전자 100주 매수 가능?", "삼성전자 차트 보여줘"]

        responses = []
        for prompt in prompts:
            response = router_agent.process(prompt)
            responses.append(response)

            # Verify state is clean for each request
            assert response.classification is not None
            assert response.formatted_response is not None

        # Verify different agents were used
        agent_types = [r.agent_type for r in responses]
        assert AgentType.MARKET_INFO in agent_types
        assert AgentType.ACCOUNT in agent_types
        assert AgentType.CHART in agent_types

        logger.info(f"State management verified across agents: {agent_types}")

    def test_agent_response_formatting(self, router_agent: KiwoomRouterAgent):
        """Test that each agent formats responses correctly."""
        test_prompts = {
            AgentType.ACCOUNT: "계좌 잔고",
            AgentType.CHART: "차트 데이터",
            AgentType.MARKET_INFO: "시장 현황",
            AgentType.ETF: "ETF 정보",
            AgentType.THEME: "테마주",
        }

        for agent_type, prompt in test_prompts.items():
            response = router_agent.process(prompt)

            # Verify formatting
            assert response.formatted_response is not None
            assert isinstance(response.formatted_response, str)
            assert len(response.formatted_response) > 0

            # Check for Korean formatting
            assert any(ord(c) > 127 for c in response.formatted_response), "Response should contain Korean characters"

            logger.info(f"✓ {agent_type} formatting verified")


@pytest.mark.integration
@pytest.mark.requires_auth
class TestErrorHandling:
    """Test error handling and recovery scenarios."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent for error testing."""
        return KiwoomRouterAgent(kiwoom_client=kiwoom_client, llm=openai_llm, verbose=True)

    def test_invalid_prompt_handling(self, router_agent: KiwoomRouterAgent):
        """Test handling of invalid or ambiguous prompts."""
        invalid_prompts = [
            "",  # Empty prompt
            "askdfjhaslkdfj",  # Gibberish
            "안녕하세요",  # Greeting (not a financial request)
            "1 + 1 = ?",  # Math question
        ]

        for prompt in invalid_prompts:
            response = router_agent.process(prompt)

            # Should not crash
            assert response is not None
            assert response.formatted_response is not None

            # Should have low confidence or error
            if response.classification:
                assert response.classification.confidence < 0.8, f"High confidence for invalid prompt: {prompt}"

            logger.info(f"Handled invalid prompt: '{prompt[:20]}...'")

    @patch("cluefin_langgraph.agents.kiwoom.routing.router_agent.IntentClassifier.classify")
    def test_classification_failure_recovery(self, mock_classify, router_agent: KiwoomRouterAgent):
        """Test recovery from classification failures."""
        # Simulate classification failure
        mock_classify.side_effect = Exception("Classification service unavailable")

        response = router_agent.process("삼성전자 현재가")

        # Should handle gracefully
        assert response is not None
        assert response.formatted_response is not None
        assert "오류" in response.formatted_response

        logger.info("Classification failure handled gracefully")

    def test_api_failure_handling(self, router_agent: KiwoomRouterAgent):
        """Test handling of API failures."""
        with patch.object(router_agent.kiwoom_client.account, "get_balance") as mock_api:
            # Simulate API failure
            mock_api.side_effect = Exception("API connection failed")

            response = router_agent.process("계좌 잔고 조회")

            # Should handle API failure
            assert response is not None
            assert response.formatted_response is not None

            # Check for error indication
            if "오류" not in response.formatted_response:
                # Some agents might handle errors differently
                assert response.result is not None

            logger.info("API failure handled")

    def test_timeout_handling(self, router_agent: KiwoomRouterAgent):
        """Test handling of timeouts."""
        with patch.object(router_agent.classifier, "classify") as mock_classify:
            # Simulate slow classification
            def slow_classify(*args, **kwargs):
                time.sleep(0.5)  # Simulate delay
                from cluefin_langgraph.agents.kiwoom.routing.routing_types import IntentClassification

                return IntentClassification(
                    agent_type=AgentType.ACCOUNT, confidence=0.9, reasoning="Test", extracted_params={}
                )

            mock_classify.side_effect = slow_classify

            start_time = time.time()
            response = router_agent.process("계좌 잔고")
            elapsed = time.time() - start_time

            # Should complete despite delay
            assert response is not None
            assert elapsed < 2.0, "Should not hang indefinitely"

            logger.info(f"Timeout scenario handled in {elapsed:.2f}s")


@pytest.mark.integration
@pytest.mark.requires_auth
class TestConcurrency:
    """Test concurrent request handling."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent for concurrency testing."""
        return KiwoomRouterAgent(
            kiwoom_client=kiwoom_client,
            llm=openai_llm,
            verbose=False,  # Reduce logging for concurrent tests
        )

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, router_agent: KiwoomRouterAgent, measure_performance: callable):
        """Test handling multiple concurrent requests."""
        # Create diverse prompts to test different agents
        prompts = [
            "삼성전자 현재가",
            "계좌 잔고 조회",
            "코스피 지수",
            "SK하이닉스 차트",
            "KODEX 200 정보",
            "AI 테마주",
            "LG화학 거래량",
            "내 보유 종목",
            "네이버 일봉 차트",
            "반도체 섹터 현황",
        ]

        start_time = time.time()

        # Process all concurrently
        tasks = [router_agent.aprocess(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        elapsed_time = time.time() - start_time

        # Analyze results
        successful = sum(1 for r in responses if not isinstance(r, Exception))
        failed = len(responses) - successful

        logger.info(f"Concurrent processing: {successful}/{len(prompts)} successful in {elapsed_time:.2f}s")

        # At least 80% should succeed
        assert successful >= len(prompts) * 0.8, f"Too many failures: {failed}/{len(prompts)}"

        # Should be faster than sequential processing
        avg_time = elapsed_time / len(prompts)
        assert avg_time < 2.0, f"Concurrent processing too slow: {avg_time:.2f}s per request"

        measure_performance("concurrent_10_requests", elapsed_time)

    @pytest.mark.asyncio
    async def test_load_test(self, router_agent: KiwoomRouterAgent, measure_performance: callable):
        """Test system under load with many requests."""
        # Generate 50 random prompts
        base_prompts = [
            "삼성전자 {action}",
            "SK하이닉스 {action}",
            "LG화학 {action}",
            "네이버 {action}",
            "카카오 {action}",
        ]
        actions = ["현재가", "차트", "거래량", "시가", "종가"]

        prompts = []
        for base in base_prompts:
            for action in actions:
                prompts.append(base.format(action=action))

        # Add some account and market prompts
        prompts.extend(["계좌 잔고", "보유 종목", "코스피 지수", "코스닥 지수", "거래량 순위"] * 2)

        logger.info(f"Starting load test with {len(prompts)} requests")

        start_time = time.time()

        # Process in batches to avoid overwhelming the system
        batch_size = 10
        all_responses = []

        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            tasks = [router_agent.aprocess(prompt) for prompt in batch]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            all_responses.extend(responses)

            # Small delay between batches
            if i + batch_size < len(prompts):
                await asyncio.sleep(0.1)

        elapsed_time = time.time() - start_time

        # Analyze results
        successful = sum(1 for r in all_responses if not isinstance(r, Exception))
        throughput = len(prompts) / elapsed_time

        logger.info(f"Load test: {successful}/{len(prompts)} successful")
        logger.info(f"Throughput: {throughput:.2f} requests/second")
        logger.info(f"Total time: {elapsed_time:.2f}s")

        measure_performance("load_test_50_requests", elapsed_time)
        measure_performance("throughput_requests_per_second", throughput)

        # Performance assertions
        assert successful >= len(prompts) * 0.7, "Too many failures under load"
        assert throughput > 1.0, f"Throughput too low: {throughput:.2f} req/s"


@pytest.mark.integration
@pytest.mark.requires_auth
@pytest.mark.skip(reason="Requires live API - run manually with real credentials")
class TestRealAPIIntegration:
    """Test with real Kiwoom API calls (requires valid credentials)."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent with real API client."""
        return KiwoomRouterAgent(kiwoom_client=kiwoom_client, llm=openai_llm, verbose=True)

    def test_real_account_balance(self, router_agent: KiwoomRouterAgent):
        """Test real account balance retrieval."""
        response = router_agent.process("내 계좌 잔고 조회해줘")

        assert response is not None
        assert response.agent_type == AgentType.ACCOUNT
        assert response.formatted_response is not None
        assert "잔고" in response.formatted_response or "계좌" in response.formatted_response

        # Check for actual data in response
        if response.result and isinstance(response.result, dict):
            # Should have some account data structure
            assert len(response.result) > 0

        logger.info("Real account balance retrieved successfully")

    def test_real_stock_price(self, router_agent: KiwoomRouterAgent):
        """Test real stock price retrieval."""
        response = router_agent.process("삼성전자 현재가 얼마야?")

        assert response is not None
        assert response.agent_type == AgentType.MARKET_INFO
        assert response.formatted_response is not None

        # Should contain price information
        assert any(char.isdigit() for char in response.formatted_response)

        logger.info(f"Real stock price: {response.formatted_response[:100]}...")

    def test_real_chart_data(self, router_agent: KiwoomRouterAgent):
        """Test real chart data retrieval."""
        response = router_agent.process("삼성전자 일봉 차트 데이터 가져와")

        assert response is not None
        assert response.agent_type == AgentType.CHART
        assert response.formatted_response is not None

        # Should have chart data
        if response.result:
            assert isinstance(response.result, (dict, list))

        logger.info("Real chart data retrieved successfully")

    def test_rate_limiting(self, router_agent: KiwoomRouterAgent):
        """Test API rate limiting handling."""
        prompts = ["삼성전자 현재가", "SK하이닉스 현재가", "LG화학 현재가", "네이버 현재가", "카카오 현재가"]

        responses = []
        for prompt in prompts:
            response = router_agent.process(prompt)
            responses.append(response)
            time.sleep(0.2)  # Small delay to respect rate limits

        # All should complete without rate limit errors
        successful = sum(1 for r in responses if r.formatted_response and "오류" not in r.formatted_response)
        assert successful == len(prompts), f"Rate limiting issues: {successful}/{len(prompts)} successful"

        logger.info("Rate limiting handled successfully")


@pytest.mark.integration
class TestPerformanceMetrics:
    """Collect and verify performance metrics."""

    @pytest.fixture
    def router_agent(self, kiwoom_client: KiwoomClient, openai_llm: BaseLanguageModel) -> KiwoomRouterAgent:
        """Create router agent for performance testing."""
        return KiwoomRouterAgent(kiwoom_client=kiwoom_client, llm=openai_llm, verbose=False)

    def test_classification_performance(self, router_agent: KiwoomRouterAgent, measure_performance: callable):
        """Measure classification performance."""
        prompts = ["계좌 잔고", "삼성전자 차트", "코스피 지수", "KODEX ETF", "AI 테마주"] * 5  # Repeat for average

        times = []
        for prompt in prompts:
            start = time.time()

            # Just classify, don't process
            router_agent.classifier.classify(prompt)

            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)

        logger.info("Classification performance:")
        logger.info(f"  Average: {avg_time:.3f}s")
        logger.info(f"  Min: {min_time:.3f}s")
        logger.info(f"  Max: {max_time:.3f}s")

        measure_performance("classification_avg_time", avg_time)

        # Performance assertions
        assert avg_time < 2.0, f"Classification too slow: {avg_time:.3f}s"
        assert max_time < 5.0, f"Max classification time too high: {max_time:.3f}s"

    def test_end_to_end_performance(self, router_agent: KiwoomRouterAgent, measure_performance: callable):
        """Measure end-to-end performance for different agent types."""
        test_cases = [
            ("계좌 잔고 조회", AgentType.ACCOUNT),
            ("삼성전자 차트", AgentType.CHART),
            ("코스피 현황", AgentType.MARKET_INFO),
            ("KODEX 200", AgentType.ETF),
            ("AI 테마주", AgentType.THEME),
        ]

        metrics = {}

        for prompt, agent_type in test_cases:
            times = []

            # Run multiple times for average
            for _ in range(3):
                start = time.time()
                router_agent.process(prompt)
                elapsed = time.time() - start
                times.append(elapsed)

            avg_time = sum(times) / len(times)
            metrics[agent_type.value] = avg_time

            logger.info(f"{agent_type.value}: {avg_time:.3f}s average")
            measure_performance(f"e2e_{agent_type.value}", avg_time)

        # Overall performance assertion
        overall_avg = sum(metrics.values()) / len(metrics)
        assert overall_avg < 3.0, f"Overall performance too slow: {overall_avg:.3f}s"

        logger.info(f"Overall average: {overall_avg:.3f}s")
