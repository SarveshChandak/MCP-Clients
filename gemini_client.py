## References:
## 1. https://modelcontextprotocol.io/quickstart/client

import sys
import os
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # Load Gemini API key from environment variables

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and available tools"""
        # Fetch available tools from the server
        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
            for tool in response.tools
        ]

        # Convert tools to Gemini function declarations
        function_declarations = [
            {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            }
            for tool in available_tools
        ]

        # Configure Gemini tools
        tools = types.Tool(function_declarations=function_declarations)
        config = types.GenerateContentConfig(tools=[tools])

        # Initial Gemini API call
        genai_response = self.genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=config,
        )

        # Process response and handle function calls
        final_text = []
        tool_results = []

        for candidate in genai_response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    function_call = part.function_call
                    print(function_call, "\n")
                    tool_name = function_call.name
                    tool_args = function_call.args

                    # Call the tool using the MCP session
                    tool_result = await self.session.call_tool(tool_name, tool_args)
                    tool_results.append(f"Tool: {tool_name}, Result: {tool_result.content}")

                    # Add tool result to the conversation
                    final_text.append(f"[Tool {tool_name} Result]: {tool_result.content}")
                else:
                    # Add regular text response
                    final_text.append(part.text)

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() in ['quit', 'exit']:
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    print("Starting MCP Client...")
    asyncio.run(main())

## Use this command to run the client with server script: uv run gemini_client.py "C:/Users/sarve/Documents/Personal Experiments/MCP Experiment/MCP Server/tool_poisoning/tool_poisoning.py"
## Use this command to run the client with server script: uv run gemini_client.py "C:/Users/sarve/Documents/Personal Experiments/MCP Experiment/MCP Server/weather/weather.py"
