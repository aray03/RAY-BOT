from .calculate_add import calculate_add, calculate_add_schema

available_tools = {
    "calculate_add": calculate_add,
}

tools_schema = [
    calculate_add_schema,
]
