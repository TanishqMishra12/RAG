"""RAG service for query answering using retrieved context."""
from typing import List, Dict
from openai import OpenAI
import time


class RAGService:
    """Service for Retrieval-Augmented Generation."""
    
    def __init__(
        self,
        openai_api_key: str,
        model: str = "gpt-4-turbo-preview"
    ):
        """Initialize RAG service.
        
        Args:
            openai_api_key: OpenAI API key
            model: Chat model to use
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
    
    def generate_answer(
        self,
        query: str,
        context_documents: List[Dict]
    ) -> Dict:
        """Generate answer using retrieved context.
        
        Args:
            query: User query
            context_documents: Retrieved context documents
            
        Returns:
            Dict with answer and metadata
        """
        start_time = time.time()
        
        # Build context from documents
        context = self._build_context(context_documents)
        
        # Create prompt
        prompt = self._create_prompt(query, context)
        
        # Generate answer
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided context. "
                               "Always cite information from the context when answering. "
                               "If the context doesn't contain enough information to answer the question, "
                               "say so clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        processing_time = time.time() - start_time
        
        return {
            "answer": answer,
            "processing_time": processing_time,
            "sources": context_documents
        }
    
    def _build_context(self, documents: List[Dict]) -> str:
        """Build context string from documents.
        
        Args:
            documents: List of document chunks
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            filename = metadata.get("filename", "Unknown")
            
            context_parts.append(
                f"[Source {i} - {filename}]\n{content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create prompt for the LLM.
        
        Args:
            query: User query
            context: Context from retrieved documents
            
        Returns:
            Formatted prompt
        """
        return f"""Context from documents:

{context}

---

Question: {query}

Please provide a comprehensive answer based on the context above. If the context doesn't contain relevant information, please state that clearly."""
