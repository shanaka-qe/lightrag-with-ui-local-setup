"""
Streamlit UI for RAG System
Simple web interface to interact with the RAG system
"""

import streamlit as st
import logging
from pathlib import Path
import time

# Import our modules
from utils.rag_system import SimpleRAG
from utils.document_ingestion import DocumentIngestion
from config.settings import STREAMLIT_CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_rag_system():
    """Initialize the RAG system"""
    try:
        if st.session_state.rag_system is None:
            st.session_state.rag_system = SimpleRAG()
            st.session_state.model_loaded = False
            st.session_state.documents_ingested = False
        return True
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {e}")
        return False


def load_model(model_name=None):
    """Load the LLM model"""
    try:
        if not st.session_state.model_loaded:
            with st.spinner("Loading model... This may take a few minutes on first run."):
                st.session_state.rag_system.setup_model(model_name)
                st.session_state.model_loaded = True
            st.success("Model loaded successfully!")
        return True
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return False


def ingest_documents():
    """Ingest documents from the ingest folder"""
    try:
        if not st.session_state.documents_ingested:
            with st.spinner("Ingesting documents..."):
                st.session_state.rag_system.ingest_documents()
                st.session_state.documents_ingested = True
            st.success("Documents ingested successfully!")
        return True
    except Exception as e:
        st.error(f"Failed to ingest documents: {e}")
        return False


# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'documents_ingested' not in st.session_state:
    st.session_state.documents_ingested = False

# Auto-initialize system at startup
if st.session_state.rag_system is None:
    if initialize_rag_system():
        st.session_state.rag_system.setup_model("gemma3:12b")
        st.session_state.model_loaded = True
        # Note: Document ingestion is manual via button due to processing time


