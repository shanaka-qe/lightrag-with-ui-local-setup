# ⚡ Quick Reference Card

> **🏗️ Modular Architecture**: The system now uses clean, single-responsibility modules for better maintainability.

## 🚀 Quick Commands

### Setup
```bash
# Automated setup
./setup/setup.sh

# Manual setup
python3.12 -m venv venv312
source venv312/bin/activate
pip install -r requirements.txt
ollama pull gemma3:12b
```

### Running
```bash
# Start web interface
python main.py streamlit

# CLI mode
python main.py cli

# Test system
python main.py test
```

### Configuration
```bash
# Interactive config
python setup/setup_env.py

# Manual config
cp env.example .env
# Edit .env file
```

## 📁 File Locations

| Purpose | Location |
|---------|----------|
| **Documents to process** | `data/ingest/` |
| **RAG data storage** | `data/rag_workspace/` |
| **Configuration** | `.env` |
| **Logs** | Terminal output |

## 🔧 Common Commands

### Ollama Management
```bash
# List models
ollama list

# Pull model
ollama pull gemma3:12b

# Start Ollama
ollama serve

# Stop Ollama
pkill ollama
```

### Application Management
```bash
# Kill existing processes
lsof -ti :8501 | xargs kill -9

# Check if running
lsof -i :8501

# View logs
python main.py streamlit
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL_NAME` | `gemma3:12b` | AI model to use |
| `LLM_HOST` | `http://localhost:11434` | Ollama server |
| `LLM_TEMPERATURE` | `0.7` | Response creativity |
| `LLM_MAX_TOKENS` | `512` | Max response length |
| `STREAMLIT_PORT` | `8501` | Web interface port |
| `RAG_MAX_TOKEN` | `2000` | Context length |

## 🐛 Troubleshooting

### Common Issues
| Problem | Solution |
|---------|----------|
| Port in use | `lsof -ti :8501 \| xargs kill -9` |
| Model not found | `ollama pull gemma3:12b` |
| No documents | Check `data/ingest/` folder |
| Memory issues | Use smaller model |
| Slow performance | Reduce context size |

### Performance Tuning
```bash
# Fast mode
LLM_MODEL_NAME=gemma2:2b
LLM_MAX_TOKENS=256
RAG_MAX_TOKEN=1000

# Quality mode  
LLM_MODEL_NAME=llama3:70b
LLM_MAX_TOKENS=1024
RAG_MAX_TOKEN=4000
```

## 📊 Supported File Types

- ✅ `.txt` - Text files
- ✅ `.md` - Markdown files  
- ✅ `.pdf` - PDF documents
- ✅ `.docx` - Word documents
- ✅ `.csv` - CSV files

## 🎯 Example Questions

### General
- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"

### Specific
- "What is the budget?"
- "Who is the project manager?"
- "What technology is used?"
- "What are the requirements?"

### Complex
- "Compare the different approaches"
- "What are the risks and mitigation?"
- "Explain the technical architecture"

## 🏗️ Modular Architecture

### Core Modules
| Module | Purpose | Key Features |
|--------|---------|--------------|
| `rag_system.py` | Main orchestrator | Coordinates all components |
| `query_engine.py` | Query processing | Direct Ollama integration |
| `graph_visualizer.py` | Graph visualization | Interactive knowledge graphs |
| `llm_provider.py` | LLM integration | Ollama model management |
| `document_ingestion.py` | Document processing | Multi-format support |

### Module Testing
```bash
# Test individual components
python -c "from utils.query_engine import QueryEngine; print('QueryEngine OK')"
python -c "from utils.graph_visualizer import GraphVisualizer; print('GraphVisualizer OK')"
python -c "from utils.rag_system import SimpleRAG; print('RAG System OK')"
```

## 🔗 Useful Links

- [Ollama Download](https://ollama.ai/download)
- [Python 3.12 Download](https://www.python.org/downloads/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LightRAG Framework](https://github.com/HKUDS/LightRAG)
- [PyVis Documentation](https://pyvis.readthedocs.io/) - Graph visualization
- [NetworkX Documentation](https://networkx.org/) - Graph processing
