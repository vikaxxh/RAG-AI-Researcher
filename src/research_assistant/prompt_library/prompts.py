CRITIC_PROMPT = """You are a hallucination detector. Check if this AI answer contains any made-up information.

CONTEXT (verified facts):
{context}

ANSWER (check this):
{answer}

REPLAN if you detect:
- Facts, numbers, or names not in the context
- Claims that go beyond what the context states
- Invented details or assumptions presented as facts

ACCEPT if the answer is mostly consistent with context and no major hallucination found.

ONE word answer: ACCEPT or REPLAN"""