from pydantic import BaseModel,Field
from typing import List, Literal


class Tool(BaseModel):
    name: str = Field(..., description="Name of the tool to use")
    query: str = Field(..., description="Query/input for the tool")

class ReasoningOutput(BaseModel):
    thought: str = Field(..., description="Reasoning about the query")
    intent: str = Field(..., description="User's intent")
    subtasks: List[str]  = Field(default_factory=list,description="List of subtasks") #type:ignore
    need_tools: bool = Field(..., description="Whether tools are needed")
    tools: List[Tool] = Field(default_factory=list,description="List of tools to execute") #type:ignore
    final_decision: Literal["continue_planning", "ready_to_answer"] = Field(..., description="Decision on next step")