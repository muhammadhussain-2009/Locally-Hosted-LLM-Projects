# Headroom Context Optimization Demo

This app demonstrates how to use **Headroom** to dramatically reduce token usage when working with AI agents and tool-heavy LLM applications. Unlike simple truncation, Headroom uses statistical analysis to keep what matters and compress what doesn't.

## What is Headroom?

Headroom is an intelligent context compression framework that helps you reduce LLM costs by 50-90% while maintaining the quality of responses. By intelligently filtering and compressing tool outputs, context windows, and conversation history, Headroom ensures your LLM applications stay within budget without sacrificing performance.

## 🎯 Key Benefits of Headroom

- **Dramatic Cost Reduction**: Reduce token consumption by up to 93.7% (as demonstrated in this project)
- **Intelligent Compression**: Keeps critical information while removing noise
- **Maintains Quality**: Statistical analysis ensures important data is preserved
- **Provider Agnostic**: Works with OpenAI, Anthropic, Google, and any OpenAI-compatible API
- **Zero Performance Loss**: Same quality answers with significantly fewer tokens
- **Seamless Integration**: Drop-in replacement for your existing LLM workflows

## ✨ Features

### SmartCrusher
Statistical compression of JSON tool outputs that intelligently keeps:
- First items (context)
- Last items (recency)
- Anomalies (errors, exceptions, non-standard entries)
- Query-relevant matches

### CacheAligner
Stabilizes prefixes for better provider-side caching support across:
- OpenAI
- Anthropic
- Google Cloud AI

### RollingWindow
Manages context limits intelligently without breaking tool call/response pairing

### Code-Aware Compression
AST-based compression using tree-sitter for intelligent code reduction

### LLMLingua-2 Integration
Optional ML-based compression for up to 20x additional compression

### Memory System
Persistent, LLM-driven memory with zero-latency inline extraction

### CCR (Compress-Cache-Retrieve)
Reversible compression—LLM requests original data when needed for full context recovery

## 📊 Benchmark Results

This demo shows real-world token savings:

```
Baseline tokens:   ~5,685
Compressed tokens: ~357
Tokens saved:      ~5,328
Savings:           93.7%
```

**Same answer quality. 93.7% fewer tokens.**

The demo compresses 100 log entries down to just 6 relevant entries while maintaining the ability to answer critical questions about what caused the outage, error codes, and fixes needed.

## 🚀 Installation

### Using pip

```bash
pip install headroom-ai[all]
```

### Using UV

```bash
uv pip install headroom-ai[all]
```
## 🔧 Framework Integration

### LangChain Integration

```python
from headroom import SmartCrusher
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

# Initialize SmartCrusher
crusher = SmartCrusher()

# Use in your tool definitions
@tool
def my_tool(data: str) -> str:
    """My custom tool."""
    # Compress the data before returning
    compressed = crusher.compress(data)
    return compressed

# Integrate with your agent
agent_executor = create_tool_calling_agent(
    llm=your_llm,
    tools=[my_tool],
    prompt=prompt
)

# Process with Headroom compression
result = agent_executor.invoke({"input": "your query"})
```

### Agno Integration

```python
from headroom import Headroom
from agno.agent import Agent
from agno.models import OpenAI

# Initialize Headroom
headroom = Headroom()

# Create agent with Headroom compression
agent = Agent(
    model=OpenAI(),
    tools=[your_tools],
    # Use Headroom's compression for context
    system_prompt=headroom.optimize_prompt(system_prompt)
)

# Run with automatic compression
response = agent.run("your query")
```

### OpenAI Integration

```python
from openai import OpenAI
from headroom import SmartCrusher

client = OpenAI()
crusher = SmartCrusher()

# Prepare your tool outputs
tool_results = [...]  # Your tool outputs

# Compress before sending to LLM
compressed_results = crusher.compress(tool_results)

# Send to OpenAI with compressed context
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": f"Analyze this data: {compressed_results}"
        }
    ]
)
```

### Google AI Integration

```python
from headroom import Headroom
import google.generativeai as genai

# Initialize Headroom
headroom = Headroom()

# Configure Google AI
genai.configure(api_key="your-api-key")
model = genai.GenerativeModel("gemini-pro")

# Compress your context
context = headroom.compress(your_data)

# Send to Google AI
response = model.generate_content(f"Analyze: {context}")
```

### Using Headroom as a Proxy

Run Headroom as a proxy to automatically compress all requests:

```bash
headroom proxy --port 8787
```

#### Claude (Anthropic)

