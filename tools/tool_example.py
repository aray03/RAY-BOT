from __future__ import annotations
from langchain_core.tools import tool

"""Template for creating a new tool module using LangChain.

Copy this file when adding another tool, then replace the function name,
docstring, and implementation with your own logic.
"""


@tool
def example_tool(value: str) -> str:
    """Describe what this tool does.

    Args:
        value: Input value for the tool.
    """
    return value