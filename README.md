![Agentic RAG Research Assistant](https://github.com/arun-nivaas/LLM-002-Agentic-Research-Assistant/blob/main/src/research_assistant/assets/banner.png?raw=true)[![Python](https://img.shields.io/badge/Python-3.11%2C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-FF4785)](https://langchain-ai.github.io/langgraph/)[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o%20Mini-412991?logo=openai&logoColor=white)](https://openai.com/)[![Google AI](https://img.shields.io/badge/Google%20AI-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)[![UV](https://img.shields.io/badge/UV-Package%20Manager-DE5FE9)](https://github.com/astral-sh/uv)[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

⭐ Star us on GitHub — it motivates me to keep improving! 🙏😊

## 🚀 About

**Agentic RAG Research Assistant** is an advanced AI-powered research tool built with LangGraph that autonomously orchestrates multi-step research workflows. It combines the power of multiple language models and specialized search agents to gather, analyze, and synthesize information from academic papers, web sources, and knowledge bases.

The system employs a **multi-agent architecture** with distinct responsibilities:

-   **🛡️ Guardrails**: Input validation and safety checks
-   **🧠 Reasoning Engine**: Query understanding and task decomposition (GPT-4o Mini)
-   **📋 Planning Engine**: Sequential execution planning (GPT-4o Mini)
-   **🔍 Specialized Agents**: Domain-specific search (arXiv, Tavily, Wikipedia)
-   **✨ Synthesis Engine**: Context-aware aggregation (Gemini 2.5 Flash)
-   **🔎 Critic Agent**: Quality assurance and validation

Built on **LangGraph's stateful workflow paradigm**, the system ensures:

-   ✅ **Modularity**: Each agent operates independently with clear interfaces
-   ✅ **Observability**: Full tracing with LangSmith integration
-   ✅ **Reliability**: Type-safe data models with Pydantic validation
-   ✅ **Scalability**: Extensible architecture for adding new tools and capabilities 

## 🌟 Key Features

### Intelligence & Reasoning

-   **🧠 Multi-Model Architecture**: Leverages GPT-4o Mini for fast reasoning/planning and Gemini 2.5 Flash for advanced synthesis
-   **🎯 Intent Understanding**: Automatically analyzes queries to identify research objectives
-   **📊 Task Decomposition**: Breaks complex queries into manageable subtasks
-   **🔄 Dynamic Planning**: Creates optimized execution strategies based on query complexity

### Safety & Quality

-   **🛡️ Input Guardrails**: Validates queries for safety, scope, and appropriateness
-   **✅ Pydantic Validation**: Runtime type checking ensures data integrity
-   **🔎 Critic Agent**: Post-synthesis quality control validates accuracy and completeness
-   **⚠️ Error Handling**: Graceful degradation with fallback mechanisms

### Data Sources

-   **📚 Academic Papers**: arXiv integration with smart query optimization
-   **🌐 Web Search**: Tavily API for recent news and articles
-   **📖 General Knowledge**: Wikipedia for background information
-   **🔌 Extensible**: Easy integration of additional data sources

### Developer Experience

-   **📊 LangSmith Tracing**: Complete observability of agent interactions
-   **⚡ UV Package Manager**: 10-100x faster dependency management
-   **🧪 Comprehensive Tests**: Extensive test coverage for reliability
-   **📝 Type Hints**: Full typing support for better IDE integration

  
## 🏗️ Architecture

![Architecture](https://github.com/arun-nivaas/LLM-002-Agentic-Research-Assistant/blob/main/src/research_assistant/assets/architecture.png?raw=true)

## Key Components

1. **Guardrails**: Validates input queries for safety, relevance, and appropriate scope before processing

2. **Reasoning Node (GPT-4o Mini)**: Analyzes user intent, identifies subtasks, and selects appropriate tools

3. **Planning Node (GPT-4o Mini)**: Creates sequential execution plan with specific queries for each tool

4. **Agent Executors**: Specialized agents for academic papers (arXiv), web search (Tavily), and general knowledge (Wikipedia)

5. **Synthesis Node (Gemini 2.5 Flash)**: Aggregates and synthesizes findings into coherent, comprehensive responses with superior context understanding

6. **Critic Agent**: Evaluates the synthesized output for quality, accuracy, completeness, and coherence before delivery

## 🚀 Installation

### Prerequisites

**System Requirements:**
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for API calls

**Required API Keys:**
- [OpenAI API Key](https://platform.openai.com/api-keys) - For GPT-4o Mini (reasoning & planning)
- [Google AI API Key](https://makersuite.google.com/app/apikey) - For Gemini 2.5 Flash (synthesis)
- [Tavily API Key](https://tavily.com/) - For web search capabilities

**Optional:**
- [LangSmith API Key](https://smith.langchain.com/) - For tracing and observability (recommended for debugging)

### Method 1: Using UV (Recommended - Fast!)

UV is 10-100x faster than pip for dependency management.
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/arun-nivaas/agentic-rag-research.git
cd agentic-rag-research

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

---

### Method 2: Using pip
```bash
# Clone the repository
git clone https://github.com/arun-nivaas/agentic-rag-research.git
cd agentic-rag-research

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

---

### Method 3: Using Docker
```bash
# Build the Docker image
docker build -t agentic-rag-assistant .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_key \
  -e GOOGLE_API_KEY=your_google_key \
  -e TAVILY_API_KEY=your_tavily_key \
  agentic-rag-assistant
```

---

### Configuration

1. **Create environment file:**
```bash
cp .env.example .env  # Or create new .env file
```

2. **Add your API keys to `.env`:**
```env
# Required
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
TAVILY_API_KEY=tvly-...

# Optional (for tracing)
LANGSMITH_API_KEY=ls...
LANGSMITH_PROJECT=agentic-rag-research
LANGCHAIN_TRACING_V2=true
```

3. **Verify installation:**
```bash
python -c "import langgraph; print('✅ Installation successful!')"
```

---

### Troubleshooting

**Issue: `ModuleNotFoundError`**
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate
pip install -e .
```

**Issue: API Key Errors**
```bash
# Check if .env file is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

**Issue: Permission Denied (UV installation)**
```bash
# Try adding UV to your PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
