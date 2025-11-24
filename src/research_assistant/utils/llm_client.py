from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langsmith import traceable #type: ignore


@traceable(
    name="LLM_execution",
    metadata={"method_type": "Primary_LLM", "version": "1.0"}
)
def get_llm_client_rag():

    try:

        llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = os.getenv("GOOGLE_API_KEY"),
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
        llm = ChatOpenAI(model="gpt-4o-mini", 
                temperature=0, 
                api_key = SecretStr(os.getenv("GPT_API_KEY") or "")
                )
        
    except Exception as e:
        raise ValueError(f"Critic LLM Failed : {e}")
    
    return llm
