# 📚 LightRAG with UI - Complete User Guide

Welcome to **LightRAG with UI** - a powerful Retrieval-Augmented Generation (RAG) system that allows you to chat with your documents using local AI models. This guide will walk you through everything you need to know to get started, from basic concepts to advanced usage.

## 🎯 What is LightRAG with UI?

LightRAG with UI is a complete RAG (Retrieval-Augmented Generation) system that lets you:
- **Upload documents** (PDFs, text files, etc.)
- **Ask questions** about your documents
- **Get AI-powered answers** based on your document content
- **Run everything locally** with your own AI models

Think of it as having a smart assistant that can read and understand your documents, then answer questions about them!

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Python 3.12** (required)
- **8GB+ RAM** (for AI models)
- **10GB+ free disk space**

### Step 1: Download the Project
```bash
git clone <your-repo-url>
cd lightrag-with-ui
```

### Step 2: Automated Setup (Recommended)
```bash
# Make setup script executable
chmod +x setup/setup.sh

# Run automated setup
./setup/setup.sh
```

### Step 3: Start the Application
```bash
# Activate virtual environment
source venv312/bin/activate

# Start the web interface
python main.py streamlit
```

### Step 4: Open Your Browser
Visit: `http://localhost:8501`

🎉 **You're ready to go!** The system will automatically load a sample document and you can start asking questions.

---

## 📋 Detailed Setup Guide

### Option A: Automated Setup (Recommended for Beginners)

The automated setup handles everything for you:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd lightrag-with-ui

# 2. Run the setup script
chmod +x setup/setup.sh
./setup/setup.sh
```

**What the automated setup does:**
- ✅ Creates Python 3.12 virtual environment
- ✅ Installs all required dependencies
- ✅ Downloads and configures Ollama
- ✅ Pulls the recommended AI model
- ✅ Sets up environment configuration
- ✅ Creates necessary directories

### Option B: Manual Setup (For Advanced Users)

If you prefer to set up manually or the automated setup doesn't work:

#### 1. Install Python 3.12
**macOS:**
```bash
# Using Homebrew
brew install python@3.12

# Verify installation
python3.12 --version
```

**Windows:**
- Download Python 3.12 from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python3.12 -m venv venv312

# Activate it
# On macOS/Linux:
source venv312/bin/activate
# On Windows:
venv312\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt
```

#### 4. Install and Configure Ollama

