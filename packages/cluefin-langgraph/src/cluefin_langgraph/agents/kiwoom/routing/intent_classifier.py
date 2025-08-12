"""Intent classifier for Kiwoom agent routing."""

import json
from typing import Dict, List, Optional

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.prompts import PromptTemplate

from ..routing.routing_types import AGENT_METADATA, AgentType, IntentClassification


def _standardize_params(raw_params: Dict[str, str]) -> Dict[str, str]:
    """Standardize parameter names to match test expectations.

    Args:
        raw_params: Raw parameters from LLM extraction

    Returns:
        Standardized parameters with consistent naming
    """
    standardized = {}

    # Define mappings from Korean/alternate names to standard names
    param_mappings = {
        # Stock-related parameters
        "종목명": "stock_name",
        "종목코드": "stock_code",
        "symbol": "stock_code",
        "ticker": "stock_code",
        "매수수량": "quantity",
        "수량": "quantity",
        "주수": "quantity",
        # ETF-related parameters
        "ETF명": "etf_name",
        "etf명": "etf_name",
        # Theme/Sector parameters
        "테마": "theme",
        "섹터": "sector",
        "테마/섹터": lambda v: {"theme": v}
        if any(keyword in v for keyword in ["AI", "2차전지", "바이오", "게임"])
        else {"sector": v},
        # Time frame parameters
        "시간프레임": "time_frame",
        "차트타입": "chart_type",
    }

    for key, value in raw_params.items():
        if key in param_mappings:
            mapping = param_mappings[key]
            if callable(mapping):
                # Special handling for complex mappings
                result = mapping(value)
                standardized.update(result)
            else:
                standardized[mapping] = value
        else:
            # Keep unknown parameters as-is
            standardized[key] = value

    # Special handling for quantities - extract numeric values
    if "quantity" in standardized:
        import re

        quantity_str = standardized["quantity"]
        numbers = re.findall(r"\d+", str(quantity_str))
        if numbers:
            standardized["quantity"] = int(numbers[0])

    # Convert stock names to stock codes when possible
    if "stock_name" in standardized and "stock_code" not in standardized:
        known_stocks = {
            "삼성전자": "005930",
            "SK하이닉스": "000660",
            "NAVER": "035420",
            "네이버": "035420",
            "LG화학": "051910",
            "현대차": "005380",
            "현대자동차": "005380",
        }
        stock_name = standardized["stock_name"]
        if stock_name in known_stocks:
            standardized["stock_code"] = known_stocks[stock_name]

    return standardized


