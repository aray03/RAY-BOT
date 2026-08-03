from __future__ import annotations
from langchain_core.tools import tool

@tool
def print_i_like_tacos(count: int = 1):
    """Print 'I LIKE TACOS' the requested number of times.

    Args:
        count: How many times to print the phrase. Defaults to 1.
    """

    output = ""
    for i in range(count):
        print("I LIKE TACOS")

        output += str(i+1) + " I LIKE TACOS\n"

    print(output)
    return output