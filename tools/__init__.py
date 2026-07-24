from .calculate_add import calculate_add
from .taco_tool import print_i_like_tacos

# List of LangChain tool objects to bind to the LLM
tools = [
    calculate_add,
    print_i_like_tacos,
]

# Dictionary for quick lookup during execution: {"calculate_add": calculate_add, ...}
available_tools = {tool.name: tool for tool in tools}


def get_tool_spec(tool_name: str) -> dict | None:
    tool = available_tools.get(tool_name)
    if tool is None:
        return None

    args_schema = getattr(tool, "args_schema", None)
    if args_schema is None:
        parameters = {}
    elif hasattr(args_schema, "model_json_schema"):
        parameters = args_schema.model_json_schema()
    elif hasattr(args_schema, "schema"):
        parameters = args_schema.schema()
    else:
        parameters = {}

    return {
        "name": tool.name,
        "schema": {
            "function": {
                "name": tool.name,
                "parameters": parameters,
            }
        },
    }