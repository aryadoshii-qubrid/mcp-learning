# MCP Learning Project: Qubrid API Server


## 🎯 Project Overview

This project demonstrates the implementation of an MCP (Model Context Protocol) server that exposes Qubrid's AI models through a standardized interface. Built as a learning exercise to understand:

- MCP architecture (Resources, Tools, Prompts)
- Async programming patterns with Python
- Real API integration with authentication
- Client-server communication

## 🚀 Features

### MCP Primitives Implemented

- **Resources**: Read-only data access
  - `qubrid://models/list` - Available AI models
  - `qubrid://info/api` - API configuration

- **Tools**: Executable functions
  - `query_model` - Query any Qubrid model with a prompt
  - `compare_models` - Compare responses from multiple models (parallel execution)

- **Prompts**: Reusable templates
  - `test_model` - Quick test prompt template
  - `explain_concept` - Concept explanation template

### Key Technical Highlights

✅ **Async Patterns**: Parallel model queries using `asyncio.gather()`  
✅ **API Integration**: Qubrid platform authentication and chat completions  
✅ **Error Handling**: Robust error handling and debugging  
✅ **UV Package Manager**: Modern Python dependency management  
✅ **Clean Architecture**: Separation of concerns (server, client, tests)


## 🎮 Usage

### Start the MCP Server

**Terminal 1:**
```bash
uv run server.py
```

Output:
```
============================================================
🚀 QUBRID MCP SERVER
============================================================
📡 API: https://platform.qubrid.com/api/v1/qubridai
🔑 Key: ✅ Configured
============================================================

✅ Server ready - waiting for connections...
```

### Run the Test Client

**Terminal 2:**
```bash
uv run client.py
```

The client will demonstrate all MCP primitives:
1. List available resources
2. Read resource data
3. List available tools
4. Execute tools (query models)
5. Compare multiple models (async parallel execution)
6. Use prompt templates

## 🧠 Key Concepts Learned

### 1. MCP Architecture
```python
# Resources - Read-only data
@app.list_resources()
async def list_resources():
    return [Resource(...)]

# Tools - Executable functions
@app.call_tool()
async def call_tool(name, arguments):
    if name == "query_model":
        return await query_model(...)
```

### 2. Async Patterns
```python
# Sequential (SLOW)
result1 = await query_model("model1", prompt)  # 3s
result2 = await query_model("model2", prompt)  # 3s
# Total: 6 seconds

# Parallel (FAST)
results = await asyncio.gather(
    query_model("model1", prompt),
    query_model("model2", prompt)
)
# Total: 3 seconds
```

### 3. API Integration
```python
async with aiohttp.ClientSession() as session:
    async with session.post(
        f"{QUBRID_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {QUBRID_API_KEY}"},
        json={"model": model, "messages": messages}
    ) as response:
        return await response.json()
```

## 🎯 Applications

### Educational Use
- Foundation for Qubrid educational notebooks
- LangGraph integration examples
- Multi-agent system demonstrations

### Production Patterns
- Reusable MCP server for Qubrid API
- Standardized interface for any MCP client
- Template for building custom MCP servers

### Performance Optimization
- Parallel model queries reduce latency
- Can be applied to multi-agent systems like AutoDev
- Demonstrates async best practices

## 📊 Performance

**Sequential vs Parallel Comparison:**

| Models | Sequential | Parallel | Improvement |
|--------|-----------|----------|-------------|
| 2      | 6s        | 3s       | 2x faster   |
| 3      | 9s        | 3s       | 3x faster   |
| 5      | 15s       | 3s       | 5x faster   |

*Assuming 3 seconds per model query*

## 📁 Project Structure
```
mcp-learning/
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── pyproject.toml       # UV dependencies
├── server.py            # MCP server (250 lines)
├── client.py            # Test client (80 lines)
└── test_quick.py        # Validation tests (60 lines)
```

## 📋 Requirements

- Python 3.10+
- UV package manager
- Qubrid API key

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/aryadoshii-qubrid/mcp-learning.git
cd mcp-learning
```

### 2. Install Dependencies
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Configure API Key
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Qubrid API key
nano .env
```

Your `.env` should look like:
```bash
QUBRID_API_KEY=qubrid_sk_your_actual_key_here
QUBRID_BASE_URL=https://platform.qubrid.com/api/v1/qubridai
```

## 🧪 Testing

Run the validation tests:
```bash
uv run test_quick.py
```

Expected output:
```
============================================================
✅ ALL TESTS PASSED
============================================================
```

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Qubrid Platform](https://platform.qubrid.com/)
- [Python Asyncio Guide](https://docs.python.org/3/library/asyncio.html)
- [UV Package Manager](https://github.com/astral-sh/uv)

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 👨‍💻 Author

**Arya Doshi**  
Generative AI Engineer @ QubridAI  
Final Year Student, VIT Pune

**LinkedIn:** [Connect with Arya](https://linkedin.com/in/arya-doshi)  
**GitHub:** [@aryadoshii-qubrid](https://github.com/aryadoshii-qubrid)

## 🙏 Acknowledgments

- QubridAI team for platform access
- Anthropic for MCP specification
- Python async community for excellent documentation

---

**⭐ If this helped you learn MCP, consider starring the repo!**
