from __future__ import annotations
from langchain_core.tools import tool

@tool
def print_i_like_tacos(count: int = 1) -> str:
    """Print 'I LIKE TACOS' the requested number of times.

    Args:
        count: How many times to print the phrase. Defaults to 1.
    """
    total = max(1, count)
    output = "\n".join(["I LIKE TACOS"] * total)
    print(output)
    return output