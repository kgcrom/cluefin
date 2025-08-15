"""Integration tests for IntentClassifier with real LLM."""

import time
from typing import Dict, List

import pytest
from cluefin_langgraph.agents.kiwoom.routing.intent_classifier import (
    IntentClassifier,
    KeywordBasedClassifier,
)
from cluefin_langgraph.agents.kiwoom.routing.routing_types import (
    AgentType,
    IntentClassification,
)
from langchain_core.language_models.base import BaseLanguageModel
from loguru import logger


@pytest.mark.integration
@pytest.mark.requires_auth
class TestIntentClassifierIntegration:
    """Integration tests for IntentClassifier with real LLM."""

    @pytest.fixture
    def intent_classifier(self, openai_llm: BaseLanguageModel):
        """Create IntentClassifier with real OpenAI LLM."""
        return IntentClassifier(openai_llm)

    @pytest.fixture
    def keyword_classifier(self):
        """Create KeywordBasedClassifier for comparison."""
        return KeywordBasedClassifier()

    def test_account_prompts_classification(
        self,
        intent_classifier: IntentClassifier,
        test_prompts: Dict[str, List[str]],
        performance_thresholds: Dict[str, float],
    ):
        """Test classification accuracy for account-related prompts."""
        account_prompts = test_prompts["account"]
        results = []

        for prompt in account_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            # Basic assertions
            assert isinstance(classification, IntentClassification)
            assert classification.agent_type == AgentType.ACCOUNT
            assert classification.confidence >= 0.5
            assert elapsed_time < performance_thresholds["classification_time_max"]

            # Add small delay to respect rate limits
            time.sleep(0.1)

        # Calculate accuracy statistics
        correct_classifications = sum(1 for r in results if r["classification"].agent_type == AgentType.ACCOUNT)
        accuracy = correct_classifications / len(results)
        avg_time = sum(r["elapsed_time"] for r in results) / len(results)
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)

        # Performance assertions
        assert accuracy >= performance_thresholds["classification_accuracy_min"]
        assert avg_time < performance_thresholds["classification_time_max"]
        assert avg_confidence > 0.7

        logger.info(
            f"Account prompts - Accur--collect-only -v acy: {accuracy:.2%}, Avg Time: {avg_time:.2f}s, Avg Confidence: {avg_confidence:.2f}"
        )

    def test_chart_prompts_classification(
        self,
        intent_classifier: IntentClassifier,
        test_prompts: Dict[str, List[str]],
        performance_thresholds: Dict[str, float],
    ):
        """Test classification accuracy for chart-related prompts."""
        chart_prompts = test_prompts["chart"]
        results = []

        for prompt in chart_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            # Basic assertions
            assert isinstance(classification, IntentClassification)
            assert classification.agent_type == AgentType.CHART
            assert classification.confidence >= 0.5
            assert elapsed_time < performance_thresholds["classification_time_max"]

            time.sleep(0.1)

        # Performance analysis
        accuracy = sum(1 for r in results if r["classification"].agent_type == AgentType.CHART) / len(results)
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)

        assert accuracy >= performance_thresholds["classification_accuracy_min"]
        assert avg_confidence > 0.7

        logger.info(f"Chart prompts - Accuracy: {accuracy:.2%}, Avg Confidence: {avg_confidence:.2f}")

    def test_market_info_prompts_classification(
        self,
        intent_classifier: IntentClassifier,
        test_prompts: Dict[str, List[str]],
        performance_thresholds: Dict[str, float],
    ):
        """Test classification accuracy for market info prompts."""
        market_info_prompts = test_prompts["market_info"]
        results = []

        for prompt in market_info_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            assert isinstance(classification, IntentClassification)
            assert classification.agent_type == AgentType.MARKET_INFO
            assert classification.confidence >= 0.5
            assert elapsed_time < performance_thresholds["classification_time_max"]

            time.sleep(0.1)

        accuracy = sum(1 for r in results if r["classification"].agent_type == AgentType.MARKET_INFO) / len(results)
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)

        assert accuracy >= performance_thresholds["classification_accuracy_min"]
        assert avg_confidence > 0.7

        logger.info(f"Market info prompts - Accuracy: {accuracy:.2%}, Avg Confidence: {avg_confidence:.2f}")

    def test_etf_prompts_classification(
        self,
        intent_classifier: IntentClassifier,
        test_prompts: Dict[str, List[str]],
        performance_thresholds: Dict[str, float],
    ):
        """Test classification accuracy for ETF-related prompts."""
        etf_prompts = test_prompts["etf"]
        results = []

        for prompt in etf_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            assert isinstance(classification, IntentClassification)
            assert classification.agent_type == AgentType.ETF
            assert classification.confidence >= 0.5
            assert elapsed_time < performance_thresholds["classification_time_max"]

            time.sleep(0.1)

        accuracy = sum(1 for r in results if r["classification"].agent_type == AgentType.ETF) / len(results)
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)

        assert accuracy >= performance_thresholds["classification_accuracy_min"]
        assert avg_confidence > 0.7

        logger.info(f"ETF prompts - Accuracy: {accuracy:.2%}, Avg Confidence: {avg_confidence:.2f}")

    def test_theme_prompts_classification(
        self,
        intent_classifier: IntentClassifier,
        test_prompts: Dict[str, List[str]],
        performance_thresholds: Dict[str, float],
    ):
        """Test classification accuracy for theme prompts."""
        theme_prompts = test_prompts["theme"]
        results = []

        for prompt in theme_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            assert isinstance(classification, IntentClassification)
            assert classification.agent_type == AgentType.THEME
            assert classification.confidence >= 0.5
            assert elapsed_time < performance_thresholds["classification_time_max"]

            time.sleep(0.1)

        accuracy = sum(1 for r in results if r["classification"].agent_type == AgentType.THEME) / len(results)
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)

        assert accuracy >= performance_thresholds["classification_accuracy_min"]
        assert avg_confidence > 0.7

        logger.info(f"Theme prompts - Accuracy: {accuracy:.2%}, Avg Confidence: {avg_confidence:.2f}")

    def test_complex_prompts_handling(
        self,
        intent_classifier: IntentClassifier,
        complex_test_prompts: List[str],
        performance_thresholds: Dict[str, float],
    ):
        """Test handling of complex prompts with multiple intents."""
        results = []

        for prompt in complex_test_prompts:
            start_time = time.time()
            classification = intent_classifier.classify(prompt)
            elapsed_time = time.time() - start_time

            results.append(
                {
                    "prompt": prompt,
                    "classification": classification,
                    "elapsed_time": elapsed_time,
                }
            )

            # For complex prompts, we expect the classifier to pick one primary intent
            assert isinstance(classification, IntentClassification)
            assert classification.agent_type in [
                AgentType.ACCOUNT,
                AgentType.CHART,
                AgentType.MARKET_INFO,
                AgentType.ETF,
                AgentType.THEME,
            ]
            assert classification.confidence >= 0.3  # Lower threshold for complex prompts
            assert elapsed_time < performance_thresholds["classification_time_max"]
            assert len(classification.reasoning) > 0  # Should provide reasoning

            time.sleep(0.1)

        # For complex prompts, we mainly check that classification doesn't fail
        avg_confidence = sum(r["classification"].confidence for r in results) / len(results)
        avg_time = sum(r["elapsed_time"] for r in results) / len(results)

        assert avg_confidence > 0.5  # Should still have reasonable confidence
        assert avg_time < performance_thresholds["classification_time_max"]

        logger.info(f"Complex prompts - Avg Confidence: {avg_confidence:.2f}, Avg Time: {avg_time:.2f}s")

    def test_parameter_extraction_accuracy(self, intent_classifier: IntentClassifier, test_stock_data, test_etf_data):
        """Test accuracy of parameter extraction from prompts."""
        test_cases = [
            {
                "prompt": "삼성전자 100주 매수하고 싶어",
                "expected_params": {"stock_name": "삼성전자", "stock_code": "005930", "quantity": "100"},
                "agent_type": AgentType.ACCOUNT,
            },
            {
                "prompt": "005930 차트를 보여줘",
                "expected_params": {"stock_code": "005930"},
                "agent_type": AgentType.CHART,
            },
            {
                "prompt": "NAVER 기업정보 알려줘",
                "expected_params": {"stock_name": "NAVER", "stock_code": "035420"},
                "agent_type": AgentType.MARKET_INFO,
            },
            {
                "prompt": "KODEX 200 수익률은?",
                "expected_params": {},  # ETF names might not be in basic extraction
                "agent_type": AgentType.ETF,
            },
        ]

        for test_case in test_cases:
            classification = intent_classifier.classify(test_case["prompt"])

            assert classification.agent_type == test_case["agent_type"]

            # Check extracted parameters (relaxed checks since extraction might vary)
            extracted_params = classification.extracted_params
            expected_params = test_case["expected_params"]

            # If we expect stock code extraction, verify it
            if "stock_code" in expected_params:
                assert "stock_code" in extracted_params or any(
                    expected_params["stock_code"] in str(v) for v in extracted_params.values()
                )

            time.sleep(0.1)

        logger.info("Parameter extraction tests completed")

    def test_llm_keyword_classifier_agreement(
        self,
        intent_classifier: IntentClassifier,
        keyword_classifier,
        test_prompts: Dict[str, List[str]],
    ):
        """Test agreement between LLM and keyword-based classification."""
        all_prompts = []
        for agent_type, prompts in test_prompts.items():
            all_prompts.extend([(prompt, AgentType(agent_type)) for prompt in prompts[:3]])  # Take first 3 of each type

        agreement_count = 0
        disagreement_cases = []

        for prompt, _ in all_prompts:
            llm_classification = intent_classifier.classify(prompt)
            keyword_classification = keyword_classifier.classify(prompt)

            if keyword_classification is not None:
                if llm_classification.agent_type == keyword_classification.agent_type:
                    agreement_count += 1
                else:
                    disagreement_cases.append(
                        {
                            "prompt": prompt,
                            "llm_type": llm_classification.agent_type,
                            "keyword_type": keyword_classification.agent_type,
                            "llm_confidence": llm_classification.confidence,
                            "keyword_confidence": keyword_classification.confidence,
                        }
                    )

            time.sleep(0.1)

        total_comparable = len([p for p, _ in all_prompts if keyword_classifier.classify(p[0]) is not None])
        if total_comparable > 0:
            agreement_rate = agreement_count / total_comparable
            logger.info(f"LLM-Keyword agreement rate: {agreement_rate:.2%} ({agreement_count}/{total_comparable})")

            # logger.info some disagreement cases for analysis
            for case in disagreement_cases[:3]:
                logger.info(
                    f"Disagreement: '{case['prompt']}' -> LLM: {case['llm_type']} ({case['llm_confidence']:.2f}), Keyword: {case['keyword_type']} ({case['keyword_confidence']:.2f})"
                )

    @pytest.mark.slow
    def test_classification_consistency(self, intent_classifier: IntentClassifier):
        """Test that the same prompt gets consistent classifications."""
        test_prompt = "내 계좌 잔고를 알려줘"
        classifications = []

        # Run the same classification multiple times
        for _ in range(5):
            classification = intent_classifier.classify(test_prompt)
            classifications.append(classification)
            time.sleep(0.2)  # Respect rate limits

        # Check consistency
        agent_types = [c.agent_type for c in classifications]
        most_common_type = max(set(agent_types), key=agent_types.count)
        consistency_rate = agent_types.count(most_common_type) / len(agent_types)

        assert consistency_rate >= 0.8  # At least 80% consistency

        # Check confidence consistency
        confidences = [c.confidence for c in classifications]
        confidence_std = (
            sum((c - sum(confidences) / len(confidences)) ** 2 for c in confidences) / len(confidences)
        ) ** 0.5

        assert confidence_std < 0.2  # Standard deviation should be low

        logger.info(f"Consistency rate: {consistency_rate:.2%}, Confidence std: {confidence_std:.3f}")

    def test_error_handling_and_fallback(self, intent_classifier: IntentClassifier):
        """Test error handling with invalid or problematic prompts."""
        problematic_prompts = [
            "",  # Empty string
            "   ",  # Whitespace only
            "asdfghjkl qwertyuiop",  # Random characters
            "🚀🚀🚀 이모지만 있는 프롬프트 💎💎💎",  # Emoji-heavy
            "a" * 1000,  # Very long prompt
            "What is the stock price in English?",  # English prompt
        ]

        for prompt in problematic_prompts:
            try:
                classification = intent_classifier.classify(prompt)

                # Should not raise an exception
                assert isinstance(classification, IntentClassification)
                assert classification.agent_type in [
                    AgentType.ACCOUNT,
                    AgentType.CHART,
                    AgentType.MARKET_INFO,
                    AgentType.ETF,
                ]

                # For problematic prompts, confidence might be low
                assert 0.0 <= classification.confidence <= 1.0

            except Exception as e:
                pytest.fail(f"Classification failed for prompt '{prompt}': {str(e)}")

            time.sleep(0.1)

        logger.info("Error handling tests completed successfully")
