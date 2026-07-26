import sys
from config import BOT_NAME, DEFAULT_MODEL, OLLAMA_HOST
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tools import available_tools
from tools.normal_prompt import normal_prompt
from bot_runtime import check_ollama_connection, prepare_tool_args

SYSTEM_PROMPT = (
    f"You are a helpful computer assistant named '{BOT_NAME}'. "
    "Always use available tools when math or tool requests are asked. Do not attempt to calculate or answer math questions yourself. "

)

def main():
    # 1. Health check
    is_connected, message = check_ollama_connection()
    if not is_connected:
        print(message)
        sys.exit(1)

    # 2. Extract CLI Input
    cli_args = sys.argv[1:]
    use_tools = False

    if cli_args and cli_args[0] == "-t":
        use_tools = True
        cli_args = cli_args[1:]

    user_input = " ".join(cli_args).strip()
    if not user_input:
        print("Please provide a prompt.")
        sys.exit(0)

    if not use_tools:
        print(normal_prompt(user_input, SYSTEM_PROMPT))
        return

    # 3. Initialize LangChain Ollama model & bind tools
    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0
    ).bind_tools(list(available_tools.values()))

    # 4. Invoke LLM
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input)
    ]

    response = llm.invoke(messages)

    # 5. Handle Tool Calls or Direct Content
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_func = available_tools.get(tool_name)

            if tool_func:
                toolArgs = prepare_tool_args(tool_name, tool_call["args"], user_input)
                output = tool_func.invoke(toolArgs)
                print(output)
    else:
        print(response.content.strip())

if __name__ == "__main__":
    main()