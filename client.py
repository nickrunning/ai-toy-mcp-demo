import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# -- Configuration --
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1") # Default to Qwen/DashScope if not set
MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "qwen-plus") # Default model

SERVER_SCRIPT = os.path.join(os.getcwd(), "server.py")
HISTORY_FILE = "chat_history.txt"

if not API_KEY:
    print("Error: OPENAI_API_KEY environment variable not found.")
    print("Please set it: export OPENAI_API_KEY=your_key_here")
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

async def run_client():
    # Define server parameters
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT],
        env=None
    )

    async with AsyncExitStack() as stack:
        print(f"Connecting to server at {SERVER_SCRIPT}...")
        try:
            stdio_transport = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(stdio_transport[0], stdio_transport[1]))
            await session.initialize()
            print("Connected to MCP Server!")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return

        # List available tools
        tools_result = await session.list_tools()
        mcp_tools = tools_result.tools
        print(f"Available tools: {[t.name for t in mcp_tools]}")

        # Convert MCP tools to OpenAI tools format
        openai_tools = []
        for t in mcp_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema
                }
            })
        
        # Load history
        messages = []
        if os.path.exists(HISTORY_FILE):
             try:
                with open(HISTORY_FILE, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("User: "):
                            messages.append({"role": "user", "content": line[6:].strip()})
                        elif line.startswith("AI: "):
                            messages.append({"role": "assistant", "content": line[4:].strip()})
                print(f"Loaded {len(messages)} turns of history.")
             except Exception as e:
                 print(f"Error loading history: {e}")

        # Prepend system instruction if needed, or rely on model behavior
        # messages.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

        print(f"\n--- Start Chatting with {MODEL_NAME} (type 'quit' to exit) ---")
        
        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.lower() in ["quit", "exit"]:
                break
            
            if not user_input.strip():
                continue

            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Save to history file (simple log)
            with open(HISTORY_FILE, "a") as f:
                f.write(f"User: {user_input}\n")

            # Chat Loop for Tool Calls
            # We loop because the model might emit multiple tool calls in sequence or need results
            
            while True:
                try:
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        tools=openai_tools,
                        tool_choice="auto"  # optional but explicit
                    )
                    
                    response_message = completion.choices[0].message
                except Exception as e:
                    print(f"Error from OpenAI/Qwen: {e}")
                    break

                # If the model wants to call a tool
                if response_message.tool_calls:
                    # Append the model's message (with tool calls) to history
                    messages.append(response_message)
                    
                    for tool_call in response_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        tool_call_id = tool_call.id
                        
                        print(f"[MCP] Calling tool: {tool_name} with args: {tool_args}")
                        
                        # Execute tool on MCP Server
                        try:
                            result = await session.call_tool(tool_name, arguments=tool_args)
                            tool_output = result.content[0].text
                            print(f"[MCP] Result: {tool_output}")
                        except Exception as e:
                            tool_output = f"Error calling tool: {e}"
                            print(tool_output)

                        # Append tool result to history
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": tool_output
                        })
                    
                    # Continue the loop to get the next response from the model (with the tool outputs available)
                    continue
                
                else:
                    # Final response from model (no more tool calls)
                    ai_text = response_message.content
                    print(f"AI: {ai_text}")
                    if ai_text:
                        messages.append({"role": "assistant", "content": ai_text})
                        with open(HISTORY_FILE, "a") as f:
                            f.write(f"AI: {ai_text}\n")
                    break

if __name__ == "__main__":
    asyncio.run(run_client())
