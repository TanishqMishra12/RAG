"""Streamlit frontend for the RAG Document Assistant."""
import streamlit as st
import requests
import time
from typing import Optional

# Configuration
BACKEND_URL = "http://localhost:8000/api"

# Page config
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide"
)


def check_backend_health() -> bool:
    """Check if backend is healthy."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("qdrant_connected", False)
    except Exception:
        return False


def upload_document(file) -> Optional[dict]:
    """Upload a document to the backend."""
    try:
        files = {"file": (file.name, file, "application/pdf")}
        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")
        return None


def query_documents(query: str, top_k: int = 5) -> Optional[dict]:
    """Query documents."""
    try:
        payload = {"query": query, "top_k": top_k}
        response = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error querying documents: {str(e)}")
        return None


def main():
    """Main application."""
    
    # Header
    st.title("📚 Event-Driven RAG Document Assistant")
    st.markdown("Upload PDF documents and ask questions using AI-powered retrieval")
    
    # Sidebar
    with st.sidebar:
        st.header("System Status")
        
        # Health check
        if check_backend_health():
            st.success("✅ Backend Connected")
            st.success("✅ Qdrant Connected")
        else:
            st.error("❌ Backend or Qdrant Unavailable")
            st.warning("Please ensure the backend is running and Qdrant is accessible")
        
        st.divider()
        
        st.header("About")
        st.markdown("""
        This RAG application features:
        - 🚀 **Event-driven** processing with Inngest
        - 📄 **PDF** document support
        - 🔍 **Semantic search** with Qdrant
        - 🤖 **AI-powered** answers with OpenAI
        - ⚡ **Async processing** for responsiveness
        """)
    
    # Main content
    tab1, tab2 = st.tabs(["📤 Upload Documents", "💬 Query Documents"])
    
    # Upload tab
    with tab1:
        st.header("Upload PDF Documents")
        st.markdown("Upload your PDF documents to add them to the knowledge base")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Only PDF files are supported"
        )
        
        if uploaded_file is not None:
            st.info(f"📄 Selected: **{uploaded_file.name}**")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🚀 Upload & Process", type="primary"):
                    with st.spinner("Uploading document..."):
                        result = upload_document(uploaded_file)
                        
                        if result:
                            st.success(f"✅ {result.get('message', 'Upload successful')}")
                            st.json({
                                "Document ID": result.get("document_id"),
                                "Filename": result.get("filename"),
                                "Status": result.get("status")
                            })
                            
                            if result.get("status") == "processing":
                                st.info("⏳ Document is being processed asynchronously. You can query it shortly.")
    
    # Query tab
    with tab2:
        st.header("Query Your Documents")
        st.markdown("Ask questions about your uploaded documents")
        
        # Query input
        query = st.text_area(
            "Enter your question:",
            height=100,
            placeholder="What is the main topic of the document?",
            help="Ask any question about your uploaded documents"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            top_k = st.number_input(
                "Number of sources",
                min_value=1,
                max_value=10,
                value=5,
                help="Number of document chunks to retrieve"
            )
        
        if st.button("🔍 Search", type="primary", disabled=not query):
            if query:
                with st.spinner("Searching and generating answer..."):
                    start_time = time.time()
                    result = query_documents(query, top_k)
                    elapsed_time = time.time() - start_time
                    
                    if result:
                        # Display answer
                        st.subheader("💡 Answer")
                        st.markdown(result.get("answer", "No answer generated"))
                        
                        # Display metadata
                        st.divider()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Processing Time", f"{result.get('processing_time', 0):.2f}s")
                        with col2:
                            st.metric("Sources Retrieved", len(result.get("sources", [])))
                        
                        # Display sources
                        st.subheader("📚 Sources")
                        sources = result.get("sources", [])
                        
                        if sources:
                            for i, source in enumerate(sources, 1):
                                with st.expander(f"Source {i} - {source['metadata'].get('filename', 'Unknown')} (Score: {source.get('score', 0):.4f})"):
                                    st.markdown(f"**Content:**")
                                    st.text(source.get("content", ""))
                                    st.markdown(f"**Metadata:**")
                                    st.json(source.get("metadata", {}))
                        else:
                            st.warning("No sources found")


if __name__ == "__main__":
    main()
