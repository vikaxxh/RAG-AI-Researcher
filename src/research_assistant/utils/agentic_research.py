from typing import Dict, Any
from src.research_assistant.graph_builder import create_research_workflow #type: ignore
from src.research_assistant.core.state_manager import ResearchState


class Research_Assistant():

    def __init__(self, query:str) -> None:
        self.query = query

    async def run_agentic_research(self) -> Dict[str, Any]:
    
        app = create_research_workflow()

    
        initial_state: ResearchState = {
        "query": self.query
        }

        result_state = await app.ainvoke(initial_state)

        

        return {
            "final_output": result_state["final_answer"],
            "query": self.query,
            "sources": result_state.get("sources",[]),
            "fused_results": result_state.get("fused_results", []),
            "rag_context": result_state.get("rag_context", []),
            "critic" : result_state.get("critic_decision",[])
        }



