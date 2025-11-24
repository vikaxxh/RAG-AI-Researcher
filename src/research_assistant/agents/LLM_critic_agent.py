from src.research_assistant.prompt_library.prompts import CRITIC_PROMPT
from typing import List,Dict,Any
from langchain_openai import ChatOpenAI
from src.research_assistant.core.logger import logger
from langsmith import traceable #type: ignore

class LLMCriticAgent:
    
    def __init__(self, llm_client:ChatOpenAI):

        self.llm = llm_client

    @traceable(
    name="LLMCritic_agent",
    metadata={"method_type": "review", "version": "1.0"})

    async def review(self, answer: str, context: List[Dict[str, Any]]) -> str:
        
        clean_context = "\n\n".join(
        f"Source: {c.get('source')}\nContent: {c.get('text', c.get('summary',''))}" 
        for c in context
        )
        
        prompt = CRITIC_PROMPT.format(context = clean_context, answer = answer)

        try:
            response = await self.llm.ainvoke(
                [{"role": "user", "content": prompt}]
            )
            
            content = response.content  #type: ignore
            logger.info(f"critic content: {content}")

            if "ACCEPT" in content:
                return "ACCEPT"
            return "REPLAN"
        
        except Exception as e:
            logger.error(f"Critic Decision {e}")
            return "REPLAN"