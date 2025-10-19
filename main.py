"""
Main application for RAG System
Simple command-line interface and Streamlit launcher
"""

import sys
import argparse
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from utils.rag_system import SimpleRAG
from utils.document_ingestion import DocumentIngestion
from config.settings import STREAMLIT_CONFIG


def run_streamlit():
    """Run the Streamlit web interface"""
    import subprocess
    import os
    import signal
    
    print("🚀 Starting Streamlit web interface...")
    print(f"📱 Open your browser to: http://{STREAMLIT_CONFIG['host']}:{STREAMLIT_CONFIG['port']}")
    
    # Kill existing processes on the port
    try:
        # Kill processes on the specific port
        subprocess.run(["lsof", "-ti", f":{STREAMLIT_CONFIG['port']}", "|", "xargs", "kill", "-9"], shell=True, check=False)
        print(f"🔄 Killed existing processes on port {STREAMLIT_CONFIG['port']}")
    except:
        pass
    
    # Also kill any existing Streamlit processes
    try:
        subprocess.run(["pkill", "-f", "streamlit"], check=False)
        print("🔄 Killed existing Streamlit processes")
    except:
        pass
    
    # Run Streamlit
    subprocess.run([
        "streamlit", "run", "app.py",
        "--server.port", str(STREAMLIT_CONFIG['port']),
        "--server.address", STREAMLIT_CONFIG['host']
    ])


def run_cli():
    """Run the command-line interface"""
    print("🤖 RAG System - Command Line Interface")
    print("=" * 50)
    
    # Create RAG system
    rag = SimpleRAG()
    
    try:
        # Set up the model
        print("📥 Setting up model...")
        rag.setup_model()
        
        # Ingest documents
        print("📚 Ingesting documents...")
        rag.ingest_documents()
        
        # Interactive query loop
        print("\n💬 Interactive Mode")
        print("Type 'quit' to exit")
        print("=" * 30)
        
        while True:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            try:
                print("🤔 Thinking...")
                answer = rag.query(question)
                print(f"💡 Answer: {answer}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        rag.cleanup()


def test_system():
    """Test the RAG system with sample data"""
    print("🧪 Testing RAG System")
    print("=" * 30)
    
    # Create RAG system
    rag = SimpleRAG()
    
    try:
        # Set up the model
        print("📥 Setting up model...")
        rag.setup_model()
        
        # Create sample document
        sample_doc_path = Path("data/ingest/sample.txt")
        sample_doc_path.parent.mkdir(exist_ok=True)
        
        sample_content = """
        Artificial Intelligence (AI) is a branch of computer science that aims to create machines 
        that can perform tasks that typically require human intelligence. These tasks include 
        learning, reasoning, problem-solving, perception, and language understanding.
        
        Machine Learning is a subset of AI that focuses on algorithms that can learn from data. 
        Deep Learning is a subset of machine learning that uses neural networks with multiple layers.
        """
        
        with open(sample_doc_path, 'w') as f:
            f.write(sample_content)
        
        print("📝 Created sample document")
        
        # Ingest documents
        print("📚 Ingesting documents...")
        rag.ingest_documents()
        
        # Test queries
        test_questions = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What is the difference between AI and machine learning?"
        ]
        
        for question in test_questions:
            print(f"\n❓ Question: {question}")
            answer = rag.query(question)
            print(f"💡 Answer: {answer}")
        
        # Show stats
        print("\n📊 System Statistics:")
        stats = rag.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Clean up sample file
        sample_doc_path.unlink()
        print("\n🗑️ Cleaned up sample file")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        rag.cleanup()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="RAG System with Local LLM")
    parser.add_argument(
        "mode",
        choices=["streamlit", "cli", "test"],
        help="Run mode: streamlit (web UI), cli (command line), test (system test)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "streamlit":
        run_streamlit()
    elif args.mode == "cli":
        run_cli()
    elif args.mode == "test":
        test_system()


if __name__ == "__main__":
    main()
