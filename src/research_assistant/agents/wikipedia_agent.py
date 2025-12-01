import wikipediaapi #type: ignore
from typing import Any,List,Dict
import wikipedia #type: ignore
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langsmith import traceable #type: ignore
from src.research_assistant.config import settings

class WikipediaAgent:

    def __init__(self):
        self.api = wikipediaapi.Wikipedia(user_agent="Agentic-research-assistant (arc@example.com)", language="en")
        self._executor = ThreadPoolExecutor(max_workers=4)

    @traceable(
    name="Wikipedia_agent",
    metadata={"method_type": "search_wikipedia", "version": "1.0"})
    
    async def search_wikipedia(self, query: str, max_results: int = settings.max_wikipedia_results) -> List[Dict[str, Any]]:
        def _fetch():
            search_titles = wikipedia.search(query, results=max_results) #type:ignore

            if not search_titles:
                raise ValueError(f"No results found for query: {query}")

            articles: List[Dict[str, Any]] = []

            for idx, title in enumerate(search_titles): #type:ignore
                page = self.api.page(title) #type:ignore
                if page.exists():
                    articles.append({
                        "id": idx,
                        "source": "Wikipedia",
                        "title": page.title,
                        "summary": page.summary
                    })

            if not articles:
                raise ValueError(f"No Wikipedia pages found for query: {query}")

            return articles

        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, _fetch)
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Wikipedia search error: {e}")
    
