from src.research_assistant.utils.rag_pipeline import PDFQA
from src.research_assistant.core.state_manager import ResearchState
from typing import Dict, Any,List
from src.research_assistant.core.logger import logger
from langsmith import traceable #type: ignore
@traceable(
    name="execution_node",
    metadata={"node_type": "execution", "version": "1.0"}
)
async def rag_node(state: ResearchState) -> ResearchState:

    logger.info("RAG Node: Starting retrieval-augmented generation process.")

    fused = state["fused_results"]

    if not fused:
        logger.warning("RAG Node: No fused results available.")
        state["rag_context"] = []
        state["rag_retriever"] = None
        return state

    try:
        combined_text: str = "\n\n".join(item["content"] for item in fused)
        pdf_qa = PDFQA(combined_text)

    except Exception as e:
        logger.error(f"Failed to initialize PDFQA: {e}")
        state["rag_context"] = []
        state["rag_retriever"] = None
        return state

    retriever = pdf_qa.retriever

    if not state["query"]:
        logger.warning("RAG Node: Query is empty or None.")
        state["rag_context"] = []
        state["rag_retriever"] = retriever
        return state

    try:
        retrieved_docs = retriever.invoke(state["query"]) # type: ignore

        rag_context: List[Dict[str, Any]] = [
            {
                "content": d.page_content, # type: ignore
                "metadata": d.metadata #type: ignore
            }
            for d in retrieved_docs #type: ignore
        ]

        state["rag_context"] = rag_context
        state["rag_retriever"] = retriever
        return state

    except Exception as e:
        logger.error(f"RAG retrieval failed for query '{state['query']}': {e}")
        state["rag_context"] = []
        state["rag_retriever"] = retriever
        return state