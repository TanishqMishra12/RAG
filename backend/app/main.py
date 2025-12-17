"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inngest.fast_api import serve

from backend.app.api.routes import router
from backend.app.config import get_settings
from backend.app.services.inngest_service import inngest_client, process_document_function

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Event-Driven RAG Document Assistant",
    description="A robust RAG application with event-driven document processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Serve Inngest functions
serve(
    app,
    inngest_client,
    [process_document_function]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    )
