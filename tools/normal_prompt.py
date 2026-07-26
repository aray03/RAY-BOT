from __future__ import annotations
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from ddgs import DDGS

from config import DEFAULT_MODEL, OLLAMA_HOST

def normal_prompt(value: str, system_prompt: str = "") -> str:
    """Send the prompt to the local LLM and return its response.

    Args:
        value: Anything you want to send to the LLM.
        system_prompt: Optional system instruction to prepend.
    """

    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0,
    )

    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=value))

    response = llm.invoke(messages)

    return str(response.content or "")
