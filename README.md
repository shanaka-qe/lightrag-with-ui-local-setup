# 🤖 LightRAG with UI

A powerful Retrieval-Augmented Generation (RAG) system that lets you chat with your documents using local AI models. Features a modern Streamlit web interface, automatic document processing, and support for multiple AI models via Ollama.

## 🚀 Features

- **🤖 Multiple AI Models**: Support for Gemma, Llama, Mistral, and more via Ollama
- **📚 Smart Document Processing**: Automatic ingestion from PDFs, TXT, DOCX, CSV files
- **💬 Natural Conversations**: Ask questions about your documents in plain English
- **🌐 Modern Web Interface**: Beautiful Streamlit UI with real-time chat
- **🔒 Complete Privacy**: Everything runs locally - no data leaves your machine
- **⚡ Fast Setup**: Automated installation and configuration
- **🎯 Intelligent Retrieval**: Smart document search and context understanding
- **📱 Cross-Platform**: Works on macOS, Windows, and Linux

## 📋 Requirements

- **Python 3.12** (required)
- **Ollama** (for local LLM models)
- **8GB+ RAM** (for recommended models)
- **10GB+ disk space** for models and data
- **Internet connection** (for initial setup and model downloads)

### Install Ollama:
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

## 🚀 Why This Project?

- **🔒 Privacy-First**: All processing happens locally on your machine
- **🎯 Easy to Use**: Simple web interface - no technical knowledge required
- **📦 Self-Contained**: Everything you need in one package
- **🛠️ Highly Customizable**: Support for multiple AI models and configurations
- **📚 Document Smart**: Understands context and relationships in your documents

## 🛠️ Quick Setup

### Automated Setup (Recommended)

**For macOS/Linux:**
```bash
./setup/setup.sh
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
├── main.py                 # Application entry point
├── app.py                  # Streamlit web interface
├── utils/                  # Core functionality
│   ├── rag_system.py       # RAG system logic
│   ├── llm_provider.py     # Ollama LLM integration
│   └── document_ingestion.py # Document processing
├── config/                 # Configuration
│   └── settings.py         # Application settings
├── data/
│   ├── ingest/            # Put your documents here (PDFs, TXT, etc.)
│   └── rag_workspace/     # RAG system workspace
├── venv312/               # Python 3.12 virtual environment
├── requirements.txt       # Python dependencies
├── env.example            # Environment template
├── setup/                 # Setup scripts
│   ├── setup_env.py       # Interactive environment setup
│   └── setup.sh           # Automated setup script
└── documents/             # Documentation
    ├── user-guide.md      # Complete user guide
    ├── quick-reference.md # Quick reference card
    └── troubleshooting.md # Troubleshooting guide
```

## 📚 Documentation

- **📖 [Complete User Guide](documents/user-guide.md)** - Comprehensive guide for beginners
- **⚡ [Quick Reference](documents/quick-reference.md)** - Commands and shortcuts for advanced users  
- **🔧 [Troubleshooting Guide](documents/troubleshooting.md)** - Solutions to common issues

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the web interface:**
   ```bash
   python main.py streamlit
   ```

2. **Open your browser to:** `http://localhost:8501`

3. **Use the interface:**
   - System automatically initializes and loads the AI model
   - Add documents to `data/ingest/` folder or use the upload feature
   - Documents are automatically processed
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
# AI Model Configuration
LLM_MODEL_NAME=gemma3:12b           # Model to use
LLM_HOST=http://localhost:11434     # Ollama server
LLM_TEMPERATURE=0.7                 # Response creativity (0.0-1.0)
LLM_MAX_TOKENS=512                  # Maximum response length

# RAG Configuration
RAG_WORKING_DIR=data/rag_workspace  # RAG data directory
RAG_MAX_TOKEN=2000                  # Context length
RAG_TIMEOUT=30                      # Query timeout

# Web Interface
STREAMLIT_PORT=8501                 # Web interface port
STREAMLIT_HOST=localhost            # Web interface host
```

## 🤖 Available AI Models

The system supports any Ollama model. Popular options:

### **Recommended Models:**
- **`gemma3:12b`** - Default, best balance of quality and speed
- **`gemma2:12b`** - High quality, good for complex tasks
- **`llama3:8b`** - Fast, good general purpose
- **`mistral:7b`** - Excellent for reasoning tasks

### **Performance Models:**
- **`gemma2:2b`** - Fastest, good for quick responses
- **`llama3:70b`** - Highest quality (requires 40GB+ RAM)
- **`codellama:7b`** - Specialized for code and technical documents

### **Install Models:**
```bash
# Install recommended model
ollama pull gemma3:12b

# Install other models
ollama pull llama3:8b
ollama pull mistral:7b
ollama pull gemma2:2b  # For faster performance
```

## 🔧 Troubleshooting

### **Quick Fixes:**

1. **"Model not found" error:**
   ```bash
   ollama pull gemma3:12b
   ```

2. **"Port 8501 already in use":**
   ```bash
   lsof -ti :8501 | xargs kill -9
   ```

3. **"No documents available":**
   - Add documents to `data/ingest/` folder
   - Restart the application

4. **Slow performance:**
   - Use smaller model: `ollama pull gemma2:2b`
   - Edit `.env`: `LLM_MODEL_NAME=gemma2:2b`

### **For detailed troubleshooting:**
- 📖 See [Complete User Guide](documents/user-guide.md)
- 🔧 See [Troubleshooting Guide](documents/troubleshooting.md)

## 🧪 Testing

```bash
# Test the system
python main.py test

# Test individual components
python -c "from utils.rag_system import SimpleRAG; print('✅ RAG system OK')"
python -c "from utils.llm_provider import OllamaLLM; print('✅ LLM provider OK')"
```

## 🎯 Example Usage

### **Ask Questions About Your Documents:**
```
Q: "What is the main topic of this document?"
A: "This document discusses the Phoenix Digital Transformation Initiative..."

Q: "What is the project budget?"
A: "$2.4 million USD"

Q: "Who is the lead architect?"
A: "Dr. Sarah Chen"
```

### **Supported Document Types:**
- 📄 **Text files** (`.txt`, `.md`)
- 📊 **PDF documents** (`.pdf`)
- 📝 **Word documents** (`.docx`)
- 📈 **CSV files** (`.csv`)

## 🎉 What's Next?

- 🔄 **Real-time document updates**
- 📊 **Knowledge graph visualization**
- 🌍 **Multi-language support**
- 🔗 **API endpoints for integration**
- 📱 **Mobile-friendly interface**

---

**🤖 Chat with your documents like never before! 📚✨**

*Built with ❤️ for the community*
