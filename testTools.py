import json
import os

os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

import ollama
from tools import available_tools, tools_schema


def append_tool_results(messages: list[dict], tool_calls: list[dict] | None) -> bool:
    if not tool_calls:
        return False

    has_results = False
    for tool_call in tool_calls:
        # Access as dict keys instead of object attributes
        function_info = tool_call.get("function", {})
        function_name = function_info.get("name")
        function_args = function_info.get("arguments", {})

        function_to_call = available_tools.get(function_name)
        if function_to_call is None:
            continue

        messages.append(
            {
                "role": "tool",
                "content": str(function_to_call(**function_args)),
                "name": function_name,
            }
        )
        has_results = True

    return has_results


messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful computer assistant named 'RAY-BOT'. "
            "Use available tools when math is requested. "
            "Always respond to the user in a natural, friendly sentence. "
            "Never output raw JSON parameters."
        ),
    },
    {
        "role": "user",
        "content": "Bro what is 140 plus 4",
    },
]

response = ollama.chat(
    model="qwen2.5-coder:7b",
    messages=messages,
    tools=tools_schema,
)

messages.append(response["message"])

# Safely handle tool_calls from response
tool_calls = response["message"].get("tool_calls") or []

# Fallback: Parse inline JSON if the model leaked a tool call inside "content"
content_str = response["message"].get("content", "").strip()
if not tool_calls and content_str.startswith("{") and content_str.endswith("}"):
    try:
        data = json.loads(content_str)
        if "name" in data and "arguments" in data:
            tool_calls = [{"function": data}]
    except json.JSONDecodeError:
        pass

# Run tool execution and re-prompt for natural text
if append_tool_results(messages, tool_calls):
    final_response = ollama.chat(model="qwen2.5-coder:7b", messages=messages)
    print("RAY-BOT Output:")
    print(final_response["message"]["content"].strip())
else:
    print("RAY-BOT Output:")
    print(content_str)