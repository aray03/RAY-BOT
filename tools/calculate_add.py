def calculate_add(a: float, b: float) -> str:
    result = str(a + b)
    print(result)
    return result


calculate_add_schema = {
    "type": "function",
    "function": {
        "name": "calculate_add",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
}

calculate_add_spec = {
    "name": "calculate_add",
    "function": calculate_add,
    "schema": calculate_add_schema,
    "terminal": True,
}
