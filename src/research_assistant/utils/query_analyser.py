from typing import Dict, Any, List

def analyse_query(query: Any) -> Dict[str, Any]:
    
    if not query:
        raise ValueError("Query cannot be empty")
    
    if not isinstance(query, str): 
        raise TypeError("Query must be a string")
    
    query = query.strip()
    if not query:
        raise ValueError("Query cannot be just whitespace")
    
    try:
        query_lower = query.lower()

        is_definition = any(word in query_lower for word in ["what is", "define", "who is", "explain"])
        is_recent = any(word in query_lower for word in ["latest", "recent", "2024", "2025", "news", "today"])
        is_research = any(word in query_lower for word in ["research", "paper", "study", "arxiv"])
        is_comparison = any(word in query_lower for word in ["vs", "versus", "compare", "difference"])
    
        sources: List[str] = []
        
        if is_recent and is_research:
            sources = ["tavily", "arxiv"]
        else:
            if is_definition:
                sources.append("wikipedia")
            
            if is_recent:
                sources.append("tavily")
            
            if is_research:
                sources.append("arxiv")
            
            if is_comparison:
                sources.extend(["wikipedia", "tavily"])
           
            if not sources:
                sources = ["wikipedia", "arxiv"]
            
            if "arxiv" not in sources:
                sources.append("arxiv")

        sources = list(set(sources))
 
        if is_recent and is_research:
            strategy = "arxiv_focus"  
        elif is_recent:
            strategy = "tavily_first"
        elif is_definition:
            strategy = "wikipedia_first"
        elif is_research:
            strategy = "arxiv_focus"
        elif is_comparison:
            strategy = "both"
        else:
            strategy = "auto"
        
        return {
            "query": query,
            "strategy": strategy,
            "sources": sources,
        }
    
    except Exception as e:
        print(f"Error analyzing query: {e}")
        return {
            "query": query,
            "strategy": "auto",
            "sources": ["tavily", "arxiv"],
            "error": str(e)
        }
