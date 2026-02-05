# server.py - Qubrid MCP Server (FIXED)
"""
Qubrid MCP Server - Learning Project
Author: Arya
Date: February 2026
"""

import asyncio
import os
import json
from typing import Sequence
from dotenv import load_dotenv
import aiohttp

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    GetPromptResult,
    PromptMessage,
    Prompt
)

load_dotenv()

app = Server("qubrid-explorer")

QUBRID_API_KEY = os.getenv("QUBRID_API_KEY")
QUBRID_BASE_URL = os.getenv("QUBRID_BASE_URL", "https://platform.qubrid.com/api/v1/qubridai")

_models_cache = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def fetch_models():
    """Fetch available models"""
    global _models_cache
    
    if _models_cache is not None:
        return _models_cache
    
    _models_cache = [
        {"id": "openai/gpt-oss-20b", "description": "GPT OSS 20B model"},
        {"id": "meta-llama/Llama-3.3-70B-Instruct", "description": "Llama 3.3 70B"},
        {"id": "Qwen/Qwen2.5-72B-Instruct", "description": "Qwen 2.5 72B"},
        {"id": "google/gemma-2-27b-it", "description": "Gemma 2 27B"},
        {"id": "mistralai/Mistral-7B-Instruct-v0.3", "description": "Mistral 7B"},
    ]
    return _models_cache


async def query_model(model: str, prompt: str, max_tokens: int = 256, temperature: float = 0.7):
    """Query a Qubrid model"""
    print(f"🔄 Querying {model}...")  # Debug
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{QUBRID_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {QUBRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            },
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            if response.status == 200:
                data = await response.json()
                
                # Handle different response formats
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    print(f"✅ Got response from {model}")  # Debug
                    return content
                elif "response" in data:
                    return data["response"]
                elif "content" in data:
                    return data["content"]
                else:
                    print(f"⚠️ Unexpected response format: {list(data.keys())}")
                    return f"Response received but format unexpected: {json.dumps(data, indent=2)}"
            else:
                error = await response.text()
                print(f"❌ API Error {response.status}: {error[:200]}")  # Debug
                raise Exception(f"API Error {response.status}: {error}")


# ============================================================================
# RESOURCES
# ============================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="qubrid://models/list",
            name="Available Models",
            description="List of all Qubrid models",
            mimeType="application/json"
        ),
        Resource(
            uri="qubrid://info/api",
            name="API Information",
            description="API configuration",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    
    print(f"📖 Resource requested: {uri}")  # Debug
    
    if uri == "qubrid://models/list":
        models = await fetch_models()
        result = json.dumps({
            "total": len(models),
            "models": models
        }, indent=2)
        print(f"✅ Returning model list")  # Debug
        return result
    
    elif uri == "qubrid://info/api":
        result = json.dumps({
            "base_url": QUBRID_BASE_URL,
            "api_key_configured": QUBRID_API_KEY is not None,
            "status": "✅ Ready" if QUBRID_API_KEY else "❌ No API key"
        }, indent=2)
        print(f"✅ Returning API info")  # Debug
        return result
    
    else:
        print(f"❌ Unknown URI: {uri}")  # Debug
        raise ValueError(f"Unknown URI: {uri}")


# ============================================================================
# TOOLS
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="query_model",
            description="Query a Qubrid model with a prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model ID",
                        "default": "openai/gpt-oss-20b"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Prompt"
                    },
                    "max_tokens": {
                        "type": "integer",
                        "default": 256
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="compare_models",
            description="Compare multiple models",
            inputSchema={
                "type": "object",
                "properties": {
                    "models": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "prompt": {
                        "type": "string"
                    }
                },
                "required": ["models", "prompt"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    """Execute a tool"""
    
    print(f"🔧 Tool called: {name}")  # Debug
    
    if name == "query_model":
        model = arguments.get("model", "openai/gpt-oss-20b")
        prompt = arguments["prompt"]
        max_tokens = arguments.get("max_tokens", 256)
        
        try:
            response = await query_model(model, prompt, max_tokens)
            
            result = f"""🤖 Model: {model}
📝 Prompt: {prompt}

💬 Response:
{response}

⚙️ Settings: max_tokens={max_tokens}
"""
            return [TextContent(type="text", text=result)]
        
        except Exception as e:
            error_msg = f"❌ Error querying {model}: {str(e)}"
            print(error_msg)  # Debug
            return [TextContent(type="text", text=error_msg)]
    
    elif name == "compare_models":
        models = arguments["models"]
        prompt = arguments["prompt"]
        
        try:
            tasks = [query_model(model, prompt, 256) for model in models]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            comparison = f"📊 Model Comparison\n📝 Prompt: {prompt}\n\n"
            
            for model, response in zip(models, responses):
                comparison += f"{'='*60}\n🤖 {model}\n{'-'*60}\n"
                
                if isinstance(response, Exception):
                    comparison += f"❌ Error: {str(response)}\n"
                else:
                    comparison += f"{response}\n"
                
                comparison += "\n"
            
            return [TextContent(type="text", text=comparison)]
        
        except Exception as e:
            error_msg = f"❌ Comparison error: {str(e)}"
            print(error_msg)  # Debug
            return [TextContent(type="text", text=error_msg)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


# ============================================================================
# PROMPTS
# ============================================================================

@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List prompt templates"""
    return [
        Prompt(
            name="test_model",
            description="Quick test prompt",
            arguments=[
                {"name": "topic", "description": "Topic", "required": True}
            ]
        ),
        Prompt(
            name="explain_concept",
            description="Explain a concept",
            arguments=[
                {"name": "concept", "description": "Concept", "required": True}
            ]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
    """Get prompt template"""
    
    if name == "test_model":
        topic = arguments["topic"]
        return GetPromptResult(
            description=f"Test about {topic}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Explain {topic} in 2-3 sentences."
                    )
                )
            ]
        )
    
    elif name == "explain_concept":
        concept = arguments["concept"]
        return GetPromptResult(
            description=f"Explain {concept}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Explain {concept} simply with an example."
                    )
                )
            ]
        )
    
    raise ValueError(f"Unknown prompt: {name}")


# ============================================================================
# SERVER STARTUP
# ============================================================================

async def main():
    """Run the MCP server"""
    print("=" * 60)
    print("🚀 QUBRID MCP SERVER")
    print("=" * 60)
    print(f"📡 API: {QUBRID_BASE_URL}")
    print(f"🔑 Key: {'✅ Configured' if QUBRID_API_KEY else '❌ Missing'}")
    print("=" * 60)
    
    if not QUBRID_API_KEY:
        print("\n❌ ERROR: Set QUBRID_API_KEY in .env")
        return
    
    print("\n✅ Server ready - waiting for connections...")
    print("📝 Debug logging enabled\n")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")