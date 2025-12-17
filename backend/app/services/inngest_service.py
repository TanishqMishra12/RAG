"""Inngest service for event-driven document processing."""
import os
from inngest import Inngest
from inngest.function import InngestFunction
from typing import Dict, Any
from backend.app.config import get_settings
from backend.app.services.document_processor import DocumentProcessor
from backend.app.services.vector_store import VectorStore

# Initialize Inngest client
settings = get_settings()
inngest_client = Inngest(
    app_id="rag-document-assistant",
    event_key=settings.inngest_event_key if settings.inngest_event_key else None,
    is_production=bool(settings.inngest_event_key)
)


# Document processing function
@inngest_client.create_function(
    fn_id="process-document",
    trigger=inngest_client.event("document/uploaded")
)
async def process_document_function(
    ctx: Any,
    step: Any
) -> Dict[str, Any]:
    """Process uploaded document asynchronously.
    
    Args:
        ctx: Inngest context
        step: Inngest step for workflow orchestration
        
    Returns:
        Processing result
    """
    event_data = ctx.event.data
    
    document_id = event_data.get("document_id")
    file_path = event_data.get("file_path")
    filename = event_data.get("filename")
    
    try:
        # Step 1: Process document
        processor = DocumentProcessor(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        chunks = await step.run(
            "process-pdf",
            lambda: processor.process_document(file_path, document_id, filename)
        )
        
        # Step 2: Store in vector database
        vector_store = VectorStore(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            collection_name=settings.qdrant_collection_name,
            openai_api_key=settings.openai_api_key,
            embedding_model=settings.embedding_model
        )
        
        point_ids = await step.run(
            "store-embeddings",
            lambda: vector_store.add_documents(chunks)
        )
        
        # Step 3: Clean up file
        await step.run(
            "cleanup",
            lambda: os.remove(file_path) if os.path.exists(file_path) else None
        )
        
        return {
            "success": True,
            "document_id": document_id,
            "chunks_processed": len(chunks),
            "point_ids": point_ids
        }
        
    except Exception as e:
        return {
            "success": False,
            "document_id": document_id,
            "error": str(e)
        }


def send_document_event(document_id: str, file_path: str, filename: str) -> Dict:
    """Send document processing event to Inngest.
    
    Args:
        document_id: Unique document identifier
        file_path: Path to the uploaded file
        filename: Original filename
        
    Returns:
        Event dispatch result
    """
    try:
        result = inngest_client.send(
            {
                "name": "document/uploaded",
                "data": {
                    "document_id": document_id,
                    "file_path": file_path,
                    "filename": filename
                }
            }
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
