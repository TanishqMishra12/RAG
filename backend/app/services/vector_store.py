"""Vector store service for Qdrant integration."""
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import uuid


class VectorStore:
    """Service for managing vector embeddings in Qdrant."""
    
    def __init__(
        self,
        host: str,
        port: int,
        collection_name: str,
        openai_api_key: str,
        embedding_model: str = "text-embedding-3-small"
    ):
        """Initialize vector store.
        
        Args:
            host: Qdrant host
            port: Qdrant port
            collection_name: Name of the collection
            openai_api_key: OpenAI API key
            embedding_model: OpenAI embedding model to use
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.embedding_model = embedding_model
        self.embedding_dimension = 1536  # text-embedding-3-small dimension
        
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def add_documents(self, chunks: List[Dict]) -> List[str]:
        """Add document chunks to vector store.
        
        Args:
            chunks: List of document chunks with content and metadata
            
        Returns:
            List of point IDs
        """
        points = []
        point_ids = []
        
        for chunk in chunks:
            # Generate embedding
            embedding = self.generate_embedding(chunk["content"])
            
            # Create unique point ID
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk["content"],
                    **chunk["metadata"]
                }
            )
            points.append(point)
        
        # Upload points in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
        
        return point_ids
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of matching documents with scores
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        # Format results
        documents = []
        for result in results:
            documents.append({
                "content": result.payload.get("content", ""),
                "metadata": {
                    k: v for k, v in result.payload.items() 
                    if k != "content"
                },
                "score": result.score
            })
        
        return documents
    
    def delete_by_document_id(self, document_id: str):
        """Delete all chunks for a document.
        
        Args:
            document_id: Document ID to delete
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={
                "filter": {
                    "must": [
                        {
                            "key": "document_id",
                            "match": {"value": document_id}
                        }
                    ]
                }
            }
        )
    
    def health_check(self) -> bool:
        """Check if Qdrant is accessible.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False
