# 🔧 Troubleshooting Guide

## 🚨 Common Issues and Solutions

### Installation Issues

#### ❌ **Python 3.12 Not Found**
**Error:** `python3.12: command not found`

**Solutions:**
```bash
# macOS (Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip

# Windows
# Download from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH"
```

#### ❌ **Virtual Environment Issues**
**Error:** `venv: command not found`

**Solutions:**
```bash
# Create venv manually
python3.12 -m venv venv312

# Activate venv
source venv312/bin/activate  # macOS/Linux
venv312\Scripts\activate     # Windows

# Verify activation
which python  # Should show venv312/bin/python
```

#### ❌ **Dependencies Installation Failed**
**Error:** `pip install` fails

**Solutions:**
```bash
# Update pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install one by one if needed
pip install streamlit
pip install ollama
pip install lightrag
```

### Ollama Issues

#### ❌ **Ollama Not Installed**
**Error:** `ollama: command not found`

**Solutions:**
1. **Download Ollama:**
   - Visit [ollama.ai/download](https://ollama.ai/download)
   - Download for your operating system
   - Install following the instructions

2. **Verify installation:**
   ```bash
   ollama --version
   ```

#### ❌ **Ollama Server Not Running**
**Error:** `Connection refused` or `Failed to connect`

**Solutions:**
```bash
# Start Ollama server
ollama serve

# Check if running
curl http://localhost:11434/api/tags

# If port is busy
lsof -i :11434
kill -9 <PID>
ollama serve
```

#### ❌ **Model Not Found**
**Error:** `Model gemma3:12b not found`

**Solutions:**
```bash
# List available models
ollama list

# Pull the model
ollama pull gemma3:12b

# Check model is available
ollama show gemma3:12b
```

#### ❌ **Model Loading Failed**
**Error:** `Failed to load model`

**Solutions:**
1. **Check system resources:**
   ```bash
   # Check available RAM
   free -h  # Linux
   vm_stat  # macOS
   ```

2. **Use smaller model:**
   ```bash
   ollama pull gemma2:2b
   # Edit .env: LLM_MODEL_NAME=gemma2:2b
   ```

3. **Restart Ollama:**
   ```bash
   pkill ollama
   ollama serve
   ```

### Application Issues

#### ❌ **Port 8501 Already in Use**
**Error:** `Port 8501 is already in use`

**Solutions:**
```bash
# Kill existing processes
lsof -ti :8501 | xargs kill -9

# Or use different port
# Edit .env: STREAMLIT_PORT=8502
```

#### ❌ **Streamlit Not Found**
**Error:** `streamlit: command not found`

**Solutions:**
```bash
# Activate virtual environment
source venv312/bin/activate

# Install streamlit
pip install streamlit

# Run with python module
python -m streamlit run app.py
```

#### ❌ **Import Errors**
**Error:** `ModuleNotFoundError`

**Solutions:**
```bash
# Activate virtual environment
source venv312/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Document Processing Issues

#### ❌ **No Documents Found**
**Error:** `No documents available for querying`

**Solutions:**
1. **Check document location:**
   ```bash
   ls -la data/ingest/
   ```

2. **Add documents:**
   ```bash
   cp your-document.pdf data/ingest/
   ```

3. **Restart application:**
   ```bash
   python main.py streamlit
   ```

#### ❌ **Document Upload Failed**
**Error:** `Failed to upload document`

**Solutions:**
1. **Check file format:**
   - Supported: `.txt`, `.pdf`, `.docx`, `.csv`
   - Not supported: images, audio, video

2. **Check file size:**
   - Large files may cause memory issues
   - Try smaller files first

3. **Check file permissions:**
   ```bash
   chmod 644 data/ingest/your-file.pdf
   ```

#### ❌ **PDF Processing Failed**
**Error:** `Failed to read PDF`

**Solutions:**
1. **Install PDF dependencies:**
   ```bash
   pip install PyPDF2
   ```

2. **Use text-based PDFs:**
   - Avoid scanned PDFs
   - Use OCR tools for scanned documents

3. **Convert to text:**
   ```bash
   # Convert PDF to text
   pdftotext document.pdf data/ingest/document.txt
   ```

### Performance Issues

#### ❌ **Slow Response Times**
**Problem:** Queries take too long

**Solutions:**
1. **Use smaller model:**
   ```bash
   # Edit .env
   LLM_MODEL_NAME=gemma2:2b
   ```

2. **Reduce context size:**
   ```bash
   # Edit .env
   RAG_MAX_TOKEN=1000
   LLM_MAX_TOKENS=256
   ```

3. **Close other applications**

#### ❌ **High Memory Usage**
**Problem:** System runs out of memory

**Solutions:**
1. **Monitor memory:**
   ```bash
   htop  # Linux
   Activity Monitor  # macOS
   Task Manager  # Windows
   ```

2. **Use smaller model:**
   ```bash
   ollama pull gemma2:2b
   # Edit .env: LLM_MODEL_NAME=gemma2:2b
   ```

3. **Reduce batch size:**
   ```bash
   # Edit .env
   RAG_MAX_TOKEN=500
   ```

#### ❌ **CPU Overload**
**Problem:** System becomes unresponsive

**Solutions:**
1. **Check CPU usage:**
   ```bash
   top  # Linux/macOS
   ```

2. **Limit concurrent processes:**
   - Close other applications
   - Use smaller model

3. **Adjust system settings:**
   ```bash
   # Edit .env
   LLM_TEMPERATURE=0.3  # Less computation
   ```

### Network Issues

#### ❌ **Ollama Connection Failed**
**Error:** `Connection refused to Ollama`

**Solutions:**
1. **Check Ollama status:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Restart Ollama:**
   ```bash
   pkill ollama
   ollama serve
   ```

3. **Check firewall:**
   - Allow port 11434
   - Check antivirus settings

#### ❌ **Model Download Failed**
**Error:** `Failed to pull model`

**Solutions:**
1. **Check internet connection**
2. **Try different model:**
   ```bash
   ollama pull gemma2:2b  # Smaller model
   ```

3. **Manual download:**
   - Download model files manually
   - Place in Ollama models directory

### Configuration Issues

#### ❌ **Environment Variables Not Loaded**
**Error:** `Configuration not found`

**Solutions:**
1. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

2. **Create .env file:**
   ```bash
   cp env.example .env
   ```

3. **Verify configuration:**
   ```bash
   python -c "from config.settings import LLM_CONFIG; print(LLM_CONFIG)"
   ```

#### ❌ **Invalid Configuration**
**Error:** `Invalid configuration value`

**Solutions:**
1. **Check .env format:**
   ```bash
   # Correct format
   LLM_MODEL_NAME=gemma3:12b
   LLM_TEMPERATURE=0.7
   
   # Wrong format
   LLM_MODEL_NAME = "gemma3:12b"  # No spaces around =
   ```

2. **Validate values:**
   - Temperature: 0.0 to 1.0
   - Port: 1024 to 65535
   - Model name: Must exist in Ollama

### System-Specific Issues

#### 🍎 **macOS Issues**

**Homebrew not found:**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Permission denied:**
```bash
# Fix permissions
sudo chown -R $(whoami) /usr/local/bin
```

#### 🐧 **Linux Issues**

**Python not found:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip

# CentOS/RHEL
sudo yum install python3.12
```

**Permission issues:**
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.local
```

#### 🪟 **Windows Issues**

**Python not in PATH:**
1. Reinstall Python with "Add to PATH" checked
2. Or add manually to system PATH

**Virtual environment issues:**
```cmd
# Use full path
C:\Python312\python.exe -m venv venv312
venv312\Scripts\activate
```

**Ollama on Windows:**
1. Download from ollama.ai
2. Run as Administrator if needed
3. Check Windows Defender settings

## 🔍 Debugging Steps

### 1. Check System Status
```bash
# Check Python
python3.12 --version

# Check virtual environment
source venv312/bin/activate
which python

# Check dependencies
pip list | grep -E "(streamlit|ollama|lightrag)"
```

### 2. Check Ollama Status
```bash
# Check if running
curl http://localhost:11434/api/tags

# Check models
ollama list

# Check logs
ollama serve  # Look for error messages
```

### 3. Check Application Logs
```bash
# Run with verbose output
python main.py streamlit

# Look for ERROR or WARNING messages
```

### 4. Test Individual Components
```bash
# Test imports
python -c "import streamlit; print('Streamlit OK')"
python -c "import ollama; print('Ollama OK')"
python -c "from utils.rag_system import SimpleRAG; print('RAG OK')"
```

### 5. Reset Everything
```bash
# Remove virtual environment
rm -rf venv312

# Remove configuration
rm -f .env

# Start fresh
./setup/setup.sh
```

## 📞 Getting Help

### Before Asking for Help
1. ✅ Read this troubleshooting guide
2. ✅ Check the main user guide
3. ✅ Try the debugging steps
4. ✅ Search for similar issues

### When Reporting Issues
Include this information:
- **Operating System:** macOS/Windows/Linux version
- **Python Version:** `python3.12 --version`
- **Error Message:** Complete error text
- **Steps to Reproduce:** What you did before the error
- **System Resources:** RAM, CPU, disk space

### Useful Commands for Debugging
```bash
# System information
uname -a  # Linux/macOS
systeminfo  # Windows

# Python environment
python3.12 --version
pip list

# Ollama status
ollama list
curl http://localhost:11434/api/tags

# Application status
lsof -i :8501
lsof -i :11434
```

Remember: Most issues can be solved by following the troubleshooting steps above. If you're still stuck, the community is here to help! 🤝
