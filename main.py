from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.research_assistant.routers.chat_router import router as chat_router
from src.research_assistant.utils.cached_models import get_cross_encoder_model,get_embedding_model
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from contextlib import asynccontextmanager

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🔥 Startup: Loading models...")

    get_embedding_model()
    get_cross_encoder_model()
    yield 

    print("🛑 Shutdown: Cleaning up...")
    get_embedding_model.cache_clear()
    get_cross_encoder_model.cache_clear()

app = FastAPI(title="Agentic_Research_Assistant",lifespan=lifespan)

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
  






