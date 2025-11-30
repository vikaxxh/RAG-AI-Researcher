from langchain_core.prompts import PromptTemplate

PLANNING_PROMPT = """
You are a PLANNING ENGINE for an AI research assistant.

Input:
- User query: {query}
- Reasoning output: {reasoning_json}

Your tasks:
- Convert subtasks into a sequential execution plan.
- For each step, choose an appropriate tool.
- ALLOWED tool names:
  - "arxiv_agent"
  - "tavily_agent"
  - "wikipedia_agent"

STRICT RULES:
- Output STRICT JSON ONLY.
- No comments, no extra text, no code, no python syntax.
- "tool_name" MUST be exactly one of the allowed names.
- "query" MUST be a plain string.
- "step_order" MUST be an integer starting from 1 and strictly increasing (1,2,3,...)
- DO NOT create or invent any other fields.
- DO NOT output Python-like code, function calls, or `.append()` or similar patterns.
- DO NOT modify the keys in the JSON.

Output Format:
{{
  "plan": [
    {{
      "tool_name": "arxiv_agent",
      "query": "...",
      "step_order": 1
    }}
  ]
}}
"""

planning_prompt = PromptTemplate(
    template=PLANNING_PROMPT,
    input_variables=["query","reasoning_json"])