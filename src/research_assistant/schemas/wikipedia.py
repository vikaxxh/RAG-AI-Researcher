from pydantic import BaseModel

class WikiContent(BaseModel):
    id: int
    source:str
    title: str
    summary: str
    