```bash
ANTHROPIC_BASE_URL=http://localhost:8787 claude
```

#### Cursor or Any OpenAI-Compatible Client

```bash
OPENAI_BASE_URL=http://localhost:8787/v1 cursor
```

The proxy automatically intercepts and compresses:
- Tool outputs
- Context windows
- Conversation history
- System prompts

## 🏃 Running the Demo

Run the included demo to see Headroom in action:

```bash
python demo.py
```

This will show:
1. **Baseline**: All 100 log entries sent to the LLM
2. **With Headroom**: Compressed to 6 relevant entries
3. **Savings**: 93.7% token reduction

## 💡 Best Use Cases

- **Log Analysis**: Compress massive log files while keeping critical errors and patterns
- **API Monitoring**: Reduce noise from repetitive API responses
- **Document Processing**: Extract and compress relevant sections from large documents
- **Code Analysis**: Intelligently compress code while preserving logic and structure
- **Data Processing Pipelines**: Reduce token usage in multi-step data transformation workflows
- **Retrieval Augmented Generation (RAG)**: Compress retrieved documents for better efficiency
- **Conversation History Management**: Keep conversation threads concise without losing context
- **Agent Tool Outputs**: Automatically compress tool responses in agentic workflows

## 🔒 Safety Guarantees

Headroom provides the following safety guarantees:

- **No Data Loss**: Critical information is never lost; only redundant or low-signal data is compressed
- **Reversible Compression**: The CCR (Compress-Cache-Retrieve) feature allows LLMs to request original data when needed
- **Anomaly Preservation**: Errors, exceptions, and unusual patterns are always kept
- **Query Awareness**: Compression respects your query context to keep relevant information
- **Audit Trail**: Full logging of what was compressed and why
- **Provider Compatibility**: Works seamlessly with all major LLM providers' safety mechanisms

## 📚 Resources

- **Official GitHub**: https://github.com/chopratejas/headroom
- **PyPI Package**: https://pypi.org/project/headroom-ai/
- **Documentation**: https://headroom.ai/docs
- **GitHub Issues**: Report bugs and request features

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/headroom.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install development dependencies: `pip install -e ".[dev]"`

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and add tests
3. Run tests: `pytest`
4. Commit with clear messages: `git commit -m "Add feature: description"`
5. Push to your fork and create a Pull Request

### Contribution Areas

- **Bug Fixes**: Report and fix issues
- **Features**: Propose and implement new compression strategies
- **Documentation**: Improve guides and API documentation
- **Examples**: Add new integration examples
- **Performance**: Optimize compression algorithms
- **Tests**: Improve test coverage

### Code Standards

- Follow PEP 8 style guide
- Add type hints to new functions
- Include docstrings
- Write tests for new features
- Update documentation as needed

## 🎯 What's Next with This Project?

This demo is a starting point. Here are ways to expand and customize it:

### Immediate Next Steps

1. **Integrate with Your Own Data**: Replace the demo logs with your real tool outputs
2. **Benchmark Your Workload**: Run Headroom against your actual use cases to measure savings
3. **Deploy the Proxy**: Use the proxy setup in your production pipeline for automatic compression
4. **Configure Framework Integration**: Choose your preferred framework (LangChain, Agno, etc.) and integrate Headroom

### Advanced Optimizations

1. **Custom Compression Rules**: Define domain-specific compression strategies for your tools
2. **ML-Based Compression**: Enable LLMLingua-2 for additional 20x compression on top of SmartCrusher
3. **Memory System Setup**: Implement persistent memory with zero-latency inline extraction
4. **CCR Workflows**: Set up reversible compression for retrieval of original data when needed
5. **Caching Strategy**: Combine CacheAligner with provider-side caching for cumulative benefits

### Production Deployment

1. **Multi-Model Strategy**: Optimize compression for different LLM models (GPT-4, Claude, Gemini, etc.)
2. **Cost Tracking**: Monitor and track token savings across your entire application
3. **Performance Tuning**: Fine-tune compression parameters for your specific use case
4. **Monitoring**: Set up dashboards to track compression effectiveness

### Community Contribution

1. **Share Your Results**: Post your token savings and use case results
2. **Create Plugins**: Build custom compression plugins for specialized domains
3. **Contribute Integrations**: Add support for additional frameworks or tools
4. **Documentation**: Help improve guides for your use case

---

**Ready to reduce your LLM costs by 90%?** Get started with Headroom today!

```bash
pip install headroom-ai[all]
```

For questions and support, visit the [Headroom GitHub repository](https://github.com/chopratejas/headroom).
