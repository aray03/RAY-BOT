def calculate_add(a: float, b: float) -> str:
    print(f"Calculating the sum of {a} and {b}")
    return str(a + b)


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
