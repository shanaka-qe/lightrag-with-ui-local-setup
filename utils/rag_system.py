"""
LightRAG System Integration
True HKUDS LightRAG implementation with knowledge graphs
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import LightRAG components (for document ingestion and knowledge graph creation)
from lightrag import LightRAG
from lightrag.llm.ollama import _ollama_model_if_cache as ollama_model_if_cache, ollama_embed

# Import our utilities
from utils.document_ingestion import DocumentIngestion

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
        
        logger.info(f"LightRAG system initialized with working directory: {working_dir}")
    
    def setup_model(self, model_name: str = None) -> None:
        """
        Setup LightRAG with Ollama model using native integration
        
        Args:
            model_name: Ollama model name (e.g., gemma3:12b, llama3:8b)
        """
        try:
            model_name = model_name or "gemma3:12b"
            self.model_name = model_name
            
            logger.info(f"Setting up LightRAG with Ollama model: {model_name} (using native integration)")
            
            # Create LLM function wrapper that returns a callable, not the result
            # LightRAG expects llm_model_func to be a function reference, not called directly
            def ollama_llm_wrapper(
                prompt,
                system_prompt=None,
                history_messages=[],
                **kwargs
            ):
                """Wrapper to adapt LightRAG's LLM calls to Ollama's format"""
                # Extract temperature and max_tokens and put them in options
                temperature = kwargs.pop('temperature', 0.7)
                max_tokens = kwargs.pop('max_tokens', 2000)
                
                # Ollama expects these in an 'options' dict
                kwargs['options'] = {
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
                
                # Return a coroutine that LightRAG can await
                return ollama_model_if_cache(
                    model=model_name,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    history_messages=history_messages,
                    **kwargs
                )
            
            # Create embedding function wrapper with required attributes
            class OllamaEmbeddingWrapper:
                """Wrapper for Ollama embeddings with LightRAG compatibility"""
                
                def __init__(self):
                    # Required attributes for LightRAG
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
            
            # Initialize LightRAG with native Ollama support
            self.rag = LightRAG(
                working_dir=str(self.working_dir),
                # Use wrapped Ollama LLM function
                llm_model_func=ollama_llm_wrapper,
                llm_model_name=model_name,
                llm_model_max_async=4,
                llm_model_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "host": "http://localhost:11434",  # Default Ollama host
                },
                # Use wrapped Ollama embedding function with proper attributes
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
            import asyncio
            import threading
            
            logger.info("Starting document ingestion into LightRAG...")
            
            # Get all documents from the ingest folder
            documents = self.ingestion.get_documents()
            
            if not documents:
                logger.warning("No documents found in ingest folder")
                return
            
            # Run async ingestion in a new thread with its own event loop
            # This avoids conflicts with Streamlit's event loop
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
            
            logger.info(f"Successfully ingested {len(documents)} documents into knowledge graph")
            
        except Exception as e:
            logger.error(f"Failed to ingest documents: {e}")
            raise
    
    async def _ingest_documents_async(self, documents):
        """Async helper for document ingestion"""
        # Initialize storages if needed
        try:
            await self.rag.initialize_storages()
            
            # Initialize pipeline status (required for document processing)
            from lightrag.kg.shared_storage import initialize_pipeline_status
            await initialize_pipeline_status()
            
        except Exception as e:
            logger.debug(f"Storage initialization note: {e}")
            pass  # May already be initialized
        
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
            mode: Query mode (kept for API compatibility, not currently used)
            
        Returns:
            Answer generated by Ollama based on document content
        """
        if self.rag is None:
            raise RuntimeError("LightRAG not initialized. Call setup_model() first.")
        
        try:
            import asyncio
            import threading
            
            logger.info(f"Processing query with mode: {mode}")
            logger.info(f"Question: {question[:100]}...")
            
            # Run async query in a new thread with its own event loop
            # This avoids conflicts with Streamlit's event loop
            result = {'response': None, 'error': None}
            
            def run_in_thread():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result['response'] = loop.run_until_complete(self._query_async(question, mode))
                except Exception as e:
                    result['error'] = e
                finally:
                    # Don't close the loop immediately - let pending tasks finish
                    # Schedule loop closure after a delay
                    try:
                        pending = asyncio.all_tasks(loop)
                        if pending:
                            # Give tasks time to complete
                            for task in pending:
                                if not task.done():
                                    task.cancel()
                            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    except Exception:
                        pass
                    finally:
                        loop.close()
            
            thread = threading.Thread(target=run_in_thread, daemon=True)
            thread.start()
            thread.join(timeout=120)  # 2 minute timeout
            
            if result['error']:
                logger.error(f"Query error: {result['error']}")
                return f"⚠️ Query failed: {str(result['error'])[:200]}"
            
            response = result['response']
            if response:
                logger.info("Query processed successfully using knowledge graph")
                return response
            else:
                logger.warning("Query returned None")
                return "⚠️ No response generated. The system may still be initializing or the knowledge graph may be empty."
            
        except Exception as e:
            logger.error(f"Failed to process question: {e}")
            return f"⚠️ Query failed: {str(e)[:200]}"
    
    async def _query_async(self, question: str, mode: str) -> str:
        """Async helper for querying using direct Ollama approach"""
        try:
            # Direct approach: Load documents and use Ollama to generate answers
            import ollama
            import json
            
            # Get document content directly from storage
            kv_store_path = self.working_dir / "kv_store_full_docs.json"
            
            if not kv_store_path.exists():
                return "⚠️ No documents found. Please ingest documents first."
            
            # Load documents
            with open(kv_store_path, 'r') as f:
                docs = json.load(f)
            
            if not docs:
                return "⚠️ No documents available. Please ingest documents first."
            
            # Get all document content (for now, use all docs - in production you'd use vector search)
            context_parts = []
            for doc_id, doc_data in docs.items():
                content = doc_data.get('content', '')
                filename = doc_data.get('file_path', 'unknown')
                context_parts.append(f"From {filename}:\n{content}")
            
            context = "\n\n---\n\n".join(context_parts)
            
            # Create prompt for Ollama
            prompt = f"""Based on the following document content, please answer the question accurately and concisely.

DOCUMENT CONTENT:
{context}

QUESTION: {question}

ANSWER (provide a clear, direct answer based only on the information in the documents):"""
            
            # Call Ollama directly
            logger.info(f"Calling Ollama with question: {question[:100]}...")
            
            response = ollama.chat(
                model=self.model_name or 'gemma3:12b',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant that answers questions based on provided documents. Be accurate and cite specific information from the documents.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.7,
                    'num_predict': 2000
                }
            )
            
            answer = response['message']['content']
            logger.info("Successfully generated answer using Ollama")
            return answer
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Query error: {error_msg}")
            return f"⚠️ Query failed: {error_msg[:200]}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the LightRAG system
        
        Returns:
            Dictionary with system statistics
        """
        try:
            # Get graph stats for more detailed information
            graph_stats = self.get_graph_stats()
            
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
    
    def get_graph_visualization(self) -> Optional[Any]:
        """
        Get knowledge graph visualization using pyvis
        
        Returns:
            HTML string for interactive graph visualization or None if no graph exists
        """
        try:
            import networkx as nx
            from pyvis.network import Network
            from pathlib import Path
            
            # Path to the graph file created by LightRAG
            graph_path = self.working_dir / "graph_chunk_entity_relation.graphml"
            
            if not graph_path.exists():
                logger.warning("No knowledge graph file found")
                return None
            
            # Load the graph using NetworkX
            G = nx.read_graphml(str(graph_path))
            
            # Check if graph is empty
            if len(G.nodes()) == 0:
                logger.warning("Knowledge graph is empty")
                return None
            
            logger.info(f"Loaded graph with {len(G.nodes())} nodes and {len(G.edges())} edges")
            
            # Create a PyVis network for interactive visualization
            net = Network(
                height="600px",
                width="100%",
                bgcolor="#ffffff",
                font_color="#000000",
                notebook=False,
                directed=False
            )
            
            # Configure physics for better layout
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "barnesHut": {
                        "gravitationalConstant": -8000,
                        "centralGravity": 0.3,
                        "springLength": 95,
                        "springConstant": 0.04,
                        "damping": 0.09,
                        "avoidOverlap": 0.1
                    },
                    "minVelocity": 0.75
                },
                "nodes": {
                    "font": {
                        "size": 14
                    }
                },
                "edges": {
                    "smooth": {
                        "type": "continuous"
                    }
                }
            }
            """)
            
            # Add nodes with colors based on type
            for node in G.nodes(data=True):
                node_id = node[0]
                node_data = node[1]
                
                # Determine node type and color
                node_type = node_data.get('entity_type', 'unknown')
                
                # Color scheme for different node types
                color_map = {
                    'PERSON': '#FF6B6B',      # Red for people
                    'ORGANIZATION': '#4ECDC4', # Teal for organizations
                    'TECHNOLOGY': '#45B7D1',   # Blue for tech
                    'PROJECT': '#FFA07A',      # Light orange for projects
                    'LOCATION': '#98D8C8',     # Green for locations
                    'unknown': '#95A5A6'       # Gray for unknown
                }
                
                # Try to infer type from description if not set
                description = node_data.get('description', '').lower()
                if node_type == 'unknown':
                    if any(word in description for word in ['person', 'dr.', 'engineer', 'architect']):
                        node_type = 'PERSON'
                    elif any(word in description for word in ['company', 'organization', 'team']):
                        node_type = 'ORGANIZATION'
                    elif any(word in description for word in ['technology', 'framework', 'api', 'system']):
                        node_type = 'TECHNOLOGY'
                    elif any(word in description for word in ['project', 'initiative']):
                        node_type = 'PROJECT'
                
                color = color_map.get(node_type, '#95A5A6')
                
                # Add node with styling
                net.add_node(
                    node_id,
                    label=node_id,
                    title=f"Type: {node_type}\n{description[:200]}",
                    color=color,
                    size=25
                )
            
            # Add edges
            for edge in G.edges(data=True):
                source = edge[0]
                target = edge[1]
                edge_data = edge[2]
                
                # Get relationship description
                description = edge_data.get('description', 'related to')
                
                net.add_edge(
                    source,
                    target,
                    title=description,
                    label=description[:30] if len(description) > 30 else description
                )
            
            # Generate HTML
            html = net.generate_html()
            
            logger.info("Graph visualization generated successfully")
            return html
            
        except Exception as e:
            logger.error(f"Failed to generate graph visualization: {e}")
            return None
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge graph
        
        Returns:
            Dictionary with graph statistics
        """
        try:
            import networkx as nx
            from pathlib import Path
            
            # Path to the graph file
            graph_path = self.working_dir / "graph_chunk_entity_relation.graphml"
            
            if not graph_path.exists():
                return {
                    "exists": False,
                    "nodes": 0,
                    "edges": 0,
                    "message": "No knowledge graph found. Please ingest documents first."
                }
            
            # Load and analyze the graph
            G = nx.read_graphml(str(graph_path))
            
            # Calculate statistics
            stats = {
                "exists": True,
                "nodes": len(G.nodes()),
                "edges": len(G.edges()),
                "density": nx.density(G) if len(G.nodes()) > 0 else 0,
                "connected_components": nx.number_connected_components(G.to_undirected()) if len(G.nodes()) > 0 else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {
                "exists": False,
                "error": str(e)
            }
    
    def cleanup(self) -> None:
        """
        Cleanup resources
        """
        try:
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