class IntentClassifier:
    """Classifies user intent to route to appropriate Kiwoom agent.

    This classifier uses both LLM-based analysis and keyword matching
    to determine the most appropriate agent for handling a user request.
    """

    def __init__(self, llm: BaseLanguageModel):
        """Initialize the intent classifier.

        Args:
            llm: Language model for intent classification
        """
        self.llm = llm
        self.classification_prompt = self._build_classification_prompt()
        self.keyword_classifier = KeywordBasedClassifier()

    def classify(self, user_prompt: str) -> IntentClassification:
        """Classify user prompt to determine appropriate agent.

        Args:
            user_prompt: Natural language prompt from user

        Returns:
            Intent classification with agent type and confidence
        """
        # First try LLM-based classification
        llm_classification = self._llm_classify(user_prompt)

        # Get keyword-based classification for validation
        keyword_classification = self.keyword_classifier.classify(user_prompt)

        # If LLM classification has high confidence, use it
        if llm_classification.confidence >= 0.8:
            return llm_classification

        # If keyword classification matches LLM with decent confidence, boost confidence
        if (
            keyword_classification
            and keyword_classification.agent_type == llm_classification.agent_type
            and llm_classification.confidence >= 0.5
        ):
            llm_classification.confidence = min(llm_classification.confidence + 0.2, 1.0)
            return llm_classification

        # If LLM confidence is low but keyword match is strong, use keyword result
        if keyword_classification and llm_classification.confidence < 0.5:
            return keyword_classification

        # Otherwise, return LLM classification as-is
        return llm_classification

    def _build_classification_prompt(self) -> PromptTemplate:
        """Build the prompt template for classification.

        Returns:
            Prompt template for LLM classification
        """
        # Build agent descriptions from metadata
        agent_descriptions = []
        for agent_type, metadata in AGENT_METADATA.items():
            examples = "\n   ".join(f"- {ex}" for ex in metadata.examples[:3])
            agent_descriptions.append(
                f"{agent_type.value.upper()}: {metadata.description}\n"
                f"   키워드: {', '.join(metadata.keywords[:5])}\n"
                f"   예시:\n   {examples}"
            )

        agent_info = "\n\n".join(agent_descriptions)

        template = """다음 사용자 요청을 분석하여 가장 적절한 Kiwoom 에이전트로 분류해주세요.

사용 가능한 에이전트:
{agent_info}

사용자 요청: {user_prompt}

다음 형식의 JSON으로 응답해주세요:
{{
    "agent_type": "선택된 에이전트 타입 (account, chart, market_info, etf, theme_sector 중 하나)",
    "confidence": 0.0-1.0 사이의 확신도,
    "reasoning": "분류 근거 설명",
    "extracted_params": {{
        "파라미터명": "추출된 값"
    }}
}}

중요 고려사항:
1. 요청의 핵심 의도를 파악하세요
2. 여러 에이전트가 가능한 경우, 가장 주요한 의도에 맞는 것을 선택하세요
3. 파라미터 추출 시 다음 표준 이름을 사용해주세요:
   - 종목명/종목코드: "stock_code" (예: "005930"), "stock_name" (예: "삼성전자")
   - 수량: "quantity" (예: 100)
   - ETF명: "etf_name" (예: "KODEX 200")
   - 섹터: "sector" (예: "반도체")
   - 테마: "theme" (예: "AI", "2차전지")
   - 시간프레임: "time_frame" (예: "5분", "일봉")
4. 확신도는 요청의 명확성과 에이전트 매칭 정도를 반영해주세요"""

        return PromptTemplate(
            template=template, input_variables=["user_prompt"], partial_variables={"agent_info": agent_info}
        )

    def _llm_classify(self, user_prompt: str) -> IntentClassification:
        """Classify using LLM.

        Args:
            user_prompt: User's natural language prompt

        Returns:
            Classification result from LLM
        """
        try:
            # Format the prompt
            prompt = self.classification_prompt.format(user_prompt=user_prompt)

            # Get LLM response
            response = self.llm.invoke(prompt)

            # Parse JSON response
            if hasattr(response, "content"):
                content = response.content
            else:
                content = str(response)

            # Extract JSON from response
            classification_data = self._extract_json(content)

            # Map string to AgentType enum
            agent_type_str = classification_data.get("agent_type", "account").lower()
            agent_type = self._map_to_agent_type(agent_type_str)

            # Standardize extracted parameters
            raw_params = classification_data.get("extracted_params", {})
            standardized_params = _standardize_params(raw_params)

            return IntentClassification(
                agent_type=agent_type,
                confidence=float(classification_data.get("confidence", 0.5)),
                reasoning=classification_data.get("reasoning", ""),
                extracted_params=standardized_params,
            )

        except Exception as e:
            # Fallback classification
            return IntentClassification(
                agent_type=AgentType.ACCOUNT,
                confidence=0.0,
                reasoning=f"Classification error: {str(e)}",
                extracted_params={},
            )

    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from LLM response text.

        Args:
            text: LLM response text

        Returns:
            Parsed JSON data
        """
        # Try to find JSON in the text
        start_idx = text.find("{")
        end_idx = text.rfind("}")

        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx : end_idx + 1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Fallback
        return {
            "agent_type": "account",
            "confidence": 0.5,
            "reasoning": "Failed to parse JSON response",
            "extracted_params": {},
        }

    def _map_to_agent_type(self, agent_type_str: str) -> AgentType:
        """Map string to AgentType enum.

        Args:
            agent_type_str: String representation of agent type

        Returns:
            Corresponding AgentType enum value
        """
        mapping = {
            "account": AgentType.ACCOUNT,
            "chart": AgentType.CHART,
            "market_info": AgentType.MARKET_INFO,
            "etf": AgentType.ETF,
            "theme_sector": AgentType.THEME_SECTOR,
        }

        return mapping.get(agent_type_str.lower(), AgentType.ACCOUNT)


class KeywordBasedClassifier:
    """Keyword-based classifier for fallback and validation.

    This classifier uses predefined keywords to quickly identify
    the most likely agent type for a given prompt.
    """

    def __init__(self):
        """Initialize the keyword classifier."""
        self.keyword_mapping = self._build_keyword_mapping()

    def _build_keyword_mapping(self) -> Dict[AgentType, List[str]]:
        """Build keyword mapping from agent metadata.

        Returns:
            Dictionary mapping agent types to keywords
        """
        mapping = {}
        for agent_type, metadata in AGENT_METADATA.items():
            mapping[agent_type] = metadata.keywords
        return mapping

    def classify(self, user_prompt: str) -> Optional[IntentClassification]:
        """Classify based on keyword matching.

        Args:
            user_prompt: User's natural language prompt

        Returns:
            Classification result if keywords match strongly
        """
        prompt_lower = user_prompt.lower()
        scores = {}

        # Calculate keyword match scores for each agent type
        for agent_type, keywords in self.keyword_mapping.items():
            score = 0
            matched_keywords = []

            for keyword in keywords:
                if keyword.lower() in prompt_lower:
                    score += 1
                    matched_keywords.append(keyword)

            if score > 0:
                scores[agent_type] = (score, matched_keywords)

        # If no keywords match, return None
        if not scores:
            return None

        # Find the agent type with highest score
        best_agent = max(scores.items(), key=lambda x: x[1][0])
        agent_type, (score, matched_keywords) = best_agent

        # Calculate confidence based on number of matches
        confidence = min(0.3 + (score * 0.2), 0.9)

        return IntentClassification(
            agent_type=agent_type,
            confidence=confidence,
            reasoning=f"Keyword matches: {', '.join(matched_keywords)}",
            extracted_params=_standardize_params(self._extract_basic_params(user_prompt)),
        )

    def _extract_basic_params(self, user_prompt: str) -> Dict[str, str]:
        """Extract basic parameters from prompt.

        Args:
            user_prompt: User's natural language prompt

        Returns:
            Dictionary of extracted parameters
        """
        params = {}

        # Extract numbers (could be quantities, prices, etc.)
        import re

        numbers = re.findall(r"\d+", user_prompt)
        if numbers:
            # Simple heuristic: first number might be quantity
            if any(word in user_prompt.lower() for word in ["주", "개", "매수", "매도"]):
                params["quantity"] = numbers[0]

        # Extract stock codes (6-digit numbers)
        stock_codes = re.findall(r"\b\d{6}\b", user_prompt)
        if stock_codes:
            params["stock_code"] = stock_codes[0]

        # Extract well-known stock names
        known_stocks = {
            "삼성전자": "005930",
            "SK하이닉스": "000660",
            "NAVER": "035420",
            "네이버": "035420",
            "LG화학": "051910",
            "현대차": "005380",
            "현대자동차": "005380",
        }

        for name, code in known_stocks.items():
            if name in user_prompt:
                params["stock_name"] = name
                params["stock_code"] = code
                break

        return params
