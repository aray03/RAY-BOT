from __future__ import annotations
import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from config import DEFAULT_MODEL, OLLAMA_HOST

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
        print(f"SearXNG connection error: {e}")
        return ""


def search_prompt(value: str, system_prompt: str = "", max_results: int = 3) -> str:
    """Search SearXNG, append context to the prompt, and send to local Ollama."""
    
    # 1. Fetch search context from local SearXNG
    web_context = search_searxng(value, max_results=max_results)

    # 2. Set up local ChatOllama instance
    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0,
    )

    # 3. Formulate system message and user prompt with grounded context
    messages = []
    
    default_system = (
        "You are a helpful assistant. Use the provided web context to answer the user's question accurately."
    )
    messages.append(SystemMessage(content=system_prompt if system_prompt else default_system))

    prompt_with_context = f"""Web Search Context:
{web_context}

User Question: {value}


Guidelines:
- Use the web search context to answer the user's question.
- Don't mention anything about the web search context in your answer, such as saying 'According to the web search results...'.
- Don't mention anything about the web search engine or SearXNG in your answer.
- Don't mention anything about sources unless it is specifically relevant to the answer or asked specifically
"""

    messages.append(HumanMessage(content=prompt_with_context))

    # 4. Invoke model locally
    response = llm.invoke(messages)

    return str(response.content or "")