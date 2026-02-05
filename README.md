# MCP Learning Project: Qubrid API Server

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-Anthropic-purple.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 🎯 Project Overview

A hands-on implementation of an **MCP (Model Context Protocol) server** that exposes Qubrid's AI models through a standardized interface. This project demonstrates:

- ✅ **MCP Architecture** - Resources, Tools, and Prompts
- ✅ **Async Programming** - Parallel execution with `asyncio.gather()`
- ✅ **API Integration** - Real-world authentication and error handling
- ✅ **Clean Code** - Professional project structure and documentation

### What is MCP?

MCP is like **USB for AI applications** - a universal protocol that standardizes how AI systems connect to data sources and tools. Just as USB works with any device, MCP works with any AI client (Claude, LangGraph, custom apps).

---

## 🎨 Features

### 1. Resources (Read-Only Data)

Resources are like a **library catalog** - you can see what's available and read it.
```python
# Available resources:
- qubrid://models/list    # List of AI models
- qubrid://info/api       # API configuration
```

**Example Usage:**
```python
# Client requests resource
content = await session.read_resource("qubrid://models/list")
# Returns JSON with all available models
```

---

### 2. Tools (Executable Functions)

Tools are like **API endpoints** - you call them with parameters and get results.
```python
# Available tools:
- query_model       # Query any Qubrid model
- compare_models    # Compare multiple models in parallel
```

**Example Usage:**
```python
# Query single model
result = await session.call_tool("query_model", {
    "prompt": "Explain quantum computing",
    "model": "openai/gpt-oss-20b"
})

# Compare multiple models (runs in parallel!)
comparison = await session.call_tool("compare_models", {
    "models": ["openai/gpt-oss-20b", "meta-llama/Llama-3.3-70B-Instruct"],
    "prompt": "What is machine learning?"
})
```

---

### 3. Prompts (Reusable Templates)

Prompts are like **email templates** - pre-defined formats you can customize.
```python
# Available prompts:
- test_model         # Quick test prompt
- explain_concept    # Concept explanation template
```

**Example Usage:**
```python
# Get prompt template
prompt = await session.get_prompt("explain_concept", {
    "concept": "async programming"
})
```

---

## 🧠 Key Concepts Explained

### Async Programming: Sequential vs Parallel

**Without Async (Slow):**
```python
# Each query waits for the previous one
result1 = query_model("model1", "prompt")  # 3 seconds
result2 = query_model("model2", "prompt")  # 3 seconds
result3 = query_model("model3", "prompt")  # 3 seconds
# Total: 9 seconds ⏰
```

**With Async (Fast):**
```python
# All queries start simultaneously
tasks = [
    query_model("model1", "prompt"),
    query_model("model2", "prompt"),
    query_model("model3", "prompt")
]
results = await asyncio.gather(*tasks)
# Total: 3 seconds ⚡ (3x faster!)
```

### Real Code Example
```python
# From src/server.py - Compare Models Tool
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "compare_models":
        models = arguments["models"]
        prompt = arguments["prompt"]
        
        # Create tasks for all models
        tasks = [query_model(model, prompt) for model in models]
        
        # Execute ALL in parallel - this is the magic! 🪄
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Format and return comparison
        return format_comparison(models, responses)
```

---

## 📊 Performance Comparison

| Number of Models | Sequential | Parallel (Async) | Speed Gain |
|-----------------|-----------|------------------|------------|
| 2 models        | 6 seconds | 3 seconds        | **2x faster** |
| 3 models        | 9 seconds | 3 seconds        | **3x faster** |
| 5 models        | 15 seconds| 3 seconds        | **5x faster** |

*Assuming 3 seconds per model query*

---

## 💡 Use Cases

### 1. Educational Notebooks
```python
# Before: Manual API calls in every notebook
response = requests.post(
    "https://platform.qubrid.com/api/...",
    headers={"Authorization": "Bearer ..."},
    json={...}
)

# After: Simple MCP interface
async with qubrid_server() as session:
    result = await session.call_tool("query_model", {
        "prompt": "Explain RAG"
    })
```

**Benefits:**
- ✅ Cleaner notebook code
- ✅ Reusable across all notebooks
- ✅ Centralized configuration
- ✅ Easy to update

---

### 2. Multi-Agent Systems
```python
# AutoDev project optimization
async def run_agents_parallel():
    async with qubrid_server() as session:
        # Run 7 agents simultaneously instead of sequentially
        tasks = [
            session.call_tool("code_agent", {...}),
            session.call_tool("review_agent", {...}),
            session.call_tool("test_agent", {...}),
            # ... more agents
        ]
        results = await asyncio.gather(*tasks)
    return results

# Result: 13 minutes → 5 minutes! 🚀
```

---

### 3. Research & Analysis
```python
# Compare multiple models on same task
async def research_topic(topic):
    models = [
        "openai/gpt-oss-20b",
        "meta-llama/Llama-3.3-70B-Instruct",
        "Qwen/Qwen2.5-72B-Instruct"
    ]
    
    # Get all perspectives simultaneously
    comparison = await session.call_tool("compare_models", {
        "models": models,
        "prompt": f"Analyze: {topic}"
    })
    
    return comparison
```

---

## 🔧 API Reference

### Server Endpoints

#### Resources

| URI | Description | Returns |
|-----|-------------|---------|
| `qubrid://models/list` | Available models | JSON array of models |
| `qubrid://info/api` | API configuration | JSON with endpoint info |

#### Tools

**query_model**
```python
Arguments:
  - prompt: str (required)        # Question/instruction for model
  - model: str (optional)         # Model ID, default: "openai/gpt-oss-20b"
  - max_tokens: int (optional)    # Max response length, default: 256

Returns:
  - Formatted response with model output
```

**compare_models**
```python
Arguments:
  - prompt: str (required)        # Same prompt for all models
  - models: list[str] (required)  # List of model IDs to compare

Returns:
  - Side-by-side comparison of all model responses
```

---

## 📁 Project Structure
```
mcp-learning/
├── 📁 src/                      # All Python source code
│   ├── __init__.py              # Package marker
│   ├── server.py                # MCP server (250 lines)
│   ├── client.py                # Test client (100 lines)
│   └── test_quick.py            # Validation tests (80 lines)
│
├── 📄 README.md                 # This file
├── 📄 .env.example              # Environment template
├── 🔒 .env                      # Your secrets (not in git)
├── 📄 .gitignore                # Git ignore rules
└── 📄 pyproject.toml            # Dependencies (UV config)
```

---


## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [UV package manager](https://github.com/astral-sh/uv)
- Qubrid API key ([Get one here](https://platform.qubrid.com))

### Installation
```bash
# 1. Clone repository
git clone https://github.com/aryadoshii-qubrid/mcp-learning.git
cd mcp-learning

# 2. Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Configure API key
cp .env.example .env
nano .env  # Add your QUBRID_API_KEY
```

### Run Tests
```bash
uv run src/test_quick.py
```

Expected output:
```
============================================================
✅ ALL TESTS PASSED
============================================================
```

### Start Server & Client

**Terminal 1 - Start Server:**
```bash
uv run src/server.py
```

**Terminal 2 - Run Client:**
```bash
uv run src/client.py
```

---

## 🤝 Contributing

Contributions welcome! This is a learning project, but improvements are appreciated.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/mcp-learning.git
cd mcp-learning

# Install dependencies
uv sync

# Create feature branch
git checkout -b feature/my-improvement

# Make changes and test
uv run src/test_quick.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/my-improvement
```

---

## 📄 License

This project is for educational purposes. Feel free to use, modify, and learn from it.

---


## ⭐ Star This Repo!

If this project helped you learn MCP and async programming, consider:
- ⭐ Starring the repository
- 🍴 Forking for your own experiments
- 📢 Sharing with others learning AI engineering

---

**Happy Learning! 🎉**
