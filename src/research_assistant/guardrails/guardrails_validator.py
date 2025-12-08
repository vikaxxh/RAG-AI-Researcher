from llm_guard.input_scanners import PromptInjection, Toxicity #type: ignore
from llm_guard import scan_prompt #type: ignore
from better_profanity import profanity #type: ignore
from typing import Tuple, Optional, Union, List
from guardrails.guard import Guard #type: ignore
from src.research_assistant.core.logger import logger
from src.research_assistant.guardrails.harmful_keywords_validator import HarmfulKeywords
from src.research_assistant.utils.cached_models import (
    get_prompt_injection_scanner, 
    get_toxicity_scanner
)


class Guardrails_check:
  
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if Guardrails_check._initialized:
            return
        
        print("⏳ Initializing Guardrails + LLM Guard...")

        self.guard = Guard()
        self.guard.use(HarmfulKeywords(on_fail="noop"))
        

        profanity.load_censor_words()  # type: ignore[no-untyped-call]
       
        self.input_scanners: List[Union[PromptInjection, Toxicity]] = [
            get_prompt_injection_scanner(),
            get_toxicity_scanner()
        ]
        
        Guardrails_check._initialized = True
        print("✅ Guardrails + LLM Guard initialized")

    def safety_check(self, query: str) -> Tuple[Optional[str], Optional[str]]:
    
        try:
            if profanity.contains_profanity(query):  # type: ignore[no-untyped-call]
                error_msg = "This query contains profanity. Please rephrase your question respectfully."
                logger.warning(f"Better-Profanity blocked: {query[:50]}...")
                return error_msg, None
            
            try:
                validation_result = self.guard.validate(query)
                
                if not validation_result.validation_passed:
                    error_msg = "Your input contains harmful or disallowed content. Please rephrase your question appropriately."
                    logger.warning(f"Guardrails HarmfulKeywords blocked: {query[:50]}...")
                    
                    if hasattr(validation_result, 'error_spans_in_output') and validation_result.error_spans_in_output:
                        error_details = validation_result.error_spans_in_output
                        logger.debug(f"Validation errors: {error_details}")
                    
                    return error_msg, None
                
                validated_query = validation_result.validated_output or query
                
            except Exception as guard_error:
                logger.error(f"Guardrails HarmfulKeywords error: {guard_error}", exc_info=True)
                validated_query = query
            
            sanitized_prompt, results_valid, results_score = scan_prompt(
                self.input_scanners,  # Uses cached scanner instances
                validated_query
            )
            
            if not results_valid:
                failed_checks: List[str] = []
                for scanner_name, score in results_score.items():
                    if score > 0.5:
                        failed_checks.append(scanner_name)
                
                error_msg = (
                    "Your input contains unsafe content detected by our AI safety system. "
                    "Please rephrase your question."
                )
                
                logger.warning(f"LLM Guard blocked query. Failed checks: {failed_checks}")
                logger.debug(f"Scores: {results_score}")
                
                return error_msg, None
            
            final_validated_query = sanitized_prompt if sanitized_prompt else validated_query
         
            logger.info(f"✅ Query passed all safety checks: {query[:50]}...")
            return None, final_validated_query
            
        except Exception as e:
            logger.error(f"⚠️ Safety check error: {e}", exc_info=True)
            error_msg = "An error occurred during safety validation. Please try again."
            return error_msg, None