"""Pydantic models for request/response schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    document_id: str
    filename: str
    status: str
    message: str


class QueryRequest(BaseModel):
    """Request model for querying documents."""
    query: str = Field(..., min_length=1, description="The query to search for")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")


class DocumentChunk(BaseModel):
    """Model for a document chunk."""
    content: str
    metadata: dict
    score: Optional[float] = None


class QueryResponse(BaseModel):
    """Response model for document queries."""
    query: str
    answer: str
    sources: List[DocumentChunk]
    processing_time: float


class DocumentStatus(BaseModel):
    """Model for document processing status."""
    document_id: str
    filename: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    qdrant_connected: bool
    timestamp: datetime
