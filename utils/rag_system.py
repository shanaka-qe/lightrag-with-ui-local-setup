"""
Simple RAG System using Ollama
Provides a basic interface for document ingestion and querying
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from utils.llm_provider import OllamaLLM
from utils.document_ingestion import DocumentIngestion

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleRAG:
    """
    Simple RAG system using Ollama for both embedding and generation
    """
    
    def __init__(self, working_dir: str = "data/rag_workspace"):
        """
        Initialize the RAG system
        
        Args:
            working_dir: Directory for RAG data storage
        """
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        
        self.ollama_model = None
        self.ingestion = DocumentIngestion()
        self.documents = []
        self.document_index = {}
        
        logger.info(f"Simple RAG system initialized with working directory: {working_dir}")
    
    def setup_model(self, model_name: str = None) -> None:
        """
        Setup the Ollama model
        
        Args:
            model_name: Name of the model to use
        """
        try:
            model_name = model_name or "gemma3:12b"
            logger.info(f"Setting up Ollama model: {model_name}")
            
            # Initialize Ollama model
            self.ollama_model = OllamaLLM(model_name=model_name)
            self.ollama_model.load_model()
            
            logger.info("Model setup completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup model: {e}")
            raise
    
    def ingest_documents(self) -> None:
        """
        Ingest documents from the data/ingest folder
        """
        if self.ollama_model is None:
            raise RuntimeError("RAG system not initialized. Call setup_model() first.")
        
        try:
            logger.info("Starting document ingestion...")
            
            # Get all documents from the ingest folder
            documents = self.ingestion.get_documents()
            
            if not documents:
                logger.warning("No documents found in ingest folder")
                return
            
            # Store documents
            self.documents = documents
            
            # Create simple index (just store document content)
            self.document_index = {}
            for i, doc in enumerate(documents):
                self.document_index[i] = {
                    'content': doc['content'],
                    'filename': doc['filename'],
                    'filepath': doc['filepath']
                }
            
            # Save to disk for persistence
            self._save_documents()
            
            logger.info(f"Successfully ingested {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            raise
    
    def _save_documents(self) -> None:
        """Save documents to disk for persistence"""
        try:
            index_file = self.working_dir / "document_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self.document_index, f, indent=2, ensure_ascii=False)
            logger.info(f"Document index saved to {index_file}")
        except Exception as e:
            logger.error(f"Failed to save documents: {e}")
    
    def _load_documents(self) -> None:
        """Load documents from disk"""
        try:
            index_file = self.working_dir / "document_index.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.document_index = json.load(f)
                logger.info(f"Document index loaded from {index_file}")
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
    
    def query(self, question: str, max_docs: int = 3, mode: str = "hybrid") -> str:
        """
        Query the RAG system with a question
        
        Args:
            question: Question to ask
            max_docs: Maximum number of documents to use for context
            mode: Query mode (for compatibility, not used in simple implementation)
            
        Returns:
            Answer from the RAG system
        """
        if self.ollama_model is None:
            raise RuntimeError("RAG system not initialized. Call setup_model() first.")
        
        try:
            logger.info(f"Processing query: {question[:50]}...")
            
            # Load documents if not already loaded
            if not self.document_index:
                self._load_documents()
            
            if not self.document_index:
                return "No documents available for querying. Please ingest documents first."
            
            # Improved retrieval: search for relevant content
            context_docs = []
            question_lower = question.lower()
            
            for doc_id, doc_data in list(self.document_index.items())[:max_docs]:
                content = doc_data['content']
                content_lower = content.lower()
                
                # Check if document contains relevant keywords
                relevant_keywords = []
                for word in question_lower.split():
                    if len(word) > 3 and word in content_lower:
                        relevant_keywords.append(word)
                
                # If document seems relevant or we need more context, include it
                if relevant_keywords or len(context_docs) < max_docs:
                    # Try to find the most relevant section
                    lines = content.split('\n')
                    relevant_lines = []
                    
                    for line in lines:
                        line_lower = line.lower()
                        if any(keyword in line_lower for keyword in relevant_keywords):
                            relevant_lines.append(line)
                    
                    # If we found relevant lines, use them; otherwise use the full content
                    if relevant_lines:
                        relevant_content = '\n'.join(relevant_lines)
                    else:
                        relevant_content = content[:800]  # Use more content for better context
                    
                    context_docs.append(f"From {doc_data['filename']}:\n{relevant_content}")
            
            context = "\n\n".join(context_docs)
            
            # Create prompt for the model
            prompt = f"""Based on the following information, please answer the question.

Information:
{context}

Question: {question}

Please provide a clear and direct answer. If the information is not available, please say so."""

            # Generate response using Ollama
            response = self.ollama_model.generate(prompt)
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system
        
        Returns:
            Dictionary with system statistics
        """
        try:
            # Load documents if not already loaded
            if not self.document_index:
                self._load_documents()
            
            stats = {
                "working_dir": str(self.working_dir),
                "model_loaded": self.ollama_model.is_loaded if self.ollama_model else False,
                "documents_in_ingest": self.ingestion.get_document_count(),
                "documents_loaded": len(self.document_index)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "working_dir": str(self.working_dir),
                "model_loaded": False,
                "documents_in_ingest": 0,
                "documents_loaded": 0,
                "error": str(e)
            }
    
    def cleanup(self) -> None:
        """
        Cleanup resources
        """
        try:
            if self.ollama_model:
                self.ollama_model.cleanup()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

