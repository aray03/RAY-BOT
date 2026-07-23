"""Template for creating a new tool module.

Copy this file when adding another tool, then replace the function name,
schema, and implementation with your own logic.
"""


def example_tool(value: str) -> str:
    return value


example_tool_schema = {
    "type": "function",
    "function": {
        "name": "example_tool",
        "description": "Describe what this tool does.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {"type": "string", "description": "Input value for the tool"},
            },
            "required": ["value"],
        },
    },
}

example_tool_spec = {
    "name": "example_tool",
    "function": example_tool,
    "schema": example_tool_schema,
    "terminal": True,
}