**Download Ollama:**
- Visit [ollama.ai](https://ollama.ai/download)
- Download and install for your operating system

**Start Ollama:**
```bash
# Start Ollama server
ollama serve
```

**Pull AI Model:**
```bash
# Pull the recommended model (in a new terminal)
ollama pull gemma3:12b
```

#### 5. Configure Environment
```bash
# Interactive setup
python setup/setup_env.py

# Or manual setup
cp env.example .env
# Edit .env file with your preferences
```

---

## 🎮 How to Use the Application

### Starting the Application

1. **Activate the virtual environment:**
   ```bash
   source venv312/bin/activate  # macOS/Linux
   # or
   venv312\Scripts\activate     # Windows
   ```

2. **Start the web interface:**
   ```bash
   python main.py streamlit
   ```

3. **Open your browser:**
   - Go to `http://localhost:8501`
   - The application will automatically load

### Understanding the Interface

The web interface has several sections:

#### 📊 **Main Dashboard**
- **System Status**: Shows if the AI model is loaded
- **Document Count**: Displays how many documents are loaded
- **Chat Interface**: Where you ask questions

#### ⚙️ **Sidebar Controls**
- **Model Selection**: Choose different AI models
- **System Information**: View system stats
- **Document Management**: Upload new documents

#### 💬 **Chat Interface**
- **Question Input**: Type your questions here
- **Response Area**: AI answers appear here
- **Query History**: Previous questions and answers

### Adding Your Documents

#### Method 1: File Upload (Web Interface)
1. Go to the **Document Management** section in the sidebar
2. Click **"Choose files"** or drag and drop files
3. Supported formats: `.txt`, `.pdf`, `.docx`, `.csv`
4. Click **"Upload"**

#### Method 2: Manual File Placement
1. Copy your documents to the `data/ingest/` folder
2. Restart the application
3. Documents will be automatically loaded

**Example:**
```bash
# Copy documents to ingest folder
cp my-document.pdf data/ingest/
cp my-notes.txt data/ingest/

# Restart the application
python main.py streamlit
```

### Asking Questions

Once your documents are loaded, you can ask questions like:

**General Questions:**
- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"

**Specific Questions:**
- "What is the budget mentioned in the document?"
- "Who is the project manager?"
- "What technology stack is used?"
- "What are the performance requirements?"

**Complex Questions:**
- "Compare the different approaches mentioned"
- "What are the risks and mitigation strategies?"
- "Explain the technical architecture"

### Example Usage Scenarios

#### 📄 **Research Papers**
```
Q: "What is the main hypothesis of this research?"
Q: "What methodology was used?"
Q: "What are the key findings and conclusions?"
```

#### 📊 **Business Documents**
```
Q: "What is the project budget?"
Q: "Who are the stakeholders?"
Q: "What are the project timelines?"
Q: "What are the success metrics?"
```

#### 📚 **Technical Documentation**
```
Q: "How do I install this software?"
Q: "What are the system requirements?"
Q: "What APIs are available?"
Q: "How do I configure the settings?"
```

---

## ⚙️ Configuration Options

### Environment Variables

You can customize the system by editing the `.env` file:

```bash
# AI Model Configuration
LLM_MODEL_NAME=gemma3:12b          # AI model to use
LLM_HOST=http://localhost:11434     # Ollama server URL
LLM_TEMPERATURE=0.7                 # Creativity level (0.0-1.0)
LLM_MAX_TOKENS=512                  # Maximum response length

# RAG Configuration
RAG_WORKING_DIR=data/rag_workspace  # Where RAG data is stored
RAG_MAX_TOKEN=2000                  # Maximum context length
RAG_TIMEOUT=30                      # Query timeout (seconds)

# Web Interface
STREAMLIT_PORT=8501                 # Web interface port
STREAMLIT_HOST=localhost            # Web interface host

# Logging
LOG_LEVEL=INFO                      # Logging level
```

### Available AI Models

You can use different AI models by changing `LLM_MODEL_NAME`:

**Recommended Models:**
- `gemma3:12b` - Best balance of quality and speed
- `gemma2:12b` - High quality, slower
- `llama3:8b` - Fast, good quality
- `llama3:70b` - Highest quality, requires 40GB+ RAM

**To change models:**
1. Edit `.env` file: `LLM_MODEL_NAME=llama3:8b`
2. Pull the new model: `ollama pull llama3:8b`
3. Restart the application

### Performance Tuning

**For Better Performance:**
```bash
# In .env file
LLM_TEMPERATURE=0.3          # More focused responses
LLM_MAX_TOKENS=256           # Shorter responses
RAG_MAX_TOKEN=1000           # Less context
```

**For Better Quality:**
```bash
# In .env file
LLM_TEMPERATURE=0.8          # More creative responses
LLM_MAX_TOKENS=1024          # Longer responses
RAG_MAX_TOKEN=4000           # More context
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ **"Model not found" Error**
**Problem:** AI model is not loaded
**Solution:**
```bash
# Check if Ollama is running
ollama list

# Pull the model
ollama pull gemma3:12b

# Restart Ollama
ollama serve
```

#### ❌ **"Port 8501 already in use" Error**
**Problem:** Another application is using the port
**Solution:**
```bash
# Kill existing processes
lsof -ti :8501 | xargs kill -9

# Or use a different port
# Edit .env: STREAMLIT_PORT=8502
```

#### ❌ **"No documents available" Error**
**Problem:** No documents are loaded
**Solution:**
1. Check if documents are in `data/ingest/` folder
2. Make sure documents are in supported formats
3. Restart the application

#### ❌ **"LightRAG not installed" Error**
**Problem:** Dependencies not installed
**Solution:**
```bash
# Activate virtual environment
source venv312/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### ❌ **Slow Performance**
**Problem:** System is running slowly
**Solutions:**
1. **Use a smaller model:**
   ```bash
   # Edit .env
   LLM_MODEL_NAME=gemma2:2b
   ollama pull gemma2:2b
   ```

2. **Reduce context size:**
   ```bash
   # Edit .env
   RAG_MAX_TOKEN=1000
   LLM_MAX_TOKENS=256
   ```

3. **Close other applications** to free up RAM

#### ❌ **Memory Issues**
**Problem:** Out of memory errors
**Solutions:**
1. **Use smaller model:**
   ```bash
   ollama pull gemma2:2b
   # Edit .env: LLM_MODEL_NAME=gemma2:2b
   ```

2. **Reduce batch size:**
   ```bash
   # Edit .env
   RAG_MAX_TOKEN=500
   ```

3. **Close other applications**

### Getting Help

If you're still having issues:

1. **Check the logs:**
   ```bash
   # Look for error messages in the terminal
   python main.py streamlit
   ```

2. **Verify installation:**
   ```bash
   # Test individual components
   python -c "import streamlit; print('Streamlit OK')"
   python -c "import ollama; print('Ollama OK')"
   ```

3. **Reset everything:**
   ```bash
   # Remove virtual environment and start fresh
   rm -rf venv312
   ./setup/setup.sh
   ```

---

## 📁 File Structure Explained

```
lightrag-with-ui/
├── 📄 main.py                    # Application entry point
├── 📄 app.py                     # Web interface (Streamlit)
├── 📄 requirements.txt           # Python dependencies
├── 📄 env.example               # Environment template
├── 📁 setup/                    # Setup scripts
│   ├── 📄 setup_env.py          # Interactive setup
│   └── 📄 setup.sh              # Automated setup
├── 📁 utils/                    # Core functionality (Modular Architecture)
│   ├── 📄 rag_system.py         # Main orchestrator
│   ├── 📄 query_engine.py       # Query processing with Ollama
│   ├── 📄 graph_visualizer.py   # Knowledge graph visualization
│   ├── 📄 llm_provider.py       # AI model integration
│   └── 📄 document_ingestion.py # Document processing
├── 📁 config/                   # Configuration
│   └── 📄 settings.py           # Application settings
├── 📁 data/                     # Data storage
│   ├── 📁 ingest/               # 📂 Put your documents here
│   └── 📁 rag_workspace/        # RAG system data
├── 📁 documents/                # Documentation
│   └── 📄 user-guide.md         # This guide
└── 📁 venv312/                  # Python virtual environment
```

### Key Directories:

- **`data/ingest/`** - Put your documents here (PDFs, TXT files, etc.)
- **`data/rag_workspace/`** - RAG system stores processed data here
- **`setup/`** - Setup scripts for easy installation
- **`utils/`** - Core application logic (modular architecture)
  - `rag_system.py` - Main orchestrator
  - `query_engine.py` - Query processing
  - `graph_visualizer.py` - Knowledge graph visualization
  - `llm_provider.py` - AI model integration
  - `document_ingestion.py` - Document processing
- **`config/`** - Configuration files

---

## 🚀 Advanced Usage

### Command Line Interface

You can also use the system from the command line:

```bash
# Test the system
python main.py test

# CLI mode (interactive)
python main.py cli

# Help
python main.py --help
```

### Custom Model Integration

To use your own AI models:

1. **Install your model in Ollama:**
   ```bash
   ollama pull your-model-name
   ```

2. **Update configuration:**
   ```bash
   # Edit .env file
   LLM_MODEL_NAME=your-model-name
   ```

3. **Restart the application**

### Batch Document Processing

For processing many documents at once:

1. **Place all documents in `data/ingest/`:**
   ```bash
   cp *.pdf data/ingest/
   cp *.txt data/ingest/
   ```

2. **Restart the application:**
   ```bash
   python main.py streamlit
   ```

3. **Documents will be automatically processed**

### Custom Document Types

The system supports various document types:

- **Text files** (`.txt`, `.md`)
- **PDF documents** (`.pdf`)
- **Word documents** (`.docx`)
- **CSV files** (`.csv`)

### Performance Monitoring

Monitor system performance:

```bash
# Check system resources
htop  # or top on macOS

# Check Ollama status
ollama list

# Check application logs
python main.py streamlit  # Look for INFO/ERROR messages
```

---

## 🔒 Security and Privacy

### Data Privacy
- ✅ **All processing is local** - No data sent to external servers
- ✅ **Documents stay on your machine** - Never uploaded anywhere
- ✅ **AI models run locally** - No cloud dependencies
- ✅ **No tracking or analytics** - Completely private

### Security Best Practices
1. **Keep your system updated**
2. **Use strong passwords** for any remote access
3. **Regular backups** of your documents
4. **Monitor system resources** to prevent overload

---

## 📈 Tips for Best Results

### Document Preparation
1. **Use clear, well-formatted documents**
2. **Avoid scanned PDFs** (use text-based PDFs when possible)
3. **Break large documents** into smaller sections
4. **Use descriptive filenames**

### Question Asking
1. **Be specific** in your questions
2. **Ask follow-up questions** for clarification
3. **Use context** from previous answers
4. **Try different phrasings** if you don't get good results

### System Optimization
1. **Use appropriate model size** for your hardware
2. **Monitor memory usage** during processing
3. **Regular cleanup** of old documents
4. **Keep the system updated**

---

## 🤝 Contributing and Support

### Getting Help
- 📖 **Read this guide** thoroughly
- 🔍 **Check the troubleshooting section**
- 🐛 **Report issues** with detailed error messages
- 💡 **Share your use cases** and improvements

### Contributing
- 🛠️ **Improve the code** and submit pull requests
- 📝 **Update documentation** and guides
- 🧪 **Test on different systems** and report results
- 💬 **Share feedback** and suggestions

### Community
- 🌟 **Star the project** if you find it useful
- 📢 **Share with others** who might benefit
- 🏷️ **Tag us** in your posts about the project
- 🤝 **Help other users** in the community

---

## 📝 License and Credits

This project is open source and available under the MIT License.

**Credits:**
- Built with [LightRAG](https://github.com/HKUDS/LightRAG) framework
- Powered by [Ollama](https://ollama.ai/) for local AI models
- Web interface built with [Streamlit](https://streamlit.io/)
- Document processing with [sentence-transformers](https://www.sbert.net/)

---

## 🎉 Congratulations!

You now have everything you need to use LightRAG with UI effectively. This system will help you:

- 📚 **Process and understand** your documents
- 🤖 **Get AI-powered answers** to your questions
- 🔒 **Keep everything private** and local
- 🚀 **Scale to handle** large document collections

**Happy document chatting!** 🎊

---

*For the latest updates and community discussions, visit our project repository.*
