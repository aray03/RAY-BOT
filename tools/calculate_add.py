from __future__ import annotations
from langchain_core.tools import tool

@tool
def calculate_add(a: float, b: float) -> str:
    """Add two numbers together.

    Args:
        a: The first number.
        b: The second number.
    """
    result = str(a + b)
    print(result)
    return result