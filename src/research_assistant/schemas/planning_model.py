from pydantic import BaseModel, Field
from typing import List, Optional

class PlanStep(BaseModel):
    tool_name: str
    query: str
    step_order: Optional[int] = Field(1, description="Execution order of this step")

class PlanningOutput(BaseModel):
    plan: List[PlanStep] = Field(default_factory=list, description="List of plan steps")