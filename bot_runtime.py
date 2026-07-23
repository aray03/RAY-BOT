from __future__ import annotations

from urllib.error import URLError
from urllib.request import urlopen

from config import BOT_NAME, DEFAULT_MODEL, OLLAMA_HOST
from tools import available_tools, get_tool_spec, tools_schema


SYSTEM_PROMPT = (
    f"You are a helpful computer assistant named '{BOT_NAME}'. "
    "Use available tools when math or tool requests are asked. "
    "Do not call the model again after a tool runs; the tool output is the response. "
    "Never output raw JSON parameters."
)


def setup_ollama_host() -> None:
    import os

    os.environ["OLLAMA_HOST"] = OLLAMA_HOST


def check_ollama_connection(timeout: float = 2.0) -> tuple[bool, str]:
    try:
        with urlopen(f"{OLLAMA_HOST}/api/tags", timeout=timeout) as response:
            if response.status == 200:
                return True, "Ollama is reachable."
    except URLError as error:
        return False, f"Failed to connect to Ollama at {OLLAMA_HOST}: {error.reason}"
    except Exception as error:
        return False, f"Failed to connect to Ollama at {OLLAMA_HOST}: {error}"

    return False, f"Failed to connect to Ollama at {OLLAMA_HOST}."


def build_messages(user_text: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]


def get_model_name() -> str:
    return DEFAULT_MODEL


def get_tool_schemas() -> list[dict]:
    return tools_schema


def execute_tool_calls(messages: list[dict], tool_calls: list[dict] | None) -> list[str]:
    outputs: list[str] = []
    if not tool_calls:
        return outputs

    user_text = ""
    for message in reversed(messages):
        if message.get("role") == "user":
            user_text = str(message.get("content", ""))
            break

    for tool_call in tool_calls:
        function_info = tool_call.get("function", {})
        function_name = function_info.get("name")
        function_args = function_info.get("arguments", {}) or {}

        function_to_call = available_tools.get(function_name)
        if function_to_call is None:
            continue

        tool_spec = get_tool_spec(function_name) or {}
        tool_schema_params = (
            tool_spec.get("schema", {})
            .get("function", {})
            .get("parameters", {})
            .get("properties", {})
        )

        # Only inject user_text if the tool schema explicitly defines it!
        if "user_text" in tool_schema_params:
            if "user_text" in function_args and not function_args["user_text"]:
                function_args["user_text"] = user_text
            else:
                function_args.setdefault("user_text", user_text)
        elif "user_text" in function_args:
            # If the model mistakenly passed user_text to a tool that doesn't accept it, remove it
            function_args.pop("user_text", None)

        tool_output = str(function_to_call(**function_args))
        messages.append({"role": "tool", "content": tool_output, "name": function_name})
        outputs.append(tool_output)

        if not tool_spec.get("terminal", True):
            continue

    return outputs;
