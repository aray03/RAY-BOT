import sys
from config import BOT_NAME, DEFAULT_MODEL, OLLAMA_HOST, USE_SEARXNG
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tools import available_tools
from tools.searxng import search_searxng
from bot_runtime import check_ollama_connection, prepare_tool_args

SYSTEM_PROMPT = (
    f"You are a helpful computer assistant named '{BOT_NAME}'. "
    "Always use available tools when math or tool requests are asked. Do not attempt to calculate or answer math questions yourself. "
)


def build_messages(user_input: str, use_tools: bool):
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    if use_tools:
        messages.append(HumanMessage(content=user_input))
        return messages

    prompt_content = user_input
    if USE_SEARXNG:
        web_context = search_searxng(user_input)
        prompt_content = f"""Web Search Context:
{web_context}

User Question: {user_input}


Guidelines:
- Use the web search context to answer the user's question.
- Don't mention anything about the web search context in your answer, such as saying 'According to the web search results...'.
- Don't mention anything about the web search engine or SearXNG in your answer.
- Don't mention anything about sources unless it is specifically relevant to the answer or asked specifically
"""

    print("Using Search Results")
    messages.append(HumanMessage(content=prompt_content))
    return messages


def call_model(llm, messages, use_tools):
    if use_tools:
        llm = llm.bind_tools(list(available_tools.values()))
    return llm.invoke(messages)


def emit_response(response, user_input: str):
    if response.tool_calls:
        outputs = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_func = available_tools.get(tool_name)

            if tool_func:
                tool_args = prepare_tool_args(tool_name, tool_call["args"], user_input)
                outputs.append(tool_func.invoke(tool_args))

        for output in outputs:
            print(output)
        return

    content = response.content.strip() if getattr(response, "content", None) else ""
    if content:
        print(content)


def main():
    # 1. Make sure Ollama is running so we can call it
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

    # 3. Initialize LangChain Ollama model & bind tools
    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0,
    )

    # 4. Build prompt and invoke LLM
    messages = build_messages(user_input, use_tools)
    response = call_model(llm, messages, use_tools)

    # 5. Handle Tool Calls or Direct Content
    emit_response(response, user_input)

if __name__ == "__main__":
    main()