from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

@lru_cache(maxsize=1)
def get_embedding_model():
    print("🔵 Loading BGE embedding model (cached)...")
    return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

@lru_cache(maxsize=1)
def get_cross_encoder_model():
    print("🔵 Loading CrossEncoder model (cached)...")
    return HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")