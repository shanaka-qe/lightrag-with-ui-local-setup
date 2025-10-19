"""
LightRAG System Integration
Main orchestrator for RAG system with knowledge graphs
"""

import logging
import asyncio
import threading
from typing import List, Dict, Any
from pathlib import Path

# Import LightRAG components (for document ingestion and knowledge graph creation)
from lightrag import LightRAG
from lightrag.llm.ollama import _ollama_model_if_cache as ollama_model_if_cache, ollama_embed

# Import our modular components
from utils.document_ingestion import DocumentIngestion
from utils.graph_visualizer import GraphVisualizer
from utils.query_engine import QueryEngine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleRAG:
    """
    Main RAG system orchestrator
    Coordinates document ingestion, knowledge graph creation, querying, and visualization
    """
    
    def __init__(self, working_dir: str = "data/rag_workspace"):
        """
        Initialize RAG system
        
        Args:
            working_dir: Directory for RAG data storage
        """
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        
        # Core components
        self.rag = None  # LightRAG instance for document ingestion
        self.model_name = None
        
        # Modular components
        self.ingestion = DocumentIngestion()
        self.visualizer = GraphVisualizer(working_dir)
        self.query_engine = None  # Initialized after model setup
        
        logger.info(f"RAG system initialized with working directory: {working_dir}")
    
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
            
            # Initialize query engine with the model
            self.query_engine = QueryEngine(str(self.working_dir), model_name)
            
            # Create LLM wrapper for LightRAG (used during document ingestion)
            def ollama_llm_wrapper(
                prompt,
                system_prompt=None,
                history_messages=[],
                **kwargs
            ):
                """Wrapper to adapt LightRAG's LLM calls to Ollama's format"""
                # Extract parameters and put them in options dict for Ollama
                temperature = kwargs.pop('temperature', 0.7)
                max_tokens = kwargs.pop('max_tokens', 2000)
                
                kwargs['options'] = {
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
                
                # Return coroutine for LightRAG to await
                return ollama_model_if_cache(
                    model=model_name,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    history_messages=history_messages,
                    **kwargs
                )
            
            # Create embedding wrapper for LightRAG
            class OllamaEmbeddingWrapper:
                """Wrapper for Ollama embeddings with LightRAG compatibility"""
                
                def __init__(self):
                    self.embedding_dim = 768  # nomic-embed-text dimension
                    self.max_token_size = 8192
                
                async def __call__(self, texts: list[str]) -> list[list[float]]:
                    """Generate embeddings for a list of texts"""
                    import numpy as np
                    
                    result = await ollama_embed(
                        texts=texts,
                        embed_model="nomic-embed-text",
                        host="http://localhost:11434"
                    )
                    
                    # Convert numpy array to list if needed
                    if isinstance(result, np.ndarray):
                        return result.tolist()
                    return result
            
            # Initialize LightRAG (used for document ingestion and knowledge graph creation)
            self.rag = LightRAG(
                working_dir=str(self.working_dir),
                llm_model_func=ollama_llm_wrapper,
                llm_model_name=model_name,
                llm_model_max_async=4,
                llm_model_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "host": "http://localhost:11434",
                },
                embedding_func=OllamaEmbeddingWrapper(),
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
            
            logger.info("✅ LightRAG setup completed with native Ollama integration")
            
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
            logger.info("Starting document ingestion...")
            
            # Get documents from ingest folder
            documents = self.ingestion.get_documents()
            
            if not documents:
                logger.warning("No documents found in ingest folder")
                return
            
            # Run async ingestion in a new thread with its own event loop
            result = {'success': False, 'error': None}
            
            def run_in_thread():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._ingest_documents_async(documents))
                    result['success'] = True
                except Exception as e:
                    result['error'] = e
                finally:
                    loop.close()
            
            thread = threading.Thread(target=run_in_thread)
            thread.start()
            thread.join()
            
            if not result['success']:
                raise result['error'] or Exception("Unknown error during ingestion")
            
            logger.info(f"✅ Successfully ingested {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            raise
    
    async def _ingest_documents_async(self, documents):
        """Async helper for document ingestion"""
        # Initialize LightRAG storages
        try:
            await self.rag.initialize_storages()
            
            from lightrag.kg.shared_storage import initialize_pipeline_status
            await initialize_pipeline_status()
            
        except Exception as e:
            logger.debug(f"Storage initialization note: {e}")
            pass  # May already be initialized
        
        # Insert each document into LightRAG for knowledge graph creation
        for i, doc in enumerate(documents):
            logger.info(f"Ingesting document {i+1}/{len(documents)}: {doc['filename']}")
            await self.rag.ainsert(doc['content'])
            logger.info(f"Successfully ingested: {doc['filename']}")
    
    def query(
        self,
        question: str,
        max_docs: int = 3,
        mode: str = "hybrid"
    ) -> str:
        """
        Query the RAG system with a question
        
        Args:
            question: Question to ask about the documents
            max_docs: Not used (kept for API compatibility)
            mode: Query mode (kept for API compatibility)
            
        Returns:
            Answer generated by Ollama based on document content
        """
        if self.query_engine is None:
            raise RuntimeError("Query engine not initialized. Call setup_model() first.")
        
        return self.query_engine.query(question, mode)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system
        
        Returns:
            Dictionary with system statistics
        """
        try:
            graph_stats = self.visualizer.get_graph_stats()
            
            stats = {
                "working_dir": str(self.working_dir),
                "model_loaded": self.rag is not None,
                "model_name": self.model_name,
                "documents_in_ingest": self.ingestion.get_document_count(),
                "lightrag_enabled": self.rag is not None,
                "knowledge_graph": "Active" if self.rag else "Not initialized",
                "graph_entities": graph_stats.get("nodes", 0),
                "graph_relationships": graph_stats.get("edges", 0)
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
    
    def get_graph_visualization(self) -> str:
        """
        Get knowledge graph visualization
        
        Returns:
            HTML string for interactive graph or None if no graph exists
        """
        return self.visualizer.generate_visualization()
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge graph
        
        Returns:
            Dictionary with graph statistics
        """
        return self.visualizer.get_graph_stats()
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        logger.info("Cleanup completed")
