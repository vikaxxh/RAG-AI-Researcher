from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from pathlib import Path
import os

# ✅ Create cache directory
MODEL_CACHE_DIR = Path("./model_cache")
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ✅ Set environment variables (works for all HuggingFace models)
os.environ['TRANSFORMERS_CACHE'] = str(MODEL_CACHE_DIR)
os.environ['HF_HOME'] = str(MODEL_CACHE_DIR)

@lru_cache(maxsize=1)
def get_embedding_model():
    print("🔵 Loading BGE embedding model (cached)...")
    
    cache_dir = MODEL_CACHE_DIR / "embedding"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        cache_folder=str(cache_dir),
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

@lru_cache(maxsize=1)
def get_cross_encoder_model():
    print("🔵 Loading CrossEncoder model (cached)...")
    
    # ✅ Uses environment variables for caching automatically
    return HuggingFaceCrossEncoder(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )