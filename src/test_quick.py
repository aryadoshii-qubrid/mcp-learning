# test_quick.py - Quick validation
"""
Quick tests to validate setup
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("🧪 Quick Validation Tests\n")

# Test 1: Environment
print("=" * 60)
print("TEST 1: Environment")
print("=" * 60)
api_key = os.getenv("QUBRID_API_KEY")
base_url = os.getenv("QUBRID_BASE_URL")
print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
print(f"Base URL: {base_url}")
print()

# Test 2: Imports
print("=" * 60)
print("TEST 2: Dependencies")
print("=" * 60)

modules = {
    "mcp.server": "MCP Server",
    "aiohttp": "HTTP Client",
    "dotenv": "Environment Loader"
}

all_good = True
for module, name in modules.items():
    try:
        __import__(module)
        print(f"✅ {name} ({module})")
    except ImportError:
        print(f"❌ {name} ({module})")
        all_good = False

print()

# Test 3: Server Init
print("=" * 60)
print("TEST 3: Server Initialization")
print("=" * 60)
try:
    from server import app
    print(f"✅ Server: {app.name}")
except Exception as e:
    print(f"❌ Error: {e}")
    all_good = False

print()

# Test 4: API Test
if api_key:
    print("=" * 60)
    print("TEST 4: API Connection")
    print("=" * 60)
    
    async def test_api():
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-oss-20b",
                        "messages": [{"role": "user", "content": "Say 'Hello'"}],
                        "max_tokens": 10,
                        "stream": False
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        print(f"✅ API Connected successfully")
                        print(f"✅ Test response received")
                        return True
                    else:
                        text = await response.text()
                        print(f"⚠️ API Status: {response.status}")
                        print(f"Response: {text[:200]}")
                        return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    api_ok = asyncio.run(test_api())
    all_good = all_good and api_ok
    print()

# Summary
print("=" * 60)
if all_good:
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run server: uv run src/server.py")
    print("2. Run client: uv run src/client.py")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED")
    print("=" * 60)
    print("\nFix errors above, then rerun:")
    print("uv run src/test_quick.py")
    sys.exit(1)
