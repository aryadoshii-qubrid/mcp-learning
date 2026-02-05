# client.py - Test MCP Client (Fixed for latest MCP version)
"""
Test client for Qubrid MCP Server
"""

import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession


async def main():
    """Test the MCP server"""
    
    print("🔌 Connecting to Qubrid MCP Server...\n")
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"]
    )
    
    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize connection
            await session.initialize()
            
            print("✅ Connected!\n")
            
            # Test 1: List Resources
            print("=" * 60)
            print("TEST 1: List Resources")
            print("=" * 60)
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"📄 {resource.name}")
                print(f"   URI: {resource.uri}")
                print(f"   Type: {resource.mimeType}\n")
            
            # Test 2: Read a Resource (FIXED)
            print("=" * 60)
            print("TEST 2: Read Model List Resource")
            print("=" * 60)
            try:
                # Use the uri directly, not wrapped in a request object
                content = await session.read_resource(uri="qubrid://models/list")
                print(content.contents[0].text)
            except Exception as e:
                print(f"⚠️ Could not read resource: {e}")
            print()
            
            # Test 3: List Tools
            print("=" * 60)
            print("TEST 3: List Available Tools")
            print("=" * 60)
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"🔧 {tool.name}")
                print(f"   {tool.description}\n")
            
            # Test 4: Call a Tool (FIXED)
            print("=" * 60)
            print("TEST 4: Query a Model")
            print("=" * 60)
            try:
                result = await session.call_tool(
                    name="query_model",
                    arguments={
                        "model": "openai/gpt-oss-20b",
                        "prompt": "What is MCP in one sentence?",
                        "max_tokens": 100
                    }
                )
                print(result.content[0].text)
            except Exception as e:
                print(f"⚠️ Tool call failed: {e}")
            print()
            
            # Test 5: Compare Models
            print("=" * 60)
            print("TEST 5: Compare Models (Async Demo)")
            print("=" * 60)
            try:
                comparison = await session.call_tool(
                    name="compare_models",
                    arguments={
                        "models": ["openai/gpt-oss-20b"],
                        "prompt": "Explain async programming in one sentence"
                    }
                )
                print(comparison.content[0].text)
            except Exception as e:
                print(f"⚠️ Comparison failed: {e}")
            print()
            
            # Test 6: List Prompts
            print("=" * 60)
            print("TEST 6: Prompt Templates")
            print("=" * 60)
            prompts = await session.list_prompts()
            if prompts.prompts:
                for prompt in prompts.prompts:
                    print(f"📝 {prompt.name}: {prompt.description}")
            else:
                print("No prompts available")
            
            print("\n" + "=" * 60)
            print("✅ All tests completed!")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())