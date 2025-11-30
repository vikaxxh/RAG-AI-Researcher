from tavily import TavilyClient #type: ignore
from typing import List, Dict, Any
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langsmith import traceable #type: ignore


class TavilyAgent:

    def __init__(self):
        self.client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))
        self._executor = ThreadPoolExecutor(max_workers = 4)
        
    @traceable(
    name="Tavily_agent",
    metadata={"method_type": "search_web", "version": "1.0"})

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:

        def _search():
        
            response: Dict[str, Any] = self.client.search(  # type: ignore
                query=query,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True,  
                max_results=max_results,
            )

            results: List[Dict[str, Any]] = response.get("results", [])  
            processed: List[Dict[str, Any]] = []

            for idx, item in enumerate(results):
                item_dict: Dict[str, Any] = item  
                processed.append({
                    "id": idx,
                    "source": "web",
                    "title": item_dict.get("title", "No title available"),
                    "summary": item_dict.get("content", ""),
                    "url": item_dict.get("url", "")
                })

            return processed   

        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, _search)
        except Exception as e:
            raise ValueError(f"Error creating tavily search: {e}")