from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.agents.LLM_critic_agent import LLMCriticAgent
from src.research_assistant.core.logger import logger
from src.research_assistant.utils.llm_client import get_critic_llm_client
from langsmith import traceable  # type: ignore


@traceable(
    name="critic_node",
    metadata={"node_type": "Critics", "version": "1.0"}
)
async def critic_node(state: ResearchState) -> ResearchState:
    try:
        critic = LLMCriticAgent(get_critic_llm_client())
        
    
        replan_count = state.get("replan_count", 0)
        if replan_count >= 1:
            state["critic_decision"] = "ACCEPT"
            return state

        raw = await critic.review(
            answer=state["final_answer"],
            context=state["rag_context"]
        )

        logger.info(f"Raw critic output: {raw}")

        if "ACCEPT" in raw.upper():
            decision = "ACCEPT"
        else:
            decision = "REPLAN"
            state["replan_count"] = replan_count + 1

        state["critic_decision"] = decision

    except Exception as e:
        state["critic_decision"] = "REPLAN"
        raise e
    
    return state
        

