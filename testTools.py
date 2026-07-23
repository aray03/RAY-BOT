import os
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

import json
import ollama

from tools import available_tools, tools_schema

messages = [
    {
        "role": "system",
        "content": "You are my helpful computer assistant named 'AIDZ'. Use available tools when math is requested.",
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
            print("Failed to parse output:")
            print(content)
    else:
        print("AIDZ Output:")
        print(content)