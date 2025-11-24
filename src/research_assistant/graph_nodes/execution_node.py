from src.research_assistant.core.logger import logger
from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.agents.arxiv_agent import ArxivAgent
from src.research_assistant.agents.tavily_search_agent import TavilyAgent
from src.research_assistant.agents.wikipedia_agent import WikipediaAgent
from langsmith import traceable #type: ignore
import asyncio


@traceable(
    name="execution_node",
    metadata={"node_type": "execution", "version": "1.0"}
)
async def execution_node(state: ResearchState) -> ResearchState:
    """Executes the plan: searches each source using agents"""
    logger.info("⚙️ Starting execution...")
    
    plan = state.get("planning", [])
    logger.info(f"Planning in Execution node{plan}")
    
    # Initialize results
    state["tavily_results"] = []
    state["wikipedia_results"] = []
    state["arxiv_results"] = []
    
    # ========================================
    # OPTIMIZED: Run all searches in parallel
    # ========================================
    
    # Determine which sources to search from plan
    sources_to_search = set()
    for step in plan:
        if step.get("action") == "search":
            sources_to_search.add(step.get("source"))
    
    # Create tasks for parallel execution
    tasks = []
    
    if "tavily" in sources_to_search:
        logger.info("🔍 Queuing Tavily search...")
        tasks.append(("tavily", TavilyAgent().search_web(state["query"])))
    
    if "wikipedia" in sources_to_search:
        logger.info("🔍 Queuing Wikipedia search...")
        tasks.append(("wikipedia", WikipediaAgent().search_wikipedia(state["query"])))
    
    if "arxiv" in sources_to_search:
        logger.info("🔍 Queuing ArXiv search...")
        tasks.append(("arxiv", ArxivAgent().search_papers(state["query"])))
    
    # Run all searches in parallel
    if tasks:
        logger.info(f"⚡ Running {len(tasks)} searches in parallel...")
        
        # Execute all tasks simultaneously
        results = await asyncio.gather(
            *[task for _, task in tasks],
            return_exceptions=True  # Don't fail if one agent errors
        )
        
        # Process results
        for (source, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                logger.error(f"❌ Failed to search {source}: {result}")
                continue
            
            if source == "tavily":
                state["tavily_results"] = result
                logger.info(f"✓ Tavily search completed: {len(result)} results")
            elif source == "wikipedia":
                state["wikipedia_results"] = result
                logger.info(f"✓ Wikipedia search completed: {len(result)} results")
            elif source == "arxiv":
                state["arxiv_results"] = result
                logger.info(f"✓ ArXiv search completed: {len(result)} results")
    
    # Handle fusion markers
    for step in plan:
        if step.get("action") == "fusion":
            logger.info("🔗 Fusion step marker - will be handled by fusion_node")
    
    logger.info("✅ Execution completed")
    
    return state

