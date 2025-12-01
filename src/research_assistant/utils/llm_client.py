from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langsmith import traceable #type: ignore
from langchain_ollama.llms import OllamaLLM
from src.research_assistant.core.logger import logger
from src.research_assistant.config import settings

@traceable(name="Reasoning_LLM_init", metadata={"method_type": "local_ollama"})
def get_common_llm_client():
   
    model_name = "phi3:mini"  
    
    try:
        llm = OllamaLLM(
            model=model_name,
            temperature=0.2,
            format="json"
        )
        
        logger.info(f"🔌 Testing connection to Ollama ({model_name})...")
        logger.info("✅ Planning LLM (Ollama) connected successfully.")
        return llm

    except Exception as e:
        logger.error("❌ Failed to connect to Ollama. Is 'ollama serve' running?")
        logger.error(f"Error details: {e}")
        raise ValueError(f"Reasoning LLM Connection Failed: {e}")


@traceable(
    name="LLM_execution",
    metadata={"method_type": "Primary_LLM", "version": "1.0"}
)
def get_llm_client_rag():

    try:

        llm = ChatGoogleGenerativeAI(
            model = settings.reasoning_model,
            google_api_key = settings.google_api_key,
            safety_settings = {
        0: 2,  # DANGEROUS_CONTENT → medium block
        1: 2,  # HARASSMENT → medium block
        2: 2,  # HATE_SPEECH → medium block
        3: 2   # SEXUALLY_EXPLICIT → medium block
        },
        temperature = 0.5)

    except Exception as e:
        raise ValueError(f"RAG LLM Failed : {e}")
        
    return llm


@traceable(
    name="Critic_LLM_execution",
    metadata={"method_type": "Critic_LLM", "version": "1.0"}
)
def get_critic_llm_client():

    try:
        llm = ChatOpenAI(model=settings.critic_model, 
                temperature = 0, 
                api_key = SecretStr(settings.openai_api_key or ""),
                )
        
    except Exception as e:
        raise ValueError(f"Critic LLM Failed : {e}")
    
    return llm


