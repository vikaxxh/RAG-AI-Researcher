from fastapi import APIRouter,HTTPException,Depends,Request
from src.research_assistant.schemas.research_model import ResearchAssistantRequest,ResearchAssistantResponse
# from src.research_assistant.utils.agentic_research import run_agentic_research
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
from src.research_assistant.utils.agentic_research import Research_Assistant
from src.research_assistant.guardrails.guardrails_validator import Guardrails_check
from langsmith import traceable


router = APIRouter(tags=["Agentic Research Assistant"])

guardrails_checker = Guardrails_check()

@traceable(name = "API_hit_point")
@router.post("/research_chat", response_model=ResearchAssistantResponse)
async def query_topic(
    request_data: ResearchAssistantRequest,
    request: Request
) -> ResearchAssistantResponse:
    
    if not request_data.query.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

   
    # ✅ Validate input using Guardrails
    try:
        error_msg, validated_query = Guardrails_check().safety_check(request_data.query)
            
        # Check if validation passed
        if error_msg:
            return ResearchAssistantResponse(
                query=request_data.query,
                error=error_msg,
                is_abusive=True
            )
        
        # validated_query is already set from safety_check, no need to reassign
            
    except Exception as guard_error:
        # Guardrails validation failed with exception
        print(f"Guard validation error: {guard_error}")
        return ResearchAssistantResponse(
            query=request_data.query,
            error="Your input contains unsafe or disallowed content. Please rephrase your question.",
            is_abusive=True
        )
    
    # ✅ Run research assistant with validated input
    try:
        if validated_query:
            assistant = Research_Assistant(query = validated_query)
            final_output = await assistant.run_agentic_research()

            return ResearchAssistantResponse(
                query=final_output["query"],
                final_output=final_output["final_output"],
                sources=final_output["sources"],
                is_abusive=False
            )
        
        else:
            raise HTTPException(status_code =500, detail = "Validated_query not passed into the research_Assistant")
    
    except Exception as research_error:
        print(f"Research assistant error: {research_error}")
        return ResearchAssistantResponse(
            query=request_data.query,
            error="An error occurred while processing your research request. Please try again.",
            is_abusive=False
        )
    
    
    















# router = APIRouter(tags = ["Agentic Research Assistant"])
# # security = HTTPBearer()

# @router.post("/research_chat", response_model= ResearchAssistantResponse)
# async def query_topic(
#     request: ResearchAssistantRequest,
#     # credentials: HTTPAuthorizationCredentials = Depends(security)
# ) -> ResearchAssistantResponse:
#     # api_key = credentials.credentials  # Extracts token from "Bearer <token>"

#     # if not api_key.strip():
#     #     raise HTTPException(status_code=400, detail="API key cannot be empty")

#     if not request.query.strip():
#         raise HTTPException(status_code = 400, detail = "Topic cannot be empty")

#     try:
#         assistant = Research_Assistant(query = request.query)
#         final_output = await assistant.run_agentic_research()  # dict with all sections

#         # ✅ Return as structured JSON

#         return {
#             "query": final_output["query"],
#             "final_output": final_output["final_output"],
#             "sources": final_output["sources"],
#             # "fused_results": final_output["fused_results"],
#             # "rag_context": final_output["rag_context"],
#             # "critic": final_output["critic"]
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing the topic: {str(e)}")
