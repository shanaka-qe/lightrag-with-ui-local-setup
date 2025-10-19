#!/bin/bash
# Setup script for RAG System with Local LLM
# This script sets up the project using pip instead of uv

set -e  # Exit on any error

echo "🚀 Setting up RAG System with Local LLM"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.13"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "⚠️  Warning: Python $PYTHON_VERSION detected. Python 3.13+ is recommended."
    echo "   The system may still work, but some features might not be available."
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
echo "   This may take a few minutes, especially for tiktoken compilation..."

# Try to install tiktoken first with pre-built wheels
echo "   Installing tiktoken with pre-built wheels..."
pip install --only-binary=all tiktoken || {
    echo "⚠️  Pre-built wheels not available, compiling from source..."
    echo "   This may take several minutes..."
    pip install tiktoken
}

# Install other dependencies
echo "   Installing other dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/ingest
mkdir -p data/rag_workspace
mkdir -p logs
mkdir -p models

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp env.example .env
    echo "   Please edit .env file with your preferences"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Configure your settings (optional):"
echo "      nano .env"
echo ""
echo "   3. Run the system:"
echo "      python main.py streamlit    # Web interface"
echo "      python main.py cli          # Command line"
echo "      python main.py test         # Test system"
echo ""
echo "🌐 Web interface will be available at: http://localhost:8501"
echo ""
echo "📚 For more information, see README.md"
