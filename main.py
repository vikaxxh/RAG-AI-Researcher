from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.research_assistant.routers.chat_router import router as chat_router
from src.research_assistant.utils.cached_models import get_cross_encoder_model,get_embedding_model
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage
from contextlib import asynccontextmanager
from src.research_assistant.guardrails.guardrails_validator import Guardrails_check
from concurrent.futures import ThreadPoolExecutor
import asyncio

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 Startup: Loading models in parallel...")
    
    # ✅ Load all 3 things at the SAME TIME (Parallelization)
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            loop.run_in_executor(executor, get_embedding_model),
            loop.run_in_executor(executor, get_cross_encoder_model),
            loop.run_in_executor(executor, Guardrails_check)  # Singleton ensures only one instance
        ]
        await asyncio.gather(*tasks)
    
    print("✅ All models loaded in parallel (2-3 seconds)")
    
    yield 
    
    print("🛑 Shutdown: Cleaning up...")
    get_embedding_model.cache_clear()
    get_cross_encoder_model.cache_clear()

app = FastAPI(title="Agentic_Research_Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
  






