from __future__ import annotations
from urllib.error import URLError
from urllib.request import urlopen
from config import OLLAMA_HOST
from tools import get_tool_spec

def check_ollama_connection(timeout: float = 2.0) -> tuple[bool, str]:
    """Verifies that the Ollama host is online."""
    try:
        with urlopen(f"{OLLAMA_HOST}/api/tags", timeout=timeout) as response:
            if response.status == 200:
                return True, "Ollama is reachable."
    except URLError as error:
        return False, f"Failed to connect to Ollama at {OLLAMA_HOST}: {error.reason}"
    except Exception as error:
        return False, f"Failed to connect to Ollama at {OLLAMA_HOST}: {error}"

    return False, f"Failed to connect to Ollama at {OLLAMA_HOST}."


def prepare_tool_args(tool_name: str, args: dict, user_text: str) -> dict:
    """
    Ensures `user_text` parameter logic is safely injected or pruned 
    based on the tool's defined schema.
    """
    clean_args = dict(args)
    tool_spec = get_tool_spec(tool_name) or {}
    tool_schema_params = (
        tool_spec.get("schema", {})
        .get("function", {})
        .get("parameters", {})
        .get("properties", {})
    )

    if "user_text" in tool_schema_params:
        if not clean_args.get("user_text"):
            clean_args["user_text"] = user_text
    else:
        clean_args.pop("user_text", None)

    return clean_args