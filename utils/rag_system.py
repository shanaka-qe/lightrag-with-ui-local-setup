"""
LightRAG System Integration
True HKUDS LightRAG implementation with knowledge graphs
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import LightRAG components
from lightrag import LightRAG, QueryParam

# Import our utilities
from utils.document_ingestion import DocumentIngestion
from utils.llm_provider import OllamaLLM

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleRAG:
    """
    LightRAG system with knowledge graph support
    Uses Ollama for local LLM and embeddings
    """
    
    def __init__(self, working_dir: str = "data/rag_workspace"):
        """
        Initialize LightRAG system
        
        Args:
            working_dir: Directory for RAG data storage
        """
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        
        # LightRAG instance
        self.rag = None
        
        # Document ingestion helper
        self.ingestion = DocumentIngestion()
        
        # Model info
        self.model_name = None
        self.ollama_model = None  # For compatibility with UI status checks
        
        logger.info(f"LightRAG system initialized with working directory: {working_dir}")
    
    def setup_model(self, model_name: str = None) -> None:
        """
        Setup LightRAG with Ollama model
        
        Args:
            model_name: Ollama model name (e.g., gemma3:12b, llama3:8b)
        """
        try:
            model_name = model_name or "gemma3:12b"
            self.model_name = model_name
            
            logger.info(f"Setting up LightRAG with Ollama model: {model_name}")
            
            # Create Ollama LLM wrapper for compatibility
            self.ollama_model = OllamaLLM(model_name=model_name)
            self.ollama_model.load_model()
            
            # Define LLM function for LightRAG
            async def ollama_llm_func(
                prompt,
                system_prompt=None,
                history_messages=[],
                **kwargs
            ) -> str:
                """LLM function for LightRAG using Ollama"""
                # Combine system prompt and prompt
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                # Generate response using Ollama
                response = self.ollama_model.generate(full_prompt, **kwargs)
                return response
            
            # Define embedding function for LightRAG
            async def ollama_embedding_func(texts: List[str]) -> List[List[float]]:
                """Embedding function for LightRAG using Ollama"""
                import ollama
                
                embeddings = []
                for text in texts:
                    try:
                        # Use Ollama's embedding API
                        response = ollama.embeddings(
                            model="nomic-embed-text",  # Optimized for embeddings
                            prompt=text
                        )
                        embeddings.append(response["embedding"])
                    except Exception as e:
                        logger.warning(f"Embedding failed for text, using zeros: {e}")
                        # Return zero vector as fallback
                        embeddings.append([0.0] * 768)
                
                return embeddings
            
            # Initialize LightRAG
            self.rag = LightRAG(
                working_dir=str(self.working_dir),
                llm_model_func=ollama_llm_func,
                llm_model_name=model_name,
                llm_model_max_async=4,
                llm_model_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                # Embedding configuration
                embedding_func=ollama_embedding_func,
                embedding_batch_num=10,
                embedding_func_max_async=4,
                # Knowledge graph settings
                chunk_token_size=1200,
                chunk_overlap_token_size=100,
                max_entity_tokens=6000,
                max_relation_tokens=8000,
                top_k=40,
                chunk_top_k=20,
            )
            
            logger.info("LightRAG setup completed successfully")
            logger.info("Knowledge graph will be created during document ingestion")
            
        except Exception as e:
            logger.error(f"Failed to setup LightRAG: {e}")
            raise
    
    def ingest_documents(self) -> None:
        """
        Ingest documents into LightRAG knowledge graph
        Creates entities and relationships automatically
        """
        if self.rag is None:
            raise RuntimeError("LightRAG not initialized. Call setup_model() first.")
        
        try:
            logger.info("Starting document ingestion into LightRAG...")
            
            # Get all documents from the ingest folder
            documents = self.ingestion.get_documents()
            
            if not documents:
                logger.warning("No documents found in ingest folder")
                return
            
            # Insert each document into LightRAG
            # LightRAG will automatically:
            # 1. Chunk the document
            # 2. Extract entities
            # 3. Identify relationships
            # 4. Build knowledge graph
            # 5. Create embeddings
            for i, doc in enumerate(documents):
                logger.info(f"Ingesting document {i+1}/{len(documents)}: {doc['filename']}")
                
                # Insert document into LightRAG
                self.rag.insert(doc['content'])
                
                logger.info(f"Successfully ingested: {doc['filename']}")
            
            logger.info(f"Successfully ingested {len(documents)} documents into knowledge graph")
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            raise
    
    def query(
        self,
        question: str,
        max_docs: int = 3,
        mode: str = "hybrid"
    ) -> str:
        """
        Query LightRAG system with knowledge graph support
        
        Args:
            question: Question to ask
            max_docs: Not used in LightRAG (kept for API compatibility)
            mode: Query mode
                - "naive": Simple vector similarity
                - "local": Uses local knowledge graph context
                - "global": Uses global knowledge graph structure
                - "hybrid": Combines local and global (recommended)
            
        Returns:
            Answer from LightRAG knowledge graph
        """
        if self.rag is None:
            raise RuntimeError("LightRAG not initialized. Call setup_model() first.")
        
        try:
            logger.info(f"Processing query with mode: {mode}")
            logger.info(f"Question: {question[:100]}...")
            
            # Query LightRAG with specified mode
            response = self.rag.query(
                question,
                param=QueryParam(mode=mode)
            )
            
            logger.info("Query processed successfully using knowledge graph")
            return response
            
        except Exception as e:
            logger.error(f"Failed to process question: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the LightRAG system
        
        Returns:
            Dictionary with system statistics
        """
        try:
            stats = {
                "working_dir": str(self.working_dir),
                "model_loaded": self.ollama_model.is_loaded if self.ollama_model else False,
                "model_name": self.model_name,
                "documents_in_ingest": self.ingestion.get_document_count(),
                "lightrag_enabled": self.rag is not None,
                "knowledge_graph": "Active" if self.rag else "Not initialized"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "working_dir": str(self.working_dir),
                "model_loaded": False,
                "documents_in_ingest": 0,
                "error": str(e)
            }
    
    def cleanup(self) -> None:
        """
        Cleanup resources
        """
        try:
            if self.ollama_model:
                logger.info("Cleaning up Ollama model resources")
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
