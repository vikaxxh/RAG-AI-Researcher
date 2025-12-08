from fastapi import APIRouter,HTTPException
from src.research_assistant.schemas.research_model import ResearchAssistantRequest,ResearchAssistantResponse
from src.research_assistant.utils.agentic_research import Research_Assistant
from src.research_assistant.guardrails.guardrails_validator import Guardrails_check
from langsmith import traceable #type: ignore
from datetime import datetime
from src.research_assistant.core.logger import logger
from typing import Any
from src.research_assistant.core.global_state import state



router = APIRouter(tags=["Agentic Research Assistant"])

guardrails_checker = state.guardrails_model

@router.get("/health")
async def health_check() -> dict[str,Any]:
  
    return {
        "status": "healthy",
        "service": "research-assistant",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/")
async def root() -> dict[str, Any]:
 
    return {
        "message": "Agentic Research Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "research": "/research_chat",
            "docs": "/docs"
        }
    }


@traceable(name="API_hit_point")
@router.post("/research_chat", response_model=ResearchAssistantResponse)
async def query_topic(
    request_data: ResearchAssistantRequest,
) -> ResearchAssistantResponse:
    
    if not request_data.query.strip():
        logger.warning("Empty query received")  
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    try:
        error_msg, validated_query = Guardrails_check().safety_check(request_data.query)
          
        if error_msg:
            logger.warning(f"Guardrails blocked query: {error_msg}") 
            return ResearchAssistantResponse(
                query=request_data.query,
                error=error_msg,
                is_abusive=True
            )
            
    except Exception as guard_error:
      
        logger.error(f"Guard validation error: {guard_error}", exc_info=True)
        return ResearchAssistantResponse(
            query=request_data.query,
            error="Your input contains unsafe or disallowed content. Please rephrase your question.",
            is_abusive=True
        )
    

    try:
        if validated_query:
            logger.info(f"Processing research query: {validated_query[:50]}...")
            
            assistant = Research_Assistant(query=validated_query)
            final_output = await assistant.run_agentic_research()
            
            logger.info(f"Research completed successfully for query: {validated_query[:50]}...") 

            return ResearchAssistantResponse(
                query=final_output["query"],
                final_output=final_output["final_output"],
                sources=final_output["sources"],
                is_abusive=False
            )
        
        else:
            logger.error("Validated_query is None after guardrails check") 
            raise HTTPException(status_code=500, detail="Validated_query not passed into the research_Assistant")
    
    except Exception as research_error:
       
        logger.error(f"Research assistant error: {research_error}", exc_info=True)
        return ResearchAssistantResponse(
            query=request_data.query,
            error="An error occurred while processing your research request. Please try again.",
            is_abusive=False
        )
    
    
    












