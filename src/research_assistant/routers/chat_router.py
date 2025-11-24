from fastapi import APIRouter,HTTPException,Depends
from src.research_assistant.schemas.research_model import ResearchAssistantRequest,ResearchAssistantResponse
# from src.research_assistant.utils.agentic_research import run_agentic_research
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
from src.research_assistant.utils.agentic_research import Research_Assistant



router = APIRouter(tags = ["Agentic Research Assistant"])
# security = HTTPBearer()

@router.post("/research_chat", response_model= ResearchAssistantResponse)
async def query_topic(
    request: ResearchAssistantRequest,
    # credentials: HTTPAuthorizationCredentials = Depends(security)
) -> ResearchAssistantResponse:
    # api_key = credentials.credentials  # Extracts token from "Bearer <token>"

    # if not api_key.strip():
    #     raise HTTPException(status_code=400, detail="API key cannot be empty")

    if not request.query.strip():
        raise HTTPException(status_code = 400, detail = "Topic cannot be empty")

    try:
        assistant = Research_Assistant(query = request.query)
        final_output = await assistant.run_agentic_research()  # dict with all sections

        # ✅ Return as structured JSON

        return {
            "query": final_output["query"],
            "final_output": final_output["final_output"],
            "sources": final_output["sources"],
            # "fused_results": final_output["fused_results"],
            # "rag_context": final_output["rag_context"],
            # "critic": final_output["critic"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the topic: {str(e)}")
