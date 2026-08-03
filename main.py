import sys
from config import BOT_NAME, DEFAULT_MODEL, OLLAMA_HOST, USE_SEARXNG
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tools import available_tools
from tools.normal_prompt import search_searxng
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

    # 3. Initialize LangChain Ollama model & bind tools
    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_HOST,
        temperature=0,
    )

    if not use_tools:
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        if USE_SEARXNG:
            web_context = search_searxng(user_input)
            prompt_with_context = f"""Web Search Context:
{web_context}

User Question: {user_input}


Guidelines:
- Use the web search context to answer the user's question.
- Don't mention anything about the web search context in your answer, such as saying 'According to the web search results...'.
- Don't mention anything about the web search engine or SearXNG in your answer.
- Don't mention anything about sources unless it is specifically relevant to the answer or asked specifically
"""
            messages.append(HumanMessage(content=prompt_with_context))
        else:
            messages.append(HumanMessage(content=user_input))

        response = llm.invoke(messages)
        print(response.content.strip())
        return

    llm = llm.bind_tools(list(available_tools.values()))

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