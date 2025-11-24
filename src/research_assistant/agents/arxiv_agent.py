import arxiv #type: ignore
from typing import Any, List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langsmith import traceable #type: ignore
 
class ArxivAgent:

    def __init__(self):
        self.client = arxiv.Client()
        self._executor = ThreadPoolExecutor(max_workers = 4)
        
    @traceable(
    name="Arxiv_agent",
    metadata={"method_type": "search_papers", "version": "1.0"}
)
    async def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        def _search():
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
            )
            
            papers: List[Dict[str, Any]] = []
            for idx, paper in enumerate(self.client.results(search)):
                papers.append({
                    "id": idx,
                    "source": "arXiv",
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "published": paper.published.strftime("%Y-%m-%d %H:%M:%S"),
                    "url": paper.entry_id
                })
            return papers

        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, _search)
        except Exception as e:
            raise ValueError(f"Error creating arXiv search: {e}")