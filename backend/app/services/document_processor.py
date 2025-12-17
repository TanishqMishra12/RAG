"""Document processing service for PDF parsing and chunking."""
import os
from typing import List, Dict
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """Service for processing PDF documents."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}"
        return text
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split text into chunks with metadata.
        
        Args:
            text: Text to split
            metadata: Metadata to attach to chunks
            
        Returns:
            List of chunks with metadata
        """
        if metadata is None:
            metadata = {}
        
        chunks = self.text_splitter.split_text(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            result.append({
                "content": chunk,
                "metadata": chunk_metadata
            })
        
        return result
    
    def process_document(self, file_path: str, document_id: str, filename: str) -> List[Dict]:
        """Process a document end-to-end.
        
        Args:
            file_path: Path to the PDF file
            document_id: Unique identifier for the document
            filename: Original filename
            
        Returns:
            List of processed chunks
        """
        # Extract text
        text = self.extract_text_from_pdf(file_path)
        
        # Create metadata
        metadata = {
            "document_id": document_id,
            "filename": filename,
            "file_path": file_path
        }
        
        # Chunk text
        chunks = self.chunk_text(text, metadata)
        
        return chunks
