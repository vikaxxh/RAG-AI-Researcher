from pydantic import BaseModel
from typing import List

class ResearchAssistantRequest(BaseModel):
    query:str
    
class ResearchAssistantResponse(BaseModel):
    final_output:str
    sources:List[str]