from src.research_assistant.core.logger import logger
from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.utils.query_analyser import analyse_query
from langsmith import traceable #type: ignore

@traceable(
    name="reasoning_node",
    metadata={"node_type": "reasoning", "version": "1.0"}
)
async def reasoning_node(state: ResearchState) -> ResearchState:

    logger.info("🧠 Starting reasoning...")

    try:
        result = analyse_query(state['query'])
        state["reasoning"] = result 
        state["strategy"] = result["strategy"] 
        state["sources"] = result["sources"]

    except Exception as e:
        raise ValueError(f"Reasoning node failed {e}")
  
    logger.info("✅ Reasoning completed")
    
    return state

