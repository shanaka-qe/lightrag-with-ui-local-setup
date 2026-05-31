"""
Configuration settings for the RAG application
Reads from environment variables and provides default values
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# LLM Configuration - Using Ollama
LLM_CONFIG = {
    "model_name": os.getenv("LLM_MODEL_NAME", "gemma3:12b"),
    "host": os.getenv("LLM_HOST", "http://localhost:11434"),
    "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "512"))
}

# RAG Configuration
RAG_CONFIG = {
    "working_dir": os.getenv("RAG_WORKING_DIR", "data/rag_workspace"),
    "embedding_model": os.getenv("RAG_EMBEDDING_MODEL", "nomic-embed-text"),
    "max_token": int(os.getenv("RAG_MAX_TOKEN", "2000")),
    "timeout": int(os.getenv("RAG_TIMEOUT", "30"))
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "port": int(os.getenv("STREAMLIT_PORT", "8501")),
    "host": os.getenv("STREAMLIT_HOST", "localhost")
}

# Directory paths
DATA_DIR = PROJECT_ROOT / "data"
INGEST_DIR = DATA_DIR / "ingest"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, INGEST_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Available Ollama models (install with: ollama pull <model_name>)
AVAILABLE_MODELS = [
    "gemma3:12b",
    "gemma2:12b", 
    "gemma2:9b",
    "gemma2:2b",
    "llama3:8b",
    "llama3:70b",
    "mistral:7b",
    "codellama:7b"
]
