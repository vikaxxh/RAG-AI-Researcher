from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.research_assistant.routers.chat_router import router as chat_router
from src.research_assistant.utils.cached_models import (
    get_cross_encoder_model,
    get_embedding_model,
    get_prompt_injection_scanner, 
    get_toxicity_scanner
)
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Dict, Any, Tuple
from src.research_assistant.core.logger import logger
from src.research_assistant.core.global_state import state

# Load environment variables
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Application settings
APP_TITLE = "Agentic Research Assistant"
APP_VERSION = "0.1.0"
HOST = "0.0.0.0"
PORT = 8000

MAX_WORKERS = 3

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def load_guardrails_models() -> Tuple[Any, Any]:
    """Load both guardrails scanners and return as tuple."""
    prompt_injection = get_prompt_injection_scanner()
    toxicity = get_toxicity_scanner()
    return (prompt_injection, toxicity)


def clear_model_caches():
    """Utility function to clear all model caches - Single source of truth."""
    if hasattr(get_embedding_model, 'cache_clear'):
        get_embedding_model.cache_clear()
    if hasattr(get_cross_encoder_model, 'cache_clear'):
        get_cross_encoder_model.cache_clear()
    if hasattr(get_prompt_injection_scanner, 'cache_clear'):
        get_prompt_injection_scanner.cache_clear()
    if hasattr(get_toxicity_scanner, 'cache_clear'):
        get_toxicity_scanner.cache_clear()
    logger.info("✅ All model caches cleared.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("🚀 Starting Agentic Research Assistant...")
    logger.info("⚡ Loading models (one-time initialization)...")
    
    loop = asyncio.get_event_loop()
  
    embedding_future = loop.run_in_executor(executor, get_embedding_model)
    cross_encoder_future = loop.run_in_executor(executor, get_cross_encoder_model)
    guardrails_future = loop.run_in_executor(executor, load_guardrails_models)
    
    try:
        state.embedding_model, state.cross_encoder_model, state.guardrails_model = await asyncio.gather(
            embedding_future,
            cross_encoder_future,
            guardrails_future
        )
        logger.info("✅ All models loaded successfully!")
        logger.info(f"Embedding Model: {type(state.embedding_model).__name__}")
        logger.info(f"Cross-Encoder: {type(state.cross_encoder_model).__name__}")
        logger.info(f"Guardrails: {type(state.guardrails_model).__name__}")
        logger.info("🎉 Application ready to serve requests!\n")
        
    except Exception as e:
        logger.error(f"❌ Error loading models: {e}")
        raise
    
    yield  

    logger.info("\n🛑 Shutting down Agentic Research Assistant...")
    logger.info("🧹 Clearing model caches...")
    
    # Use the single source of truth function
    clear_model_caches()

    executor.shutdown(wait=False)
    logger.info("✅ Cleanup complete. Goodbye!")


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Advanced AI-powered research tool with multi-agent architecture",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/", tags=["Health"])
async def root() -> Dict[str, Any]:
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "service": APP_TITLE,
        "version": APP_VERSION,
        "models_loaded": all([
            state.embedding_model is not None,
            state.cross_encoder_model is not None,
            state.guardrails_model is not None
        ])
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """Detailed health check endpoint"""
    return {
        "status": "ok",
        "models": {
            "embedding": state.embedding_model is not None,
            "cross_encoder": state.cross_encoder_model is not None,
            "guardrails": state.guardrails_model is not None
        }
    }


@app.post("/admin/clear-cache", tags=["Admin"])
async def clear_cache_endpoint() -> Dict[str, str]:
    """Manual endpoint to clear model caches (for admin/debugging)."""
    clear_model_caches()
    return {"status": "success", "message": "Model caches cleared"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🌐 Starting server on http://{HOST}:{PORT}")
    logger.info(f"📚 API docs available at http://{HOST}:{PORT}/docs\n")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,  # Set to False for production
        log_level="info",
    )