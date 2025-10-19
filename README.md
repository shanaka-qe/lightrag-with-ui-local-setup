# RAG System with Local LLM

A simple, modular Python project that uses LightRAG with a local Gemma 2 12B model. Features a Streamlit web interface and command-line access.

## 🚀 Features

- **Local LLM**: Uses Gemma 2 12B model locally (configurable)
- **LightRAG Integration**: Advanced RAG capabilities with knowledge graphs
- **Streamlit UI**: Web interface for easy interaction
- **Document Ingestion**: Automatic processing from `data/ingest/` folder
- **Modular Design**: Clean, simple code structure
- **Environment Configuration**: Easy setup with `.env` file

## 📋 Requirements

- Python 3.13+
- pip (Python package manager)
- **Ollama** (for local LLM models)
- 8GB+ RAM (for Gemma 2 12B)
- 4GB+ disk space for model files

### Install Ollama:
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

## 🚀 Why pip?

- **🔒 Reliable**: Standard Python package manager
- **🎯 Simple**: One command to install and run
- **📦 Compatible**: Works with all Python environments
- **🛠️ Well-supported**: Handles complex dependencies like tiktoken

## 🛠️ Quick Setup

### Automated Setup (Recommended)

**For macOS/Linux:**
```bash
./setup/setup.sh
```

**For Windows:**
```cmd
setup/setup.bat
```

### Manual Setup

1. **Create Python 3.12 virtual environment:**
   ```bash
   python3.12 -m venv venv312
   source venv312/bin/activate  # On Windows: venv312\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama:**
   ```bash
   # Install Ollama (macOS)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull the model
   ollama pull gemma3:12b
   ```

4. **Configure environment:**
   ```bash
   # Option 1: Interactive setup (recommended)
   python setup/setup_env.py
   
   # Option 2: Manual setup
   cp env.example .env
   # Edit .env file with your preferences
   ```

5. **Run the system:**
   ```bash
   # Web interface (recommended)
   python main.py streamlit
   
   # Command line interface
   python main.py cli
   
   # Test the system
   python main.py test
   ```

## 📁 Project Structure

```
lightrag-with-ui/
├── main.py                 # Main application launcher
├── app.py                  # Streamlit web interface
├── simple_rag.py           # Core RAG system
├── ollama_llm.py           # Ollama LLM integration
├── config/
│   └── settings.py        # Configuration management
├── utils/
│   └── document_ingestion.py  # Document processing utilities
├── data/
│   ├── ingest/            # Put your documents here (PDFs, TXT, etc.)
│   └── rag_workspace/     # RAG system workspace
├── venv312/               # Python 3.12 virtual environment
├── requirements.txt       # Python dependencies
├── env.example            # Environment template
└── setup/                 # Setup scripts
    ├── setup_env.py       # Interactive environment setup
    └── setup.sh           # Automated setup script
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the web interface:**
   ```bash
   python main.py streamlit
   ```

2. **Open your browser to:** `http://localhost:8501`

3. **Use the interface:**
   - Click "Initialize RAG System"
   - Click "Load Model" (downloads Gemma 2 12B on first run)
   - Add documents to `data/ingest/` folder
   - Click "Ingest Documents"
   - Ask questions in the chat interface

### Command Line Interface

```bash
python main.py cli
```

### Adding Documents

1. **Place documents in `data/ingest/` folder:**
   - Supported formats: `.txt`, `.md`, `.pdf`, `.docx`, `.csv`
   - The system will automatically process them

2. **Upload via web interface:**
   - Use the file upload feature in the Streamlit app

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# LLM Configuration
LLM_MODEL_NAME=gemma-2-12b          # Model to use
LLM_CONTEXT_SIZE=4096               # Context window
LLM_THREADS=4                       # CPU threads
LLM_TEMPERATURE=0.7                 # Response creativity

# RAG Configuration
RAG_WORKING_DIR=data/rag_workspace  # RAG data directory
RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Streamlit Configuration
STREAMLIT_PORT=8501                 # Web interface port
```

## 🎯 Available Models (Ollama)

Use `ollama list` to see your installed models. Popular options:

- **Gemma 2 12B** (`gemma2:12b`) - Default, best performance
- **Gemma 2 9B** (`gemma2:9b`) - Good balance
- **Gemma 2 2B** (`gemma2:2b`) - Fastest, lower quality
- **Llama 3.1 8B** (`llama3.1:8b`) - Good general purpose
- **Llama 3.1 70B** (`llama3.1:70b`) - Best quality (needs lots of RAM)
- **Mistral 7B** (`mistral:7b`) - Good balance
- **CodeLlama 7B** (`codellama:7b`) - For code tasks
- **Phi-3 3.8B** (`phi3:3.8b`) - Microsoft's efficient model

### Install Models:
```bash
# Install Gemma 2 12B (default)
ollama pull gemma2:12b

# Install other models
ollama pull llama3.1:8b
ollama pull mistral:7b
```

## 🔧 Troubleshooting

### Common Issues

1. **Model download fails:**
   - Check internet connection
   - Ensure sufficient disk space (4GB+)

2. **Out of memory:**
   - Use smaller model: `gemma-2-2b`
   - Reduce context size in `.env`

3. **Slow performance:**
   - Increase CPU threads in `.env`
   - Use smaller model

### Logs

Check `logs/` directory for detailed error messages.

## 🧪 Testing

```bash
# Test the installation
python test_installation.py

# Test the system
python main.py test

# Test individual components
python local_llama.py
python simple_rag.py
```

## 📚 API Reference

### RAGSystem Class

- `setup_model(model_name)` - Load LLM model
- `ingest_documents()` - Process documents from ingest folder
- `query(question, mode)` - Ask questions
- `get_stats()` - Get system statistics

### DocumentIngestion Class

- `get_documents()` - Get all documents from ingest folder
- `get_document_count()` - Count documents
- `clear_ingest_folder()` - Clear all documents

## 🎉 What's Next?

- Add more model support
- Implement document preprocessing
- Add knowledge graph visualization
- Support for multiple languages

---

**Simple, Fast, Local RAG! 🤖📚**
