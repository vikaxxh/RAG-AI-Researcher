from pydantic import BaseModel
from typing import List

class ArxivPaper(BaseModel):
    id: int
    source:str
    title: str
    authors: List[str]
    summary: str
    published: str
    url: str