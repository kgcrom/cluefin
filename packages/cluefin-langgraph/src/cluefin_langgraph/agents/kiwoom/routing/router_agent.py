"""Main router agent for Kiwoom agent system."""

from typing import Any, Dict, Optional, TypedDict

from langchain_core.language_models.base import BaseLanguageModel
from langgraph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from cluefin_openapi.kiwoom import Client as KiwoomClient

from ..routing.intent_classifier import IntentClassifier
from ..routing.routing_types import (
    AgentType,
    IntentClassification,
    RoutingRequest,
    RoutingResponse,
)


class RouterState(TypedDict):
    """State definition for the router workflow."""
    
    user_prompt: str
    classification: Optional[IntentClassification]
    agent_response: Optional[Any]
    final_response: Optional[str]
    error: Optional[str]


class KiwoomRouterAgent:
    """Main router agent that directs requests to specialized agents.
    
    This agent analyzes user prompts, classifies intent, and routes
    the request to the appropriate specialized agent for processing.
    """
    
    def __init__(
        self,
        kiwoom_client: KiwoomClient,
        llm: BaseLanguageModel,
        verbose: bool = False,
    ):
        """Initialize the router agent.
        
        Args:
            kiwoom_client: Authenticated Kiwoom API client
            llm: Language model for intent classification
            verbose: Enable verbose logging
        """
        self.kiwoom_client = kiwoom_client
        self.llm = llm
        self.verbose = verbose
        self.classifier = IntentClassifier(llm)
        self.agents = self._initialize_agents()
        self.graph = self._build_graph()
    
    def _initialize_agents(self) -> Dict[AgentType, Any]:
        """Initialize all specialized agents.
        
        Returns:
            Dictionary mapping agent types to agent instances
        """
        # Import specialized agents to avoid circular imports
        from ..specialized.account_agent import AccountAgent
        from ..specialized.chart_agent import ChartAgent
        from ..specialized.market_info_agent import MarketInfoAgent
        from ..specialized.etf_agent import ETFAgent
        from ..specialized.theme_sector_agent import ThemeSectorAgent
        
        agents = {
            AgentType.ACCOUNT: AccountAgent(self.kiwoom_client, self.llm, self.verbose),
            AgentType.CHART: ChartAgent(self.kiwoom_client, self.llm, self.verbose),
            AgentType.MARKET_INFO: MarketInfoAgent(self.kiwoom_client, self.llm, self.verbose),
            AgentType.ETF: ETFAgent(self.kiwoom_client, self.llm, self.verbose),
            AgentType.THEME_SECTOR: ThemeSectorAgent(self.kiwoom_client, self.llm, self.verbose),
        }
        
        return agents
    
    def _build_graph(self) -> CompiledStateGraph:
        """Build the LangGraph workflow.
        
        Returns:
            Compiled state graph for routing workflow
        """
        # Create workflow
        workflow = StateGraph(RouterState)
        
        # Add nodes
        workflow.add_node("classify", self._classify_intent)
        workflow.add_node("route_to_agent", self._route_to_agent)
        workflow.add_node("format_response", self._format_final_response)
        workflow.add_node("handle_error", self._handle_error)
        
        # Add edges
        workflow.set_entry_point("classify")
        
        # Conditional routing based on classification success
        workflow.add_conditional_edges(
            "classify",
            self._should_route_or_error,
            {
                "route": "route_to_agent",
                "error": "handle_error",
            }
        )
        
        workflow.add_edge("route_to_agent", "format_response")
        workflow.add_edge("handle_error", "format_response")
        workflow.set_finish_point("format_response")
        
        return workflow.compile()
    
    def _should_route_or_error(self, state: RouterState) -> str:
        """Decide whether to route to agent or handle error.
        
        Args:
            state: Current router state
            
        Returns:
            "route" or "error" based on classification result
        """
        if state.get("error") or not state.get("classification"):
            return "error"
        return "route"
    
    def _classify_intent(self, state: RouterState) -> RouterState:
        """Classify user intent from prompt.
        
        Args:
            state: Current router state
            
        Returns:
            Updated state with classification
        """
        try:
            if self.verbose:
                print(f"Classifying intent for: {state['user_prompt']}")
            
            classification = self.classifier.classify(state["user_prompt"])
            state["classification"] = classification
            
            if self.verbose:
                print(f"Classified as: {classification.agent_type.value} "
                      f"(confidence: {classification.confidence})")
            
        except Exception as e:
            state["error"] = f"Intent classification failed: {str(e)}"
            
        return state
    
    def _route_to_agent(self, state: RouterState) -> RouterState:
        """Route request to appropriate specialized agent.
        
        Args:
            state: Current router state
            
        Returns:
            Updated state with agent response
        """
        try:
            classification = state["classification"]
            agent_type = classification.agent_type
            
            if agent_type not in self.agents:
                state["error"] = f"No agent available for type: {agent_type}"
                return state
            
            agent = self.agents[agent_type]
            
            if self.verbose:
                print(f"Routing to {agent_type.value} agent")
            
            # Process request with the specialized agent
            response = agent.process_request(
                state["user_prompt"],
                classification.extracted_params
            )
            
            state["agent_response"] = response
            
        except Exception as e:
            state["error"] = f"Agent processing failed: {str(e)}"
            
        return state
    
    def _format_final_response(self, state: RouterState) -> RouterState:
        """Format the final response for user presentation.
        
        Args:
            state: Current router state
            
        Returns:
            Updated state with formatted response
        """
        if state.get("error"):
            state["final_response"] = f"오류가 발생했습니다: {state['error']}"
        elif state.get("agent_response"):
            # Get the agent that processed the request
            agent_type = state["classification"].agent_type
            agent = self.agents[agent_type]
            
            # Use agent's formatting method
            formatted = agent._format_response(state["agent_response"])
            state["final_response"] = formatted
        else:
            state["final_response"] = "요청을 처리할 수 없습니다."
            
        return state
    
    def _handle_error(self, state: RouterState) -> RouterState:
        """Handle errors in the routing process.
        
        Args:
            state: Current router state
            
        Returns:
            Updated state with error handling
        """
        if self.verbose:
            print(f"Error occurred: {state.get('error', 'Unknown error')}")
        
        # Error is already set, just pass through
        return state
    
    async def aprocess(self, user_prompt: str) -> RoutingResponse:
        """Asynchronously process a user prompt.
        
        Args:
            user_prompt: Natural language prompt from user
            
        Returns:
            Routing response with results
        """
        initial_state: RouterState = {
            "user_prompt": user_prompt,
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }
        
        # Run the workflow
        result = await self.graph.ainvoke(initial_state)
        
        # Build response
        if result.get("error"):
            # Create error response
            return RoutingResponse(
                agent_type=AgentType.ACCOUNT,  # Default
                classification=IntentClassification(
                    agent_type=AgentType.ACCOUNT,
                    confidence=0.0,
                    reasoning="Error occurred",
                    extracted_params={},
                ),
                result={"error": result["error"]},
                formatted_response=result["final_response"],
            )
        
        return RoutingResponse(
            agent_type=result["classification"].agent_type,
            classification=result["classification"],
            result=result["agent_response"],
            formatted_response=result["final_response"],
        )
    
    def process(self, user_prompt: str) -> RoutingResponse:
        """Synchronously process a user prompt.
        
        Args:
            user_prompt: Natural language prompt from user
            
        Returns:
            Routing response with results
        """
        initial_state: RouterState = {
            "user_prompt": user_prompt,
            "classification": None,
            "agent_response": None,
            "final_response": None,
            "error": None,
        }
        
        # Run the workflow synchronously
        result = self.graph.invoke(initial_state)
        
        # Build response
        if result.get("error"):
            # Create error response
            return RoutingResponse(
                agent_type=AgentType.ACCOUNT,  # Default
                classification=IntentClassification(
                    agent_type=AgentType.ACCOUNT,
                    confidence=0.0,
                    reasoning="Error occurred",
                    extracted_params={},
                ),
                result={"error": result["error"]},
                formatted_response=result["final_response"],
            )
        
        return RoutingResponse(
            agent_type=result["classification"].agent_type,
            classification=result["classification"],
            result=result["agent_response"],
            formatted_response=result["final_response"],
        )