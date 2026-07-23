import json
import ollama

# 1. Define the Python function
def calculate_add(a: float, b: float) -> str:
    """Add two numbers together.

    Args:
        a: The first number.
        b: The second number.
    """
    return str(a + b)

available_tools = {
    "calculate_add": calculate_add
}

# 2. Explicit JSON schema format for Ollama
tools_schema = [
    {
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
]

messages = [
    {
        "role": "system",
        "content": "You are my helpful computer assistant named 'AIDZ'. Use available tools when math is requested.",
    },
    {
        "role": "user",
        "content": "Bro what is 140 times 4",
    },
]

# 3. First call to Ollama
response = ollama.chat(
    model="qwen2.5-coder:7b",
    messages=messages,
    tools=tools_schema,
)

# Keep track of conversation history
messages.append(response["message"])

# 4. Check for native tool calls or parse raw JSON fallback
tool_calls = response["message"].get("tool_calls")

if tool_calls:
    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        function_args = tool_call["function"]["arguments"]

        if function_to_call := available_tools.get(function_name):
            result = function_to_call(**function_args)

            messages.append({
                "role": "tool",
                "content": str(result),
                "name": function_name,
            })

    final_response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=messages,
    )

    print("AIDZ Output:")
    print(final_response["message"]["content"])

else:
    # Fallback logic: If the model output raw JSON into the text content, parse it with json.loads
    content = response["message"]["content"].strip()

    if content.startswith("{") and "name" in content:
        try:
            parsed = json.loads(content)
            func_name = parsed.get("name")
            args = parsed.get("arguments", {})

            if func_to_call := available_tools.get(func_name):
                result = func_to_call(**args)

                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "name": func_name,
                })

                final_response = ollama.chat(
                    model="qwen2.5-coder:7b",
                    messages=messages,
                )
                print("AIDZ Output (via JSON fallback):")
                print(final_response["message"]["content"])

        except json.JSONDecodeError:
            print("Failed to parse string output as JSON:")
            print(content)
    else:
        print("AIDZ Output:")
        print(content)