def main():
    """Main Streamlit application"""
    
    # Title and description
    st.title("🤖 LightRAG Implementation with Local LLM")
    st.markdown("**Retrieval-Augmented Generation using LightRAG and Gemma 2 12B**")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Ingest Documents button
        if st.button("📚 Ingest Documents", disabled=not st.session_state.model_loaded):
            with st.spinner("Ingesting documents... This may take several minutes."):
                try:
                    st.session_state.rag_system.ingest_documents()
                    st.session_state.documents_ingested = True
                    st.success("✅ Documents ingested successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to ingest documents: {e}")
        
        st.markdown("---")
        
        # System status
        st.subheader("📊 System Status")
        st.write(f"**RAG System:** {'✅ Initialized' if st.session_state.rag_system else '❌ Not initialized'}")
        st.write(f"**Model:** {'✅ Loaded (gemma3:12b)' if st.session_state.model_loaded else '❌ Not loaded'}")
        
        # Show actual document count
        if st.session_state.rag_system:
            try:
                doc_count = st.session_state.rag_system.ingestion.get_document_count()
                st.write(f"**Documents:** ✅ {doc_count} loaded")
            except:
                st.write(f"**Documents:** {'✅ Ingested' if st.session_state.documents_ingested else '❌ Not ingested'}")
        else:
            st.write(f"**Documents:** {'✅ Ingested' if st.session_state.documents_ingested else '❌ Not ingested'}")
        
        # System stats
        if st.session_state.rag_system:
            try:
                stats = st.session_state.rag_system.get_stats()
                st.subheader("📈 Statistics")
                for key, value in stats.items():
                    st.write(f"**{key}:** {value}")
            except:
                st.write("**Status:** System ready")
    
    # Main content area
    if not st.session_state.rag_system or not st.session_state.model_loaded:
        st.warning("🔄 System is initializing... Please wait a moment.")
        return
    
    # Show document status
    if st.session_state.rag_system:
        try:
            doc_count = st.session_state.rag_system.ingestion.get_document_count()
            if doc_count > 0:
                st.success(f"📚 {doc_count} documents loaded and ready for queries!")
            else:
                st.info("📚 No documents loaded. Add files to the 'data/ingest' folder and restart the system.")
        except:
            st.info("📚 Documents status unavailable.")
    
    # Query interface
    st.header("💬 Ask Questions")
    
    # Query mode selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input(
            "Enter your question:",
            placeholder="What is this document about?",
            key="question_input"
        )
    
    with col2:
        query_mode = st.selectbox(
            "Query Mode",
            ["hybrid", "naive", "local", "global"],
            index=0,
            help="hybrid: Best of local and global, naive: Simple retrieval, local: Local context, global: Global context"
        )
    
    # Ask question button
    if st.button("🔍 Ask Question", type="primary", disabled=not question):
        if question:
            try:
                with st.spinner("Thinking..."):
                    answer = st.session_state.rag_system.query(question, mode=query_mode)
                
                st.subheader("💡 Answer")
                st.write(answer)
                
                # Store in session state for history
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': answer,
                    'mode': query_mode,
                    'timestamp': time.time()
                })
                
            except Exception as e:
                st.error(f"Failed to process question: {e}")
    
    # Chat history
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        st.header("📝 Chat History")
        
        # Show recent conversations
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
            with st.expander(f"Q: {chat['question'][:50]}..."):
                st.write(f"**Question:** {chat['question']}")
                st.write(f"**Mode:** {chat['mode']}")
                st.write(f"**Answer:** {chat['answer']}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Knowledge Graph Visualization
    st.header("🕸️ Knowledge Graph Visualization")
    
    if st.session_state.rag_system:
        # Get graph statistics
        graph_stats = st.session_state.rag_system.get_graph_stats()
        
        if graph_stats.get("exists"):
            # Display graph statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Entities", graph_stats.get("nodes", 0))
            with col2:
                st.metric("Relationships", graph_stats.get("edges", 0))
            with col3:
                st.metric("Density", f"{graph_stats.get('density', 0):.3f}")
            with col4:
                st.metric("Components", graph_stats.get("connected_components", 0))
            
            # Add refresh button
            if st.button("🔄 Refresh Graph Visualization"):
                st.rerun()
            
            # Generate and display visualization
            with st.spinner("Generating interactive graph visualization..."):
                graph_html = st.session_state.rag_system.get_graph_visualization()
                
                if graph_html:
                    st.subheader("Interactive Knowledge Graph")
                    st.info("💡 **Tip:** Click and drag nodes to explore. Hover over nodes and edges to see details.")
                    
                    # Display the interactive graph
                    import streamlit.components.v1 as components
                    components.html(graph_html, height=650, scrolling=True)
                    
                    # Legend
                    st.markdown("""
                    **Legend:**
                    - 🔴 **Red**: People/Persons
                    - 🔵 **Teal**: Organizations
                    - 🟦 **Blue**: Technologies
                    - 🟧 **Orange**: Projects
                    - 🟩 **Green**: Locations
                    - ⚫ **Gray**: Other entities
                    """)
                else:
                    st.warning("Unable to generate graph visualization. Please ensure documents have been ingested.")
        else:
            st.info("📊 No knowledge graph available yet. Ingest documents to build the graph!")
            if graph_stats.get("message"):
                st.write(graph_stats["message"])
    else:
        st.warning("RAG system not initialized")
    
    # Document management
    st.header("📁 Document Management")
    
    # Show documents in ingest folder
    ingestion = DocumentIngestion()
    documents = ingestion.get_documents()
    
    if documents:
        st.write(f"**Found {len(documents)} documents in ingest folder:**")
        for doc in documents:
            st.write(f"- {doc['filename']} ({doc['file_type']})")
    else:
        st.warning("No documents found in the ingest folder. Add documents to `data/ingest/` folder.")
    
    # File upload for new documents
    st.subheader("📤 Upload New Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'md', 'pdf', 'docx', 'csv'],
        help="Upload a document to add to the RAG system"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to ingest folder
        file_path = Path("data/ingest") / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File {uploaded_file.name} uploaded successfully!")
        st.info("Click 'Ingest Documents' in the sidebar to process the new document.")
    
    # Footer
    st.markdown("---")
    st.markdown("**RAG System** - Powered by LightRAG and Gemma 2 12B")


if __name__ == "__main__":
    main()
