from langgraph.graph import StateGraph, END #type: ignore
from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.graph_nodes.reasoning_node import reasoning_node
from src.research_assistant.graph_nodes.planning_node import planning_node
from src.research_assistant.graph_nodes.execution_node import execution_node
from src.research_assistant.graph_nodes.fusion_node import fusion_node
from src.research_assistant.graph_nodes.rag_node import rag_node
from src.research_assistant.graph_nodes.llm_synthesis_node import llm_synthesizer_node
from src.research_assistant.graph_nodes.critic_node import critic_node

def create_research_workflow() -> StateGraph: #type: ignore
    
    # Initialize the graph with state
    workflow = StateGraph(ResearchState)
    
    # Add all nodes
    workflow.add_node("reasoning", reasoning_node)  #type: ignore
    workflow.add_node("planning", planning_node)  #type: ignore
    workflow.add_node("execution", execution_node)  #type: ignore
    workflow.add_node("fusion", fusion_node)  #type: ignore
    workflow.add_node("rag", rag_node)  #type: ignore
    workflow.add_node("llm_synthesizer", llm_synthesizer_node)#type: ignore
    workflow.add_node("critic",critic_node) #type: ignore
    
    # Define the flow (edges)
    workflow.set_entry_point("reasoning") 
    workflow.add_edge("reasoning", "planning")    
    workflow.add_edge("planning", "execution")    
    workflow.add_edge("execution", "fusion")      
    workflow.add_edge("fusion", "rag")            
    workflow.add_edge("rag", "llm_synthesizer")                              
    workflow.add_edge("llm_synthesizer", "critic")

    workflow.add_conditional_edges(
    "critic",
    lambda out: out["critic_decision"],   
    {
        "ACCEPT": END,
        "REPLAN": "planning",             
    }
    )          
    
    return workflow.compile() #type: ignore
    
