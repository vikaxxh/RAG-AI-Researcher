from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.core.logger import logger
from typing import List,Dict,Any 
from langsmith import traceable #type: ignore

@traceable(
    name="planning_node",
    metadata={"node_type": "planning", "version": "1.0"}
)
async def planning_node(state: ResearchState) -> ResearchState:
    """Creates a simple plan based on strategy"""
    logger.info("📌 Starting planning...")
    
    strategy = state.get("strategy", "auto")
    sources = state.get("sources", [])
    query = state.get("query", "")
    
    plan:List[Dict[str,Any]] = []
    
    # Step 1: Decide search order based on strategy
    if strategy == "tavily_first":
        # Search tavily first, then arxiv
        for source in ["tavily", "arxiv"]:
            if source in sources:
                plan.append({
                    "action": "search",
                    "source": source,
                    "query": query
                })
    
    elif strategy == "wikipedia_first":
        # Search wikipedia first, then arxiv
        for source in ["wikipedia", "arxiv"]:
            if source in sources:
                plan.append({
                    "action": "search",
                    "source": source,
                    "query": query
                })
    
    elif strategy == "arxiv_focus":
        # Search arxiv first, then others
        if "arxiv" in sources:
            plan.append({
                "action": "search",
                "source": "arxiv",
                "query": query
            })
        for source in sources:
            if source != "arxiv":
                plan.append({
                    "action": "search",
                    "source": source,
                    "query": query
                })
    
    elif strategy == "both":
        # Search all sources (order doesn't matter much)
        for source in sources:
            plan.append({
                "action": "search",
                "source": source,
                "query": query
            })
    
    else:  # auto
        # Just search in the order they appear
        for source in sources:
            plan.append({
                "action": "search",
                "source": source,
                "query": query
            })
    
    # Step 2: Add fusion step at the end
    plan.append({
        "action": "fusion",
        "sources": sources
    })
    
    state["planning"] = plan
    
    logger.info(f"📝 Plan created with strategy '{strategy}'")
    logger.info(f"   Will search: {[step['source'] for step in plan if step['action'] == 'search']}")
    
    return state
