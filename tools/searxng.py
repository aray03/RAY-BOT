from __future__ import annotations
import requests

SEARXNG_URL = "http://localhost:8080/search"


def search_searxng(query: str, max_results: int = 3) -> str:
    """Fetch search results from local SearXNG and format as context."""
    params = {
        "q": query,
        "format": "json"
    }
    
    try:
        response = requests.get(SEARXNG_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])[:max_results]
        if not results:
            return "No web search results found."
            
        snippets = []
        for i, res in enumerate(results, 1):
            title = res.get("title", "No Title")
            content = res.get("content", "No Content")
            url = res.get("url", "")
            snippets.append(f"[{i}] {title}\nSnippet: {content}\nSource: {url}")
            
        return "\n\n".join(snippets)
        
    except requests.exceptions.RequestException as e:
        print(f"SearXNG connection error: {e}\n Returning without web search context.")
        return ""