import os
from functools import lru_cache


class Settings:
    def __init__(self):
        
        #Api_key settings
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

        #Langsmith settings
        self.langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        self.langsmith_tracing = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
        self.langsmith_project = os.getenv("LANGSMITH_PROJECT", "research-assistant")
        self.langsmith_endpoint = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

        # Model settings
        self.reasoning_model = os.getenv("REASONING_MODEL", "gpt-4o-mini")
        self.planning_model = os.getenv("PLANNING_MODEL", "gpt-4o-mini")
        self.critic_model = os.getenv("PLANNING_MODEL", "gpt-4o-mini")
        self.synthesis_model = os.getenv("SYNTHESIS_MODEL", "gemini-2.5-flash")

        #Tool settings
        self.max_arxiv_results = int(os.getenv("MAX_ARXIV_RESULTS", "5"))
        self.max_tavily_results = int(os.getenv("MAX_TAVILY_RESULTS", "5"))
        self.max_wikipedia_results = int(os.getenv("MAX_WIKIPEDIA_RESULTS", "3"))

@lru_cache()
def get_settings():
    return Settings()
settings = get_settings()

