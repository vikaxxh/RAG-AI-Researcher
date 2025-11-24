from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.core.logger import logger
from langsmith import traceable #type: ignore


@traceable(
    name="fusion_node",
    metadata={"node_type": "output_fusion", "version": "1.0"}
)
async def fusion_node(state: ResearchState) -> ResearchState:
    """Fuses results from tavily, wikipedia, and arxiv"""
    logger.info("🔗 Starting fusion...")
    
    state["fused_results"] = []

    # Fuse Tavily results
    tavily_results = state.get("tavily_results", [])
    for item in tavily_results:
        state["fused_results"].append({
            "content": item["summary"],
            "metadata": {
                "id": item["id"],
                "source": item["source"],
                "title": item["title"],
                "url": item["url"]
            }
        })
    
    # Fuse Wikipedia results
    wikipedia_results = state.get("wikipedia_results", [])
    for item in wikipedia_results:
        state["fused_results"].append({
            "content": item["summary"],
            "metadata": {
                "id": item["id"],
                "source": item["source"],
                "title": item["title"],
            }
        })

    # Fuse ArXiv results
    arxiv_results = state.get("arxiv_results", [])
    for item in arxiv_results:
        state["fused_results"].append({
            "content": item["summary"],
            "metadata": {
                "id": item["id"],
                "source": item["source"],
                "title": item["title"],
                "authors": item["authors"],
                "published": item["published"],
                "url": item["url"]
            }
        })
    
    logger.info(f"✅ Fusion completed: {len(tavily_results)} tavily + {len(wikipedia_results)} wikipedia + {len(arxiv_results)} arxiv = {len(state['fused_results'])} total")
    
    return state