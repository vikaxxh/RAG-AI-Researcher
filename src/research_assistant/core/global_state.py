from typing import Optional, Any

class GlobalState:
    embedding_model: Optional[Any] = None
    cross_encoder_model: Optional[Any] = None
    guardrails_model: Optional[Any] = None


state = GlobalState()