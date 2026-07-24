from __future__ import annotations
from langchain_core.tools import tool

@tool
def calculate_add(a: float, b: float) -> str:
    """Use this tool exclusively whenever you are asked to add two numbers together. 
    You must use this tool instead of calculating the sum yourself.

    Args:
        a: The first number.
        b: The second number.
    """
    result = str(a + b)

    return result