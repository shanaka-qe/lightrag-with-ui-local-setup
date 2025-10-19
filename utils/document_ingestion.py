"""
Data ingestion module for RAG system
Handles loading and processing documents from the ingest folder
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentIngestion:
    """
    Handles document ingestion for the RAG system
    Reads documents from the data/ingest folder and processes them
    """
    
    def __init__(self, ingest_dir: str = "data/ingest"):
        """
        Initialize the document ingestion system
        
        Args:
            ingest_dir: Directory containing documents to ingest
        """
        self.ingest_dir = Path(ingest_dir)
        self.ingest_dir.mkdir(exist_ok=True)
        
        # Supported file extensions
        self.supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.csv'}
        
        logger.info(f"Document ingestion initialized with directory: {self.ingest_dir}")
    
    def get_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents from the ingest directory
        
        Returns:
            List of document dictionaries with content and metadata
        """
        documents = []
        
        # Walk through all files in the ingest directory
        for file_path in self.ingest_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    # Read file content
                    content = self._read_file(file_path)
                    
                    if content.strip():  # Only add non-empty files
                        documents.append({
                            'content': content,
                            'filename': file_path.name,
                            'filepath': str(file_path),
                            'file_type': file_path.suffix.lower()
                        })
                        
                        logger.info(f"Loaded document: {file_path.name}")
                    
                except Exception as e:
                    logger.error(f"Failed to read file {file_path}: {e}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def _read_file(self, file_path: Path) -> str:
        """
        Read content from a file based on its extension
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
        """
        extension = file_path.suffix.lower()
        
        if extension == '.txt' or extension == '.md':
            return self._read_text_file(file_path)
        elif extension == '.pdf':
            return self._read_pdf_file(file_path)
        elif extension == '.docx':
            return self._read_docx_file(file_path)
        elif extension == '.csv':
            return self._read_csv_file(file_path)
        else:
            # Try to read as text file
            return self._read_text_file(file_path)
    
    def _read_text_file(self, file_path: Path) -> str:
        """Read a text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _read_pdf_file(self, file_path: Path) -> str:
        """Read a PDF file"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            logger.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"Failed to read PDF {file_path}: {e}")
            return ""
    
    def _read_docx_file(self, file_path: Path) -> str:
        """Read a DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            logger.warning("python-docx not installed. Install with: pip install python-docx")
            return ""
        except Exception as e:
            logger.error(f"Failed to read DOCX {file_path}: {e}")
            return ""
    
    def _read_csv_file(self, file_path: Path) -> str:
        """Read a CSV file"""
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            # Convert DataFrame to text
            text = df.to_string(index=False)
            return text
        except ImportError:
            logger.warning("pandas not installed. Install with: pip install pandas")
            return ""
        except Exception as e:
            logger.error(f"Failed to read CSV {file_path}: {e}")
            return ""
    
    def get_document_count(self) -> int:
        """
        Get the number of documents in the ingest directory
        
        Returns:
            Number of documents
        """
        count = 0
        for file_path in self.ingest_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                count += 1
        return count
    
    def clear_ingest_folder(self) -> None:
        """
        Clear all files from the ingest directory
        Use with caution - this will delete all files!
        """
        for file_path in self.ingest_dir.rglob('*'):
            if file_path.is_file():
                file_path.unlink()
                logger.info(f"Deleted file: {file_path.name}")
        
        logger.info("Ingest directory cleared")


