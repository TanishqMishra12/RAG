"""API routes for the RAG application."""
import os
import uuid
from datetime import datetime
from typing import Dict
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from backend.app.config import get_settings
from backend.app.models.schemas import (
    DocumentUploadResponse,
    QueryRequest,
    QueryResponse,
    HealthResponse,
    DocumentChunk
)
from backend.app.services.vector_store import VectorStore
from backend.app.services.rag_service import RAGService
from backend.app.services.inngest_service import send_document_event

router = APIRouter()
settings = get_settings()

# Initialize services
vector_store = VectorStore(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    collection_name=settings.qdrant_collection_name,
    openai_api_key=settings.openai_api_key,
    embedding_model=settings.embedding_model
)

rag_service = RAGService(
    openai_api_key=settings.openai_api_key,
    model=settings.chat_model
)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    qdrant_connected = vector_store.health_check()
    
    return HealthResponse(
        status="healthy" if qdrant_connected else "degraded",
        qdrant_connected=qdrant_connected,
        timestamp=datetime.utcnow()
    )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document for processing.
    
    Args:
        file: PDF file to upload
        
    Returns:
        Upload response with document ID
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save file temporarily
        file_path = f"uploads/{document_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Send event to Inngest for async processing
        event_result = send_document_event(
            document_id=document_id,
            file_path=file_path,
            filename=file.filename
        )
        
        if event_result.get("success"):
            return DocumentUploadResponse(
                document_id=document_id,
                filename=file.filename,
                status="processing",
                message="Document uploaded successfully and is being processed"
            )
        else:
            # Fallback: If Inngest is not configured, process synchronously
            from backend.app.services.document_processor import DocumentProcessor
            
            processor = DocumentProcessor(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            
            chunks = processor.process_document(file_path, document_id, file.filename)
            vector_store.add_documents(chunks)
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return DocumentUploadResponse(
                document_id=document_id,
                filename=file.filename,
                status="completed",
                message="Document processed successfully (synchronous mode)"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG.
    
    Args:
        request: Query request with search parameters
        
    Returns:
        Query response with answer and sources
    """
    try:
        # Search for relevant documents
        documents = vector_store.search(
            query=request.query,
            top_k=request.top_k
        )
        
        if not documents:
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found. Please upload documents first."
            )
        
        # Generate answer using RAG
        result = rag_service.generate_answer(
            query=request.query,
            context_documents=documents
        )
        
        # Format sources
        sources = [
            DocumentChunk(
                content=doc["content"],
                metadata=doc["metadata"],
                score=doc.get("score")
            )
            for doc in result["sources"]
        ]
        
        return QueryResponse(
            query=request.query,
            answer=result["answer"],
            sources=sources,
            processing_time=result["processing_time"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Event-Driven RAG Document Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload",
            "query": "/query"
        }
    }
