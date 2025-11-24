from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict, total=True):
    #User Query
    query: str
    
    #Results from reasoning node
    reasoning: Dict[str, Any]  
    strategy: str              
    sources: List[str]

    #Results from Planning
    planning: list[dict[str, str]]   
             
    #Results from execution
    wikipedia_results: List[Dict[str, Any]]
    arxiv_results: List[Dict[str, Any]]
    tavily_results: List[Dict[str, Any]]

    #Results from fusion
    fused_results: List[Dict[str, Any]]

    #Results from RAG
    rag_context: List[Dict[str, Any]]
    rag_retriever: Any

    #Memory
    memory: Any

    critic_decision: str

    replan_count:int
    
    ##Results from LLM
    final_answer: str