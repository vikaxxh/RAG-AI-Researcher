from guardrails.validator_base import Validator, register_validator, FailResult, PassResult
from src.research_assistant.guardrails.guardrails_patterns import banned_keywords,injection_patterns
import re

@register_validator(name="harmful_keywords", data_type="string")
class HarmfulKeywords(Validator):
    """Validates that input doesn't contain harmful keywords or prompt injection patterns."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.banned_keywords = banned_keywords
        self.injection_patterns = injection_patterns
    
    def validate(self, value, metadata=None):
        """Check if input contains harmful keywords or prompt injection patterns."""
        lower_value = value.lower()
        
        found_keywords = [kw for kw in self.banned_keywords if kw in lower_value]
        
        if found_keywords:
            return FailResult(
                error_message=f"Your input contains harmful content: '{', '.join(found_keywords)}'. I cannot process requests related to dangerous or illegal activities."
            )
        
        for pattern in self.injection_patterns:
            if re.search(pattern, lower_value, re.IGNORECASE):
                return FailResult(
                    error_message="Your input appears to contain a prompt injection attempt. Please ask your question directly without trying to manipulate the system."
                )
        
        return PassResult()