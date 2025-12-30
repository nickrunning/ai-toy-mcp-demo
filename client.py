import asyncio
import os
import sys
from contextlib import AsyncExitStack

from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# -- Configuration --
API_KEY = os.environ.get("GOOGLE_API_KEY")
SERVER_SCRIPT = os.path.join(os.getcwd(), "server.py")
HISTORY_FILE = "chat_history.txt"

if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not found.")
    print("Please set it: export GOOGLE_API_KEY=your_key_here")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

async def run_client():
    # Define server parameters
    # We use the same python interpreter to run the server script
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT],
        env=None
    )

    async with AsyncExitStack() as stack:
        # Connect to MCP Server
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

        # Convert MCP tools to Gemini tools format
        gemini_tools = []
        for t in mcp_tools:
            gemini_tools.append(types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name=t.name,
                    description=t.description,
                    parameters=t.inputSchema
                )
            ]))
        
        # Load history and convert to Gemini format
        gemini_history = []
        if os.path.exists(HISTORY_FILE):
             try:
                with open(HISTORY_FILE, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("User: "):
                            gemini_history.append(types.Content(role="user", parts=[types.Part(text=line[6:].strip())]))
                        elif line.startswith("AI: "):
                            gemini_history.append(types.Content(role="model", parts=[types.Part(text=line[4:].strip())]))
                print(f"Loaded {len(gemini_history)} turns of history.")
             except Exception as e:
                 print(f"Error loading history: {e}")

        # Start Chat Session
        # Using gemini-2.5-flash as it is more stable and has higher quota availability
        # gemini-2.0-flash-exp might have a quota limit of 0 for some projects.
        chat = client.chats.create(
            model="gemini-2.5-flash",
            history=gemini_history
        )
        
        print("\n--- Start Chatting (type 'quit' to exit) ---")
        
        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.lower() in ["quit", "exit"]:
                break
            
            if not user_input.strip():
                continue

            # Send message to Gemini
            try:
                response = chat.send_message(
                    user_input,
                    config=types.GenerateContentConfig(
                        tools=gemini_tools
                    )
                )
            except Exception as e:
                print(f"Error from Gemini: {e}")
                continue

            # Save to history file (simple log)
            with open(HISTORY_FILE, "a") as f:
                f.write(f"User: {user_input}\n")

            # Handle Tool Calls
            # Gemini might return a tool call. We need to loop until we get a text response.
            while response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
                part = response.candidates[0].content.parts[0]
                fc = part.function_call
                tool_name = fc.name
                tool_args = fc.args
                
                print(f"[MCP] Calling tool: {tool_name} with args: {tool_args}")
                
                # Execute tool on MCP Server
                try:
                    # call_tool expects arguments as a dictionary
                    result = await session.call_tool(tool_name, arguments=dict(tool_args))
                    tool_output = result.content[0].text
                    print(f"[MCP] Result: {tool_output}")
                except Exception as e:
                    tool_output = f"Error calling tool: {e}"
                    print(tool_output)

                # Send result back to Gemini
                # We need to construct a proper ToolResponse
                response = chat.send_message(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=tool_name,
                            response={"result": tool_output}
                        )
                    )
                )

            # Print final model response
            model_text = response.text
            print(f"AI: {model_text}")
            
            with open(HISTORY_FILE, "a") as f:
                f.write(f"AI: {model_text}\n")


if __name__ == "__main__":
    asyncio.run(run_client())
