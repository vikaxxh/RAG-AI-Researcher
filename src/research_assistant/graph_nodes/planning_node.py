from src.research_assistant.core.state_manager import ResearchState
from src.research_assistant.core.logger import logger
from typing import Dict,Any 
from langsmith import traceable #type: ignore
from src.research_assistant.prompt_library.planning_prompt import planning_prompt
from src.research_assistant.utils.llm_client import get_critic_llm_client
from src.research_assistant.schemas.planning_model import PlanningOutput,PlanStep
import json
import re



@traceable(
    name="planning_node_llm",
    metadata={"node_type": "planning", "version": "1.0"}
)
async def planning_node(state: ResearchState) -> ResearchState:
   
    logger.info("📝 Planning code activated...")

    try:
        reasoning = state.get("reasoning", {})
        logger.info(f"planning code reason is passed: {reasoning}")

        llm = get_critic_llm_client()  # This returns Phi-3
        logger.info("phi3 function implemented")

        prompt = planning_prompt.format(
            query=state["query"],
            reasoning_json=json.dumps(reasoning)
        )

        raw_output = llm.invoke(prompt)
        logger.info(f"planning raw output: {raw_output}")

        # 🔧 FIX: Extract content from message object
        if hasattr(raw_output, 'content'):
            output_text = raw_output.content
        else:
            output_text = str(raw_output)
        
        # Clean any markdown formatting
        cleaned_text = re.sub(r"```(?:json)?", "", output_text).strip()
        logger.info(f"cleaned text: {cleaned_text}")

        try:
            plan_dict = json.loads(cleaned_text)
            logger.info(f"parsed plan_dict: {plan_dict}")

        except json.JSONDecodeError as e:
            logger.warning(f"phi3 output not valid JSON: {e}. Output: {output_text}")
            plan_dict: Dict[str, Any] = {"plan": []}

        try:
            planning_output = PlanningOutput(**plan_dict)
            
        except Exception as ve:
            logger.warning(f"Pydantic validation failed: {ve}")
            
            tools = reasoning.get("tools", [])
            fallback_plan = [
                PlanStep(tool_name=t["name"], query=t["query"], step_order=i+1)
                for i, t in enumerate(tools)
            ]
            planning_output = PlanningOutput(plan=fallback_plan)

        # Update state
        state["planning"] = [step.model_dump() for step in planning_output.plan]
        logger.info(f"final Planning output: {state.get('planning', {})}")

    except Exception as e:
        logger.error(f"Planning node failed: {e}", exc_info=True)
        raise ValueError(f"LLM-driven planning node failed: {e}")

    logger.info("✅ Planning code completed")
    return state