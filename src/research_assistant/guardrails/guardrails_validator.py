from llm_guard.input_scanners import PromptInjection, Toxicity
from llm_guard import scan_prompt
from better_profanity import profanity
from typing import Tuple, Optional, Union
from guardrails.guard import Guard
from src.research_assistant.core.logger import logger
from src.research_assistant.guardrails.harmful_keywords_validator import HarmfulKeywords


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

        # ===== Initialize Guardrails-AI with your HarmfulKeywords =====
        # This already contains your banned_keywords and injection_patterns
        self.guard = Guard()
        self.guard.use(HarmfulKeywords(on_fail="noop"))
        
        # ===== Initialize Better Profanity =====
        profanity.load_censor_words()  # type: ignore[no-untyped-call]
        
        # ===== Initialize LLM Guard (AI-powered backup) =====
        self.input_scanners: list[Union[PromptInjection, Toxicity]] = [
            # AI-powered prompt injection detection (catches complex patterns)
            PromptInjection(
                threshold=0.5,
                match_type="full"
            ),
            # AI-powered toxicity detection
            Toxicity(
                threshold=0.5,
                match_type="sentence"
            )
        ]
        
        Guardrails_check._initialized = True
        print("✅ Guardrails + LLM Guard initialized")

    def safety_check(self, query: str) -> Tuple[Optional[str], Optional[str]]:
      
        try:
            # ===== LAYER 1: Better Profanity (Fastest) =====
            if profanity.contains_profanity(query):  # type: ignore[no-untyped-call]
                error_msg = "This query contains profanity. Please rephrase your question respectfully."
                logger.warning(f"Better-Profanity blocked: {query[:50]}...")
                return error_msg, None
            
            # ===== LAYER 2: Guardrails HarmfulKeywords (Your Custom Validator) =====
            try:
                validation_result = self.guard.validate(query)
                
                if not validation_result.validation_passed:
                    # Your HarmfulKeywords validator provides detailed error messages
                    error_msg = "Your input contains harmful or disallowed content. Please rephrase your question appropriately."
                    
                    logger.warning(f"Guardrails HarmfulKeywords blocked: {query[:50]}...")
                    
                    # Log detailed error information if available
                    if hasattr(validation_result, 'error_spans_in_output') and validation_result.error_spans_in_output:
                        error_details = validation_result.error_spans_in_output
                        logger.debug(f"Validation errors: {error_details}")
                    
                    return error_msg, None
                
                # Get validated output from Guardrails
                validated_query = validation_result.validated_output or query
                
            except Exception as guard_error:
                logger.error(f"Guardrails HarmfulKeywords error: {guard_error}", exc_info=True)
                # Continue to LLM Guard as backup
                validated_query = query
            
            # ===== LAYER 3: LLM Guard (AI-Powered Backup) =====
            sanitized_prompt, results_valid, results_score = scan_prompt(
                self.input_scanners,
                validated_query
            )
            
            if not results_valid:
                failed_checks: list[str] = []
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
            
            # Use LLM Guard's sanitized output if available, otherwise use Guardrails output
            final_validated_query = sanitized_prompt if sanitized_prompt else validated_query
            
            # ===== ALL CHECKS PASSED ✅ =====
            logger.info(f"✅ Query passed all safety checks: {query[:50]}...")
            return None, final_validated_query
            
        except Exception as e:
            logger.error(f"⚠️ Safety check error: {e}", exc_info=True)
            error_msg = "An error occurred during safety validation. Please try again."
            return error_msg, None