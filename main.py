import sys
from config import BOT_NAME, DEFAULT_MODEL, OLLAMA_HOST
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tools import available_tools
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
    user_input = " ".join(sys.argv[1:]).strip()
    if not user_input:
        user_input = input("Please provide a prompt: ")

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
                # Use the .invoke() method and pass the args dictionary directly
                output = tool_func.invoke(toolArgs) 
                print(output) 
    else:
        
        print(response.content.strip())

if __name__ == "__main__":
    main()