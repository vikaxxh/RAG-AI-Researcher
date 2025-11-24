from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.core.logger import logger
from src.research_assistant.utils.llm_client import get_llm_client_rag
from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_classic.chains.combine_documents import create_stuff_documents_chain #type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langsmith import traceable #type: ignore

@traceable(
    name="synthesis",
    metadata={"node_type": "synthesis_output", "version": "1.0"}
)
async def llm_synthesizer_node(state: ResearchState) -> ResearchState:
    
    retriever = state["rag_retriever"]
    if retriever is None:
        logger.warning("LLM Synthesizer: No retriever available.")
        state["final_answer"] = "No retriever available. Unable to generate answer."
        state["rag_context"] = []
        return state

    # Validate query exists
    if not state["query"]:
        logger.warning("LLM Synthesizer: Query is empty or None.")
        state["final_answer"] = "No query provided."
        state["rag_context"] = []
        return state

    # Load your LLM
    try:
        llm = get_llm_client_rag()  
    except Exception as e:
        logger.error(f"LLM initialization failed: {e}")
        state["final_answer"] = "LLM initialization failed. Unable to generate answer."
        state["rag_context"] = []
        return state


    contextualize_prompt = ChatPromptTemplate.from_messages([ #type: ignore
    ("system",
     "Given the chat history and the latest user question, "
     "reformulate it as a standalone question that can be understood without the chat history. "
     "Do NOT answer the question, only reformulate it if needed. "
     "If it's already standalone, return it unchanged."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

    try:
        history_aware_retriever = create_history_aware_retriever(
            llm,
            retriever,
            contextualize_prompt
        )
    except Exception as e:
        logger.error(f"Failed to create history-aware retriever: {e}")
        state["final_answer"] = "Failed to create retriever chain."
        state["rag_context"] = []
        return state


    # ENHANCED QA Prompt with query-type awareness
    qa_prompt = ChatPromptTemplate.from_messages([ #type: ignore
        ("system",
        """You are a knowledgeable research assistant. Use the retrieved context to generate a comprehensive, accurate response.

    **Retrieved Context:**
    {context}

    **Instructions:**

    1. **For "What is" or "Define" queries:**
    - Provide a clear, concise definition
    - Include key characteristics
    - Give 2-3 brief examples
    - Keep response to 2-3 paragraphs

    2. **For "Explain" queries:**
    - Start with a clear definition
    - Explain how it works or why it matters
    - Provide 3-5 concrete examples with details
    - Include real-world applications or use cases
    - Structure with clear sections (use bullet points for examples)
    - Aim for comprehensive but readable response

    3. **For "Compare" or "Difference" queries:**
    - Create clear comparisons
    - Use structured format (tables or bullet points)
    - Highlight key similarities and differences

    4. **General Rules:**
    - Base your answer ONLY on the retrieved context
    - If context is insufficient, acknowledge limitations
    - Be accurate - avoid hallucinations or speculation
    - Cite specific details from the context
    - Use clear, accessible language
    - If the context contains contradictions, mention them

    5. **Response Quality:**
    - Prioritize clarity and accuracy over length
    - Use examples to illustrate abstract concepts
    - Structure information logically
    - For technical topics, explain jargon when first used"""),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    try:
        document_chain = create_stuff_documents_chain(
            llm=llm,
            prompt=qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            document_chain
        )
    except Exception as e:
        logger.error(f"Failed to create RAG chain: {e}")
        state["final_answer"] = "Failed to create answer generation chain."
        state["rag_context"] = []
        return state

 
    # Convert memory to proper format for chat_history
    chat_history = []
    if "memory" in state and state["memory"] is not None:
        if hasattr(state["memory"], "chat_memory"):
            # Extract messages from BufferMemory or similar
            chat_history = state["memory"].chat_memory.messages if hasattr(state["memory"].chat_memory, "messages") else [] #type: ignore
        elif hasattr(state["memory"], "messages"):
            chat_history = state["memory"].messages

 
    try:
        response = rag_chain.invoke({
            "input": state["query"],
            "chat_history": chat_history
        })

        final_answer = response.get("answer", "No answer generated.")
        retrieved_docs = response.get("context", [])

        # Convert retrieved docs to consistent format
        rag_context = [    #type: ignore
            {
                "content": doc.page_content if hasattr(doc, "page_content") else str(doc),
                "metadata": doc.metadata if hasattr(doc, "metadata") else {}
            }
            for doc in retrieved_docs
        ]

        logger.info(f"LLM Synthesizer: Successfully generated answer for query: {state['query'][:50]}...")

        state["final_answer"] = final_answer
        state["rag_context"] = rag_context
        return state

    except Exception as e:
        logger.error(f"RAG chain invocation failed: {e}")
        state["final_answer"] = f"Failed to generate answer: {str(e)}"
        state["rag_context"] = []
        return state