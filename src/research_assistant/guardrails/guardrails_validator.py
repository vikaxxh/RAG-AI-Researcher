from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage
from src.research_assistant.guardrails.harmful_keywords_validator import HarmfulKeywords
from typing import Tuple, Optional

class Guardrails_check:
    """
    Singleton Guardrails checker - initializes once and reuses.
    This prevents reloading validators on every instantiation.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """
        Singleton pattern: Only create one instance of this class.
        All calls to Guardrails_check() return the same instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """
        Initialize Guardrails only once (even if called multiple times).
        """
        # ✅ Skip initialization if already done
        if Guardrails_check._initialized:
            return
        
        print("⏳ Initializing Guardrails...")
        
        # Initialize Guard
        self.guard = Guard()
        
        # Add validators
        self.guard.use(ProfanityFree(on_fail="noop"))
        self.guard.use(ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="noop"))
        self.guard.use(HarmfulKeywords(on_fail="noop"))
        
        # Mark as initialized
        Guardrails_check._initialized = True
        print("✅ Guardrails initialized")

    def safety_check(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Check if query is safe.
        
        Args:
            query: User input string to validate
            
        Returns:
            Tuple of (error_message, validated_query)
            - If safe: (None, validated_query)
            - If unsafe: (error_message, None)
        """
        try:
            validation_result = self.guard.validate(query)
            
            if not validation_result.validation_passed:
                error_msg = "This is an abusive or harmful query. I cannot process this further. Please rephrase your question respectfully."
                return error_msg, None
            else:
                validated_query = validation_result.validated_output or query
                return None, validated_query
            
        except Exception as guard_error:
            print(f"⚠️ Guard validation error: {guard_error}")
            error_msg = "Your input contains unsafe or disallowed content. Please rephrase your question."
            return error_msg, None
            

