from pydantic import BaseModel
from typing import List,Optional

class ResearchAssistantRequest(BaseModel):
    query:str
    
class ResearchAssistantResponse(BaseModel):
    query:str
    final_output: Optional[str] = None
    sources: Optional[List[str]] = None
    error: Optional[str] = None
    is_abusive:bool = False