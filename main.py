import json
import ollama
from config import BOT_NAME, OLLAMA_HOST
from bot_runtime import (
    build_messages,
    check_ollama_connection,
    execute_tool_calls,
    get_model_name,
    get_tool_schemas,
)

# Initialize the Ollama Client directly with your host string
client = ollama.Client(host=OLLAMA_HOST)

is_connected, connection_message = check_ollama_connection()
if not is_connected:
    print(connection_message)
    raise SystemExit(1)

messages = build_messages("Count to 5 tacos")

# Call chat using the configured client
response = client.chat(
    model=get_model_name(),
    messages=messages,
    tools=get_tool_schemas()
)

messages.append(response["message"])

tool_calls = response["message"].get("tool_calls") or []
content_str = response["message"].get("content", "").strip()

if not tool_calls and content_str.startswith("{") and content_str.endswith("}"):
    try:
        data = json.loads(content_str)
        if "name" in data and "arguments" in data:
            tool_calls = [{"function": data}]
    except json.JSONDecodeError:
        pass

print(f"{BOT_NAME} Output:")
outputs = execute_tool_calls(messages, tool_calls)
if not outputs:
    print(content_str)