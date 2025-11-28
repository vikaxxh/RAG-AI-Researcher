import arxiv  # type: ignore
from typing import Any, List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langsmith import traceable  # type: ignore
import time
from src.research_assistant.core.logger import logger
import re


class ArxivAgent:

    def __init__(self):
        self.client = arxiv.Client()
        self._executor = ThreadPoolExecutor(max_workers=4)
        self.max_retries = 5


    def clean_for_arxiv(self, user_query: str) -> str:
        q = user_query.lower()
        q = re.sub(r"[^\w\s]", "", q)

        stopwords = {"what", "is", "are", "the", "explain", "definition", "of"}
        tokens = [t for t in q.split() if t not in stopwords]

        keywords = " ".join(tokens).strip()

        if not keywords:
            keywords = user_query

        return f'(all:"{keywords}") AND (cat:cs.AI OR cat:cs.LG OR cat:cs.CL)'


    @traceable(
        name="Arxiv_agent",
        metadata={"method_type": "search_papers", "version": "1.0"}
    )
    async def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:

        def _search() -> List[Dict[str,Any]]:
            cleaned_query = self.clean_for_arxiv(query)
            logger.info(f"🔍 Final arXiv Query: {cleaned_query}")

            for attempt in range(1, self.max_retries + 1):
                try:
                    search = arxiv.Search(
                        query=cleaned_query,
                        max_results=max_results,
                        sort_by=arxiv.SortCriterion.Relevance,
                    )

                    papers = []
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

                except Exception as e:
                    if "429" in str(e):
                        wait = 2 ** attempt
                        logger.warning(f"⚠️ arXiv rate-limit. Retrying in {wait}s...")
                        time.sleep(wait)
                        continue
                    
                    raise e

            return []

        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, _search)

        except Exception as e:
            raise ValueError(f"Error creating arXiv search: {e}")













# import arxiv #type: ignore
# from typing import Any, List, Dict
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from langsmith import traceable #type: ignore
 
# class ArxivAgent:

#     def __init__(self):
#         self.client = arxiv.Client()
#         self._executor = ThreadPoolExecutor(max_workers = 4)
        
#     @traceable(
#     name="Arxiv_agent",
#     metadata={"method_type": "search_papers", "version": "1.0"}
# )
#     async def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
#         def _search():
#             search = arxiv.Search(
#                 query=query,
#                 max_results=max_results,
#                 sort_by=arxiv.SortCriterion.Relevance,
#             )
            
#             papers: List[Dict[str, Any]] = []
#             for idx, paper in enumerate(self.client.results(search)):
#                 papers.append({
#                     "id": idx,
#                     "source": "arXiv",
#                     "title": paper.title,
#                     "authors": [author.name for author in paper.authors],
#                     "summary": paper.summary,
#                     "published": paper.published.strftime("%Y-%m-%d %H:%M:%S"),
#                     "url": paper.entry_id
#                 })
#             return papers

#         try:
#             loop = asyncio.get_event_loop()
#             return await loop.run_in_executor(self._executor, _search)
#         except Exception as e:
#             raise ValueError(f"Error creating arXiv search: {e}")