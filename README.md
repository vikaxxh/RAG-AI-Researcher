# 🚀 Agentic RAG Research Assistant

**Owner:** Vikash  
**Project:** RAG AI Researcher - An Intelligent Multi-Agent Research System

---

## 📋 Overview

Welcome to the **Agentic RAG Research Assistant** — a sophisticated AI-powered research platform designed and developed by Vikash. This project demonstrates advanced agentic AI capabilities, combining multiple language models with specialized search agents to deliver comprehensive, intelligent research workflows.

Built on cutting-edge technologies including **LangGraph**, **LangChain**, and modern LLMs (GPT-4o Mini, Gemini 2.5 Flash), this system autonomously orchestrates complex research tasks with remarkable accuracy and efficiency.

---

## 💡 Project Vision

This project showcases a production-grade implementation of multi-agent AI architecture, demonstrating:

- **Intelligent Task Decomposition**: Breaking down complex research queries into manageable subtasks
- **Multi-Source Intelligence**: Aggregating data from academic papers, web sources, and knowledge bases
- **Quality Assurance**: Leveraging AI critics to validate synthesis quality
- **Modularity & Scalability**: Building extensible systems that can integrate new tools and capabilities

---

## 🎯 Key Features

### 🧠 Intelligent Architecture
- **Multi-Model System**: Combines GPT-4o Mini for reasoning/planning with Gemini 2.5 Flash for synthesis
- **Intent Recognition**: Automatically understands user research objectives
- **Dynamic Planning**: Creates optimized execution strategies based on query complexity
- **Modular Design**: Each component operates independently with clear interfaces

### 🛡️ Safety & Reliability
- **Input Validation**: Comprehensive guardrails for query safety and appropriateness
- **Type Safety**: Pydantic validation ensures data integrity throughout the pipeline
- **Quality Control**: Critic agent validates output accuracy and completeness
- **Error Handling**: Graceful degradation with intelligent fallbacks

### 🔍 Multi-Source Research
- **📚 Academic Papers**: arXiv integration for scholarly research
- **🌐 Web Search**: Tavily API for current news and articles
- **📖 Knowledge Base**: Wikipedia integration for foundational knowledge
- **🔌 Extensible Framework**: Easy addition of new data sources

### 👨‍💻 Developer Experience
- **📊 Full Observability**: LangSmith integration for complete tracing
- **⚡ Fast Setup**: UV package manager for 10-100x faster dependency management
- **🧪 Comprehensive Testing**: Extensive test coverage for reliability
- **📝 Type Hints**: Full typing support for better development experience

---

## 🏗️ System Architecture

The system employs a sophisticated multi-agent workflow:

```
Input Query
    ↓
[Guardrails] - Safety & Validation
    ↓
[Reasoning Node] - GPT-4o Mini (Intent Understanding)
    ↓
[Planning Node] - GPT-4o Mini (Task Decomposition)
    ↓
[Agent Executors] (Parallel Execution)
    ├─ arXiv Agent (Academic Papers)
    ├─ Tavily Agent (Web Search)
    └─ Wikipedia Agent (Knowledge)
    ↓
[Synthesis Node] - Gemini 2.5 Flash (Aggregation)
    ↓
[Critic Agent] - Quality Validation
    ↓
Final Response
```

### Core Components

| Component | Purpose | Model |
|-----------|---------|-------|
| **Guardrails** | Input validation and safety checks | Custom Rules |
| **Reasoning Node** | Query analysis and task identification | GPT-4o Mini |
| **Planning Node** | Sequential execution plan creation | GPT-4o Mini |
| **Search Agents** | Multi-source information gathering | Specialized APIs |
| **Synthesis Node** | Context-aware aggregation | Gemini 2.5 Flash |
| **Critic Agent** | Quality assurance and validation | LLM-based |

---

## 🚀 Getting Started

### Prerequisites

**System Requirements:**
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for API integration

**Required API Keys:**
- [OpenAI API Key](https://platform.openai.com/api-keys) - GPT-4o Mini
- [Google AI API Key](https://makersuite.google.com/app/apikey) - Gemini 2.5 Flash
- [Tavily API Key](https://tavily.com/) - Web Search

**Optional:**
- [LangSmith API Key](https://smith.langchain.com/) - For debugging and observability

### Installation

```bash
# Clone the repository
git clone https://github.com/arun-nivaas/LLM-002-Agentic-Research-Assistant.git
cd LLM-002-Agentic-Research-Assistant

# Install UV (optional but recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with UV
uv sync

# Or use pip
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_AI_API_KEY=your_google_ai_key
TAVILY_API_KEY=your_tavily_key
LANGSMITH_API_KEY=your_langsmith_key  # Optional
```

### Usage

```python
from research_assistant.agentic_research import run_research

# Simple usage
result = run_research("Latest advances in quantum computing")
print(result)
```

---

## 📁 Project Structure

```
src/research_assistant/
├── agents/               # Specialized search agents
│   ├── arxiv_agent.py
│   ├── tavily_search_agent.py
│   └── wikipedia_agent.py
├── core/                 # Core utilities
│   ├── state_manager.py
│   ├── logger.py
│   └── global_state.py
├── graph_nodes/          # Workflow nodes
│   ├── reasoning_node.py
│   ├── planning_node.py
│   ├── rag_node.py
│   ├── fusion_node.py
│   ├── llm_synthesis_node.py
│   └── critic_node.py
├── guardrails/           # Safety & validation
│   ├── guardrails_validator.py
│   └── harmful_keywords_validator.py
├── schemas/              # Pydantic models
│   ├── planning_model.py
│   ├── reasoning_model.py
│   └── research_model.py
└── utils/                # Utilities
    ├── llm_client.py
    ├── rag_pipeline.py
    └── query_analyser.py
```

---

## 🔧 Technologies Used

- **Framework**: LangGraph, LangChain
- **LLMs**: GPT-4o Mini (reasoning/planning), Gemini 2.5 Flash (synthesis)
- **Search APIs**: arXiv, Tavily, Wikipedia
- **Data Validation**: Pydantic
- **Package Manager**: UV
- **Observability**: LangSmith
- **Language**: Python 3.11+

---

## 📊 Performance & Metrics

- **Query Processing**: ~5-15 seconds for complex research queries
- **Source Integration**: Parallel execution of 3+ search agents
- **Accuracy**: Critic-validated outputs with quality scoring
- **Reliability**: Graceful error handling with fallback mechanisms

---

## 🤝 Contributing

This project represents my exploration of advanced agentic AI systems. For suggestions, improvements, or collaboration opportunities, please feel free to reach out!

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to the open-source communities behind:
- LangChain & LangGraph
- OpenAI & Google AI
- Tavily Search
- All the amazing tools that made this project possible

---

**Built with ❤️ by Vikash**

*Last Updated: 2026-07-17*
