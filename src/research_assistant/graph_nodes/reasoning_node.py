from src.research_assistant.core.logger import logger
from src.research_assistant.core.state_manager import ResearchState
from langsmith import traceable #type: ignore
from src.research_assistant.utils.llm_client import get_common_llm_client,get_critic_llm_client
from src.research_assistant.prompt_library.reasoning_prompt import REASONING_PROMPT
from src.research_assistant.schemas.reasoning_model import ReasoningOutput
import json
from typing import Any
from pydantic import ValidationError
import re

@traceable(
    name="reasoning_node",
    metadata={"node_type": "reasoning", "version": "1.0"}
)
async def reasoning_node(state: ResearchState) -> ResearchState:

    logger.info("🧠 Starting reasoning...")

    try:
        llm = get_critic_llm_client()
        prompt= REASONING_PROMPT.format(query = state["query"])
        raw_output = llm.invoke(prompt)

    
        if hasattr(raw_output, 'content'):
            output_text = raw_output.content #type: ignore
        else:
            output_text = str(raw_output)

        cleaned_text = re.sub(r"```(?:json)?", "", output_text).strip() #type:ignore
        
        try:
            raw_dict = json.loads(cleaned_text) #type: ignore
            logger.info(f"{raw_dict}")

        except json.JSONDecodeError:
            logger.warning(f"phi3 output invalid JSON: {output_text}")

            raw_dict:dict[str,Any] = {
                "thought": output_text,  
                "intent": state['query'],
                "subtasks": [],
                "need_tools": False,
                "tools": [],
                "final_decision": "continue_planning"
            }
        
        try:
            reasoning = ReasoningOutput(**raw_dict)

        except ValidationError as ve:
            logger.warning(f"Pydantic validation failed: {ve}")
          
            reasoning = ReasoningOutput(
                thought=raw_dict.get("thought", ""),
                intent=raw_dict.get("intent", state['query']),
                subtasks=raw_dict.get("subtasks", []),
                need_tools=raw_dict.get("need_tools", False),
                tools=raw_dict.get("tools", []),
                final_decision=raw_dict.get("final_decision", "continue_planning")
            )
        
        state["reasoning"] = reasoning.model_dump()
        state["strategy"] = ", ".join(reasoning.subtasks)
        state["sources"] = [tool.name for tool in reasoning.tools]
        
    except Exception as e:
        raise ValueError(f"Reasoning node failed: {e}")
    
    logger.info("✅ Reasoning completed")
    return state

